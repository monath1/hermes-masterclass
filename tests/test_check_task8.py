"""Regression coverage for the retained Task 8 career and family audit."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHECKER = PROJECT_ROOT / "tools" / "check_task8.py"
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from check_task8 import find_unsafe_authorizations  # noqa: E402


CHAPTER_PATHS = (
    "docs/part-4/17-resume-interview-brand.md",
    "docs/part-4/18-family-operations-canada.md",
)
CHAPTER_17 = CHAPTER_PATHS[0]
CHAPTER_18 = CHAPTER_PATHS[1]
OFFICIAL_REFERENCES = (
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


def run_check(book_root: Path, *, hermes_source: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(CHECKER), "--root", str(book_root)]
    if hermes_source is not None:
        command.extend(["--hermes-source", str(hermes_source)])
    return subprocess.run(command, check=False, capture_output=True, text=True)


def copy_task8_chapters(tmp_path: Path) -> tuple[Path, Path]:
    destinations: list[Path] = []
    for relative_path in CHAPTER_PATHS:
        destination = tmp_path / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PROJECT_ROOT / relative_path, destination)
        destinations.append(destination)
    return destinations[0], destinations[1]


def test_task8_career_and_family_contract() -> None:
    """Catch weakened truth, child-data, advice, and source controls."""
    result = run_check(
        PROJECT_ROOT,
        hermes_source=Path("/tmp/hermes-agent-v2026.8.19"),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "check_task8: OK" in result.stdout


@pytest.mark.parametrize(
    ("diagnostic", "unsafe_paraphrase"),
    [
        ("fabricated career evidence", "Hermes may invent achievements for Priya."),
        ("fabricated career evidence", "Hermes can embellish unsupported results."),
        ("unapproved career publishing", "Hermes may publish the LinkedIn rewrite without review."),
        ("bulk networking", "Hermes can send bulk networking messages to strangers."),
        ("candidate impersonation", "Hermes may answer the live interview for Priya."),
        ("medical decision", "Hermes may diagnose a child's symptoms."),
        ("medical decision", "Hermes can prescribe a family fitness treatment plan."),
        ("tax filing", "Hermes may file the family's tax returns."),
        ("financial decision", "Hermes can choose investments and move retirement money."),
        ("primary credential access", "Hermes may log in to CRA with Priya's primary credentials."),
        ("raw child dossier", "Hermes can maintain a complete child health dossier."),
        ("school or travel consent", "Hermes may sign school and travel consent forms."),
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
        "Hermes may not invent achievements for Priya.",
        "Hermes cannot publish the LinkedIn rewrite without review.",
        "Hermes must not send bulk networking messages.",
        "Hermes may not answer the live interview for Priya.",
        "Hermes cannot diagnose symptoms or prescribe treatment.",
        "Hermes may not file tax returns or choose investments.",
        "Hermes must not log in to CRA with primary credentials.",
        "Hermes cannot maintain a raw child dossier or sign school consent.",
    ],
)
def test_authorization_scanner_does_not_flag_explicit_negations(safe_negation: str) -> None:
    assert find_unsafe_authorizations(safe_negation) == []


def test_task8_audit_rejects_an_end_to_end_unsafe_child_data_mutation(tmp_path: Path) -> None:
    _chapter_17, chapter_18 = copy_task8_chapters(tmp_path)
    chapter_18.write_text(
        chapter_18.read_text(encoding="utf-8")
        + "\nHermes may maintain a complete child health dossier for convenience.\n",
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "unsafe authorization: raw child dossier" in result.stdout


def test_task8_audit_requires_the_evidence_gate(tmp_path: Path) -> None:
    chapter_17, _chapter_18 = copy_task8_chapters(tmp_path)
    contents = chapter_17.read_text(encoding="utf-8")
    chapter_17.write_text(
        contents.replace("EVIDENCE GATE: PASS / HOLD", "CAREER REVIEW: PASS / HOLD", 1),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "missing Chapter 17 anti-hallucination evidence gate" in result.stdout


def test_task8_audit_requires_professional_handoffs(tmp_path: Path) -> None:
    _chapter_17, chapter_18 = copy_task8_chapters(tmp_path)
    contents = chapter_18.read_text(encoding="utf-8")
    chapter_18.write_text(
        contents.replace("PROFESSIONAL HANDOFF MATRIX", "SPECIALIST CONTACT MATRIX", 1),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "missing Chapter 18 professional-handoff matrix" in result.stdout


@pytest.mark.parametrize("official_url", OFFICIAL_REFERENCES)
def test_task8_audit_requires_each_exact_official_reference_url(
    tmp_path: Path, official_url: str
) -> None:
    _chapter_17, chapter_18 = copy_task8_chapters(tmp_path)
    contents = chapter_18.read_text(encoding="utf-8")
    target = chapter_18
    if official_url not in contents:
        target = tmp_path / CHAPTER_17
        contents = target.read_text(encoding="utf-8")
    target.write_text(
        contents.replace(official_url, "https://example.invalid/replaced", 1),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert f"missing exact official reference URL: {official_url}" in result.stdout


@pytest.mark.parametrize("official_url", OFFICIAL_REFERENCES)
def test_task8_audit_requires_a_visible_verification_date_for_each_official_reference(
    tmp_path: Path, official_url: str
) -> None:
    chapter_17, chapter_18 = copy_task8_chapters(tmp_path)
    target = chapter_18 if official_url in chapter_18.read_text(encoding="utf-8") else chapter_17
    lines = target.read_text(encoding="utf-8").splitlines()
    matching_index = next(index for index, line in enumerate(lines) if official_url in line)
    lines[matching_index] = lines[matching_index].replace("2026-08-21", "2026-08-20")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert f"missing visible verification date: {official_url}" in result.stdout


def test_task8_audit_rejects_the_wrong_pinned_hermes_source(tmp_path: Path) -> None:
    copy_task8_chapters(tmp_path)
    fake_source = tmp_path / "fake-hermes"
    fake_source.mkdir()

    result = run_check(tmp_path, hermes_source=fake_source)

    assert result.returncode == 1
    assert "wrong pinned Hermes commit" in result.stdout
