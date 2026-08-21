#!/usr/bin/env python3
"""Audit the retained workflow, source, and state contracts in Chapters 15–16."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from check_book import markdown_words


PINNED_COMMIT = "fcbd1076a93841fa88855acce810e342a5b78101"
CHAPTERS = {
    "docs/part-4/15-daily-weekly-operating-rhythms.md": (4000, 4600),
    "docs/part-4/16-job-search-opportunity-pipeline.md": (4400, 5000),
}
REQUIRED_PINNED_PATHS = {
    "website/docs/guides/daily-briefing-bot.md",
    "website/docs/user-guide/features/browser.md",
    "website/docs/user-guide/features/cron.md",
    "website/docs/user-guide/features/document-extraction.md",
    "website/docs/user-guide/features/mcp.md",
    "website/docs/user-guide/features/skills.md",
    "website/docs/user-guide/features/tools.md",
    "website/docs/user-guide/features/web-search.md",
    "website/docs/user-guide/messaging/email.md",
    "website/docs/user-guide/profiles.md",
    "website/docs/user-guide/security.md",
    "website/docs/user-guide/skills/bundled/productivity/productivity-google-workspace.md",
    "website/docs/user-guide/skills/bundled/productivity/productivity-meeting-action-items.md",
    "website/docs/user-guide/skills/bundled/productivity/productivity-weekly-review-planning.md",
    "website/docs/user-guide/skills/bundled/productivity/productivity-xlsx.md",
    "website/docs/user-guide/skills/bundled/research/research-grounded-citations.md",
}
PINNED_SOURCE_ASSERTIONS = (
    ("website/docs/user-guide/features/web-search.md", "search the web and return ranked results"),
    ("website/docs/user-guide/features/web-search.md", "fetch and extract readable content"),
    (
        "website/docs/user-guide/features/browser.md",
        "For simple information retrieval, prefer `web_search` or `web_extract`",
    ),
    (
        "website/docs/user-guide/skills/bundled/productivity/productivity-google-workspace.md",
        "Never send email, create/delete calendar events",
    ),
    (
        "website/docs/user-guide/skills/bundled/productivity/productivity-weekly-review-planning.md",
        "Default to recommendations/drafts, not mutations",
    ),
    (
        "website/docs/user-guide/skills/bundled/productivity/productivity-meeting-action-items.md",
        "do not publish yet",
    ),
    ("website/docs/guides/daily-briefing-bot.md", "completely fresh session"),
    (
        "website/docs/user-guide/features/document-extraction.md",
        "PDF conversion reads the **text layer only**",
    ),
)
CHAPTER_15_STATES = {
    "captured",
    "accepted",
    "doing",
    "waiting",
    "blocked",
    "done",
    "cancelled",
    "superseded",
}
CHAPTER_16_STATES = {
    "discovered",
    "qualifying",
    "researching",
    "hold",
    "no-go",
    "preparing",
    "ready-for-review",
    "approved-to-submit",
    "submission-unknown",
    "submitted",
    "interviewing",
    "offer",
    "closed-or-unavailable",
    "closed",
    "withdrawn",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="book root")
    parser.add_argument(
        "--hermes-source",
        type=Path,
        help="optional pinned Hermes v2026.8.19 checkout for source verification",
    )
    return parser.parse_args()


def require(text: str, phrase: str, label: str, failures: list[str]) -> None:
    if phrase.casefold() not in text.casefold():
        failures.append(f"missing {label}: {phrase}")


def extract_state_vocabulary(text: str, label: str, failures: list[str]) -> set[str]:
    match = re.search(r"^- state: (?P<states>.+?);$", text, re.MULTILINE)
    if match is None:
        failures.append(f"missing canonical state vocabulary: {label}")
        return set()
    return set(re.findall(r"`([^`]+)`", match.group("states")))


def validate_source(source: Path, failures: list[str]) -> None:
    if not source.is_dir():
        failures.append(f"missing pinned Hermes source: {source}")
        return
    result = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or result.stdout.strip() != PINNED_COMMIT:
        failures.append(
            f"wrong pinned Hermes commit: expected {PINNED_COMMIT}, "
            f"found {result.stdout.strip() or 'unreadable'}"
        )
    for relative_path, phrase in PINNED_SOURCE_ASSERTIONS:
        path = source / relative_path
        if not path.is_file():
            failures.append(f"missing pinned source path: {relative_path}")
        elif phrase not in path.read_text(encoding="utf-8"):
            failures.append(f"missing pinned source assertion: {relative_path}: {phrase}")


def audit_task7(root: Path, hermes_source: Path | None = None) -> list[str]:
    failures: list[str] = []
    content: dict[str, str] = {}
    for relative_path, (minimum, maximum) in CHAPTERS.items():
        path = root / relative_path
        if not path.is_file():
            failures.append(f"missing chapter: {relative_path}")
            continue
        chapter = path.read_text(encoding="utf-8")
        content[relative_path] = chapter
        words = markdown_words(chapter)
        if not minimum <= words <= maximum:
            failures.append(
                f"word count out of range: {relative_path}: "
                f"{minimum}–{maximum} (found {words})"
            )
    if len(content) != len(CHAPTERS):
        return failures

    chapter_15 = content["docs/part-4/15-daily-weekly-operating-rhythms.md"]
    chapter_16 = content["docs/part-4/16-job-search-opportunity-pipeline.md"]
    combined = chapter_15 + "\n" + chapter_16

    for phrase in (
        "primary inbox is not transferred to Hermes",
        "Never connect the primary inbox",
        "Primary inbox triage stays human-led",
        "primary inboxes remain outside Hermes",
    ):
        require(chapter_15, phrase, "Chapter 15 primary-inbox exclusion", failures)
    for phrase in (
        "Native `web_search` and `web_extract`",
        "Bundled `weekly-review-planning`",
        "reviewed Hermes-compatible MCP server or custom integration",
        "Human reads it and copies the minimum needed",
    ):
        require(chapter_15, phrase, "Chapter 15 capability layer", failures)
    for phrase in (
        "**Unresolved field.**",
        "`unresolved` is a field value, not a ledger state",
        "must leave an unstated owner or date `unresolved`",
        "must supply it or explicitly confirm it from an identified source",
        "never invents a candidate owner or date for approval",
    ):
        require(chapter_15, phrase, "Chapter 15 unresolved-field control", failures)
    if "accepts unstated owners and deadlines" in chapter_15.casefold():
        failures.append("ambiguous Chapter 15 approval language: accepts unstated owners and deadlines")

    chapter_15_states = extract_state_vocabulary(chapter_15, "Chapter 15", failures)
    if chapter_15_states != CHAPTER_15_STATES:
        failures.append(
            "inconsistent Chapter 15 state vocabulary: expected "
            f"{sorted(CHAPTER_15_STATES)}, found {sorted(chapter_15_states)}"
        )

    for phrase in (
        "Job Bank's current seeker terms prohibit these",
        "LinkedIn's current agreement prohibits these methods",
        "Do not schedule Job Bank or LinkedIn access",
        "- **Native Hermes:**",
        "- **Bundled Hermes skills:**",
        "- **MCP or custom work:**",
        "- **Human/manual:**",
        "send bulk or deceptive outreach",
        "claim audit rejects",
        "exact submission packages",
        "prepares—not submits",
    ):
        require(chapter_16, phrase, "Chapter 16 ethical pipeline control", failures)

    chapter_16_states = extract_state_vocabulary(chapter_16, "Chapter 16", failures)
    if chapter_16_states != CHAPTER_16_STATES:
        failures.append(
            "inconsistent Chapter 16 state vocabulary: expected "
            f"{sorted(CHAPTER_16_STATES)}, found {sorted(chapter_16_states)}"
        )
    for phrase in (
        "`submission-unknown` cannot transition to any submission retry",
        "Priya resolves the state",
        "fresh exact submission approval",
    ):
        require(chapter_16, phrase, "Chapter 16 uncertain-submission control", failures)

    pinned_pattern = re.compile(
        r"https://github\.com/NousResearch/hermes-agent/blob/v2026\.8\.19/([^\s)#]+)"
    )
    linked_paths = set(pinned_pattern.findall(combined))
    for relative_path in sorted(REQUIRED_PINNED_PATHS - linked_paths):
        failures.append(f"missing pinned reference URL: {relative_path}")
    if hermes_source is not None:
        source = hermes_source.resolve()
        validate_source(source, failures)
        for relative_path in sorted(linked_paths):
            if not (source / relative_path).is_file():
                failures.append(f"pinned reference URL does not resolve: {relative_path}")

    return failures


def main() -> int:
    args = parse_args()
    failures = audit_task7(args.root.resolve(), args.hermes_source)
    for failure in failures:
        print(f"ERROR: {failure}")
    status = "OK" if not failures else "FAILED"
    source_status = "verified" if args.hermes_source else "reference paths checked"
    print(f"check_task7: {status} — {len(CHAPTERS)} chapters; pinned source {source_status}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
