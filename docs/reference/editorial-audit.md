# First-edition editorial audit

**Audit date:** 2026-08-21

**Product baseline:** Hermes Agent v0.20.5, tag `v2026.8.19`, commit
`fcbd1076a93841fa88855acce810e342a5b78101`

**Scope:** 22 numbered chapters, four appendices, project guides, source map,
image provenance, site configuration, and release checks.

## Method

The release audit combined deterministic validators with a chapter-by-chapter
editorial pass. `tools/check_book.py --final` supplied the canonical file order,
word count, chapter and appendix contracts, Mermaid, local-link and asset,
version-label, prohibited-term, unresolved-marker, secret-pattern, provenance,
and project-guide checks. The Task 6–11 audits rechecked their bounded safety,
source, command, extension, Canadian-fact, delegation, and appendix-ledger
contracts against the immutable Hermes checkout. Pytest exercised the validator
mutation cases.

The final review also built from the hash-locked transitive Python environment,
checked source and built HTML links separately, and loaded every Mermaid-bearing
page in a browser process that blocked non-loopback requests. The browser assertion
required all 24 source diagrams to become non-empty SVG elements and recorded any
attempted third-party script, font, image, stylesheet, or API request as a failure.

The editorial pass compared every opening, Definitions section, Hermes mechanism,
professional and personal example, authority table, recovery section, field kit,
exercise/rubric, checklist, and reference list in manuscript order. It separately
scanned names and case facts, command families, model identifiers, ISO dates,
chapter references, repeated cross-file paragraphs, advice boundaries, local
assets, and source-map destinations. Commands were compared with Appendix A and
the pinned source-backed audits; factual or consequential language was checked
for a dated source and human or professional decision owner.

## Release counts

| Measure | Result |
| --- | ---: |
| Numbered chapters | 22 |
| Appendices | 4 |
| Chapter words | 99,654 |
| Appendix words | 10,599 |
| Total measured Markdown words | 110,253 |
| Required chapter-section checks | 264 of 264 |
| Mermaid blocks in numbered chapters | 24 |
| Chapter reference URL occurrences | 261 |
| Deduplicated external source-ledger rows | 168 |
| Explicit pinned Hermes links in the source map | 137 |
| Version-labelled manuscript units | 26 of 26 |
| Chapters containing Green, Amber, and Red boundaries | 22 of 22 |
| Narrative cross-chapter references | 36 |
| ISO date occurrences in numbered chapters | 122 |
| Provenanced local image assets | 8 |

The validator excludes fenced code blocks from manuscript word counts. The source
ledger is fenced so its 168 repetitive CSV records remain copyable without
distorting Appendix D's prose contract.

## Editorial findings and corrections

- Replaced the temporary MkDocs navigation with the canonical Home, six-part,
  22-chapter, four-appendix, About order and corrected the stale home-page count.
- Expanded all 137 pinned Hermes source-map paths into direct, clickable tag URLs.
- Added the missing agent-loop, prompt-assembly, and session-storage evidence to
  Chapter 1 and updated Appendix D's affected-unit mappings.
- Standardized Chapter 2's **Evidence check** capitalization.
- Made Chapter 5's installer download stop immediately on `curl` failure and
  clarified that a version-stamped local filename is an operator label, not proof
  that the unversioned installer URL is release-pinned.
- Removed generic runtime model naming from the manuscript. The only named model
  identifier is the official `gpt-5.6-sol`; other lanes remain criteria-based.
- Repaired the Chapter 3 worksheet table and Chapter 11 boundary sentence so
  Markdown lint and rendered emphasis are unambiguous.
- Placed all eight pinned, provenance-tracked Hermes screenshots and feature
  illustrations in their intended chapters, with version captions and meaningful
  alt text; added one rendered warning admonition for the OS-boundary rule.
- Placed the official Desktop session and administration-dashboard screenshots
  directly beside their Chapter 5 interface explanations for beginner orientation.
- Replaced remote Mermaid and font dependencies with exact hash-verified local
  assets, built the unlisted image-provenance page, pinned every GitHub Action to a
  reviewed commit with checkout credentials disabled, and added the single
  `tools/verify_release.sh` clean-release entry point.
- Created an original editorial theme and cover using self-hosted OFL Newsreader,
  Space Grotesk, and JetBrains Mono fonts; made curator and repository identity
  persistent; and corrected desktop title wrapping plus mobile table/code overflow
  found during light, dark, 390-by-844, and print review.
- Preserved the Chen–Patel family, Priya's career transition, Alex's business role,
  children Leena and Ben, and Harbourlight Learning without introducing real data.
  Later chapters progressively move from concepts and installation to controls,
  family/career work, business operation, delegation, and evidence-gated autonomy.
- Confirmed that Definitions precede mechanism detail in all 22 chapters, that
  every consequential workflow retains Green/Amber/Red semantics, and that
  financial, tax, health, legal, employment, school-consent, and privacy decisions
  stop at accountable people or qualified professionals.
- Found no repeated cross-file prose paragraph of 18 or more words after excluding
  headings, tables, references, and copy-ready code; repeated policy vocabulary is
  intentional. Final validation found no broken local link, missing asset,
  unresolved marker, prohibited model spelling, or secret pattern.

## Residual versioned limits

This audit proves the first-edition contracts at the pinned release; it does not
turn mutable provider, government, pricing, law, platform-policy, or model pages
into permanent facts. External facts and source-ledger rows were observed on
2026-08-21. The deterministic CI run therefore checks inventory and pinned source
content without depending on live government availability. Task 8's bounded live
source check remains an explicit manual workflow option for release editors.

The semantic Task 6–11 linters are finite regression guards, not general natural-
language safety proofs. Lychee can prove reachability at one moment, not continuing
authority or factual support. Its deterministic release configuration excludes
loopback preview URLs, generated or installed trees where appropriate, and only the
exact private book-repository URL, which returns 404 to unauthenticated runners.
The built HTML is checked from the `site/` root rather than excluded. A future
baseline update must repeat the coordinated source, command, screenshot, model,
manuscript, ledger, test, build, link, offline-network, and visual review described
in the contributor guide and Appendix D.
