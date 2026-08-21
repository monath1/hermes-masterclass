#!/usr/bin/env python3
"""Audit the retained small-business operating contracts in Chapters 19–20."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from check_book import markdown_words


PINNED_COMMIT = "fcbd1076a93841fa88855acce810e342a5b78101"
CHAPTERS = {
    "docs/part-5/19-one-two-person-business-os.md": (4200, 4800),
    "docs/part-5/20-business-functions.md": (4600, 5200),
}
REQUIRED_PINNED_PATHS = {
    "website/docs/user-guide/profiles.md",
    "website/docs/user-guide/bot-mode.md",
    "website/docs/user-guide/features/browser.md",
    "website/docs/user-guide/features/cron.md",
    "website/docs/user-guide/features/deliverable-mode.md",
    "website/docs/user-guide/features/document-extraction.md",
    "website/docs/user-guide/features/goals.md",
    "website/docs/user-guide/features/hooks.md",
    "website/docs/user-guide/features/kanban.md",
    "website/docs/user-guide/features/skills.md",
    "website/docs/user-guide/features/tools.md",
    "website/docs/user-guide/features/web-search.md",
    "website/docs/user-guide/messaging/email.md",
    "website/docs/user-guide/skills/bundled/productivity/productivity-google-workspace.md",
    "website/docs/user-guide/skills/bundled/productivity/productivity-meeting-action-items.md",
    "website/docs/user-guide/skills/bundled/research/research-grounded-citations.md",
}
PINNED_SOURCE_ASSERTIONS = (
    ("website/docs/user-guide/profiles.md", "A profile is a separate Hermes home directory"),
    ("website/docs/user-guide/bot-mode.md", "A Bot is a profile"),
    ("website/docs/user-guide/features/kanban.md", "durable task board"),
    ("website/docs/user-guide/features/deliverable-mode.md", "native attachments"),
    ("website/docs/user-guide/features/web-search.md", "web_search"),
    ("website/docs/user-guide/messaging/email.md", "A dedicated email account"),
    ("website/docs/user-guide/features/document-extraction.md", "text layer only"),
    ("website/docs/user-guide/features/tools.md", "Search the web and extract page content"),
    (
        "website/docs/user-guide/skills/bundled/productivity/productivity-google-workspace.md",
        "Google Workspace",
    ),
    (
        "website/docs/user-guide/skills/bundled/productivity/productivity-meeting-action-items.md",
        "Do not turn brainstorming into decisions",
    ),
    ("website/docs/user-guide/features/cron.md", "fresh agent session"),
    (
        "website/docs/user-guide/features/hooks.md",
        "Gateway hooks fire automatically during gateway operation",
    ),
    (
        "website/docs/user-guide/features/hooks.md",
        "Both Python plugin hooks and shell hooks flow through the same `invoke_hook()` dispatcher",
    ),
    (
        "website/docs/user-guide/features/hooks.md",
        "`fail_closed` only applies to blocking-capable events (`pre_tool_call` today)",
    ),
    (
        "website/docs/user-guide/features/hooks.md",
        "outbound webhooks cannot block tool calls or inject context",
    ),
    (
        "website/docs/user-guide/skills/bundled/research/research-grounded-citations.md",
        "Register every source at retrieval time",
    ),
)

AFFIRMATIVE = re.compile(
    r"\b(?:may|can|could|will|should|must|is able to|is allowed to|"
    r"is permitted to|is authorized to)\b",
    re.IGNORECASE,
)
NEGATED = re.compile(
    r"\b(?:may not|cannot|can't|could not|will not|won't|should not|must not|"
    r"must (?:refuse|decline) to|must avoid|does not|doesn't|do not|never|"
    r"is prohibited from|is forbidden from|has no authority to)\b",
    re.IGNORECASE,
)
AGENT = re.compile(r"\b(?:Hermes|the agent)\b", re.IGNORECASE)
CLAUSE_SPLIT = re.compile(
    r"(?:[.;]|,\s*(?:but|although|though|however|yet|provided that|unless|while)\s+)",
    re.IGNORECASE,
)
POLICIES = (
    (
        "contract or legal commitment",
        re.compile(r"\b(?:sign|execute|accept|agree to)\b.{0,35}\b(?:contract|agreement|terms)\b", re.IGNORECASE),
    ),
    (
        "price or discount commitment",
        re.compile(r"\b(?:set|change|approve|offer|commit|determine)\b.{0,35}\b(?:prices?|pricing|discounts?|credits?)\b", re.IGNORECASE),
    ),
    (
        "money movement",
        re.compile(
            r"\b(?:charge.{0,20}(?:card|account)|pay.{0,20}(?:invoice|supplier|bill)|"
            r"purchase.{0,20}(?:item|service|subscription)|transfer|move.{0,20}(?:money|funds?)|"
            r"refund|withdraw|deposit)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "customer promise",
        re.compile(
            r"\b(?:(?:promise|guarantee|commit)\b.{0,50}\b(?:customer|delivery|outcome|result|deadline|date|service)?|"
            r"set\b.{0,30}\b(?:customer\s+)?delivery\s+(?:date|deadline))\b",
            re.IGNORECASE,
        ),
    ),
    (
        "mass outreach",
        re.compile(r"\b(?:blast|bulk[- ]send|mass[- ]email|send mass|scrape.{0,25}(?:lead|address)|cold[- ]email.{0,20}(?:every|all|list))\b", re.IGNORECASE),
    ),
    (
        "deceptive marketing",
        re.compile(r"\b(?:fabricate|invent|fake|impersonate)\b.{0,35}\b(?:testimonial|review|customer|claim|endorsement)?\b", re.IGNORECASE),
    ),
    (
        "professional bookkeeping or tax decision",
        re.compile(
            r"\b(?:(?:classify|categorize)\b.{0,45}\b(?:expenses?|transactions?|deductions?|books?)|"
            r"(?:choose|determine|decide)\b.{0,45}\b(?:tax treatment|tax position|deductibility|account classification)|"
            r"post\b.{0,20}\bfinal entries|(?:file|submit)\b.{0,45}\b(?:taxes|tax return|returns?))\b",
            re.IGNORECASE,
        ),
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="book root")
    parser.add_argument(
        "--hermes-source",
        type=Path,
        help="optional pinned Hermes v2026.8.19 checkout for source-content verification",
    )
    return parser.parse_args()


def require(text: str, phrase: str, label: str, failures: list[str]) -> None:
    if phrase.casefold() not in text.casefold():
        failures.append(f"missing {label}: {phrase}")


def _prose_without_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def find_unsafe_authorizations(text: str) -> list[tuple[str, str]]:
    """Find affirmative grants for Task 9's finite list of forbidden effects."""
    findings: list[tuple[str, str]] = []
    for sentence in re.split(r"(?<=[.!?])\s+|\n+", _prose_without_code(text)):
        if not AGENT.search(sentence):
            continue
        for clause in CLAUSE_SPLIT.split(sentence):
            if not clause.strip():
                continue
            for label, action in POLICIES:
                match = action.search(clause)
                if not match:
                    continue
                prefix = clause[: match.end()]
                local_actor = AGENT.search(prefix) or re.match(r"\s*it\b", prefix, re.IGNORECASE)
                if local_actor and AFFIRMATIVE.search(prefix) and not NEGATED.search(prefix):
                    findings.append((label, clause.strip()))
    return findings


def validate_responsibility_map(text: str, failures: list[str]) -> None:
    lines = text.splitlines()
    start = next(
        (
            index
            for index, line in enumerate(lines)
            if line.startswith("|") and "Decision or work" in line
        ),
        None,
    )
    table: list[str] = []
    if start is not None:
        for line in lines[start:]:
            if not line.startswith("|"):
                break
            table.append(line)
    header = table[0] if table else ""
    for column in ("Owner", "Co-owner", "Hermes", "Evidence"):
        if not re.search(rf"\|\s*{re.escape(column)}\s*(?=\|)", header, re.IGNORECASE):
            failures.append(f"responsibility map missing {column} column")
    row_names = {
        cells[0].strip().casefold()
        for line in table[2:]
        if len(cells := line.strip("|").split("|")) >= 4
    }
    for decision in (
        "mission and offer",
        "customer promise",
        "contract acceptance",
        "price or discount",
        "payment or refund",
        "bookkeeping classification and tax",
        "customer-data access",
        "incident stop",
    ):
        if decision.casefold() not in row_names:
            failures.append(f"responsibility map missing decision: {decision}")


def validate_trajectory(diagram: str, name: str, failures: list[str]) -> None:
    if name == "lead-to-customer":
        required = (("I", "Q"), ("Q", "R"), ("R", "D"), ("D", "A"), ("A", "S"), ("S", "P"), ("P", "M"))
        bypasses = (("D", "S"), ("R", "S"), ("Q", "S"))
    elif name == "content-to-campaign":
        required = (("B", "E"), ("E", "D"), ("D", "F"), ("F", "A"), ("A", "P"), ("P", "R"), ("R", "M"))
        bypasses = (("D", "P"), ("E", "P"), ("F", "P"))
    else:
        failures.append(f"unknown trajectory: {name}")
        return
    edges = set(
        re.findall(
            r"(?m)^\s*([A-Za-z][A-Za-z0-9_]*)[^\n]*?-->\s*([A-Za-z][A-Za-z0-9_]*)",
            diagram,
        )
    )
    for edge in required:
        if edge not in edges:
            failures.append(f"{name} trajectory missing edge: {edge[0]} --> {edge[1]}")
    if any(edge in edges for edge in bypasses):
        failures.append(f"{name} trajectory bypasses owner approval")

    labels = {
        node: label.strip().casefold()
        for node, label in re.findall(
            r'\b([A-Za-z][A-Za-z0-9_]*)\["([^"\n]+)"\]', diagram
        )
    }
    action_node = "S" if name == "lead-to-customer" else "P"
    receipt_node = "P" if name == "lead-to-customer" else "R"
    approval = labels.get("A", "")
    if (
        "approval" not in approval
        or not re.search(r"\b(?:owner|human)\b", approval)
        or re.search(r"\b(?:hermes|agent|auto(?:matic)?(?:ally)?)\b", approval)
    ):
        failures.append(f"{name} trajectory approval must belong to a human owner")

    action = labels.get(action_node, "")
    action_words = r"send|accept|publish|schedule"
    if (
        not re.search(r"\bhuman\b", action)
        or not re.search(rf"\b(?:{action_words})", action)
        or re.search(r"\b(?:hermes|agent|auto(?:matic)?(?:ally)?)\b", action)
    ):
        failures.append(f"{name} trajectory consequential action must belong to a human")

    receipt = labels.get(receipt_node, "")
    if "receipt" not in receipt or not re.search(
        r"\b(?:read[- ]?back|verif(?:y|ied|ication))\b", receipt
    ):
        failures.append(
            f"{name} trajectory missing receipt and read-back/verification label"
        )

    if not re.search(r"\bmetrics?\b", labels.get("M", "")):
        failures.append(f"{name} trajectory missing metrics label")


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
    found = result.stdout.strip() or "unreadable"
    if result.returncode != 0 or found != PINNED_COMMIT:
        failures.append(f"wrong pinned Hermes commit: expected {PINNED_COMMIT}, found {found}")
    for relative_path, assertion in PINNED_SOURCE_ASSERTIONS:
        path = source / relative_path
        if not path.is_file():
            failures.append(f"missing pinned source path: {relative_path}")
        elif assertion not in path.read_text(encoding="utf-8"):
            failures.append(f"missing pinned source assertion: {relative_path}: {assertion}")


def _extract_marked_diagram(text: str, marker: str) -> str:
    match = re.search(
        rf"{re.escape(marker)}.*?(```mermaid.*?```)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return match.group(1) if match else ""


def audit_task9(root: Path, hermes_source: Path | None = None) -> list[str]:
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
                f"word count out of range: {relative_path}: {minimum}–{maximum} (found {words})"
            )
    if len(content) != len(CHAPTERS):
        return failures

    chapter_19 = content["docs/part-5/19-one-two-person-business-os.md"]
    chapter_20 = content["docs/part-5/20-business-functions.md"]
    combined = chapter_19 + "\n" + chapter_20

    for phrase in (
        "MISSION AND OFFER REGISTER",
        "CUSTOMER PROMISE REGISTER",
        "SHARED GLOSSARY",
        "SYSTEM OF RECORD REGISTER",
        "PROJECT CHARTER",
        "KANBAN POLICY",
        "MEETING CONTRACT",
        "DECISION LOG",
        "SOP LIBRARY",
        "RISK REGISTER",
        "FINANCE HANDOFF: PREPARED / REVIEWED",
        "RESPONSIBILITY MAP",
    ):
        label = "finance handoff gate" if phrase.startswith("FINANCE HANDOFF") else "Chapter 19 business-OS contract"
        require(chapter_19, phrase, label, failures)
    validate_responsibility_map(chapter_19, failures)

    for phrase in (
        "RESEARCH PLAYBOOK",
        "SALES PLAYBOOK",
        "CRM PLAYBOOK",
        "MARKETING PLAYBOOK",
        "CONTENT PLAYBOOK",
        "SUPPORT PLAYBOOK",
        "PROJECT PLAYBOOK",
        "OPERATIONS PLAYBOOK",
        "BOOKKEEPING-PREPARATION PLAYBOOK",
        "TRAJECTORY: LEAD TO CUSTOMER",
        "TRAJECTORY: CONTENT TO CAMPAIGN",
        "evidence packet",
        "approval object",
        "provider receipt",
        "conversion metric",
        "quality metric",
        "privacy metric",
        "- **Native Hermes:**",
        "- **Bundled Hermes skills:**",
        "- **MCP or custom work:**",
        "- **Human/manual:**",
    ):
        if phrase == "TRAJECTORY: LEAD TO CUSTOMER":
            label = "lead-to-customer trajectory"
        elif phrase == "TRAJECTORY: CONTENT TO CAMPAIGN":
            label = "content-to-campaign trajectory"
        else:
            label = "Chapter 20 functional-playbook contract"
        require(chapter_20, phrase, label, failures)

    lead_diagram = _extract_marked_diagram(chapter_20, "TRAJECTORY: LEAD TO CUSTOMER")
    campaign_diagram = _extract_marked_diagram(chapter_20, "TRAJECTORY: CONTENT TO CAMPAIGN")
    validate_trajectory(lead_diagram, "lead-to-customer", failures)
    validate_trajectory(campaign_diagram, "content-to-campaign", failures)

    for label, clause in find_unsafe_authorizations(combined):
        failures.append(f"unsafe authorization: {label}: {clause}")

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
    failures = audit_task9(args.root.resolve(), args.hermes_source)
    for failure in failures:
        print(f"ERROR: {failure}")
    status = "OK" if not failures else "FAILED"
    source_status = "verified" if args.hermes_source else "reference paths checked"
    print(f"check_task9: {status} — {len(CHAPTERS)} chapters; pinned source {source_status}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
