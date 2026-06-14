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
MESH_RL_RE='hit your (usage|session) limit|usage limit reached|rate.?limit|429|too many requests|quota.*(exhaust|exceed)|out of credits|purchase more credits|upgrade to (pro|team)|try again (at|later|in)|resets? (at )?[0-9]|overloaded'

# auth / context wall → a real steward action (not just route-elsewhere)
MESH_AUTH_RE='login.*required|oauth.*required|please (log|sign) ?in|authentication required|100% context (used|left)|context (full|exhausted)|/login'

# approval dialog awaiting Y/N → operator-approvable gate
MESH_GATE_RE='Do you want to (proceed|make this edit|create|delete|allow|run)|❯ 1\. Yes|Allow (once|this|always)|Always allow|Permission required|\(y/[Nn]\)[[:space:]]*$|press Enter to continue'

export MESH_RL_RE MESH_AUTH_RE MESH_GATE_RE

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
  ck "$MESH_RL_RE" match "rate limit reached"                "rate-limit"
  ck "$MESH_RL_RE" match "Overloaded"                        "overloaded"
  echo "MESH_RL_RE — must NOT match benign output:"
  ck "$MESH_RL_RE" no "✻ Crunched for 4m"                    "past-tense-crunched"
  ck "$MESH_RL_RE" no "editing rate_card.py"                 "rate_card-filename"
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
