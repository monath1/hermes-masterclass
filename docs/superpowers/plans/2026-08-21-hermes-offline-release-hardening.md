# Hermes Offline Release Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the complete first-edition site render without third-party runtime requests and make its release process reproducible and supply-chain pinned.

**Architecture:** MkDocs emits local Mermaid markup, loads a vendored exact Mermaid browser bundle, and initializes it with a small Material-compatible local script. A release-policy checker validates configuration, built resources, provenance, workflow pins, and locked installation; a shell entry point bootstraps the pinned environment and runs every release gate, including an offline Chromium diagram smoke test.

**Tech Stack:** MkDocs Material, Mermaid 10.4.0, Python 3.11, pytest, shell, Chromium, markdownlint-cli2 0.23.2, Lychee 0.24.2, GitHub Actions.

**Spec:** Approved Task 12 whole-branch review fix wave and `.superpowers/sdd/2026-08-21-hermes-masterclass-first-edition/task-12-brief.md`.

## Global Constraints

- Preserve the canonical 28-page navigation order.
- Make every runtime script, style, font, image, and diagram dependency local.
- Record exact version, license, source, archive integrity, and vendored-file hash.
- Pin every GitHub Action to a 40-character commit and disable checkout credential persistence.
- Install Python dependencies only from a fully hashed transitive lock.
- Do not push, merge, open a pull request, or deploy.

---

### Task 1: Regression guards

**Files:**

- Create: `tests/test_release_policy.py`
- Create: `tools/check_release.py`

**Interfaces:**

- Produces: `python tools/check_release.py --site site` for repository and built-site policy checks.

- [ ] Write policy tests for local scripts/fonts, built provenance, action SHAs, checkout credentials, hash locks, and release-command inventory.
- [ ] Run the new tests and observe failures against the current release.
- [ ] Implement the smallest reusable policy checker that makes the fixture tests pass.

### Task 2: Offline site runtime

**Files:**

- Create: `docs/assets/vendor/mermaid/10.4.0/mermaid.min.js`
- Create: `docs/assets/vendor/mermaid/10.4.0/LICENSE`
- Create: `docs/assets/vendor/mermaid/README.md`
- Create: `docs/javascripts/mermaid-init.js`
- Create: `tools/check_offline_site.py`
- Modify: `mkdocs.yml`
- Modify: `docs/stylesheets/extra.css`
- Modify: `requirements.txt`

**Interfaces:**

- Consumes: rendered `.mermaid` blocks in the built site.
- Produces: 24 non-empty local SVG diagrams under network-denied Chromium.

- [ ] Vendor and hash Mermaid 10.4.0 plus its MIT license.
- [ ] Replace the remote Mermaid plugin loader with local scripts and a Material `document$` initializer.
- [ ] Disable Material remote fonts and declare system font stacks.
- [ ] Add a CSP-and-DNS-blocked Chromium smoke checker and verify 24 non-empty SVG diagrams.

### Task 3: Built provenance and supply-chain lock

**Files:**

- Modify: `mkdocs.yml`
- Modify: `.github/workflows/quality.yml`
- Create: `requirements.lock`
- Create: `tools/verify_release.sh`
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`

**Interfaces:**

- Produces: one fresh-clone release command and a reachable built provenance page.

- [ ] Build `PROVENANCE.md` outside the canonical navigation and validate its output path.
- [ ] Pin checkout/setup actions to reviewed SHAs and disable persisted credentials.
- [ ] Generate a transitive Python 3.11 lock with hashes and switch local/CI installation to `--require-hashes`.
- [ ] Add the release shell entry point for pinned Hermes bootstrap, all audits, tests, build, linters, link checks, compilation, browser smoke, and diff checks.

### Task 4: Editorial and final verification

**Files:**

- Modify: `docs/part-2/05-install-hermes-on-mac-mini.md`
- Modify: `docs/superpowers/specs/2026-08-21-hermes-masterclass-design.md`
- Modify: `.gitignore`
- Modify: hidden Task 12 report.

**Interfaces:**

- Produces: clean branch whitespace, two beginner-facing Chapter 5 screenshots, and final evidence.

- [ ] Embed the administration and desktop-session screenshots beside their interface explanations.
- [ ] Remove all net whitespace errors from the branch and restore one final newline in `.gitignore`.
- [ ] Install the hash lock into a clean Python 3.11 environment and build the site.
- [ ] Run the full release script, built-site Lychee, offline browser light/dark/mobile/print inspection, and network/resource audit.
- [ ] Append exact evidence to the hidden report and commit the focused fix.
