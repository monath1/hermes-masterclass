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

The machine-readable ledger below is the consolidated bibliography for the release manuscript. Its scope is exact: every distinct HTTP or HTTPS destination in a Markdown citation in Chapters 1–22 or Appendices A–D is included once. Local relative links, image paths, anchor links, plain-text examples, build configuration, and the URLs inside the ledger itself are excluded. Excluding the ledger carrier prevents its rows from citing themselves. A URL linked elsewhere in Appendix D remains in scope. For example, the pinned [Hermes FAQ](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/faq.md) is a normal external citation and therefore has a row whose affected field includes D.

“Affected” means that the chapter or appendix contains that exact URL outside the ledger. It does not speculate about every chapter that could benefit from a source, and it does not collapse different pages from one publisher into a family. Numeric labels identify chapters; letters identify appendices. Multiple occurrences in one manuscript unit still produce one label. The audit sorts chapters numerically before appendices, so a mapping such as `6, 14, A` is stable and reviewable. If a link is moved, added, replaced, or removed, the ledger must change in the same commit.

Each row supplies six explicit fields: URL, human-readable title, publisher, verification date, affected manuscript units, and version-sensitive status. `Yes—pinned` means the destination is tied to an immutable tag, commit, dated specification, or versioned artifact used by this edition. `Yes—mutable` means the publisher can change the page without this repository changing; re-open it during an edition update and record a new verification date. `No—stable` is reserved for unusually durable material, but still requires link and applicability review. The label describes drift risk, not authority or correctness.

The title and publisher help a reviewer recognize substitutions, redirects, mirrors, and misleading domains. The verification date records the editorial observation date, not a claim that the page will remain available. Government, legal, pricing, model, product, OAuth, platform, and provider documentation is treated as mutable unless a versioned artifact makes the cited content immutable. Hermes repository pages are pinned to `v2026.8.19`; their contents were also checked against commit `fcbd1076a93841fa88855acce810e342a5b78101`. External MCP examples remain third-party sources even when a matching manifest appears in the pinned Nous-approved catalog.

Treat a redirect as a source change: confirm ownership, destination, scope, and retained version evidence before accepting it.

Use the ledger with the nearby claim, not instead of it. Start from a chapter reference, inspect the source’s publisher and version status here, then verify the claim against the cited page. A source may support several claims without validating the surrounding recommendation. When a page disappears, do not silently substitute a search result or archive: identify the current primary source, reassess the claim, update every affected unit, and preserve the edition’s pinned evidence where reproducibility matters.

The repository audit reconstructs the URL set and affected mappings directly from the manuscript, parses every CSV row, rejects duplicates and orphan rows, and requires all fields. This catches omissions and incorrect mappings but cannot decide whether a title is editorially precise, a publisher remains authoritative, a live page changed meaning, or a source is sufficient for a claim. Those remain source-review duties. During a release, run the audit after editing references, then sample high-risk mutable sources and every changed row manually.

## Source and version ledger

The CSV is intentionally copyable and excluded from the prose word count. Every row remains visible in the appendix and every field is explicit; no publisher family, URL prefix, range, or source bundle stands in for an individual citation.

```csv
url,title,publisher,verified,affected,version_sensitive
"https://antifraudcentre-centreantifraude.ca/scams-fraudes/job-emploi-eng.htm","Job fraud","Canadian Anti-Fraud Centre","2026-08-21","16","Yes—mutable"
"https://bitwarden.com/help/machine-accounts/","Machine accounts","Bitwarden","2026-08-21","12","Yes—mutable"
"https://bitwarden.com/help/setup-two-step-login/","Two-step login methods","Bitwarden","2026-08-21","12","Yes—mutable"
"https://bitwarden.com/help/two-step-recovery-code/","Two-step login recovery code","Bitwarden","2026-08-21","12","Yes—mutable"
"https://competition-bureau.canada.ca/deceptive-marketing-practices","Deceptive marketing practices","Competition Bureau Canada","2026-08-21","20","Yes—mutable"
"https://core.telegram.org/bots/api","Bot API","Telegram","2026-08-21","9","Yes—mutable"
"https://core.telegram.org/bots/faq","Bots FAQ and broadcast limits","Telegram","2026-08-21","9","Yes—mutable"
"https://developer.1password.com/docs/service-accounts/","Use service accounts","1Password","2026-08-21","12","Yes—mutable"
"https://developer.apple.com/documentation/xcode/installing-the-command-line-tools/","Install the Command Line Tools for Xcode","Apple","2026-08-21","5","Yes—mutable"
"https://developers.asana.com/docs/using-asanas-mcp-server","Asana MCP","Asana","2026-08-21","C","Yes—mutable"
"https://developers.facebook.com/docs/whatsapp/cloud-api/","WhatsApp Cloud API","Meta","2026-08-21","12","Yes—mutable"
"https://developers.intercom.com/docs/guides/mcp","Intercom MCP","Intercom","2026-08-21","C","Yes—mutable"
"https://developers.notion.com/docs/mcp","Notion MCP","Notion","2026-08-21","C","Yes—mutable"
"https://developers.openai.com/api/docs/guides/latest-model","Latest-model guidance for gpt-5.6-sol","OpenAI","2026-08-21","6","Yes—mutable"
"https://developers.openai.com/api/docs/guides/webhooks","Webhooks","OpenAI","2026-08-21","22","Yes—mutable"
"https://developers.openai.com/api/docs/models/gpt-5.6-sol","gpt-5.6-sol model","OpenAI","2026-08-21","6, 10","Yes—mutable"
"https://developers.openai.com/api/reference/resources/webhooks","Webhook events","OpenAI","2026-08-21","22","Yes—mutable"
"https://docs.stripe.com/mcp","Stripe MCP","Stripe","2026-08-21","C","Yes—mutable"
"https://food-guide.canada.ca/en/","Canada's Food Guide","Health Canada","2026-08-21","18","Yes—mutable"
"https://github.com/CyberSamuraiX/hermes-n8n-mcp","n8n bridge","CyberSamuraiX","2026-08-21","C","Yes—mutable"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/README.md","Hermes Agent README at tag v2026.8.19","Nous Research","2026-08-21","1","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/SECURITY.md","Hermes Agent Security Policy","Nous Research","2026-08-21","11, 13, 14","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/developer-guide/agent-loop.md","Agent loop internals","Nous Research","2026-08-21","1, 2, 3, 4","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/developer-guide/architecture.md","Architecture","Nous Research","2026-08-21","1, 2, 3","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/developer-guide/cron-internals.md","Cron internals","Nous Research","2026-08-21","10","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/developer-guide/prompt-assembly.md","Prompt assembly","Nous Research","2026-08-21","1, 2, 3, 4","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/developer-guide/session-storage.md","Session storage","Nous Research","2026-08-21","1, 2, 3","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/developer-guide/subagent-lifecycle-api.md","Public subagent lifecycle API","Nous Research","2026-08-21","21","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/developer-guide/trajectory-format.md","Trajectory format","Nous Research","2026-08-21","1, 2, 3, 13, 22","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/getting-started/installation.md","Installation","Nous Research","2026-08-21","5","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/getting-started/learning-path.md","Hermes Agent learning path","Nous Research","2026-08-21","1","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/getting-started/quickstart.md","Quickstart","Nous Research","2026-08-21","5","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/getting-started/updating.md","Updating and uninstalling","Nous Research","2026-08-21","5, 14, A","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/guides/automation-blueprints.md","Automation blueprints","Nous Research","2026-08-21","10","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/guides/cron-troubleshooting.md","Cron troubleshooting","Nous Research","2026-08-21","10, 22","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/guides/daily-briefing-bot.md","Daily briefing bot","Nous Research","2026-08-21","10, 15","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/guides/delegation-patterns.md","Delegation and parallel-work patterns","Nous Research","2026-08-21","21","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/guides/local-llm-on-mac.md","Run local LLMs on Mac","Nous Research","2026-08-21","5, 6","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/guides/local-ollama-setup.md","Run Hermes locally with Ollama","Nous Research","2026-08-21","6","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/guides/run-hermes-with-nous-portal.md","Run Hermes with Nous Portal","Nous Research","2026-08-21","6","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/guides/troubleshooting-agent-quality.md","Troubleshooting agent quality","Nous Research","2026-08-21","22","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/integrations/providers.md","AI providers","Nous Research","2026-08-21","6, 10","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/cli-commands.md","CLI commands","Nous Research","2026-08-21","6, 14, A","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/faq.md","Hermes FAQ","Nous Research","2026-08-21","D","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/model-catalog.md","Model catalog","Nous Research","2026-08-21","6","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/optional-skills-catalog.md","Official optional skills catalog","Nous Research","2026-08-21","8, C","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/profile-commands.md","profile commands reference at tag v2026.8.19","Nous Research","2026-08-21","A","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/skills-catalog.md","Bundled skills catalog","Nous Research","2026-08-21","8, C","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/slash-commands.md","slash commands reference at tag v2026.8.19","Nous Research","2026-08-21","A","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/tools-reference.md","built-in tools reference at tag v2026.8.19","Nous Research","2026-08-21","A","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/toolsets-reference.md","Toolsets reference","Nous Research","2026-08-21","8, 21","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/bot-mode.md","Bot Mode","Nous Research","2026-08-21","7, 19, 21","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/checkpoints-and-rollback.md","Checkpoints and rollback","Nous Research","2026-08-21","10, 13, 14, 22, A, B","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/cli.md","CLI","Nous Research","2026-08-21","5","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/configuring-models.md","Configuring models","Nous Research","2026-08-21","6","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/desktop.md","Desktop app","Nous Research","2026-08-21","5","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/docker.md","Docker guide","Nous Research","2026-08-21","11","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/egress/index.md","Egress proxy overview","Nous Research","2026-08-21","11, 13","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/egress/iron-proxy.md","Iron Proxy integration","Nous Research","2026-08-21","11, 13","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/browser.md","Browser automation","Nous Research","2026-08-21","15, 16, 20","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/built-in-plugins.md","Built-in plugins","Nous Research","2026-08-21","8, C","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/codex-app-server-runtime.md","Codex app-server runtime","Nous Research","2026-08-21","21","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/context-files.md","Context files","Nous Research","2026-08-21","7","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/credential-pools.md","Credential pools","Nous Research","2026-08-21","12","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/cron.md","Scheduled tasks","Nous Research","2026-08-21","10, 13, 14, 15, 16, 18, 19, 22, B","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/delegation.md","Subagent delegation","Nous Research","2026-08-21","4, 21, 22","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/deliverable-mode.md","Deliverable Mode","Nous Research","2026-08-21","19, 20","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/document-extraction.md","Document extraction","Nous Research","2026-08-21","16, 17, 18, 20","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/fallback-providers.md","Fallback providers","Nous Research","2026-08-21","6, 21, 22","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/goals.md","Persistent goals","Nous Research","2026-08-21","2, 3, 4, 10, 19, 22, B","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/heartbeat.md","Session heartbeats","Nous Research","2026-08-21","10","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/hooks.md","Event hooks","Nous Research","2026-08-21","10, 13, 19","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/kanban.md","Kanban multi-agent board","Nous Research","2026-08-21","19, 20","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/loops.md","Recurring loops","Nous Research","2026-08-21","10","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/mcp.md","MCP client and server support","Nous Research","2026-08-21","8, 16, C","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/memory-providers.md","Memory providers","Nous Research","2026-08-21","7","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/memory.md","Persistent memory","Nous Research","2026-08-21","7, 18","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/mixture-of-agents.md","Mixture of Agents","Nous Research","2026-08-21","21","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/overview.md","Features overview","Nous Research","2026-08-21","1","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/personality.md","Personality and SOUL.md","Nous Research","2026-08-21","4, 7","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/plugins.md","Plugins","Nous Research","2026-08-21","8, C","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/provider-routing.md","Provider routing","Nous Research","2026-08-21","6, 21","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/skills.md","Skills system and Skills Hub","Nous Research","2026-08-21","8, 16, 19, C","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/tools.md","Tools and toolsets","Nous Research","2026-08-21","8, 16, 18, 20","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/voice-mode.md","Voice mode","Nous Research","2026-08-21","9, 17","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/web-dashboard.md","Web dashboard","Nous Research","2026-08-21","5","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/web-search.md","Web search and extraction","Nous Research","2026-08-21","15, 16, 17, 18, 20","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/managed-scope.md","Managed scope","Nous Research","2026-08-21","11, 13","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/messaging/email.md","Email setup","Nous Research","2026-08-21","9, 15, 18, 20","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/messaging/index.md","Messaging gateway","Nous Research","2026-08-21","9, 10","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/messaging/sms.md","SMS through Twilio","Nous Research","2026-08-21","9","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/messaging/telegram.md","Telegram setup","Nous Research","2026-08-21","9","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/messaging/whatsapp-cloud.md","WhatsApp Business Cloud API setup","Nous Research","2026-08-21","9, 12","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/messaging/whatsapp.md","WhatsApp Baileys bridge","Nous Research","2026-08-21","9","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/multi-profile-gateways.md","macOS gateway LaunchAgent","Nous Research","2026-08-21","5, 12","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/profile-distributions.md","Profile exports and distributions","Nous Research","2026-08-21","14","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/profiles.md","Profiles","Nous Research","2026-08-21","5, 7, 10, 15, 16, 19","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/secrets/bitwarden.md","Bitwarden Secrets Manager provider","Nous Research","2026-08-21","12","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/secrets/command.md","Command-helper secret provider","Nous Research","2026-08-21","12","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/secrets/index.md","Secrets overview","Nous Research","2026-08-21","12, 14","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/secrets/onepassword.md","1Password secret provider","Nous Research","2026-08-21","12","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/security.md","Security","Nous Research","2026-08-21","1, 3, 4, 8, 9, 11, 12, 13, 15, B","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/sessions.md","Sessions","Nous Research","2026-08-21","7, 13, 14, 22, B","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex.md","Bundled Codex skill","Nous Research","2026-08-21","21","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/skills/bundled/productivity/productivity-docx.md","DOCX bundled skill","Nous Research","2026-08-21","17","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/skills/bundled/productivity/productivity-google-workspace.md","Google Workspace bundled skill","Nous Research","2026-08-21","15, 20","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/skills/bundled/productivity/productivity-meeting-action-items.md","Meeting action items bundled skill","Nous Research","2026-08-21","15, 19","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/skills/bundled/productivity/productivity-pdf.md","PDF bundled skill","Nous Research","2026-08-21","17","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/skills/bundled/productivity/productivity-weekly-review-planning.md","Weekly review and planning bundled skill","Nous Research","2026-08-21","15","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/skills/bundled/productivity/productivity-xlsx.md","XLSX bundled skill","Nous Research","2026-08-21","15, 16, 18","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/skills/bundled/research/research-grounded-citations.md","Grounded citations bundled skill","Nous Research","2026-08-21","16, 17, 18, 20","Yes—pinned"
"https://github.com/NousResearch/hermes-agent/tree/v2026.8.19/optional-mcps","pinned optional MCP manifests","Nous Research","2026-08-21","C","Yes—pinned"
"https://help.twilio.com/articles/46871410243099-Understanding-SMS-Message-Fees-Carrier-Fees-and-Phone-Number-Fees","SMS, carrier, and phone-number fees","Twilio","2026-08-21","9","Yes—mutable"
"https://learn.chatgpt.com/docs/agent-configuration/subagents","Codex subagents","OpenAI","2026-08-21","21","Yes—mutable"
"https://learn.chatgpt.com/docs/app-server","Codex App Server","OpenAI","2026-08-21","21","Yes—mutable"
"https://learn.chatgpt.com/docs/build-skills","Build skills for ChatGPT and Codex","OpenAI","2026-08-21","21","Yes—mutable"
"https://learn.chatgpt.com/docs/sandboxing","Sandbox","OpenAI","2026-08-21","21","Yes—mutable"
"https://modelcontextprotocol.io/specification/2025-06-18","Specification","Model Context Protocol","2026-08-21","8, C","Yes—pinned"
"https://pages.nist.gov/800-63-4/","Digital Identity Guidelines","National Institute of Standards and Technology","2026-08-21","12","Yes—mutable"
"https://platform.openai.com/pricing","API pricing","OpenAI","2026-08-21","6","Yes—mutable"
"https://support.1password.com/recovery-codes/","Generate and use recovery codes","1Password","2026-08-21","12","Yes—mutable"
"https://support.1password.com/recovery/","Recover accounts for family or team members","1Password","2026-08-21","12","Yes—mutable"
"https://support.1password.com/secret-key/","Find your Secret Key or Setup Code","1Password","2026-08-21","12","Yes—mutable"
"https://support.airtable.com/docs/using-the-airtable-mcp-server","Airtable MCP","Airtable","2026-08-21","C","Yes—mutable"
"https://support.apple.com/en-ca/102316","Automatic login and FileVault","Apple","2026-08-21","5","Yes—mutable"
"https://support.apple.com/en-ca/guide/mac-help/flvlt003/mac","Set up your Mac to be secure","Apple","2026-08-21","5","Yes—mutable"
"https://support.apple.com/en-ca/guide/mac-help/mh11783/mac","Change Firewall settings on Mac","Apple","2026-08-21","5","Yes—mutable"
"https://support.apple.com/en-gb/guide/findmy-mac/fmmbe7bb71f4/mac","Erase a device in Find My on Mac","Apple","2026-08-21","14","Yes—mutable"
"https://support.apple.com/en-la/104978","Use Find My to locate or erase a lost Apple device","Apple","2026-08-21","14","Yes—mutable"
"https://support.apple.com/en-us/104984","Back up your Mac with Time Machine","Apple","2026-08-21","14","Yes—mutable"
"https://support.apple.com/guide/mac-help/add-a-user-or-group-mchl3e281fc9/mac","Add a user or group on Mac","Apple","2026-08-21","11","Yes—mutable"
"https://support.apple.com/guide/mac-help/back-up-files-mh35860/mac","Back up your files with Time Machine","Apple","2026-08-21","5","Yes—mutable"
"https://support.apple.com/guide/mac-help/set-up-your-mac-to-be-secure-flvlt003/mac","Set up your Mac to be secure","Apple","2026-08-21","11","Yes—mutable"
"https://support.apple.com/guide/mac-help/software-update-settings-on-mac-mchla7037245/mac","Software Update settings on Mac","Apple","2026-08-21","5","Yes—mutable"
"https://support.apple.com/guide/mac-help/verify-your-backup-disk-mh26840/mac","Verify your backup disk on Mac","Apple","2026-08-21","14","Yes—mutable"
"https://support.apple.com/guide/security/sec4c6dc1b6e/web","Volume encryption with FileVault in macOS","Apple","2026-08-21","14","Yes—mutable"
"https://support.apple.com/guide/security/welcome/web","Apple Platform Security","Apple","2026-08-21","11","Yes—mutable"
"https://support.google.com/accounts/answer/185833","Sign in with app passwords","Google","2026-08-21","9","Yes—mutable"
"https://travel.gc.ca/travelling/advisories","Travel Advice and Advisories","Global Affairs Canada","2026-08-21","18","Yes—mutable"
"https://travel.gc.ca/travelling/children/consent-letter","Recommended consent letter for children travelling abroad","Global Affairs Canada","2026-08-21","18","Yes—mutable"
"https://whatsappbusiness.com/developers/developer-hub/","Developer Hub","Meta","2026-08-21","9","Yes—mutable"
"https://whatsappbusiness.com/products/platform-pricing/","Business Platform pricing","Meta","2026-08-21","9","Yes—mutable"
"https://www.canada.ca/en/financial-consumer-agency/services/make-budget.html","Making a budget","Financial Consumer Agency of Canada","2026-08-21","18","Yes—mutable"
"https://www.canada.ca/en/public-health/services/being-active/physical-activity-your-health.html","Physical activity for your health","Public Health Agency of Canada","2026-08-21","18","Yes—mutable"
"https://www.canada.ca/en/revenue-agency/news/newsroom/tax-tips/tax-tips-2026/tax-slips-what-they-are-where-find-why-waiting-can-help-avoid-mistakes.html","Tax slips at tax time","Canada Revenue Agency","2026-08-21","18","Yes—mutable"
"https://www.canada.ca/en/revenue-agency/news/newsroom/tax-tips/tax-tips-2026/what-you-need-for-2026-tax-filing-season.html","What you need to know for the 2026 tax-filing season","Canada Revenue Agency","2026-08-21","18","Yes—mutable"
"https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/keeping-records.html","Business records","Canada Revenue Agency","2026-08-21","20","Yes—mutable"
"https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/long-should-you-keep-your-income-tax-records.html","How long should you keep your income tax records?","Canada Revenue Agency","2026-08-21","18","Yes—mutable"
"https://www.canada.ca/en/services/benefits/calendar.html","Benefits payment dates","Government of Canada","2026-08-21","18","Yes—mutable"
"https://www.canada.ca/en/services/benefits/finder.html","Benefits Finder","Government of Canada","2026-08-21","18","Yes—mutable"
"https://www.canada.ca/en/services/benefits/publicpensions/cpp/retirement-income-calculator.html","Canadian Retirement Income Calculator","Government of Canada","2026-08-21","18","Yes—mutable"
"https://www.cisa.gov/securebydesign","Secure by Design","Cybersecurity and Infrastructure Security Agency","2026-08-21","11","Yes—mutable"
"https://www.jobbank.gc.ca/jobsearch/","Job search","Government of Canada Job Bank","2026-08-21","16","Yes—mutable"
"https://www.jobbank.gc.ca/termsofuse-seeker.xhtml","Terms of Use for job seekers","Government of Canada Job Bank","2026-08-21","16","Yes—mutable"
"https://www.jobbank.gc.ca/trend-analysis/search-job-outlooks","Search job outlooks","Government of Canada Job Bank","2026-08-21","17","Yes—mutable"
"https://www.linkedin.com/help/linkedin/answer/a1341387/prohibited-software-and-extensions","Prohibited software and extensions","LinkedIn","2026-08-21","16","Yes—mutable"
"https://www.linkedin.com/legal/user-agreement","User Agreement","LinkedIn","2026-08-21","16","Yes—mutable"
"https://www.nist.gov/itl/ai-risk-management-framework","AI Risk Management Framework","National Institute of Standards and Technology","2026-08-21","2, 13, 22, B","Yes—mutable"
"https://www.ontario.ca/page/school-year-calendars","School year calendars","Government of Ontario","2026-08-21","18","Yes—mutable"
"https://www.ontario.ca/page/your-health","Your health and Health811","Government of Ontario","2026-08-21","18","Yes—mutable"
"https://www.pcisecuritystandards.org/faqs/1318/","What is the maximum period cardholder data may be stored?","PCI Security Standards Council","2026-08-21","14","Yes—mutable"
"https://www.pcisecuritystandards.org/faqs/are-merchants-allowed-to-request-card-verification-codes-values-from-cardholders/","Are merchants allowed to request card-verification codes/values?","PCI Security Standards Council","2026-08-21","14","Yes—mutable"
"https://www.pcisecuritystandards.org/faqs/does-pci-dss-apply-to-merchants-who-outsource-all-payment-processing-operations-and-never-store-process-or-transmit-cardholder-data/","Does PCI DSS apply when payment processing is outsourced?","PCI Security Standards Council","2026-08-21","14","Yes—mutable"
"https://www.priv.gc.ca/en/privacy-topics/business-privacy/breaches-and-safeguards/privacy-breaches-at-your-business/contain_pb/","Contain a privacy breach at your business","Office of the Privacy Commissioner of Canada","2026-08-21","14","Yes—mutable"
"https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/p_principle/","PIPEDA fair information principles","Office of the Privacy Commissioner of Canada","2026-08-21","7, 14, B","Yes—mutable"
"https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/p_principle/principles/p_use/","Limiting use, disclosure, and retention","Office of the Privacy Commissioner of Canada","2026-08-21","7","Yes—mutable"
"https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/r_o_p/prov-pipeda/","Provincial laws that may apply instead of PIPEDA","Office of the Privacy Commissioner of Canada","2026-08-21","14","Yes—mutable"
"https://www.twilio.com/en-us/sms/pricing/ca","SMS pricing in Canada","Twilio","2026-08-21","9","Yes—mutable"
```

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
