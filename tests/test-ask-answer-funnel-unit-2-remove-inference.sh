#!/usr/bin/env bash
set -u
repo="$(cd "$(dirname "$0")/.." && pwd)"
lib="$repo/scripts/mesh-claim-shape.sh"
key='ask-answer-funnel-implementation-20260907/unit-2-remove-inference'
fail=0

claim_id_of(){ . "$lib"; }

source "$lib"
legacy_subject="$(claim_id_of "[done] $key: legacy subject")"
legacy_prose="$(claim_id_of "[done] NOVELTY: prose cites $key")"
explicit="$(claim_id_of "[done] $key: verified task:$key")"
[ "$legacy_subject" = UNKNOWN ] || { echo "FAIL shared legacy subject: got [$legacy_subject]"; fail=1; }
[ "$legacy_prose" = UNKNOWN ] || { echo "FAIL shared legacy prose: got [$legacy_prose]"; fail=1; }
[ "$explicit" = "$key" ] || { echo "FAIL shared explicit key: got [$explicit]"; fail=1; }

joined="$(bash "$repo/scripts/mesh-dispatch" --derive-ids \
  "2026-09-07T16:15:00Z tg@host :: [task] $key: mint task:$key" \
  "[done] $key: verified task:$key" 2>/dev/null)"
printf '%s\n' "$joined" | grep -qF "task=$key claim=$key" || {
  echo "FAIL dispatch explicit join: [$joined]"; fail=1;
}

exit "$fail"
