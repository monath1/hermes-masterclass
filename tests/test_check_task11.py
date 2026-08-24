"""Regression coverage for the Task 11 appendices and source ledger audit."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHECKER = PROJECT_ROOT / "tools" / "check_task11.py"
PINNED_HERMES = Path(
    os.environ.get("HERMES_TEST_SOURCE", "/tmp/hermes-agent-v2026.8.19")
)
CLI_URL = (
    "https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/"
    "website/docs/reference/cli-commands.md"
)


def run_check(book_root: Path, *, hermes_source: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(CHECKER), "--root", str(book_root)]
    if hermes_source is not None:
        command.extend(["--hermes-source", str(hermes_source)])
    return subprocess.run(command, check=False, capture_output=True, text=True)


def copy_docs(tmp_path: Path) -> None:
    shutil.copytree(PROJECT_ROOT / "docs", tmp_path / "docs")


def load_checker():
    sys.path.insert(0, str(PROJECT_ROOT / "tools"))
    __import__("check_task11")
    return sys.modules["check_task11"]


def test_task11_appendix_source_contract() -> None:
    result = run_check(PROJECT_ROOT, hermes_source=PINNED_HERMES)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "check_task11: OK" in result.stdout
    assert "170 external URLs" in result.stdout


def test_source_map_includes_chapter_6_for_the_cli_reference() -> None:
    checker = load_checker()

    source_map = checker.collect_external_sources(PROJECT_ROOT)

    assert source_map[CLI_URL].affected == ("6", "14", "A")


def test_source_ledger_rejects_an_incorrect_affected_mapping(tmp_path: Path) -> None:
    copy_docs(tmp_path)
    appendix = tmp_path / "docs/appendices/appendix-d-troubleshooting-glossary-bibliography.md"
    text = appendix.read_text(encoding="utf-8")
    appendix.write_text(
        text.replace('"6, 14, A","Yes—pinned"', '"14, A","Yes—pinned"', 1),
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert f"wrong source-ledger mapping: {CLI_URL}: expected 6, 14, A" in result.stdout


def test_source_ledger_requires_every_field() -> None:
    checker = load_checker()
    failures: list[str] = []
    table = """## Source and version ledger

```csv
url,title,publisher,verified,affected,version_sensitive
https://example.com/cli,CLI,,2026-08-21,6,Yes—mutable
```
"""

    checker.parse_source_ledger(table, failures)

    assert "missing source-ledger publisher: https://example.com/cli" in failures


def test_task11_audit_rejects_an_unverified_appendix_a_command(tmp_path: Path) -> None:
    copy_docs(tmp_path)
    appendix = tmp_path / "docs/appendices/appendix-a-command-reference.md"
    appendix.write_text(
        appendix.read_text(encoding="utf-8").replace("`hermes status`", "`hermes imaginary`", 1),
        encoding="utf-8",
    )

    result = run_check(tmp_path, hermes_source=PINNED_HERMES)

    assert result.returncode == 1
    assert "unverified Appendix A command: hermes imaginary" in result.stdout


def test_task11_audit_rejects_an_unverified_appendix_c_skill(tmp_path: Path) -> None:
    copy_docs(tmp_path)
    appendix = tmp_path / "docs/appendices/appendix-c-curated-stack.md"
    appendix.write_text(
        appendix.read_text(encoding="utf-8").replace(
            "`grounded-citations` — bundled", "`imaginary-skill` — bundled", 1
        ),
        encoding="utf-8",
    )

    result = run_check(tmp_path, hermes_source=PINNED_HERMES)

    assert result.returncode == 1
    assert "unverified Appendix C skill: imaginary-skill" in result.stdout
