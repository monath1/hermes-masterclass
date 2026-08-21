"""Regression coverage for the retained Task 9 small-business audit."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHECKER = PROJECT_ROOT / "tools" / "check_task9.py"
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from check_task9 import (  # noqa: E402
    find_unsafe_authorizations,
    validate_responsibility_map,
    validate_trajectory,
)


CHAPTER_PATHS = (
    "docs/part-5/19-one-two-person-business-os.md",
    "docs/part-5/20-business-functions.md",
)


def run_check(book_root: Path, *, hermes_source: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(CHECKER), "--root", str(book_root)]
    if hermes_source is not None:
        command.extend(["--hermes-source", str(hermes_source)])
    return subprocess.run(command, check=False, capture_output=True, text=True)


def copy_task9_chapters(tmp_path: Path) -> tuple[Path, Path]:
    destinations: list[Path] = []
    for relative_path in CHAPTER_PATHS:
        destination = tmp_path / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PROJECT_ROOT / relative_path, destination)
        destinations.append(destination)
    return destinations[0], destinations[1]


def test_task9_business_contract() -> None:
    result = run_check(
        PROJECT_ROOT,
        hermes_source=Path("/tmp/hermes-agent-v2026.8.19"),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "check_task9: OK" in result.stdout


@pytest.mark.parametrize(
    ("diagnostic", "unsafe_paraphrase"),
    [
        ("contract or legal commitment", "Hermes may sign the customer contract."),
        ("contract or legal commitment", "The agent can accept the vendor agreement."),
        ("price or discount commitment", "Hermes may set prices and approve discounts."),
        ("money movement", "Hermes can charge the card and issue a refund."),
        ("customer promise", "The agent may promise delivery by Friday."),
        ("mass outreach", "Hermes can blast cold emails to every scraped lead."),
        ("deceptive marketing", "Hermes may fabricate testimonials for the campaign."),
        ("professional bookkeeping or tax decision", "The agent may classify expenses and file the tax return."),
    ],
)
def test_business_safety_scanner_rejects_forbidden_authority(
    diagnostic: str, unsafe_paraphrase: str
) -> None:
    findings = find_unsafe_authorizations(unsafe_paraphrase)

    assert diagnostic in {label for label, _clause in findings}


@pytest.mark.parametrize(
    "safe_boundary",
    [
        "Hermes may not sign contracts or accept vendor agreements.",
        "The agent cannot set prices or approve discounts.",
        "Hermes must not charge cards, move money, or issue refunds.",
        "Hermes may draft a reply, but it cannot promise delivery.",
        "The agent must not send mass outreach or scrape personal addresses.",
        "Hermes cannot fabricate testimonials or impersonate a customer.",
        "Hermes may organize receipts, but it may not classify expenses or file taxes.",
    ],
)
def test_business_safety_scanner_accepts_explicit_refusals(safe_boundary: str) -> None:
    assert find_unsafe_authorizations(safe_boundary) == []


@pytest.mark.parametrize(
    ("diagnostic", "mixed_clause"),
    [
        ("customer promise", "Hermes may draft a reply, but it can promise a delivery date."),
        ("money movement", "The agent cannot sign a contract, but it may issue the refund."),
        ("mass outreach", "Hermes must not invent testimonials; it can blast cold email."),
        (
            "professional bookkeeping or tax decision",
            "Hermes may organize receipts, although it may classify the expense for tax.",
        ),
    ],
)
def test_business_safety_scanner_binds_negation_to_the_local_clause(
    diagnostic: str, mixed_clause: str
) -> None:
    findings = find_unsafe_authorizations(mixed_clause)

    assert diagnostic in {label for label, _clause in findings}


def test_responsibility_map_requires_owner_co_owner_and_hermes() -> None:
    text = """
| Decision or work | Owner | Co-owner | Hermes | Evidence |
| --- | --- | --- | --- | --- |
| Mission and offer | A | C | Prepare | decision ID |
| Customer promise | A | C | Draft only | approval ID |
| Contract acceptance | A | C | Prohibited | signed copy |
| Price or discount | A | C | Prohibited | decision ID |
| Payment or refund | A | C | Prohibited | provider receipt |
| Bookkeeping classification and tax | A | C | Organize only | professional handoff |
| Customer-data access | A | C | Minimized | access review |
| Incident stop | A | C | Stop and escalate | incident ID |
"""
    failures: list[str] = []

    validate_responsibility_map(text, failures)

    assert failures == []


def test_responsibility_map_rejects_missing_co_owner_column() -> None:
    text = """
| Decision or work | Owner | Hermes | Evidence |
| --- | --- | --- | --- |
| Mission and offer | A | Prepare | decision ID |
| Customer promise | A | Draft only | approval ID |
| Contract acceptance | A | Prohibited | signed copy |
| Price or discount | A | Prohibited | decision ID |
| Payment or refund | A | Prohibited | provider receipt |
| Bookkeeping classification and tax | A | Organize only | professional handoff |
| Customer-data access | A | Minimized | access review |
| Incident stop | A | Stop and escalate | incident ID |
"""
    failures: list[str] = []

    validate_responsibility_map(text, failures)

    assert "responsibility map missing Co-owner column" in failures


@pytest.mark.parametrize(
    ("name", "diagram"),
    [
        (
            "lead-to-customer",
            """```mermaid
flowchart LR
    I["Permitted lead intake"] --> Q["Qualification"]
    Q --> R["Research and evidence"]
    R --> D["Draft"]
    D --> A["Owner approval"]
    A --> S["Human send or acceptance"]
    S --> P["Provider receipt"]
    P --> M["Metrics and review"]
```""",
        ),
        (
            "content-to-campaign",
            """```mermaid
flowchart LR
    B["Approved brief"] --> E["Evidence"]
    E --> D["Draft"]
    D --> F["Fact and policy review"]
    F --> A["Owner approval"]
    A --> P["Human publish or schedule"]
    P --> R["Platform receipt"]
    R --> M["Metrics and review"]
```""",
        ),
    ],
)
def test_trajectory_accepts_complete_approval_receipt_metric_chain(name: str, diagram: str) -> None:
    failures: list[str] = []

    validate_trajectory(diagram, name, failures)

    assert failures == []


def test_trajectory_rejects_a_bypassed_approval_seam() -> None:
    diagram = """```mermaid
flowchart LR
    I["Permitted lead intake"] --> Q["Qualification"]
    Q --> R["Research and evidence"]
    R --> D["Draft"]
    D --> A["Owner approval"]
    D --> S["Human send or acceptance"]
    S --> P["Provider receipt"]
    P --> M["Metrics and review"]
```"""
    failures: list[str] = []

    validate_trajectory(diagram, "lead-to-customer", failures)

    assert "lead-to-customer trajectory bypasses owner approval" in failures


def test_task9_audit_rejects_an_unsafe_customer_promise_mutation(tmp_path: Path) -> None:
    _chapter_19, chapter_20 = copy_task9_chapters(tmp_path)
    chapter_20.write_text(
        chapter_20.read_text(encoding="utf-8")
        + "\nHermes may promise delivery by Friday when the pipeline score is high.\n",
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "unsafe authorization: customer promise" in result.stdout


def test_task9_audit_requires_the_finance_handoff(tmp_path: Path) -> None:
    chapter_19, _chapter_20 = copy_task9_chapters(tmp_path)
    contents = chapter_19.read_text(encoding="utf-8")
    chapter_19.write_text(
        contents.replace("FINANCE HANDOFF: PREPARED / REVIEWED", "FINANCE PACKET: READY", 1),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "missing finance handoff gate" in result.stdout


def test_task9_audit_requires_both_end_to_end_trajectories(tmp_path: Path) -> None:
    _chapter_19, chapter_20 = copy_task9_chapters(tmp_path)
    contents = chapter_20.read_text(encoding="utf-8")
    chapter_20.write_text(
        contents.replace("TRAJECTORY: CONTENT TO CAMPAIGN", "CONTENT WORKFLOW", 1),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "missing content-to-campaign trajectory" in result.stdout
