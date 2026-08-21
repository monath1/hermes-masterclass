#!/usr/bin/env python3
"""Render every Mermaid page in network-denied Chromium and require non-empty SVGs."""

from __future__ import annotations

import argparse
import functools
import http.server
import json
import shutil
import subprocess
import tempfile
import threading
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

import websocket


CSP = (
    "default-src 'self' data:; "
    "connect-src 'self'; "
    "font-src 'self'; "
    "frame-src 'none'; "
    "img-src 'self' data:; "
    "object-src 'none'; "
    "script-src 'self' 'unsafe-inline'; "
    "style-src 'self' 'unsafe-inline'"
)
EXPECTED_DIAGRAMS = 24


class OfflineHandler(http.server.SimpleHTTPRequestHandler):
    """Serve the site with a self-only content policy and quiet request logging."""

    def end_headers(self) -> None:
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def log_message(self, format: str, *args: object) -> None:
        return


class DevToolsSession:
    """Minimal Chrome DevTools Protocol session with network request interception."""

    def __init__(self, endpoint: str, allowed_origin: str) -> None:
        self.socket = websocket.create_connection(
            endpoint, timeout=1, origin=allowed_origin, http_proxy_host=None
        )
        self.next_id = 1
        self.blocked: list[str] = []
        self.allowed_origin = allowed_origin

    def close(self) -> None:
        self.socket.close()

    def send(self, method: str, params: dict[str, object] | None = None) -> int:
        request_id = self.next_id
        self.next_id += 1
        self.socket.send(
            json.dumps({"id": request_id, "method": method, "params": params or {}})
        )
        return request_id

    def handle_event(self, message: dict[str, object]) -> None:
        if message.get("method") != "Fetch.requestPaused":
            return
        params = message.get("params", {})
        if not isinstance(params, dict):
            return
        request = params.get("request", {})
        if not isinstance(request, dict):
            return
        url = str(request.get("url", ""))
        parsed = urlparse(url)
        allowed = (
            url.startswith(self.allowed_origin)
            or parsed.scheme in {"about", "blob", "data"}
        )
        if allowed:
            self.send("Fetch.continueRequest", {"requestId": params["requestId"]})
        else:
            self.blocked.append(url)
            self.send(
                "Fetch.failRequest",
                {"requestId": params["requestId"], "errorReason": "BlockedByClient"},
            )

    def command(
        self,
        method: str,
        params: dict[str, object] | None = None,
        timeout: float = 10,
    ) -> dict[str, object]:
        request_id = self.send(method, params)
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                message = json.loads(self.socket.recv())
            except websocket.WebSocketTimeoutException:
                continue
            self.handle_event(message)
            if message.get("id") != request_id:
                continue
            if "error" in message:
                raise RuntimeError(f"CDP {method} failed: {message['error']}")
            result = message.get("result", {})
            return result if isinstance(result, dict) else {}
        raise TimeoutError(f"CDP command timed out: {method}")


def find_chrome(explicit: str | None) -> str:
    if explicit:
        path = Path(explicit)
        if path.is_file():
            return str(path)
        raise FileNotFoundError(f"Chrome executable does not exist: {path}")
    candidates = (
        shutil.which("google-chrome"),
        shutil.which("google-chrome-stable"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    )
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(candidate)
    raise FileNotFoundError("Chrome/Chromium is required for the offline diagram smoke test")


def page_url(relative: Path, origin: str) -> str:
    if relative.name == "index.html":
        suffix = relative.parent.as_posix().strip("/")
        path = f"/{suffix}/" if suffix else "/"
    else:
        path = f"/{relative.as_posix()}"
    return f"{origin}{path}"


def start_chrome(chrome: str, profile: Path, log: Path) -> tuple[subprocess.Popen[bytes], int]:
    command = [
        chrome,
        "--headless=new",
        "--disable-background-networking",
        "--disable-component-extensions-with-background-pages",
        "--disable-default-apps",
        "--disable-domain-reliability",
        "--disable-features=OptimizationHints,MediaRouter,Translate",
        "--disable-gpu",
        "--disable-sync",
        "--metrics-recording-only",
        "--no-first-run",
        "--remote-allow-origins=*",
        "--remote-debugging-port=0",
        "--safebrowsing-disable-auto-update",
        f"--user-data-dir={profile}",
        "about:blank",
    ]
    log_handle = log.open("wb")
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=log_handle)
    log_handle.close()
    port_file = profile / "DevToolsActivePort"
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Chrome exited before DevTools startup; see {log}")
        if port_file.is_file():
            return process, int(port_file.read_text(encoding="utf-8").splitlines()[0])
        time.sleep(0.05)
    process.terminate()
    raise TimeoutError(f"Chrome DevTools startup timed out; see {log}")


def page_endpoint(port: int) -> str:
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=1) as response:
                targets = json.load(response)
        except (OSError, ValueError):
            time.sleep(0.05)
            continue
        for target in targets:
            if target.get("type") == "page":
                return str(target["webSocketDebuggerUrl"])
        time.sleep(0.05)
    raise TimeoutError("Chrome page target was not available")


def inspect_diagrams(
    session: DevToolsSession, url: str, expected: int
) -> tuple[int, list[str], str]:
    session.command("Page.navigate", {"url": url})
    expression = """
(() => {
  const diagrams = [...document.querySelectorAll('.mermaid')];
  const drawing = 'path,rect,circle,ellipse,line,polygon,polyline,text';
  return {
    ready: document.documentElement.dataset.mermaidReady || '',
    count: diagrams.length,
    valid: diagrams.filter((node) =>
      node.dataset.processed === 'true' &&
      node.querySelector('svg') &&
      node.querySelector(`svg ${drawing}`)
    ).length,
    resources: performance.getEntriesByType('resource').map((entry) => entry.name)
    ,error: document.documentElement.dataset.mermaidError || ''
  };
})()
"""
    deadline = time.monotonic() + 12
    latest: dict[str, object] = {}
    while time.monotonic() < deadline:
        result = session.command(
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": True},
            timeout=2,
        )
        remote = result.get("result", {})
        if isinstance(remote, dict):
            value = remote.get("value", {})
            if isinstance(value, dict):
                latest = value
        if latest.get("ready") == "false":
            break
        if latest.get("count") == expected and latest.get("valid") == expected:
            break
        time.sleep(0.1)
    resources = [str(value) for value in latest.get("resources", [])]
    ready = str(latest.get("ready", ""))
    if latest.get("error"):
        ready = f"{ready}: {latest['error']}"
    return int(latest.get("valid", 0)), resources, ready


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=Path("site"))
    parser.add_argument("--chrome")
    args = parser.parse_args()
    site = args.site.resolve()
    if not site.is_dir():
        print(f"check_offline_site: FAILED — built site does not exist: {site}")
        return 1

    pages: list[tuple[Path, int]] = []
    for path in sorted(site.rglob("*.html")):
        contents = path.read_text(encoding="utf-8")
        count = contents.count('class="mermaid"')
        if count:
            pages.append((path.relative_to(site), count))
    expected_total = sum(count for _, count in pages)
    if expected_total != EXPECTED_DIAGRAMS:
        print(
            "check_offline_site: FAILED — expected "
            f"{EXPECTED_DIAGRAMS} Mermaid blocks, found {expected_total}"
        )
        return 1

    try:
        chrome = find_chrome(args.chrome)
    except FileNotFoundError as error:
        print(f"check_offline_site: FAILED — {error}")
        return 1

    handler = functools.partial(OfflineHandler, directory=str(site))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f"http://127.0.0.1:{server.server_port}"
    rendered = 0
    failures: list[str] = []
    process: subprocess.Popen[bytes] | None = None
    session: DevToolsSession | None = None
    try:
        with tempfile.TemporaryDirectory(prefix="hermes-offline-chrome-") as temp_root:
            temporary = Path(temp_root)
            process, port = start_chrome(chrome, temporary / "profile", temporary / "chrome.log")
            session = DevToolsSession(page_endpoint(port), origin)
            session.command("Page.enable")
            session.command("Network.enable")
            session.command("Fetch.enable", {"patterns": [{"urlPattern": "*"}]})
            for relative, expected in pages:
                url = page_url(relative, origin)
                valid, resources, ready = inspect_diagrams(session, url, expected)
                rendered += valid
                external = [resource for resource in resources if not resource.startswith(origin)]
                if valid != expected or ready != "true":
                    failures.append(
                        f"{relative}: expected {expected} non-empty SVGs, found {valid}; "
                        f"ready={ready or 'unset'}"
                    )
                if external:
                    failures.append(f"{relative}: external resource entries: {external}")
            if session.blocked:
                failures.append(f"attempted external requests were blocked: {session.blocked}")
    except (OSError, RuntimeError, TimeoutError, websocket.WebSocketException) as error:
        failures.append(str(error))
    finally:
        if session is not None:
            session.close()
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    if failures or rendered != EXPECTED_DIAGRAMS:
        print("check_offline_site: FAILED")
        for failure in failures:
            print(f"- {failure}")
        print(f"- rendered non-empty SVGs: {rendered}/{EXPECTED_DIAGRAMS}")
        return 1
    print(
        f"check_offline_site: OK — {rendered}/{EXPECTED_DIAGRAMS} non-empty SVG "
        f"diagrams across {len(pages)} pages; self-only CSP and CDP request blocking active"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
