"""Regression coverage for the retained Task 10 management/capstone audit."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHECKER = PROJECT_ROOT / "tools" / "check_task10.py"
sys.path.insert(0, str(PROJECT_ROOT / "tools"))


CHAPTER_PATHS = (
    "docs/part-5/21-hermes-as-manager.md",
    "docs/part-6/22-evaluation-observability-capstone.md",
)


def run_check(book_root: Path, *, hermes_source: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(CHECKER), "--root", str(book_root)]
    if hermes_source is not None:
        command.extend(["--hermes-source", str(hermes_source)])
    return subprocess.run(command, check=False, capture_output=True, text=True)


def copy_task10_chapters(tmp_path: Path) -> tuple[Path, Path]:
    destinations: list[Path] = []
    for relative_path in CHAPTER_PATHS:
        destination = tmp_path / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PROJECT_ROOT / relative_path, destination)
        destinations.append(destination)
    return destinations[0], destinations[1]


def load_checker():
    __import__("check_task10")
    return sys.modules["check_task10"]


def test_task10_management_and_capstone_contract() -> None:
    result = run_check(
        PROJECT_ROOT,
        hermes_source=Path("/tmp/hermes-agent-v2026.8.19"),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "check_task10: OK" in result.stdout


def test_delegation_flow_accepts_bounded_verification_and_human_gate() -> None:
    checker = load_checker()
    diagram = """```mermaid
flowchart LR
    O["Human-approved outcome"] --> B["Bounded task brief"]
    B --> S["One suitable specialist"]
    S --> A["Shared artifact"]
    A --> V["Independent verification"]
    V --> H["Hermes handback"]
    H --> G["Human approval gate"]
```"""
    failures: list[str] = []

    checker.validate_delegation_flow(diagram, failures)

    assert failures == []


def test_delegation_flow_rejects_specialist_bypass() -> None:
    checker = load_checker()
    diagram = """```mermaid
flowchart LR
    O["Human-approved outcome"] --> B["Bounded task brief"]
    B --> S["One suitable specialist"]
    S --> A["Shared artifact"]
    A --> V["Independent verification"]
    V --> H["Hermes handback"]
    H --> G["Human approval gate"]
    S --> G
```"""
    failures: list[str] = []

    checker.validate_delegation_flow(diagram, failures)

    assert "delegation flow lets a specialist bypass verification and handback" in failures


def test_evidence_flow_requires_reduction_when_gate_fails() -> None:
    checker = load_checker()
    diagram = """```mermaid
flowchart LR
    I["Expected attempt"] --> R["Run/session record"]
    R --> C["Completion state"]
    C --> V["Verification evidence"]
    V --> S["Scorecard row"]
    S --> G["Weekly evidence gate"]
    G --> K["Keep or narrowly expand authority"]
```"""
    failures: list[str] = []

    checker.validate_evidence_flow(diagram, failures)

    assert "evidence flow missing failed-gate reduction path" in failures


@pytest.mark.parametrize(
    ("source", "gate"),
    [
        ("Gate 1", "GATE 1"),
        ("Gate 2", "GATE 2"),
        ("Gate 3", "GATE 3"),
        ("Gate 4", "GATE 4"),
        ("Gate 5", "GATE 5"),
        ("Gate 6 — qualification", "GATE 6 — QUALIFICATION"),
    ],
)
def test_task10_audit_rejects_each_removed_capstone_gate(
    tmp_path: Path, source: str, gate: str
) -> None:
    _chapter_21, chapter_22 = copy_task10_chapters(tmp_path)
    contents = chapter_22.read_text(encoding="utf-8")
    chapter_22.write_text(contents.replace(source, "Promotion check", 1), encoding="utf-8")

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert f"missing capstone evidence gate: {gate}" in result.stdout


def test_task10_audit_requires_flat_roster_control(tmp_path: Path) -> None:
    chapter_21, _chapter_22 = copy_task10_chapters(tmp_path)
    contents = chapter_21.read_text(encoding="utf-8")
    chapter_21.write_text(
        contents.replace("Keep delegation flat", "Enable recursive teams", 1),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "missing flat-roster control" in result.stdout


def test_task10_audit_requires_completion_correctness_separation(tmp_path: Path) -> None:
    _chapter_21, chapter_22 = copy_task10_chapters(tmp_path)
    contents = chapter_22.read_text(encoding="utf-8")
    chapter_22.write_text(
        contents.replace("Completion and correctness must be separate columns", "Completion is sufficient", 1),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "missing completion/correctness separation" in result.stdout
