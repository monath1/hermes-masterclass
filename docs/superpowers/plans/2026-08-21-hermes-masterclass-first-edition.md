# Hermes Agent Masterclass First Edition Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a complete 100,000–120,000-word, beginner-to-advanced Hermes Agent textbook and private MkDocs site, then merge it through a feature-branch pull request.

**Architecture:** The manuscript is divided into 22 independent chapter files and four appendix files, all governed by one chapter contract and one pinned Hermes source baseline. A lightweight Python validator enforces structure, word-count, links, assets, source labels, and placeholder hygiene; MkDocs Material provides the local reading experience. Content tasks are grouped by coherent parts so fresh sub-agents can research and write bounded files while a reviewer enforces the shared editorial and safety contract.

**Tech Stack:** Markdown, MkDocs Material, Python 3.11+, pytest, PyYAML, Mermaid via `mkdocs-mermaid2-plugin`, GitHub Actions, Codespell, markdownlint, Lychee.

**Spec:** `docs/superpowers/specs/2026-08-21-hermes-masterclass-design.md`

## Global Constraints

- Product baseline is Nous Research Hermes Agent `v0.20.5`, tag `v2026.8.19`; version-sensitive instructions must say “Verified against Hermes Agent v0.20.5 (2026-08-19).”
- The repository remains private and is implemented on `codex/hermes-masterclass-first-edition`; completion uses a pull request merged into `main`.
- Platform scope is Apple silicon macOS on a Mac mini; Windows and Linux setup instructions are excluded.
- Manuscript scope is exactly 22 numbered chapters and four appendices totaling 100,000–120,000 measured Markdown words.
- Prose, examples, diagrams, and exercises are net new; do not copy passages, structure, diagrams, or code from `agentic-ai-deep-dive`.
- The extension stack is Hermes-native skills, Hermes plugins, and Hermes-compatible MCP servers; Codex marketplace plugins are excluded.
- Codex is a specialist worker managed by Hermes, not the default always-on supervisor.
- The official model identifier is `gpt-5.6-sol`; never spell it “Soul” or invent a different alias.
- Readers are beginner-to-intermediate and are not expected to code; unavoidable technical work includes a copy-ready prompt for delegating it to Codex.
- Every chapter contains a concrete opening, beginner definitions, a Hermes mechanism, professional and personal examples, authority boundaries, failure/recovery guidance, a reusable field kit, an exercise with answer/rubric, a mastery checklist, and primary references.
- Every numbered chapter contains at least one substantive Mermaid diagram; setup and interface chapters also use relevant official screenshots where available.
- Every consequential workflow uses Green (may act), Amber (may prepare), and Red (may not act) authority boundaries.
- Financial, tax, health, employment, legal, and privacy content teaches preparation and professional handoff, not professional advice.
- Hermes runs under a dedicated macOS account with secondary identities, minimal access, isolated browser/workspaces, managed secrets, and human approval for consequential effects.
- Commands, settings, UI labels, plugins, skills, prices, laws, and platform capabilities require primary-source support; invented operational details are prohibited.
- Screenshot assets are local, copied from the MIT-licensed Hermes repository at the pinned tag, and documented in `docs/assets/images/PROVENANCE.md`; no external image hotlinks or placeholders.
- The site must build with `mkdocs build --strict`, pass `pytest -q`, pass `python tools/check_book.py --final`, and contain no secrets, private family data, unresolved markers, or broken local links.

---

## Planned File Map

### Project and build files

- `README.md` — project overview, local preview, contents, status, and private-publishing note.
- `LICENSE` — MIT license with 2026 credit.
- `CONTRIBUTING.md` — editorial rules, source policy, checks, and update procedure.
- `requirements.txt` — pinned documentation and validation dependencies.
- `mkdocs.yml` — theme, extensions, Mermaid, explicit final navigation, and exclusions.
- `.gitignore` — virtual environments, site output, caches, and SDD workspace.
- `.markdownlint.json` — prose-aware Markdown lint configuration.
- `.codespellrc` — project spelling configuration and product terms.
- `book-manifest.yml` — canonical chapter/appendix order, file paths, part labels, and word targets.
- `tools/check_book.py` — incremental and final manuscript validation.
- `tests/test_check_book.py` — validator unit tests.
- `.github/workflows/quality.yml` — tests, manuscript validation, strict build, Markdown lint, spelling, and links.

### Site foundation

- `docs/index.md` — cover, promise, audience, reading paths, authority legend, and full contents.
- `docs/about.md` — scope, baseline, curator credit, licensing, and source policy.
- `docs/stylesheets/extra.css` — original warm-paper/copper/navy visual system, responsive and print styles.
- `docs/javascripts/extra.js` — progressive enhancement only; no analytics or network calls.
- `docs/assets/images/PROVENANCE.md` — screenshot source paths, tag, license, captions, and chapter usage.
- `docs/assets/images/hermes/` — selected official screenshots and feature images.
- `research/hermes-v2026.8.19-source-map.md` — local source routing guide for chapter authors.

### Manuscript

- `docs/part-1/01-meet-hermes.md`
- `docs/part-1/02-agentic-ai-first-principles.md`
- `docs/part-1/03-hermes-loop.md`
- `docs/part-1/04-write-the-job-description.md`
- `docs/part-2/05-install-hermes-on-mac-mini.md`
- `docs/part-2/06-models-and-routing.md`
- `docs/part-2/07-personality-context-sessions-memory.md`
- `docs/part-2/08-tools-skills-plugins-mcp.md`
- `docs/part-2/09-message-hermes-everywhere.md`
- `docs/part-2/10-goals-and-background-operations.md`
- `docs/part-3/11-family-safe-security.md`
- `docs/part-3/12-identities-burner-accounts-secrets.md`
- `docs/part-3/13-approvals-autonomy-egress-audit.md`
- `docs/part-3/14-sensitive-data-backups-recovery.md`
- `docs/part-4/15-daily-weekly-operating-rhythms.md`
- `docs/part-4/16-job-search-opportunity-pipeline.md`
- `docs/part-4/17-resume-interview-brand.md`
- `docs/part-4/18-family-operations-canada.md`
- `docs/part-5/19-one-two-person-business-os.md`
- `docs/part-5/20-business-functions.md`
- `docs/part-5/21-hermes-as-manager.md`
- `docs/part-6/22-evaluation-observability-capstone.md`
- `docs/appendices/appendix-a-command-reference.md`
- `docs/appendices/appendix-b-templates-playbooks.md`
- `docs/appendices/appendix-c-curated-stack.md`
- `docs/appendices/appendix-d-troubleshooting-glossary-bibliography.md`

---

### Task 1: Build the Site, Research Baseline, and Validation Harness

**Files:**

- Create: all project/build files and site-foundation files listed above
- Copy: selected official images into `docs/assets/images/hermes/`
- Test: `tests/test_check_book.py`

**Interfaces:**

- Consumes: approved design spec and pinned official source checkout `/tmp/hermes-agent-v2026.8.19`
- Produces: buildable MkDocs shell, canonical manifest, source map, image provenance, and validator commands used by every later task

- [ ] **Step 1: Write validator tests before the validator**

  Create tests using temporary book fixtures. Cover: valid incremental manuscript, missing final file, duplicate manifest number, missing required section, out-of-range final word count, unresolved `TODO`/`TBD`/`FIXME`, missing local image, broken local Markdown link, missing Mermaid block, missing reference URL, prohibited “GPT-5.6 Soul,” and accidental secret patterns.

  The tests must assert named diagnostic fragments, for example:

  ```python
  result = run_check(tmp_path, "--final")
  assert result.returncode == 1
  assert "missing chapter: docs/part-1/01-meet-hermes.md" in result.stdout
  ```

- [ ] **Step 2: Run the validator tests and confirm the expected failure**

  Run: `pytest -q tests/test_check_book.py`

  Expected: failure because `tools/check_book.py` does not exist or cannot yet satisfy the fixtures.

- [ ] **Step 3: Implement `book-manifest.yml` and `tools/check_book.py`**

  The validator must support incremental default mode and strict `--final` mode. Final mode enforces exact file count, order, required sections, 100,000–120,000 aggregate words, one Mermaid block per numbered chapter, local link/asset resolution, reference URLs, placeholder hygiene, screenshot provenance, version label, secret-pattern scan, and absence of prohibited product terms. It prints one diagnostic per failure and a summary with file and word counts.

- [ ] **Step 4: Create the MkDocs shell and original visual system**

  Configure Material navigation only for files that exist at this stage; final explicit navigation is added in Task 12. Enable admonitions, footnotes, tables, task lists, code highlighting, Mermaid, search, light/dark palettes, and print CSS. Exclude `docs/superpowers/**` from the rendered site. The home page must explain who the book is for, how to read it, and the Green/Amber/Red legend without pretending unwritten chapters exist.

- [ ] **Step 5: Create the pinned research source map**

  Map every planned chapter to exact official Hermes source paths under `/tmp/hermes-agent-v2026.8.19`, official URLs at tag `v2026.8.19`, and non-Hermes primary authorities needed later. Include commands for verifying current release drift. Record the official OpenAI `gpt-5.6-sol` page. Do not summarize from the reference textbook.

- [ ] **Step 6: Copy and document official visual assets**

  Copy the dashboard admin views, dashboard model views, TUI orchestrator view, desktop session-source view, and four tier feature images that materially help later chapters. Record each upstream repository path, tag, license, local filename, intended chapter, and descriptive alt text in `PROVENANCE.md`.

- [ ] **Step 7: Add project quality configuration**

  Add pinned requirements, `.gitignore`, Markdown lint, Codespell terms, and a GitHub Actions workflow. During incremental work CI may run unit tests and MkDocs; Task 12 switches the manuscript check to `--final` after all files exist.

- [ ] **Step 8: Verify and commit the foundation**

  Run:

  ```bash
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
  .venv/bin/pytest -q
  .venv/bin/mkdocs build --strict
  .venv/bin/python tools/check_book.py
  git diff --check
  ```

  Commit only Task 1 files with message: `build: scaffold Hermes masterclass site`.

---

### Task 2: Write Part I — From Chatbot to Colleague

**Files:**

- Create: `docs/part-1/01-meet-hermes.md`
- Create: `docs/part-1/02-agentic-ai-first-principles.md`
- Create: `docs/part-1/03-hermes-loop.md`
- Create: `docs/part-1/04-write-the-job-description.md`
- Modify: `docs/index.md`, `book-manifest.yml`

**Interfaces:**

- Consumes: chapter contract, pinned source map, validator, and family/business running case
- Produces: conceptual vocabulary and job-charter artifacts referenced by all later chapters

- [ ] **Step 1: Research the four chapter claims against primary sources**

  Read the pinned Hermes README, architecture, agent-loop, prompt-assembly, trajectory, personality, goals, and security documents. Record URLs in each chapter’s References section.

- [ ] **Step 2: Write Chapter 1, 3,600–4,300 words**

  Contrast chatbot, workflow, and always-on agent; introduce the family case, colleague metaphor, authority ladder, trajectory, continuity, and a first “Monday morning” workflow. End with a one-page readiness rubric.

- [ ] **Step 3: Write Chapter 2, 4,000–4,600 words**

  Explain model, harness, loop, tool call, observation, context, state, memory, plan, trajectory, autonomy, and reliability compounding with original arithmetic and diagrams. Make the limits of model intelligence explicit.

- [ ] **Step 4: Write Chapter 3, 4,000–4,600 words**

  Walk through Hermes’s runtime loop, prompt assembly, tools, sessions, persistence, compression, stopping, and uncertain outcomes. Use a single job-research trajectory from request to handback.

- [ ] **Step 5: Write Chapter 4, 3,600–4,300 words**

  Produce the Hermes Job Charter, delegation contract, definition of done, escalation policy, service levels, communication norms, working-hours policy, and first-week probation plan. The full copy-ready charter belongs in the chapter and is later repeated in Appendix B only as a compact template, not verbatim prose.

- [ ] **Step 6: Run incremental checks and commit**

  Run `python tools/check_book.py`, `mkdocs build --strict`, `git diff --check`, and spelling checks limited to the four new files. Commit: `docs: write Hermes foundations`.

---

### Task 3: Write Part II-A — Mac mini, Interfaces, Models, and Memory

**Files:**

- Create: `docs/part-2/05-install-hermes-on-mac-mini.md`
- Create: `docs/part-2/06-models-and-routing.md`
- Create: `docs/part-2/07-personality-context-sessions-memory.md`
- Modify: `docs/index.md`, `book-manifest.yml`

**Interfaces:**

- Consumes: Job Charter and authority ladder from Part I
- Produces: operational installation, provider policy, and profile/memory boundaries used by all workflow chapters

- [ ] **Step 1: Verify commands and screenshots at the pinned Hermes tag**

  Use official installation, quickstart, updating, desktop, CLI/TUI, web-dashboard, configuration, provider, model-catalog, local-Mac, Ollama, session, personality, context, memory, and profile docs. Do not rely on release snippets.

- [ ] **Step 2: Write Chapter 5, 4,000–4,600 words**

  Cover Mac mini sizing decisions, dedicated macOS user, FileVault/firewall/update prerequisites, installer and Desktop paths, setup, first-run verification, TUI/dashboard, gateway service, update receipts, backup, and rollback. Include copy-ready Codex prompts for any terminal work a non-coder may delegate.

- [ ] **Step 3: Write Chapter 6, 4,300–5,000 words**

  Compare local/private, everyday hosted, and frontier lanes; explain Apple-silicon local inference, Ollama or supported endpoints, Nous Portal, OpenRouter, OpenAI API, `gpt-5.6-sol`, fallbacks, cost controls, privacy, reasoning effort, and an explicit routing table. Do not claim ChatGPT subscription credits pay API charges.

- [ ] **Step 4: Write Chapter 7, 4,000–4,600 words**

  Explain `SOUL.md`, context files, sessions, memory, user profile, project profile, Bot Mode, and memory providers. Define what must never be remembered, retention review, family member separation, and recovery from poisoned or stale memory.

- [ ] **Step 5: Verify and commit**

  Run incremental manuscript, build, link, and spelling checks. Commit: `docs: add Mac mini models and memory`.

---

### Task 4: Write Part II-B — Extensions, Channels, and Background Work

**Files:**

- Create: `docs/part-2/08-tools-skills-plugins-mcp.md`
- Create: `docs/part-2/09-message-hermes-everywhere.md`
- Create: `docs/part-2/10-goals-and-background-operations.md`
- Modify: `docs/index.md`, `book-manifest.yml`

**Interfaces:**

- Consumes: model, profile, and memory policy from Task 3
- Produces: vetted capability stack, channel matrix, and scheduling contract used by Parts III–V

- [ ] **Step 1: Verify the extension and channel landscape**

  Read official tools/toolsets, Skills Hub, optional-skills catalog, plugins, MCP, security, messaging index, WhatsApp Cloud, WhatsApp bridge, Telegram, email, SMS, voice, goals, cron, heartbeat, loops, hooks, checkpoints, and automation blueprint docs.

- [ ] **Step 2: Write Chapter 8, 4,300–5,000 words**

  Distinguish tool, skill, plugin, MCP server, provider, and connector. Build a curated native stack for research, productivity, Google Workspace, documents, career work, finance preparation, health routines, smart home, and Codex delegation. For each category include value, permissions, supply-chain questions, maintenance, and a “do not install yet” threshold.

- [ ] **Step 3: Write Chapter 9, 4,000–4,600 words**

  Compare WhatsApp Cloud, unofficial WhatsApp bridge, Telegram, email, SMS, and voice. Recommend secondary identities and a dedicated WhatsApp Business Cloud number. State actual free-tier or charge limitations from provider sources. Include pairing, allowlists, group-room behavior, urgent escalation, and lost-phone procedures.

- [ ] **Step 4: Write Chapter 10, 4,300–5,000 words**

  Explain goals, cron, heartbeat, loops, hooks, persistent cron memory, delivery routes, missed schedules, time zones, duplicate execution, checkpoints, rollback, and kill procedures. Build daily briefing, weekly review, deadline watch, and household reminder automations.

- [ ] **Step 5: Verify and commit**

  Run incremental checks and commit: `docs: cover extensions channels and automation`.

---

### Task 5: Write Part III-A — Host Security and Identity Isolation

**Files:**

- Create: `docs/part-3/11-family-safe-security.md`
- Create: `docs/part-3/12-identities-burner-accounts-secrets.md`
- Modify: `docs/index.md`, `book-manifest.yml`

**Interfaces:**

- Consumes: capability, channel, and background-operation surfaces from Part II
- Produces: threat model, trust envelope, identity inventory, and secret-handling controls required by every later workflow

- [ ] **Step 1: Research load-bearing security claims**

  Use Hermes `SECURITY.md`, security, Docker, managed scope, egress, Iron Proxy, secret providers, credential pools, messaging pairing, Apple platform security, and primary provider security documentation.

- [ ] **Step 2: Write Chapter 11, 4,400–5,000 words**

  Build a family threat model: prompt injection, malicious content, compromised skills/plugins, excessive host permissions, credential leakage, channel impersonation, runaway automation, and physical compromise. Define dedicated user, sandbox/container, filesystem mounts, browser profiles, egress tiers, and emergency stop/rebuild procedures.

- [ ] **Step 3: Write Chapter 12, 4,200–4,800 words**

  Build an identity map for primary, secondary, burner, recovery, business, and child-related accounts. Cover alias mailboxes, dedicated phone/channel identity, WhatsApp Business Cloud, password managers, Hermes secret providers, rotation, recovery codes, test accounts, offboarding, and a quarterly access review.

- [ ] **Step 4: Verify and commit**

  Run incremental checks plus a secret scan. Commit: `docs: establish Hermes security and identity boundaries`.

---

### Task 6: Write Part III-B — Authority, Sensitive Data, and Recovery

**Files:**

- Create: `docs/part-3/13-approvals-autonomy-egress-audit.md`
- Create: `docs/part-3/14-sensitive-data-backups-recovery.md`
- Modify: `docs/index.md`, `book-manifest.yml`

**Interfaces:**

- Consumes: threat model and identity inventory from Task 5
- Produces: policy matrix, audit rhythm, data map, retention schedule, backup/restore plan, and incident drills

- [ ] **Step 1: Verify approval, egress, checkpoint, and privacy mechanisms**

  Use Hermes security, checkpoints/rollback, egress, hooks, trajectories, sessions, managed scope, and backup-relevant docs plus PCI SSC and Canadian privacy authority sources.

- [ ] **Step 2: Write Chapter 13, 4,200–4,800 words**

  Turn Green/Amber/Red into an executable household/business policy. Cover plan versus action approval, time-bounded approval, timeout behavior, egress allowlists, tool restrictions, audit fields, monthly sampling, false-confidence signals, and authority expansion/revocation.

- [ ] **Step 3: Write Chapter 14, 4,400–5,000 words**

  Map PII, PCI, health, school, employment, tax, and business data; minimize collection; define retention and deletion; distinguish encryption, backup, and access control; test restore; handle checkpoint limitations and uncertain external effects; run lost-device, leaked-token, wrong-recipient, and duplicate-action drills.

- [ ] **Step 4: Verify and commit**

  Run incremental checks and a security-language review for overclaims. Commit: `docs: define authority data and recovery controls`.

---

### Task 7: Write Part IV-A — Chief-of-Staff Rhythms and Job Search

**Files:**

- Create: `docs/part-4/15-daily-weekly-operating-rhythms.md`
- Create: `docs/part-4/16-job-search-opportunity-pipeline.md`
- Modify: `docs/index.md`, `book-manifest.yml`

**Interfaces:**

- Consumes: approved identity, channel, scheduling, and audit controls
- Produces: daily/weekly meeting system and ethical job-opportunity pipeline used by Chapter 17

- [ ] **Step 1: Research supported productivity and research capabilities**

  Use official cron, email, Google Workspace, meeting-action, weekly-review, browser, web-search, document, and research skill docs plus primary job-platform terms where claims are necessary.

- [ ] **Step 2: Write Chapter 15, 4,000–4,600 words**

  Build morning briefing, calendar/inbox/task triage, focus plan, end-of-day handback, weekly family council, travel and household administration, commitment ledger, stale-task cleanup, and attention/escalation rules. Avoid granting Hermes the primary inbox.

- [ ] **Step 3: Write Chapter 16, 4,400–5,000 words**

  Build profile intake, target-role thesis, source strategy, job discovery, fit scoring, employer research, opportunity ledger, networking queue, application preparation, follow-up, metrics, and anti-spam/anti-fabrication boundaries. Hermes may prepare applications but may not submit or misrepresent without explicit approval.

- [ ] **Step 4: Verify and commit**

  Run incremental checks and commit: `docs: add chief of staff and job search systems`.

---

### Task 8: Write Part IV-B — Career Brand and Canadian Family Operations

**Files:**

- Create: `docs/part-4/17-resume-interview-brand.md`
- Create: `docs/part-4/18-family-operations-canada.md`
- Modify: `docs/index.md`, `book-manifest.yml`

**Interfaces:**

- Consumes: job pipeline from Task 7 and sensitive-data policy from Part III
- Produces: evidence bank, interview curriculum, family operating calendar, and professional-handoff checklists

- [ ] **Step 1: Research career and Canadian primary sources**

  Use official Hermes document/voice/research tools and primary Government of Canada/CRA/FCAC/provincial education or health authorities for jurisdiction-sensitive statements. Date every changeable threshold or avoid hard-coding it.

- [ ] **Step 2: Write Chapter 17, 4,200–4,800 words**

  Build an evidence bank, master résumé, truthful tailoring, executive bio, LinkedIn/about copy, portfolio narratives, interview question bank, voice mock interviews, scorecards, post-interview review, networking messages, and an anti-hallucination evidence gate.

- [ ] **Step 3: Write Chapter 18, 4,400–5,000 words**

  Build school-year planning, activities and forms, meal/health/fitness routines, household budget preparation, Canadian tax-document collection, benefit/deadline monitoring, retirement-goal inputs, travel, and family review. Clearly separate organization from medical, financial, or tax advice and identify professional handoff points.

- [ ] **Step 4: Verify and commit**

  Run incremental checks, validate government links, and commit: `docs: add career brand and Canadian family operations`.

---

### Task 9: Write Part V-A — The Small-Business Operating System

**Files:**

- Create: `docs/part-5/19-one-two-person-business-os.md`
- Create: `docs/part-5/20-business-functions.md`
- Modify: `docs/index.md`, `book-manifest.yml`

**Interfaces:**

- Consumes: Job Charter, authority policy, audit system, and personal operating rhythms
- Produces: business workspace, project system, functional playbooks, and owner/agent responsibility map

- [ ] **Step 1: Research Hermes business-operation surfaces**

  Use official profiles, Bot Mode, Kanban, deliverable mode, research, document, email, Google Workspace, meetings, browser, cron, hooks, and relevant native skill documentation.

- [ ] **Step 2: Write Chapter 19, 4,200–4,800 words**

  Create the one- or two-person business OS: mission, offers, customer promises, roles, shared glossary, records, projects, Kanban, meetings, decision log, SOPs, risk register, finance handoff, and explicit responsibility assignment between owner, co-owner, and Hermes.

- [ ] **Step 3: Write Chapter 20, 4,600–5,200 words**

  Create practical research, sales, CRM, marketing, content, support, project, operations, and bookkeeping-preparation playbooks. Show one lead-to-customer trajectory and one content-to-campaign trajectory with approval seams, verification, and metrics. Exclude autonomous contracts, payments, or customer promises.

- [ ] **Step 4: Verify and commit**

  Run incremental checks and commit: `docs: build the Hermes small business operating system`.

---

### Task 10: Write Part V-B and Part VI — Management, Evaluation, and Capstone

**Files:**

- Create: `docs/part-5/21-hermes-as-manager.md`
- Create: `docs/part-6/22-evaluation-observability-capstone.md`
- Modify: `docs/index.md`, `book-manifest.yml`

**Interfaces:**

- Consumes: every preceding workflow and safety boundary
- Produces: delegation contract, specialist architecture, scorecard, failure taxonomy, troubleshooting loop, and staged 90-day deployment plan

- [ ] **Step 1: Verify delegation and observability mechanisms**

  Use official delegation, subagent lifecycle, Bot Mode, provider routing, mixture-of-agents, Codex skill, API server, webhook, sessions, trajectories, troubleshooting-quality, checkpoints, goals, and cron docs plus official OpenAI Codex/API documentation where Codex behavior is described.

- [ ] **Step 2: Write Chapter 21, 4,400–5,000 words**

  Teach Hermes as manager of Codex, Hermes subagents, and named Bots. Define when to delegate, task brief, context boundary, tool restriction, shared artifact, verification evidence, retry/fix loop, cost budget, and handback. Include career, business, and family specialist examples without creating an uncontrolled agent swarm.

- [ ] **Step 3: Write Chapter 22, 4,800–5,300 words**

  Define operational scorecards, traces, sampled reviews, cost/latency, completion versus correctness, escalation quality, memory drift, automation failures, incident review, and troubleshooting. Finish with a staged 90-day capstone that moves from read-only assistant to bounded digital employee through explicit evidence gates.

- [ ] **Step 4: Verify and commit**

  Run incremental checks and commit: `docs: add Hermes management evaluation and capstone`.

---

### Task 11: Write Appendices and Complete Reader/Contributor Documentation

**Files:**

- Create: all four `docs/appendices/*.md` files
- Create: `LICENSE`, `CONTRIBUTING.md`
- Replace: `README.md`
- Modify: `docs/about.md`, `docs/index.md`, `book-manifest.yml`

**Interfaces:**

- Consumes: all 22 completed chapters and their references/artifacts
- Produces: compact lookup material, reusable templates, curated extension matrix, consolidated bibliography, glossary, troubleshooting tree, and repository handoff documentation

- [ ] **Step 1: Write Appendix A, 2,000–2,800 words**

  Build a source-verified command/interface reference grouped by setup, status, model, tools, skills, plugins, profiles, gateway, cron, goals, sessions, checkpoints, secrets, update, and recovery. Label version-sensitive commands and avoid duplicating chapter prose.

- [ ] **Step 2: Write Appendix B, 3,000–3,800 words**

  Provide compact copy-ready Job Charter, authority matrix, approval request, task brief, daily briefing, weekly review, job-fit rubric, interview rubric, business SOP, incident record, data-retention schedule, and 90-day scorecard templates with safe default values.

- [ ] **Step 3: Write Appendix C, 2,500–3,200 words**

  Curate Hermes-native skills, plugins, and MCP categories for this book’s workflows. Rate value, permissions, data exposure, setup effort, recurring cost, maintenance, and recommended deployment phase. List only entries verified in official Hermes sources or clearly label external MCP examples with primary links.

- [ ] **Step 4: Write Appendix D, 3,000–3,600 words**

  Provide symptom-to-cause troubleshooting, safe recovery order, glossary, consolidated bibliography, source/version ledger, screenshot provenance pointer, and an update checklist for future Hermes releases.

- [ ] **Step 5: Finish repository documentation**

  README must state the book’s promise, audience, contents, exact local setup commands, check commands, private status, baseline version, curator credit, license, and current measured word count. CONTRIBUTING defines source hierarchy, style, chapter contract, screenshot policy, and version-update procedure.

- [ ] **Step 6: Verify and commit**

  Run incremental checks and commit: `docs: complete appendices and project guide`.

---

### Task 12: Integrate, Render, Audit, and Prepare the Pull Request

**Files:**

- Modify: any manuscript, reference, manifest, style, configuration, or workflow file required to resolve integration findings
- Modify: `mkdocs.yml` with explicit final navigation
- Modify: `.github/workflows/quality.yml` to require final validation
- Create: `docs/reference/editorial-audit.md`

**Interfaces:**

- Consumes: the complete manuscript and all prior task reports/reviews
- Produces: coherent first edition, strict local build, final evidence record, and merge-ready branch

- [ ] **Step 1: Add final explicit navigation and CI gates**

  Navigation order must exactly match the design: Home, six parts with 22 chapters, four appendices, About. CI runs pytest, `check_book.py --final`, `mkdocs build --strict`, Markdown lint, Codespell, and Lychee with deterministic exclusions documented.

- [ ] **Step 2: Run the structural and manuscript audit**

  Verify exact count/order, 100,000–120,000 words, chapter-contract sections, Mermaid presence, references, local assets, version labels, prohibited terms, duplication, unresolved markers, secret patterns, and professional-advice boundaries. Correct every failure.

- [ ] **Step 3: Run a cross-chapter editorial audit**

  Check vocabulary, commands, authority colors, running-case continuity, model names, source dates, cross-links, duplicated explanations, progressive difficulty, and whether every chapter remains understandable to a beginner. Record method, counts, and corrections in `docs/reference/editorial-audit.md`.

- [ ] **Step 4: Render and visually inspect the site**

  Start the local MkDocs server, inspect cover, navigation, search, chapter pages, tables, admonitions, Mermaid diagrams, screenshots, code blocks, dark mode, mobile width, and print CSS. Capture no private data. Correct overflow, illegible diagrams, broken image sizing, and navigation defects.

- [ ] **Step 5: Run the complete local verification suite**

  Run:

  ```bash
  .venv/bin/pytest -q
  .venv/bin/python tools/check_book.py --final
  .venv/bin/mkdocs build --strict
  npx --yes markdownlint-cli2 "**/*.md" "#site/**" "#.venv/**"
  .venv/bin/codespell docs README.md CONTRIBUTING.md
  git diff --check
  git status --short
  ```

  Inspect full output and fix every failure before committing.

- [ ] **Step 6: Commit integration and audit evidence**

  Commit: `docs: finalize Hermes Agent Masterclass first edition`.

- [ ] **Step 7: Push, open the private pull request, inspect checks, and merge**

  Push `codex/hermes-masterclass-first-edition`, open a non-draft PR against `main`, wait for checks, fix any failures through reviewed commits, then merge through the PR. Do not change repository visibility and do not push content directly to `main`.

- [ ] **Step 8: Synchronize and prove the local handoff**

  Update the local checkout to the merged `main`, rerun the full verification suite, and report the absolute local path plus `mkdocs serve` command and local URL.
