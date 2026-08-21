# Contributing

## Style

Write original, compact prose for a beginner-to-intermediate reader. Define unavoidable technical vocabulary before relying on it, lead with observable outcomes, distinguish prompts from executable commands and tool calls, and prefer short concrete examples over feature lists. Preserve the Canadian family and one- or two-person business running case without turning its fictional details into product facts.

## Chapter contract

Every numbered chapter must include the chapter-contract sections validated by `tools/check_book.py`, one substantive Mermaid diagram, Green/Amber/Red authority boundaries, failure and recovery guidance, a reusable field kit, an exercise with a separated answer or rubric, and primary references. Appendices use their manifest word contracts and required section contracts instead of the numbered-chapter structure.

Use the Canadian family and small-business running case only as a fictional operating case. Never add real family information, credentials, API keys, or screenshots from personal accounts. Financial, health, tax, legal, employment, and privacy material must prepare readers for review or professional handoff; it must not present professional advice.

## Source hierarchy

Begin research at `research/hermes-v2026.8.19-source-map.md`, then read the exact cited source. Use this hierarchy:

1. the pinned Hermes repository, official Hermes documentation, security policy, and release material;
2. official OpenAI documentation for OpenAI models, APIs, and Codex;
3. official Apple, Canadian government, messaging, identity, and service-provider material for platform or jurisdiction claims;
4. primary standards and research where the product and government sources do not answer the question.

Commands, settings, model names, prices, laws, and interface labels require a primary source. Version-sensitive Hermes statements must carry the exact label: `Verified against Hermes Agent v0.20.5 (2026-08-19).` Use the official identifier `gpt-5.6-sol`; the validator rejects the common incorrect spelling. Record an ISO observation date for mutable external facts. Paraphrase sources; do not reproduce documentation passages as manuscript prose.

## Screenshot policy

Copy screenshots only from the pinned official Hermes checkout, preserve their local filename, and add a complete entry to `docs/assets/images/PROVENANCE.md`. Do not use external image hotlinks or placeholders.

Every screenshot also needs a matching `docs/assets/images/provenance.yml` entry with exact upstream path, `v2026.8.19` tag, MIT license, chapter usage, and meaningful alt text. Captions identify the pinned release when the interface is version evidence. Never capture personal accounts, credentials, private family/business data, or live provider tokens. A replacement updates the image, both provenance records, captions, and every use together.

## Version-update procedure

Treat a baseline update as one coordinated editorial change:

1. identify the candidate Hermes tag and commit, then diff the pinned command, tool, model, profile, messaging, automation, security, secret, skill, plugin, MCP, update, and recovery sources;
2. inventory changed commands, defaults, trust assumptions, extension entries, screenshots, provider behavior, and external dated facts;
3. update the source map, verification label, affected chapters and appendices, manifest, README, About page, provenance, and tests together;
4. run every bounded task audit against the candidate checkout, plus declared live primary-source checks where applicable;
5. run the full release suite and record deliberate pinned exceptions rather than mixing releases silently.

Appendix D contains the detailed release checklist. Do not change only the displayed version string.

## Local checks

```shell
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pytest -q
.venv/bin/mkdocs build --strict
.venv/bin/python tools/check_book.py
.venv/bin/python tools/check_task6.py --hermes-source /tmp/hermes-agent-v2026.8.19
.venv/bin/python tools/check_task7.py --hermes-source /tmp/hermes-agent-v2026.8.19
.venv/bin/python tools/check_task8.py --hermes-source /tmp/hermes-agent-v2026.8.19
.venv/bin/python tools/check_task9.py --hermes-source /tmp/hermes-agent-v2026.8.19
.venv/bin/python tools/check_task10.py --hermes-source /tmp/hermes-agent-v2026.8.19
```

The Task 10 audit is a bounded manuscript lint for Chapters 21–22. It checks
their word contracts, named delegation and evaluation artifacts, the flat
specialist-roster control, prompt-versus-enforced capability boundaries,
completion-versus-correctness denominators, ordered delegation and evidence
flows, the strengthened Gate 1 and feasible Gate 5 review window, all six
90-day phases and gates, and pinned Hermes source assertions. Keep its semantic
checks finite and structural; it is not a general natural-language evaluator
or a claim that a passing chapter makes an agent safe.

The Task 9 audit is a bounded manuscript lint for Chapters 19–20. It checks their word contracts, named business-OS and functional-playbook artifacts, required decision rows inside the owner/co-owner/Hermes responsibility table, human approval/action plus receipt/read-back/metrics labels in the lead and campaign trajectories, the finite list of prohibited business authorizations, and pinned Hermes source assertions. When changing the checker, keep semantic tests focused on those declared contracts and include safe negations plus structural mutation cases; do not grow it into a general NLP policy engine.

The ordinary Task 8 audit is deterministic and network-free: it checks the selected official URLs, visible observation dates, declared content contracts, dated Canadian amounts/deadlines/thresholds, and pinned Hermes source text. Run the separate live verification to exercise the load-bearing content assertions when preparing a release or substantively revising Chapters 17–18:

```shell
.venv/bin/python tools/check_task8.py --hermes-source /tmp/hermes-agent-v2026.8.19 --live
```

Live mode requires a terminal 2xx response, follows a bounded number of redirects one hop at a time, rejects non-HTTPS or off-domain hops before following them, and checks factual anchors in the returned page. It is intentionally excluded from push and pull-request runs because external availability is nondeterministic. To run it in CI, open the **Quality** workflow manually and enable **Verify Task 8 official pages, redirect domains, and content anchors**.

The Canadian numeric-claim scan requires a nearby ISO observation date for government amounts, deadlines, percentages, and retention periods. A local cadence or planning cap is exempt only when the prose explicitly calls it a `family-selected` or `owner-selected` `operating policy`; that marker must not be used for an externally imposed rule.

Use `--final` only once all 22 chapters and four appendices exist. Run `git diff --check` before committing.
