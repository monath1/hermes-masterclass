"""Regression coverage for the retained Task 7 workflow audit."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHECKER = PROJECT_ROOT / "tools" / "check_task7.py"


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
