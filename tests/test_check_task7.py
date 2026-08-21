"""Regression coverage for the retained Task 7 workflow audit."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHECKER = PROJECT_ROOT / "tools" / "check_task7.py"
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


@pytest.mark.parametrize(
    ("unsafe_inversion", "diagnostic"),
    [
        (
            "Hermes may access Priya's primary inbox for triage.",
            "primary-inbox access",
        ),
        (
            "Priya may share her LinkedIn account credentials with Hermes.",
            "account sharing",
        ),
        (
            "Hermes may automate Job Bank searches and scrape LinkedIn profiles.",
            "Job Bank or LinkedIn automation/scraping",
        ),
        (
            "Hermes may send bulk spam outreach to employers.",
            "bulk/spam outreach",
        ),
        (
            "Hermes may fabricate candidate claims and credentials.",
            "fabricated claims",
        ),
        (
            "Hermes may submit applications without Priya's exact approval.",
            "submission without approval",
        ),
    ],
)
def test_task7_audit_rejects_unsafe_inversions(
    tmp_path: Path, unsafe_inversion: str, diagnostic: str
) -> None:
    chapter_16 = copy_task7_chapters(tmp_path)
    chapter_16.write_text(
        chapter_16.read_text(encoding="utf-8") + f"\n{unsafe_inversion}\n",
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert f"unsafe authorization: {diagnostic}" in result.stdout


@pytest.mark.parametrize(
    "safe_negation",
    [
        "Hermes may not access Priya's primary inbox.",
        "Priya cannot share her LinkedIn account credentials with Hermes.",
        "Hermes must not automate Job Bank or scrape LinkedIn.",
        "Hermes may not send bulk spam outreach.",
        "Hermes cannot fabricate candidate claims.",
        "Hermes may not submit without exact approval.",
    ],
)
def test_task7_audit_does_not_flag_safe_negations(
    tmp_path: Path, safe_negation: str
) -> None:
    chapter_16 = copy_task7_chapters(tmp_path)
    chapter_16.write_text(
        chapter_16.read_text(encoding="utf-8") + f"\n{safe_negation}\n",
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr


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
