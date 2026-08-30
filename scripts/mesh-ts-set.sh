#!/usr/bin/env bash
# mesh-ts-set.sh — THE ONE WAY THIS MESH CALLS `tailscale set`. Sourced; never executed.
# orphan-ok: sourced library, never executed. Its launchers are the tools that source it —
# mesh-revive (the exit-node rungs of its heal ladder) and mesh-exit (--off / --on / auto-revert).
#
#   . "${MESH_TS_SET_LIB:-$HOME/.local/bin/mesh-ts-set.sh}"
#   err="$(ts_set --exit-node=)" || echo "REFUSED: $err"
#
# WHY IT IS A LIB (discover {#80589d28} 2026-08-30, verified by health the same hour): the stderr
# discard was repaired at ONE call site and survived at its sibling. mesh-revive grew ts_set() on
# 2026-08-27 after its exit-node rung was measured to have been a NO-OP for its whole life; mesh-exit
# kept THREE raw `tailscale set … 2>/dev/null` calls (its --off, its backgrounded auto-revert, its
# --on), so on this node all three were denied, the refusal text went to the bin, and the user was
# told only "mesh-exit: tailscale set failed". One function, two callers, no third copy to forget.
#
# ts_set — THE ACTUATOR THAT WAS NEVER ALLOWED TO RUN (measured 2026-08-27T18:57Z on mesh-home).
# `tailscale set --exit-node=…` as uid 1000 on this node answers:
#     Access denied: checkprefs access denied
#     Use 'sudo tailscale set …'.  To not require root, use 'sudo tailscale set --operator=$USER'.
# mesh-revive runs as uid 1000 under `mesh-selfcare --loop`, and BOTH exit-node call sites were
# written `timeout 15 tailscale set … 2>/dev/null && note "…" || true` — stderr to the bin, rc
# swallowed by `|| true`. So the entire exit-node rung has been a NO-OP for its whole life, and its
# denial was indistinguishable from a branch that simply did not apply. That is the answer to "did
# that leg run at all": it ran, it was REFUSED, and nothing anywhere could say so — the same shape
# as a silent fallback turning a total failure into a plausible constant.
# Unprivileged FIRST (a node that has run `tailscale set --operator=$USER` needs no sudo and must
# not be pushed through one), then `sudo -n` — never a password prompt, which would hang a reflex.
# The stderr of whichever attempt failed is RETURNED, so the ledger can name the refusal instead of
# printing a generic non-zero.
#
# A TIMEOUT IS NOT A DENIAL, and both used to print the same shape. Measured on mesh-home
# 2026-08-30T21:21:13Z: `RESTORE-FAILED ... err=[Access denied: checkprefs access denied ... | sudo: ]`
# — the sudo half's text is EMPTY, because `timeout 15` killed it (rc 124) rather than sudo refusing.
# The bound bites exactly when this actuator matters: a pref write during a degraded uplink is the
# SLOW case, so a 15s cap turns "the network is struggling" into "the restore is impossible", and the
# node stays off its exit node with every mind dark. The refusal string now NAMES which happened, and
# the bound is generous and overridable. [[a-timed-out-push-is-not-a-failed-push]]
TS_SET_TIMEOUT="${MESH_TS_SET_TIMEOUT:-45}"
ts_set(){
  local out rc unpriv urc
  out="$(timeout "$TS_SET_TIMEOUT" tailscale set "$@" 2>&1)"; rc=$?
  [ "$rc" = 0 ] && { printf '%s' "$out"; return 0; }
  unpriv="$out"; urc=$rc
  out="$(timeout "$TS_SET_TIMEOUT" sudo -n tailscale set "$@" 2>&1)"; rc=$?
  [ "$rc" = 0 ] && { printf 'via-sudo %s' "$out"; return 0; }
  # 124 is timeout(1)'s own verdict; anything else with empty text is a silent non-zero, which is a
  # THIRD thing and must not wear either word.
  _w(){ case "$1" in 124) printf 'TIMED-OUT after %ss' "$TS_SET_TIMEOUT" ;; *) [ -n "$2" ] && printf '%s' "$(printf '%s' "$2" | tr '\n' ' ' | cut -c1-90)" || printf 'rc=%s with no message' "$1" ;; esac; }
  printf 'unpriv: %s | sudo: %s' "$(_w "$urc" "$unpriv")" "$(_w "$rc" "$out")"
  return 1
}
