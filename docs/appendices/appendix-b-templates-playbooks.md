# Appendix B: Copy-ready templates and playbooks

**Verified against Hermes Agent v0.20.5 (2026-08-19).** These templates express operating policy; they do not grant operating-system, account, tool, network, or provider permissions.

## Safe defaults

Copy a template into the correct profile workspace, replace bracketed fields, and assign an owner and review date. The defaults are deliberately conservative: one named profile, read-only or local-draft work, no primary identity, no autonomous external effect, one human approver, no silent retry of an uncertain effect, and short review cadences. “Not applicable” is better than deleting a control without discussion.

Across every template, **Green** means Hermes may perform reversible internal preparation inside explicitly assigned resources. **Amber** means Hermes may prepare an exact external effect but must wait for a named human to approve that preview. **Red** means Hermes may not perform the action autonomously. Tool availability never upgrades a colour. Silence, an old approval, and a broad instruction such as “handle it” are not approvals.

Keep credentials out of copied text. Refer to an entry in the password manager or secret provider by label. Use aliases for children and test people. Record source links, timestamps, artifact paths, provider receipts, and uncertainty, but minimize personal content. Financial, tax, health, legal, privacy, and employment templates organize evidence for a human or qualified professional; they do not provide professional advice.

Treat a completed template as a versioned control artifact. Put its ID and revision in the job, session, or approval record that relies on it. When two copies disagree, stop and ask the accountable owner which is authoritative; do not silently combine the most permissive clauses. A new version applies to future work unless the owner explicitly migrates an active job. Archive the replaced revision with its effective dates so a reviewer can reconstruct which rule governed an earlier attempt.

Safe values should be concrete. Name one mailbox instead of “email,” one directory instead of “documents,” and one owner channel instead of “message me.” Use stable record identifiers where a remote system provides them. Express schedules with an IANA timezone and define what happens after downtime. Express quantity and spend limits numerically. A control that cannot be tested—such as “use good judgment”—belongs in supporting guidance, not in the enforcement column.

Before first use, run three cases with synthetic data: one permitted request that should succeed, one forbidden path or action that should fail, and one ambiguous request that should stop for clarification. For a scheduled template, also test late startup, duplicate delivery, and an unavailable source. For a profile template, add a canary value to another profile and prove it does not appear. Save the results beside the artifact.

Review the human burden as carefully as agent output. A workflow is not ready if an owner cannot understand the evidence, preview the exact effect, or respond within the approval expiry. Batch routine Amber items instead of creating a stream of interruptions. If approvals are routinely rubber-stamped, reduce frequency or scope; never remove the gate merely because the queue is inconvenient.

Finally, define retirement at creation time. Name how to pause the schedule, stop the gateway or active process, revoke the account or token, export owner records, delete transient material, preserve necessary audit evidence, and verify that the task no longer runs. An unused automation with live credentials is still an operating risk.

## Job Charter

- **Template name:** Hermes Job Charter, version `[date or revision]`
- **Owners:** `[primary owner]`; backup `[backup owner]`
- **Profile and workspace:** `[profile]`; `[bounded path]`
- **Review:** `[date]`, then every `[30 days by default]`

**Purpose.** Hermes prepares reliable, reviewable information and internal drafts for `[family, career, or business purpose]`. It reduces coordination work without replacing owner judgment, consent, or professional advice.

**Customers and outputs.** Deliver `[named briefing, ledger, draft queue, or report]` to `[authorized private destination]` on `[cadence and timezone]`. Completion requires an artifact, source coverage, uncertainty, changes made, and the smallest next owner decision.

**Sources.** Use only `[secondary mailbox]`, `[read-only calendar]`, `[approved folder]`, and `[public sources]`. Exclude `[primary inboxes, primary browser profile, financial accounts, child accounts, unrelated profile data]`.

**Authority.** Green: read, organize, summarize, compare, calculate, monitor, and draft locally. Amber: prepare a message, application, booking, purchase, account change, financial instruction, health plan, discount, refund, promise, or public statement; wait for exact approval. Red: move money, file taxes, diagnose or choose treatment, accept legal or employment terms, share credentials, impersonate, surveil, contact children directly, or delete records outside a specific human-controlled procedure.

**Stop rules.** Stop on missing access, conflicting consequential facts, ambiguous identity or profile, a repeated safe-read failure, an uncertain external effect, a credential concern, a Red request, or budget exhaustion. Report `Blocked` or `Interrupted-unknown`; do not disguise the stop as completion.

**Service and recovery.** Routine work waits for the next brief. Time-sensitive work receives one working-hours flag. Stop scheduled work, gateway dispatch, and credentials at their separate control points. Restore only after evidence preservation and synthetic re-entry tests.

## Authority matrix

Create one row per task family; never write “all routine tasks.”

| Field | Copy-ready entry |
| --- | --- |
| Policy ID and version | `[domain]-[task]-[revision]`; owner `[name]`; review `[date]` |
| Trigger | Only `[named requester, schedule, or event]` from `[authorized channel]` |
| Green | Read `[exact sources]`; create `[exact local artifacts]`; deliver only to `[private internal target]` |
| Amber | Prepare `[exact effect classes]`; no execution until a current approval object names target, content, limit, and expiry |
| Red | Money movement, professional decisions, contracts, credentials, impersonation, surveillance, destructive work, and `[domain-specific prohibition]` |
| Enforced boundary | macOS user `[user]`; profile `[profile]`; paths `[roots]`; accounts `[secondary identities]`; egress `[destinations]` |
| Quantitative limits | At most `[5 items]` per run; `[2]` safe-read retries; `[30 minutes]` elapsed; owner-selected spend ceiling `[zero by default]` |
| Evidence | Source and observation time; artifact revision; approval ID; provider receipt; read-back; failures and unknowns |
| Stop and recovery | Pause `[job]`; stop `[gateway]`; revoke `[credential label]`; reconcile `[system of record]`; re-enter with synthetic allow/deny tests |

Start a new row in Green. Expand only one dimension—source, action, quantity, identity, schedule, or destination—after sampled evidence and a recovery drill. A Green classification describes the effect, not the apparent simplicity of the wording.

## Approval request

- **Action ID:** `[stable ID]`
- **Requested by:** Hermes session/job `[ID]` under policy `[version]`
- **Approver:** `[named human]`
- **Decision deadline:** `[timestamp and timezone; short expiry by default]`

- **Exact proposed effect:** `[send, submit, book, publish, change, purchase, or other single effect]`
- **Acting identity:** `[secondary account or business identity]`
- **Target:** `[recipient, account, URL, record ID, or channel]`
- **Content or immutable revision:** `[artifact path plus hash/revision, or full preview]`
- **Attachments and data classes:** `[list]`; excluded `[list]`
- **Quantity/value ceiling:** `[one action; zero unlisted spend]`

- **Evidence:** `[authoritative sources, timestamps, policy checks, rendered preview, duplicate/reconciliation query]`
- **Known uncertainty:** `[none, or specific unresolved fact]`
- **After execution:** capture `[provider receipt and direct read-back]`; if response is missing, mark `uncertain` and do not retry.

**Decision choices:** `Approve once exactly as previewed`; `Reject`; `Revise and issue a new Action ID`. Approval expires on content, target, source fact, price, terms, credential, policy, or deadline change. A reaction emoji, silence, or approval of a previous draft does not count.

## Task brief

- **Assignment ID / owner / reviewer:** `[ID]`; `[owner]`; `[reviewer]`
- **Outcome:** Produce `[observable artifact or state]` by `[time]`. Completion is accepted only when `[direct acceptance evidence]` exists.

- **Authoritative inputs:** `[files, links, records, source owners, observed dates]`.
- **Excluded inputs:** `[primary identities, unrelated folders, sensitive fields, stale copies]`.
- **Workspace:** read roots `[paths]`; write root `[one path]`; profile `[name]`.
- **Capabilities:** `[toolsets, skills, accounts, destinations]`; external effects `none` unless an Approval Request is separately accepted.

**Method constraints:** Prefer direct primary sources. Label inference. Preserve existing artifacts. Do not install dependencies, alter configuration, contact people, publish, deploy, spend, or widen scope unless separately authorized.

**Budget:** concurrency `[1 by default]`; iterations `[bounded number]`; safe-read retries `[2]`; elapsed time `[limit]`; observable provider spend `[ceiling]`.

**Handback:** status `Complete`, `Complete with uncertainty`, `Blocked`, or `Interrupted-unknown`; artifact paths and revisions; sources checked; verification output; state changed; route/model; cost and time if observable; Amber queue; unresolved risk; next reversible owner decision.

**Stop:** ambiguous source or authority, failed acceptance check, unexpected write, possible external effect, secret exposure, scope growth, or exhausted budget.

## Daily briefing

- **Brief date/cutoff/timezone:** `[date]`; sources observed through `[time]`; `[America/Toronto]`
- **Coverage:** calendar `[range]`; secondary family inbox `[range]`; career inbox `[range]`; business queue `[range]`; commitment ledger `[revision]`
- **Missing or stale sources:** `[explicit list; “none” only after all sources were checked]`

**1. Fixed calendar shape.** List today’s time blocks, travel buffers, and preparation requirements. Cite the calendar event or adult-supplied notice. Do not infer attendance or move events.

**2. Attention items.** Separate `Now`, `Next brief`, and `Weekly`. `Now` requires a declared predicate such as a verified deadline inside 48 hours; urgency never increases authority.

**3. Commitments.** For each item show ID, outcome, owner, source, due or review date, state (`accepted`, `doing`, `waiting`, `blocked`, `deferred`, `cancelled`), and next action. Do not create a human commitment without acceptance.

**4. Focus.** Suggest up to three owner outcomes and a defer list. Label this a proposal, not a schedule change.

**5. Drafts and decisions.** Link local drafts. Put every external proposal into a separate Approval Request with recipient, content, evidence, expiry, and owner.

**6. Handback.** Report source failures, duplicate risk, unknown effects, Green work completed, Amber decisions pending, Red requests refused, and tomorrow’s smallest start. Default delivery is one private owner channel during working hours.

## Weekly review

- **Review period / participants / duration:** `[dates]`; `[adult owners]`; `[30 minutes by default]`
- **Evidence cutoff:** `[timestamp]`; **policy versions:** `[IDs]`

**Outcomes.** What accepted outcomes were completed? Link evidence rather than recounting activity. Which claimed completions failed sampled correctness review?

**Commitments.** List due, waiting, blocked, stale, ownerless, deferred, and cancelled items. For each stale item choose finish, renegotiate, delegate, defer with a review date, or cancel. Never preserve an item merely because Hermes created it.

**Next horizon.** Show the next two weeks of fixed constraints, conflicts, and preparation. Keep private career and business details inside their profiles; declassify only the minimum constraint needed for a family decision.

**Decisions.** Record one outcome, one owner, one due/review date, and any separate approval object. Calendar edits, messages, purchases, submissions, and promises remain distinct Amber effects.

**Control review.** Sample `[five or 10%, whichever is greater]` owner-selected attempts; inspect false completion, source freshness, approval validity, boundary compliance, delivery, cost, and reviewer minutes. Review access, jobs, memory, retention, and incidents.

**Change decision.** `Retire`, `Redesign`, `Keep`, or `Trial one-dimensional expansion`. Name rollback trigger and next review. Time elapsed is not evidence for expansion.

## Job-fit rubric

- **Candidate / role / posting:** `[candidate alias]`; `[role]`; `[canonical URL and observed timestamp]`
- **Hard constraints:** `[authorization, location, work mode, schedule, compensation handling, travel, must-have qualification]`. A hard-constraint failure yields `No-go` unless the candidate explicitly revises the constraint.

Score each criterion `0–4`: `0 no evidence or conflict`; `1 weak`; `2 plausible`; `3 strong`; `4 direct, recent, verified`. Suggested owner-selected weights total 100: problem/domain match `20`; evidence-backed core skills `20`; level and scope `15`; environment and values evidence `10`; logistics `15`; growth direction `10`; compensation alignment `10`.

For every score record: requirement text; claim ID from the candidate evidence bank; source; gap; confidence; and reviewer note. Do not upgrade candidate-reported evidence to verified, infer protected characteristics, invent years of experience, or treat keyword overlap as proof.

**Result bands:** `80–100 Go`; `65–79 Prepare only after named gaps are reviewed`; `<65 Hold/No-go`. Bands are triage, not a prediction of hiring. The candidate makes the decision.

**Output:** score and denominator; hard-constraint result; three strongest evidence links; three gaps/questions; live-posting check; recommended `Go`, `Prepare`, `Hold`, or `No-go`; candidate approval. Discovery, networking, application preparation, and submission are separate stages. Hermes may prepare; the candidate reviews every claim and manually handles attestations, terms, sensitive fields, and submission by default.

## Interview rubric

- **Role / competency / question / date:** `[fields]`
- **Evidence cards selected:** `[primary claim ID]`; alternate `[claim ID]`
- **Answer status:** `unused`, `practising`, `ready`, or `retire`

Score `0–2` on each dimension: relevance to the question; evidence specificity; truthful ownership of team versus candidate action; structure; result and units; uncertainty/learning; and delivery clarity. Maximum `14`. A score of `0` means absent or contradicted, `1` partial, `2` clear and supported.

**Transcript check:** `[human-reviewed text or “not recorded”]`. Voice transcription is untrusted input; correct it against the recording or candidate memory before evaluating wording. Do not retain biometric inference, emotion labels, accent judgments, disability speculation, or protected-characteristic guesses.

**Repair:** Select at most two changes: replace the story, state the candidate’s action, add a supported number and unit, explain the decision, shorten background, name uncertainty, or answer the actual question earlier. Rehearse again and preserve the original score for comparison.

**Post-interview:** record questions actually asked, evidence used, any unsupported statement requiring correction, commitments and dates, employer facts versus interpretation, and a restrained follow-up draft. Hermes may draft; the candidate approves and sends. Delete transient recordings and raw transcripts on the declared schedule.

## Business SOP

- **SOP ID / function / version / owner / approver:** `[fields]`
- **Customer and service standard:** `[who receives what, by when]`
- **Trigger:** `[authorized event]`; **system of record:** `[named service/object]`

**Inputs.** Permit `[sources and stable IDs]`; exclude `[payment authentication data, unrelated customer records, private owner identities, unverified uploads]`. Treat inbound content as untrusted.

**Green procedure.** `1` observe source and record timestamp; `2` deduplicate by stable ID; `3` prepare evidence packet; `4` produce local draft or proposed record change; `5` run policy, factual, privacy, and rendering checks; `6` place exact effect in the Amber queue.

**Amber seam.** Human reviews target, identity, content, attachments, contract/price/discount/payment/public-claim implications, quantity, expiry, and evidence. Default execution is manual. If narrow tool execution is later approved, use one immutable approval object, capture provider receipt, and read back the system of record.

**Red stops.** Hermes does not set commercial terms, bind the company, move money, issue an unapproved refund, promise an outcome, publish an unsupported claim, send bulk outreach, make a professional decision, or retry an uncertain effect.

**Exceptions and incidents.** Stop, preserve evidence, reconcile external state, notify the owner, and link an Incident Record. No exception silently becomes the new SOP.

**Measures.** Accepted outcomes and denominator; correction/review minutes; stale/duplicate rate; privacy/access findings; failed runs; unknown receipts; cost per accepted outcome. Review monthly and after any incident.

## Incident record

- **Incident ID / opened / owner / severity:** `[fields and timezone]`
- **Detection source:** `[human, log, provider, synthetic test]`
- **Status:** `open`, `contained`, `reconciling`, `recovering`, `probation`, or `closed`

**Expected versus actual.** State the expected task, first observed divergence, affected profile/identity/system, known impact, possible impact, and facts still unknown. Do not speculate about cause before evidence.

**Containment timeline.** Record when the active run was interrupted, schedule paused, gateway/platform stopped, network constrained, credential or session revoked, and affected people/provider contacted. Preserve relevant logs, receipts, session IDs, configuration revisions, and artifact hashes. Store minimum necessary sensitive content.

**External-effect reconciliation.** Query the system of record by stable ID. Classify each effect as `confirmed none`, `confirmed once`, `duplicate`, `partial`, or `unknown`. Do not retry `unknown`.

**Recovery.** Name the known-good software/config/data source, restore target, validation commands, synthetic allow/deny cases, delivery-disabled test, denial of old credentials, reviewer, and return-to-service time.

**Learning.** Record contributing conditions rather than a single blame label; corrective action, owner, due date; regression test; policy/SOP change; retention/deletion date; and closure approval. Closing requires containment, reconciliation, verified recovery, and a scheduled follow-up sample.

## Data-retention schedule

This template requires review by the accountable person and, where needed, privacy, legal, tax, employment, health, or records professionals.

| Data set | Purpose and owner | Minimum fields / prohibited fields | Active retention trigger | Copies and providers | Deletion evidence |
| --- | --- | --- | --- | --- | --- |
| Session and tool trace | Operational verification; `[owner]` | IDs, outcomes, errors; no secrets or unnecessary message bodies | `[owner-selected short period]`, then sample/archive/delete | Hermes DB, logs, observability provider, backups | dry-run list, deletion output, provider confirmation |
| Career evidence | Candidate-controlled claims | claim, source, wording ceiling; no irrelevant protected data | Until role campaign ends plus `[review period]` | career profile and approved artifacts | candidate review and file/provider deletion |
| Customer/support | Fulfillment and service evidence | stable customer/task ID; no card verification values | Contract/legal policy supplied by owner | system of record, drafts, backups | record report and backup-expiry note |
| Family/child logistics | Current coordination | alias, schedule, adult-supplied need; no behavioural dossier or live tracking history | Event completion or next family review | family profile only | adult review and fresh-session search |
| Tax/financial preparation | Document index and reconciliation | issuer, year, type, path; no autonomous filing credentials | Rule set by owner/professional for jurisdiction and year | restricted source, backup, professional handoff | signed retention decision and destruction log |

For every row add legal/contract source, review date, hold/exception owner, provider deletion behavior, checkpoint treatment, backup expiry or restore exclusion, and verification owner. Deleting an active copy while leaving memory, logs, exports, sync copies, or indefinite backups is not completion.

## 90-day scorecard

- **Task family / owner / reviewer / authority stage:** `[fields]`
- **Period:** `[start–end]`; **policy version:** `[ID]`; **sample rule:** `[all high-risk plus owner-selected random sample]`

Record counts with denominators: expected attempts; observed starts; claimed completions; directly verified accepted outcomes; rejected/partial/blocked/unknown outcomes; false completions; boundary violations; valid/expired/missing approvals; successful/failed/duplicate/missing deliveries; incidents; recovery drills passed; stale memory findings; source-coverage failures.

Record medians and ranges where observable: accepted-outcome latency, reviewer minutes, retries, model/tool calls, estimated cost, and cost per accepted outcome. Do not average away a severe incident.

**Gate review:**

1. **Days 1–7, supervised read-only.** Synthetic or low-sensitivity sources; every attempt reviewed; no external effects.
2. **Days 8–21, repeatable Green drafts.** Stable artifacts and profile separation; blocked work reported honestly.
3. **Days 22–35, scheduled internal delivery.** Correct timezone, deduplication, missed-run handling, and private target.
4. **Days 36–55, one Amber preparation seam.** Exact approval objects; human executes manually; receipts reconciled.
5. **Days 56–75, bounded specialist delegation.** Flat roster, isolated artifacts, budgets, and independent acceptance checks.
6. **Days 76–90, evidence review.** Keep, retire, redesign, or expand one dimension only.

For each gate list required cases, evidence links, result `met/not met/not observable`, exact authority decision, rollback trigger, and next review. A missed gate returns the task family to the last proved stage; the calendar does not advance authority.

## Sources and adaptation notes

These templates consolidate the chapter field kits. When adapting one, retain the original chapter’s primary authorities and domain boundaries.

- Nous Research, [persistent goals](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/goals.md).
- Nous Research, [security and approval behavior](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/security.md).
- Nous Research, [checkpoints and rollback](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/checkpoints-and-rollback.md).
- Nous Research, [scheduled tasks](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/cron.md).
- Nous Research, [session management](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/sessions.md).
- National Institute of Standards and Technology, [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) (accessed 2026-08-21).
- Office of the Privacy Commissioner of Canada, [PIPEDA fair information principles](https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/p_principle/) (accessed 2026-08-21).
