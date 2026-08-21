# Hermes Agent Masterclass

A private, practical textbook for operating Hermes Agent as a capable and bounded personal agent on an Apple-silicon Mac mini.

The book is being built in stages. See the local site home page for the reader promise and authority model, and the pinned [research source map](research/hermes-v2026.8.19-source-map.md) for evidence routing.

## Local preview

```shell
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve
```

## Quality checks

```shell
.venv/bin/pytest -q
.venv/bin/mkdocs build --strict
.venv/bin/python tools/check_book.py
```

The release manuscript additionally uses `.venv/bin/python tools/check_book.py --final` to enforce all 22 chapters, four appendices, and the 100,000–120,000 word contract.
