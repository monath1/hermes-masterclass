"""Behavioral tests for the manuscript validation command."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

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


def test_accepts_a_valid_incremental_manuscript(tmp_path: Path) -> None:
    write_book(tmp_path)

    result = run_check(tmp_path)

    assert result.returncode == 0, result.stdout
    assert "check_book: OK — 1 files" in result.stdout


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
