#!/usr/bin/env bash
# mesh-split-tabs.sh — CANONICAL tab-field splitter for bash (the DRY source).
#
# WHY THIS FILE EXISTS. `IFS=$'\t' read -r a b c` is not a tab splitter and never was. Tab is an
# IFS *whitespace* character, so bash collapses a RUN of tabs into ONE delimiter and strips leading
# and trailing ones. Every empty field vanishes and the fields after it shift LEFT — into the wrong
# variable, silently, with the last variable left empty. A TRAILING empty is handled correctly by
# accident (`read` simply runs out of fields), which is exactly why these survive: the common shape
# on a given fleet renders right while a leading or middle empty renders garbage.
#
# WHY IT IS SHARED RATHER THAN COPIED. It was written twice in one week — mesh-load-audit (cda823df)
# and mesh-mind-state (7f31c58a) — as two private copies of one predicate. A mesh-wide sweep then
# found the same defect live in six more files. N private copies of one predicate are all green and
# none of them is complete: the seventh site does not get the fix by being near the first six. One
# definition, sourced.
#
# SOURCING CONTRACT — copy this shape verbatim, including the empty argument:
#     source "$HOME/.local/bin/mesh-split-tabs.sh" "" 2>/dev/null \
#       || source "$(dirname "$0")/mesh-split-tabs.sh" "" 2>/dev/null || true
#     declare -F split_tabs >/dev/null \
#       || { echo "<tool>: mesh-split-tabs.sh not found — refusing to run with a tab reader that drops empty fields" >&2; exit 1; }
# The `""` is NOT decoration. `source` with no arguments leaves the CALLER's positional parameters
# in place, so `<tool> --test` hands `--test` to this file. The guard below stops that here, but a
# peer node whose deployed copy PREDATES that guard would still be hijacked, and these tools run
# fleet-wide — so the defence is written on the caller side too, where it cannot go stale. The
# second `source` is the in-genome path, so a tool run from scripts/ works before deploy.
# An inline fallback would be copy number three wearing a different hat, and a fallback that quietly
# reinstates `IFS=$'\t' read` would restore the exact defect this file removes while reading as a
# safety net. A missing library is a deploy fault: it must be LOUD (mesh-sync-tools flags the drift).
#
# NOT A REPLACEMENT FOR awk -F'\t' / cut -f. Those already honour empty fields and are the right
# tool when the row is being processed rather than bound to shell variables. This is for the case
# `read` is reached for: assign N tab-separated fields to N named shell variables.

# split_tabs <line> <var>... — assign the line's TAB-separated fields one per var, PRESERVING EMPTY
# ONES; the last var takes the whole remaining tail, exactly like `read` does with its final
# variable. Fewer fields than vars leaves the surplus vars empty (also like `read`).
split_tabs() {
  local _line="$1"; shift
  local _v _rest="$_line"
  while [ "$#" -gt 1 ]; do
    _v="$1"; shift
    printf -v "$_v" '%s' "${_rest%%$'\t'*}"
    case "$_rest" in *$'\t'*) _rest="${_rest#*$'\t'}" ;; *) _rest='' ;; esac
  done
  [ "$#" -eq 1 ] && printf -v "$1" '%s' "$_rest"
  return 0
}

# --test: driven directly (`mesh-split-tabs.sh --test`) ONLY.
# The legs are the three positions an empty field can occupy, because only ONE of them (trailing)
# is handled correctly by the thing this replaces — a suite that drove trailing empties alone would
# pass against `IFS=$'\t' read` itself and assert nothing.
#
# THE EXECUTED-NOT-SOURCED GUARD IS LOAD-BEARING, and it is here because it bit on the first wiring.
# A sourced file inherits the CALLER's positional parameters, so `mesh-load-audit --test` sourcing
# this library made `$1` read `--test` INSIDE it — the library ran its own suite, printed its own
# green line, and `exit 0` terminated the PARENT's --test after a single leg. Both rewired tools
# reported rc=0 having asserted nothing at all: a library that silences its callers' gates by being
# adopted, which is a worse defect than the one it fixes. `${BASH_SOURCE[0]} != $0` is the whole
# distinction — when sourced they differ, when executed they are the same path.
if [ "${BASH_SOURCE[0]}" = "$0" ] && [ "${1:-}" = "--test" ]; then
  _st_fail(){ echo "mesh-split-tabs: FAIL ($1)"; exit 1; }
  _st_chk(){ # <what> <expected-joined-by-|> <line> <var>...
    local _what="$1" _exp="$2" _line="$3"; shift 3
    local _v _got=""
    split_tabs "$_line" "$@"
    for _v in "$@"; do _got="$_got|${!_v}"; done
    [ "${_got#|}" = "$_exp" ] || _st_fail "$_what — expected '$_exp', got '${_got#|}'"
  }
  _st_chk "no empties"      "a|b|c"   "$(printf 'a\tb\tc')"    x y z
  _st_chk "LEADING empty"   "|b|c"    "$(printf '\tb\tc')"     x y z
  _st_chk "MIDDLE empty"    "a||c"    "$(printf 'a\t\tc')"     x y z
  _st_chk "TRAILING empty"  "a|b|"    "$(printf 'a\tb\t')"     x y z
  _st_chk "RUN of empties"  "a||||e"  "$(printf 'a\t\t\t\te')" v w x y z
  _st_chk "all empty"       "||"      "$(printf '\t\t')"       x y z
  _st_chk "short row"       "a|b||"   "$(printf 'a\tb')"       w x y z
  # the last var takes the TAIL, tabs and all — the one place `read`'s behaviour is the contract
  _st_chk "last var eats the tail" "$(printf 'a|b|c\td')" "$(printf 'a\tb\tc\td')" x y z
  # spaces are DATA here, never delimiters — the whole point of not using IFS whitespace
  _st_chk "spaces are data" "a b|c d" "$(printf 'a b\tc d')" x y
  # a single var gets the whole line untouched
  _st_chk "single var" "$(printf 'a\tb')" "$(printf 'a\tb')" x
  # THE ANTI-REGRESSION LEG: the thing this file replaces must actually DISAGREE on the middle
  # empty. If `read` ever agreed, every leg above would be vacuous.
  _st_rd_b=""; _st_rd_c=""
  IFS=$'\t' read -r _st_rd_a _st_rd_b _st_rd_c <<< "$(printf 'a\t\tc')"
  [ "$_st_rd_b" = "c" ] && [ -z "$_st_rd_c" ] \
    || _st_fail "the control arm did not reproduce the defect (IFS=tab read gave b='$_st_rd_b' c='$_st_rd_c') — without it these legs assert nothing"
  echo "mesh-split-tabs: ok (leading/middle/trailing/run/all-empty/short/tail/spaces/single + the IFS-read control arm still shifts)"
  exit 0
fi
