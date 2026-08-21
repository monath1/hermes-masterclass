#!/usr/bin/env bash
set -euo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly HERMES_REF="v2026.8.19"
readonly HERMES_COMMIT="fcbd1076a93841fa88855acce810e342a5b78101"
readonly HERMES_REPOSITORY="https://github.com/NousResearch/hermes-agent.git"
readonly MARKDOWNLINT_VERSION="0.23.2"
readonly LYCHEE_VERSION="0.24.2"
readonly VERIFY_VENV="${HERMES_VERIFY_VENV:-$PROJECT_ROOT/.venv}"

cd "$PROJECT_ROOT"

cleanup_paths=()
cleanup() {
  local path
  # Bash 3.2 (the macOS system shell) treats an empty array expansion as an
  # unbound variable under `set -u`; the default keeps cleanup portable.
  for path in "${cleanup_paths[@]:-}"; do
    test -n "$path" && test -d "$path" && rm -rf "$path"
  done
  return 0
}
trap cleanup EXIT

if test ! -x "$VERIFY_VENV/bin/python"; then
  "${PYTHON_BIN:-python3}" -m venv "$VERIFY_VENV"
fi
"$VERIFY_VENV/bin/python" -m pip install --require-hashes -r requirements.lock

if test -n "${HERMES_SOURCE:-}"; then
  hermes_source="$HERMES_SOURCE"
else
  hermes_checkout_root="$(mktemp -d "${TMPDIR:-/tmp}/hermes-source.XXXXXX")"
  cleanup_paths+=("$hermes_checkout_root")
  hermes_source="$hermes_checkout_root/hermes-agent"
  git init -q "$hermes_source"
  git -C "$hermes_source" remote add origin "$HERMES_REPOSITORY"
  for fetch_attempt in 1 2 3; do
    if git -C "$hermes_source" fetch -q --depth=1 origin "refs/tags/$HERMES_REF"; then
      break
    fi
    if test "$fetch_attempt" = 3; then
      echo "Unable to fetch pinned Hermes tag after three attempts" >&2
      exit 1
    fi
  done
  git -C "$hermes_source" checkout -q --detach FETCH_HEAD
fi

actual_commit="$(git -C "$hermes_source" rev-parse HEAD)"
test "$actual_commit" = "$HERMES_COMMIT" || {
  echo "Pinned Hermes checkout mismatch: expected $HERMES_COMMIT, found $actual_commit" >&2
  exit 1
}

HERMES_TEST_SOURCE="$hermes_source" "$VERIFY_VENV/bin/pytest" -q
"$VERIFY_VENV/bin/python" tools/check_book.py --final
for audit in 6 7 8 9 10 11; do
  "$VERIFY_VENV/bin/python" "tools/check_task${audit}.py" --hermes-source "$hermes_source"
done
if test "${HERMES_TASK8_LIVE:-0}" = "1"; then
  "$VERIFY_VENV/bin/python" tools/check_task8.py \
    --hermes-source "$hermes_source" --live
fi

"$VERIFY_VENV/bin/mkdocs" build --strict
"$VERIFY_VENV/bin/python" tools/check_release.py --site site
"$VERIFY_VENV/bin/codespell" \
  --skip "docs/assets/vendor/mermaid/10.4.0/mermaid.min.js" \
  docs README.md CONTRIBUTING.md research
"$VERIFY_VENV/bin/python" -m py_compile tools/*.py tests/*.py
npx --yes "markdownlint-cli2@$MARKDOWNLINT_VERSION" \
  "**/*.md" "#site/**" "#.venv/**" "#.superpowers/**"

case "$(uname -s)-$(uname -m)" in
  Darwin-arm64)
    lychee_asset="lychee-aarch64-apple-darwin.tar.gz"
    lychee_sha256="c9d3740ea2d891854d37116c9fba840f37b6e7c89d330e7db84ac333631c4977"
    ;;
  Darwin-x86_64)
    lychee_asset="lychee-x86_64-apple-darwin.tar.gz"
    lychee_sha256="887503a9cff667d322b8d0892b40bf49976eb9507af8483220a3706cdad55978"
    ;;
  Linux-aarch64)
    lychee_asset="lychee-aarch64-unknown-linux-gnu.tar.gz"
    lychee_sha256="91a7bd65685da41b90ccb9bc867a3d649a7818042dae04ff405e55a25bddee4c"
    ;;
  Linux-x86_64)
    lychee_asset="lychee-x86_64-unknown-linux-gnu.tar.gz"
    lychee_sha256="1f4e0ef7f6554a6ed33dd7ac144fb2e1bbed98598e7af973042fc5cd43951c9a"
    ;;
  *)
    echo "Unsupported Lychee release platform: $(uname -s)-$(uname -m)" >&2
    exit 1
    ;;
esac

lychee_root="$(mktemp -d "${TMPDIR:-/tmp}/hermes-lychee.XXXXXX")"
cleanup_paths+=("$lychee_root")
lychee_archive="$lychee_root/$lychee_asset"
curl --retry 3 --retry-all-errors -fsSLo "$lychee_archive" \
  "https://github.com/lycheeverse/lychee/releases/download/lychee-v$LYCHEE_VERSION/$lychee_asset"
actual_lychee_sha256="$(
  "$VERIFY_VENV/bin/python" -c \
    'import hashlib, pathlib, sys; print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())' \
    "$lychee_archive"
)"
test "$actual_lychee_sha256" = "$lychee_sha256" || {
  echo "Lychee archive hash mismatch" >&2
  exit 1
}
tar -xzf "$lychee_archive" -C "$lychee_root"
lychee_bin="$(find "$lychee_root" -type f -name lychee -perm -111 -print -quit)"
test -n "$lychee_bin" || {
  echo "Verified Lychee archive did not contain an executable" >&2
  exit 1
}
"$lychee_bin" --version | grep -F "lychee $LYCHEE_VERSION"

lychee_common=(
  --no-progress
  --exclude-loopback
  --exclude '^https://github\.com/monath1/hermes-masterclass$'
  --exclude-path .venv
  --exclude-path .superpowers
)
"$lychee_bin" "${lychee_common[@]}" --root-dir . --exclude-path site '**/*.md'
"$lychee_bin" "${lychee_common[@]}" --root-dir site 'site/**/*.html'

"$VERIFY_VENV/bin/python" tools/check_offline_site.py --site site

git diff --check
git diff --cached --check
if git rev-parse --verify origin/main >/dev/null 2>&1; then
  comparison_base="$(git merge-base HEAD origin/main)"
else
  comparison_base="$(git rev-list --max-parents=0 HEAD)"
fi
git diff --check "$comparison_base"

echo "verify_release: OK — pinned environment, manuscript, site, links, and offline diagrams"
