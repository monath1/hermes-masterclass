#!/usr/bin/env python3
"""Audit the retained truth, advice, privacy, and source contracts in Chapters 17–18."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from check_book import markdown_words


PINNED_COMMIT = "fcbd1076a93841fa88855acce810e342a5b78101"
CHAPTERS = {
    "docs/part-4/17-resume-interview-brand.md": (4200, 4800),
    "docs/part-4/18-family-operations-canada.md": (4400, 5000),
}
REQUIRED_PINNED_PATHS = {
    "website/docs/user-guide/features/cron.md",
    "website/docs/user-guide/features/document-extraction.md",
    "website/docs/user-guide/features/memory.md",
    "website/docs/user-guide/features/tools.md",
    "website/docs/user-guide/features/voice-mode.md",
    "website/docs/user-guide/features/web-search.md",
    "website/docs/user-guide/messaging/email.md",
    "website/docs/user-guide/skills/bundled/productivity/productivity-docx.md",
    "website/docs/user-guide/skills/bundled/productivity/productivity-pdf.md",
    "website/docs/user-guide/skills/bundled/research/research-grounded-citations.md",
}
PINNED_SOURCE_ASSERTIONS = (
    (
        "website/docs/user-guide/features/document-extraction.md",
        "PDF conversion reads the **text layer only**",
    ),
    (
        "website/docs/user-guide/skills/bundled/productivity/productivity-docx.md",
        "**Verify** (always): re-read the output",
    ),
    (
        "website/docs/user-guide/skills/bundled/productivity/productivity-pdf.md",
        "Scanned (image-only) PDFs contain no text layer",
    ),
    (
        "website/docs/user-guide/features/voice-mode.md",
        "Press Ctrl+B",
    ),
    (
        "website/docs/user-guide/features/cron.md",
        "Cron jobs run in a completely fresh agent session",
    ),
    (
        "website/docs/user-guide/features/memory.md",
        "Raw data dumps",
    ),
    (
        "website/docs/user-guide/features/tools.md",
        "Search the web and extract page content",
    ),
    (
        "website/docs/user-guide/messaging/email.md",
        "A dedicated email account",
    ),
    (
        "website/docs/user-guide/skills/bundled/research/research-grounded-citations.md",
        "Register every source at retrieval time",
    ),
)
OFFICIAL_REFERENCE_URLS = (
    "https://www.jobbank.gc.ca/trend-analysis/search-job-outlooks",
    "https://www.ontario.ca/page/school-year-calendars",
    "https://food-guide.canada.ca/en/",
    "https://www.canada.ca/en/public-health/services/being-active/physical-activity-your-health.html",
    "https://www.ontario.ca/page/your-health",
    "https://www.canada.ca/en/financial-consumer-agency/services/make-budget.html",
    "https://www.canada.ca/en/revenue-agency/news/newsroom/tax-tips/tax-tips-2026/what-you-need-for-2026-tax-filing-season.html",
    "https://www.canada.ca/en/revenue-agency/news/newsroom/tax-tips/tax-tips-2026/tax-slips-what-they-are-where-find-why-waiting-can-help-avoid-mistakes.html",
    "https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/long-should-you-keep-your-income-tax-records.html",
    "https://www.canada.ca/en/services/benefits/finder.html",
    "https://www.canada.ca/en/services/benefits/calendar.html",
    "https://www.canada.ca/en/services/benefits/publicpensions/cpp/retirement-income-calculator.html",
    "https://travel.gc.ca/travelling/advisories",
    "https://travel.gc.ca/travelling/children/consent-letter",
)

AFFIRMATIVE = re.compile(
    r"\b(?:may|can|will|should|is allowed to|is permitted to|is authorized to)\b",
    re.IGNORECASE,
)
NEGATED = re.compile(
    r"\b(?:may not|cannot|can't|must not|does not|do not|never|is not allowed to|"
    r"is prohibited from|is forbidden from)\b",
    re.IGNORECASE,
)
CLAUSE_BOUNDARY = re.compile(r"\s*(?:;|\bbut\b|\bhowever\b)\s*", re.IGNORECASE)

POLICIES = (
    (
        "fabricated career evidence",
        re.compile(
            r"\b(?:invent|fabricat|embellish|exaggerat|make up).{0,70}"
            r"(?:achievement|result|evidence|experience|qualification|credential)",
            re.IGNORECASE,
        ),
    ),
    (
        "unapproved career publishing",
        re.compile(
            r"\b(?:publish|post|update).{0,70}(?:linkedin|about|portfolio|career profile)",
            re.IGNORECASE,
        ),
    ),
    (
        "bulk networking",
        re.compile(
            r"\b(?:send|message|contact|blast).{0,80}"
            r"(?:bulk|blanket|hundreds|strangers|networking|outreach)",
            re.IGNORECASE,
        ),
    ),
    (
        "candidate impersonation",
        re.compile(
            r"\b(?:answer|attend|conduct|take).{0,60}(?:live )?interview.{0,40}"
            r"(?:for|as) (?:priya|the candidate|candidate)",
            re.IGNORECASE,
        ),
    ),
    (
        "medical decision",
        re.compile(
            r"\b(?:diagnos|prescrib|choose treatment|medical decision|fitness treatment plan)",
            re.IGNORECASE,
        ),
    ),
    (
        "tax filing",
        re.compile(r"\b(?:file|submit).{0,45}(?:tax returns?|taxes)\b", re.IGNORECASE),
    ),
    (
        "financial decision",
        re.compile(
            r"\b(?:choose|select|buy|sell|move).{0,60}"
            r"(?:investment|security|retirement money|funds|money)",
            re.IGNORECASE,
        ),
    ),
    (
        "primary credential access",
        re.compile(
            r"\b(?:access|use|log in|sign in).{0,70}"
            r"(?:cra|bank|health|school).{0,50}(?:primary credential|password|account)",
            re.IGNORECASE,
        ),
    ),
    (
        "raw child dossier",
        re.compile(
            r"\b(?:maintain|create|store|compile|retain).{0,70}"
            r"(?:complete|full|raw).{0,35}child.{0,35}(?:dossier|record|file|history)",
            re.IGNORECASE,
        ),
    ),
    (
        "school or travel consent",
        re.compile(
            r"\b(?:sign|submit|give|authorize).{0,55}"
            r"(?:school|travel).{0,35}(?:consent|form|permission)",
            re.IGNORECASE,
        ),
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--hermes-source", type=Path)
    return parser.parse_args()


def require(text: str, phrase: str, label: str, failures: list[str]) -> None:
    if phrase.casefold() not in text.casefold():
        failures.append(f"missing {label}: {phrase}")


def find_unsafe_authorizations(text: str) -> list[tuple[str, str]]:
    """Return unsafe affirmative permissions while accepting explicit prohibitions."""
    findings: list[tuple[str, str]] = []
    for sentence in re.split(r"(?<=[.!?])(?:\s+|$)|\n+", text):
        for clause in CLAUSE_BOUNDARY.split(sentence):
            if not re.search(r"\bHermes\b", clause, re.IGNORECASE):
                continue
            if not AFFIRMATIVE.search(clause) or NEGATED.search(clause):
                continue
            for label, pattern in POLICIES:
                if pattern.search(clause):
                    findings.append((label, clause.strip()))
    return findings


def validate_official_references(text: str, failures: list[str]) -> None:
    for url in OFFICIAL_REFERENCE_URLS:
        reference_lines = [line for line in text.splitlines() if f"]({url})" in line]
        if not reference_lines:
            failures.append(f"missing exact official reference URL: {url}")
            continue
        if not any("accessed 2026-08-21" in line.casefold() for line in reference_lines):
            failures.append(f"missing visible verification date: {url}")


def validate_source(source: Path, failures: list[str]) -> None:
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


def audit_task8(root: Path, hermes_source: Path | None = None) -> list[str]:
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

    chapter_17 = content["docs/part-4/17-resume-interview-brand.md"]
    chapter_18 = content["docs/part-4/18-family-operations-canada.md"]
    combined = chapter_17 + "\n" + chapter_18

    for phrase in (
        "EVIDENCE GATE: PASS / HOLD",
        "claim-strength ladder",
        "master résumé",
        "executive bio",
        "LinkedIn About",
        "portfolio narrative",
        "interview question bank",
        "voice mock interview",
        "interview scorecard",
        "post-interview review",
        "networking message",
        "- **Native Hermes:**",
        "- **Bundled Hermes skills:**",
        "- **MCP or custom work:**",
        "- **Human/manual:**",
    ):
        label = (
            "Chapter 17 anti-hallucination evidence gate"
            if phrase == "EVIDENCE GATE: PASS / HOLD"
            else "Chapter 17 career-brand contract"
        )
        require(chapter_17, phrase, label, failures)

    for phrase in (
        "PROFESSIONAL HANDOFF MATRIX",
        "school-year",
        "activities and forms",
        "meal routine",
        "health routine",
        "fitness routine",
        "budget preparation",
        "tax-document collection",
        "benefit and deadline monitor",
        "retirement-goal inputs",
        "travel packet",
        "family review",
        "organization, not medical, financial, or tax advice",
        "No raw child dossier",
        "no primary credentials",
        "For the 2026 tax-filing season",
    ):
        label = (
            "Chapter 18 professional-handoff matrix"
            if phrase == "PROFESSIONAL HANDOFF MATRIX"
            else "Chapter 18 family-operations contract"
        )
        require(chapter_18, phrase, label, failures)

    for label, sentence in find_unsafe_authorizations(combined):
        failures.append(f"unsafe authorization: {label}: {sentence}")

    validate_official_references(combined, failures)
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
    failures = audit_task8(args.root.resolve(), args.hermes_source)
    for failure in failures:
        print(f"ERROR: {failure}")
    status = "OK" if not failures else "FAILED"
    source_status = "verified" if args.hermes_source else "reference paths checked"
    print(f"check_task8: {status} — {len(CHAPTERS)} chapters; pinned source {source_status}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
