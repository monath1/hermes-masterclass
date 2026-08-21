# Appendix C: Curated Hermes extension stack

**Verified against Hermes Agent v0.20.5 (2026-08-19).** This appendix describes Hermes-native extension mechanisms and Hermes-compatible MCP servers. It does not list or recommend Codex marketplace plugins. The bundled `codex` skill is a Hermes skill for delegating bounded coding work to Codex; that is categorically different from installing an extension into Codex.

## How the ratings work

Install nothing merely because it appears here. Begin with a workflow failure that a simpler built-in tool cannot solve, then review the exact skill, plugin, or MCP artifact at the pinned release. Ratings describe a conservative family-and-microbusiness deployment, not universal product quality.

| Dimension | Scale |
| --- | --- |
| Value | **High** materially supports several book workflows; **Medium** is useful for a narrower case; **Conditional** depends on a specific service. |
| Permissions | **Low** is procedural or local read-heavy; **Medium** reads scoped work data or writes local artifacts; **High** can send, mutate remote state, run code, or observe broad traces. |
| Data exposure | **Local**, **Provider**, or **Broad provider** describes where task content may travel. It does not claim a legal privacy classification. |
| Setup | **Low** uses shipped material with few dependencies; **Medium** needs a CLI/account; **High** needs OAuth, service configuration, or infrastructure. |
| Recurring cost | **None**, **Service plan**, **Usage**, or **Self-hosting**. Prices are deliberately omitted because they drift; check the primary provider page on the installation date. |
| Maintenance | **Low** follows Hermes updates; **Medium** needs periodic auth/dependency review; **High** adds a server, SDK, or operational service. |
| Phase | **1** supervised local assistant; **2** repeatable Green work; **3** scheduled internal delivery; **4** Amber preparation; **5** bounded specialist/business integration; **6** evidence-led expansion. |

“Bundled” means the skill or plugin ships in the official Hermes repository. Bundled skills are copied into the profile during installation and synchronized with update rules. Bundled plugins are discovered but opt-in: they do not load until explicitly enabled. “Official optional” means the skill ships in the upstream `optional-skills/` catalog but must be installed. “Nous-approved catalog MCP” means its manifest entered `optional-mcps/` through Hermes repository review. That review does not make the external server’s implementation, future updates, OAuth scopes, terms, or data handling part of Hermes.

## Recommended deployment stack

The minimum useful stack is smaller than the catalog. In Phase 1, use built-in web, file, document, session, and terminal capabilities only where the Job Charter permits them; keep bundled skills available but invoke a skill only for a named task. Add `grounded-citations` and `document-to-action-items` for evidence-heavy reading, then `weekly-review-planning` after the commitment ledger exists. Add document-format skills only when their output is reviewed in that format.

Separate selection from activation. Selection answers whether an extension has enough value to enter a controlled trial. Activation answers which profile, account, tools, and destinations it may use today. Installation alone answers neither question. Keep an extension register with status `proposed`, `inspected`, `trial`, `active`, `paused`, or `retired`; do not infer status from whether files remain on disk. A paused or disabled extension can still leave OAuth grants, API keys, local data, provider records, and dependency risk behind.

Review extension combinations as well as individual entries. A read-only mail connection plus a write-capable CRM connection can transfer content between systems even if each looks acceptable alone. A document skill plus a messaging adapter can turn a local draft into an external attachment. A tracing plugin can observe data handled by every other tool. Map the complete path from source through model, temporary files, logs, plugin hooks, MCP server, target service, and backup. Apply the strictest relevant data and authority rule across that path.

In Phase 2, introduce one account-facing skill in its own profile, preferably read-only at first. In Phase 3, schedule the already-proved workflow; scheduling is not a reason to add another extension. Phase 4 may add a remote service integration, but every write/send action remains Amber. Phase 5 may add the Hermes `codex` skill or a business MCP behind a bounded assignment. Phase 6 is for observability and evidence-driven expansion, not a late catalog shopping spree.

Recommended order:

1. Enable only needed built-in toolsets and record the baseline with `hermes tools --summary`.
2. Inspect the shipped skill definition and dependencies; run a synthetic success, forbidden-action, wrong-profile, and offline/expired-auth test.
3. For an optional skill, use `hermes skills inspect <identifier>` before `install`, then `hermes skills audit`.
4. For a plugin, inspect its manifest and capabilities, enable one plugin, restart, and verify its kill switch or disable path.
5. For MCP, prefer the Nous-approved catalog, install one server, mark external servers untrusted where appropriate, choose the smallest tool subset, and test denial as well as success.
6. Record owner, exact version or commit, scopes, cost model, review date, disable/remove procedure, remote revocation, and retained data.

## Hermes-native skills

These entries are verified in the pinned official bundled or optional skills catalogs. A skill is procedural guidance and may call existing tools or third-party CLIs; its presence does not itself grant account access.

| Hermes skill and status | Book use | Value | Permissions | Exposure | Setup | Cost | Maintenance | Phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `grounded-citations` — bundled | Source-led research, employer briefs, Canadian public-information checks, and claim ledgers | High | Low–Medium: web reads and local writing | Provider for searched/extracted content | Low | Search/extraction usage may apply | Low | 1 |
| `document-to-action-items` — bundled | Convert adult-supplied notices, policies, and meeting documents into cited obligations | High | Low–Medium: read documents, write local ledger | Local or configured model provider | Low | Model usage | Low | 1 |
| `weekly-review-planning` — bundled | Review commitments, stale work, owner decisions, and next-week shape | High | Low: local planning by default | Local or model provider | Low | Model usage | Low | 2 |
| `meeting-action-items` — bundled | Extract decisions, owners, and tasks from business meeting notes | Medium | Low–Medium: reads notes, can prepare tickets | Notes may reach model provider | Low | Model usage | Low | 2 |
| `email-inbox-triage` — bundled | Prioritize a dedicated secondary inbox and prepare replies | High | High if sending is available; constrain to read/draft | Mail and model providers | Medium | Mail service plus model usage | Medium: auth and policy drift | 2, Green read/draft only |
| `google-workspace` — bundled | Gmail, Calendar, Drive, Docs, and Sheets in family or business workflows | High | High: broad read/write APIs are possible | Broad Google workspace plus model route | High | Service plan may apply | High: OAuth scopes, CLI, account changes | 2–4, narrow scopes |
| `xlsx` — bundled | Opportunity, budget, scorecard, and operations workbooks | High | Medium: local file reads/writes | Local or model provider | Low | None beyond model route | Low | 2 |
| `docx` and `pdf` — bundled | Résumé artifacts, professional handoffs, rendered review, and forms | High | Medium: local document mutation | Local or model provider | Medium: rendering dependencies | None beyond model route | Medium | 2 |
| `session-librarian` — bundled | Find, rename, archive, and prune accumulated sessions under retention policy | Medium | Medium: session metadata and deletion capability | Local | Low | None | Low | 2 |
| `codex` — bundled | Delegate a bounded coding or artifact-production assignment from Hermes | Conditional high | High: may read/write code, run commands, and use network depending on enforcement | Codex route plus assigned workspace | High: Codex CLI/auth/sandbox | Service/usage | High: runtime and acceptance tests | 5 |
| `one-three-one-rule` — official optional | Turn a problem into three evidence-backed options and one recommendation | Medium | Low: procedural | Local or model provider | Low after `official/communication/one-three-one-rule` install | Model usage | Low | 2 |
| `1password` — official optional | Configure the `op` CLI and inject scoped secrets without copying values into prompts | Conditional high | High: secret read/injection | 1Password plus consuming process | High | Service plan | High: service account, vault, rotation | 3–5 |

Account-facing skills require the same external-identity and scope review as any custom integration. For example, the Google Workspace skill’s breadth is a reason to authorize one secondary account and the smallest required APIs, not a reason to connect the family’s primary Google identity. The `codex` skill must receive a bounded assignment card, enforced file/network/tool limits, and acceptance commands. A summary from the specialist is not acceptance evidence.

Useful but excluded from the default stack include `imessage`, `findmy`, `computer-use`, `xurl`, shopping, telephony, payment, and security-testing skills. Their potential to message people, observe location, control a desktop, publish, buy, call, trade, or probe systems is disproportionate to the first phases. “Excluded by default” is not a claim that the skill is malicious; it is a deployment decision based on effect and exposure.

## Hermes plugins

The following are official bundled Hermes plugins. All are opt-in. Run `hermes plugins list`, inspect the pinned source, enable by exact name, restart the relevant process, and prove disablement. Plugin code runs inside the Hermes process and lifecycle; a prompt boundary does not confine it.

| Bundled plugin | Book use | Value | Permissions | Exposure | Setup | Cost | Maintenance | Phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `disk-cleanup` | Track and remove defined ephemeral files under constrained Hermes/temp roots | Medium | High: deletion inside its allowed roots | Local | Low | None | Medium: review tracking and cleanup log | 2 after dry-run |
| `security-guidance` | Warn on 25 dangerous code patterns during file writes; optional block mode | Medium | Medium–High: observes and may block write/patch content | Local | Low | None | Medium: false positives and rule coverage | 2 for coding profiles |
| `observability/langfuse` | Export turn, model, and tool spans for evaluation | Conditional high | High: reads serialized messages, tool arguments/results, and usage | Broad provider or self-hosted Langfuse | High | Service plan or self-hosting | High: SDK, keys, retention, sampling | 6 |
| `teams_pipeline` | Graph-backed, transcript-first Microsoft Teams meeting processing | Conditional | High: meeting/transcript and Graph access | Microsoft plus model route | High | Service plan/usage | High | 4–5, business only |

`disk-cleanup` is not a general data-retention engine. Its quick mode uses defined categories and thresholds, while deep cleanup requests confirmation for riskier classes. Keep required audit records out of ephemeral categories and inspect `$HERMES_HOME/disk-cleanup/cleanup.log`. `security-guidance` is heuristic and explicitly does not replace isolation, review, or tests. Warning mode still writes the file; block mode can create workflow failures that require handling.

Langfuse is valuable only after a measurement question and retention policy exist. Its plugin can send message and tool content to the configured endpoint, subject to truncation and sanitization behavior. Start with synthetic data, self-host or choose a provider deliberately, reduce sampling, minimize fields, set retention, verify deletion, and keep family/career profiles out until separately approved. “Fail-open” means an observability outage does not stop the agent; therefore missing traces must be measured rather than mistaken for no activity.

Other shipped plugins—Spotify playback, Google Meet participation, image generation backends, achievements, and the Kanban dashboard—solve narrower needs. They are not part of the default family/business control stack. If adopted, rate their current pinned implementation using the same matrix rather than inheriting a rating from this section.

## MCP categories and examples

MCP is an interoperability protocol, not an endorsement channel. Hermes supports local stdio and remote HTTP servers, OAuth, environment substitution, per-server tool filters, and a trust setting. An MCP server can expose data and real mutations. Configure only one server at a time, prefer read-only tools, and treat a server’s `readOnlyHint` as a hint supplied by that server.

Every named example below is **external to Hermes**. The first six are present in the pinned Nous-approved MCP catalog; each uses an external vendor or bridge and links to its primary documentation. Catalog presence means the manifest received Hermes repository review, not that Nous operates or guarantees the external service.

| External MCP category and example | Value | Permissions | Exposure | Setup | Cost | Maintenance | Phase and control |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Work database — [Airtable MCP](https://support.airtable.com/docs/using-the-airtable-mcp-server) | High for a small-business ledger | High: bases, tables, records | Broad Airtable workspace | Medium OAuth | Service plan | Medium | 4–5; authorize a dedicated base/workspace and prune writes |
| Project management — [Asana MCP](https://developers.asana.com/docs/using-asanas-mcp-server) | Medium–High | High: tasks, projects, goals | Asana workspace | Medium OAuth | Service plan | Medium | 4–5; start with list/read tools and one project |
| Knowledge workspace — [Notion MCP](https://developers.notion.com/docs/mcp) | Medium | High: pages/databases may be mutable | Notion workspace | Medium OAuth | Service plan | Medium | 4; dedicate a teamspace/database and exclude family/career notes |
| Customer support — [Intercom MCP](https://developers.intercom.com/docs/guides/mcp) | High for support preparation | High: conversations, tickets, customer data | Broad customer/support data | Medium OAuth | Service plan | High: scopes, retention, policy | 5; read/draft first, human sends/changes state |
| Automation operations — [n8n bridge](https://github.com/CyberSamuraiX/hermes-n8n-mcp) | Conditional high | High: workflow inspection and optional activation/deactivation | Self-hosted n8n plus connected services | High: pinned git bridge, venv, API key | Self-hosting | High | 5; use catalog’s read-mostly default tool set |
| Payments — [Stripe MCP](https://docs.stripe.com/mcp) | Conditional | Critical: customers, invoices, payment-adjacent mutation | Financial/customer provider | High OAuth | Service plan/transaction ecosystem | High | 5 read-only preparation at most; Red for autonomous money movement |

The catalog also contains Atlassian, Linear, Figma, Sentry, Datadog, Supabase, Netlify, Vercel, Webflow, PayPal, Square, and other service-specific entries. They are intentionally not a recommended bundle. Choose the service already designated as the system of record; never add parallel SaaS merely to give Hermes another interface.

Filesystem and GitHub servers appear in official Hermes MCP documentation as configuration examples, but they are not in the pinned `optional-mcps/` catalog. Treat any package or server chosen for those examples as an **external MCP selected by the operator**: verify its primary repository, immutable version, maintainer, license, install script, dependencies, scopes, and revocation. Prefer Hermes built-in file tools or bundled GitHub skills when they already meet the task.

For external servers, set `trust: untrusted` unless the operator fully controls and has reviewed the server, then use `tools.include` as a whitelist. Disable resource and prompt utilities if they are unnecessary. A local stdio server runs a process and can inherit allowed environment variables; a remote server receives request content and may retain it. Neither is made safe simply by using MCP.

## Installation and review gate

Use this gate for each extension:

1. **Need:** name the observed workflow gap and why a built-in tool or plain prompt is insufficient.
2. **Provenance:** record Hermes-native status, exact upstream URL, pinned release/commit, license, manifest, bootstrap commands, dependencies, and maintainer.
3. **Capability:** enumerate reads, writes, sends, deletes, local processes, paths, OAuth scopes, environment values, network destinations, provider routes, and cost triggers.
4. **Confinement:** select dedicated profile, macOS account, secondary service identity, narrow resources, MCP tool include list, and egress controls. Prompt-declared limits are documented intent; OS/service enforcement is the boundary.
5. **Tests:** synthetic success, forbidden action, wrong profile, expired token, offline service, duplicate/unknown effect, disable/restart, uninstall, and remote revocation.
6. **Operations:** owner, installed date, review cadence, update policy, cost review, log/trace retention, kill switch, rollback version, and do-not-install threshold.

Commands are version-sensitive. Typical read-first sequences are `hermes skills inspect …` before `hermes skills install …`, `hermes plugins doctor … --ci` before `hermes plugins enable …`, and `hermes mcp catalog` before `hermes mcp install …`, `configure …`, and `test …`. Run `hermes security audit` after changing plugin or MCP dependencies. An audit with no known vulnerability does not prove safe behavior.

Reject or postpone an extension when its provenance is unclear, install script is opaque, required scopes exceed the task, it needs a primary identity, it cannot be disabled or remotely revoked, its writes cannot be reconciled, its cost cannot be bounded, or the owner cannot maintain it. The correct size of the extension stack is the smallest one whose evidence and maintenance burden the household or business can actually review.

## Sources

- Nous Research, [bundled skills catalog](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/skills-catalog.md).
- Nous Research, [official optional skills catalog](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/optional-skills-catalog.md).
- Nous Research, [skills system](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/skills.md).
- Nous Research, [plugins](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/plugins.md).
- Nous Research, [built-in plugins](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/built-in-plugins.md).
- Nous Research, [MCP client and server support](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/features/mcp.md).
- Nous Research, [pinned optional MCP manifests](https://github.com/NousResearch/hermes-agent/tree/v2026.8.19/optional-mcps).
- Model Context Protocol, [specification 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18) (accessed 2026-08-21).
