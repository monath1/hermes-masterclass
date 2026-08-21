# Appendix D: Troubleshooting, glossary, bibliography, and provenance

**Verified against Hermes Agent v0.20.5 (2026-08-19).** Troubleshooting commands, configuration keys, interface labels, defaults, and source locations are version-sensitive. Diagnose the installed release before applying this appendix to a newer one.

## Safe recovery order

When something feels wrong, do not begin with a blind retry, update, reset, import, checkpoint clear, or credential paste. A disappearing error is not the same as a reconciled incident. Use this order:

1. **Stop the active effect.** Interrupt the current turn with `/stop` where available. Pause the specific cron job, heartbeat, loop, or platform. Stop the affected gateway if messages may continue. Disconnect network access only when the risk justifies it.
2. **Preserve evidence.** Record time, timezone, profile, session/job ID, model/provider, requested outcome, exact error, log paths, artifact revisions, approval ID, and provider receipts. Avoid debug uploads until the bundle is reviewed locally.
3. **Protect identities.** If compromise is plausible, revoke the narrowest affected token/session at the provider, pause channel pairings, and stop consumers. Rotation is incomplete until the old credential is denied.
4. **Reconcile external state.** Query the authoritative remote system by stable ID. Classify the effect as none, once, duplicate, partial, or unknown. Never retry an unknown non-idempotent effect.
5. **Reduce variables.** Confirm active profile and workspace. Check `hermes --version`, `hermes status`, `hermes doctor`, configuration paths, gateway state, and recent logs. A safe-mode read-only reproduction can distinguish core behavior from custom rules, plugins, hooks, and MCP.
6. **Repair the smallest layer.** Fix one credential, dependency, configuration entry, source, schedule, or artifact. Restore a backup only when its scope and timestamp match the failed layer. Filesystem rollback does not undo remote effects.
7. **Prove re-entry.** Run synthetic allowed, denied, wrong-profile, stale-source, duplicate, offline, and delivery-disabled cases as relevant. Keep authority at the last proved stage.
8. **Resume deliberately.** A named human re-enables one component, observes the first live run, updates the incident record, and schedules a follow-up sample.

If there is risk to money, legal rights, health, employment, privacy, a child, or another person’s account, contain first and involve the appropriate human or qualified professional. This book is an operating guide, not incident-response, legal, medical, tax, financial, or employment advice.

## Symptom-to-cause troubleshooting

| Symptom | Likely causes to test | Safe checks | Recovery and stop rule |
| --- | --- | --- | --- |
| `hermes` is not found | Shell did not reload; per-user install directory absent from `PATH`; wrong macOS account | Open a new Terminal; inspect the dedicated user’s shell configuration and install ledger | Repair only the dedicated user’s path. Do not reinstall with `sudo` over an existing per-user install. |
| Version differs from the book | Another checkout/profile wrapper; update changed baseline; old gateway still runs previous code | `hermes --version`; `hermes update --plan`; `hermes gateway list`; update receipt | Keep this edition pinned or update all affected claims and assets together. Do not mix command references across releases. |
| `doctor` reports stale config | New or removed keys; manual edit; partial migration | `hermes config path`; `hermes config check`; review diff and backup | Use interactive migration after backup. Preserve local intent; do not accept broad defaults without review. |
| Provider authentication fails | Expired/revoked key; wrong profile; pool cooldown; OAuth state; process not restarted | `hermes auth status <provider>`; active profile; provider console; local redacted logs | Rotate through the secret source, restart consumers, prove new access and old denial. Never paste the value into chat or an issue. |
| Model is unavailable | Retired/renamed model; wrong provider; aggregator routing; invalid custom endpoint | Exit chat and run `hermes model`; inspect exact provider/model; test a low-risk prompt | Select a supported exact identifier. Confirm data and cost policy before fallback; block if no equivalent route is approved. |
| Only one provider appears in `/model` | Only that provider is configured; `/model` cannot add providers | Run `hermes model` in Terminal outside chat | Complete provider setup, then start a fresh session. Treat model switch as a route and cache change. |
| Response is slow or expensive | Oversized context, skills index, tool schemas, repeated retries, slow route | `hermes prompt-size`; `/context all`; `/usage`; session and tool logs | Disable unused toolsets/skills, compress or start a scoped session, and cap turns. Do not remove evidence needed for an active consequential task. |
| Session seems to forget or mix work | Wrong profile/workspace; context compression; stale memory; gateway routing repair needed | `/profile`; session title/ID; `hermes sessions list`; inspect memory and context files | Stop external work, correct the authoritative store, open a fresh test session, and run cross-profile canaries. Do not “fix” it by adding sensitive facts to memory. |
| Gateway is not responding | Service stopped; adapter breaker; missing dependency; invalid token; unknown sender not allowed | `hermes gateway status`; `hermes gateway list`; `hermes logs gateway --since 1h`; pairing list | Fix one adapter or credential, test with an allowlisted secondary identity, then observe. Do not broaden allowlists to diagnose. |
| An allowed user gets no reply | Pairing pending; group/chat restriction; mention requirement; ordinary-user command restriction | `hermes pairing list`; platform configuration; `/whoami`; gateway logs | Approve the exact platform ID or correct the narrow rule. Never switch to unrestricted mode as a shortcut. |
| Messages may have delivered twice | Gateway restart, provider retry, missed acknowledgement, catch-up policy, duplicate cron attempt | Provider conversation/receipt; cron history; stable message/action ID | Reconcile at the platform. Send no replacement until state is known; correct duplicates manually under owner control. |
| Cron job did not fire | Paused/inactive job; wrong schedule/timezone; gateway/ticker stopped; host asleep | `hermes cron list`; `hermes cron status`; next run and host clock; gateway status | Correct schedule or service, then run one controlled test. Do not replay every missed external effect. |
| Cron ran but nothing arrived | Wrong delivery target; `[SILENT]`; platform permission; wrapper/truncation failure | Job output/history, provider logs, configured home target, platform send test | Repair delivery separately from job logic and deduplicate before redelivery. A successful run is not proof of delivery. |
| Job loads the wrong skill | Folder/name mismatch, missing install, multi-skill order, fresh-session prompt lacks context | `hermes skills list`; inspect job’s attached skills and self-contained prompt | Attach exact reviewed skills and rerun synthetically. Cron starts fresh; never rely on the current chat’s unstated context. |
| MCP server will not connect | Runtime missing; OAuth incomplete; wrong URL/command; environment absent; server down | `hermes mcp list`; `hermes mcp test <name>`; local server test; logs | Repair auth/runtime, keep server disabled until it passes, then select tools. Do not expose the whole server to see whether one tool works. |
| MCP tools are missing | Include filter; server advertised fewer capabilities; reload needed; probe failed | `hermes mcp configure <name>`; `/reload-mcp`; server docs | Enable only the required current tool. Missing tools can be a desired policy result, not a defect. |
| Plugin behavior is unexpected | Wrong plugin enabled; capability grant; dependency drift; lifecycle hook sees more data than expected | `hermes plugins list`; `doctor`; pinned manifest/source; local logs | Disable the plugin, restart, reproduce with synthetic data, and review retained provider/local data. Remove and remotely revoke if retired. |
| Skill output is unsafe or stale | Skill changed upstream or locally; procedure assumes broader authority; dependency changed | `hermes skills inspect`; `check`; `audit`; diff installed copy | Pin/restore only after review, or retire the skill. Skill text never overrides the Job Charter or enforced boundary. |
| File change must be undone | Wrong local write; checkpoint enabled and retained; human edits after checkpoint | `/diff`; `/rollback`; `/rollback diff <N>`; version-control status | Preview and restore the smallest file/change. Preserve human edits. Separately reconcile any remote effects. |
| Backup import is considered | Corrupt/missing state; wrong profile; update regression | Verify archive custody, timestamp, scope, checksum, and isolated restore result | Stop gateway before `hermes import`. Restore to an isolated target first; import overwrites active Hermes-home files. |
| Dashboard cannot be reached | Server absent; port conflict; wrong bind; missing web extra | `hermes dashboard --status`; loopback URL; desktop/backend logs | Keep loopback binding, repair local dependency/port, and tunnel when remote access is required. Never expose unauthenticated public access. |
| Claimed completion is wrong | Acceptance check tested activity, not outcome; source truncated; worker summary trusted | Inspect artifact, raw tool result, system of record, receipt, and denominator | Mark rejected/partial/unknown, repair the acceptance test, and sample similar attempts. Do not reward fluent handback as evidence. |

When the table offers several causes, test the least invasive discriminating check first. Change one variable, keep a timeline, and retain the failure state long enough to learn from it.

## Glossary

**Acceptance evidence.** Direct observation that proves the requested artifact or state meets its criteria; a worker’s completion statement is not evidence.

**Action ID.** Stable identifier binding one preview, approval, execution attempt, receipt, and reconciliation record.

**Agent.** A model operating inside a harness that can observe, choose tools, change state, and continue across steps.

**Amber.** Work Hermes may prepare but may not execute until a named human approves the exact current effect.

**Approval object.** Versioned record of target, identity, content, limits, expiry, evidence, and human decision for one Amber action.

**Authority.** Permission to produce a class of effect in a defined context; capability or tool access is not authority.

**Bot Mode.** Hermes facility for persistent named agent profiles with their own sessions and operating context.

**Checkpoint.** Opt-in local filesystem snapshot created before defined mutations; it does not reverse external effects.

**Commit point.** Moment an operation becomes externally effective or no longer safely reversible without compensation.

**Context.** Information assembled for the current model call, including conversation, rules, skills, memory, tool schemas, and workspace files.

**Cron job.** Scheduled prompt that runs in a fresh session and may have explicit delivery and attached skills.

**Data exposure.** People, services, providers, processes, logs, and storage locations that can receive or retain task content.

**Definition of done.** Observable outcome, artifact, and verification conditions required for completion.

**Egress.** Outbound network destinations and data flows reachable by the process or its tools.

**External effect.** Change outside the local draft workspace, such as a sent message, submitted form, purchase, booking, or remote record mutation.

**Fallback.** Alternate provider/model tried after eligible primary-route errors; it requires equivalent data authorization.

**Green.** Reversible internal work Hermes may perform inside explicitly assigned resources.

**Harness.** Runtime around the model that assembles context, exposes tools, persists state, enforces some controls, and manages the loop.

**Heartbeat.** Recurring prompt that re-enters an idle session on an interval.

**Idempotency key.** Stable request identifier intended to prevent or detect duplicate processing.

**Job Charter.** Owner-approved operating contract defining purpose, customers, sources, authority, evidence, service levels, stop rules, records, and offboarding.

**MCP.** Model Context Protocol, an interoperability layer through which Hermes can connect to external tool servers.

**Memory.** Durable user or operational information injected into future sessions; it requires purpose, source, correction, retention, and separation rules.

**Profile.** Isolated Hermes instance with its own home, configuration, sessions, skills, and related state; profiles under one macOS user can still share OS-level access.

**Provenance.** Evidence of where an artifact, claim, skill, plugin, MCP manifest, or screenshot came from and which version it represents.

**Red.** Action Hermes may not perform autonomously, including money movement, professional decisions, credentials, impersonation, surveillance, and unbounded destructive work.

**Reconciliation.** Direct query of the authoritative external system to establish whether an effect occurred none, once, more than once, partially, or remains unknown.

**Recovery point objective (RPO).** Maximum tolerable data gap after recovery; an owner-selected target, not proof a backup meets it.

**Recovery time objective (RTO).** Target duration for restoring service; measured drills establish actual capability.

**Session.** Persisted conversation and tool trajectory associated with a profile, source, workspace, and routing identity.

**Skill.** Procedural instruction package Hermes can load to guide a task; it may reference scripts, assets, and dependencies.

**System of record.** Authoritative service or artifact used to reconcile current state.

**Tool.** Callable operation exposed to the agent, such as reading a file, searching the web, scheduling a job, or invoking an MCP function.

**Trajectory.** Sequence of model decisions, tool calls, observations, state changes, and handbacks in an attempt.

**Trust envelope.** Combined boundary of macOS identity, filesystem, browser/accounts, credentials, network, tools, profiles, approvals, audit, and recovery.

**Uncertain effect.** External operation whose success or failure cannot be directly established; it must not be blindly retried.

**Watermark.** Persisted source cursor, timestamp, or stable ID marking what a recurring workflow has processed.

## Consolidated bibliography

### Hermes Agent

- Nous Research, [Hermes Agent repository README](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/README.md), [Security Policy](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/SECURITY.md), and [architecture](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/developer-guide/architecture.md).
- Nous Research, [CLI commands](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/cli-commands.md), [slash commands](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/slash-commands.md), [tools](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/tools-reference.md), and [profiles](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/profiles.md).
- Nous Research, [models](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/configuring-models.md), [provider routing](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/provider-routing.md), and [fallback providers](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/fallback-providers.md).
- Nous Research, [sessions](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/sessions.md), [memory](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/memory.md), [goals](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/goals.md), [cron](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/cron.md), and [checkpoints](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/checkpoints-and-rollback.md).
- Nous Research, [skills](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/skills.md), [plugins](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/plugins.md), [MCP](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/mcp.md), and [toolsets](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/toolsets-reference.md).
- Nous Research, [messaging gateway](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/messaging/index.md), [secrets](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/secrets/index.md), [updating](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/getting-started/updating.md), and [FAQ](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/faq.md).

### Platform, protocol, and provider sources

- Apple, [Apple Platform Security](https://support.apple.com/guide/security/welcome/web), [FileVault](https://support.apple.com/en-ca/guide/mac-help/flvlt003/mac), [Firewall](https://support.apple.com/en-ca/guide/mac-help/mh11783/mac), and [Time Machine](https://support.apple.com/guide/mac-help/back-up-files-mh35860/mac) (accessed 2026-08-21).
- OpenAI, [`gpt-5.6-sol`](https://developers.openai.com/api/docs/models/gpt-5.6-sol), [API pricing](https://platform.openai.com/pricing), and [Codex documentation](https://developers.openai.com/codex/) (accessed 2026-08-21).
- Model Context Protocol, [specification 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18) (accessed 2026-08-21).
- Meta, [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api/); Telegram, [Bot API](https://core.telegram.org/bots/api); Twilio, [Canada SMS pricing](https://www.twilio.com/en-us/sms/pricing/ca) (accessed 2026-08-21).
- 1Password, [service accounts](https://developer.1password.com/docs/service-accounts/); Bitwarden, [machine accounts](https://bitwarden.com/help/machine-accounts/) (accessed 2026-08-21).

### Canadian and risk authorities

- Office of the Privacy Commissioner of Canada, [PIPEDA fair information principles](https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/p_principle/) and [privacy-breach containment](https://www.priv.gc.ca/en/privacy-topics/business-privacy/breaches-and-safeguards/privacy-breaches-at-your-business/contain_pb/) (accessed 2026-08-21).
- Government of Canada Job Bank, [job search](https://www.jobbank.gc.ca/jobsearch/) and [terms for job seekers](https://www.jobbank.gc.ca/termsofuse-seeker.xhtml) (accessed 2026-08-21).
- Canada Revenue Agency, [individual record retention](https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/long-should-you-keep-your-income-tax-records.html) and [business records](https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/keeping-records.html) (accessed 2026-08-21).
- Health Canada, [Canada’s Food Guide](https://food-guide.canada.ca/en/); Financial Consumer Agency of Canada, [making a budget](https://www.canada.ca/en/financial-consumer-agency/services/make-budget.html); Global Affairs Canada, [travel advisories](https://travel.gc.ca/travelling/advisories) (accessed 2026-08-21).
- National Institute of Standards and Technology, [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) and [Digital Identity Guidelines](https://pages.nist.gov/800-63-4/) (accessed 2026-08-21).
- Payment Card Industry Security Standards Council, [PCI DSS standards](https://www.pcisecuritystandards.org/standards/pci-dss/) (accessed 2026-08-21); Competition Bureau Canada, [deceptive marketing practices](https://competition-bureau.canada.ca/deceptive-marketing-practices) (accessed 2026-08-21).

## Source and version ledger

| Source, title, publisher | Verified | Affected chapters/appendices | Version-sensitive? |
| --- | --- | --- | --- |
| [Hermes Agent tag `v2026.8.19`](https://github.com/NousResearch/hermes-agent/tree/v2026.8.19), Nous Research | 2026-08-21; commit `fcbd1076a93841fa88855acce810e342a5b78101` | 1–22, A–D | Yes: entire product baseline |
| [Hermes CLI commands](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/cli-commands.md), Nous Research | 2026-08-21 | 5, 7–10, 12–14, 22, A, D | Yes: names, flags, defaults |
| [Hermes skills catalog](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/skills-catalog.md), Nous Research | 2026-08-21 | 8, 15–21, C | Yes: entries and behavior |
| [Hermes built-in plugins](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/built-in-plugins.md), Nous Research | 2026-08-21 | 8, 22, C | Yes: inventory and hooks |
| [Hermes MCP](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/mcp.md), Nous Research | 2026-08-21 | 8, 16, 19–20, C | Yes: protocol support, filters, catalog |
| [Hermes Security Policy](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/SECURITY.md), Nous Research | 2026-08-21 | 1–4, 8–14, 19–22, B–D | Yes: trust and scope statements |
| [Apple Platform Security](https://support.apple.com/guide/security/welcome/web), Apple | 2026-08-21 | 5, 11, 14 | Yes: macOS controls evolve |
| [`gpt-5.6-sol`](https://developers.openai.com/api/docs/models/gpt-5.6-sol), OpenAI | 2026-08-21 | 6, 10, 21, D | Yes: model, service behavior, pricing elsewhere |
| [PIPEDA fair information principles](https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/p_principle/), Office of the Privacy Commissioner of Canada | 2026-08-21 | 7, 12–14, 18, 20, B, D | Yes: law/guidance may change |
| [Canada Revenue Agency](https://www.canada.ca/en/revenue-agency.html), Government of Canada | 2026-08-21 | 18–20, B, D | Yes: tax-year rules and dates |
| [Government of Canada Job Bank](https://www.jobbank.gc.ca/), Government of Canada | 2026-08-21 | 16–17, D | Yes: postings, terms, labour information |
| [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), NIST | 2026-08-21 | 2, 13, 22, B, D | Lower drift, but verify current publication |

The chapter reference sections remain the granular ledger for individual claims. This table identifies load-bearing families and update scope; it does not replace those citations.

## Screenshot provenance

The canonical screenshot ledger is [the local image provenance document](../assets/images/PROVENANCE.md), backed by `docs/assets/images/provenance.yml`. It records local filename, exact upstream path, tag, MIT license, chapter use, and alt text. All official Hermes images in this edition were copied locally from the pinned repository; there are no external screenshot hotlinks.

When replacing an image, verify the checkout tag and commit, copy from the official source path without adding private overlays, update both provenance files, update every chapter caption and reference, confirm the file is registered exactly once, and inspect light/dark/mobile/print rendering. A screenshot is version evidence, not decoration; an interface change that makes it stale requires an explicit edition decision.

## Release update checklist

- [ ] Identify the candidate Hermes tag and immutable commit; read release notes and security changes before editing prose.
- [ ] Diff pinned versus candidate documentation for CLI, slash commands, tools, profiles, models, providers, sessions, memory, cron, checkpoints, secrets, skills, plugins, MCP, messaging, security, update, and recovery.
- [ ] Run old commands with read-only help/status surfaces first. Record removed, renamed, changed-default, newly destructive, and newly networked behavior.
- [ ] Review trust-model and approval changes before feature changes. Re-test OS boundary, dedicated account, profile canaries, path denial, egress denial, unknown sender, and external-effect reconciliation.
- [ ] Rebuild the skill/plugin/MCP inventory from official candidate sources. Do not carry names forward because they existed in this edition; re-rate permission, exposure, setup, cost, maintenance, and phase.
- [ ] Verify provider/model identifiers, prices, limits, OAuth behavior, message-platform rules, laws, Canadian amounts/dates, and primary-source observation dates.
- [ ] Update product baseline, exact verification label, source map, Appendix A commands, Appendix C matrix, Appendix D ledger, README, About, manifest, and contributor procedure together.
- [ ] Replace only screenshots whose interface evidence changed. Update local files, captions, alt text, Markdown provenance, YAML provenance, and chapter usage in one change.
- [ ] Re-run every chapter-specific source audit against the new Hermes checkout and any separate live checks required for external government/provider pages.
- [ ] Measure every chapter and appendix with the repository checker. Preserve exactly 22 numbered chapters and four appendices and the 100,000–120,000-word release contract.
- [ ] Run tests, final manuscript validation, strict MkDocs build, spelling, Markdown/link checks, Python compilation, `git diff --check`, and a secret/private-data scan.
- [ ] Render and inspect navigation, search, tables, code labels, Mermaid, screenshots, mobile width, dark mode, and print output.
- [ ] Record corrections and deliberate pinned exceptions in the editorial audit. Do not silently mix old and new baseline behavior.
- [ ] Trial update/rollback on an isolated profile with synthetic sources, stopped external delivery, a verified backup, and a named approver before updating the live Mac mini.
- [ ] Publish through the private repository workflow, inspect checks, retain prior-edition tags/artifacts, and schedule the next source-drift review.
