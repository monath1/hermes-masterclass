# Contributing

## Editorial contract

Write original, compact prose for a beginner-to-intermediate reader. Every numbered chapter must include the chapter-contract sections validated by `tools/check_book.py`, one substantive Mermaid diagram, Green/Amber/Red authority boundaries, failure and recovery guidance, a reusable field kit, an exercise with a separated answer or rubric, and primary references.

Use the Canadian family and small-business running case only as a fictional operating case. Never add real family information, credentials, API keys, or screenshots from personal accounts. Financial, health, tax, legal, employment, and privacy material must prepare readers for review or professional handoff; it must not present professional advice.

## Source and version discipline

Begin research at `research/hermes-v2026.8.19-source-map.md`. Commands, settings, model names, prices, laws, and interface labels require a primary source. Version-sensitive Hermes statements must carry the exact label: `Verified against Hermes Agent v0.20.5 (2026-08-19).` Use the official identifier `gpt-5.6-sol`; the validator rejects the common incorrect spelling.

Copy screenshots only from the pinned official Hermes checkout, preserve their local filename, and add a complete entry to `docs/assets/images/PROVENANCE.md`. Do not use external image hotlinks or placeholders.

## Local checks

```shell
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pytest -q
.venv/bin/mkdocs build --strict
.venv/bin/python tools/check_book.py
.venv/bin/python tools/check_task6.py --hermes-source /tmp/hermes-agent-v2026.8.19
.venv/bin/python tools/check_task7.py --hermes-source /tmp/hermes-agent-v2026.8.19
```

Use `--final` only once all 22 chapters and four appendices exist. Run `git diff --check` before committing.
