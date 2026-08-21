#!/usr/bin/env python3
"""Audit Task 11 appendices against manuscript citations and pinned Hermes sources."""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
from dataclasses import dataclass
from io import StringIO
from pathlib import Path


PINNED_COMMIT = "fcbd1076a93841fa88855acce810e342a5b78101"
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
LEDGER_PATTERN = re.compile(
    r"^## Source and version ledger\s.*?^```csv\s*\n(.*?)^```",
    re.MULTILINE | re.DOTALL,
)
APPENDIX_PATHS = (
    Path("docs/appendices/appendix-a-command-reference.md"),
    Path("docs/appendices/appendix-b-templates-playbooks.md"),
    Path("docs/appendices/appendix-c-curated-stack.md"),
    Path("docs/appendices/appendix-d-troubleshooting-glossary-bibliography.md"),
)
VALID_VERSION_LABELS = {"Yes—pinned", "Yes—mutable", "No—stable"}


@dataclass(frozen=True)
class SourceUse:
    title: str
    affected: tuple[str, ...]


@dataclass(frozen=True)
class LedgerEntry:
    url: str
    title: str
    publisher: str
    verified: str
    affected: tuple[str, ...]
    version_sensitive: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--hermes-source", type=Path)
    return parser.parse_args()


def source_label(path: Path) -> str:
    if path.parts[1].startswith("part-"):
        return str(int(path.name.split("-", 1)[0]))
    return path.name.split("appendix-", 1)[1][0].upper()


def label_sort_key(label: str) -> tuple[int, int | str]:
    return (0, int(label)) if label.isdigit() else (1, label)


def without_ledger(text: str) -> str:
    match = re.search(
        r"^## Source and version ledger\s.*?(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return text[: match.start()] + text[match.end() :] if match else text


def collect_external_sources(root: Path) -> dict[str, SourceUse]:
    """Collect primary/external Markdown citations; local links and D's carrier ledger are out of scope."""
    titles: dict[str, str] = {}
    affected: dict[str, set[str]] = {}
    chapter_paths = tuple(
        path.relative_to(root) for path in sorted(root.glob("docs/part-*/*.md"))
    )
    for relative in chapter_paths + APPENDIX_PATHS:
        path = root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if relative == APPENDIX_PATHS[-1]:
            text = without_ledger(text)
        label = source_label(relative)
        for title, url in LINK_PATTERN.findall(text):
            titles.setdefault(url, re.sub(r"[`*_]", "", title).strip())
            affected.setdefault(url, set()).add(label)
    return {
        url: SourceUse(titles[url], tuple(sorted(labels, key=label_sort_key)))
        for url, labels in sorted(affected.items())
    }


def parse_source_ledger(text: str, failures: list[str]) -> dict[str, LedgerEntry]:
    match = LEDGER_PATTERN.search(text)
    if match is None:
        failures.append("missing source-ledger CSV block")
        return {}
    reader = csv.DictReader(StringIO(match.group(1)))
    required = ("url", "title", "publisher", "verified", "affected", "version_sensitive")
    if tuple(reader.fieldnames or ()) != required:
        failures.append("invalid source-ledger fields: expected " + ",".join(required))
        return {}
    entries: dict[str, LedgerEntry] = {}
    for row in reader:
        url = (row.get("url") or "").strip()
        if not url.startswith(("https://", "http://")):
            failures.append(f"invalid source-ledger URL: {url or '<blank>'}")
            continue
        if url in entries:
            failures.append(f"duplicate source-ledger URL: {url}")
            continue
        for field in ("title", "publisher", "verified", "affected", "version_sensitive"):
            if not (row.get(field) or "").strip():
                failures.append(f"missing source-ledger {field.replace('_', '-')}: {url}")
        verified = (row.get("verified") or "").strip()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", verified):
            failures.append(f"invalid source-ledger verification date: {url}")
        labels = tuple(label.strip() for label in (row.get("affected") or "").split(",") if label.strip())
        if not labels or any(
            not (label.isdigit() and 1 <= int(label) <= 22)
            and label not in {"A", "B", "C", "D"}
            for label in labels
        ):
            failures.append(f"invalid source-ledger affected value: {url}")
        version = (row.get("version_sensitive") or "").strip()
        if version not in VALID_VERSION_LABELS:
            failures.append(f"invalid source-ledger version-sensitive value: {url}")
        entries[url] = LedgerEntry(
            url=url,
            title=(row.get("title") or "").strip(),
            publisher=(row.get("publisher") or "").strip(),
            verified=verified,
            affected=labels,
            version_sensitive=version,
        )
    return entries


def validate_source_ledger(root: Path, failures: list[str]) -> int:
    expected = collect_external_sources(root)
    ledger_path = root / APPENDIX_PATHS[-1]
    if not ledger_path.is_file():
        failures.append(f"missing Appendix D: {APPENDIX_PATHS[-1]}")
        return len(expected)
    actual = parse_source_ledger(ledger_path.read_text(encoding="utf-8"), failures)
    for url in sorted(expected.keys() - actual.keys()):
        failures.append(f"missing source-ledger URL: {url}")
    for url in sorted(actual.keys() - expected.keys()):
        failures.append(f"source-ledger URL has no manuscript citation: {url}")
    for url in sorted(expected.keys() & actual.keys()):
        if actual[url].title != expected[url].title:
            failures.append(f"wrong source-ledger title: {url}: expected {expected[url].title}")
        if actual[url].affected != expected[url].affected:
            wanted = ", ".join(expected[url].affected)
            failures.append(f"wrong source-ledger mapping: {url}: expected {wanted}")
    return len(expected)


def git_text(source: Path, relative: str) -> str:
    path = source / relative
    if path.is_file():
        return path.read_text(encoding="utf-8")
    result = subprocess.run(
        ["git", "-C", str(source), "show", f"HEAD:{relative}"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout if result.returncode == 0 else ""


def table_code_values(text: str, start: str, end: str) -> list[str]:
    section = text.split(start, 1)[1].split(end, 1)[0]
    values: list[str] = []
    for line in section.splitlines():
        if line.startswith("|") and not line.startswith("| ---"):
            first_cell = line.split("|", 2)[1]
            values.extend(re.findall(r"`([^`]+)`", first_cell))
    return values


def command_signature(command: str) -> str:
    tokens = command.split()
    if not tokens:
        return command
    if tokens[0].startswith("/"):
        return tokens[0].rstrip(",")
    return " ".join(tokens[:2])


def validate_pinned_appendices(root: Path, source: Path, failures: list[str]) -> None:
    head = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if head != PINNED_COMMIT:
        failures.append(f"wrong pinned Hermes commit: expected {PINNED_COMMIT}")
        return

    appendix_a = (root / APPENDIX_PATHS[0]).read_text(encoding="utf-8")
    official_commands = "\n".join(
        git_text(source, path)
        for path in (
            "website/docs/reference/cli-commands.md",
            "website/docs/reference/slash-commands.md",
            "website/docs/reference/tools-reference.md",
        )
    )
    for line in appendix_a.splitlines():
        if not line.startswith(("| Terminal |", "| In chat |")):
            continue
        command_cell = line.split("|", 3)[2]
        for command in re.findall(r"`([^`]+)`", command_cell):
            signature = command_signature(command)
            tokens = signature.split()
            needle = tokens[1] if len(tokens) > 1 and tokens[1].startswith("-") else signature
            if needle not in official_commands:
                failures.append(f"unverified Appendix A command: {signature}")

    appendix_c = (root / APPENDIX_PATHS[2]).read_text(encoding="utf-8")
    official_skills = git_text(source, "website/docs/reference/skills-catalog.md") + git_text(
        source, "website/docs/reference/optional-skills-catalog.md"
    )
    for skill in table_code_values(appendix_c, "## Hermes-native skills", "## Hermes plugins"):
        for name in (part.strip() for part in skill.split(" and ")):
            if name and name not in official_skills:
                failures.append(f"unverified Appendix C skill: {name}")

    official_plugins = git_text(source, "website/docs/user-guide/features/built-in-plugins.md")
    for plugin in table_code_values(appendix_c, "## Hermes plugins", "## MCP categories and examples"):
        if plugin not in official_plugins:
            failures.append(f"unverified Appendix C plugin: {plugin}")

    manifest_paths = subprocess.run(
        ["git", "-C", str(source), "ls-tree", "-r", "--name-only", "HEAD", "optional-mcps"],
        check=False,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    official_mcps = {
        str(data.get("name"))
        for path in manifest_paths
        if path.endswith("/manifest.yaml")
        for data in [__import__("yaml").safe_load(git_text(source, path))]
        if isinstance(data, dict) and data.get("name")
    }
    mcp_section = appendix_c.split("## MCP categories and examples", 1)[1].split(
        "## Installation and review gate", 1
    )[0]
    for line in mcp_section.splitlines():
        if not line.startswith("|") or line.startswith("| ---"):
            continue
        first_cell = line.split("|", 2)[1]
        match = re.search(r"\[([^]]+)\]\(https?://", first_cell)
        if match is None:
            continue
        name = re.sub(r"\s+(?:MCP|bridge)$", "", match.group(1), flags=re.IGNORECASE).lower()
        if name not in official_mcps:
            failures.append(f"unverified Appendix C catalog MCP: {name}")


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    failures: list[str] = []
    count = validate_source_ledger(root, failures)
    if args.hermes_source is not None:
        validate_pinned_appendices(root, args.hermes_source.resolve(), failures)
    for failure in failures:
        print(f"ERROR: {failure}")
    status = "FAILED" if failures else "OK"
    print(f"check_task11: {status} — {count} external URLs")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
