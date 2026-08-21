# Hermes Agent Masterclass

## A practical operating handbook for a capable, bounded personal agent

This book is for people who can see the promise in AI agents but want a dependable way to use one in everyday life. It follows a Canadian family operating Hermes Agent from a dedicated Apple-silicon Mac mini: first as a supervised assistant, then as a personal chief of staff, then as a carefully bounded partner for career, family, and a small business.

The first edition is being written in public view inside this private repository. Part I establishes the vocabulary, runtime model, and operating contract used throughout the manuscript. Part II turns that contract into a secured Mac mini installation, a three-lane model policy, inspectable continuity boundaries, a vetted extension stack, safe messaging routes, and controlled background operations. The navigation deliberately grows only as complete chapters are added.

## How to read this book

Start with `research/hermes-v2026.8.19-source-map.md` if you want to inspect the pinned product evidence. Read the chapters in order for the full operating model. If you are already comfortable with agents, use the chapter checklists and field kits as a reference—but do not skip the security and authority material before giving Hermes real access.

Every version-sensitive instruction will be labeled **Verified against Hermes Agent v0.20.5 (2026-08-19).** Commands and interface labels are researched against that pinned release, not recalled from memory.

## The authority legend

| Level | Hermes may do | Human role |
| --- | --- | --- |
| Green | Read, organize, summarize, draft, calculate, remind, and monitor inside defined resources. | Set the boundaries and review outcomes. |
| Amber | Prepare messages, applications, purchases, bookings, account changes, financial instructions, health plans, and business commitments. | Approve before anything leaves the workspace or creates an external effect. |
| Red | Move money, file taxes, diagnose or choose medical treatment, make legal commitments, share credentials, impersonate someone, surveil people, or perform destructive actions. | Use a specific human-controlled procedure; Hermes does not act autonomously. |

The book treats operating-system isolation, limited identities, and recovery practice as real controls. A prompt, a scanner, or an approval dialog is useful, but none replaces a sound host boundary.

## Part I — From Chatbot to Colleague

1. [Meet Hermes: An Agent That Stays on the Job](part-1/01-meet-hermes.md) — decide when an agent is appropriate, set the authority ladder, and test operational readiness.
2. [Agentic AI From First Principles](part-1/02-agentic-ai-first-principles.md) — separate the model, harness, context, state, trajectory, autonomy, and reliability problem.
3. [The Hermes Loop](part-1/03-hermes-loop.md) — follow one research job through prompt assembly, tool observations, persistence, compression, stopping, and handback.
4. [Write the Job Description](part-1/04-write-the-job-description.md) — adopt a copy-ready charter, service levels, delegation contract, and supervised first-week plan.

Read these chapters in order before granting recurring access. Returning readers can use the Chapter 1 readiness rubric, Chapter 2 diagnostic card, Chapter 3 handback contract, and Chapter 4 Job Charter as operating references.

## Part II — Build the Mac mini Foundation

5. [Install Hermes CLI, Desktop, and Web Dashboard](part-2/05-install-hermes-on-mac-mini.md) — prepare a dedicated macOS host, prove each Hermes interface, install the gateway, and rehearse update and rollback.
6. [Choose Models and Route Work](part-2/06-models-and-routing.md) — adopt local/private, everyday hosted, and `gpt-5.6-sol` frontier lanes with explicit cost, privacy, fallback, and verification rules.
7. [Personality, Context, Sessions, and Memory](part-2/07-personality-context-sessions-memory.md) — separate `SOUL.md`, project context, sessions, built-in and external memory, profiles, and Bot Mode, including what must never be remembered.
8. [Tools, Skills, Plugins, and MCP](part-2/08-tools-skills-plugins-mcp.md) — distinguish extension types, curate a Hermes-native stack, and require permission, supply-chain, confinement, removal, and maintenance evidence.
9. [Message Hermes Everywhere](part-2/09-message-hermes-everywhere.md) — choose secondary identities across WhatsApp Cloud, Telegram, email, SMS, and voice with pairing, group, cost, escalation, and lost-device controls.
10. [Goals and Background Operations](part-2/10-goals-and-background-operations.md) — select goals, cron, heartbeats, loops, and hooks; make delivery duplicate-safe; and deploy four bounded recurring workflows.

Complete these chapters before connecting real family or business channels. Chapter 5's installation ledger, Chapter 6's route card, Chapter 7's retention review sheet, Chapter 8's extension card, Chapter 9's channel card, and Chapter 10's background-operation contract become the operating evidence used by later workflow chapters.

## What this edition will cover

The planned manuscript has 22 chapters and four appendices: foundations, Mac mini setup, trust and recovery, chief-of-staff operations, a small-business operating system, and a 90-day capstone. Chapters 1–10 are complete; later chapters remain unavailable until authored and reviewed.

## Local preview

```shell
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve
```

The site is a local, private preview. It is not configured for public deployment.
