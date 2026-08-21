# Vendored Mermaid runtime

The book renders diagrams with the browser bundle from Mermaid **10.4.0**. The
runtime is local so a private preview never needs a CDN, and the version remains
identical to the release that the first-edition visual audit covered.

The upstream bundle contains trailing spaces. `.gitattributes` disables Git's
whitespace warning only for this exact hash-verified file so it remains byte-for-byte
identical; authored files retain the normal whitespace checks.

| Item | Value |
| --- | --- |
| Package | `mermaid@10.4.0` |
| License | MIT |
| Registry tarball | `https://registry.npmjs.org/mermaid/-/mermaid-10.4.0.tgz` |
| npm integrity | `sha512-4QCQLp79lvz7UZxow5HUX7uWTPJOaQBVExduo91tliXC7v78i6kssZOPHxLL+Xs30KU72cpPn3g3imw/xm/gaw==` |
| Tarball SHA-256 | `91cb14dc936d0234aa37122c7f28d62d132eb5e09392082ef876d5eaf492ce08` |
| `mermaid.min.js` SHA-256 | `2cf7bb6cdc4a6ea96da3d324a4447d8300d1da703ce5f31311608642c0f86269` |
| `LICENSE` SHA-256 | `ec9fb67dcb25eccc416ed56e1aab819222c805a2a4bfe4cb19e7556bf2ffde80` |
| Source tag | `https://github.com/mermaid-js/mermaid/tree/v10.4.0` |

## Audited update procedure

1. Choose an exact Mermaid release and review its release notes, license, and browser
   bundle changes.
2. In a temporary directory, run `npm pack --ignore-scripts --json mermaid@VERSION`.
3. Verify the registry-reported integrity and record a SHA-256 for the downloaded
   archive.
4. Extract only `package/dist/mermaid.min.js`. Copy the exact tagged upstream
   `LICENSE`; the 10.4.0 npm archive does not contain a license file.
5. Record both file hashes here, update the versioned paths in `mkdocs.yml` and
   `tools/check_release.py`, then run `tools/verify_release.sh`.
6. Accept the update only when the network-denied browser check renders every diagram
   as a non-empty SVG and the light, dark, mobile, and print audits remain readable.
