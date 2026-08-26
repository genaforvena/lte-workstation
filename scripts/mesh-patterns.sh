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
# 429 needs HTTP/error CONTEXT, never the bare digits: a mind's own rendered statusline shows
# token cache-deltas like '+429' (and any larger number can contain 429), which satisfied the old
# bare '429' alternative purely by digit coincidence → a genuine 1800s pane shed off telemetry
# (live-reproduced 2026-07-22, mesh-home:sound; chat-review/rl-token-429-matches-statusline-telemetry).
# The 429 segment is deliberately BRACE-FREE ([^..]?x3, not {0,3}): consumers embed this string in
# their inline `: "${MESH_RL_RE:=...}"` fallbacks, where a literal `}` TRUNCATES the default — keep
# every copy textually identical so the fallbacks can't silently diverge.
MESH_RL_RE='hit your (usage|session) limit|usage limit reached|rate.?limit(ed|[ _.-]?(reach|exceed|error|hit|wall|block))|(error|status|code|http)[^0-9a-z]?[^0-9a-z]?[^0-9a-z]?429([^0-9]|$)|too many requests|quota.*(exhaust|exceed)|out of credits|purchase more credits|upgrade to (pro|team)|try again (at|later|in)|resets? (at )?[0-9]|overloaded'

# auth / context wall → a real steward action (not just route-elsewhere)
MESH_AUTH_RE='login.*required|oauth.*required|please (log|sign) ?in|authentication required|100% context (used|left)|context (full|exhausted)|/login'

# approval dialog awaiting Y/N → operator-approvable gate
MESH_GATE_RE='Do you want to (proceed|make this edit|create|delete|allow|run)|❯ 1\. Yes|Allow (once|this|always)|Always allow|Permission required|\(y/[Nn]\)[[:space:]]*$|press Enter to continue'

export MESH_RL_RE MESH_AUTH_RE MESH_GATE_RE

# STRONG quota phrases — an engine STOP banner uses these but a mind's natural-language prose almost
# never does → safe to match at ANY length. The rest of MESH_RL_RE (rate-limited/wall/overloaded/
# try-again/resets) ALSO appears when a mind writes ABOUT quotas in its own summary/task text, so
# those count only on a TERSE banner line. (operator FP 2026-06-15: a mind read RATE-LIMITED — and
# was SHED — off its own 150-char summary "rate-limit walls cascading" / a design doc literally
# containing "RATE-LIMITED".) Banner-SHAPE decides state, not keyword presence.
MESH_STRONG_RL_RE='hit your (usage|session) limit|usage limit reached|too many requests|(error|status|code|http)[^0-9a-z]?[^0-9a-z]?[^0-9a-z]?429([^0-9]|$)|out of credits|purchase more credits|upgrade to (pro|team)'
MESH_RL_BANNER_MAXLEN=100   # an engine banner is terse; a mind's prose is long-form
export MESH_STRONG_RL_RE MESH_RL_BANNER_MAXLEN
# rl_is_walled — stdin: the bottom pane lines. Returns 0 iff a GENUINE quota wall banner is present.
# Every shedder/classifier SHOULD use this (not a raw `grep MESH_RL_RE`) so a mind is never shed or
# mislabelled off its own prose. Drops input-box (prompt-glyph) lines; STRONG phrases match any
# length; broad RL tokens only on a line <= MESH_RL_BANNER_MAXLEN bytes.
rl_is_walled(){
  local txt; txt="$(cat)"
  # STRIP BOARD-ECHO lines FIRST. A mesh-chat board line (TIMESTAMP␠␠who@node␠␠::␠␠body, double-space
  # separators) shown in a mind's pane is the mesh's OWN chatter — NEVER a real TUI quota banner. A
  # free-pool mind doing board-reading work (e.g. opencode 'verify') echoes [mind-paused]/[mind-limited]
  # lines like "monthly usage limit reached, reset in 18-20 hours" that otherwise match MESH_RL_RE → it
  # is FALSELY shed off the mesh's own quota-chatter. (phaedra verify — free opencode pool, no real wall —
  # was shed ~hourly all afternoon 2026-06-15, then an 18h banner-reset MISPARSE of an echoed monthly
  # line pinned it dead 17h.) Real banners carry no timestamped who@node prefix, so this is always safe.
  txt="$(printf '%s\n' "$txt" | grep -vE '^[[:space:]]*[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:Z]+  [^ ]+  ::  ')"
  # STATE = MOST-RECENT signal. A live ready-footer or working spinner at the very bottom means any
  # quota banner ABOVE it is STALE — the mind recovered / moved on — so it is NOT currently walled.
  # (operator FP 2026-06-15: discover/sense recovered after their 2:20pm reset but the old "hit your
  # session limit" banner sat in scrollback above the live idle footer → falsely RATE-LIMITED + shed.)
  printf '%s\n' "$txt" | grep -vE '^[[:space:]]*$' | tail -4 \
    | grep -qE '⏵⏵ auto mode on|\? for shortcuts[^$]*agents|Use /skills to list|Ask anything|ctrl\+p commands|esc to interrupt|…[[:space:]]*\([0-9]|ing\.\.\.[[:space:]]*\([0-9]' && return 1
  printf '%s\n' "$txt" | grep -vE '^[[:space:]]*[❯›]' | grep -qiE "$MESH_STRONG_RL_RE" && return 0
  printf '%s\n' "$txt" | grep -vE '^[[:space:]]*[❯›]' \
    | awk -v m="$MESH_RL_BANNER_MAXLEN" 'length($0)<=m' | grep -qiE "$MESH_RL_RE" && return 0
  return 1
}

# ---- AUTH-DEAD (logged out) banner shape ----
#
# auth_is_dead — stdin: the bottom pane lines. Returns 0 iff a GENUINE logged-out ENGINE BANNER is
# present. Same discipline, same reason as rl_is_walled above, learned the same way: a bare substring
# scan turns a mind's PROSE into a verdict. Live 2026-08-18, minutes after channel-keepalive grew an
# AUTH-DEAD arm that KILLS and relaunches on this verdict: mesh-home:health — a perfectly healthy mind
# — was classified AUTH-DEAD off its own board message *about* the auth outage it had just survived
# ("…my window was 403 auth-dead … only the handoff's tail showing Please run /login · API Error:
# 403"). The arm's debounce does NOT save it: that text sits in the pane for many minutes, so two
# consecutive passes agree and a healthy mind gets killed with its context. The FP also hurts today,
# with no arm at all — mesh-tell REFUSES to send to an AUTH-DEAD pane and dispatch HOLDs on rc 9, so a
# mind is silenced by discussing an auth incident, exactly when the mesh needs it talking.
# TWO shape rules, both required, because either alone leaks:
#   TERSE  — an engine banner is short; the FP line was ~200 chars of narrative.
#   LEADS  — after stripping leading whitespace and any TUI result/bullet glyph (the glyph group is
#            OPTIONAL — a banner is often just indented, and requiring a glyph made the anchor
#            unreachable for those, i.e. the rule was carried entirely by TERSE), a real banner
#            BEGINS with the phrase
#            ('Please run /login · API Error: 403 Request not allowed'), while prose embeds it
#            mid-sentence. Anchoring is what survives a SHORT quote of the same string.
# Deliberately NOT reusing MESH_AUTH_RE (which includes '/login' bare and context-exhaustion tokens):
# that pattern answers "does a steward action appear anywhere in this text", a different question.
MESH_AUTHDEAD_RE='not logged in|please run /login|invalid api key'
MESH_AUTHDEAD_BANNER_MAXLEN=100   # an engine banner is terse; a mind's prose is long-form
export MESH_AUTHDEAD_RE MESH_AUTHDEAD_BANNER_MAXLEN
auth_is_dead(){
  local txt; txt="$(cat)"
  # board-echo strip, same rationale as rl_is_walled: the mesh's own chatter relayed into a pane
  # ("[mind-authdead] mesh-home:health is AUTH-DEAD…") is never that pane's engine banner.
  txt="$(printf '%s\n' "$txt" | grep -vE '^[[:space:]]*[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:Z]+  [^ ]+  ::  ')"
  printf '%s\n' "$txt" \
    | grep -vE '^[[:space:]]*[❯›]' \
    | sed -E 's/^[[:space:]]*([●⏺⎿│*•▪◆·>-]+[[:space:]]*)?//' \
    | awk -v m="$MESH_AUTHDEAD_BANNER_MAXLEN" 'length($0)<=m' \
    | grep -qiE "^($MESH_AUTHDEAD_RE)" && return 0
  return 1
}

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
MESH_FIXED_RE='\[TV\]|MiTV-|Mi Box|Bluedroid TV|GR-AC_|MI SCALE|LYWSD|Vega BLE|GEELY_BT|CAR-BT|Bose Revolve|Bose SoundLink|DRG[0-9]| [Тт][Вв]$|LED_BLE_'
# DRG[0-9] = Sercomm Digital Residential Gateway (e.g. DRG70-5AC65F) — a neighbor's home router,
# confirmed STABLE fixed appliance: 2 sightings, same real-OUI MAC 4C:E1:74:5A:C6:5F (2026-06-15).
# " [Тт][Вв]$" = a Cyrillic "<name> тв/ТВ" TV (e.g. "ваня тв") — a neighbor's TV, the bracketed-[TV]
# pattern misses these. STABLE fixed appliance: 2 sightings, same real-OUI MAC F0:A3:B2:DF:EB:83
# (2026-06-15). Anchored to a trailing " тв" word so it never matches mid-name; no person device is
# named "<x> тв".
# "LED_BLE_" = cheap RGB LED strip controller (e.g. LED_BLE_72284E6F) — fixed appliance, always
# powered, BLE broadcasts 24/7. First seen 2026-06-15.
# MESH_NOISE_RE — rotating serial-number names: devices that embed their serial/ID into the BLE
# advertisement name and rotate it with the MAC. Looks like a "real name" (not a bare MAC) but is
# per-device-instance noise producing false [arrived]/[left] churn.
# Observed: WSH86<serial> (wearable/scale), C04-/C05-<serial>, SBB01W12AL028100,
#   SC-<14-hex> (smart-sensor series, 180-345 sightings each, 2026-06-15),
#   J65172082 (9-char uppercase+digit serial, 2026-06-15).
# Three sub-patterns (consumers apply -i, so [A-Z] matches lowercase too — be precise):
#   (1) Known prefix+hyphen: WSH86/C04-/C05-/SC-<12-hex> — hyphens break the generic threshold
#   (2) Letter + 7+ digits only: ^[A-Z][0-9]{7,}$ — catches J65172082 (J+8 digits); safe: -i
#       can't false-positive on "Bluetooth" (has letter chars, not all digits after initial)
#   (3) Generic 12+ chars all-uppercase+digit: ^[A-Z][A-Z0-9]{11,}$ — catches SBB01W12AL028100
#       (16c); threshold kept at 12 because -i makes [A-Z0-9] match lowercase too (9c would
#       catch "Bluetooth" = B+luetooth at 9c)
MESH_NOISE_RE='^(WSH86|C04-|C05-)[0-9A-Za-z]|^SC-[0-9A-F]{12,}$|^[A-Z][0-9]{7,}$|^[A-Z][A-Z0-9]{11,}$'

export MESH_PERSON_RE MESH_FIXED_RE MESH_NOISE_RE

# ---- phone IP resolution (shared by mesh-phone-* tools) ----
#
# phone_reachable_ip — probe the phone body's candidate addresses for an SSH connection on
# PHONE_SSH_PORT. Returns the first reachable IP, sets PHONE_REACHABLE_IP (and PHONE_REACHABLE_VIA =
# which rung won). Exit 2 if the phone is unreachable on every path.
#
# Usage:
#   pip="$(phone_reachable_ip 2>/dev/null)" || exit 2
#
# A LADDER MUST BE MORE THAN ONE ADDRESS WEARING TWO LABELS (2026-08-20). Step 1 was labelled
# "Tailscale IP" but is whatever text the operator put in the MESH_NODES ts slot — and mesh-peer-addr
# itself falls back to a PHONE_LAN_IPS address when the ts addr does not ping, so BOTH rungs can
# resolve to the same string. That is not a hypothetical: for ~7 weeks the slot held
# `Redmi:u0_a380@192.168.8.146` (a workaround that outlived the tailscale outage it was written for),
# so the "2-path" ladder was ONE dead LAN address probed twice while the phone answered on
# 100.103.99.16 in 0.47s and every phone sense (prox/light/body-motion/tamper) rendered UNREACHABLE.
# Two rules follow:
#   (a) DEDUP — an address probed once is never probed again, whichever rung produced it. Duplicate
#       rungs are not redundancy; they are a fallback that silently is not one.
#   (b) The declared ts slot is OPERATOR TEXT and rots; tailscale's own peer table cannot. The LIVE
#       tailnet address of the phone peer is offered as its own candidate on every call (~5ms, local
#       API, measured), so a stale / LAN / re-issued slot costs one deduped entry instead of the whole
#       tailnet path. Querying unconditionally (rather than only when the slot is not 100.64/10) also
#       covers a slot that IS CGNAT-shaped but stale — same fault, same cost, since a slot that already
#       equals the live address dedups to zero extra probes.
# Rungs are ordered ts-slot -> ts-live -> lan and the winner is named in PHONE_REACHABLE_VIA, so a
# consumer can SEE the slot being wrong instead of inferring it.

# _mesh_is_cgnat <ip> → rc 0 if the address is in 100.64.0.0/10 (the tailnet range).
_mesh_is_cgnat() {
  local o2
  case "${1:-}" in 100.*) : ;; *) return 1 ;; esac
  o2="${1#100.}"; o2="${o2%%.*}"
  [ "$o2" -ge 64 ] 2>/dev/null && [ "$o2" -le 127 ] 2>/dev/null
}

# phone_ts_peer_ip — the phone body's LIVE tailnet address, read from tailscale itself, never from
# ~/.mesh/nodes. Peer matched by hostname/DNS-name regex (PHONE_TS_PEER_RE, default '^redmi' — the
# live HostName is "Redmi 10"). Prints nothing (rc 1) when tailscale/jq is absent or no peer matches;
# only a 100.64/10 address is ever returned, so a v6/other address cannot pose as the tailnet path.
phone_ts_peer_ip() {
  local re="${PHONE_TS_PEER_RE:-^redmi}" a
  command -v tailscale >/dev/null 2>&1 || return 1
  command -v jq >/dev/null 2>&1 || return 1
  while read -r a; do
    _mesh_is_cgnat "$a" && { printf '%s\n' "$a"; return 0; }
  done < <(timeout 3 tailscale status --json 2>/dev/null | jq -r --arg re "$re" '
      .Peer[]? | select((((.HostName // "") | ascii_downcase) | test($re))
                     or (((.DNSName  // "") | ascii_downcase) | test($re)))
      | .TailscaleIPs[]?' 2>/dev/null)
  return 1
}

# phone_reach_candidates — the DEDUPED probe ladder, one "<rung> <ip>" line per candidate. Split out
# of the prober so the ladder's SHAPE is gateable without an SSH round trip (--test drives this off a
# stubbed mesh-peer-addr + tailscale, i.e. the real assembly code, never an injected candidate list).
phone_reach_candidates() {
  local slot live ip seen=" "
  _phone_cand_emit() {  # <rung> <ip> — dedup is here and nowhere else
    [ -n "${2:-}" ] || return 0
    case "$seen" in *" $2 "*) return 0 ;; esac
    seen+="$2 "
    printf '%s %s\n' "$1" "$2"
  }
  slot="$(mesh-peer-addr Redmi 2>/dev/null || mesh-peer-addr redmi 2>/dev/null || true)"
  slot="${slot##*$'\n'}"          # mesh-peer-addr's notes go to stderr; take the address line only
  _phone_cand_emit ts-slot "$slot"
  live="$(phone_ts_peer_ip 2>/dev/null || true)"
  _phone_cand_emit ts-live "$live"
  for ip in ${PHONE_LAN_IPS:-}; do _phone_cand_emit lan "$ip"; done
}

 phone_reachable_ip() {
   local port="${PHONE_SSH_PORT:-8022}"
   local puser="${PHONE_USER:-u0_a380}"
   local rung ip slot=""
   # On failure, classify WHY (chat-review/Redmi-body-degraded, 2026-07-24): a silent KEY ROTATION
   # (phone UP, sshd answered, our pubkey untrusted) read identically to a genuinely-OFFLINE phone
   # for 8 days of degrade logs — zero signal to tell 'gone' from 'key rotated'. PHONE_REACH_FAIL:
   #   offline (default)  = no route / timeout / refused (network-level: phone not answering)
   #   auth-rejected      = sshd ANSWERED + rejected our key (phone UP; the key is the problem)
   PHONE_REACH_FAIL=offline; export PHONE_REACH_FAIL
   PHONE_REACHABLE_VIA=""; export PHONE_REACHABLE_VIA
   _probe() {  # <ip> → rc 0 reachable; on failure sets PHONE_REACH_FAIL + PHONE_REACH_LAST_IP
     PHONE_REACH_LAST_IP="$1"; export PHONE_REACH_LAST_IP
     local err rc
     err="$(timeout 4 ssh -p "$port" -o BatchMode=yes -o ConnectTimeout=3 \
       -o StrictHostKeyChecking=accept-new "${puser}@${1}" 'echo ok' </dev/null 2>&1 >/dev/null)"
     rc=$?
     [ "$rc" = 0 ] && return 0
     printf '%s' "$err" | grep -qi 'Permission denied' && PHONE_REACH_FAIL=auth-rejected
     return 1
   }
   while read -r rung ip; do
     [ -n "$ip" ] || continue
     [ "$rung" = ts-slot ] && slot="$ip"
     if _probe "$ip"; then
       PHONE_REACHABLE_IP="$ip"; PHONE_REACHABLE_VIA="$rung"
       export PHONE_REACHABLE_IP PHONE_REACHABLE_VIA
       # LOUD, and only in the case that is a CONFIG FAULT: the live tailnet address answered while a
       # non-tailnet slot did not. Silence here is exactly how the LAN-in-the-ts-slot workaround
       # outlived its outage for 7 weeks. stderr, so it cannot corrupt a $(...) capture.
       if [ "$rung" = ts-live ] && [ -n "$slot" ] && ! _mesh_is_cgnat "$slot"; then
         printf 'phone_reachable_ip: MESH_NODES ts slot for Redmi is %s (not a 100.64/10 tailnet addr) and did not answer; live tailnet %s did — fix ~/.mesh/nodes\n' "$slot" "$ip" >&2
       fi
       printf '%s\n' "$ip"; return 0
     fi
   done < <(phone_reach_candidates)
   return 2
 }

# ---- outdoor-weather honest-fusion (shared by mesh-therm-watch / mesh-mind-control / mesh-node-care) ----
#
# weather-consumers-phase2 (2026-07-07): mesh-weather (hourly cadence) writes 'OK <ts> now_c=..
# today_max_c=.. peak_hour=<h> thermal_day=<0|1> thresh_c=..' to .weather-state; a BLIND fetch
# failure leaves the file UNTOUCHED (offline is not the same claim as a mild day), so staleness is
# judged by MTIME, not by content. Every consumer of this sense goes through weather_field (never
# greps the state file directly) so an absent/stale sense degrades HONESTLY: UNKNOWN, never a
# silently-fabricated "not a thermal day" or a stale outdoor reading passed off as current — the
# same discipline as every other honest-fusion sense in this mesh (an unreachable input renders
# UNKNOWN, it never assumes the calm case).
WEATHER_STATE_TTL="${MESH_WEATHER_STATE_TTL:-10800}"   # 3h: tolerates one missed hourly mesh-weather cycle
export WEATHER_STATE_TTL
#
# weather_field <field> [state-file] → prints the field's value, or UNKNOWN if the state file is
# missing/unreadable/stale. <field> is one of thermal_day|peak_hour|now_c|today_max_c|thresh_c.
weather_field() {
  local field="$1" f="${2:-$HOME/.mesh/.weather-state}" age v
  [ -r "$f" ] || { echo UNKNOWN; return; }
  age=$(( $(date +%s) - $(stat -c %Y "$f" 2>/dev/null || echo 0) ))
  [ "$age" -lt "$WEATHER_STATE_TTL" ] 2>/dev/null || { echo UNKNOWN; return; }
  v="$(grep -oE "${field}=[^ ]+" "$f" 2>/dev/null | head -1 | cut -d= -f2)"
  printf '%s\n' "${v:-UNKNOWN}"
}

# ---- shared-board cross-node dedup (extracted 2026-07-08 — see LITERATURE note below) ----
#
# LITERATURE (live review, 2026-07-08): Kumar, Clune, Lehman & Stanley, "Questioning
# Representational Optimism in Deep Learning: The Fractured Entangled Representation Hypothesis"
# (arXiv:2505.11581, 2025). FER names a failure mode of incremental, gradient-style optimization:
# a single concept ends up re-encoded as multiple disconnected, slightly-divergent copies
# ("fractured") instead of one reusable modular unit — versus the "unified factored representation"
# open-ended/evolutionary search tends to produce. WE APPLIED THIS MESH'S OWN REMEDY (this file,
# built 2026-06-14 for the rate-limit-regex case — see the file header) TOO LOOSELY: it fixed ONE
# instance of the pattern and was never generalized as a standing rule, so the SAME anti-pattern
# re-grew somewhere this file doesn't cover. Concretely: "check the shared mesh-chat board for
# another node's matching post within a cooldown window before minting my own" is ONE concept, but
# it now has independently-hand-rolled copies in scan_orphans (mesh-mind-control, 04a98cf),
# mesh-sweep-rollcall-proposes (d357653, exact-substring match), and — freshly written the same day
# this was noticed — mesh-criticality's alarm_emit() (timestamp-window match). Three fractured,
# slightly-divergent encodings of one idea, exactly the FER symptom, not three genuinely different
# problems. board_recent_ts_within() below is the ONE reusable primitive; mesh-criticality has been
# migrated onto it (lowest-risk instance — written same-session, fully understood). scan_orphans and
# sweep-rollcall-proposes are NOT yet migrated (each has its own battle-tested match semantics —
# exact-substring vs timestamp-window — worth reconciling deliberately, not folded in blind); flagged
# here rather than silently left, per the mesh's own no-silent-caps convention.
#
# board_recent_ts_within — $1=board-log-path $2=literal marker (grep -F, NOT a regex) $3=window_s
# [$4=now_epoch, default now] → prints the epoch of the most recent matching line IF one exists
# within the window; exit 0. Otherwise prints nothing, exit 1. Read-only / no side effects — the
# caller decides what "found" means (adopt the timestamp into local cooldown state, skip a post,
# log-only, etc).
board_recent_ts_within(){
  local board="$1" marker="$2" window="$3" now="${4:-$(date +%s)}"
  [ -r "$board" ] || return 1
  local ts epoch
  ts="$(grep -F -- "$marker" "$board" 2>/dev/null | tail -1 | awk '{print $1}')"
  [ -n "$ts" ] || return 1
  epoch="$(date -u -d "$ts" +%s 2>/dev/null)" || return 1
  [ $(( now - epoch )) -lt "$window" ] || return 1
  printf '%s' "$epoch"
}

# board_presync — $1=stamp_file $2=min_interval_s $3=timeout_s $4=sync_cmd (may be empty to disable)
# Pulls fresh cross-node gossip synchronously, rate-limited by $stamp_file so repeat calls within
# min_interval_s no-op, hard-timeout so a slow/partitioned peer can never wedge the caller. Call this
# immediately before board_recent_ts_within (or any other read of the local gossiped board) whenever
# the caller is about to trust that board for cross-node dedup — extracted from mesh-mind-control's
# dispatch() presync gate (538b3f1, chat-review/dispatch-gossip-lag-recur 2026-07-09), which closed a
# live double-dispatch (two nodes minted the same slug 4s apart because the periodic mesh-chat-sync
# gossip cron — up to ~25min stale — hadn't yet pulled the peer's fresh post). That fix stayed local
# to dispatch(); mesh-fawxible-watch/mesh-criticality/mesh-session-watchdog hit the identical gap
# (mesh-fawxible-watch double-posted fawxible-review-b0aa8ba from 2 nodes 0s apart, 2026-07-09T21:17:03Z)
# with no shared remedy — chat-review/patterns-presync-gate-shared(-relanded).
# No side effects beyond running $sync_cmd and touching $stamp_file; caller decides what "synced" means.
board_presync(){
  local stamp="$1" min_interval="${2:-300}" timeout_s="${3:-25}" cmd="$4"
  [ -n "$cmd" ] || return 0
  local now age
  now=$(date +%s)
  age=999999
  [ -f "$stamp" ] && age=$(( now - $(stat -c %Y "$stamp" 2>/dev/null || echo 0) ))
  if [ "$age" -ge "$min_interval" ]; then
    timeout "$timeout_s" $cmd >/dev/null 2>&1 || true
    touch "$stamp" 2>/dev/null || true
  fi
}

# mesh_is_minter — $1=board-log-path [$2=window_s, default 86400] → true (exit 0) iff THIS host is
# the elected minter: the lexically-lowest hostname that posted ANY line to the board within the
# window. Origin: mesh-sweep-rollcall-proposes' _rollcall_is_minter (6b3281b, chat-review/
# rollcallprop-dedup-race-persists) — closes the case board_recent_ts_within can't: a genuine
# same-tick collision where every racing host's check-then-act grep sees an empty/no-match board
# (nobody has posted yet) and all fall through to mint. Election converges concurrent same-cadence
# cron ticks across mind nodes onto ONE poster instead of racing; board_recent_ts_within stays the
# first-line (staggered-race) defense, this is the true-simultaneity guard behind it.
# NOT YET migrated: mesh-sweep-rollcall-proposes keeps its own copy (own battle-tested env-var
# names, MESH_ROLLCALL_HOSTNAME/MESH_ROLLCALL_MINTER) — flagged here rather than silently left, same
# as board_recent_ts_within above. mesh-criticality is the first consumer of this shared copy.
# MESH_MINTER_HOSTNAME overrides the real hostname (hermetic multi-host test fixtures);
# MESH_MINTER_PIN pins an explicit override, skipping election entirely.
mesh_is_minter(){
  local log="$1" window="${2:-86400}" host="${MESH_MINTER_HOSTNAME:-$(hostname)}" minter="${MESH_MINTER_PIN:-}"
  [ -n "$minter" ] && { [ "$host" = "$minter" ]; return; }
  [ -r "$log" ] || return 0   # nothing to elect from -> mint anyway (racy edge, never a silent drop)
  local cutoff now_e
  now_e="$(date +%s)"
  cutoff="$(date -u -d "@$(( now_e - window ))" +%FT%TZ 2>/dev/null)" || cutoff=""
  minter="$(awk -v cut="$cutoff" '$1 >= cut { n = split($2, a, "@"); if (n > 1) print a[n] }' "$log" 2>/dev/null | sort -u | head -1)"
  [ -n "$minter" ] || return 0
  [ "$host" = "$minter" ]
}

# ---- MISSED-BEACON grammar (shared by mesh-wifi-rf / -quality) ----
#
# /proc/net/wireless COLUMN 11 ("Missed beacon") IS DEAD ZERO ON rtw88, and both parses of it were
# CORRECT — the column is the right column, the SOURCE is empty. Measured 2026-08-26 on this node's
# sole uplink (rtw_8822bu): col 11 read 0 in 3574 of 3574 recorded readings across two senses, and
# at one instant, in one association, `iw dev <if> station dump` read `beacon loss: 9` while
# /proc col 11 read 0 and mesh-wifi-rf printed `EXCELLENT ... beacon_missed=0`.
#
# The field is ALARM-NAMED — mesh-wifi-rf documents it as "AP unreachable ticks" and
# mesh-wifi-quality ships it as discard_beacon_missed — so a consumer reading it for
# AP-unreachability got a PERMANENT ALL-CLEAR on the one link everything here rides.
# [[a-silent-fallback-turns-a-failure-into-a-plausible-constant]]
#
# THE TRAP THAT MAKES THIS EASY TO GET WRONG TWICE: neighbouring column 10 ("misc") DOES track
# nl80211's `rx drop misc` exactly (950 vs 951 in the same read), so the block LOOKS alive and a
# careless check grabs the working neighbour and concludes the parse is fine.
#
# NO DRIVER ALLOWLIST. "rtw88 does not fill it" is an exclusion list whose failure direction is
# SILENCE — the next driver that also leaves it empty is simply not on the list and inherits the
# false all-clear. [[an-exclusion-allowlist-fails-toward-silence-so-invert-the-polarity]]
# Instead: ASK THE SURFACE THAT CLAIMS TO KNOW, and publish WHICH one answered.
#
#   nl80211 answered            -> that value, src=nl80211        (authoritative)
#   nl80211 silent, proc  > 0   -> that value, src=proc           (the counter is demonstrably live)
#   nl80211 silent, proc == 0   -> na,         src=none           (0 here is INDISTINGUISHABLE from
#                                                                  a driver that never fills it)
#
# The third line is the whole point: a proc-sourced zero is not a reading, it is the absence of one,
# and it must never wear the alarm field's name. [[a-blindness-sentinel-fused-as-a-reading]]
BEACON_GRAMMAR_SRC="mesh-patterns.sh"
export BEACON_GRAMMAR_SRC
beacon_missed_read() { # <iface> <proc-col-11> -> "<value|na> <nl80211|proc|none>"
  local iface="${1:-}" proc_v="${2:-}" nl=""
  case "$proc_v" in ''|*[!0-9]*) proc_v="";; esac
  if [ -n "$iface" ] && command -v iw >/dev/null 2>&1; then
    # `beacon loss` is per-STATION, so it lives in `station dump`, never in `link`. Take the FIRST
    # match: a managed interface has one AP station, and a stray second would otherwise silently
    # concatenate into a number no counter ever held.
    nl="$(iw dev "$iface" station dump 2>/dev/null \
          | awk -F: '/beacon loss:/{gsub(/[^0-9]/,"",$2); if ($2 != "") {print $2; exit}}')"
    case "$nl" in ''|*[!0-9]*) nl="";; esac
  fi
  if [ -n "$nl" ]; then printf '%s nl80211\n' "$nl"; return 0; fi
  if [ -n "$proc_v" ] && [ "$proc_v" -gt 0 ] 2>/dev/null; then printf '%s proc\n' "$proc_v"; return 0; fi
  printf 'na none\n'
}

# ---- RSSI sentinel grammar (shared by mesh-wifi-mimo / -quality / -rf / -contention) ----
#
# ONE blindness, TWO renderings, and until 2026-08-24 FOUR private copies of the predicate, no two
# of which agreed. When this node's uplink (RTL8822BU/rtw_8822bu, the sole uplink) goes momentarily
# blind, nl80211 renders the instant as `signal: 0 dBm` and /proc/net/wireless renders the SAME
# instant as `level -256.` — discover measured 11/90 samples railed with coincident=11, proc-only=0,
# iw-only=0, and health replicated it with a read-proc/read-iw/read-proc bracket that rules the
# inter-read gap out by construction: 16 of 16 coincident among the 79 stable brackets.
#
# Why no existing guard caught the nl80211 half: mesh-wifi-quality/-rf's `level_valid` is a
# MAGNITUDE bound (`> -200`) and it works only because -256 is out of range. **0 dBm is IN range,
# well-formed and MAXIMAL** — no plausibility bound rejects it, and the rail is ALWAYS toward
# perfect (valid band here -54..-43, so the rail is +43..+54 dB in the flattering direction).
# mesh-wifi-contention's `dbm()` rejected 0 but not -256; mesh-wifi-mimo had no guard at all and
# published `signal=0dBm` into a sense whose whole discriminator is "NSS collapsed WHILE signal
# held steady" — a rail coinciding with a real NSS collapse manufactures the most emphatic possible
# instance of that inference out of a blind moment.
#
# So: the two sentinels are ONE concept (RAILED) and belong to ONE predicate, exactly as
# MESH_RL_RE above exists because four detectors of one concept drifted apart in private.
#
# rssi_valid is a SENTINEL test, NOT a plausibility bound. It rejects only what the driver emits
# when it has no reading: >= 0 (nl80211's blind instant, and a receiver RSSI is never positive) and
# <= RSSI_MIN_DBM (/proc's -256). It deliberately does NOT bound the plausible band — a bound is
# what failed here, and health measured why a bound cannot be the fix: the rail flips INSIDE the
# gap between two adjacent reads (22 of 100 brackets had proc CHANGE across one intervening iw
# call, a few milliseconds), so a single sample is untrustworthy on its face and even a
# cross-surface agreement check is not a validity proof — it just has a ~78% chance of catching the
# same instant. What survives is a MEDIAN over a burst. That is rssi_burst, and it is why every
# consumer publishes its BLIND FRACTION beside the value rather than a quietly cleaned-up number.
RSSI_MIN_DBM="${MESH_RSSI_MIN_DBM:--200}"
# Which copy of the grammar is live is a CHECKABLE FACT, not a comment: every consumer carries an
# inline fallback for a node without this lib, and "the fallback is the same predicate, never a
# laxer one" is exactly the kind of claim that rots into a comment nobody re-derives. Consumers set
# this to "inline" in their fallback branch and gate BOTH copies against the same sentinels.
RSSI_GRAMMAR_SRC="mesh-patterns.sh"
export RSSI_MIN_DBM RSSI_GRAMMAR_SRC
rssi_valid() {  # <value> -> 0 iff a real dBm reading (tolerates a trailing '.' or ' dBm')
  local v="${1:-}"
  v="${v% dBm}"; v="${v%dBm}"; v="${v%.}"
  case "$v" in ''|-|NA|na|n/a) return 1;; esac
  case "$v" in *[!0-9.-]*) return 1;; esac
  case "$v" in *.*) v="${v%%.*}";; esac       # -49.5 -> -49 (integer compare; dBm resolution is 1)
  case "$v" in ''|-) return 1;; esac
  [ "$v" -lt 0 ] 2>/dev/null || return 1      # 0 dBm = nl80211 blind instant; positive is not an RSSI
  [ "$v" -gt "$RSSI_MIN_DBM" ] 2>/dev/null    # -256 = /proc driver-not-ready sentinel
}
# rssi_burst — stdin: one candidate value per line (as read, sentinels included).
# stdout: "<median|na> <valid> <total>". Median of the VALID samples only; "na" when none are
# valid, NEVER 0 and never a silently carried last value. Lower median on an even count (a dBm
# reading is an integer; averaging two would mint a value no sample ever had).
rssi_burst() {
  awk -v minv="$RSSI_MIN_DBM" '
    { total++
      v = $0
      sub(/ ?dBm$/, "", v); sub(/\.$/, "", v)
      if (v !~ /^-?[0-9]+(\.[0-9]+)?$/) next
      n = int(v + 0)
      if (n >= 0 || n <= minv) next          # same predicate as rssi_valid, one grammar
      vals[++k] = n
    }
    END {
      if (k == 0) { printf "na %d %d\n", 0, total; exit }
      asort_n(vals, k)
      printf "%d %d %d\n", vals[int((k+1)/2)], k, total
    }
    function asort_n(a, n,   i, j, t) {       # tiny insertion sort: k is a burst size, not a corpus
      for (i = 2; i <= n; i++) { t = a[i]; j = i - 1
        while (j >= 1 && a[j] > t) { a[j+1] = a[j]; j-- }
        a[j+1] = t }
    }'
}

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
  ck "$MESH_RL_RE" match "HTTP 429"                           "http-429"
  ck "$MESH_RL_RE" match "Request failed with status code 429" "status-code-429"
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
  ck "$MESH_RL_RE" no "+429"                                 "bare-cache-delta-429 (statusline telemetry)"
  ck "$MESH_RL_RE" no "tok 14290 cached"                     "429-inside-larger-number"
  ck "$MESH_STRONG_RL_RE" no "+429"                          "STRONG: bare-cache-delta-429"
  echo "MESH_AUTH_RE — login/context, distinct from quota:"
  ck "$MESH_AUTH_RE" match "Please login to continue"        "login-required"
  ck "$MESH_AUTH_RE" match "100% context used"               "context-full"
  ck "$MESH_AUTH_RE" no    "hit your usage limit"            "quota-is-NOT-auth"
  echo "MESH_GATE_RE — approval dialog, distinct from quota:"
  ck "$MESH_GATE_RE" match "Do you want to make this edit?"  "edit-gate"
  ck "$MESH_GATE_RE" match "❯ 1. Yes"                        "yes-option"
  ck "$MESH_GATE_RE" no    "hit your usage limit"            "quota-is-NOT-gate"
  echo "MESH_FIXED_RE — fixed appliances (EXCLUDED from arrivals, INCLUDED by ambient-clock):"
  ck "$MESH_FIXED_RE" match "[TV] Samsung 5 Series (40)"  "TV-bracket"
  ck "$MESH_FIXED_RE" match "MiTV-MZTU1"                  "MiTV"
  ck "$MESH_FIXED_RE" match "Bose Revolve SoundLink"       "Bose-desk-speaker"
  ck "$MESH_FIXED_RE" match "DRG70-5AC65F"                "Sercomm-DRG-gateway"
  ck "$MESH_FIXED_RE" match "ваня тв"                     "cyrillic-TV-suffix"
  ck "$MESH_FIXED_RE" match "Гостиная ТВ"                 "cyrillic-TV-uppercase"
  ck "$MESH_FIXED_RE" match "LED_BLE_72284E6F"             "LED-strip-controller-fixed"
  ck "$MESH_FIXED_RE" no    "iPhone 13"                   "person-phone-NOT-fixed"
  ck "$MESH_FIXED_RE" no    "Quest 3"                     "person-headset-NOT-fixed"
  ck "$MESH_FIXED_RE" no    "Светлана"                    "cyrillic-name-NOT-fixed (no тв suffix)"
  echo "MESH_NOISE_RE — rotating serial-name churn (ignored):"
  ck "$MESH_NOISE_RE" match "WSH86ABC123"                  "WSH86-noise"
  ck "$MESH_NOISE_RE" match "ABCDEFGHIJKLM"                "13-char-allcaps-serial"
  ck "$MESH_NOISE_RE" match "J65172082"                    "9-char-serial (2026-06-15)"
  ck "$MESH_NOISE_RE" match "SC-31142100007F1F"            "SC-hex-sensor (2026-06-15)"
  ck "$MESH_NOISE_RE" match "SC-31150200034BED"            "SC-hex-sensor-variant"
  ck "$MESH_NOISE_RE" no    "DRG70-5AC65F"                "DRG-not-noise (in FIXED_RE)"
  ck "$MESH_NOISE_RE" no    "Bluetooth"                   "Bluetooth-not-noise (lowercase)"
  ck "$MESH_NOISE_RE" no    "Samsung 5 Series (40)"       "TV-not-noise"
  ck "$MESH_NOISE_RE" no    "DV8235"                      "6-char-model-not-noise (too short)"
  echo "rl_is_walled — banner-shape gate (a mind is never shed off its own prose):"
  ckw(){ local want="$1" label="$2" txt="$3"; if printf '%s\n' "$txt" | rl_is_walled; then got=walled; else got=clear; fi
         if [ "$got" = "$want" ]; then echo "  ok: $label ($got)"; else echo "  FAIL: $label want=$want got=$got"; fail=1; fi; }
  ckw walled "session-limit banner"   "⎿  You've hit your session limit · resets 2:20pm (Europe/Moscow)"
  ckw walled "usage-limit banner"     "■ You've hit your usage limit. Upgrade to Pro to continue."
  ckw walled "terse rate-limit"       "API request failed: rate limit exceeded"
  ckw clear  "summary-prose quota"    "Noted but no action: rate-limit walls cascading (09:56-10:05) are designed thermal/quota backpressure via channel-keepalive, not a fault — just fewer hands during cooldown."
  ckw clear  "task-text about RL"     "on a rate-limited claude worker auto-re-routes to an idle FREE-engine worker. Propose the trigger (mind-state RATE-LIMITED → re-dispatch its open task) plus de-dup."
  ckw clear  "input-box quota draft"  "❯ should we retry after we hit the usage limit?"
  ckw clear  "statusline cache-delta +429" "main · 41% ctx · +429 cache tokens"
  ckw clear  "STALE banner + idle footer" "$(printf '⎿  You'"'"'ve hit your session limit · resets 2:20pm (Europe/Moscow)\n   /upgrade to increase your usage limit.\n✻ Worked for 1s\n❯ \n  ⏵⏵ auto mode on (shift+tab to cycle) · ← for agents')"
  ckw clear  "STALE banner + spinner"     "$(printf '⎿  You'"'"'ve hit your session limit · resets 2:20pm\n✻ Cogitating… (12s · esc to interrupt)')"
  echo "auth_is_dead — banner-shape gate (a mind is never killed or silenced off its own prose):"
  cka(){ local want="$1" label="$2" txt="$3"; if printf '%s\n' "$txt" | auth_is_dead; then got=dead; else got=clear; fi
         if [ "$got" = "$want" ]; then echo "  ok: $label ($got)"; else echo "  FAIL: $label want=$want got=$got"; fail=1; fi; }
  cka dead  "403 logged-out banner"   "● Please run /login · API Error: 403 Request not allowed"
  cka dead  "not-logged-in banner"    "⎿  Not logged in · Please run /login"
  cka dead  "indented banner, no glyph" "   Please run /login"
  cka dead  "invalid api key banner"  "Invalid API key · Please run /login"
  # the live 2026-08-18 FP verbatim: mesh-home:health acknowledging the outage it had just survived
  cka clear "prose quoting the banner" "On (2): acknowledged, my window was 403 auth-dead - I have no record of the interval, only the handoff tail showing Please run /login · API Error: 403. Thanks for the relaunch."
  # one fixture per RULE, so neither rule can be deleted while the other silently covers for it
  cka clear "long line that LEADS with the phrase (TERSE rule)" "Please run /login was what the pane showed for seven hours, and I am quoting the banner verbatim here so a future reader can match the exact string."
  cka clear "short mid-sentence quote (LEADS rule)"             "handoff tail showed Please run /login"
  cka clear "input-box draft about /login"                      "❯ how do I fix Not logged in · Please run /login on phaedra?"
  cka clear "board echo of an authdead post"                    "2026-08-18T20:16:18Z  channel-keepalive@mesh-home  ::  [mind-authdead] mesh-home:health is AUTH-DEAD - Please run /login"
  echo "weather_field — honest-fusion: fresh state parses, stale/absent/malformed renders UNKNOWN:"
  _wtd="$(mktemp -d)"
  printf 'OK 2026-07-07T10:00:00Z now_c=25.1 today_max_c=31.5 peak_hour=15 thermal_day=1 thresh_c=28\n' > "$_wtd/fresh"
  ck2(){ local got="$1" want="$2" label="$3"; if [ "$got" = "$want" ]; then echo "  ok: $label"; else echo "  FAIL: $label (got '$got' want '$want')"; fail=1; fi; }
  ck2 "$(weather_field thermal_day "$_wtd/fresh")"  1    "fresh state, thermal_day"
  ck2 "$(weather_field peak_hour   "$_wtd/fresh")"  15   "fresh state, peak_hour"
  ck2 "$(weather_field today_max_c "$_wtd/fresh")"  31.5 "fresh state, today_max_c"
  touch -d '-4 hours' "$_wtd/fresh"   # older than WEATHER_STATE_TTL (default 3h) → stale
  ck2 "$(weather_field thermal_day "$_wtd/fresh")"  UNKNOWN "stale state (>TTL) → UNKNOWN, never the last-good value"
  ck2 "$(weather_field thermal_day "$_wtd/no-such-file")" UNKNOWN "absent state → UNKNOWN"
  printf 'mesh-weather: BLIND (open-meteo fetch/parse failed)\n' > "$_wtd/blind"
  ck2 "$(weather_field thermal_day "$_wtd/blind")" UNKNOWN "BLIND/malformed content → UNKNOWN, never a fabricated 0"
  rm -rf "$_wtd"
  echo "board_recent_ts_within — shared cross-node dedup primitive (FER extraction, 2026-07-08):"
  _brd="$(mktemp -d)"
  _bts0="$(date -u -d '2026-07-08T12:00:00Z' +%s)"
  printf '2026-07-08T12:00:00Z  a@host  ::  [alert] widget: SUPERCRITICAL\n' > "$_brd/board"
  bts="$(board_recent_ts_within "$_brd/board" '[alert] widget: SUPERCRITICAL' 3600 "$((_bts0+1800))")"
  ck2 "$bts" "$_bts0" "match within window (30min later, 1h window) → epoch printed"
  board_recent_ts_within "$_brd/board" '[alert] widget: SUPERCRITICAL' 3600 "$((_bts0+1800))" >/dev/null
  ck2 "$?" 0 "match within window → exit 0"
  board_recent_ts_within "$_brd/board" '[alert] widget: SUPERCRITICAL' 3600 "$((_bts0+7200))" >/dev/null
  ck2 "$?" 1 "match but OUTSIDE window (2h later, 1h window) → exit 1"
  board_recent_ts_within "$_brd/board" '[alert] nomatch: anything' 3600 "$((_bts0+1800))" >/dev/null
  ck2 "$?" 1 "no matching marker → exit 1"
  board_recent_ts_within "$_brd/no-such-file" '[alert] widget: SUPERCRITICAL' 3600 "$((_bts0+1800))" >/dev/null
  ck2 "$?" 1 "unreadable board → exit 1, never a false match"
  rm -rf "$_brd"
  echo "mesh_is_minter — single-minter election, true-simultaneity guard:"
  _mnd="$(mktemp -d)"
  # timestamps RELATIVE to test-run time (was hardcoded 2026-07-09T02:00:00Z..:02Z, which aged out of
  # mesh_is_minter's own 86400s window as wall-clock advanced → host-b/c wrongly "mint anyway" → FAIL
  # on any run >~24h after the fixed date; chat-review/patterns-minter-test-date-drift 2026-07-10).
  _mn_e="$(date +%s)"
  printf '%s  a@host-a  ::  hello\n%s  b@host-b  ::  hello\n%s  c@host-c  ::  hello\n' \
    "$(date -u -d "@$((_mn_e-30))" +%FT%TZ)" "$(date -u -d "@$((_mn_e-29))" +%FT%TZ)" "$(date -u -d "@$((_mn_e-28))" +%FT%TZ)" > "$_mnd/board"
  if MESH_MINTER_HOSTNAME=host-a mesh_is_minter "$_mnd/board" 86400; then got=minter; else got=not; fi
  ck2 "$got" "minter" "lexically-lowest hostname (host-a) elected"
  if MESH_MINTER_HOSTNAME=host-b mesh_is_minter "$_mnd/board" 86400; then got=minter; else got=not; fi
  ck2 "$got" "not" "non-lowest hostname (host-b) NOT elected"
  if MESH_MINTER_HOSTNAME=host-c mesh_is_minter "$_mnd/board" 86400; then got=minter; else got=not; fi
  ck2 "$got" "not" "non-lowest hostname (host-c) NOT elected"
  if MESH_MINTER_HOSTNAME=host-z mesh_is_minter "$_mnd/no-such-file" 86400; then got=minter; else got=not; fi
  ck2 "$got" "minter" "unreadable/empty log -> mint anyway (racy edge, never a silent drop)"
  if MESH_MINTER_HOSTNAME=host-b MESH_MINTER_PIN=host-b mesh_is_minter "$_mnd/board" 86400; then got=minter; else got=not; fi
  ck2 "$got" "minter" "MESH_MINTER_PIN overrides election"
  rm -rf "$_mnd"
  echo "board_presync — rate-limited synchronous gossip pull before trusting the local board:"
  _psd="$(mktemp -d)"
  _ps_calls="$_psd/calls"
  _ps_cmd="$_psd/ps_cmd.sh"
  printf '#!/bin/sh\necho called >> "%s"\n' "$_ps_calls" > "$_ps_cmd"; chmod +x "$_ps_cmd"
  board_presync "$_psd/stamp" 300 5 ""
  [ -f "$_ps_calls" ] && { echo "  FAIL: empty cmd must be a no-op (nothing called)"; fail=1; } || echo "  ok: empty cmd no-op"
  board_presync "$_psd/stamp" 300 5 "$_ps_cmd"
  [ "$(grep -c . "$_ps_calls" 2>/dev/null || echo 0)" = 1 ] || { echo "  FAIL: no stamp (first call) must sync (got $(grep -c . "$_ps_calls" 2>/dev/null || echo 0) calls)"; fail=1; }
  [ -f "$_psd/stamp" ] || { echo "  FAIL: stamp file must be touched after a sync"; fail=1; }
  echo "  ok: first call (no stamp) syncs + touches stamp"
  board_presync "$_psd/stamp" 300 5 "$_ps_cmd"
  [ "$(grep -c . "$_ps_calls" 2>/dev/null || echo 0)" = 1 ] || { echo "  FAIL: fresh stamp (within min_interval) must skip the pull (rate-limit) — got $(grep -c . "$_ps_calls" 2>/dev/null || echo 0) calls"; fail=1; }
  echo "  ok: fresh stamp skips (rate-limited)"
  touch -d '-400 seconds' "$_psd/stamp"
  board_presync "$_psd/stamp" 300 5 "$_ps_cmd"
  [ "$(grep -c . "$_ps_calls" 2>/dev/null || echo 0)" = 2 ] || { echo "  FAIL: stale stamp (older than min_interval) must sync again — got $(grep -c . "$_ps_calls" 2>/dev/null || echo 0) calls"; fail=1; }
  echo "  ok: stale stamp (past min_interval) re-syncs"
  _ps_start=$(date +%s)
  board_presync "$_psd/hangstamp" 300 1 "sleep 5"
  _ps_elapsed=$(( $(date +%s) - _ps_start ))
  [ "$_ps_elapsed" -lt 4 ] || { echo "  FAIL: a hanging sync_cmd must be killed by the timeout (elapsed=${_ps_elapsed}s, want <4s)"; fail=1; }
  echo "  ok: hung sync_cmd bounded by timeout (elapsed=${_ps_elapsed}s)"
  rm -rf "$_psd"
  echo "_mesh_is_cgnat — 100.64/10 is the tailnet, and its EDGES are not off by one:"
  ckc(){ local want="$1" label="$2" addr="$3" got; if _mesh_is_cgnat "$addr"; then got=cgnat; else got=no; fi
         if [ "$got" = "$want" ]; then echo "  ok: $label"; else echo "  FAIL: $label ($addr → $got, want $want)"; fail=1; fi; }
  ckc cgnat "low edge 100.64.0.0"      "100.64.0.0"
  ckc cgnat "live phone 100.103.99.16" "100.103.99.16"
  ckc cgnat "high edge 100.127.255.255" "100.127.255.255"
  ckc no    "100.63.x is BELOW the range" "100.63.255.255"
  ckc no    "100.128.x is ABOVE the range" "100.128.0.1"
  ckc no    "a LAN addr is not a tailnet addr" "192.168.8.146"
  ckc no    "empty is not a tailnet addr"      ""
  echo "phone_reach_candidates — a 3-rung ladder must be 3 DISTINCT addresses, never one probed twice:"
  # The 2026-08-20 fault verbatim: the MESH_NODES ts slot held a LAN address, so step 1 ("Tailscale
  # IP") and step 2 (PHONE_LAN_IPS) were the same dead string. Drives the REAL assembly function off
  # stubbed organs (mesh-peer-addr / tailscale on PATH) — no candidate list is ever injected.
  _prd="$(mktemp -d)"
  cat > "$_prd/peers.json" <<'PJ'
{"Peer":{"a":{"HostName":"Redmi 10","DNSName":"redmi-10.tail3e4555.ts.net.","TailscaleIPs":["fd7a:115c:a1e0::1","100.103.99.16"]},
         "b":{"HostName":"phaedra","DNSName":"phaedra.tail3e4555.ts.net.","TailscaleIPs":["100.94.116.17"]}}}
PJ
  _pr_stub(){ # <slot-addr> <with-tailscale:yes|no>
    printf '#!/bin/sh\nprintf "%%s\\n" "%s"\n' "$1" > "$_prd/mesh-peer-addr"; chmod +x "$_prd/mesh-peer-addr"
    if [ "$2" = yes ]; then printf '#!/bin/sh\ncat "%s"\n' "$_prd/peers.json" > "$_prd/tailscale"; chmod +x "$_prd/tailscale"
    else rm -f "$_prd/tailscale"; fi
  }
  _pr_run(){ ( PATH="$_prd:$PATH"; PHONE_LAN_IPS="$1"; unset PHONE_TS_PEER_RE; phone_reach_candidates ); }
  # 1. THE LIVE FAULT: LAN address in the ts slot, and the same address also in PHONE_LAN_IPS.
  _pr_stub 192.168.8.146 yes
  _pr_out="$(_pr_run "192.168.8.203 192.168.8.146")"
  ck2 "$(printf '%s\n' "$_pr_out" | grep -c '192\.168\.8\.146')" 1 \
      "LAN-in-ts-slot: the duplicated address is probed ONCE, not once per rung"
  ck2 "$(printf '%s\n' "$_pr_out" | awk '{print $2}' | sort -u | wc -l)" 3 \
      "LAN-in-ts-slot: 3 rungs → 3 distinct addresses"
  printf '%s\n' "$_pr_out" | grep -q '^ts-live 100\.103\.99\.16$' \
    || { echo "  FAIL: a non-tailnet ts slot must ALSO offer the live tailnet peer addr: $_pr_out"; fail=1; }
  printf '%s\n' "$_pr_out" | grep -q '^ts-live fd7a' \
    && { echo "  FAIL: a v6 tailnet addr must not pose as the 100.64/10 candidate"; fail=1; }
  # 2. Healthy slot: the live lookup adds nothing — it dedups away, so the probe count is unchanged.
  _pr_stub 100.103.99.16 yes
  _pr_out="$(_pr_run "192.168.8.203 192.168.8.146")"
  ck2 "$(printf '%s\n' "$_pr_out" | grep -c '100\.103\.99\.16')" 1 \
      "correct ts slot: live lookup dedups away (no second probe of the same addr)"
  ck2 "$(printf '%s\n' "$_pr_out" | wc -l)" 3 "correct ts slot: ladder stays 3 candidates"
  # 3. A duplicated PHONE_LAN_IPS entry is also one probe.
  _pr_stub 100.103.99.16 yes
  ck2 "$(_pr_run "192.168.8.146 192.168.8.146" | grep -c '192\.168\.8\.146')" 1 \
      "duplicate PHONE_LAN_IPS entry collapses to one candidate"
  # 4. No tailscale binary at all → degrade to slot+LAN, never a crash or an empty ladder. PATH is
  #    narrowed to the stub dir (+ a jq symlink) so `command -v tailscale` genuinely finds nothing —
  #    with the node's own /usr/bin still on PATH this gate would silently test the LIVE tailnet.
  _pr_stub 192.168.8.146 no
  ln -sf "$(command -v jq)" "$_prd/jq"
  _pr_out="$( ( PATH="$_prd"; PHONE_LAN_IPS="192.168.8.203"; unset PHONE_TS_PEER_RE; phone_reach_candidates ) )"
  ck2 "$(printf '%s\n' "$_pr_out" | wc -l)" 2 "tailscale absent: ladder degrades to slot+LAN"
  printf '%s\n' "$_pr_out" | grep -q '^ts-live' \
    && { echo "  FAIL: no tailscale → there is no live rung to claim"; fail=1; }
  # 5. No peer matches the phone regex → no ts-live rung invented.
  _pr_stub 192.168.8.146 yes
  _pr_out="$( ( PATH="$_prd:$PATH"; PHONE_LAN_IPS="192.168.8.203"; PHONE_TS_PEER_RE='^nosuchpeer'; phone_reach_candidates ) )"
  printf '%s\n' "$_pr_out" | grep -q '^ts-live' \
    && { echo "  FAIL: unmatched peer must yield NO ts-live candidate: $_pr_out"; fail=1; }
  ck2 "$(printf '%s\n' "$_pr_out" | wc -l)" 2 "unmatched peer: ladder is slot+LAN only"
  rm -rf "$_prd"

  # ---- RSSI sentinel grammar ----
  echo "rssi_valid — the two renderings of ONE blind instant must BOTH be rejected:"
  rssi_valid -49    || { echo "  FAIL: -49 is a real reading";                       fail=1; }
  rssi_valid -49.   || { echo "  FAIL: -49. (proc trailing dot) is a real reading";  fail=1; }
  rssi_valid '-54 dBm' || { echo "  FAIL: '-54 dBm' (iw suffix) is a real reading";  fail=1; }
  rssi_valid -43.5  || { echo "  FAIL: -43.5 is a real reading";                     fail=1; }
  rssi_valid 0      && { echo "  FAIL: 0 is nl80211's BLIND instant, not a perfect link"; fail=1; }
  rssi_valid 0.     && { echo "  FAIL: 0. is the same sentinel with proc's dot";     fail=1; }
  rssi_valid -0     && { echo "  FAIL: -0 is still zero";                            fail=1; }
  rssi_valid 5      && { echo "  FAIL: a receiver RSSI is never positive";           fail=1; }
  rssi_valid -256   && { echo "  FAIL: -256 is /proc's driver-not-ready sentinel";   fail=1; }
  rssi_valid -256.  && { echo "  FAIL: -256. sentinel with the dot";                 fail=1; }
  rssi_valid -200   && { echo "  FAIL: -200 is at the sentinel floor, not above it"; fail=1; }
  rssi_valid ''     && { echo "  FAIL: empty is not a reading";                      fail=1; }
  rssi_valid NA     && { echo "  FAIL: NA is not a reading";                         fail=1; }
  rssi_valid -      && { echo "  FAIL: '-' is not a reading";                        fail=1; }
  rssi_valid abc    && { echo "  FAIL: non-numeric is not a reading";                fail=1; }
  # THE WHOLE POINT: the old magnitude bound (> -200) accepts 0, and that is the dangerous half.
  # This asserts the two guards are NOT the same predicate, so a regression back to a bound is red.
  _rv_bound(){ local l="${1%.}"; case "$l" in ''|*[!0-9-]*) return 1;; esac; [ "$l" -gt -200 ] 2>/dev/null; }
  _rv_bound 0 || { echo "  FAIL: fixture wrong — the OLD level_valid bound does accept 0"; fail=1; }
  rssi_valid 0 && { echo "  FAIL: rssi_valid must differ from the bound exactly here"; fail=1; }

  echo "rssi_burst — median over a burst, blind fraction published, NEVER 0:"
  ck2 "$(printf -- '-49\n-50\n-48\n' | rssi_burst)" "-49 3 3"  "all valid: median, 3/3"
  ck2 "$(printf -- '-49\n0\n-51\n' | rssi_burst)"   "-51 2 3"  "one railed sample is dropped, not averaged in"
  ck2 "$(printf -- '0\n0\n0\n' | rssi_burst)"       "na 0 3"   "all railed -> na, never 0"
  ck2 "$(printf -- '-256.\n-49.\n' | rssi_burst)"   "-49 1 2"  "proc rendering: sentinel dropped, dot tolerated"
  ck2 "$(printf -- '-40\n-50\n-60\n-70\n' | rssi_burst)" "-60 4 4" "even count takes the WEAKER median (never averages two into a value no sample had)"
  ck2 "$(printf -- '\n' | rssi_burst)"              "na 0 1"   "an empty line is a sample that yielded nothing"
  ck2 "$(printf -- '' | rssi_burst)"                "na 0 0"   "no samples at all: na with total 0, never a value"
  # A railed burst must not be rescued into a plausible-looking number by ANY path.
  printf -- '0\n0\n0\n0\n0\n' | rssi_burst | grep -q '^na ' \
    || { echo "  FAIL: a fully blind burst must render na"; fail=1; }
  # ...and a burst that is blind in the /proc rendering must land on the SAME verdict as the
  # nl80211 one — one blindness, one answer, whichever surface reported it.
  ck2 "$(printf -- '-256.\n-256.\n' | rssi_burst)"  "na 0 2"   "the twin rendering of the same blindness -> na too"

  # ---- beacon_missed_read: a proc ZERO is not a reading -------------------------------------
  # Every arm asserts the same thing from a different side: the alarm-named field must never be
  # published as 0 on the strength of a column the driver does not fill.
  _bmk(){ ck2 "$1" "$2" "$3"; }
  # A node with no `iw` and a proc zero: the ONLY honest answer is na/none.
  _bm_noiw="$(PATH=/nonexistent-for-this-arm beacon_missed_read someif 0)"
  ck2 "$_bm_noiw" "na none" "no surface answered and proc reads 0 -> na, NEVER 0"
  ck2 "$(PATH=/nonexistent-for-this-arm beacon_missed_read someif 7)" "7 proc" \
      "a proc counter that is demonstrably LIVE (>0) is used, and says it came from proc"
  ck2 "$(PATH=/nonexistent-for-this-arm beacon_missed_read someif '')" "na none" \
      "an unreadable proc field is na, not 0"
  ck2 "$(PATH=/nonexistent-for-this-arm beacon_missed_read someif xx)" "na none" \
      "a non-numeric proc field is rejected rather than passed through"
  ck2 "$(beacon_missed_read '' 0)" "na none" "no interface to ask -> na"
  # nl80211 WINS over proc, and that is the whole fix: on rtw88 proc is 0 in the same instant that
  # nl80211 reports a real loss count, so a rule that preferred proc would keep the all-clear.
  _bmd="$(mktemp -d)"
  cat > "$_bmd/iw" <<'IWEOF'
#!/bin/sh
[ "$2" = "wlanTEST" ] || exit 1
cat <<'X'
Station aa:bb:cc:dd:ee:ff (on wlanTEST)
	rx drop misc:	951
	beacon loss:	9
	beacon rx:	7397
X
IWEOF
  chmod +x "$_bmd/iw"
  ck2 "$(PATH="$_bmd:$PATH" beacon_missed_read wlanTEST 0)" "9 nl80211" \
      "nl80211 answers over a proc ZERO — the exact rtw88 instant that was published as 0"
  ck2 "$(PATH="$_bmd:$PATH" beacon_missed_read wlanTEST 3)" "9 nl80211" \
      "...and over a nonzero proc too: the authoritative surface wins, it is not a max()"
  # `beacon loss` lives in station dump, never in `link`; and the neighbouring `rx drop misc` line
  # is the value a careless parse grabs, so assert we did not take 951.
  ck2 "$(PATH="$_bmd:$PATH" beacon_missed_read wlanTEST 0)" "9 nl80211" \
      "the neighbouring rx-drop-misc line (951) is NOT what the parse returns"
  # An interface iw refuses falls all the way through rather than inheriting another one's number.
  ck2 "$(PATH="$_bmd:$PATH" beacon_missed_read otherif 0)" "na none" \
      "an interface the tool cannot dump renders na, never another interface's count"
  # TWO STATIONS IS WHAT MAKES THE `exit` LOAD-BEARING. Managed mode has one AP station, but an
  # interface in another mode (or mid-roam) dumps more than one, and without the exit awk prints
  # both lines — which a `$(...)` capture joins into "9 4", a number no counter ever held and one
  # that fails the numeric guard downstream into a silent na. A one-station fixture cannot see it.
  # [[a-fixture-whose-two-candidates-carry-one-value-cannot-discriminate]]
  cat > "$_bmd/iw" <<'IWEOF'
#!/bin/sh
[ "$2" = "wlanTEST" ] || exit 1
cat <<'X'
Station aa:bb:cc:dd:ee:ff (on wlanTEST)
	rx drop misc:	951
	beacon loss:	9
Station 11:22:33:44:55:66 (on wlanTEST)
	rx drop misc:	12
	beacon loss:	4
X
IWEOF
  chmod +x "$_bmd/iw"
  ck2 "$(PATH="$_bmd:$PATH" beacon_missed_read wlanTEST 0)" "9 nl80211" \
      "a multi-station dump yields the FIRST station's count, never two joined into one number"
  rm -rf "$_bmd"

  [ "$fail" = 0 ] && { echo "smoke-test: ok"; exit 0; } || { echo "smoke-test: FAIL"; exit 1; }
fi
