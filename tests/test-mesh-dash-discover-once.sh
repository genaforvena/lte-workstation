#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/.mesh/knowledge"
: > "$td/.mesh/study.log"
: > "$td/.mesh/ideas-queue"
: > "$td/.mesh/chat.log"

for n in $(seq 1 381); do
  printf 'capability fixture %03d\n' "$n" >"$td/.mesh/knowledge/capability-old-2026-08-$(printf '%02d' "$(( (n % 28) + 1 ))")-${n}.md"
done
printf 'newest\n' >"$td/.mesh/knowledge/capability-new-20260919.md"
printf 'middle\n' >"$td/.mesh/knowledge/capability-mid-2026-09-18.md"

out="$td/out"
if ! timeout 10s env HOME="$td" MESH_DIR="$td/.mesh" MESH_DASH_FAST=1 \
    bash "$ROOT/scripts/mesh-dash" --once discover >"$out" 2>&1; then
  echo "FAIL: discover one-shot exceeded 10s or exited non-zero"
  exit 1
fi
grep -q '^mission: ' "$out" || { echo "FAIL: discover frame missing mission"; exit 1; }
grep -q '^-- FRONTIER: recent capability finds (apply targets) --' "$out" \
  || { echo "FAIL: discover frame missing FRONTIER"; exit 1; }
mapfile -t rows < <(sed -n '/^-- FRONTIER: recent capability finds/,${/^  capability-/p;}' "$out")
[ "${#rows[@]}" -eq 2 ] || { echo "FAIL: expected two frontier rows, got ${#rows[@]}"; exit 1; }
case "${rows[0]}" in
  *capability-new-20260919.md) : ;;
  *) echo "FAIL: newest filename-date was not first: ${rows[0]}"; exit 1 ;;
esac
case "${rows[1]}" in
  *capability-mid-2026-09-18.md) : ;;
  *) echo "FAIL: second filename-date was not next: ${rows[1]}"; exit 1 ;;
esac
echo "PASS: discover one-shot handles 383 capability fixtures within 10s and preserves filename-date ordering"
fixture_chain="literature-fixture-20260925"
fixture_step="$fixture_chain/real-review"
fixture_review="$td/.mesh/knowledge/review-real-2026-09-25.md"
fixture_receipt="$td/.mesh/evidence/$fixture_chain/receipt.md"
mkdir -p "$td/.mesh/task-chains" "$(dirname "$fixture_receipt")"
printf 'Review: review-real-2026-09-25.md\n' >"$fixture_receipt"
receipt_sha="$(sha256sum "$fixture_receipt" | cut -d' ' -f1)"
cat >"$td/.mesh/task-chains/$fixture_chain.json" <<EOF
{"chain":"$fixture_chain","status":"complete","steps":[{"id":"$fixture_step","owner":"discover","status":"done","finished":"2026-09-25T20:52:34Z","artifact":"$fixture_receipt","artifact_sha256":"$receipt_sha"}]}
EOF
printf '<!-- mesh-literature-attempt-v1 chain=%s step=real-review -->\n' "$fixture_chain" >"$fixture_review"
printf '%s\n' '<!-- mesh-literature-attempt-v1 chain=literature-missing-20260925 step=missing-review -->' >"$td/.mesh/knowledge/review-unverified-2026-09-25.md"
bad_chain="literature-bad-hash-20260925"
bad_receipt="$td/.mesh/evidence/$bad_chain/receipt.md"
mkdir -p "$(dirname "$bad_receipt")"
printf 'Review: review-bad-hash-2026-09-25.md\n' >"$bad_receipt"
cat >"$td/.mesh/task-chains/$bad_chain.json" <<EOF
{"chain":"$bad_chain","status":"complete","steps":[{"id":"$bad_chain/bad-hash","owner":"discover","status":"done","finished":"2026-09-25T20:52:34Z","artifact":"$bad_receipt","artifact_sha256":"0000000000000000000000000000000000000000000000000000000000000000"}]}
EOF
printf '%s\n' "<!-- mesh-literature-attempt-v1 chain=$bad_chain step=bad-hash -->" >"$td/.mesh/knowledge/review-bad-hash-2026-09-25.md"
owner_chain="literature-other-owner-20260925"
owner_receipt="$td/.mesh/evidence/$owner_chain/receipt.md"
mkdir -p "$(dirname "$owner_receipt")"
printf 'Review: review-unowned-2026-09-25.md\n' >"$owner_receipt"
owner_sha="$(sha256sum "$owner_receipt" | cut -d' ' -f1)"
cat >"$td/.mesh/task-chains/$owner_chain.json" <<EOF
{"chain":"$owner_chain","status":"complete","steps":[{"id":"$owner_chain/unowned","owner":"health","status":"done","finished":"2026-09-25T20:52:34Z","artifact":"$owner_receipt","artifact_sha256":"$owner_sha"}]}
EOF
printf '%s\n' "<!-- mesh-literature-attempt-v1 chain=$owner_chain step=unowned -->" >"$td/.mesh/knowledge/review-unowned-2026-09-25.md"
printf '2026-09-25T20:52:34Z discover@mesh-home :: [done] literature-fixture-20260925/real-review: artifact=%s\n' "$fixture_receipt" >"$td/.mesh/chat.log"
cat >>"$td/.mesh/chat.log" <<'EOF'
2026-09-25T20:53:02Z health@mesh-home :: [task-ledger] health-decoy /steps/0/description=s:literature review-foo is still open
2026-09-25T20:53:09Z pub@mesh-home :: [task-ledger] pub-decoy /steps/0/description=s:review-literature prose does not prove an attempt
EOF
if ! timeout 10s env HOME="$td" MESH_DIR="$td/.mesh" MESH_DASH_FAST=1 \
    bash "$ROOT/scripts/mesh-dash" --once discover >"$out" 2>&1; then
  echo "FAIL: discover APPLY fixture exceeded 10s or exited non-zero"
  exit 1
fi
apply="$(sed -n '/^-- APPLY:/,/^-- FRONTIER:/p' "$out")"
printf '%s\n' "$apply"
grep -Fq 'review-real-2026-09-25' <<<"$apply" \
  || { echo "FAIL: source-backed literature attempt missing from APPLY"; exit 1; }
grep -Fq 'receipt=verified' <<<"$apply" \
  || { echo "FAIL: APPLY omitted receipt verification"; exit 1; }
grep -Eq 'age=[0-9]+[mhd]' <<<"$apply" \
  || { echo "FAIL: APPLY omitted measured attempt age"; exit 1; }
grep -Fq 'coverage: 1/4 receipt verified; 3 UNKNOWN' <<<"$apply" \
  || { echo "FAIL: APPLY omitted verified/UNKNOWN source coverage"; exit 1; }
if grep -Eq 'review-(bad-hash|unowned)-2026-09-25' <<<"$apply"; then
  echo "FAIL: invalid-hash or non-discover-owned marker was rendered as an attempt"
  exit 1
fi
if grep -Fq 'review-unverified-2026-09-25' <<<"$apply"; then
  echo "FAIL: unverified marker was rendered as an attempt"
  exit 1
fi
if grep -Eq 'health-decoy|pub-decoy' <<<"$apply"; then
  echo "FAIL: unrelated task-ledger prose leaked into APPLY"
  exit 1
fi
echo "PASS: discover APPLY shows only a receipt-backed attempt with age/coverage"
