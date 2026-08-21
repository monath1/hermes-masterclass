#!/usr/bin/env python3
"""Validate offline-site and reproducible-release policy."""

from __future__ import annotations

import argparse
import hashlib
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ACTION_PATTERN = re.compile(r"^\s*-\s+uses:\s+([^\s#]+)(?:\s+#\s*(\S.*))?$", re.MULTILINE)
PINNED_ACTION_PATTERN = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")
REMOTE_PATTERN = re.compile(r"^(?:https?:)?//", re.IGNORECASE)
MERMAID_VERSION = "10.4.0"
MERMAID_SHA256 = "2cf7bb6cdc4a6ea96da3d324a4447d8300d1da703ce5f31311608642c0f86269"
MERMAID_LICENSE_SHA256 = "ec9fb67dcb25eccc416ed56e1aab819222c805a2a4bfe4cb19e7556bf2ffde80"
MERMAID_ARCHIVE_SHA256 = "91cb14dc936d0234aa37122c7f28d62d132eb5e09392082ef876d5eaf492ce08"
LOCAL_MERMAID = f"assets/vendor/mermaid/{MERMAID_VERSION}/mermaid.min.js"
LOCAL_INIT = "javascripts/mermaid-init.js"
FONT_ASSETS = {
    "docs/assets/vendor/fonts/newsreader/5.3.0/newsreader-latin-wght-normal.woff2": "62981321d9a3cc7a61a73792729043703fd6112da86e8ec848bb57f088578757",
    "docs/assets/vendor/fonts/newsreader/5.3.0/newsreader-latin-wght-italic.woff2": "48bc8861b9b2ca9300747cad4fd6a3b4ac3028d364df00bd1b72097baa75e509",
    "docs/assets/vendor/fonts/newsreader/5.3.0/LICENSE": "26028ec4e13b650065fa525a09532176f8a668b76ff849ea01c564a7480f91e7",
    "docs/assets/vendor/fonts/space-grotesk/5.3.0/space-grotesk-latin-wght-normal.woff2": "0640890476fc1198ab4de571fb658de443c4d85b66466ec09534a8737ab1ce9d",
    "docs/assets/vendor/fonts/space-grotesk/5.3.0/LICENSE": "18a4de52385f6b988782639d5d0cc1326e5a8c2de9a7f01d7b20d9aedcc60943",
    "docs/assets/vendor/fonts/jetbrains-mono/5.3.0/jetbrains-mono-latin-wght-normal.woff2": "18be452724bfdc236c074ca94a249a7f41a86752c7d04ab258ce9ed5651f6a7e",
    "docs/assets/vendor/fonts/jetbrains-mono/5.3.0/jetbrains-mono-latin-wght-italic.woff2": "a8afa085e9ca5e53434e2ee918ba6b65c7dd4dda56509976b36591478c99d62e",
    "docs/assets/vendor/fonts/jetbrains-mono/5.3.0/LICENSE": "403581b69dac5cff4079205e01c6b467e56af449ecbd7247693ddb1baafa005b",
}
REQUIRED_RELEASE_TOKENS = (
    "--require-hashes",
    "requirements.lock",
    '"$VERIFY_VENV/bin/pytest" -q',
    "check_book.py --final",
    "check_task${audit}.py",
    '"$VERIFY_VENV/bin/mkdocs" build --strict',
    "markdownlint-cli2@$MARKDOWNLINT_VERSION",
    "0.24.2",
    r"^https://github\.com/monath1/hermes-masterclass$",
    "codespell",
    "docs/assets/vendor/mermaid/10.4.0/mermaid.min.js",
    "py_compile",
    "check_offline_site.py",
    "git diff --check",
    "v2026.8.19",
    "fcbd1076a93841fa88855acce810e342a5b78101",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read(path: Path, failures: list[str], label: str) -> str:
    if not path.is_file():
        failures.append(f"missing {label}: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def check_mkdocs(root: Path, failures: list[str]) -> None:
    config = read(root / "mkdocs.yml", failures, "MkDocs configuration")
    if not re.search(r"(?m)^\s{2}font:\s+false\s*$", config):
        failures.append("Material fonts must be disabled with theme.font: false")
    if "mermaid2" in config or "unpkg.com" in config:
        failures.append("remote or plugin-provided Mermaid runtime is forbidden")
    if LOCAL_MERMAID not in config or LOCAL_INIT not in config:
        failures.append("MkDocs must load the pinned Mermaid bundle and local initializer")
    for token in (
        "custom_dir: overrides",
        "stylesheets/fonts.css",
        "site_author: Moumita Nath",
        "repo_url: https://github.com/monath1/hermes-masterclass",
        "link: https://github.com/monath1",
        "link: https://github.com/monath1/hermes-masterclass",
    ):
        if token not in config:
            failures.append(f"editorial identity/theme configuration is missing: {token}")
    exclude_match = re.search(r"(?ms)^exclude_docs:\s*\|\n(?P<body>(?:\s+.*\n?)*)", config)
    if exclude_match and "assets/images/PROVENANCE.md" in exclude_match.group("body"):
        failures.append("image provenance must be built as an unlisted reachable page")

    requirements = read(root / "requirements.txt", failures, "human-readable requirements")
    if "mkdocs-mermaid2-plugin" in requirements:
        failures.append("mkdocs-mermaid2-plugin must not inject a remote runtime")


def check_actions(root: Path, failures: list[str]) -> None:
    workflow = read(
        root / ".github/workflows/quality.yml", failures, "quality workflow"
    )
    actions = list(ACTION_PATTERN.finditer(workflow))
    if not actions:
        failures.append("quality workflow contains no GitHub Actions")
    for match in actions:
        action = match.group(1)
        comment = match.group(2)
        if not PINNED_ACTION_PATTERN.fullmatch(action):
            failures.append(
                f"GitHub Action is not pinned to a 40-character commit: {action}"
            )
        if not comment or not re.search(r"\bv\d", comment):
            failures.append(f"GitHub Action pin lacks a version comment: {action}")
        if action.startswith("actions/checkout@"):
            block_end = min(
                (
                    candidate.start()
                    for candidate in actions
                    if candidate.start() > match.start()
                ),
                default=len(workflow),
            )
            block = workflow[match.start() : block_end]
            if not re.search(r"(?m)^\s+persist-credentials:\s+false\s*$", block):
                failures.append("checkout must set persist-credentials: false")
    if re.search(r"persist-credentials:\s+true", workflow):
        failures.append("checkout credentials must never persist")
    if "bash tools/verify_release.sh" not in workflow:
        failures.append("quality workflow must call tools/verify_release.sh")


def requirement_blocks(lock: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    for line in lock.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line[:1].isspace():
            if current:
                current.append(stripped)
            continue
        if current:
            blocks.append(" ".join(current))
        current = [stripped]
    if current:
        blocks.append(" ".join(current))
    return blocks


def check_lock_and_verifier(root: Path, failures: list[str]) -> None:
    lock = read(root / "requirements.lock", failures, "hashed requirements lock")
    blocks = requirement_blocks(lock)
    if not blocks:
        failures.append("requirements.lock contains no pinned packages")
    for block in blocks:
        requirement = block.split("\\", 1)[0].strip()
        if "==" not in requirement or "--hash=sha256:" not in block:
            failures.append(f"unhashed or unpinned requirement: {requirement}")

    verifier_path = root / "tools/verify_release.sh"
    verifier = read(verifier_path, failures, "release verifier")
    if "--require-hashes" not in verifier or "requirements.lock" not in verifier:
        failures.append(
            "release verifier must install requirements.lock with --require-hashes"
        )
    for token in REQUIRED_RELEASE_TOKENS:
        if token not in verifier:
            failures.append(f"release verifier is missing required command token: {token}")
    common_match = re.search(r"(?ms)^lychee_common=\((.*?)^\)", verifier)
    common_excludes_site = bool(
        common_match
        and re.search(
            r"--exclude-path\s+['\"]?site(?:['\"]?|/)", common_match.group(1)
        )
    ) or bool(
        re.search(
            r"(?m)^lychee_common=\([^\n]*--exclude-path\s+['\"]?site(?:['\"]?|/)",
            verifier,
        )
    )
    if common_excludes_site:
        failures.append("Lychee common options must not exclude the built site")
    if not re.search(
        r'"\$lychee_bin"\s+"\$\{lychee_common\[@\]\}"\s+'
        r"--root-dir\s+site\s+'site/\*\*/\*\.html'",
        verifier,
    ):
        failures.append("release verifier must link-check built site HTML from site root")
    if verifier_path.is_file() and not verifier_path.stat().st_mode & 0o111:
        failures.append("tools/verify_release.sh must be executable")

    for relative in ("README.md", "CONTRIBUTING.md", "docs/index.md"):
        path = root / relative
        if not path.is_file():
            continue
        contents = path.read_text(encoding="utf-8")
        if re.search(r"pip install\s+-r\s+requirements\.txt", contents):
            failures.append(f"unlocked install documentation: {relative}")


def check_vendor(root: Path, failures: list[str]) -> None:
    attributes = read(root / ".gitattributes", failures, "Git attributes")
    whitespace_exclusions = [
        line.strip()
        for line in attributes.splitlines()
        if line.strip() and not line.lstrip().startswith("#") and "-whitespace" in line
    ]
    expected_whitespace_exclusion = (
        "docs/assets/vendor/mermaid/10.4.0/mermaid.min.js -whitespace"
    )
    if whitespace_exclusions != [expected_whitespace_exclusion]:
        failures.append(
            "Git whitespace exclusion must name only the exact vendored Mermaid bundle"
        )

    vendor_root = root / "docs/assets/vendor/mermaid"
    bundle = vendor_root / MERMAID_VERSION / "mermaid.min.js"
    license_path = vendor_root / MERMAID_VERSION / "LICENSE"
    provenance = read(vendor_root / "README.md", failures, "Mermaid provenance")
    for path, expected, label in (
        (bundle, MERMAID_SHA256, "Mermaid bundle"),
        (license_path, MERMAID_LICENSE_SHA256, "Mermaid license"),
    ):
        if not path.is_file():
            failures.append(f"missing {label}: {path}")
        elif sha256(path) != expected:
            failures.append(f"{label} hash mismatch: {path}")
    for token in (
        MERMAID_VERSION,
        "MIT",
        MERMAID_SHA256,
        MERMAID_LICENSE_SHA256,
        MERMAID_ARCHIVE_SHA256,
        "npm pack",
    ):
        if token not in provenance:
            failures.append(f"Mermaid provenance is missing: {token}")

    font_provenance = read(
        root / "docs/assets/vendor/fonts/README.md", failures, "font provenance"
    )
    for relative, expected in FONT_ASSETS.items():
        path = root / relative
        if not path.is_file():
            failures.append(f"missing vendored font asset: {relative}")
        elif sha256(path) != expected:
            failures.append(f"vendored font hash mismatch: {relative}")
        if expected not in font_provenance:
            failures.append(f"font provenance is missing hash: {expected}")
    for token in ("Newsreader", "Space Grotesk", "JetBrains Mono", "OFL", "npm pack"):
        if token not in font_provenance:
            failures.append(f"font provenance is missing: {token}")


class ResourceParser(HTMLParser):
    """Collect page-load resource attributes, excluding ordinary hyperlinks."""

    def __init__(self) -> None:
        super().__init__()
        self.resources: list[tuple[str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag == "script" and values.get("src"):
            self.resources.append((tag, "src", values["src"]))
        if tag == "link" and values.get("href"):
            rel = set(values.get("rel", "").lower().split())
            if rel & {
                "stylesheet",
                "preload",
                "modulepreload",
                "prefetch",
                "dns-prefetch",
                "preconnect",
                "icon",
            }:
                self.resources.append((tag, "href", values["href"]))
        for resource_tag, attribute in (
            ("img", "src"),
            ("source", "src"),
            ("video", "src"),
            ("audio", "src"),
            ("iframe", "src"),
        ):
            if tag == resource_tag and values.get(attribute):
                self.resources.append((tag, attribute, values[attribute]))


def check_site(site: Path, failures: list[str]) -> None:
    provenance = site / "assets/images/PROVENANCE/index.html"
    if not provenance.is_file():
        failures.append(
            "built provenance page is missing: assets/images/PROVENANCE/index.html"
        )

    appendix = site / "appendices/appendix-d-troubleshooting-glossary-bibliography/index.html"
    if appendix.is_file():
        appendix_html = appendix.read_text(encoding="utf-8")
        if "../../assets/images/PROVENANCE/" not in appendix_html:
            failures.append("Appendix D does not link to the built provenance page")

    raw_diagrams = 0
    for html_path in site.rglob("*.html"):
        contents = html_path.read_text(encoding="utf-8")
        raw_diagrams += len(re.findall(r'class="[^"]*\bmermaid\b', contents))
        parser = ResourceParser()
        parser.feed(contents)
        for tag, attribute, value in parser.resources:
            if REMOTE_PATTERN.match(value):
                failures.append(
                    f"external page-load resource in {html_path.relative_to(site)}: "
                    f"{tag}[{attribute}]={value}"
                )
    if raw_diagrams != 24:
        failures.append(f"built site must contain 24 Mermaid blocks; found {raw_diagrams}")

    for css_path in site.rglob("*.css"):
        contents = css_path.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r"(?:@import\s+|url\(\s*['\"]?)(https?:)?//", contents):
            failures.append(
                f"external CSS resource in {css_path.relative_to(site)} at byte {match.start()}"
            )

    for relative in (
        LOCAL_MERMAID,
        LOCAL_INIT,
        "stylesheets/fonts.css",
    ):
        if not (site / relative).is_file():
            failures.append(f"built local runtime is missing: {relative}")
    for relative in FONT_ASSETS:
        built_relative = relative.removeprefix("docs/")
        if not (site / built_relative).is_file():
            failures.append(f"built vendored font asset is missing: {built_relative}")

    index = site / "index.html"
    if index.is_file():
        home = index.read_text(encoding="utf-8")
        for token in (
            "Curated by",
            "Moumita Nath",
            "https://github.com/monath1",
            "https://github.com/monath1/hermes-masterclass",
        ):
            if token not in home:
                failures.append(f"built homepage identity is missing: {token}")


def check_repository(root: Path, site: Path | None = None) -> list[str]:
    failures: list[str] = []
    check_mkdocs(root, failures)
    check_actions(root, failures)
    check_lock_and_verifier(root, failures)
    check_vendor(root, failures)
    if site is not None:
        check_site(site, failures)
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--site", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    site = args.site.resolve() if args.site else None
    failures = check_repository(root, site)
    if failures:
        print("check_release: FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    suffix = " and built site" if site else ""
    print(f"check_release: OK — repository{suffix} policy verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
