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

from check_task8 import (  # noqa: E402
    OFFICIAL_SOURCE_CONTRACTS,
    fetch_official_source,
    find_undated_changeable_claims,
    find_unsafe_authorizations,
    validate_live_sources,
)


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


@pytest.mark.parametrize(
    ("diagnostic", "unsafe_paraphrase"),
    [
        (
            "fabricated career evidence",
            "Hermes organizes the evidence. It may invent a qualification.",
        ),
        (
            "unapproved career publishing",
            "The agent can publish the LinkedIn About without approval.",
        ),
        (
            "medical decision",
            "Hermes may not diagnose symptoms, but it can prescribe treatment.",
        ),
        (
            "financial decision",
            "The agent must not file taxes, but it may choose investments.",
        ),
        (
            "unapproved career publishing",
            "Hermes can prepare a resume; it may post the career profile.",
        ),
        (
            "bulk networking",
            "Hermes cannot send a draft, but it will blast networking outreach.",
        ),
    ],
)
def test_authorization_scanner_tracks_agent_antecedents_and_local_predicates(
    diagnostic: str, unsafe_paraphrase: str
) -> None:
    findings = find_unsafe_authorizations(unsafe_paraphrase)

    assert diagnostic in {label for label, _sentence in findings}


@pytest.mark.parametrize(
    "safe_paraphrase",
    [
        "Hermes may draft a resume, but it may not publish LinkedIn changes.",
        "The agent can organize tax records; it cannot file taxes.",
        "Hermes may not diagnose symptoms. It may organize appointment questions.",
        "Hermes reviews a budget. It must not move retirement money.",
        "The agent may draft a portfolio, but cannot post the portfolio.",
    ],
)
def test_authorization_scanner_accepts_local_negation_with_agent_antecedents(
    safe_paraphrase: str,
) -> None:
    assert find_unsafe_authorizations(safe_paraphrase) == []


@pytest.mark.parametrize(
    ("diagnostic", "mixed_predicates"),
    [
        (
            "tax filing",
            "Hermes may file taxes and is prohibited from retaining a raw child dossier.",
        ),
        (
            "tax filing",
            "Hermes may file taxes, although it must not retain a raw child dossier.",
        ),
        (
            "raw child dossier",
            "Hermes may retain a raw child dossier and is prohibited from filing taxes.",
        ),
        (
            "raw child dossier",
            "Although it must not file taxes, Hermes may retain a raw child dossier.",
        ),
        (
            "tax filing",
            "Hermes may file taxes, provided it does not retain a raw child dossier.",
        ),
        (
            "medical decision",
            "Hermes may diagnose symptoms unless it is prohibited from filing taxes.",
        ),
        (
            "raw child dossier",
            "Hermes may retain a raw child dossier, as long as it does not file taxes.",
        ),
    ],
)
def test_authorization_scanner_binds_modality_to_each_coordinated_predicate(
    diagnostic: str, mixed_predicates: str
) -> None:
    findings = find_unsafe_authorizations(mixed_predicates)

    assert diagnostic in {label for label, _sentence in findings}


@pytest.mark.parametrize(
    "required_refusal",
    [
        "Hermes must refuse to file taxes.",
        "The agent must decline to file the family's tax return.",
        "Hermes must avoid filing taxes.",
        "Hermes may prepare records, although it must not file taxes.",
        "Hermes may prepare records, provided it does not file taxes.",
        "Hermes can organize appointments unless it must not diagnose symptoms.",
        "Hermes may draft a form, as long as it cannot sign consent.",
    ],
)
def test_authorization_scanner_treats_required_refusals_as_safe(
    required_refusal: str,
) -> None:
    assert find_unsafe_authorizations(required_refusal) == []


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


def test_task8_audit_requires_every_career_artifact_to_enter_its_gate(tmp_path: Path) -> None:
    chapter_17, _chapter_18 = copy_task8_chapters(tmp_path)
    contents = chapter_17.read_text(encoding="utf-8")
    chapter_17.write_text(contents.replace("T --> GT", "T -.-> GT", 1), encoding="utf-8")

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "missing Chapter 17 per-artifact evidence-gate flow" in result.stdout


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


@pytest.mark.parametrize(
    ("unsafe_green_action", "diagnostic"),
    [
        ("provide medical, financial, and tax advice; ", "professional advice"),
        ("diagnose symptoms; ", "medical action"),
        ("treat injuries; ", "medical action"),
        ("prescribe medication; ", "medical action"),
        ("dispense medical advice; ", "medical action"),
        ("triage emergencies; ", "medical action"),
        ("set therapeutic diets; ", "medical action"),
        ("decide return-to-play; ", "medical action"),
        ("file taxes; ", "tax filing"),
        ("submit tax returns; ", "tax filing"),
        ("choose investments; ", "investment or benefit decision"),
        ("recommend investments; ", "investment or benefit decision"),
        ("choose benefits; ", "investment or benefit decision"),
        ("recommend benefits; ", "investment or benefit decision"),
        ("sign consent forms; ", "consent or rights"),
        ("consent to travel; ", "consent or rights"),
        ("waive family rights; ", "consent or rights"),
        ("compile raw child dossiers; ", "raw child dossier"),
        ("use primary credentials; ", "primary credential"),
        ("access CRA accounts; ", "protected account access"),
        ("impersonate a guardian; ", "impersonation"),
        ("apply for benefits; ", "benefit application"),
        ("move money; ", "money movement"),
        ("book travel; ", "travel booking"),
        ("accept terms; ", "terms acceptance"),
        ("disclose across profiles; ", "cross-profile disclosure"),
        ("infer eligibility and custody; ", "sensitive inference"),
    ],
)
def test_task8_audit_semantically_rejects_unsafe_green_family_authority(
    tmp_path: Path, unsafe_green_action: str, diagnostic: str
) -> None:
    _chapter_17, chapter_18 = copy_task8_chapters(tmp_path)
    contents = chapter_18.read_text(encoding="utf-8")
    chapter_18.write_text(
        contents.replace(
            "| **Green — may act** | Read approved",
            f"| **Green — may act** | {unsafe_green_action}Read approved",
            1,
        ),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert f"unsafe Chapter 18 Green authority: {diagnostic}" in result.stdout


def test_task8_audit_semantically_rejects_hermes_as_professional_decider(
    tmp_path: Path,
) -> None:
    _chapter_17, chapter_18 = copy_task8_chapters(tmp_path)
    contents = chapter_18.read_text(encoding="utf-8")
    chapter_18.write_text(
        contents.replace(
            "Decide: taxpayer or authorized accountant/tax professional; CRA where needed.",
            "Decide: Hermes; CRA where needed.",
            1,
        ),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "unsafe Chapter 18 professional handoff decision owner" in result.stdout


def test_task8_audit_rejects_diagnosis_bearing_shared_index_metadata(tmp_path: Path) -> None:
    _chapter_17, chapter_18 = copy_task8_chapters(tmp_path)
    contents = chapter_18.read_text(encoding="utf-8")
    chapter_18.write_text(
        contents.replace("provider-plan update", "asthma-plan update", 1),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "diagnosis-bearing sample metadata" in result.stdout


def test_task8_audit_requires_the_pinned_xlsx_reference(tmp_path: Path) -> None:
    chapter_17, chapter_18 = copy_task8_chapters(tmp_path)
    pinned_path = (
        "website/docs/user-guide/skills/bundled/productivity/productivity-xlsx.md"
    )
    target = chapter_18 if pinned_path in chapter_18.read_text(encoding="utf-8") else chapter_17
    target.write_text(
        target.read_text(encoding="utf-8").replace(pinned_path, "missing-xlsx.md", 1),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert f"missing pinned reference URL: {pinned_path}" in result.stdout


@pytest.mark.parametrize(
    ("claim", "diagnostic"),
    [
        ("The benefit pays C$500 per month.", "Canadian dollar amount"),
        ("The tax filing deadline is April 30.", "Canadian deadline"),
        ("Families must keep tax records for six years.", "Canadian threshold"),
        ("The tax credit is 15% of the eligible amount.", "Canadian threshold"),
    ],
)
def test_changeable_claim_scan_rejects_undated_numeric_facts(
    claim: str, diagnostic: str
) -> None:
    findings = find_undated_changeable_claims(claim)

    assert diagnostic in {label for label, _paragraph in findings}


@pytest.mark.parametrize(
    "safe_claim",
    [
        "For the 2026 tax year, the filing deadline is April 30, 2027; checked 2026-08-21.",
        "The six-year CRA retention example was verified on 2026-08-21.",
        "Review the household budget every two weeks as a family-selected operating policy.",
        "Use a C$500 planning cap as an owner-selected operational policy, not a benefit amount.",
    ],
)
def test_changeable_claim_scan_accepts_dated_facts_and_operational_policy_exemptions(
    safe_claim: str,
) -> None:
    assert find_undated_changeable_claims(safe_claim) == []


@pytest.mark.parametrize(
    "unrelated_context",
    [
        "The unrelated retention example was checked on 2026-08-21.",
        "A weekly review is a family-selected operating policy.",
    ],
)
def test_changeable_claim_scan_does_not_apply_distant_context_to_numeric_claim(
    unrelated_context: str,
) -> None:
    filler = " ".join(["Unrelated background material."] * 30)
    claim = f"The benefit pays C$500 monthly. {filler} {unrelated_context}"

    findings = find_undated_changeable_claims(claim)

    assert "Canadian dollar amount" in {label for label, _paragraph in findings}


@pytest.mark.parametrize(
    "nearby_but_unrelated_context",
    [
        "The six-year retention threshold was checked on 2026-08-21.",
        "A weekly review is an owner-selected operating policy.",
    ],
)
def test_changeable_claim_scan_requires_semantic_binding_for_nearby_markers(
    nearby_but_unrelated_context: str,
) -> None:
    claim = f"The benefit pays C$500 monthly. {nearby_but_unrelated_context}"

    findings = find_undated_changeable_claims(claim)

    assert "Canadian dollar amount" in {label for label, _paragraph in findings}


@pytest.mark.parametrize(
    "wrong_category_marker",
    [
        "The benefit pays C$500 monthly; the six-year retention threshold was checked on 2026-08-21.",
        "The benefit pays C$500 monthly, and a weekly review is an owner-selected operating policy.",
    ],
)
def test_changeable_claim_scan_requires_same_clause_and_category_marker(
    wrong_category_marker: str,
) -> None:
    findings = find_undated_changeable_claims(wrong_category_marker)

    assert "Canadian dollar amount" in {label for label, _paragraph in findings}


@pytest.mark.parametrize(
    "bound_marker",
    [
        "The benefit amount was C$500, checked on 2026-08-21.",
        "The owner selected a C$500 planning cap as an owner-selected operating policy.",
    ],
)
def test_changeable_claim_scan_accepts_same_clause_and_category_marker(
    bound_marker: str,
) -> None:
    assert find_undated_changeable_claims(bound_marker) == []


def test_task8_audit_rejects_wrong_category_marker_mutation(tmp_path: Path) -> None:
    _chapter_17, chapter_18 = copy_task8_chapters(tmp_path)
    mutation = (
        "The benefit pays C$500 monthly; the six-year retention threshold was "
        "checked on 2026-08-21."
    )
    chapter_18.write_text(
        chapter_18.read_text(encoding="utf-8").replace(
            "\n## References", f"\n{mutation}\n\n## References", 1
        ),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "undated Canadian dollar amount" in result.stdout


def test_task8_audit_rejects_distant_date_hiding_undated_threshold(
    tmp_path: Path,
) -> None:
    _chapter_17, chapter_18 = copy_task8_chapters(tmp_path)
    filler = " ".join(["Background note."] * 30)
    mutation = (
        "Families must keep benefit records for seven years. "
        f"{filler} An unrelated source was checked on 2026-08-21."
    )
    chapter_18.write_text(
        chapter_18.read_text(encoding="utf-8").replace(
            "\n## References", f"\n{mutation}\n\n## References", 1
        ),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "undated Canadian threshold" in result.stdout


def test_task8_audit_rejects_an_undated_canadian_amount_mutation(tmp_path: Path) -> None:
    _chapter_17, chapter_18 = copy_task8_chapters(tmp_path)
    chapter_18.write_text(
        chapter_18.read_text(encoding="utf-8").replace(
            "\n## References",
            "\nThe federal benefit pays C$500 per month.\n\n## References",
            1,
        ),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "undated Canadian dollar amount" in result.stdout


def test_live_source_contract_accepts_declared_domains_and_content() -> None:
    bodies = {
        contract.url: " | ".join(contract.assertions)
        for contract in OFFICIAL_SOURCE_CONTRACTS
    }
    failures: list[str] = []

    validate_live_sources(failures, lambda url, _domain: (url, bodies[url]))

    assert failures == []


def test_live_source_contract_rejects_redirect_outside_declared_domain() -> None:
    bodies = {
        contract.url: " | ".join(contract.assertions)
        for contract in OFFICIAL_SOURCE_CONTRACTS
    }
    first_url = OFFICIAL_SOURCE_CONTRACTS[0].url
    failures: list[str] = []

    validate_live_sources(
        failures,
        lambda url, _domain: (
            "https://example.invalid/redirect" if url == first_url else url,
            bodies[url],
        ),
    )

    assert any("redirected outside allowed domain" in failure for failure in failures)


def test_live_source_contract_rejects_non_default_port_from_fetcher() -> None:
    bodies = {
        contract.url: " | ".join(contract.assertions)
        for contract in OFFICIAL_SOURCE_CONTRACTS
    }
    first_url = OFFICIAL_SOURCE_CONTRACTS[0].url
    failures: list[str] = []

    validate_live_sources(
        failures,
        lambda url, _domain: (
            "https://www.jobbank.gc.ca:8443/trap" if url == first_url else url,
            bodies[url],
        ),
    )

    assert any("non-default HTTPS port" in failure for failure in failures)


def test_live_source_contract_rejects_missing_load_bearing_content() -> None:
    first_url = OFFICIAL_SOURCE_CONTRACTS[0].url
    bodies = {
        contract.url: " | ".join(contract.assertions)
        for contract in OFFICIAL_SOURCE_CONTRACTS
    }
    bodies[first_url] = "A reachable page with unrelated content."
    failures: list[str] = []

    validate_live_sources(failures, lambda url, _domain: (url, bodies[url]))

    assert any("missing live source content assertion" in failure for failure in failures)


def test_live_fetch_follows_safe_relative_redirect_and_requires_2xx() -> None:
    responses = {
        "https://www.ontario.ca/start": (
            302,
            "https://www.ontario.ca/start",
            {"location": "/page/school-year-calendars"},
            "",
        ),
        "https://www.ontario.ca/page/school-year-calendars": (
            200,
            "https://www.ontario.ca/page/school-year-calendars",
            {},
            "School year calendars and school boards",
        ),
    }
    requested: list[str] = []

    def transport(url: str, _timeout: float) -> tuple[int, str, dict[str, str], str]:
        requested.append(url)
        return responses[url]

    final_url, body = fetch_official_source(
        "https://www.ontario.ca/start",
        "ontario.ca",
        transport=transport,
        max_redirects=3,
        total_timeout=5,
    )

    assert final_url == "https://www.ontario.ca/page/school-year-calendars"
    assert body == "School year calendars and school boards"
    assert requested == [
        "https://www.ontario.ca/start",
        "https://www.ontario.ca/page/school-year-calendars",
    ]


@pytest.mark.parametrize("status", [400, 404, 500, 503])
def test_live_fetch_rejects_non_2xx_terminal_status(status: int) -> None:
    def transport(url: str, _timeout: float) -> tuple[int, str, dict[str, str], str]:
        return status, url, {}, "Error page"

    with pytest.raises(RuntimeError, match=f"HTTP {status}"):
        fetch_official_source(
            "https://www.ontario.ca/failure",
            "ontario.ca",
            transport=transport,
        )


def test_live_fetch_rejects_off_domain_intermediate_before_following() -> None:
    requested: list[str] = []

    def transport(url: str, _timeout: float) -> tuple[int, str, dict[str, str], str]:
        requested.append(url)
        return 302, url, {"location": "https://example.invalid/trap"}, ""

    with pytest.raises(RuntimeError, match="outside allowed domain"):
        fetch_official_source(
            "https://www.ontario.ca/start",
            "ontario.ca",
            transport=transport,
        )

    assert requested == ["https://www.ontario.ca/start"]


def test_live_fetch_rejects_off_domain_effective_final_url() -> None:
    def transport(_url: str, _timeout: float) -> tuple[int, str, dict[str, str], str]:
        return 200, "https://example.invalid/final", {}, "Unexpected page"

    with pytest.raises(RuntimeError, match="outside allowed domain"):
        fetch_official_source(
            "https://www.ontario.ca/start",
            "ontario.ca",
            transport=transport,
        )


def test_live_fetch_rejects_insecure_redirect_and_redirect_overflow() -> None:
    def insecure_transport(
        url: str, _timeout: float
    ) -> tuple[int, str, dict[str, str], str]:
        return 302, url, {"location": "http://www.ontario.ca/insecure"}, ""

    with pytest.raises(RuntimeError, match="HTTPS"):
        fetch_official_source(
            "https://www.ontario.ca/start",
            "ontario.ca",
            transport=insecure_transport,
        )

    def looping_transport(
        url: str, _timeout: float
    ) -> tuple[int, str, dict[str, str], str]:
        return 302, url, {"location": "/loop"}, ""

    with pytest.raises(RuntimeError, match="redirect limit"):
        fetch_official_source(
            "https://www.ontario.ca/start",
            "ontario.ca",
            transport=looping_transport,
            max_redirects=2,
        )


@pytest.mark.parametrize(
    "url",
    [
        "https://www.ontario.ca:444/start",
        "https://www.ontario.ca:8443/start",
    ],
)
def test_live_fetch_rejects_non_default_https_ports_before_request(url: str) -> None:
    requested: list[str] = []

    def transport(
        target: str, _timeout: float
    ) -> tuple[int, str, dict[str, str], str]:
        requested.append(target)
        return 200, target, {}, "Unexpected"

    with pytest.raises(RuntimeError, match="non-default HTTPS port"):
        fetch_official_source(url, "ontario.ca", transport=transport)

    assert requested == []


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
