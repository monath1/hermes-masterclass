#!/usr/bin/env python3
"""Audit the retained specialist-management and 90-day capstone contracts."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from check_book import markdown_words


PINNED_COMMIT = "fcbd1076a93841fa88855acce810e342a5b78101"
CHAPTERS = {
    "docs/part-5/21-hermes-as-manager.md": (4400, 5000),
    "docs/part-6/22-evaluation-observability-capstone.md": (4800, 5300),
}
REQUIRED_PINNED_PATHS = {
    "website/docs/developer-guide/subagent-lifecycle-api.md",
    "website/docs/developer-guide/trajectory-format.md",
    "website/docs/guides/cron-troubleshooting.md",
    "website/docs/guides/delegation-patterns.md",
    "website/docs/guides/troubleshooting-agent-quality.md",
    "website/docs/user-guide/bot-mode.md",
    "website/docs/user-guide/checkpoints-and-rollback.md",
    "website/docs/user-guide/features/codex-app-server-runtime.md",
    "website/docs/user-guide/features/cron.md",
    "website/docs/user-guide/features/delegation.md",
    "website/docs/user-guide/features/fallback-providers.md",
    "website/docs/user-guide/features/goals.md",
    "website/docs/user-guide/features/mixture-of-agents.md",
    "website/docs/user-guide/features/provider-routing.md",
    "website/docs/user-guide/sessions.md",
    "website/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex.md",
}
PINNED_SOURCE_ASSERTIONS = (
    ("website/docs/user-guide/features/delegation.md", "completely fresh conversation"),
    ("website/docs/guides/delegation-patterns.md", "No conversation history"),
    ("website/docs/user-guide/bot-mode.md", "A Bot is a profile"),
    ("website/docs/user-guide/features/codex-app-server-runtime.md", "This is **opt-in only**"),
    ("website/docs/developer-guide/subagent-lifecycle-api.md", "The stable states are"),
    ("website/docs/user-guide/features/mixture-of-agents.md", "virtual model provider"),
    (
        "website/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex.md",
        "Delegate coding tasks",
    ),
    ("website/docs/user-guide/features/provider-routing.md", "only applies when using OpenRouter or Nous Portal"),
    ("website/docs/user-guide/features/fallback-providers.md", "turn-scoped"),
    ("website/docs/developer-guide/trajectory-format.md", "ShareGPT-compatible JSONL"),
    ("website/docs/user-guide/features/goals.md", "standing objective"),
    ("website/docs/guides/troubleshooting-agent-quality.md", "frozen memory snapshot"),
    ("website/docs/user-guide/checkpoints-and-rollback.md", "Checkpoints are **opt-in**"),
    ("website/docs/guides/cron-troubleshooting.md", "gateway's background ticker thread"),
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


def _edges(diagram: str) -> set[tuple[str, str]]:
    return set(
        re.findall(
            r"(?m)^\s*([A-Za-z][A-Za-z0-9_]*)[^\n]*?-->\s*(?:\|[^\n|]+\|\s*)?([A-Za-z][A-Za-z0-9_]*)",
            diagram,
        )
    )


def validate_delegation_flow(diagram: str, failures: list[str]) -> None:
    edges = _edges(diagram)
    required = (("O", "B"), ("B", "S"), ("S", "A"), ("A", "V"), ("V", "H"), ("H", "G"))
    for source, target in required:
        if (source, target) not in edges:
            failures.append(f"delegation flow missing edge: {source} --> {target}")
    if any(edge in edges for edge in (("S", "G"), ("A", "G"), ("S", "H"))):
        failures.append("delegation flow lets a specialist bypass verification and handback")


def validate_evidence_flow(diagram: str, failures: list[str]) -> None:
    edges = _edges(diagram)
    required = (("I", "R"), ("R", "C"), ("C", "V"), ("V", "S"), ("S", "G"), ("G", "K"))
    for source, target in required:
        if (source, target) not in edges:
            failures.append(f"evidence flow missing edge: {source} --> {target}")
    if ("G", "D") not in edges:
        failures.append("evidence flow missing failed-gate reduction path")


def _extract_first_diagram(text: str) -> str:
    match = re.search(r"```mermaid.*?```", text, flags=re.DOTALL)
    return match.group(0) if match else ""


def validate_capstone(chapter: str, failures: list[str]) -> None:
    positions: list[int] = []
    for label in (
        "Gate 1",
        "Gate 2",
        "Gate 3",
        "Gate 4",
        "Gate 5",
        "Gate 6 — qualification",
    ):
        match = re.search(rf"\*\*{re.escape(label)}\s*:", chapter, flags=re.IGNORECASE)
        if match is None:
            failures.append(f"missing capstone evidence gate: {label.upper()}")
        else:
            positions.append(match.start())
    if len(positions) == 6 and positions != sorted(positions):
        failures.append("capstone evidence gates are out of order")
    for phase in (
        "Days 1–15",
        "Days 16–30",
        "Days 31–45",
        "Days 46–60",
        "Days 61–75",
        "Days 76–90",
    ):
        require(chapter, phase, "90-day phase", failures)


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


def audit_task10(root: Path, hermes_source: Path | None = None) -> list[str]:
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

    chapter_21 = content["docs/part-5/21-hermes-as-manager.md"]
    chapter_22 = content["docs/part-6/22-evaluation-observability-capstone.md"]
    combined = chapter_21 + "\n" + chapter_22

    chapter_21_contract = (
        ("nine-part delegation contract", "delegation contract"),
        ("Hermes subagent", "temporary specialist"),
        ("Named Bot", "persistent specialist"),
        ("Codex specialist", "Codex boundary"),
        ("Mixture of Agents", "MoA distinction"),
        ("context boundary", "context boundary"),
        ("tool boundary", "tool boundary"),
        ("shared artifact", "shared artifact"),
        ("verification evidence", "verification evidence"),
        ("retry/fix loop", "retry/fix loop"),
        ("handback", "handback"),
        ("Keep delegation flat", "flat-roster control"),
        ("BOUNDED SPECIALIST ASSIGNMENT CARD", "field kit"),
    )
    for phrase, label in chapter_21_contract:
        require(chapter_21, phrase, label, failures)

    chapter_22_contract = (
        ("balanced operational scorecard", "operational scorecard"),
        ("Completion and correctness must be separate columns", "completion/correctness separation"),
        ("risk-weighted sampled reviews", "sampled review"),
        ("cost per accepted outcome", "cost measure"),
        ("Score escalation quality", "escalation quality"),
        ("memory and context drift", "memory drift"),
        ("automation failure", "automation failures"),
        ("incident review", "incident review"),
        ("Troubleshoot in a fixed order", "troubleshooting loop"),
        ("OPERATIONAL EVIDENCE AND CAPSTONE CARD", "field kit"),
        ("bounded digital employee", "bounded employee conclusion"),
    )
    for phrase, label in chapter_22_contract:
        require(chapter_22, phrase, label, failures)

    validate_delegation_flow(_extract_first_diagram(chapter_21), failures)
    validate_evidence_flow(_extract_first_diagram(chapter_22), failures)
    validate_capstone(chapter_22, failures)

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
    failures = audit_task10(args.root.resolve(), args.hermes_source)
    for failure in failures:
        print(f"ERROR: {failure}")
    status = "OK" if not failures else "FAILED"
    source_status = "verified" if args.hermes_source else "reference paths checked"
    print(f"check_task10: {status} — {len(CHAPTERS)} chapters; pinned source {source_status}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
