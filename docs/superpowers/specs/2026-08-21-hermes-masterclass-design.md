# Hermes Agent Masterclass — First Edition Design

**Status:** Approved on 2026-08-21  
**Curator:** Moumita Nath  
**Repository:** `monath1/hermes-masterclass` (private)  
**Product baseline:** Nous Research Hermes Agent `v0.20.5` / tag `v2026.8.19`  
**Primary platform:** macOS on an Apple silicon Mac mini  
**License:** MIT

## Purpose

Build a complete, practical textbook for beginner-to-intermediate readers who understand that AI agents exist but do not yet understand how to operate one deeply or safely. The reader will learn to run Hermes Agent as an always-available personal chief of staff, career operator, family assistant, and bounded employee in a one- or two-person digital business.

This is a Hermes textbook, not a general survey of agentic AI and not a Codex textbook. Agent fundamentals appear only where they help the reader reason about Hermes. Codex is introduced narrowly as a specialist harness to which Hermes can delegate suitable coding or artifact-production work.

## Editorial Position

The book will use entirely new prose and examples. It may echo the strengths of the reference textbook `arubhatt/agentic-ai-deep-dive`—economical explanations, concrete openings, named rules, diagrams, running examples, failure analysis, exercises, and primary citations—but it must not copy its passages, chapter structure, diagrams, code, or named system.

The writing should be terse without being shallow. A new reader must be able to follow each chapter, while an intermediate reader should come away with an operational mental model rather than a list of interface features.

Target length is **100,000–120,000 measured Markdown words** across 22 chapters and four appendices. The lower bound matters: “complete first edition” means substantive treatment, not chapter stubs. The upper bound protects the handbook quality the user requested.

## Reader and Running Case

The running case follows a Canadian family of four:

- two earning adults;
- two school-age children;
- one adult navigating a job transition;
- a one- or two-person online business growing from a side project;
- a Mac mini acting as the local, always-on Hermes host.

Hermes develops through four authority stages:

1. supervised assistant;
2. personal chief of staff;
3. career and family operator;
4. bounded multi-function business employee.

Every increase in authority must be paired with a stronger control, isolation boundary, approval rule, or recovery procedure.

## Product Scope

The book covers Hermes Agent on macOS through:

- Hermes Desktop;
- CLI and TUI;
- web dashboard and API server;
- messaging gateways, especially WhatsApp Cloud, Telegram, email, SMS, and voice;
- goals, cron jobs, heartbeats, loops, hooks, checkpoints, rollback, and background delivery;
- personality, context files, sessions, memory, profiles, Bot Mode, and multi-profile operation;
- native Hermes tools, toolsets, skills, plugins, MCP servers, provider routing, and delegation;
- local inference on Apple silicon plus OpenAI, Nous Portal, OpenRouter, and fallback routing;
- specialist delegation to Codex without making Codex the always-on supervisor.

The curated extension stack is **Hermes-native skills, Hermes plugins, and Hermes-compatible MCP servers**. Codex marketplace plugins are excluded.

## Model Strategy

The default deployment teaches three model lanes:

1. **Local/private lane:** a model served on the Mac mini for low-risk summaries, classification, extraction, and private drafting where capability permits.
2. **Everyday hosted lane:** a cost-conscious provider through Nous Portal, OpenRouter, or another Hermes-supported endpoint.
3. **Frontier lane:** OpenAI `gpt-5.6-sol` for complex professional work when its cost and data-routing implications are justified.

“GPT-5.6 Soul” is corrected to the official identifier `gpt-5.6-sol`. Model names, prices, rate limits, and provider behavior are versioned facts and must be cited and labeled with the verification date. The book teaches selection criteria and routing policy rather than claiming one permanent best model.

## Safety and Governance Model

Hermes is a single-tenant personal agent whose effective access is determined by its host environment. The book treats operating-system isolation—not an in-process prompt, allowlist, scanner, or approval dialog—as the load-bearing security boundary.

The recommended family deployment uses:

- a dedicated macOS user account;
- an isolated Hermes workspace and browser profile;
- secondary email and messaging identities rather than primary accounts;
- a dedicated WhatsApp Business Cloud number or other non-primary channel;
- password-manager or Hermes secret-provider integration;
- minimal filesystem mounts and network egress;
- explicit retention, backup, audit, and deletion policies;
- separate personal, family, career, and business profiles;
- human review for consequential actions.

Every workflow uses the same authority ladder:

- **Green — may act:** read, organize, summarize, draft, calculate, remind, and monitor within defined resources.
- **Amber — may prepare:** external messages, applications, purchases, bookings, account changes, financial instructions, health-related plans, and business commitments require approval.
- **Red — may not act:** autonomous money movement, tax filing, medical diagnosis or treatment decisions, legal commitments, credential sharing, impersonation, surveillance, or destructive actions without a specific human-controlled procedure.

Financial, tax, health, employment, and privacy chapters teach preparation and review workflows rather than professional advice. Canadian government and other primary sources must support jurisdiction-sensitive claims.

## Chapter Architecture

### Part I — From Chatbot to Colleague

1. **Meet Hermes: An Agent That Stays on the Job** — chatbot versus agent, the colleague metaphor, authority as a design decision, and the running case.
2. **Agentic AI From First Principles** — model, harness, loop, observation, state, trajectory, autonomy, and failure compounding.
3. **The Hermes Loop** — how Hermes assembles context, selects tools, observes results, persists state, and stops.
4. **Write the Job Description** — role charter, operating contract, service levels, escalation, delegation ladder, and first-day checklist.

### Part II — Build the Mac mini Foundation

5. **Install Hermes CLI, Desktop, and Web Dashboard** — Mac mini preparation, installation, update strategy, profiles, first conversation, and rollback.
6. **Choose Models and Route Work** — local models, Nous Portal, OpenAI, OpenRouter, cost/privacy/quality matrix, fallbacks, and routing policy.
7. **Personality, Context, Sessions, and Memory** — `SOUL.md`, `AGENTS.md`, user memory, workspace boundaries, memory hygiene, and profile separation.
8. **Tools, Skills, Plugins, and MCP** — precise distinctions, curated stack, installation review, permissions, maintenance, and supply-chain risk.
9. **Message Hermes Everywhere** — WhatsApp Cloud, Telegram, email, SMS, voice, account separation, pairing, and channel-specific authority.
10. **Goals and Background Operations** — goals, cron, heartbeats, loops, hooks, delivery, checkpoints, rollback, and missed-run handling.

### Part III — Build the Trust Envelope

11. **The Family-Safe Security Architecture** — threats, trust envelope, dedicated account, OS/container isolation, browser separation, and incident stop controls.
12. **Identities, Burner Accounts, and Secrets** — secondary inboxes, dedicated numbers, aliases, secret stores, rotation, recovery, and offboarding.
13. **Approvals, Autonomy, Egress, and Audit** — green/amber/red policy, allow/deny design, approvals, external effects, logs, and monthly review.
14. **Sensitive Data, Backups, and Recovery** — PII/PCI minimization, retention, encryption, backup/restore, checkpoints, uncertain outcomes, and family incident drills.

### Part IV — Your Personal Chief of Staff

15. **Daily and Weekly Operating Rhythms** — briefing, inbox/calendar/task triage, travel, household administration, weekly review, and focus coaching.
16. **The Job-Search and Opportunity Pipeline** — profile intake, job discovery, fit scoring, research, application ledger, networking, and anti-spam controls.
17. **Résumé, Interview, and Brand Overhaul** — evidence bank, tailored résumé, bios, portfolios, mock interviews, feedback, and truthful positioning.
18. **Family Operations in Canada** — school planning, health and fitness routines, household finance, tax-document preparation, retirement inputs, and professional handoffs.

### Part V — Your First Digital Employee

19. **The One- or Two-Person Business OS** — mission, roles, projects, Kanban, meetings, policies, records, and owner/agent responsibility split.
20. **Research, Sales, Marketing, Support, and Finance** — functional playbooks, CRM hygiene, content pipeline, customer response drafts, bookkeeping preparation, and approval seams.
21. **Hermes as Manager** — delegating to Codex and Hermes subagents, Bot Mode specialists, task contracts, shared artifacts, verification, and handback.

### Part VI — Advanced Operations

22. **Evaluation, Observability, and the 90-Day Capstone** — traces, scorecards, cost and quality review, failure taxonomy, troubleshooting, staged autonomy, and a complete rollout plan.

### Appendices

A. Commands and interface reference.  
B. Copy-ready charters, policies, prompts, checklists, and playbooks.  
C. Curated native skill/plugin/MCP stack with value, risk, cost, and maintenance ratings.  
D. Troubleshooting, glossary, bibliography, version ledger, and source provenance.

## Chapter Contract

Every chapter must contain:

- a concrete opening scenario;
- beginner-friendly definitions before advanced vocabulary;
- an explicit Hermes mechanism or interface;
- at least one professional and one personal example;
- authority boundaries: what Hermes may do, may prepare, and may not do;
- failure modes and recovery procedures;
- a reusable playbook, policy, prompt, or configuration artifact;
- an exercise and a separated answer or rubric;
- a mastery checklist;
- primary references at the end.

Chapters should normally contain 4,000–5,500 words. Structural chapters may be shorter if the total manuscript still meets the target. Commands and settings must come from the pinned official Hermes source or current official documentation. Invented commands, settings, UI labels, plugins, prices, and capabilities are prohibited.

## Site and Asset Design

The book ships as Markdown rendered by MkDocs Material with:

- responsive navigation and search;
- light and dark modes;
- readable typography and constrained line length;
- chapter progress and previous/next navigation;
- print-friendly styling;
- Mermaid and original SVG diagrams;
- selected screenshots from the MIT-licensed official Hermes repository, copied with provenance and version captions;
- no screenshot placeholders or externally hot-linked assets.

The site remains private and is previewed locally with `mkdocs serve`. Public GitHub Pages deployment is excluded.

## Repository and Quality Design

The target repository begins with only `README.md`. The implementation will add:

- `mkdocs.yml` and pinned Python build dependencies;
- `docs/` chapter, appendix, reference, and asset directories;
- custom CSS and lightweight JavaScript only where MkDocs cannot provide the behavior;
- source/provenance manifests;
- automated content checks and tests;
- GitHub Actions for build, links, Markdown quality, spelling, and structural validation;
- contributor and editorial guidance;
- MIT license.

Validation must prove:

- exactly 22 numbered chapters and four appendices are in navigation;
- total Markdown manuscript word count is 100,000–120,000;
- no placeholder markers remain;
- internal links and referenced local assets resolve;
- required chapter-contract sections are present;
- commands highlighted as executable are supported by cited sources;
- the MkDocs strict build succeeds;
- security-sensitive chapters contain the green/amber/red authority model and professional-advice boundaries;
- screenshot provenance and software-version labels are complete;
- the repository contains no secrets or private family data.

## GitHub Workflow

Implementation occurs on `codex/hermes-masterclass-first-edition`, never by direct development on `main`. The final branch is pushed, a pull request is opened, checks are inspected, and the pull request is merged into `main` when green. The repository remains private.

Branch protection is not required for this edition. The current GitHub plan does not permit enabling protection on this private repository, and privacy takes precedence over changing visibility or subscription.

## Source Policy

Use paraphrased prose and primary sources. Priority order:

1. pinned Hermes repository, official docs, security policy, and release notes;
2. official OpenAI documentation;
3. official Apple, Canadian government, Meta, and provider documentation;
4. primary standards and research when needed.

The final appendix records source URL, title, publisher, verification date, affected chapters, and version-sensitive status. Short quotations are unnecessary; explanations should be original.

## Completion Criteria

The first edition is complete only when all planned content and assets exist, validation passes, a clean local site renders, a PR has been merged into private `main`, and the local checkout is synchronized to the merged state. Editorial refinement may follow later, but no chapter may remain a stub or deferred outline.
