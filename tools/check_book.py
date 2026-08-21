#!/usr/bin/env python3
"""Validate the Hermes Agent Masterclass manuscript during drafting and release."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml


REQUIRED_CHAPTER_SECTIONS = (
    "## Opening scenario",
    "## Definitions",
    "## Hermes in practice",
    "## Professional example",
    "## Personal example",
    "## Authority boundaries",
    "## Failure modes and recovery",
    "## Field kit",
    "## Exercise",
    "## Answer or rubric",
    "## Mastery checklist",
    "## References",
)
EXPECTED_CHAPTER_PATHS = (
    "docs/part-1/01-meet-hermes.md",
    "docs/part-1/02-agentic-ai-first-principles.md",
    "docs/part-1/03-hermes-loop.md",
    "docs/part-1/04-write-the-job-description.md",
    "docs/part-2/05-install-hermes-on-mac-mini.md",
    "docs/part-2/06-models-and-routing.md",
    "docs/part-2/07-personality-context-sessions-memory.md",
    "docs/part-2/08-tools-skills-plugins-mcp.md",
    "docs/part-2/09-message-hermes-everywhere.md",
    "docs/part-2/10-goals-and-background-operations.md",
    "docs/part-3/11-family-safe-security.md",
    "docs/part-3/12-identities-burner-accounts-secrets.md",
    "docs/part-3/13-approvals-autonomy-egress-audit.md",
    "docs/part-3/14-sensitive-data-backups-recovery.md",
    "docs/part-4/15-daily-weekly-operating-rhythms.md",
    "docs/part-4/16-job-search-opportunity-pipeline.md",
    "docs/part-4/17-resume-interview-brand.md",
    "docs/part-4/18-family-operations-canada.md",
    "docs/part-5/19-one-two-person-business-os.md",
    "docs/part-5/20-business-functions.md",
    "docs/part-5/21-hermes-as-manager.md",
    "docs/part-6/22-evaluation-observability-capstone.md",
)
EXPECTED_APPENDIX_PATHS = (
    "docs/appendices/appendix-a-command-reference.md",
    "docs/appendices/appendix-b-templates-playbooks.md",
    "docs/appendices/appendix-c-curated-stack.md",
    "docs/appendices/appendix-d-troubleshooting-glossary-bibliography.md",
)
PLACEHOLDER_PATTERN = re.compile(r"\b(TODO|TBD|FIXME)\b")
LOCAL_LINK_PATTERN = re.compile(r"!?(?:\[[^\]]*\])\(([^)\s]+)(?:\s+['\"][^)]*['\"])?\)")
HTML_ASSET_PATTERN = re.compile(r"<(?:img|source)\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)
SECRET_PATTERNS = (
    ("OPENAI_API_KEY", re.compile(r"\bOPENAI_API_KEY\s*=")),
    ("Anthropic API key", re.compile(r"\bANTHROPIC_API_KEY\s*=")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("OpenAI key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--final", action="store_true", help="enforce the release manuscript contract")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="book root (default: current directory)")
    return parser.parse_args()


def load_manifest(root: Path, failures: list[str]) -> dict[str, object]:
    manifest_path = root / "book-manifest.yml"
    if not manifest_path.is_file():
        failures.append("missing manifest: book-manifest.yml")
        return {"chapters": [], "appendices": []}
    try:
        loaded = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        failures.append(f"invalid manifest YAML: {error}")
        return {"chapters": [], "appendices": []}
    if not isinstance(loaded, dict):
        failures.append("invalid manifest: expected a mapping")
        return {"chapters": [], "appendices": []}
    return loaded


def manifest_paths(entries: object, key: str) -> list[str]:
    if not isinstance(entries, list):
        return []
    return [entry[key] for entry in entries if isinstance(entry, dict) and isinstance(entry.get(key), str)]


def validate_manifest(manifest: dict[str, object], final: bool, failures: list[str]) -> tuple[list[str], list[str]]:
    chapters = manifest.get("chapters", [])
    appendices = manifest.get("appendices", [])
    if not isinstance(chapters, list):
        failures.append("invalid manifest: chapters must be a list")
        chapters = []
    if not isinstance(appendices, list):
        failures.append("invalid manifest: appendices must be a list")
        appendices = []

    numbers = [entry.get("number") for entry in chapters if isinstance(entry, dict)]
    for number in sorted({number for number in numbers if numbers.count(number) > 1}, key=str):
        failures.append(f"duplicate chapter number: {number}")
    chapter_paths = manifest_paths(chapters, "path")
    appendix_paths = manifest_paths(appendices, "path")

    if final:
        if numbers != list(range(1, 23)):
            failures.append("invalid chapter order: expected chapter numbers 1 through 22")
        if chapter_paths != list(EXPECTED_CHAPTER_PATHS):
            failures.append("invalid chapter paths or order: expected canonical 22-chapter manifest")
        if appendix_paths != list(EXPECTED_APPENDIX_PATHS):
            failures.append("invalid appendix paths or order: expected canonical appendices A through D")
    return chapter_paths, appendix_paths


def relative_path(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def local_target_exists(root: Path, source: Path, target: str) -> bool:
    parsed = urlparse(target)
    if parsed.scheme or target.startswith("//") or target.startswith("#"):
        return True
    target_path = unquote(parsed.path)
    if not target_path:
        return True
    destination = root / target_path.lstrip("/") if target_path.startswith("/") else source.parent / target_path
    return destination.exists()


def validate_links(root: Path, path: Path, content: str, failures: list[str]) -> None:
    rel_path = relative_path(root, path)
    for target in LOCAL_LINK_PATTERN.findall(content):
        if local_target_exists(root, path, target):
            continue
        label = "missing local asset" if target.lower().split("?", 1)[0].endswith((".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".pdf")) else "broken local link"
        failures.append(f"{label}: {rel_path}: {target}")
    for target in HTML_ASSET_PATTERN.findall(content):
        if not local_target_exists(root, path, target):
            failures.append(f"missing local asset: {rel_path}: {target}")


def markdown_words(content: str) -> int:
    without_code = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    return len(re.findall(r"\b[\w][\w’'/-]*\b", without_code))


def validate_file(root: Path, path: Path, final: bool, is_chapter: bool, failures: list[str]) -> int:
    content = path.read_text(encoding="utf-8")
    rel_path = relative_path(root, path)
    for marker in PLACEHOLDER_PATTERN.findall(content):
        failures.append(f"unresolved marker {marker}: {rel_path}")
    if "GPT-5.6 Soul".casefold() in content.casefold():
        failures.append(f"prohibited product term: GPT-5.6 Soul: {rel_path}")
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(content):
            failures.append(f"possible secret: {rel_path}: {label}")
    validate_links(root, path, content, failures)
    if is_chapter:
        for section in REQUIRED_CHAPTER_SECTIONS:
            if section not in content:
                failures.append(f"missing required section: {rel_path}: {section}")
        if final and "```mermaid" not in content:
            failures.append(f"missing Mermaid block: {rel_path}")
        if final:
            references = content.split("## References", maxsplit=1)
            if len(references) == 1 or not re.search(r"https?://", references[1]):
                failures.append(f"missing reference URL: {rel_path}")
            if "Verified against Hermes Agent v0.20.5 (2026-08-19)." not in content:
                failures.append(f"missing version label: {rel_path}")
    return markdown_words(content)


def validate_provenance(root: Path, failures: list[str]) -> None:
    provenance = root / "docs/assets/images/PROVENANCE.md"
    if not provenance.is_file():
        failures.append("missing screenshot provenance: docs/assets/images/PROVENANCE.md")
        return
    content = provenance.read_text(encoding="utf-8")
    for asset in sorted((root / "docs/assets/images/hermes").glob("*")) if (root / "docs/assets/images/hermes").exists() else []:
        if asset.is_file() and asset.name not in content:
            failures.append(f"missing screenshot provenance entry: docs/assets/images/hermes/{asset.name}")


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    failures: list[str] = []
    manifest = load_manifest(root, failures)
    chapter_paths, appendix_paths = validate_manifest(manifest, args.final, failures)

    all_paths = chapter_paths + appendix_paths
    words = 0
    existing_files = 0
    for index, rel_path in enumerate(all_paths):
        path = root / rel_path
        is_chapter = index < len(chapter_paths)
        if not path.is_file():
            if args.final:
                kind = "chapter" if is_chapter else "appendix"
                failures.append(f"missing {kind}: {rel_path}")
            continue
        existing_files += 1
        words += validate_file(root, path, args.final, is_chapter, failures)

    if args.final:
        actual_chapter_paths = sorted(
            relative_path(root, path) for path in root.glob("docs/part-*/*.md")
        )
        actual_appendix_paths = sorted(
            relative_path(root, path) for path in root.glob("docs/appendices/*.md")
        )
        if len(actual_chapter_paths) != 22:
            failures.append(f"wrong chapter file count: expected 22, found {len(actual_chapter_paths)}")
        if len(actual_appendix_paths) != 4:
            failures.append(f"wrong appendix file count: expected 4, found {len(actual_appendix_paths)}")
        for rel_path in sorted(set(actual_chapter_paths) - set(EXPECTED_CHAPTER_PATHS)):
            failures.append(f"unexpected chapter: {rel_path}")
        for rel_path in sorted(set(actual_appendix_paths) - set(EXPECTED_APPENDIX_PATHS)):
            failures.append(f"unexpected appendix: {rel_path}")
        if not 100_000 <= words <= 120_000:
            failures.append(f"word count out of range: 100000–120000 (found {words})")
        validate_provenance(root, failures)

    for failure in failures:
        print(f"ERROR: {failure}")
    status = "OK" if not failures else "FAILED"
    print(f"check_book: {status} — {existing_files} files, {words} words")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
