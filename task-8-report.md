# Task 8 Report — Career Brand and Canadian Family Operations

## Status

Task 8 is complete on branch `codex/hermes-masterclass-first-edition` in the isolated worktree `/Users/monath/Desktop/HERMES/.worktrees/hermes-masterclass-first-edition`.

The requested commit message is:

```text
docs: add career brand and Canadian family operations
```

The branch and worktree are being preserved for the parent task. Nothing was pushed, merged, or published.

## Deliverables

### Chapter 17

Created `docs/part-4/17-resume-interview-brand.md` at 4,273 measured Markdown words. It contains:

- an evidence bank and reusable claim ledger;
- claim units, wording ceilings, a claim-strength ladder, contradiction review, and an `EVIDENCE GATE: PASS / HOLD` anti-hallucination control;
- a private master résumé and change-controlled truthful tailoring;
- executive-bio, LinkedIn About, and disclosure-safe portfolio workflows;
- an interview question bank, voice mock interview contract, observable-answer scorecard, and post-interview review;
- contextual, low-volume networking-message rules;
- separate native Hermes, bundled skill, reviewed MCP/custom, and human/manual capability seams;
- explicit prohibitions on invented achievements, hidden live interview assistance, impersonation, bulk outreach, autonomous publishing, and unapproved submission;
- professional and personal examples, recovery procedures, a reusable field kit, exercise, rubric, mastery checklist, Mermaid diagram, and primary references.

### Chapter 18

Created `docs/part-4/18-family-operations-canada.md` at 5,000 measured Markdown words. It contains:

- a minimized operating index instead of a central family or child dossier;
- an Ontario school-year map and local-board authority rule;
- activity and form states with guardian-controlled consent and submission;
- administrative meal, health, and fitness routines with clinician/dietitian handoffs;
- household budget preparation with transparent reconciliation and no bank access or money movement;
- a Canadian tax-document index, dated 2026 filing examples, CRA source checks, and taxpayer/professional filing seam;
- official benefit/deadline monitoring with no inferred eligibility;
- retirement-goal inputs and estimate-versus-advice separation;
- a source-dated family travel packet and child-consent/legal handoff;
- a respectful weekly/seasonal family review and a copy-ready `PROFESSIONAL HANDOFF MATRIX`;
- explicit exclusion of primary credentials, raw child dossiers, diagnosis, filing, investment decisions, consent, signatures, bookings, and portal control;
- professional and personal examples, recovery procedures, field kit, exercise, rubric, mastery checklist, Mermaid diagram, and primary references.

### Integration and retained audit

Updated:

- `book-manifest.yml` to mark Chapters 17 and 18 complete with exact word targets;
- `docs/index.md` to list both chapters and advance the completed-book status to Chapters 1–18;
- `CONTRIBUTING.md` with the Task 8 audit command;
- `.github/workflows/quality.yml` so CI checks Task 8 against the pinned Hermes source.

Created:

- `tools/check_task8.py`, a reproducible audit of word ranges, career/family contract markers, unsafe affirmative authority, exact official source URLs and access dates, pinned Hermes reference paths, pinned source assertions, and pinned commit identity;
- `tests/test_check_task8.py`, with end-to-end document mutations plus affirmative and negative authorization cases.

## Source work

Hermes capability claims were checked against the local repository at tag `v2026.8.19`, commit `fcbd1076a93841fa88855acce810e342a5b78101`. The retained audit verifies ten pinned documentation paths and nine load-bearing source assertions covering document extraction, DOCX/PDF verification, voice mode, cron fresh sessions, memory exclusions, tools, email identity, and grounded citations.

Canadian and career claims use fourteen exact primary official URLs, each carrying a visible `accessed 2026-08-21` date:

- Government of Canada Job Bank occupational outlooks;
- Ontario Ministry of Education school-year calendars;
- Health Canada Canada's Food Guide;
- Public Health Agency of Canada physical-activity guidance;
- Ontario Health811 information;
- Financial Consumer Agency of Canada budget guidance;
- CRA 2026 filing-season, tax-slip, and record-retention pages;
- Government of Canada Benefits Finder and benefit payment dates;
- Canadian Retirement Income Calculator;
- Global Affairs Canada travel advisories and child consent-letter guidance.

Changeable dates and thresholds are either avoided or explicitly framed as dated examples. Chapter 18 identifies the 2026 individual and self-employed filing dates only within a 2026 filing-season paragraph, tells readers to recheck the relevant tax-year page, and dates the CRA record-retention threshold. Benefit amounts and schedules, retirement benefit amounts, travel requirements, and board-specific school dates are not hard-coded.

## Test-first evidence

The first Task 8 test run failed during collection with `ModuleNotFoundError: No module named 'check_task8'`, proving that the new audit did not exist. The authorization scanner was then implemented and run independently; its first run found a real plural-handling defect in the tax-return pattern. After the pattern was corrected, all 20 focused affirmative/negative scanner cases passed.

The complete Task 8 suite now contains 53 tests. Mutation checks prove that the audit fails when:

- an affirmative raw-child-dossier authorization is appended;
- the evidence-gate marker is removed;
- the professional-handoff matrix is removed;
- any one of fourteen exact official URLs is replaced;
- an official reference's visible verification date is changed;
- the supplied pinned Hermes repository has the wrong commit.

The negative cases prove that explicit prohibitions such as “Hermes cannot diagnose,” “must not use primary credentials,” and “may not invent achievements” are not falsely reported as unsafe permissions.

## Counts

- Chapter 17: 4,273 words, 414 lines.
- Chapter 18: 5,000 words, 425 lines.
- New chapter total: 9,273 words.
- Draft manuscript after Task 8: 18 chapter files, 80,223 words.
- Focused Task 8 tests: 53.
- Full pytest suite: 148 tests.
- New audit implementation: 337 lines.
- New audit regression suite: 202 lines.
- Files created: 5, including this report.
- Existing files modified: 4.

## Verification evidence

The implementation tree produced these results before commit:

```text
.venv/bin/python tools/check_book.py
check_book: OK — 18 files, 80223 words

.venv/bin/python tools/check_task6.py --hermes-source /tmp/hermes-agent-v2026.8.19
check_task6: OK — 2 chapters; pinned source verified

.venv/bin/python tools/check_task7.py --hermes-source /tmp/hermes-agent-v2026.8.19
check_task7: OK — 2 chapters; pinned source verified

.venv/bin/python tools/check_task8.py --hermes-source /tmp/hermes-agent-v2026.8.19
check_task8: OK — 2 chapters; pinned source verified

.venv/bin/pytest -q
148 passed

.venv/bin/mkdocs build --strict
Documentation built successfully

.venv/bin/codespell docs README.md CONTRIBUTING.md research
exit 0

.venv/bin/python -m py_compile tools/check_task8.py tests/test_check_task8.py
exit 0

git diff --check
exit 0
```

The complete suite is rerun after this report is added and immediately before the requested commit.

## Concerns and follow-up

- The manuscript is intentionally incomplete after Chapter 18. Chapters 19–22 and the four appendices remain for later tasks, so `check_book.py --final` is not appropriate yet; the contributor guide explicitly reserves it for the complete manuscript.
- Chapter 18 is exactly at its 5,000-word ceiling. Future edits must replace or tighten prose unless the approved target changes.
- Canadian tax, benefit, health-service, school-calendar, retirement, and travel information is time-sensitive. The retained audit protects the selected URLs and the visible verification date, but a later edition still needs a substantive source review rather than a date-only update.
- The checker detects a bounded set of realistic unsafe affirmative phrasings and document-contract mutations. It is a regression guard, not a general natural-language safety proof. Human editorial review remains required.
- A whole-repository Markdown lint run currently reports 172 existing issues in earlier plans, SDD artifacts, chapters, and the established continued numbering in `docs/index.md`. The three net-new Task 8 Markdown files report zero scoped lint issues. Fixing the inherited lint backlog is outside this task and remains integration work.
- No real family data, child records, credentials, account identifiers, or application data were added. All names and operational examples remain fictional.
