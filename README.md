# Hermes Agent Masterclass

Hermes Agent Masterclass is a private, practical textbook for turning Hermes Agent into a capable but bounded personal chief of staff, career and family operator, and small-business employee on an Apple-silicon Mac mini. Its promise is operational: a reader learns not only what Hermes can do, but how to define authority, isolate access, verify outcomes, recover safely, and expand responsibility only when evidence supports it.

The audience is beginner-to-intermediate readers who understand that AI agents exist but do not yet have a deep operating model for one. No programming background is assumed. Technical interfaces are introduced through source-verified commands, copy-ready artifacts, and specialist delegation prompts.

## Edition status

This private repository contains the complete first-edition manuscript. Its contents comprise 22 chapters and four appendices, organized as foundations, the Mac mini platform, the trust envelope, personal chief-of-staff workflows, a one- or two-person business operating system, supervised specialist management, and an evidence-gated 90-day capstone.

The product baseline is **Nous Research Hermes Agent v0.20.5, tag `v2026.8.19`**. Version-sensitive instructions use the label “Verified against Hermes Agent v0.20.5 (2026-08-19).” The pinned [source map](research/hermes-v2026.8.19-source-map.md) routes claims to primary evidence.

Current measured manuscript word count: **109,964 words**. The repository validator excludes fenced code blocks and counts the 22 chapter files plus four appendix files listed in `book-manifest.yml`.

## Contents

- Parts I–II establish the Hermes mental model, Job Charter, Mac mini installation, model routing, continuity, extensions, messaging, and background operations.
- Part III builds the family-safe trust envelope across OS isolation, identities, secrets, approvals, egress, audit, sensitive data, backup, and recovery.
- Parts IV–V apply those controls to daily and weekly rhythms, job search, career artifacts, Canadian family operations, a microbusiness operating system, functional playbooks, and specialist delegation.
- Part VI evaluates correctness, boundaries, cost, recovery, and staged authority through a 90-day capstone.
- Appendices provide a command/interface reference, copy-ready templates, a Hermes-native extension matrix, and consolidated troubleshooting, glossary, bibliography, version, and provenance material.

Start at the local [book home](docs/index.md), or use [Appendix A](docs/appendices/appendix-a-command-reference.md) for commands and [Appendix B](docs/appendices/appendix-b-templates-playbooks.md) for operating artifacts.

## Exact local setup

From the repository root on macOS:

```shell
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve
```

Open <http://127.0.0.1:8000/>. This is the supported private local preview; the edition is not configured for public deployment.

## Quality checks

Run the release checks from the repository root:

```shell
.venv/bin/pytest -q
.venv/bin/python tools/check_book.py --final
.venv/bin/mkdocs build --strict
.venv/bin/codespell docs README.md CONTRIBUTING.md
python3 -m py_compile tools/*.py tests/*.py
git diff --check
```

The final validator enforces the canonical 22+4 file set, appendix and chapter word contracts, the 100,000–120,000 total, required structures, source/version labels, local links, provenance, project-guide promises, and private-data hygiene. Contributor-specific audits are documented in [CONTRIBUTING.md](CONTRIBUTING.md).

## Credit and license

Curated by Moumita Nath. The project is available under the [MIT License](LICENSE). Selected upstream Hermes images retain their upstream MIT provenance, recorded in [docs/assets/images/PROVENANCE.md](docs/assets/images/PROVENANCE.md).
