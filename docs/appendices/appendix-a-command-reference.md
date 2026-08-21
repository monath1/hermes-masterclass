# Appendix A: Commands and interface reference

**Verified against Hermes Agent v0.20.5 (2026-08-19).** Commands and labels in this appendix are version-sensitive. Recheck the linked pinned source before using them with another release.

## How to use this reference

Hermes has several control surfaces. A shell command starts with `hermes` and belongs in macOS Terminal, outside an active chat unless the row says otherwise. An in-chat command starts with `/` and belongs in the CLI, TUI, or a supported messaging conversation. A Hermes tool call is selected by the agent from an enabled toolset; it is an interface description, not text to paste into Terminal. A conceptual snippet is a prompt or policy fragment, not executable code.

The labels below make that distinction explicit:

When a row omits an optional flag, consult the pinned reference and the installed command help before assuming the omitted behavior is harmless.

| Label | Where it runs | Safe reading rule |
| --- | --- | --- |
| **Terminal** | macOS shell under the dedicated Hermes user | Inspect flags before commands that update, import, delete, send, or change service state. |
| **In chat** | Active Hermes session or authorized gateway chat | Messaging permissions can differ between admins and ordinary allowed users. |
| **Hermes tool** | Agent loop with the named toolset enabled | Tool availability is capability, not permission; the Job Charter still governs use. |
| **Conceptual** | Prompt, runbook, or approval record | Do not paste it into a shell. Fill in the brackets and review it as prose. |

The safest lookup sequence is: identify the surface, select the profile, inspect current state, preview a change where possible, apply one change, then observe the result. Avoid `--yolo`, `--force`, `--yes`, destructive checkpoint clearing, and unreviewed imports in routine operations. They are convenience switches, not safe defaults.

## Setup and status

| Surface | Reference | Purpose and caution |
| --- | --- | --- |
| Terminal | `hermes --version` | Print the installed version. Record it before troubleshooting or changing the baseline. |
| Terminal | `hermes setup` | Run the configuration wizard. Section forms include `hermes setup model`, `terminal`, `gateway`, `tools`, and `agent`. A bare rerun revisits existing values. |
| Terminal | `hermes status` | Show agent, authentication, and platform state. Add `--all` for a redacted shareable view or `--deep` for slower checks. |
| Terminal | `hermes doctor` | Diagnose configuration and dependency problems. Review findings before considering `hermes doctor --fix`. |
| Terminal | `hermes dump` | Produce a support-oriented setup summary. It is designed for sharing, but still inspect it for household or business metadata. |
| Terminal | `hermes debug share --local` | Render a diagnostic bundle locally without uploading it. Prefer this before any networked support share. |
| Terminal | `hermes dashboard` | Open the local dashboard at the default loopback address. Keep the default `127.0.0.1` bind; a non-loopback bind requires an authentication provider. |

A clean initial proof is deliberately small: version, `doctor`, status, then a read-only chat. Do not connect a primary inbox, broad home directory, or payment service merely to make the status screen look complete.

## Models

| Surface | Reference | Meaning |
| --- | --- | --- |
| Terminal | `hermes model` | Full provider-and-model setup. It can add providers, run OAuth, accept API keys, and configure custom endpoints. Exit the active chat first. |
| In chat | `/model` | Show or switch among providers already configured. It cannot add a provider or collect a new credential. |
| Terminal | `hermes chat --provider <provider> --model <model>` | Override routing for one run without changing the saved default. |
| Terminal | `hermes fallback list` | Inspect the ordered fallback chain. `add`, `remove`, and `clear` mutate it. A fallback must be allowed to receive the same data as the primary route. |
| Terminal | `hermes prompt-size` | Measure the fixed system-prompt and tool-schema budget offline. `--json` supports local analysis without an API call. |
| In chat | `/usage` | Show session token and estimated-cost information; provider account limits appear only when available. |

Use the exact provider/model identifier shown by the installed release. A mid-session model switch can invalidate prompt caching and changes the system that will interpret the existing conversation. For consequential work, record provider, model, route, and fallback in the handback.

## Tools, skills, plugins, and MCP

These layers are not synonyms. Tools perform actions; skills provide procedural instructions; plugins add code through lifecycle hooks, tools, commands, or provider interfaces; MCP connects Hermes to an external tool server.

| Surface | Reference | Use |
| --- | --- | --- |
| Terminal | `hermes tools --summary` | Print the enabled-tools summary. Bare `hermes tools` opens per-platform configuration. |
| Hermes tool | `skills_list`, `skill_view`, `skill_manage` | List and load skill instructions, or manage user-created skills. The agent invokes these; do not type them as shell commands. |
| Terminal | `hermes skills inspect <identifier>` | Preview a registry skill before installation. Follow with `audit`, then install only if provenance and requested capabilities are acceptable. |
| Terminal | `hermes skills list` | List installed skills. `check` finds upstream changes; `update` changes installed hub skills; `uninstall` removes one. |
| Terminal | `hermes plugins list` | Inspect installed and bundled plugins and their enabled state. Bundled plugins are opt-in. |
| Terminal | `hermes plugins enable <name>` | Enable one reviewed plugin. `disable` preserves it without loading; `remove` uninstalls a user-installed plugin. |
| Terminal | `hermes plugins doctor <path-or-id> --ci` | Validate manifest, loader, and registration paths. Passing validation is not a security endorsement. |
| Terminal | `hermes security audit` | Query OSV.dev for the Hermes environment, plugin requirements, and pinned MCP packages. It is a networked supply-chain check. |
| Terminal | `hermes mcp catalog` | List Nous-approved catalog entries. Catalog review is a starting point, not authority to expose every tool. |
| Terminal | `hermes mcp install <name>` | Install a catalog MCP, then select the smallest tool subset. Use `configure`, `test`, `list`, and `remove` for lifecycle operations. |
| In chat | `/reload-skills`, `/reload-mcp`, `/plugins` | Refresh skill or MCP discovery, or inspect plugin status without leaving the session. |

For a conceptual tool call, write the intent rather than pretending the call is a shell command: “Use the `cronjob` tool with action `list`; make no changes.” MCP tool names are registered dynamically from the server and its advertised capabilities. Confirm the current names with the installed configuration instead of copying a guessed call signature.

## Profiles and gateways

| Surface | Reference | Use |
| --- | --- | --- |
| Terminal | `hermes profile list` | List isolated Hermes profiles. Each has its own configuration, sessions, skills, and home directory. |
| Terminal | `hermes profile create work --clone` | Create a profile by cloning configuration, environment, personality, and skills. Inspect copied credentials immediately; clone only from an appropriate source profile. |
| Terminal | `hermes profile use <name>` | Set the sticky default. Prefer explicit `hermes -p <name> …` in scripts so profile choice is visible. |
| Terminal | `hermes profile show <name>` | Display the resolved profile home and details before a destructive or external action. |
| Terminal | `hermes profile export <name> -o <archive>` | Export one profile. Treat the archive as sensitive and test import into an isolated location. |
| Terminal | `hermes gateway install` | Install the macOS launchd service for the active profile. Then use `start`, `stop`, `restart`, and `status`. |
| Terminal | `hermes gateway list` | See gateway state across profiles. `--all` on start, stop, or restart affects every profile and therefore deserves explicit review. |
| In chat | `/platform list` | Inspect loaded adapters. Admin-only pause/resume can stop dispatch to one platform without broadening authority. |
| Terminal | `hermes pairing list` | Show pending and approved messaging identities. Use `approve`, `revoke`, or `clear-pending` with exact platform and identity values. |

Stopping a gateway halts new messaging dispatch but does not revoke provider tokens, close every active child process, or undo external effects. A complete stop procedure addresses each layer separately.

## Cron and goals

Cron is scheduled fresh-session work; a goal is an active standing objective that may continue across turns. Do not use either as an approval substitute.

| Surface | Reference | Use |
| --- | --- | --- |
| Terminal | `hermes cron list` | Inspect jobs before editing them. `status` checks the scheduler; `tick` runs due jobs once. |
| Terminal | `hermes cron create` | Create a job from a prompt, optionally with repeated `--skill`. Record timezone, delivery target, and missed-run policy in the job contract. |
| Terminal | `hermes cron pause <job>` | Pause without deletion. `resume` computes a future run; `run` requests execution on the next scheduler tick. |
| Hermes tool | `cronjob` | Unified manager with `create`, `list`, `update`, `pause`, `resume`, `run`, and `remove` actions. Require the agent to return the job ID and next run. |
| In chat | `/goal <text>` | Set a persistent goal. Use `/goal status`, `pause`, `resume`, or `clear`; setting a replacement while the agent runs requires `/stop` first. |
| In chat | `/heartbeat every <interval> <prompt>` | Re-enter an idle session on a cadence. Status, pause, resume, and clear are available. |
| In chat | `/stop` | Interrupt the running agent and kill tracked background processes. Follow with job, gateway, and credential controls when the incident is broader. |

Conceptual safe default: “Run once in a synthetic profile; deliver only to the owner’s private test channel; create drafts only; report missing sources; never catch up external effects after downtime.”

## Sessions and checkpoints

| Surface | Reference | Use |
| --- | --- | --- |
| Terminal | `hermes sessions list` | List recent sessions. `browse` adds search and lifecycle status; `stats` summarizes storage. |
| Terminal | `hermes --resume <id-or-title>` | Resume a named session. `--continue` selects the most recent match; `--in <dir>` scopes lookup to a workspace. |
| In chat | `/new <name>` | Start a fresh session. `/resume`, `/sessions`, `/title`, `/compress`, `/undo`, and `/branch` manage continuity. |
| Terminal | `hermes sessions export <output> --session-id <id>` | Export JSONL for review or transfer. Redact before sharing. |
| Terminal | `hermes sessions prune --dry-run` | Preview retention filters. Archive is reversible visibility control; prune and delete remove records. |
| Terminal | `hermes chat --checkpoints` | Enable file checkpoints for one session. Checkpoints are opt-in and cover filesystem changes, not remote messages or payments. |
| In chat | `/rollback` | List checkpoints; `/rollback diff <N>` previews; `/rollback <N>` restores while keeping human edits by default. |
| Terminal | `hermes checkpoints` | Inspect shadow-store size. `prune` performs maintenance; `clear` is irreversible and is not a routine recovery step. |

Before a retry, determine whether the previous operation changed only files or may have changed an external system. Rollback can restore a file while leaving an already-sent message, submitted form, or provider mutation untouched.

## Secrets

| Surface | Reference | Use |
| --- | --- | --- |
| Terminal | `hermes config env-path` | Print the active profile’s environment-file path without printing values. `config path` locates configuration. |
| Terminal | `hermes auth list` | Inspect provider credential pools. `status`, `add`, `remove`, `reset`, and `logout` change provider authentication state. |
| Terminal | `hermes secrets bitwarden status` | Verify Bitwarden Secrets Manager configuration and token validation. |
| Terminal | `hermes secrets bitwarden sync` | Dry-run a secret fetch and report changes. `--apply` exports into the current shell, so use it only in a controlled terminal. |
| In chat | `/reload` | Reload environment variables into the current CLI session after an authorized rotation. Restart gateway services separately so they receive new values. |

Never put a secret value in a prompt, Job Charter, incident ticket, screenshot, shell history, or appendix example. Record a label, scope, owner, expiry, and fingerprint or suffix. After rotation, restart consumers, prove the new credential works within least privilege, revoke the old credential at the provider, and prove the old one fails.

## Update and recovery

| Surface | Reference | Use |
| --- | --- | --- |
| Terminal | `hermes update --check` | Read-only check for an available update. |
| Terminal | `hermes update --plan` | Print install type, running profile services, versions, and restart plan without changing them. |
| Terminal | `hermes update --backup` | Force quick state plus a full pre-update Hermes-home archive before updating. Confirm archive custody and free space. |
| Terminal | `hermes backup -o <path>` | Create a full Hermes-data archive; `--quick --label <name>` creates a state-focused snapshot. Checkpoints and source code are excluded. |
| Terminal | `hermes import <archive>` | Restore an archive, overwriting files in the active Hermes home. Stop the gateway first and do not use `--force` during a rehearsal. |
| Terminal | `hermes logs gateway --since 1h` | Inspect gateway evidence. Other useful forms are `errors`, `--level`, `--session`, and `-f`. |
| Terminal | `hermes config check` | Find missing or stale configuration; `migrate` interactively adds newly introduced options. |

Recovery order is containment, evidence preservation, identity and effect reconciliation, configuration diagnosis, restore or repair, synthetic re-entry testing, and only then resumption. Do not start with an update, broad reset, checkpoint clear, or blind retry. The command that makes an error disappear can also erase the evidence needed to understand an uncertain external effect.

## Sources

- Nous Research, [CLI commands reference at tag v2026.8.19](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/cli-commands.md).
- Nous Research, [slash commands reference at tag v2026.8.19](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/slash-commands.md).
- Nous Research, [built-in tools reference at tag v2026.8.19](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/tools-reference.md).
- Nous Research, [profile commands reference at tag v2026.8.19](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/reference/profile-commands.md).
- Nous Research, [checkpoints and rollback](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/user-guide/checkpoints-and-rollback.md).
- Nous Research, [updating and uninstalling](https://github.com/NousResearch/hermes-agent/blob/v2026.8.19/website/docs/getting-started/updating.md).
