"""Regression coverage for the retained Task 7 workflow audit."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHECKER = PROJECT_ROOT / "tools" / "check_task7.py"
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from check_task7 import find_unsafe_authorizations  # noqa: E402


CHAPTER_PATHS = (
    "docs/part-4/15-daily-weekly-operating-rhythms.md",
    "docs/part-4/16-job-search-opportunity-pipeline.md",
)
CHAPTER_16 = CHAPTER_PATHS[1]
OFFICIAL_REFERENCES = (
    "https://www.jobbank.gc.ca/termsofuse-seeker.xhtml",
    "https://www.jobbank.gc.ca/jobsearch/",
    "https://www.linkedin.com/legal/user-agreement",
    "https://www.linkedin.com/help/linkedin/answer/a1341387/prohibited-software-and-extensions",
    "https://antifraudcentre-centreantifraude.ca/scams-fraudes/job-emploi-eng.htm",
)


def run_check(book_root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(book_root)],
        check=False,
        capture_output=True,
        text=True,
    )


def copy_task7_chapters(tmp_path: Path) -> Path:
    for relative_path in CHAPTER_PATHS:
        destination = tmp_path / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PROJECT_ROOT / relative_path, destination)
    return tmp_path / CHAPTER_16


def test_task7_chief_of_staff_and_job_search_contract() -> None:
    """Catch weakened inbox, platform, capability, claim, and state controls."""
    result = subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(PROJECT_ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "check_task7: OK" in result.stdout


def test_task7_audit_rejects_an_end_to_end_unsafe_inbox_mutation(tmp_path: Path) -> None:
    chapter_16 = copy_task7_chapters(tmp_path)
    chapter_16.write_text(
        chapter_16.read_text(encoding="utf-8")
        + "\nHermes may manage the family's primary mailboxes.\n",
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "unsafe authorization: primary-inbox access" in result.stdout


@pytest.mark.parametrize(
    ("diagnostic", "unsafe_paraphrase"),
    [
        ("primary-inbox access", "Hermes may access Priya's primary inbox for triage."),
        ("primary-inbox access", "Hermes can monitor both primary inboxes."),
        ("primary-inbox access", "Hermes is allowed to manage the family's primary mailboxes."),
        ("account sharing", "Priya may share her LinkedIn account credentials with Hermes."),
        ("account sharing", "Hermes can control Priya's Job Bank account."),
        ("account sharing", "Priya may let Hermes use her LinkedIn account."),
        (
            "Job Bank or LinkedIn automation/scraping",
            "Hermes may automate Job Bank searches and scrape LinkedIn profiles.",
        ),
        (
            "Job Bank or LinkedIn automation/scraping",
            "Hermes automatically queries Job Bank every morning.",
        ),
        (
            "Job Bank or LinkedIn automation/scraping",
            "Hermes can automatically access LinkedIn to collect new roles.",
        ),
        ("bulk/spam outreach", "Hermes may send bulk spam outreach to employers."),
        ("bulk/spam outreach", "Hermes can blast hundreds of identical messages."),
        ("bulk/spam outreach", "Hermes is allowed to generate blanket outreach emails."),
        ("fabricated claims", "Hermes may fabricate candidate claims and credentials."),
        ("fabricated claims", "Hermes can embellish Priya's experience."),
        ("fabricated claims", "Hermes is permitted to make up qualifications."),
        (
            "submission without approval",
            "Hermes may submit applications without Priya's exact approval.",
        ),
        (
            "submission without approval",
            "Hermes can file an application before candidate sign-off.",
        ),
        (
            "submission without approval",
            "Hermes submits applications by default unless Priya opts out.",
        ),
        (
            "submission without approval",
            "Applications are submitted automatically unless the candidate opts out.",
        ),
        (
            "submission without approval",
            "Hermes may send candidate materials autonomously.",
        ),
    ],
)
def test_authorization_scanner_rejects_realistic_unsafe_paraphrases(
    diagnostic: str, unsafe_paraphrase: str
) -> None:
    findings = find_unsafe_authorizations(unsafe_paraphrase)

    assert diagnostic in {label for label, _sentence in findings}


@pytest.mark.parametrize(
    "safe_negation",
    [
        "Hermes may not access Priya's primary inbox.",
        "Hermes cannot monitor the primary mailboxes.",
        "Priya must not share her LinkedIn account credentials with Hermes.",
        "Hermes cannot control Priya's Job Bank account.",
        "Hermes must not automate Job Bank queries or scrape LinkedIn.",
        "Hermes does not automatically access LinkedIn.",
        "Hermes may not send bulk spam outreach.",
        "Hermes cannot blast hundreds of messages.",
        "Hermes cannot fabricate candidate claims.",
        "Hermes must not embellish Priya's experience.",
        "Hermes may not submit applications without exact approval.",
        "Hermes does not submit applications by default or on an opt-out basis.",
    ],
)
def test_authorization_scanner_does_not_flag_explicit_negations(
    safe_negation: str,
) -> None:
    findings = find_unsafe_authorizations(safe_negation)

    assert findings == []


@pytest.mark.parametrize(
    "safe_coordination",
    [
        "Hermes may query public employers but must not scrape LinkedIn.",
        "Hermes may prepare applications while Priya submits them manually.",
        "Hermes may search employer pages; it must not automatically access LinkedIn.",
        "Hermes may draft outreach, but it cannot blast hundreds of messages.",
    ],
)
def test_authorization_scanner_binds_safe_coordination_locally(
    safe_coordination: str,
) -> None:
    assert find_unsafe_authorizations(safe_coordination) == []


@pytest.mark.parametrize(
    ("diagnostic", "unsafe_coordination"),
    [
        (
            "submission without approval",
            "Hermes may not draft but may submit applications without approval.",
        ),
        (
            "primary-inbox access",
            "Hermes may not only summarize notices but also access primary inboxes.",
        ),
        (
            "submission without approval",
            "Hermes may prepare applications; it may submit them without approval.",
        ),
        (
            "Job Bank or LinkedIn automation/scraping",
            "Hermes may query public employers while it can scrape LinkedIn.",
        ),
        (
            "bulk/spam outreach",
            "Hermes may draft one note; it may send blanket outreach messages.",
        ),
    ],
)
def test_authorization_scanner_finds_unsafe_adjacent_clauses_and_pronouns(
    diagnostic: str, unsafe_coordination: str
) -> None:
    findings = find_unsafe_authorizations(unsafe_coordination)

    assert diagnostic in {label for label, _clause in findings}


def test_authorization_scanner_does_not_guess_pronouns_across_sentences() -> None:
    prose = "Hermes may prepare applications. It may submit them without approval."

    assert find_unsafe_authorizations(prose) == []


@pytest.mark.parametrize("official_url", OFFICIAL_REFERENCES)
def test_task7_audit_requires_each_exact_official_reference_url(
    tmp_path: Path, official_url: str
) -> None:
    chapter_16 = copy_task7_chapters(tmp_path)
    contents = chapter_16.read_text(encoding="utf-8")
    chapter_16.write_text(
        contents.replace(official_url, "https://example.invalid/replaced", 1),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert f"missing exact official reference URL: {official_url}" in result.stdout


@pytest.mark.parametrize("official_url", OFFICIAL_REFERENCES)
def test_task7_audit_requires_a_visible_verification_date_for_each_official_reference(
    tmp_path: Path, official_url: str
) -> None:
    chapter_16 = copy_task7_chapters(tmp_path)
    lines = chapter_16.read_text(encoding="utf-8").splitlines()
    matching_index = next(index for index, line in enumerate(lines) if official_url in line)
    lines[matching_index] = lines[matching_index].replace("2026-08-21", "2026-08-20")
    chapter_16.write_text("\n".join(lines) + "\n", encoding="utf-8")

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert f"missing visible verification date: {official_url}" in result.stdout
