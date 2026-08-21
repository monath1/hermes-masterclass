"""Regression coverage for the retained Task 10 management/capstone audit."""

from __future__ import annotations

import os
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
PINNED_HERMES = Path(
    os.environ.get("HERMES_TEST_SOURCE", "/tmp/hermes-agent-v2026.8.19")
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
        hermes_source=PINNED_HERMES,
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
    chapter_22.write_text(
        contents.replace(f"**{source}:", "**Promotion check:", 1),
        encoding="utf-8",
    )

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


@pytest.mark.parametrize(
    ("source", "replacement", "label"),
    [
        (
            "Prompt-declared read and write roots are instructions, not enforced capability",
            "Prompt-declared roots enforce capability",
            "declared/enforced boundary",
        ),
        (
            "The model-facing `delegate_task` inherits the parent’s enabled toolsets",
            "The child receives only tools listed in its prompt",
            "model-facing tool inheritance",
        ),
        (
            "the `file` toolset bundles read, search, patch, and write operations",
            "the file toolset is read-only",
            "file toolset read/write scope",
        ),
        (
            "Per-launch tool blocks and working-directory overrides are unavailable in the model-facing call",
            "The prompt can set per-launch tool blocks and workdir",
            "model-facing per-launch limits",
        ),
        (
            "True read-only delegation requires a constrained parent or profile with no write-capable toolset, plus OS or container read-only mounts",
            "A read-only prompt is enough",
            "enforced read-only boundary",
        ),
        (
            "A clean worktree and `workspace-write` are not a secret-read boundary",
            "A clean worktree prevents secret reads",
            "Codex secret-read boundary",
        ),
        (
            "`CODEX_HOME` isolates Codex authentication, configuration, and plugin state only",
            "`CODEX_HOME` isolates the whole operating-system account",
            "CODEX_HOME scope",
        ),
        (
            "Hermes’s app-server process retains the real OS `HOME` and can read ordinary user credential state",
            "Hermes rewrites HOME to an empty profile directory",
            "real HOME credential exposure",
        ),
        (
            "a dedicated macOS user, container, or equivalent environment with unrelated credentials and data absent",
            "the ordinary login account is sufficient",
            "dedicated execution environment",
        ),
    ],
)
def test_task10_audit_requires_enforced_delegation_boundaries(
    tmp_path: Path, source: str, replacement: str, label: str
) -> None:
    chapter_21, _chapter_22 = copy_task10_chapters(tmp_path)
    contents = chapter_21.read_text(encoding="utf-8")
    chapter_21.write_text(contents.replace(source, replacement, 1), encoding="utf-8")

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert f"missing {label}" in result.stdout


def test_task10_audit_requires_illustrative_delegate_task_label(tmp_path: Path) -> None:
    chapter_21, _chapter_22 = copy_task10_chapters(tmp_path)
    contents = chapter_21.read_text(encoding="utf-8")
    chapter_21.write_text(
        contents.replace(
            "illustrative Hermes tool call, not pasteable Python or shell",
            "ready-to-run Python",
            1,
        ),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "missing illustrative tool-call label" in result.stdout


@pytest.mark.parametrize(
    ("source", "replacement", "expected"),
    [
        (
            "at least fifteen independently reviewed and accepted reference cases",
            "at least fifteen completed reference cases",
            "missing Gate 1 accepted-case threshold",
        ),
        (
            "every attempt dispositioned",
            "most attempts dispositioned",
            "missing Gate 1 attempt disposition",
        ),
        (
            "no unresolved false completion",
            "few false completions",
            "missing Gate 1 false-completion control",
        ),
        (
            "four weekly reviews completed across Days 46–75",
            "four weekly reviews completed",
            "missing Gate 5 feasible review window",
        ),
        (
            "Start the Gate 5 sampled-review cadence during this phase",
            "Start reviews on Day 61",
            "missing Gate 5 review start",
        ),
    ],
)
def test_task10_audit_requires_strengthened_gate_language(
    tmp_path: Path, source: str, replacement: str, expected: str
) -> None:
    _chapter_21, chapter_22 = copy_task10_chapters(tmp_path)
    contents = chapter_22.read_text(encoding="utf-8")
    chapter_22.write_text(contents.replace(source, replacement, 1), encoding="utf-8")

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert expected in result.stdout


def test_task10_audit_rejects_false_completion_denominator_drift(tmp_path: Path) -> None:
    _chapter_21, chapter_22 = copy_task10_chapters(tmp_path)
    contents = chapter_22.read_text(encoding="utf-8")
    chapter_22.write_text(
        contents.replace(
            "false completion is one of ten reviewed completed claims",
            "false completion is one of the eleven completed claims",
            1,
        ),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "missing reviewed false-completion denominator" in result.stdout
