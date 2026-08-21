#!/usr/bin/env python3
"""Audit the retained workflow, source, and state contracts in Chapters 15–16."""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

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
OFFICIAL_REFERENCE_URLS = (
    "https://www.jobbank.gc.ca/termsofuse-seeker.xhtml",
    "https://www.jobbank.gc.ca/jobsearch/",
    "https://www.linkedin.com/legal/user-agreement",
    "https://www.linkedin.com/help/linkedin/answer/a1341387/prohibited-software-and-extensions",
    "https://antifraudcentre-centreantifraude.ca/scams-fraudes/job-emploi-eng.htm",
)
Phrase = tuple[str, ...]
AUTHORIZATION_MARKERS: tuple[Phrase, ...] = (
    ("may",),
    ("can",),
    ("should",),
    ("must",),
    ("will",),
    ("allowed", "to"),
    ("permitted", "to"),
    ("authorized", "to"),
    ("permission", "to"),
    ("let",),
    ("allow",),
    ("permit",),
    ("enable",),
)
NEGATION_TOKENS = {"not", "never", "cannot", "prohibited", "forbidden"}
KNOWN_ACTORS = {"hermes", "priya", "alex", "candidate", "user", "users", "person", "human"}
HUMAN_ACTORS = KNOWN_ACTORS - {"hermes"}
TOKEN_ALIASES = {
    "accesses": "access",
    "allows": "allow",
    "applies": "apply",
    "automates": "automate",
    "blasts": "blast",
    "controls": "control",
    "crawls": "crawl",
    "embellishes": "embellish",
    "emails": "email",
    "enables": "enable",
    "exaggerates": "exaggerate",
    "fabricates": "fabricate",
    "files": "file",
    "generates": "generate",
    "gives": "give",
    "invents": "invent",
    "lets": "let",
    "mailboxes": "mailboxes",
    "manages": "manage",
    "manufactures": "manufacture",
    "messages": "messages",
    "monitors": "monitor",
    "operates": "operate",
    "permits": "permit",
    "provides": "provide",
    "queries": "query",
    "reads": "read",
    "scrapes": "scrape",
    "searches": "search",
    "sends": "send",
    "shares": "share",
    "submits": "submit",
    "submitted": "submit",
    "uses": "use",
}


def phrases(*values: str) -> tuple[Phrase, ...]:
    return tuple(tuple(value.split()) for value in values)


@dataclass(frozen=True)
class SentenceView:
    """Normalized sentence used by the prose-policy scanner."""

    source: str
    tokens: tuple[str, ...]

    @classmethod
    def parse(cls, source: str) -> SentenceView:
        normalized = (
            source.casefold()
            .replace("’", "'")
            .replace("can't", "cannot")
            .replace("won't", "will not")
            .replace("n't", " not")
        )
        raw_tokens = re.findall(r"[a-z0-9]+(?:'[a-z]+)?", normalized)
        tokens = []
        for token in raw_tokens:
            if token.endswith("'s"):
                token = token[:-2]
            tokens.append(TOKEN_ALIASES.get(token, token))
        return cls(source=source.strip(), tokens=tuple(tokens))

    def positions(self, candidates: tuple[Phrase, ...]) -> list[tuple[int, int]]:
        matches: list[tuple[int, int]] = []
        for phrase in candidates:
            width = len(phrase)
            for start in range(len(self.tokens) - width + 1):
                if self.tokens[start : start + width] == phrase:
                    matches.append((start, start + width))
        return sorted(matches)

    def has(self, candidates: tuple[Phrase, ...]) -> bool:
        return bool(self.positions(candidates))

    def has_after(self, candidates: tuple[Phrase, ...], start: int) -> bool:
        return any(position >= start for position, _end in self.positions(candidates))

    def nearest_actor_before(self, position: int) -> str | None:
        actors = [token for token in self.tokens[:position] if token in KNOWN_ACTORS]
        return actors[-1] if actors else None

    def is_negated(self, marker_start: int, action_end: int) -> bool:
        window_start = max(0, marker_start - 3)
        return bool(NEGATION_TOKENS.intersection(self.tokens[window_start:action_end]))

    def authorized_actions(
        self,
        actions: tuple[Phrase, ...],
        *,
        actors: set[str] | None = None,
        direct_actions: tuple[Phrase, ...] = (),
        automatic_is_authorization: bool = False,
    ) -> list[tuple[int, int]]:
        """Return actions asserted or affirmatively authorized for the selected actor."""
        authorized: list[tuple[int, int]] = []
        marker_positions = self.positions(AUTHORIZATION_MARKERS)
        automatic_positions = self.positions(phrases("automatic", "automatically"))
        direct_positions = set(self.positions(direct_actions))
        for action_start, action_end in self.positions(actions):
            actor = self.nearest_actor_before(action_start)
            if actors is not None and actor not in actors:
                continue
            candidates = [
                marker
                for marker in marker_positions
                if marker[0] <= action_start and action_start - marker[0] <= 12
            ]
            if automatic_is_authorization:
                candidates.extend(
                    marker
                    for marker in automatic_positions
                    if marker[0] <= action_start and action_start - marker[0] <= 4
                )
            if (action_start, action_end) in direct_positions and not candidates:
                candidates.append((action_start, action_start))
            if any(not self.is_negated(marker_start, action_end) for marker_start, _ in candidates):
                authorized.append((action_start, action_end))
        return authorized


def has_unsafe_primary_inbox_access(sentence: SentenceView) -> bool:
    actions = phrases("access", "read", "manage", "monitor", "open", "triage", "connect to")
    objects = phrases(
        "primary inbox",
        "primary inboxes",
        "primary mailbox",
        "primary mailboxes",
        "personal inbox",
        "personal mailbox",
    )
    return any(
        sentence.has_after(objects, action_end)
        for _action_start, action_end in sentence.authorized_actions(actions, actors={"hermes"})
    )


def has_unsafe_account_sharing(sentence: SentenceView) -> bool:
    account_objects = phrases(
        "job bank account",
        "linkedin account",
        "job platform account",
        "platform account",
        "job bank credentials",
        "linkedin credentials",
        "account credentials",
        "login credentials",
        "password",
        "sign in",
    )
    hermes_actions = phrases("access", "control", "use", "operate", "manage", "log in", "sign in")
    if any(
        sentence.has_after(account_objects, action_end)
        for _action_start, action_end in sentence.authorized_actions(
            hermes_actions, actors={"hermes"}
        )
    ):
        return True

    sharing_actions = phrases("share", "give", "provide", "hand over")
    return any(
        sentence.has_after(account_objects, action_end)
        and sentence.has_after(phrases("hermes"), action_end)
        for _action_start, action_end in sentence.authorized_actions(
            sharing_actions, actors=HUMAN_ACTORS
        )
    )


def has_unsafe_platform_automation(sentence: SentenceView) -> bool:
    actions = phrases("automate", "query", "search", "access", "scrape", "crawl", "harvest")
    direct_actions = phrases("automate", "scrape", "crawl", "harvest")
    platforms = phrases("job bank", "linkedin")
    return any(
        sentence.has_after(platforms, action_end)
        for _action_start, action_end in sentence.authorized_actions(
            actions,
            actors={"hermes"},
            direct_actions=direct_actions,
            automatic_is_authorization=True,
        )
    )


def has_unsafe_mass_outreach(sentence: SentenceView) -> bool:
    actions = phrases("send", "generate", "automate", "blast", "message", "email", "contact")
    objects = phrases("outreach", "message", "messages", "email", "emails", "contacts")
    mass_markers = phrases(
        "mass",
        "bulk",
        "spam",
        "blanket",
        "high volume",
        "hundreds",
        "thousands",
        "identical",
        "indiscriminate",
        "unsolicited",
    )
    return sentence.has(mass_markers) and any(
        sentence.has_after(objects, action_end)
        for _action_start, action_end in sentence.authorized_actions(
            actions, actors={"hermes"}, direct_actions=phrases("blast")
        )
    )


def has_unsafe_fabricated_claims(sentence: SentenceView) -> bool:
    actions = phrases("fabricate", "invent", "make up", "embellish", "exaggerate", "manufacture", "falsify")
    objects = phrases(
        "claim",
        "claims",
        "credential",
        "credentials",
        "experience",
        "qualification",
        "qualifications",
        "achievement",
        "achievements",
        "reference",
        "references",
        "result",
        "results",
        "relationship",
        "relationships",
        "work history",
    )
    return any(
        sentence.has_after(objects, action_end)
        for _action_start, action_end in sentence.authorized_actions(
            actions, actors={"hermes"}, direct_actions=actions
        )
    )


def has_unsafe_submission(sentence: SentenceView) -> bool:
    actions = phrases("submit", "file", "send", "apply")
    applications = phrases(
        "application",
        "applications",
        "application package",
        "application materials",
        "candidate materials",
        "form",
    )
    bypass_cues = phrases("without", "before", "no", "skip", "bypass")
    approval_terms = phrases("approval", "consent", "sign off", "authorization", "review")
    independent_bypasses = phrases(
        "independently",
        "autonomously",
        "unilaterally",
        "on its own",
    )
    defaults = phrases("by default", "automatically", "unless priya opts out", "unless the candidate opts out")
    action_positions = sentence.positions(actions)
    if not action_positions or not sentence.has(applications):
        return False

    # Default or opt-out submission is unsafe even when written in passive voice.
    if sentence.has(defaults):
        return any(
            not sentence.is_negated(max(0, action_start - 4), action_end)
            for action_start, action_end in action_positions
        )

    cue_before_approval = any(
        0 < approval_start - cue_start <= 5
        for cue_start, _cue_end in sentence.positions(bypass_cues)
        for approval_start, _approval_end in sentence.positions(approval_terms)
    )
    if not cue_before_approval and not sentence.has(independent_bypasses):
        return False
    return bool(sentence.authorized_actions(actions, actors={"hermes"}))


POLICY_SCANNERS: tuple[tuple[str, Callable[[SentenceView], bool]], ...] = (
    ("primary-inbox access", has_unsafe_primary_inbox_access),
    ("account sharing", has_unsafe_account_sharing),
    ("Job Bank or LinkedIn automation/scraping", has_unsafe_platform_automation),
    ("bulk/spam outreach", has_unsafe_mass_outreach),
    ("fabricated claims", has_unsafe_fabricated_claims),
    ("submission without approval", has_unsafe_submission),
)


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


def find_unsafe_authorizations(text: str) -> list[tuple[str, str]]:
    """Return policy labels and sentences containing affirmative unsafe authority."""
    findings: list[tuple[str, str]] = []
    sentence_sources = re.split(r"(?<=[.!?;])(?:\s+|$)|\n+", text)
    for source in sentence_sources:
        sentence = SentenceView.parse(source)
        if not sentence.tokens:
            continue
        for label, scanner in POLICY_SCANNERS:
            if scanner(sentence):
                findings.append((label, sentence.source))
    return findings


def reject_unsafe_authorizations(text: str, failures: list[str]) -> None:
    """Reject affirmative unsafe permissions without matching explicit negations."""
    for label, sentence in find_unsafe_authorizations(text):
        failures.append(f"unsafe authorization: {label}: {sentence}")


def validate_official_references(text: str, failures: list[str]) -> None:
    """Require the exact official reference and a visible same-line access date."""
    for url in OFFICIAL_REFERENCE_URLS:
        reference_lines = [line for line in text.splitlines() if f"]({url})" in line]
        if not reference_lines:
            failures.append(f"missing exact official reference URL: {url}")
            continue
        if not any("accessed 2026-08-21" in line.casefold() for line in reference_lines):
            failures.append(f"missing visible verification date: {url}")


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

    reject_unsafe_authorizations(combined, failures)
    validate_official_references(chapter_16, failures)

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
