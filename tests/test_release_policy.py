"""Regression tests for offline rendering and release supply-chain policy."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHECKER = PROJECT_ROOT / "tools" / "check_release.py"


def run_check(root: Path, site: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(CHECKER), "--root", str(root)]
    if site is not None:
        command.extend(("--site", str(site)))
    return subprocess.run(command, check=False, capture_output=True, text=True)


def write_policy_fixture(tmp_path: Path) -> None:
    (tmp_path / ".github/workflows").mkdir(parents=True)
    (tmp_path / "docs/assets/vendor/mermaid/10.4.0").mkdir(parents=True)
    (tmp_path / "tools").mkdir()
    (tmp_path / "mkdocs.yml").write_text(
        "theme:\n  font: false\n"
        "extra_javascript:\n"
        "  - assets/vendor/mermaid/10.4.0/mermaid.min.js\n"
        "  - javascripts/mermaid-init.js\n"
        "plugins: [search]\n",
        encoding="utf-8",
    )
    (tmp_path / ".github/workflows/quality.yml").write_text(
        "steps:\n"
        "  - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2\n"
        "    with:\n"
        "      persist-credentials: false\n"
        "  - run: bash tools/verify_release.sh\n",
        encoding="utf-8",
    )
    (tmp_path / "requirements.lock").write_text(
        "example==1.0 \\" "\n"
        "    --hash=sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n",
        encoding="utf-8",
    )
    (tmp_path / "tools/verify_release.sh").write_text(
        "#!/usr/bin/env bash\n"
        "python -m pip install --require-hashes -r requirements.lock\n"
        "pytest -q\n"
        "python tools/check_book.py --final\n"
        "for audit in 6 7 8 9 10 11; do python tools/check_task${audit}.py; done\n"
        "mkdocs build --strict\n"
        "npx --yes markdownlint-cli2@0.23.2\n"
        "lychee 0.24.2\n"
        "codespell docs README.md CONTRIBUTING.md research\n"
        "python -m py_compile tools/*.py tests/*.py\n"
        "python tools/check_offline_site.py\n"
        "git diff --check\n"
        "v2026.8.19\n"
        "fcbd1076a93841fa88855acce810e342a5b78101\n",
        encoding="utf-8",
    )
    (tmp_path / "docs/assets/vendor/mermaid/README.md").write_text(
        "Mermaid 10.4.0 MIT 2cf7bb6cdc4a6ea96da3d324a4447d8300d1da703ce5f31311608642c0f86269\n",
        encoding="utf-8",
    )
    (tmp_path / "docs/assets/vendor/mermaid/10.4.0/mermaid.min.js").write_text(
        "fixture", encoding="utf-8"
    )
    (tmp_path / "docs/assets/vendor/mermaid/10.4.0/LICENSE").write_text(
        "MIT", encoding="utf-8"
    )


def test_rejects_mutable_action_and_persisted_checkout_credentials(tmp_path: Path) -> None:
    write_policy_fixture(tmp_path)
    workflow = tmp_path / ".github/workflows/quality.yml"
    workflow.write_text(
        "steps:\n  - uses: actions/checkout@v4\n    with:\n      persist-credentials: true\n",
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "GitHub Action is not pinned to a 40-character commit" in result.stdout
    assert "checkout must set persist-credentials: false" in result.stdout


def test_rejects_remote_runtime_resources_and_unlocked_install(tmp_path: Path) -> None:
    write_policy_fixture(tmp_path)
    (tmp_path / "mkdocs.yml").write_text(
        "theme:\n  font:\n    text: Roboto\n"
        "extra_javascript: [https://unpkg.com/mermaid.js]\n"
        "plugins: [search, mermaid2]\n",
        encoding="utf-8",
    )
    (tmp_path / "tools/verify_release.sh").write_text(
        "pip install -r requirements.txt\n", encoding="utf-8"
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "Material fonts must be disabled" in result.stdout
    assert "remote or plugin-provided Mermaid runtime is forbidden" in result.stdout
    assert "release verifier must install requirements.lock with --require-hashes" in result.stdout


def test_rejects_missing_provenance_and_external_built_resources(tmp_path: Path) -> None:
    write_policy_fixture(tmp_path)
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text(
        '<script src="https://cdn.example/diagram.js"></script>', encoding="utf-8"
    )

    result = run_check(tmp_path, site)

    assert result.returncode == 1
    assert "built provenance page is missing" in result.stdout
    assert "external page-load resource" in result.stdout


def test_rejects_missing_editorial_identity_and_local_font_inventory(tmp_path: Path) -> None:
    write_policy_fixture(tmp_path)

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "editorial identity/theme configuration is missing" in result.stdout
    assert "missing vendored font asset" in result.stdout
    assert "font provenance is missing" in result.stdout


def test_rejects_release_verifier_that_excludes_built_site(tmp_path: Path) -> None:
    write_policy_fixture(tmp_path)
    verifier = tmp_path / "tools/verify_release.sh"
    verifier.write_text(
        verifier.read_text(encoding="utf-8")
        + "\nlychee_common=(--exclude-path site)\n",
        encoding="utf-8",
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "Lychee common options must not exclude the built site" in result.stdout


def test_verifier_passes_bootstrapped_hermes_source_to_pytest(tmp_path: Path) -> None:
    """Catch a verifier that validates a checkout but hides it from pytest."""
    fake_venv = tmp_path / "venv"
    fake_bin = tmp_path / "bin"
    hermes_source = tmp_path / "fresh-hermes-checkout"
    capture = tmp_path / "pytest-hermes-source.txt"
    (fake_venv / "bin").mkdir(parents=True)
    fake_bin.mkdir()
    hermes_source.mkdir()

    python = fake_venv / "bin/python"
    python.write_text("#!/usr/bin/env sh\nexit 0\n", encoding="utf-8")
    python.chmod(0o755)
    pytest = fake_venv / "bin/pytest"
    pytest.write_text(
        "#!/usr/bin/env sh\n"
        "printf '%s' \"${HERMES_TEST_SOURCE-}\" > \"$HERMES_ENV_CAPTURE\"\n"
        "exit 23\n",
        encoding="utf-8",
    )
    pytest.chmod(0o755)
    git = fake_bin / "git"
    git.write_text(
        "#!/usr/bin/env sh\n"
        "printf '%s\\n' fcbd1076a93841fa88855acce810e342a5b78101\n",
        encoding="utf-8",
    )
    git.chmod(0o755)

    env = os.environ.copy()
    env.update(
        {
            "HERMES_ENV_CAPTURE": str(capture),
            "HERMES_SOURCE": str(hermes_source),
            "HERMES_VERIFY_VENV": str(fake_venv),
            "PATH": f"{fake_bin}{os.pathsep}{env['PATH']}",
        }
    )

    result = subprocess.run(
        ["bash", str(PROJECT_ROOT / "tools/verify_release.sh")],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 23, result.stdout + result.stderr
    assert capture.read_text(encoding="utf-8") == str(hermes_source)


def test_contract_tests_resolve_env_provided_hermes_source(tmp_path: Path) -> None:
    """Catch contract tests that silently keep using a developer-only /tmp clone."""
    sentinel = tmp_path / "env-selected-hermes-source"
    env = os.environ.copy()
    env["HERMES_TEST_SOURCE"] = str(sentinel)
    contract_modules = (
        "tests/test_check_task8.py",
        "tests/test_check_task9.py",
        "tests/test_check_task10.py",
        "tests/test_check_task11.py",
    )

    for index, contract_module in enumerate(contract_modules):
        module_path = PROJECT_ROOT / contract_module
        load_module = (
            "import importlib.util; "
            f"spec = importlib.util.spec_from_file_location('contract_{index}', "
            f"{str(module_path)!r}); "
            "module = importlib.util.module_from_spec(spec); "
            "spec.loader.exec_module(module); "
            "print(module.PINNED_HERMES)"
        )
        result = subprocess.run(
            [sys.executable, "-c", load_module],
            cwd=PROJECT_ROOT,
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

        assert result.returncode == 0, result.stdout + result.stderr
        assert result.stdout.strip() == str(sentinel)


def test_current_repository_satisfies_release_policy() -> None:
    result = run_check(PROJECT_ROOT)

    assert result.returncode == 0, result.stdout
