# Vendored editorial fonts

The site self-hosts three variable fonts from Fontsource 5.3.0. Each package and
font is distributed under the SIL Open Font License 1.1 (`OFL-1.1`). Only the Latin WOFF2 files
used by the book are copied; no font request leaves the local preview.

| Family | Exact package | Package archive SHA-256 | Vendored files and SHA-256 |
| --- | --- | --- | --- |
| Newsreader | `@fontsource-variable/newsreader@5.3.0` | `4b8cfba8f4e79abe7b221b761b751d76569fd2d2303a9cace2e90b862c56630d` | normal `62981321d9a3cc7a61a73792729043703fd6112da86e8ec848bb57f088578757`; italic `48bc8861b9b2ca9300747cad4fd6a3b4ac3028d364df00bd1b72097baa75e509`; license `26028ec4e13b650065fa525a09532176f8a668b76ff849ea01c564a7480f91e7` |
| Space Grotesk | `@fontsource-variable/space-grotesk@5.3.0` | `47d1b51d64ed541b7e74f38e9e682a8ff1bbfd1b68bfd7fff74ac9175058e73c` | normal `0640890476fc1198ab4de571fb658de443c4d85b66466ec09534a8737ab1ce9d`; license `18a4de52385f6b988782639d5d0cc1326e5a8c2de9a7f01d7b20d9aedcc60943` |
| JetBrains Mono | `@fontsource-variable/jetbrains-mono@5.3.0` | `996fe6368a480c9ce15d4de22a2682b7c40b403718fee2b15e7272f244fd993f` | normal `18be452724bfdc236c074ca94a249a7f41a86752c7d04ab258ce9ed5651f6a7e`; italic `a8afa085e9ca5e53434e2ee918ba6b65c7dd4dda56509976b36591478c99d62e`; license `403581b69dac5cff4079205e01c6b467e56af449ecbd7247693ddb1baafa005b` |

The package integrity strings recorded by npm are:

- Newsreader: `sha512-rrzYi43qMpbzwuFtf9OkWH8sxAPVPcQQQEwXpPtwaKYeJ8yVg5aLs5kawmo1f2Q1t1M38TLmEKCkGVDsYwgdFw==`
- Space Grotesk: `sha512-2IxmvfB08i9vnGB3Ym/AXvhRE+8XOjWMXIyDum03c+tPwH0FUoMNQfGpU8NXPxjbws0Vvss3AH0Zqt4oJBBAdw==`
- JetBrains Mono: `sha512-F32xpS2NsGYoQi2ADSkKTgpJj7ozajsGgDJ8woTnqjmIB+dxDIqImjl4pXZVEExu8UFZ2ndhmX18EBS/hdz3Lw==`

## Audited update procedure

1. Review the candidate Fontsource release, metadata, upstream family license, and
   glyph coverage.
2. Run `npm pack --ignore-scripts --json @fontsource-variable/FAMILY@VERSION` in a
   temporary directory and verify the registry integrity before extracting it.
3. Copy only the required WOFF2 subsets and the package `LICENSE`; record archive,
   file, and license SHA-256 values above.
4. Update `fonts.css` and the exact hash inventory in `tools/check_release.py`.
5. Run `tools/verify_release.sh` and inspect representative light, dark, mobile, and
   print pages before accepting the update.
