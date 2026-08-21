"""Behavioral tests for the manuscript validation command."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHECKER = PROJECT_ROOT / "tools" / "check_book.py"
REQUIRED_SECTIONS = [
    "## Opening scenario",
    "## Definitions",
    "## Hermes in practice",
    "## Professional example",
    "## Personal example",
    "## Authority boundaries",
    "## Failure modes and recovery",
    "## Field kit",
    "## Exercise",
    "## Answer or rubric",
    "## Mastery checklist",
    "## References",
]


def chapter(number: int = 1, *, body: str = "") -> str:
    """Return a complete numbered-chapter fixture with one Mermaid block."""
    sections = "\n\n".join(f"{section}\n\nFixture prose." for section in REQUIRED_SECTIONS)
    return (
        f"# Chapter {number}: Fixture\n\n"
        "Verified against Hermes Agent v0.20.5 (2026-08-19).\n\n"
        "```mermaid\nflowchart LR\n  A[Start] --> B[Finish]\n```\n\n"
        f"{sections}\n\n"
        "- [Official Hermes source](https://github.com/NousResearch/hermes-agent)\n"
        f"{body}\n"
    )


def manifest(chapters: list[dict[str, object]] | None = None) -> dict[str, object]:
    return {
        "product_baseline": "Hermes Agent v0.20.5 (2026-08-19)",
        "chapters": chapters
        or [
            {
                "number": 1,
                "title": "Fixture",
                "path": "docs/part-1/01-meet-hermes.md",
                "part": "Part I",
            }
        ],
        "appendices": [],
    }


def write_book(
    tmp_path: Path,
    *,
    chapters: list[dict[str, object]] | None = None,
    files: dict[str, str] | None = None,
) -> None:
    (tmp_path / "book-manifest.yml").write_text(
        yaml.safe_dump(manifest(chapters), sort_keys=False), encoding="utf-8"
    )
    fixture_files = {"docs/part-1/01-meet-hermes.md": chapter()} if files is None else files
    for relative_path, contents in fixture_files.items():
        destination = tmp_path / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(contents, encoding="utf-8")


def run_check(book_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(book_root), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def measured_words(contents: str) -> int:
    """Measure fixture words independently using the documented checker contract."""
    without_code = re.sub(r"```.*?```", "", contents, flags=re.DOTALL)
    return len(re.findall(r"\b[\w][\w’'/-]*\b", without_code))


def provenance_entry(**overrides: object) -> dict[str, object]:
    entry: dict[str, object] = {
        "filename": "dashboard-admin-system-top.png",
        "upstream_path": "website/static/img/dashboard/admin-system-top.png",
        "tag": "v2026.8.19",
        "license": "MIT",
        "chapters": [5, 13],
        "alt": "Hermes web dashboard administration screen showing top-level system controls.",
    }
    entry.update(overrides)
    return entry


def write_provenance(book_root: Path, entry: dict[str, object]) -> None:
    images = book_root / "docs/assets/images/hermes"
    images.mkdir(parents=True, exist_ok=True)
    (images / "dashboard-admin-system-top.png").write_bytes(b"fixture image")
    (book_root / "docs/assets/images/PROVENANCE.md").write_text(
        "# Fixture provenance\n\ndashboard-admin-system-top.png\n", encoding="utf-8"
    )
    (book_root / "docs/assets/images/provenance.yml").write_text(
        yaml.safe_dump({"assets": [entry]}, sort_keys=False), encoding="utf-8"
    )


def test_accepts_a_valid_incremental_manuscript(tmp_path: Path) -> None:
    write_book(tmp_path)

    result = run_check(tmp_path)

    assert result.returncode == 0, result.stdout
    assert "check_book: OK — 1 files" in result.stdout


@pytest.mark.parametrize(
    ("minimum_offset", "maximum_offset"),
    [
        (0, 10),
        (-10, 0),
    ],
)
def test_completed_chapter_accepts_word_counts_at_manifest_boundaries(
    tmp_path: Path, minimum_offset: int, maximum_offset: int
) -> None:
    contents = chapter()
    words = measured_words(contents)
    minimum = words + minimum_offset
    maximum = words + maximum_offset
    entry = {
        "number": 1,
        "title": "Fixture",
        "path": "docs/part-1/01-meet-hermes.md",
        "part": "Part I",
        "word_target": f"{minimum}–{maximum}",
        "status": "complete",
    }
    write_book(tmp_path, chapters=[entry], files={entry["path"]: contents})

    result = run_check(tmp_path)

    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize(
    ("minimum_offset", "maximum_offset"),
    [
        (1, 10),
        (-10, -1),
    ],
)
def test_completed_chapter_rejects_word_counts_outside_manifest_target(
    tmp_path: Path, minimum_offset: int, maximum_offset: int
) -> None:
    contents = chapter()
    words = measured_words(contents)
    minimum = words + minimum_offset
    maximum = words + maximum_offset
    entry = {
        "number": 1,
        "title": "Fixture",
        "path": "docs/part-1/01-meet-hermes.md",
        "part": "Part I",
        "word_target": f"{minimum}–{maximum}",
        "status": "complete",
    }
    write_book(tmp_path, chapters=[entry], files={entry["path"]: contents})

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert (
        f"word count outside manifest target: docs/part-1/01-meet-hermes.md: "
        f"{minimum}–{maximum} (found {words})"
    ) in result.stdout


@pytest.mark.parametrize("word_target", [None, "four thousand", "500–400"])
def test_completed_chapter_requires_a_valid_manifest_word_target(
    tmp_path: Path, word_target: str | None
) -> None:
    entry: dict[str, object] = {
        "number": 1,
        "title": "Fixture",
        "path": "docs/part-1/01-meet-hermes.md",
        "part": "Part I",
        "status": "complete",
    }
    if word_target is not None:
        entry["word_target"] = word_target
    write_book(tmp_path, chapters=[entry])

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert (
        "invalid completed chapter word_target: docs/part-1/01-meet-hermes.md: "
        "expected MIN–MAX with MIN <= MAX"
    ) in result.stdout


def test_incremental_mode_reports_a_missing_completed_chapter(tmp_path: Path) -> None:
    entry = {
        "number": 1,
        "title": "Fixture",
        "path": "docs/part-1/01-meet-hermes.md",
        "part": "Part I",
        "word_target": "100–200",
        "status": "complete",
    }
    write_book(tmp_path, chapters=[entry], files={})

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "missing completed chapter: docs/part-1/01-meet-hermes.md" in result.stdout


def test_final_mode_reports_a_missing_planned_chapter(tmp_path: Path) -> None:
    write_book(tmp_path, files={})

    result = run_check(tmp_path, "--final")

    assert result.returncode == 1
    assert "missing chapter: docs/part-1/01-meet-hermes.md" in result.stdout


def test_reports_duplicate_manifest_chapter_numbers(tmp_path: Path) -> None:
    chapters = [
        {"number": 1, "title": "First", "path": "docs/part-1/01-first.md", "part": "Part I"},
        {"number": 1, "title": "Second", "path": "docs/part-1/02-second.md", "part": "Part I"},
    ]
    write_book(tmp_path, chapters=chapters, files={"docs/part-1/01-first.md": chapter()})

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "duplicate chapter number: 1" in result.stdout


def test_reports_missing_required_section(tmp_path: Path) -> None:
    write_book(tmp_path, files={"docs/part-1/01-meet-hermes.md": chapter().replace("## Field kit", "## Kit")})

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "missing required section: docs/part-1/01-meet-hermes.md: ## Field kit" in result.stdout


def test_final_mode_enforces_the_manuscript_word_range(tmp_path: Path) -> None:
    write_book(tmp_path)

    result = run_check(tmp_path, "--final")

    assert result.returncode == 1
    assert "word count out of range: 100000–120000" in result.stdout


def test_reports_each_unresolved_placeholder_marker(tmp_path: Path) -> None:
    write_book(
        tmp_path,
        files={"docs/part-1/01-meet-hermes.md": chapter(body="TODO: draft. TBD: verify. FIXME: repair.")},
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "unresolved marker TODO: docs/part-1/01-meet-hermes.md" in result.stdout
    assert "unresolved marker TBD: docs/part-1/01-meet-hermes.md" in result.stdout
    assert "unresolved marker FIXME: docs/part-1/01-meet-hermes.md" in result.stdout


def test_reports_missing_local_images(tmp_path: Path) -> None:
    write_book(tmp_path, files={"docs/part-1/01-meet-hermes.md": chapter(body="![Missing](../assets/missing.png)")})

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "missing local asset: docs/part-1/01-meet-hermes.md: ../assets/missing.png" in result.stdout


def test_reports_broken_local_markdown_links(tmp_path: Path) -> None:
    write_book(tmp_path, files={"docs/part-1/01-meet-hermes.md": chapter(body="[Missing](../missing.md)")})

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "broken local link: docs/part-1/01-meet-hermes.md: ../missing.md" in result.stdout


def test_final_mode_requires_a_mermaid_block_in_every_chapter(tmp_path: Path) -> None:
    write_book(tmp_path, files={"docs/part-1/01-meet-hermes.md": chapter().replace("```mermaid\nflowchart LR\n  A[Start] --> B[Finish]\n```\n\n", "")})

    result = run_check(tmp_path, "--final")

    assert result.returncode == 1
    assert "missing Mermaid block: docs/part-1/01-meet-hermes.md" in result.stdout


def test_final_mode_requires_a_reference_url(tmp_path: Path) -> None:
    write_book(tmp_path, files={"docs/part-1/01-meet-hermes.md": chapter().replace("https://github.com/NousResearch/hermes-agent", "" )})

    result = run_check(tmp_path, "--final")

    assert result.returncode == 1
    assert "missing reference URL: docs/part-1/01-meet-hermes.md" in result.stdout


def test_reports_the_prohibited_model_name(tmp_path: Path) -> None:
    write_book(tmp_path, files={"docs/part-1/01-meet-hermes.md": chapter(body="GPT-5.6 Soul")})

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "prohibited product term: GPT-5.6 Soul: docs/part-1/01-meet-hermes.md" in result.stdout


def test_reports_accidental_secret_patterns(tmp_path: Path) -> None:
    write_book(tmp_path, files={"docs/part-1/01-meet-hermes.md": chapter(body="OPENAI_API_KEY=sk-abcdefghijklmnopqrstuvwxyz123456")})

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "possible secret: docs/part-1/01-meet-hermes.md: OPENAI_API_KEY" in result.stdout


@pytest.mark.parametrize(
    ("field", "diagnostic"),
    [
        ("filename", "missing provenance field: assets[0]: filename"),
        ("upstream_path", "missing provenance field: assets[0]: upstream_path"),
        ("tag", "missing provenance field: assets[0]: tag"),
        ("license", "missing provenance field: assets[0]: license"),
        ("chapters", "missing provenance field: assets[0]: chapters"),
        ("alt", "missing provenance field: assets[0]: alt"),
    ],
)
def test_final_mode_rejects_missing_provenance_fields(
    tmp_path: Path, field: str, diagnostic: str
) -> None:
    write_book(tmp_path)
    entry = provenance_entry()
    entry.pop(field)
    write_provenance(tmp_path, entry)

    result = run_check(tmp_path, "--final")

    assert result.returncode == 1
    assert diagnostic in result.stdout


@pytest.mark.parametrize(
    ("field", "value", "diagnostic"),
    [
        ("filename", "unknown.png", "unregistered provenance filename: unknown.png"),
        ("upstream_path", "website/static/img/dashboard/wrong.png", "wrong provenance upstream_path: dashboard-admin-system-top.png"),
        ("tag", "v0.0.0", "wrong provenance tag: dashboard-admin-system-top.png: expected v2026.8.19"),
        ("license", "Apache-2.0", "wrong provenance license: dashboard-admin-system-top.png: expected MIT"),
        ("chapters", "5", "invalid provenance chapters: dashboard-admin-system-top.png"),
        ("alt", "", "invalid provenance alt: dashboard-admin-system-top.png"),
    ],
)
def test_final_mode_rejects_wrong_provenance_fields(
    tmp_path: Path, field: str, value: object, diagnostic: str
) -> None:
    write_book(tmp_path)
    write_provenance(tmp_path, provenance_entry(**{field: value}))

    result = run_check(tmp_path, "--final")

    assert result.returncode == 1
    assert diagnostic in result.stdout


def test_final_mode_rejects_an_image_without_provenance_registration(tmp_path: Path) -> None:
    write_book(tmp_path)
    write_provenance(tmp_path, provenance_entry())
    (tmp_path / "docs/assets/images/hermes/unregistered.png").write_bytes(b"fixture image")

    result = run_check(tmp_path, "--final")

    assert result.returncode == 1
    assert "unregistered image: docs/assets/images/hermes/unregistered.png" in result.stdout
