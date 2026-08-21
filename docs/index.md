# Hermes Agent Masterclass

## A practical operating handbook for a capable, bounded personal agent

This book is for people who can see the promise in AI agents but want a dependable way to use one in everyday life. It follows a Canadian family operating Hermes Agent from a dedicated Apple-silicon Mac mini: first as a supervised assistant, then as a personal chief of staff, then as a carefully bounded partner for career, family, and a small business.

The first edition is being written in public view inside this private repository. The navigation deliberately includes only the pages that exist today; chapter navigation will grow with the manuscript.

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

## What this edition will cover

The planned manuscript has 22 chapters and four appendices: foundations, Mac mini setup, trust and recovery, chief-of-staff operations, a small-business operating system, and a 90-day capstone. Until those chapters are authored and reviewed, this site makes no claim that they are already available.

## Local preview

```shell
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve
```

The site is a local, private preview. It is not configured for public deployment.
