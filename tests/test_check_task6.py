"""Regression coverage for the retained Task 6 security audit."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHECKER = PROJECT_ROOT / "tools" / "check_task6.py"


def test_task6_security_contract() -> None:
    """Catch weakened egress/export/data-language contracts in Chapters 13–14."""
    result = subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(PROJECT_ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "check_task6: OK" in result.stdout
