#!/usr/bin/env bash
# mesh-patterns.sh — CANONICAL shared regexes for mind-pane state detection (the DRY source).
#
# WHY: independent detectors (mesh-channel-keepalive / mesh-session-watchdog / mesh-mind-state /
# mesh-generate) each encoded the SAME concept with their OWN regex → they drifted, one ended up
# wrong, the failure was SILENT — a mind walled by an UNRECOGNISED phrasing busy-waits instead of
# being shed (the exact quota+heat burn shedding exists to stop). See
# knowledge/inter-tool-inconsistency-canonical-definitions-2026-06-14.md. This is the ONE source:
# every detector sources it (with an inline fallback) so a NEW wall phrasing is added in ONE place
# and the whole mesh stays aligned.
#
# Three concepts → three DIFFERENT actions (do not conflate them):
#   MESH_RL_RE    quota / rate-limit / credits wall   → [mind-limited]: resets or provision,
#                                                        route work elsewhere (NOT operator-approvable)
#   MESH_AUTH_RE  login / oauth / context-full        → [mind-blocked]: a REAL steward action
#                                                        (re-login / clear context)
#   MESH_GATE_RE  approval dialog awaiting Y/N         → NEEDS-INPUT: an operator-approvable gate
#
#   . mesh-patterns.sh         # source → MESH_*_RE exported
#   mesh-patterns.sh --test    # assert representative strings classify correctly
#
# Consumers MUST apply these with `grep -iE` (case-insensitive — panes vary "Upgrade"/"upgrade")
# against a TIGHT window (the bottom few pane lines). That context, not the regex, is what
# suppresses quoted-in-output false positives.

# quota / rate-limit / credits wall → mind is UP for liveness but DEAD for work
MESH_RL_RE='hit your (usage|session) limit|usage limit reached|rate.?limit(ed|[ _.-]?(reach|exceed|error|hit|wall|block))|429|too many requests|quota.*(exhaust|exceed)|out of credits|purchase more credits|upgrade to (pro|team)|try again (at|later|in)|resets? (at )?[0-9]|overloaded'

# auth / context wall → a real steward action (not just route-elsewhere)
MESH_AUTH_RE='login.*required|oauth.*required|please (log|sign) ?in|authentication required|100% context (used|left)|context (full|exhausted)|/login'

# approval dialog awaiting Y/N → operator-approvable gate
MESH_GATE_RE='Do you want to (proceed|make this edit|create|delete|allow|run)|❯ 1\. Yes|Allow (once|this|always)|Always allow|Permission required|\(y/[Nn]\)[[:space:]]*$|press Enter to continue'

export MESH_RL_RE MESH_AUTH_RE MESH_GATE_RE

# ---- BLE device classification (shared by mesh-arrivals + mesh-ambient-clock) ----
#
# MESH_PERSON_RE  — KNOWN person-carried devices (operator + known items). Used for WEIGHTING
#                   and confidence (e.g. room-sense PRESENT_STRONG, operator-state NEARBY).
#                   NOT a gate for mesh-arrivals — use MESH_FIXED_RE exclusion there.
#   Mobicar = operator's car (arrival = operator coming home).
#
# MESH_FIXED_RE   — fixed APPLIANCE devices: BLE cycling = ambient social clock / weather proxy,
#                   definitionally NOT person-movement signals. EXCLUDED from mesh-arrivals,
#                   HARVESTED by mesh-ambient-clock. Includes TVs, ACs, smart scales, sensors.
#
# Consumer contract (agreed 2026-06-15):
#   mesh-arrivals:     EXCLUSION-based — tracks any real name NOT matching MESH_FIXED_RE.
#                      Unknown-but-named devices (DV8235, guest phones) ARE tracked: a stranger's
#                      device appearing IS a life event. MESH_PERSON_RE = confidence weighting only.
#   mesh-ambient-clock: INCLUSION-based — harvests MESH_FIXED_RE matches.
#   Unknown C04-/C05-/WSH86-: rotating serial-name churn — rejected by MESH_NOISE_RE (2026-06-15).
# Pattern agreement: genome controls this; both tools source mesh-patterns.sh.

MESH_PERSON_RE='JBL|AirPods|Galaxy Buds|Galaxy S|Galaxy A|Galaxy Note|Quest|Pixel|iPhone|Redmi|Armor|EDIFIER|Mobicar|Car Remote|Huawei|HUAWEI|Xiaomi Band|Mi Band'
# Bose Revolve SoundLink is a desk speaker broadcasting BLE 24/7 in standby — fixed appliance, not person-movement.
# Generic Bose removed from PERSON_RE; Bose headphones (QC, Earbuds) not yet observed, add if seen.
MESH_FIXED_RE='\[TV\]|MiTV-|Mi Box|Bluedroid TV|GR-AC_|MI SCALE|LYWSD|Vega BLE|GEELY_BT|CAR-BT|Bose Revolve|Bose SoundLink'
# MESH_NOISE_RE — rotating serial-number names: devices that embed their serial/ID into the BLE
# advertisement name and rotate it with the MAC. Looks like a "real name" (not a bare MAC, not SC-)
# but is per-device-instance noise that produces the same false [arrived]/[left] churn as random MACs.
# Observed: WSH86<serial> (wearable/scale), C04-<serial>, C05-<serial>, SBB01W12AL028100, ...
# Generic heuristic: 12+ chars, all uppercase+digits, no spaces/hyphens — serial/UUID-in-name
# regardless of prefix. Prefix list kept for backwards compat / C0x- with hyphens.
MESH_NOISE_RE='^(WSH86|C04-|C05-)[0-9A-Za-z]|^[A-Z][A-Z0-9]{11,}$'

export MESH_PERSON_RE MESH_FIXED_RE MESH_NOISE_RE

# Guard: run the test block ONLY when this file is EXECUTED directly — never when SOURCED.
# (A sourced lib inherits the caller's $1, so without this guard `consumer --test` would trip the
# lib's own test+exit and hijack the consumer's self-check.)
if [ "${1:-}" = --test ] && [ "${BASH_SOURCE[0]}" = "${0}" ]; then
  fail=0
  ck(){ # $1=regex $2=want(match|no) $3=string $4=label
    local got; if printf '%s' "$3" | grep -qiE "$1"; then got=match; else got=no; fi
    if [ "$got" = "$2" ]; then echo "  ok: $4"; else echo "  FAIL: $4 (got $got, want $2)"; fail=1; fi
  }
  echo "MESH_RL_RE — must MATCH every real wall phrasing:"
  ck "$MESH_RL_RE" match "You've hit your usage limit. Upgrade or try again at 6:03 PM." "usage-limit+try-again"
  ck "$MESH_RL_RE" match "· resets 6:03 PM"                  "resets-bullet"
  ck "$MESH_RL_RE" match "Error: 429 Too Many Requests"      "429+too-many"
  ck "$MESH_RL_RE" match "quota exceeded"                    "quota-exceeded"
  ck "$MESH_RL_RE" match "You're out of credits"            "out-of-credits"
  ck "$MESH_RL_RE" match "Purchase more credits to continue" "purchase-credits"
  ck "$MESH_RL_RE" match "Upgrade to Pro"                    "upgrade-pro (case-insensitive)"
  ck "$MESH_RL_RE" match "rate limit reached"                "rate-limit-reached"
  ck "$MESH_RL_RE" match "the mind is rate-limited"          "rate-limited-ed"
  ck "$MESH_RL_RE" match "rate_limit_error from the API"     "rate_limit_error"
  ck "$MESH_RL_RE" match "Overloaded"                        "overloaded"
  echo "MESH_RL_RE — must NOT match benign output:"
  ck "$MESH_RL_RE" no "✻ Crunched for 4m"                    "past-tense-crunched"
  ck "$MESH_RL_RE" no "editing rate_card.py"                 "rate_card-filename"
  ck "$MESH_RL_RE" no "spam fixed by rate-limit patch (1329d22)" "rate-limit-patch-prose"
  ck "$MESH_RL_RE" no "all systems nominal"                  "nominal"
  echo "MESH_AUTH_RE — login/context, distinct from quota:"
  ck "$MESH_AUTH_RE" match "Please login to continue"        "login-required"
  ck "$MESH_AUTH_RE" match "100% context used"               "context-full"
  ck "$MESH_AUTH_RE" no    "hit your usage limit"            "quota-is-NOT-auth"
  echo "MESH_GATE_RE — approval dialog, distinct from quota:"
  ck "$MESH_GATE_RE" match "Do you want to make this edit?"  "edit-gate"
  ck "$MESH_GATE_RE" match "❯ 1. Yes"                        "yes-option"
  ck "$MESH_GATE_RE" no    "hit your usage limit"            "quota-is-NOT-gate"
  [ "$fail" = 0 ] && { echo "smoke-test: ok"; exit 0; } || { echo "smoke-test: FAIL"; exit 1; }
fi
