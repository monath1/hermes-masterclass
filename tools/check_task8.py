#!/usr/bin/env python3
"""Audit the retained truth, advice, privacy, and source contracts in Chapters 17–18."""

from __future__ import annotations

import argparse
import html
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from urllib.parse import parse_qs, urljoin, urlparse

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
    "website/docs/user-guide/skills/bundled/productivity/productivity-xlsx.md",
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
        "website/docs/user-guide/skills/bundled/productivity/productivity-xlsx.md",
        "openpyxl itself NEVER evaluates formulas",
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
@dataclass(frozen=True)
class OfficialSourceContract:
    """A live primary source, its allowed redirect domain, and factual anchors."""

    url: str
    allowed_domain: str
    assertions: tuple[str, ...]


OFFICIAL_SOURCE_CONTRACTS = (
    OfficialSourceContract(
        "https://www.jobbank.gc.ca/trend-analysis/search-job-outlooks",
        "jobbank.gc.ca",
        ("Explore job outlooks", "employment prospects"),
    ),
    OfficialSourceContract(
        "https://www.ontario.ca/page/school-year-calendars",
        "ontario.ca",
        ("School year calendars", "school boards"),
    ),
    OfficialSourceContract(
        "https://food-guide.canada.ca/en/",
        "canada.ca",
        ("Canada's food guide", "healthy eating"),
    ),
    OfficialSourceContract(
        "https://www.canada.ca/en/public-health/services/being-active/physical-activity-your-health.html",
        "canada.ca",
        ("Recommended physical activity levels", "movement that makes your body work"),
    ),
    OfficialSourceContract(
        "https://www.ontario.ca/page/your-health",
        "ontario.ca",
        ("Your health", "Health811"),
    ),
    OfficialSourceContract(
        "https://www.canada.ca/en/financial-consumer-agency/services/make-budget.html",
        "canada.ca",
        ("Making a budget", "Budget Planner"),
    ),
    OfficialSourceContract(
        "https://www.canada.ca/en/revenue-agency/news/newsroom/tax-tips/tax-tips-2026/what-you-need-for-2026-tax-filing-season.html",
        "canada.ca",
        ("April 30, 2026", "June 15, 2026"),
    ),
    OfficialSourceContract(
        "https://www.canada.ca/en/revenue-agency/news/newsroom/tax-tips/tax-tips-2026/tax-slips-what-they-are-where-find-why-waiting-can-help-avoid-mistakes.html",
        "canada.ca",
        ("Tax slips", "My Account"),
    ),
    OfficialSourceContract(
        "https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/long-should-you-keep-your-income-tax-records.html",
        "canada.ca",
        ("How long should you keep", "six years"),
    ),
    OfficialSourceContract(
        "https://www.canada.ca/en/services/benefits/finder.html",
        "canada.ca",
        ("Benefits Finder", "federal programs and benefits"),
    ),
    OfficialSourceContract(
        "https://www.canada.ca/en/services/benefits/calendar.html",
        "canada.ca",
        ("Benefits payment dates", "Canada Child Benefit"),
    ),
    OfficialSourceContract(
        "https://www.canada.ca/en/services/benefits/publicpensions/cpp/retirement-income-calculator.html",
        "canada.ca",
        ("Canadian Retirement Income Calculator", "estimates"),
    ),
    OfficialSourceContract(
        "https://travel.gc.ca/travelling/advisories",
        "travel.gc.ca",
        ("Travel advice and advisories", "Risk level"),
    ),
    OfficialSourceContract(
        "https://travel.gc.ca/travelling/children/consent-letter",
        "travel.gc.ca",
        ("Recommended consent letter", "not legally required in Canada"),
    ),
)
OFFICIAL_REFERENCE_URLS = tuple(contract.url for contract in OFFICIAL_SOURCE_CONTRACTS)

AFFIRMATIVE = re.compile(
    r"\b(?:may|can|could|will|should|must|is able to|has permission to|"
    r"is allowed to|is permitted to|is authorized to)\b",
    re.IGNORECASE,
)
NEGATED = re.compile(
    r"\b(?:may not|cannot|can't|could not|will not|won't|should not|must not|"
    r"must (?:refuse|decline) to|must avoid|refuses? to|declines? to|"
    r"does not|doesn't|do not|never|is unable to|has no permission to|"
    r"is not allowed to|is prohibited from|is forbidden from)\b",
    re.IGNORECASE,
)
CLAUSE_BOUNDARY = re.compile(
    r"\s*(?:;|,(?=\s*(?:Hermes\b|the agent\b|it\b|may\b|can\b|could\b|"
    r"will\b|should\b|must\b))|\bbut\b|\bhowever\b|\bwhile\b|"
    r"\balthough\b|\bthough\b|\byet\b|"
    r"\bprovided(?: that)?\b|\bunless\b|\bas long as\b|\beven if\b|"
    r"\bwhereas\b|\bexcept(?: when| that)?\b|\bon condition that\b|"
    r"\band(?=\s+(?:it\b|Hermes\b|the agent\b|may\b|can\b|could\b|will\b|"
    r"should\b|must\b|is prohibited\b|is forbidden\b|is not allowed\b|"
    r"has no permission\b)))\s*",
    re.IGNORECASE,
)
AGENT_NAME = re.compile(r"\b(?:Hermes|the agent)\b", re.IGNORECASE)
AGENT_PRONOUN = re.compile(r"^\s*it\b", re.IGNORECASE)
ELLIPTICAL_MODAL = re.compile(
    r"^\s*(?:may|can|could|will|should|must|cannot|can't|won't)\b", re.IGNORECASE
)

POLICIES = (
    (
        "fabricated career evidence",
        re.compile(
            r"\b(?:invent|fabricat|embellish|exaggerat|make up|create false|"
            r"generate fake|add unsupported).{0,70}"
            r"(?:achievement|result|evidence|experience|qualification|credential)",
            re.IGNORECASE,
        ),
    ),
    (
        "unapproved career publishing",
        re.compile(
            r"\b(?:publish|post|update|push live|change).{0,70}"
            r"(?:linkedin(?: about)?|portfolio|career profile)",
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
            r"\b(?:diagnos|prescrib|recommend medication|set dosage|choose treatment|"
            r"medical decision|fitness treatment plan)",
            re.IGNORECASE,
        ),
    ),
    (
        "tax filing",
        re.compile(
            r"\b(?:file|submit|e-file).{0,45}(?:tax returns?|taxes)\b", re.IGNORECASE
        ),
    ),
    (
        "financial decision",
        re.compile(
            r"\b(?:choose|select|recommend|allocate|buy|sell|move).{0,60}"
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
    parser.add_argument(
        "--live",
        action="store_true",
        help="fetch official sources, enforce redirect domains, and check factual anchors",
    )
    return parser.parse_args()


def require(text: str, phrase: str, label: str, failures: list[str]) -> None:
    if phrase.casefold() not in text.casefold():
        failures.append(f"missing {label}: {phrase}")


def find_unsafe_authorizations(text: str) -> list[tuple[str, str]]:
    """Return unsafe permissions with actor resolution and predicate-local negation."""
    findings: list[tuple[str, str]] = []
    prior_agent = False
    for sentence in re.split(r"(?<=[.!?])(?:\s+|$)|\n+", text):
        if not sentence.strip():
            continue
        explicit_agent = bool(AGENT_NAME.search(sentence))
        sentence_agent = explicit_agent or (prior_agent and bool(AGENT_PRONOUN.search(sentence)))
        clause_agent = sentence_agent
        for clause in CLAUSE_BOUNDARY.split(sentence):
            if AGENT_NAME.search(clause):
                clause_agent = True
            elif AGENT_PRONOUN.search(clause) or ELLIPTICAL_MODAL.search(clause):
                clause_agent = clause_agent or prior_agent
            if not clause_agent:
                continue
            if not AFFIRMATIVE.search(clause) or NEGATED.search(clause):
                continue
            for label, pattern in POLICIES:
                if pattern.search(clause):
                    findings.append((label, clause.strip()))
        prior_agent = explicit_agent or (
            prior_agent and bool(AGENT_PRONOUN.search(sentence))
        )
    return findings


def _without_fenced_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


DATED_ASSERTION = re.compile(
    r"\b(?:accessed|checked|verified|observed|published|modified|dated)"
    r"(?:\s+\w+){0,5}\s+\d{4}-\d{2}-\d{2}\b",
    re.IGNORECASE,
)
OPERATIONAL_EXEMPTION = re.compile(
    r"\b(?:operational policy|operating policy|family-selected|owner-selected|"
    r"example cadence|local workflow)\b",
    re.IGNORECASE,
)
CANADIAN_DOLLAR = re.compile(r"(?:C\$|CAD\s+|\$)\s*\d[\d,]*(?:\.\d+)?", re.IGNORECASE)
CANADIAN_DEADLINE = re.compile(
    r"\b(?:deadline|due|filing|payment)\b.{0,100}\b(?:January|February|March|April|"
    r"May|June|July|August|September|October|November|December)\s+\d{1,2}\b|"
    r"\b(?:January|February|March|April|May|June|July|August|September|October|"
    r"November|December)\s+\d{1,2}\b.{0,100}\b(?:deadline|due|filing|payment)\b",
    re.IGNORECASE | re.DOTALL,
)
CANADIAN_THRESHOLD = re.compile(
    r"(?:\b(?:tax|benefit|credit|eligib\w*|retain\w*|retention|keep|records?)\b"
    r".{0,120}(?:\b(?:at least|minimum|maximum|within)\b\s*)?"
    r"(?:\d+(?:\.\d+)?%|(?:one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve|\d+)\s+(?:days?|months?|years?))|"
    r"(?:\d+(?:\.\d+)?%|(?:one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve|\d+)\s+(?:days?|months?|years?)).{0,120}"
    r"\b(?:tax|benefit|credit|eligib\w*|retain\w*|retention|keep|records?)\b)",
    re.IGNORECASE | re.DOTALL,
)
DEADLINE_VALUE = re.compile(
    r"\b(?:January|February|March|April|May|June|July|August|September|October|"
    r"November|December)\s+\d{1,2}\b",
    re.IGNORECASE,
)
THRESHOLD_VALUE = re.compile(
    r"\d+(?:\.\d+)?%|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve|\d+)\s+(?:days?|months?|years?)\b",
    re.IGNORECASE,
)
CLAIM_MARKER_WINDOW = 220
CLAIM_CLAUSE_BOUNDARY = re.compile(
    r";|[.!?](?=\s|$)|,\s+(?:and|but|while|whereas|although|though|provided|unless)\b",
    re.IGNORECASE,
)
CLAIM_CATEGORY_CUE = {
    "dollar": re.compile(
        r"\b(?:amount|dollar|price|cost|payment|benefit|cap|ceiling)\w*\b",
        re.IGNORECASE,
    ),
    "deadline": re.compile(
        r"\b(?:deadline|due|filing|payment date|dated examples?|calendar date)\b",
        re.IGNORECASE,
    ),
    "threshold": re.compile(
        r"\b(?:threshold|retention|eligibility|percentage|percent|minimum|maximum)\b",
        re.IGNORECASE,
    ),
}
OPERATIONAL_CATEGORY_CUE = {
    "dollar": re.compile(
        r"\b(?:planning cap|budget ceiling|scenario amount|example amount)\b",
        re.IGNORECASE,
    ),
    "deadline": re.compile(
        r"\b(?:family deadline|review date|preparation window|operational cadence)\b",
        re.IGNORECASE,
    ),
    "threshold": re.compile(
        r"\b(?:review cadence|operational interval|planning horizon)\b",
        re.IGNORECASE,
    ),
}


def _claim_clause(text: str, start: int, end: int) -> tuple[str, int]:
    """Return the bounded clause containing a numeric value and its end offset."""
    boundaries = list(CLAIM_CLAUSE_BOUNDARY.finditer(text))
    clause_start = max(
        (boundary.end() for boundary in boundaries if boundary.end() <= start),
        default=0,
    )
    clause_end = min(
        (boundary.start() for boundary in boundaries if boundary.start() >= end),
        default=len(text),
    )
    return text[clause_start:clause_end], clause_end


def _match_has_local_marker(
    text: str,
    match: re.Match[str],
    value_pattern: re.Pattern[str],
    category: str,
) -> bool:
    """Bind each value to a same-category clause or referential follow-up."""
    values = list(value_pattern.finditer(match.group()))
    if not values:
        values = [match]
    for value in values:
        start = match.start() + value.start() if value is not match else match.start()
        end = match.start() + value.end() if value is not match else match.end()
        clause, clause_end = _claim_clause(text, start, end)
        category_cue = CLAIM_CATEGORY_CUE[category]
        if DATED_ASSERTION.search(clause) and category_cue.search(clause):
            continue
        operational_cue = OPERATIONAL_CATEGORY_CUE[category]
        if OPERATIONAL_EXEMPTION.search(clause) and operational_cue.search(clause):
            continue
        follow_up = text[
            clause_end : min(len(text), clause_end + CLAIM_MARKER_WINDOW)
        ]
        direct_date = re.match(
            r"[\s,;.]*(?:accessed|checked|verified|observed|published|modified|dated)\b",
            follow_up,
            re.IGNORECASE,
        )
        referential = re.search(
            r"(?:^|[.!?]\s+)(?:These|Those|This|That)\b",
            follow_up,
            re.IGNORECASE,
        )
        if direct_date and DATED_ASSERTION.search(follow_up) and category_cue.search(clause):
            continue
        if (
            referential
            and DATED_ASSERTION.search(follow_up)
            and category_cue.search(follow_up)
        ):
            continue
        return False
    return True


def find_undated_changeable_claims(text: str) -> list[tuple[str, str]]:
    """Find numeric Canadian claims lacking a date or explicit local-policy marker."""
    body = _without_fenced_code(text).split("\n## References", 1)[0]
    findings: list[tuple[str, str]] = []
    for paragraph in re.split(r"\n\s*\n", body):
        compact = " ".join(paragraph.split())
        if not compact:
            continue
        dollar_matches = list(CANADIAN_DOLLAR.finditer(compact))
        if any(
            not _match_has_local_marker(compact, match, CANADIAN_DOLLAR, "dollar")
            for match in dollar_matches
        ):
            findings.append(("Canadian dollar amount", compact))
        deadline_matches = list(CANADIAN_DEADLINE.finditer(compact))
        if any(
            not _match_has_local_marker(compact, match, DEADLINE_VALUE, "deadline")
            for match in deadline_matches
        ):
            findings.append(("Canadian deadline", compact))
        threshold_matches = list(CANADIAN_THRESHOLD.finditer(compact))
        if any(
            not _match_has_local_marker(compact, match, THRESHOLD_VALUE, "threshold")
            for match in threshold_matches
        ):
            findings.append(("Canadian threshold", compact))
    return findings


def _normalized_source_text(source: str) -> str:
    without_markup = re.sub(r"<[^>]+>", " ", source)
    return " ".join(html.unescape(without_markup).casefold().split())


LiveTransport = Callable[[str, float], tuple[int, str, dict[str, str], str]]


def _curl_once(url: str, timeout: float) -> tuple[int, str, dict[str, str], str]:
    """Fetch exactly one HTTP response; redirects are deliberately not followed."""
    marker = "__HERMES_HTTP_META__="
    result = subprocess.run(
        [
            "curl",
            "--silent",
            "--show-error",
            "--max-time",
            f"{timeout:.3f}",
            "--user-agent",
            "HERMES-book-source-audit/1.0 (+manual verification)",
            "--write-out",
            f"\n{marker}%{{http_code}}\t%{{url_effective}}\t%{{redirect_url}}",
            url,
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"curl exited {result.returncode}")
    body, separator, metadata = result.stdout.rpartition(f"\n{marker}")
    if not separator:
        raise RuntimeError("curl did not report HTTP metadata")
    fields = metadata.rstrip("\n").split("\t", 2)
    if len(fields) != 3 or not fields[0].isdigit():
        raise RuntimeError("curl returned malformed HTTP metadata")
    status_text, effective_url, redirect_url = fields
    headers = {"location": redirect_url} if redirect_url else {}
    return int(status_text), effective_url, headers, body


def _require_allowed_live_url(url: str, allowed_domain: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme.casefold() != "https":
        raise RuntimeError(f"live source redirect must use HTTPS: {url}")
    hostname = (parsed.hostname or "").casefold()
    allowed = allowed_domain.casefold()
    if hostname != allowed and not hostname.endswith(f".{allowed}"):
        raise RuntimeError(f"live source redirected outside allowed domain: {url}")
    try:
        port = parsed.port
    except ValueError as error:
        raise RuntimeError(f"live source URL has an invalid port: {url}") from error
    if port not in (None, 443):
        raise RuntimeError(f"live source URL uses a non-default HTTPS port: {url}")
    if parsed.username or parsed.password:
        raise RuntimeError(f"live source URL must not contain credentials: {url}")


def fetch_official_source(
    url: str,
    allowed_domain: str,
    *,
    transport: LiveTransport = _curl_once,
    max_redirects: int = 5,
    total_timeout: float = 30,
) -> tuple[str, str]:
    """Fetch one source with bounded, validated, manually followed redirects."""
    if max_redirects < 0 or total_timeout <= 0:
        raise ValueError("redirect and timeout bounds must be positive")
    deadline = time.monotonic() + total_timeout
    current_url = url
    redirects = 0
    while True:
        _require_allowed_live_url(current_url, allowed_domain)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise RuntimeError(f"live source total timeout exceeded: {url}")
        status, effective_url, headers, body = transport(
            current_url, min(20.0, remaining)
        )
        _require_allowed_live_url(effective_url, allowed_domain)

        target: str | None = None
        if 300 <= status < 400:
            location = next(
                (value for key, value in headers.items() if key.casefold() == "location"),
                "",
            )
            if not location:
                raise RuntimeError(f"HTTP {status} redirect missing Location: {effective_url}")
            target = urljoin(effective_url, location)
        elif 200 <= status < 300:
            parsed = urlparse(effective_url)
            moved_target = parse_qs(parsed.query).get("to", [])
            if parsed.path.endswith("/cfgredirect.html") and moved_target:
                target = urljoin(effective_url, moved_target[0])
            else:
                return effective_url, body
        else:
            raise RuntimeError(f"HTTP {status} from live source: {effective_url}")

        _require_allowed_live_url(target, allowed_domain)
        if redirects >= max_redirects:
            raise RuntimeError(f"live source redirect limit exceeded: {url}")
        redirects += 1
        current_url = target


def validate_live_sources(
    failures: list[str],
    fetcher: Callable[[str, str], tuple[str, str]] = fetch_official_source,
) -> None:
    """Check live reachability, redirect ownership, and load-bearing page content."""
    def check_contract(contract: OfficialSourceContract) -> list[str]:
        contract_failures: list[str] = []
        try:
            final_url, body = fetcher(contract.url, contract.allowed_domain)
        except Exception as error:  # pragma: no cover - exercised by manual network mode
            return [f"live source fetch failed: {contract.url}: {error}"]
        try:
            _require_allowed_live_url(final_url, contract.allowed_domain)
        except RuntimeError as error:
            return [f"invalid live source authority: {contract.url}: {error}"]
        normalized = _normalized_source_text(body)
        for assertion in contract.assertions:
            if _normalized_source_text(assertion) not in normalized:
                contract_failures.append(
                    f"missing live source content assertion: {contract.url}: {assertion}"
                )
        return contract_failures

    with ThreadPoolExecutor(max_workers=4) as executor:
        for contract_failures in executor.map(check_contract, OFFICIAL_SOURCE_CONTRACTS):
            failures.extend(contract_failures)


def validate_official_references(text: str, failures: list[str]) -> None:
    for url in OFFICIAL_REFERENCE_URLS:
        reference_lines = [line for line in text.splitlines() if f"]({url})" in line]
        if not reference_lines:
            failures.append(f"missing exact official reference URL: {url}")
            continue
        if not any("accessed 2026-08-21" in line.casefold() for line in reference_lines):
            failures.append(f"missing visible verification date: {url}")


GREEN_AUTHORITY_POLICIES = (
    (
        "professional advice",
        re.compile(
            r"\b(?:provide|give|offer).{0,50}"
            r"\b(?:medical|financial|tax) advice\b",
            re.IGNORECASE,
        ),
    ),
    (
        "medical action",
        re.compile(
            r"\b(?:diagnos\w*|treat\w*|prescrib\w*|dispens\w*|triag\w*|"
            r"set therapeutic diets?|decide return-to-play)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "tax filing",
        re.compile(
            r"\b(?:file|submit|e-file).{0,30}\b(?:tax(?:es)?|tax returns?|returns?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "investment or benefit decision",
        re.compile(
            r"\b(?:choose|select|recommend).{0,35}\b(?:investments?|benefits?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "consent or rights",
        re.compile(
            r"\b(?:sign.{0,25}consent|consent to|waive.{0,25}rights?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "raw child dossier",
        re.compile(
            r"\b(?:compile|create|store|retain|hold).{0,35}"
            r"\braw child dossiers?\b",
            re.IGNORECASE,
        ),
    ),
    (
        "primary credential",
        re.compile(
            r"\b(?:use|hold|access|store|retain).{0,30}"
            r"\bprimary credentials?\b",
            re.IGNORECASE,
        ),
    ),
    (
        "protected account access",
        re.compile(
            r"\b(?:access|log in|sign in).{0,35}"
            r"\b(?:bank(?:ing)?|CRA|health|school|travel) accounts?\b",
            re.IGNORECASE,
        ),
    ),
    (
        "impersonation",
        re.compile(r"\bimpersonat\w*.{0,25}\b(?:child|guardian)\b", re.IGNORECASE),
    ),
    (
        "benefit application",
        re.compile(r"\bapply for benefits?\b", re.IGNORECASE),
    ),
    (
        "money movement",
        re.compile(r"\b(?:move|transfer|send).{0,20}\bmoney\b", re.IGNORECASE),
    ),
    (
        "travel booking",
        re.compile(r"\bbook.{0,20}\b(?:travel|flight|hotel|accommodation)\b", re.IGNORECASE),
    ),
    (
        "terms acceptance",
        re.compile(r"\baccept.{0,20}\bterms\b", re.IGNORECASE),
    ),
    (
        "cross-profile disclosure",
        re.compile(r"\bdisclos\w*.{0,25}\bacross profiles\b", re.IGNORECASE),
    ),
    (
        "sensitive inference",
        re.compile(
            r"\binfer.{0,45}\b(?:eligibility|custody|health|family values?)\b",
            re.IGNORECASE,
        ),
    ),
)
HANDOFF_DECISION_CONTRACTS = (
    (
        "health",
        r"Health or nutrition concern:.*?Decide:.*?"
        r"(?:clinician|pharmacist|dietitian|emergency service)",
    ),
    (
        "tax",
        r"Tax question:.*?Decide:.*?"
        r"(?:taxpayer|accountant|tax professional|CRA)",
    ),
    (
        "financial",
        r"Budget, debt, retirement, pension, investment, or insurance question:"
        r".*?Decide:.*?"
        r"(?:adults|planner|administrator|provider|insolvency professional)",
    ),
    (
        "school/legal/travel",
        r"School, child consent, custody, or travel-document question:"
        r".*?Decide:.*?(?:guardian|school|board|authority|lawyer)",
    ),
    (
        "benefits",
        r"Benefit eligibility, overpayment, appeal, or account change:"
        r".*?Decide:.*?(?:agency|representative|adviser)",
    ),
)


def validate_family_semantics(chapter: str, failures: list[str]) -> None:
    """Validate decision ownership and prohibited Green authority structurally."""
    green_match = re.search(
        r"^\| \*\*Green — may act\*\* \|(?P<body>.*?)\|\s*$",
        chapter,
        re.IGNORECASE | re.MULTILINE,
    )
    if not green_match:
        failures.append("missing Chapter 18 Green authority row")
    else:
        green = green_match.group("body")
        for label, pattern in GREEN_AUTHORITY_POLICIES:
            if pattern.search(green):
                failures.append(f"unsafe Chapter 18 Green authority: {label}")

    matrix_match = re.search(
        r"```text\s+PROFESSIONAL HANDOFF MATRIX(?P<body>.*?)```",
        chapter,
        re.IGNORECASE | re.DOTALL,
    )
    if not matrix_match:
        failures.append("missing semantic Chapter 18 professional handoff matrix")
        return
    matrix = matrix_match.group("body")
    if re.search(r"\bDecide:\s*(?:Hermes|the agent)\b", matrix, re.IGNORECASE):
        failures.append("unsafe Chapter 18 professional handoff decision owner")
    for label, pattern in HANDOFF_DECISION_CONTRACTS:
        if not re.search(pattern, matrix, re.IGNORECASE | re.DOTALL):
            failures.append(f"missing Chapter 18 professional handoff decision contract: {label}")


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


def audit_task8(
    root: Path, hermes_source: Path | None = None, *, live: bool = False
) -> list[str]:
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

    for edge in ("M --> GM", "T --> GT", "X --> GX", "GM -->|Pass| H", "GT -->|Pass| H", "GX -->|Pass| H"):
        if edge not in chapter_17:
            failures.append(f"missing Chapter 17 per-artifact evidence-gate flow: {edge}")

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

    if "asthma-plan update" in chapter_18.casefold():
        failures.append("diagnosis-bearing sample metadata: asthma-plan update")

    validate_family_semantics(chapter_18, failures)

    for label, paragraph in find_undated_changeable_claims(chapter_18):
        failures.append(f"undated {label}: {paragraph}")

    for label, sentence in find_unsafe_authorizations(combined):
        failures.append(f"unsafe authorization: {label}: {sentence}")

    validate_official_references(combined, failures)
    if live:
        validate_live_sources(failures)
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
    failures = audit_task8(args.root.resolve(), args.hermes_source, live=args.live)
    for failure in failures:
        print(f"ERROR: {failure}")
    status = "OK" if not failures else "FAILED"
    source_status = "verified" if args.hermes_source else "reference paths checked"
    live_status = ""
    if args.live:
        live_status = "; live sources verified" if not failures else "; live source check failed"
    print(
        f"check_task8: {status} — {len(CHAPTERS)} chapters; "
        f"pinned source {source_status}{live_status}"
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
