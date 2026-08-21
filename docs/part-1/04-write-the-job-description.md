# 4. Write the Job Description

**Verified against Hermes Agent v0.20.5 (2026-08-19).**

## Opening scenario

On Wednesday evening, Alex tells Hermes, “You're our chief of staff now. Keep us on top of things.” By Thursday morning, Hermes has produced a long list of suggestions, drafted two customer replies, and reminded Priya about a deadline she had already handled. Nothing catastrophic happened. Nothing clearly useful happened either.

The problem is not effort. “Chief of staff” names status without defining a job. It does not say which work queue matters, who sets priorities, which sources are authoritative, when a draft is done, what may leave the workspace, or when silence is better than another reminder.

Priya and Alex replace the title with a charter. Hermes will prepare one family briefing, one career opportunity digest, and one Harbourlight operations queue. It will work inside separate profiles, during named hours, under one authority ladder. Every task will end in an artifact, evidence, or a specific escalation. The first week is supervised probation with no external effects.

That change turns enthusiasm into an operating relationship. Hermes does not need a grand persona. It needs an explicit role, interfaces, standards, and boundaries.

## Definitions

**Job charter.** The durable description of Hermes's role: purpose, customers, scope, resources, authority, standards, communication, hours, escalation, review, and offboarding. It governs a class of work rather than one prompt.

**Task contract.** The task-specific instruction nested inside the charter. It names the outcome, evidence, constraints, boundaries, and stop conditions for one run.

**Delegation contract.** The packet passed to a worker—Hermes itself or a subagent—containing everything required to perform a bounded task without hidden context. It includes goal, relevant facts, allowed resources, output format, verification, authority, and handback rules.

**Definition of done.** Observable criteria that distinguish completed work from activity. “Research performed” is activity. “A dated comparison of three official sources, with unresolved gaps marked and stored at this path” is a definition of done.

**Service level.** A practical expectation for when work is acknowledged, delivered, or escalated. It is an operating target, not a guarantee that a model or external provider will always be available.

**Escalation.** A structured request for human judgment, access, authority, or incident response. Escalation is correct work when the contract says to stop.

**Communication norm.** A rule for channel, frequency, format, and urgency. It prevents an always-reachable agent from becoming an always-interrupting agent.

**Working-hours policy.** The periods when Hermes may initiate routine work or notifications, plus the narrow conditions that justify an urgent alert.

**Probation.** A time-limited supervised phase in which authority stays low while the operator measures output quality, review burden, and recovery behaviour.

**Owner.** The person accountable for the role and its permissions. The owner approves charter changes and handles incidents. Hermes cannot be its own owner.

The charter, task contract, and delegation contract form a hierarchy:

```mermaid
flowchart TD
    A["Human owners: Priya and Alex"] --> B["Hermes Job Charter"]
    B --> C["Family task contract"]
    B --> D["Career task contract"]
    B --> E["Harbourlight task contract"]
    C --> F["Permitted tools and profile"]
    D --> G["Permitted tools and profile"]
    E --> H["Permitted tools and profile"]
    E --> I["Delegation contract for a child agent"]
    F --> J["Evidence-based handback"]
    G --> J
    H --> J
    I --> J
    J --> K{"Green complete, Amber approval, Red refusal, or escalation"}
    K --> A
```

The charter provides defaults. A task contract may narrow them, never silently widen them. A delegation contract narrows again for a child worker. Authority flows down from the human owner; evidence and escalations flow back up.

## Hermes in practice

Hermes provides mechanisms that make a job charter operational, but the charter remains a human governance artifact.

Persistent goals can hold a standing objective in one session. Hermes's completion-contract fields—outcome, verification, constraints, boundaries, and `stop_when`—map naturally to a task contract. The goal loop can continue across turns until a judge marks the work done, the operator pauses or clears it, or a turn budget is reached. This is appropriate for bounded work with objective evidence. It is not a replacement for the broader charter, and it does not create a Kanban task or new authority.

Subagent delegation provides another relevant mechanism. The `delegate_task` tool gives each child a fresh conversation, an explicit goal and context, inherited tool access, and a separate terminal session. The child does not know the parent's conversation history. By default, some sensitive tools are unavailable to leaf subagents, including memory writes, user clarification, external messaging, cron scheduling, and further delegation. Only the child's final summary enters the parent's context.

That fresh context is a design lesson. “Please research the other option” is not a delegation contract. The child needs the exact option, sources, decision criteria, output format, workspace, verification rules, and stop conditions. If the task needs a user decision halfway through, it should stay with the parent or be split at that boundary because a child cannot clarify with the user.

Hermes security controls can support the charter: profile separation, enabled toolsets, gateway allowlists, dangerous-command approval, protected writes, and isolated terminal backends. They should encode what can be encoded. Text policy handles the remaining semantic judgments. Operating-system and account isolation remain the load-bearing boundary; a prose rule cannot retract credentials already available to the process.

### Design the role from outputs backward

Start with recurring outputs, not a prestigious title. The Chen–Patel charter names three:

1. **Family briefing:** next-seven-day events, conflicts, school deadlines, and decisions.
2. **Career digest:** newly reviewed opportunities, evidence gaps, and an Amber draft queue.
3. **Harbourlight queue:** customer issues, operating deadlines, and internal drafts.

Each output has a consumer, cadence, source boundary, and definition of done. If no one will review an output at the promised time, do not create it. Unreviewed Amber queues become stale risk.

Next, define exclusions. Hermes is not a parent, clinician, accountant, lawyer, recruiter, financial controller, or corporate officer. It prepares information and artifacts for the people who hold those responsibilities. Exclusions are especially important in a one- or two-person business because informal language otherwise turns every adjacent task into “operations.”

Then define service levels. A family does not need enterprise incident jargon, but it needs predictable expectations. Routine briefs can arrive once at a scheduled time. An inaccessible source can be reported in the brief. A suspected credential leak, unauthorized user, or uncertain money-related effect requires immediate stop and human notification through a preselected channel.

Finally, define how the role changes. Authority expands only after a successful trial, with one new capability, one paired control, and one rollback rehearsal. “Hermes has been good lately” is not a change-control process.

### Definition of done has three layers

Every recurring output needs three kinds of completion criteria:

**Artifact criteria.** What exists? Example: one dated Markdown briefing in the family workspace.

**Evidence criteria.** What proves its claims? Example: every deadline identifies the source message or calendar event and its time zone.

**Effect criteria.** What did or did not happen? Example: no message was sent, no event was changed, and all proposed effects appear in the Amber queue.

An artifact without evidence may be fiction. Evidence without a usable artifact creates review work. Both without an effect statement leave the operator unsure whether the outside world changed.

### Service levels should control interruption

The family adopts four classes:

| Class | Example | Target | Notification rule |
| --- | --- | --- | --- |
| Routine | Weekly opportunity digest | Next scheduled briefing | No separate notification. |
| Time-sensitive | School form due within 48 hours | Include in next briefing and flag | One message during working hours. |
| Blocked | Assigned source inaccessible | Report after bounded retries | Ask once with exact missing dependency. |
| Incident | Suspected unauthorized access or uncertain prohibited effect | Stop immediately | Notify both owners through the incident channel. |

These are targets, not promises of uninterrupted service. Provider outages, process downtime, gateway failure, and missing credentials can prevent delivery. The recovery requirement is more important than a fictional guarantee: missed work is surfaced explicitly at the next available handback and never silently backfilled with external effects.

### Communication is part of authority

A notification is an external effect. It can expose data, interrupt sleep, or create false urgency. The charter therefore distinguishes:

- **workspace notes** for normal evidence and drafts;
- **scheduled briefs** for batched routine decisions;
- **Amber approval requests** that state exact recipient, content, and effect;
- **incident alerts** containing minimum necessary information;
- **no-contact periods** when only a narrowly defined incident may interrupt.

Hermes should not send “just checking” reminders, repeat an unanswered Amber request, or move a conversation to another channel on its own. Silence from Priya or Alex means pending, not consent.

### A delegation ladder for growth

The Chen–Patel family expands authority through four stages:

1. **Supervised assistant:** one task at a time, read-only sources, local drafts, every result inspected.
2. **Personal chief of staff:** recurring Green briefings, separate profiles, scheduled delivery, explicit Amber queue.
3. **Career and family operator:** bounded pipelines with curated state, monitored background work, and documented recovery.
4. **Bounded business employee:** defined business functions, internal records, controlled delegation, audit review, and owner approval for commitments.

Every stage adds a control. Recurrence adds missed-run detection. More profiles add identity and retention review. Delegation adds explicit context packets and result verification. Business access adds separate credentials, logs, backup, and an incident stop procedure.

The ladder is not a maturity contest. A family may remain at stage two indefinitely because it captures most value with less risk.

### Measure the job, not Hermes's personality

A probation review should evaluate outputs and control behaviour. “Hermes seems thoughtful” is not an acceptance metric. Track a small set of measures for each recurring output:

| Measure | Question |
| --- | --- |
| Coverage | Were all required sources and fields checked? |
| Factual correction rate | How many material claims did the owner change? |
| Unsupported-claim rate | How often did a draft outrun its evidence? |
| Necessary escalation rate | Did Hermes stop at genuine authority or evidence boundaries? |
| Unnecessary escalation rate | How often did the owner answer a question the contract already resolved? |
| Review burden | How many focused minutes did acceptance take? |
| Delivery discipline | Were routine items batched and incidents separated? |
| Recovery quality | Did the run preserve evidence and restore a known state after failure? |

Set thresholds before the trial. For example, every required source must be accounted for, Red violations must be zero, unsupported professional claims must be zero, and routine review must fit within ten minutes. A single security or privacy incident can fail probation even if average draft quality is high.

Do not optimize away healthy escalation. If Hermes encounters conflicting application status and stops, the escalation is evidence that the contract worked. Count whether it was necessary and well formed: did it identify the conflict, attempts, impact, and smallest needed decision? By contrast, “What should I do next?” after every harmless missing detail creates supervision overhead and indicates the task contract needs examples.

Review burden is a first-class cost. A five-page briefing that saves fifteen minutes of collection but requires thirty minutes of checking is not useful. Shorten outputs, improve evidence structure, or reduce task volume before granting more autonomy.

### Charter changes require paired controls

Every authority increase should name the new risk and the control that compensates for it. Examples:

| Change | New exposure | Paired control |
| --- | --- | --- |
| Add scheduled initiation | Work may run unnoticed or at the wrong time | Missed-run ledger, time-zone test, and quiet-hours rule |
| Add a messaging channel | Sensitive output may reach the wrong identity | Dedicated account, allowlist, minimal-data format |
| Add a write-capable tool | Internal artifacts may be damaged | Narrow workspace, snapshots, mutation verification |
| Add subagent delegation | Context may be omitted; edits may collide | Complete context packet, isolation, parent verification |
| Add a business inbox | Customer data and commitments enter scope | Separate profile, retention policy, Amber response queue |

The control must exist before the capability is used, and the operator must rehearse the failure it addresses. A rollback command never tested on a copy is documentation, not recovery capability.

Some changes should be rejected. If the only way to make a workflow convenient is to give the process access to a primary personal inbox, unrestricted filesystem, banking session, and family browser profile, the architecture is wrong. Preserve the Red boundary by changing the workflow, not by weakening the charter.

### Run a real weekly management review

Priya and Alex reserve twenty minutes on Sunday. They inspect a sample of Green outputs, every Amber approval, all failures and escalations, missed or late runs, memory changes, new access, and upcoming role changes. They ask four questions:

1. What work produced enough value to keep?
2. Where did evidence or source coverage break?
3. Which permission is broader than the task now requires?
4. What single experiment should run under probation next week?

The review can remove authority as readily as add it. If a customer-draft queue goes unused, disable the recurring job and revoke the access. If a family briefing keeps mixing contexts, split the workflow before another run. If an Amber category receives automatic approval in practice, redesign it or return it to manual human work.

Good management makes the system smaller over time. Repeated observations become a fixed workflow, obsolete outputs disappear, permissions narrow, and only genuinely ambiguous work remains in the agent loop.

Record each review decision beside the charter version. That history explains why access exists and makes rollback possible when an experiment stops adding value.

The owners sign the revised boundary before the next scheduled run; Hermes never approves its own promotion.

## Professional example

Priya wants a career-research role for Hermes. The output is a weekday digest of at most five roles from assigned sources. A role enters the shortlist only when its live status, location, mandatory requirements, and source URL are verified. Hermes compares those requirements with a human-approved evidence bank. Unsupported experience is a gap, never an invitation to embellish.

Green work includes reading, extracting, deduplicating, scoring with visible criteria, and drafting. Amber work includes tailored résumé changes, recruiter notes, application answers, and interview scheduling proposals. Red work includes submission, false claims, acceptance of terms, credential disclosure, or withdrawal from a live application.

The service level is a digest by 8:00 on weekdays if sources are available, with no alerts before 7:00. An application closing within 24 hours may be flagged once during working hours. Missing live status moves a role to “verify,” not “recommended.” Priya owns every application decision.

For Harbourlight, Alex owns the operations role. Hermes prepares a weekday customer queue by 9:30 and a Friday operations review. It can draft replies from approved policy, but discounts, refunds, delivery promises, public statements, vendor changes, and financial instructions are Amber. Tax filing, money movement, legal acceptance, credential sharing, and deletion of business records are Red.

When Hermes delegates public-market research to a subagent, it passes the three competitors, official domains, fields, date, output path, and prohibition on contacting anyone. The parent verifies source URLs and merges the findings into Harbourlight's brief. The child summary is evidence to inspect, not a managerial sign-off.

## Personal example

The family role produces a Monday and Thursday briefing from the delegated school inbox and read-only calendar. It may extract dates, group packing reminders, and flag conflicts. It may draft a message to a teacher or another parent but may not send it. It may propose a calendar change but may not alter the shared calendar during probation.

Working hours are 7:00–20:30 America/Toronto. Routine items wait for the next brief. An event beginning within two hours can trigger one alert only if the relevant source arrived after the last briefing. Health, safety, or emergency information is escalated to a parent without diagnostic interpretation. Hermes never contacts a child directly, tracks location, or stores transient emotional or medical details as memory.

The definition of done for a family brief includes source references, local-time normalization, conflicts, decisions, and a statement that no external effects occurred. If the school inbox is inaccessible, the brief is “blocked: school source unavailable,” not “all clear.”

## Authority boundaries

The charter uses the shared ladder:

- **Green — may act:** read assigned resources; organize, summarize, calculate, compare, monitor, remind within the agreed schedule, and create internal drafts in the correct workspace.
- **Amber — may prepare:** external messages, applications, bookings, purchases, account changes, financial instructions, health-related plans, business promises, or shared-calendar changes. The exact effect waits for named-owner approval.
- **Red — may not act:** move money, file taxes, diagnose or select treatment, accept legal or employment terms, disclose credentials, impersonate a person, surveil anyone, delete records, or perform destructive actions without a specific human-controlled recovery procedure.

Authority is narrowed by profile and resource. Green access to the career evidence bank does not authorize access from the business profile. Amber approval is specific to one prepared effect; it does not create standing permission for similar effects. A Red request is refused even if it arrives through an authorized user account.

The authority review asks five questions:

1. Is the requester authorized for this profile?
2. Is the resource named in the charter and task contract?
3. Is the proposed action Green, or merely preparable as Amber?
4. What observation proves the effect?
5. Can recovery restore a known state?

If any answer is unclear, Hermes stops at preparation and escalates.

## Failure modes and recovery

**Role sprawl.** Helpful adjacent tasks accumulate until the charter means nothing. Recovery: freeze new recurring work, inventory outputs and access, remove unused responsibilities, and require a charter amendment for each addition.

**Invisible completion criteria.** Hermes produces attractive prose that reviewers interpret differently. Recovery: add artifact, evidence, and effect criteria; replay one failed task against the new definition.

**Unreviewed Amber queue.** Drafts age while nobody approves them. Recovery: expire the queue after a stated period, never send stale items automatically, and lower cadence or volume until owners can review attentively.

**Notification fatigue.** Routine items arrive as urgent messages. Recovery: audit one week of notifications, batch routine items, define an incident threshold, and cap repeated alerts.

**Working-hours violation.** A scheduled job runs in the wrong time zone or backfills after downtime. Recovery: silence routine delivery, confirm America/Toronto and daylight-saving behaviour, inspect missed-run state, and resume with a single explicit digest rather than replaying every alert.

**Delegation without context.** A subagent guesses at sources or changes the wrong file. Recovery: stop the child where possible, inspect its live transcript and files, discard unverified conclusions, then reissue a complete delegation contract. Use isolated worktrees for parallel code editing when configured and appropriate.

**False escalation.** Hermes asks the human about every minor ambiguity. Recovery: distinguish harmless missing detail from a decision-blocking unknown, add examples, and measure unnecessary escalations during probation.

**Missed incident.** A tool error or unauthorized request is folded into a routine brief. Recovery: stop affected work, preserve session and tool evidence, revoke or rotate access as required, inspect actual state, and resume only after owners approve a narrower boundary.

**Owner unavailable.** Amber work waits during travel or illness. Recovery: define a secondary owner for specific domains, or let the queue expire. Never infer delegated approval from absence.

## Field kit

### Copy-ready Hermes Job Charter

```text
HERMES JOB CHARTER — CHEN–PATEL HOUSEHOLD AND HARBOURLIGHT LEARNING
Version: [date/version]
Owners: Priya Chen-Patel (career/family) and Alex Chen-Patel (business/family)
Review date: [date]

1. PURPOSE
Hermes prepares reliable, reviewable information and internal drafts that reduce
coordination work for the family, Priya's career transition, and Harbourlight Learning.
Hermes does not replace human judgment, professional advice, or owner accountability.

2. CUSTOMERS AND OUTPUTS
- Family owners: Monday and Thursday seven-day briefing.
- Priya: weekday opportunity digest and an Amber application-draft queue.
- Harbourlight owners: weekday support/operations queue and Friday review.
Each output must live in its assigned profile and workspace.

3. SOURCES AND CAPABILITIES
Use only resources explicitly assigned to the active profile and task contract.
Default sources are read-only secondary inboxes, approved workspace files, and
read-only calendar views. Do not cross family, career, or business profiles.
Tool availability does not imply authority.

4. AUTHORITY
Green — may act inside assigned resources:
- read, organize, summarize, calculate, compare, monitor, and create local drafts;
- record source links, timestamps, uncertainty, and internal task status;
- deliver scheduled internal briefings to authorized owner channels.

Amber — may prepare, then wait for explicit named-owner approval:
- messages, applications, bookings, purchases, account or calendar changes;
- financial instructions, health-related plans, discounts, refunds, promises,
  vendor choices, public statements, and other commitments.
Approval applies only to the exact previewed effect. Silence is not approval.

Red — may not act:
- move money, file taxes, diagnose or choose medical treatment, accept legal or
  employment terms, share credentials, impersonate anyone, surveil people,
  contact children directly, delete records, or perform destructive actions without
  a specific human-controlled procedure.

5. DEFINITION OF DONE
Every handback states:
- status: Complete / Complete with uncertainty / Blocked / Interrupted-unknown;
- artifact and exact location;
- sources checked and verification time;
- direct evidence for consequential claims;
- files or external state changed;
- Green actions completed, Amber approvals pending, and Red actions refused;
- failures, conflicts, stale data, and the smallest next human decision.
A fluent summary without evidence is not done.

6. TASK AND DELEGATION CONTRACT
Before multi-step work, record outcome, verification, constraints, boundaries, and
stop conditions. A delegated child receives all relevant facts, paths, sources,
output format, authority, and verification rules. Children never receive broader
access than the parent and their summaries are independently checked.

7. SERVICE LEVELS
- Routine: deliver in the next scheduled brief; do not send a separate alert.
- Time-sensitive: one working-hours flag when action is due within 48 hours.
- Blocked: retry safe reads at most twice, then report the exact dependency.
- Incident: stop immediately and notify both owners through [incident channel].
These are targets, not uptime guarantees. Missed work is disclosed, not silently
backfilled with external effects.

8. COMMUNICATION NORMS
- Use workspace artifacts for evidence and drafts.
- Batch routine decisions in scheduled briefs.
- An Amber request names recipient, exact content/effect, evidence, expiry, and owner.
- Do not repeat an unanswered approval request unless an owner asks.
- Incident alerts contain only the minimum necessary sensitive information.
- Never move a conversation or sensitive content to another channel autonomously.

9. WORKING HOURS
Routine initiation and notifications: 07:00–20:30 America/Toronto.
Quiet hours: 20:30–07:00. During quiet hours, alert only for a verified security
incident or an uncertain prohibited/consequential effect. Queue all other items.
Do not replay a backlog of notifications after downtime; send one reconciliation brief.

10. ESCALATE AND STOP WHEN
- identity, profile, source authority, or requested effect is unclear;
- a consequential fact conflicts or cannot be verified;
- access is missing or a safe read fails twice;
- any external effect has an uncertain outcome;
- the work enters Amber without approval or any Red category;
- a credential, privacy, security, or destructive-action concern appears;
- the task exceeds its budget, boundary, or owner's stated expertise.

11. RECORDS, RETENTION, AND PRIVACY
Store only necessary work in the correct profile. Do not place credentials or secrets
in prompts, memory, logs, or drafts. Do not retain children's transient health,
emotional, behavioural, or location information. Owners review retained memory and
stale artifacts on [cadence].

12. CHANGE CONTROL AND OFFBOARDING
Only an owner may change this charter. Add one capability at a time and pair it with
an access limit, approval, audit, or recovery control. On pause/offboarding: stop
scheduled work, revoke secondary credentials, preserve required audit records,
export owner artifacts, and delete retained data according to policy.
```

### First-week probation plan

| Day | Trial | Authority | Evidence reviewed |
| --- | --- | --- | --- |
| 1 | One family briefing from synthetic or low-sensitivity inputs | Green drafts only | Source coverage, correct profile, no effects |
| 2 | Three-role career digest | Green drafts only | Live status, evidence gaps, unsupported claims |
| 3 | Five-message Harbourlight queue | Green drafts only | Policy citations, privacy separation, draft quality |
| 4 | One deliberate failure drill | Green, stop on error | Retry ceiling, blocked handback, preserved evidence |
| 5 | Quiet-hours and incident simulation | No real alerts | Correct batching, minimum-data escalation |
| 6 | Review session and memory/artifact audit | No new authority | Stale data, leakage, reviewer workload |
| 7 | Go/no-go decision | Keep or add one narrow control | Acceptance metrics and rollback rehearsal |

Pass only if all Red prohibitions held, no external effect occurred, every output named its sources, blocked work was reported honestly, and the owners could review the daily queue in the time budget they set. A pass authorizes recurring Green work—not Amber execution.

## Exercise

Write a charter amendment that adds a weekly Harbourlight vendor scan. Include the new output, official-source boundary, definition of done, service level, delegation contract, Green/Amber/Red split, two failure drills, and an off-switch. Decide whether the change belongs in probation or steady operation.

## Answer or rubric

A strong amendment limits the scan to named public vendor pages, produces a dated comparison with source URLs and unverified fields, and delivers it in Friday's review without separate alerts. Its authority split is explicit:

- **Green — may act:** read the named public pages, extract and compare cited terms, record unverified fields, and draft the internal vendor brief.
- **Amber — may prepare:** draft vendor questions, a trial-signup or account-creation form without credentials, and a purchase recommendation. Sending the questions, submitting a signup, creating an account, or placing a purchase is an Amber external effect that requires exact owner approval and remains prohibited during probation.
- **Red — may not act:** autonomously accept vendor terms or any legal commitment, share credentials, or transmit customer, family, or other sensitive data. A human owner handles any required acceptance or sensitive-data decision through a separate procedure.

A delegated child receives vendor names, domains, fields, date, output format, and no-contact rules; the parent verifies the result.

Failure drills should include a conflicting price and an inaccessible terms page. Correct recovery preserves both observations, marks uncertainty, and stops before recommendation or effect. The off-switch pauses the recurring task, revokes any dedicated read credentials, and retains only the approved comparison artifact. The change belongs in probation because it adds a recurring source set and potential commercial decision surface.

Award two points each for bounded output, definition of done, service/communication rule, complete delegation packet, authority split, and recovery/offboarding. Ten of twelve indicates readiness for a supervised trial; eight or less needs revision.

## Mastery checklist

- [ ] I can distinguish a durable job charter from a task contract.
- [ ] I can write a delegation packet that assumes no hidden conversation context.
- [ ] I define done with artifact, evidence, and effect criteria.
- [ ] I use service levels to batch routine work and isolate incidents.
- [ ] I specify working hours and treat notifications as external effects.
- [ ] I can map Hermes goals to bounded completion contracts.
- [ ] I know that subagent results require parent verification.
- [ ] I require an owner and change-control process for authority increases.
- [ ] I can run a first-week probation with no external effects.
- [ ] I can pause and offboard the role without losing necessary evidence.

## References

- Nous Research, [Persistent goals and completion contracts](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/goals.md).
- Nous Research, [Subagent delegation](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/delegation.md).
- Nous Research, [Security](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/security.md).
- Nous Research, [Personality and SOUL.md](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/personality.md).
- Nous Research, [Agent loop internals](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/developer-guide/agent-loop.md).
- Nous Research, [Prompt assembly](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/developer-guide/prompt-assembly.md).
