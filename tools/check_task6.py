#!/usr/bin/env python3
"""Audit the security-sensitive claims and word contracts in Chapters 13–14."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from check_book import markdown_words


PINNED_COMMIT = "fcbd1076a93841fa88855acce810e342a5b78101"
CHAPTERS = {
    "docs/part-3/13-approvals-autonomy-egress-audit.md": (4800, 5400),
    "docs/part-3/14-sensitive-data-backups-recovery.md": (4400, 5000),
}
REQUIRED_PINNED_PATHS = {
    "SECURITY.md",
    "website/docs/developer-guide/trajectory-format.md",
    "website/docs/getting-started/updating.md",
    "website/docs/reference/cli-commands.md",
    "website/docs/user-guide/checkpoints-and-rollback.md",
    "website/docs/user-guide/egress/index.md",
    "website/docs/user-guide/egress/iron-proxy.md",
    "website/docs/user-guide/features/cron.md",
    "website/docs/user-guide/features/hooks.md",
    "website/docs/user-guide/managed-scope.md",
    "website/docs/user-guide/profile-distributions.md",
    "website/docs/user-guide/secrets/index.md",
    "website/docs/user-guide/security.md",
    "website/docs/user-guide/sessions.md",
}
PINNED_SOURCE_ASSERTIONS = (
    ("website/docs/user-guide/security.md", "approvals.mode"),
    ("website/docs/user-guide/security.md", "timeout: 300"),
    ("website/docs/user-guide/security.md", "cron_mode: deny"),
    ("website/docs/user-guide/security.md", "single_query_mode: deny"),
    ("website/docs/user-guide/security.md", "mcp_reload_confirm: true"),
    ("website/docs/user-guide/security.md", "destructive_slash_confirm: true"),
    ("website/docs/user-guide/security.md", "denied** by default (fail-closed)"),
    ("website/docs/user-guide/security.md", "command_allowlist"),
    ("website/docs/user-guide/security.md", "hermes approvals suggest"),
    ("website/docs/user-guide/security.md", "HERMES_YOLO_MODE=1"),
    ("website/docs/user-guide/egress/iron-proxy.md", "hermes egress setup"),
    ("website/docs/user-guide/egress/iron-proxy.md", "hermes egress start"),
    ("website/docs/user-guide/egress/iron-proxy.md", "hermes egress status"),
    ("website/docs/user-guide/egress/iron-proxy.md", "enforce_on_docker: true"),
    ("website/docs/user-guide/egress/iron-proxy.md", "extra_allowed_hosts: []"),
    ("website/docs/user-guide/egress/iron-proxy.md", "OpenRouter"),
    ("website/docs/user-guide/egress/iron-proxy.md", "Nous Research"),
    ("website/docs/user-guide/egress/iron-proxy.md", "v0.39.0"),
    ("website/docs/user-guide/egress/iron-proxy.md", "iron-proxy.log"),
    ("website/docs/user-guide/egress/iron-proxy.md", "audit.log"),
    ("website/docs/user-guide/egress/iron-proxy.md", "raw sockets"),
    ("website/docs/user-guide/checkpoints-and-rollback.md", "hermes chat --checkpoints"),
    ("website/docs/user-guide/checkpoints-and-rollback.md", "default: false — opt-in"),
    ("website/docs/user-guide/checkpoints-and-rollback.md", "/rollback diff <N>"),
    ("website/docs/user-guide/checkpoints-and-rollback.md", "/rollback <N> --all"),
    ("website/docs/user-guide/checkpoints-and-rollback.md", "shared shadow git repository"),
    ("website/docs/user-guide/checkpoints-and-rollback.md", "your tools continue to run"),
    ("website/docs/user-guide/sessions.md", "~/.hermes/state.db"),
    ("website/docs/user-guide/sessions.md", "canonical store for all session messages"),
    ("website/docs/user-guide/features/hooks.md", "Callback exceptions are logged and skipped"),
    ("website/docs/user-guide/features/hooks.md", "fail_closed: true"),
    ("website/docs/developer-guide/trajectory-format.md", "trajectory_samples.jsonl"),
    ("website/docs/developer-guide/trajectory-format.md", "does not expose a config key or flag"),
    ("website/docs/user-guide/features/cron.md", "never\nautomatically rerun"),
    ("website/docs/user-guide/features/cron.md", "claimed`, `running`"),
    ("website/docs/reference/cli-commands.md", "SQLite's `backup()` API"),
    ("website/docs/reference/cli-commands.md", "`checkpoints/` — per-session trajectory caches"),
    ("website/docs/reference/cli-commands.md", "All files in the archive overwrite existing files"),
    ("website/docs/getting-started/updating.md", "credentials excluded by design"),
    ("website/docs/user-guide/profile-distributions.md", "Credentials are filtered by filename; content is not"),
    ("website/docs/user-guide/profile-distributions.md", "if the profile has `state.db`, logs, or caches"),
    ("website/docs/user-guide/profile-distributions.md", "publish a [distribution]"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="book root")
    parser.add_argument(
        "--hermes-source",
        type=Path,
        help="optional pinned Hermes v2026.8.19 checkout for source-content verification",
    )
    return parser.parse_args()


def require(text: str, phrase: str, label: str, failures: list[str]) -> None:
    if phrase.casefold() not in text.casefold():
        failures.append(f"missing {label}: {phrase}")


def luhn(number: str) -> bool:
    digits = [int(character) for character in number]
    parity = len(digits) % 2
    total = 0
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def validate_source(source: Path, failures: list[str]) -> None:
    if not source.is_dir():
        failures.append(f"missing pinned Hermes source: {source}")
        return

    result = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or result.stdout.strip() != PINNED_COMMIT:
        failures.append(
            f"wrong pinned Hermes commit: expected {PINNED_COMMIT}, found {result.stdout.strip() or 'unreadable'}"
        )

    for relative_path, phrase in PINNED_SOURCE_ASSERTIONS:
        path = source / relative_path
        if not path.is_file():
            failures.append(f"missing pinned source path: {relative_path}")
        elif phrase not in path.read_text(encoding="utf-8"):
            failures.append(f"missing pinned source assertion: {relative_path}: {phrase}")


def audit_task6(root: Path, hermes_source: Path | None = None) -> list[str]:
    failures: list[str] = []
    content: dict[str, str] = {}
    for relative_path, (minimum, maximum) in CHAPTERS.items():
        path = root / relative_path
        if not path.is_file():
            failures.append(f"missing chapter: {relative_path}")
            continue
        chapter = path.read_text(encoding="utf-8")
        content[relative_path] = chapter
        words = markdown_words(chapter)
        if not minimum <= words <= maximum:
            failures.append(
                f"word count out of range: {relative_path}: {minimum}–{maximum} (found {words})"
            )

    if len(content) != len(CHAPTERS):
        return failures

    chapter_13 = content["docs/part-3/13-approvals-autonomy-egress-audit.md"]
    chapter_14 = content["docs/part-3/14-sensitive-data-backups-recovery.md"]
    combined = chapter_13 + "\n" + chapter_14

    for phrase in (
        "policy targets",
        "OpenRouter, OpenAI, Anthropic, Google, xAI, Mistral, Groq, Together, DeepSeek, and Nous Research",
        "`proxy.extra_allowed_hosts` can only expand",
        "selected-provider-only",
        "firewall or whole-process",
        "custom proxy rules",
        "different bundled provider host",
    ):
        require(chapter_13, phrase, "Chapter 13 egress caveat", failures)

    for phrase in (
        "excluded by filename",
        "content is not scanned",
        "USER.md",
        "sessions",
        "memories",
        "state.db",
        "logs",
        "caches",
        "protect and inspect",
        "distribution",
        "next time it connects to a Wi-Fi or mobile network",
        "cannot be undone",
    ):
        require(chapter_14, phrase, "Chapter 14 export/erase caveat", failures)

    for phrase in (
        "Hermes must not solicit card numbers or verification codes",
        "memory, logs, tests, backups, or templates",
        "primary credentials and recovery codes are absent",
        "raw child dossiers",
        "do not claim PCI certification",
    ):
        require(chapter_14, phrase, "prohibited-data language", failures)

    pinned_pattern = re.compile(
        r"https://github\.com/NousResearch/hermes-agent/blob/v2026\.8\.19/([^\s)#]+)"
    )
    linked_paths = set(pinned_pattern.findall(combined))
    for relative_path in sorted(REQUIRED_PINNED_PATHS - linked_paths):
        failures.append(f"missing pinned reference URL: {relative_path}")
    if hermes_source is not None:
        validate_source(hermes_source.resolve(), failures)
        for relative_path in sorted(linked_paths):
            if not (hermes_source / relative_path).is_file():
                failures.append(f"pinned reference URL does not resolve: {relative_path}")

    for pattern in (
        r"PCI[- ]?DSS (?:certified|compliant)",
        r"PIPEDA[- ]?compliant",
        r"HIPAA[- ]?compliant",
        r"fully secure",
        r"zero risk",
        r"encryption (?:is|provides|replaces) access control",
        r"backup (?:is|provides|replaces) access control",
        r"guarantees? (?:security|privacy|compliance)",
        r"never leaks?",
        r"cannot leak",
    ):
        if re.search(pattern, combined, re.IGNORECASE):
            failures.append(f"security-language overclaim: {pattern}")

    for label, pattern in (
        ("OpenAI assignment", r"\bOPENAI_API_KEY\s*="),
        ("Anthropic assignment", r"\bANTHROPIC_API_KEY\s*="),
        ("GitHub token", r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
        ("OpenAI key", r"\bsk-[A-Za-z0-9_-]{20,}\b"),
        ("private key", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ):
        if re.search(pattern, combined):
            failures.append(f"possible secret: {label}")
    card_numbers = [
        candidate
        for candidate in re.findall(r"(?<!\d)\d{13,19}(?!\d)", combined)
        if luhn(candidate)
    ]
    if card_numbers:
        failures.append(f"possible payment-card number: {card_numbers[0]}")

    return failures


def main() -> int:
    args = parse_args()
    failures = audit_task6(args.root.resolve(), args.hermes_source)
    for failure in failures:
        print(f"ERROR: {failure}")
    status = "OK" if not failures else "FAILED"
    source_status = "verified" if args.hermes_source else "reference paths checked"
    print(f"check_task6: {status} — {len(CHAPTERS)} chapters; pinned source {source_status}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
