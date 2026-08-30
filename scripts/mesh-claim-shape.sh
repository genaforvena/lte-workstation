#!/usr/bin/env bash
# mesh-claim-shape.sh — THE ONE SLUG-TOKEN SHAPE. Sourced; never executed.
# orphan-ok: sourced library, never executed. Its launchers are the tools that source it —
# mesh-dispatch (idof/slugof on the TASK side, claim_id_of on the CLAIM side) and
# mesh-mind-control (claim_id_of for the resume-resurface close key it hands a mind verbatim).
#
#   . "${MESH_CLAIM_SHAPE_LIB:-$HOME/.local/bin/mesh-claim-shape.sh}"
#
#   $MESH_SLUG_TOK_RE   ERE: a bare slug token   ("foo-bar-baz", "a-dispatch-HOLD-returns")
#   $MESH_SLUG_PATH_RE  ERE: an ns/slug path     ("chat-review/foo-bar-baz")
#   $MESH_SLUG_MIN_LEN  a derived id shorter than this is quoting debris, not an id
#
# WHY A LIB AND NOT FOUR LITERALS (measured 2026-08-30, task
# claim-id-derivation-is-lowercase-only-so-an-uppercase-slug-is-handed-a-close-key-that-cannot-close):
# the TASK side (mesh-dispatch slugof) tests a token with `case $t in *-*)` — case-INSENSITIVE by
# construction — while every CLAIM side derived with a lowercase-only `[a-z0-9]+(-[a-z0-9]+)+`. On the
# real board slug 'a-dispatch-HOLD-returns-the-same-exit-code-as-a-DELIVERY-…' the two answered
# 'a-dispatch-HOLD-returns-…-forever' (whole) and 'a-dispatch' (stopped dead at the first uppercase
# segment, 10 chars, so it passed the min-length gate and was RETURNED as a generic close key).
# mesh-mind-control's resume-resurface then instructed a mind, verbatim, to post that key; the mind
# obeyed; the close could not match idof(task) and a fully finished task was re-dispatched 31 minutes
# later. Two copies of the derivation existed and had already drifted apart in three other ways, so a
# per-copy edit is the same defect class one round later: the shape lives in ONE place and a reader
# that cannot find it REFUSES to derive rather than carrying a constant of its own.
MESH_SLUG_TOK_RE='[A-Za-z0-9]+(-[A-Za-z0-9]+)+'
MESH_SLUG_PATH_RE='([A-Za-z0-9]+(-[A-Za-z0-9]+)*/)+[A-Za-z0-9]+(-[A-Za-z0-9]+)+'
MESH_SLUG_MIN_LEN=6
# strip_urls <text> — URL POISON IN THE DERIVATION LANE (chat-review/claim-id-url-path-outranks-the-
# real-slug, measured by pub 2026-08-28 against the real claim_id_of in a harness): an http(s) URL's
# path is EXACTLY the ns/slug shape claim_id_of()'s whole-body widen looks for first, so a pasted
# article link outranks the claim's own subject slug even when that slug appears EARLIER in the same
# body. Live: pub's 12:52:09Z '[done] pub: devto-log-this-once-ship … PUBLISHED https://dev.to/<user>/
# log-this-once-is-a-tense-change-not-a-rate-limit-1dmk …' keyed as the ARTICLE slug — the task stayed
# open 4h16m and owner-direct re-dispatched finished work. Worse than a miss: it MINTS a phantom
# account number ('…-1dmk') that no [done] can ever settle, because no task was ever filed under it.
# Control (pub's four-body run): identical body minus the URL, still tag-less, still a non-slug lead
# ('pub'), keys correctly — the URL is the sole cause. Replaced by a SPACE rather than deleted, as
# defence only: [^[:space:]]+ runs the match to the next whitespace, so no neighbour can actually fuse
# across a removed URL and a delete-vs-space mutant stays GREEN (driven). Not claimed as a gate.
# WHY IT LIVES UP HERE, far from its three strip_* siblings: everything below the --test block is
# unreachable from --test (bash resolves at call time and the block runs first), which is why those
# siblings are gated by hand-copied hermetic twins + source greps — the drift this file complains
# about in five places. Defined above the block, the REAL function is driven by --test directly, and
# the wiring is driven end-to-end through a sandbox board (HOME=<td> "$0" --status), so both arms go
# red on MUTATION rather than on the pattern's absence. Same idiom as _route_orphan_resolved_after().
strip_urls(){
  printf '%s' "$1" | sed -E 's#\bhttps?://[^[:space:]]+# #g'
}
# claim_id_of <claim-body>: the id a CLAIMS line is ABOUT = its OWN SUBJECT id, taken as the FIRST
# slug-shaped token (a slashed ns/slug path — ns may itself contain hyphens like "chat-review/" — or a
# bare hyphen-slug), else the first SHOUTY key. The subject leads; any LATER slug is prose citation.
# Keying on the subject (not substring-anywhere) is what stops chat-review/dispatch-claim-match-unanchored:
# the inner is_open scans matched *"[done]"*"$id"* — a real [done]/[taking] for task A whose prose merely
# CITES task B's slug (routine in a review that compares siblings) false-registered as B's own claim and
# silently evaporated B. Robust to the [done] "stale:"/"rejected:" qualifier prefix and a dropped "ns/"
# (the slug is found wherever it FIRST appears), so it never regresses the 2026-06-20 prefix-drop match.
# SELF-REPORT PREFIX (chat-review/dispatch-claimid-hostname-collision): a claim body opening with
# a "role@host: " self-identity prefix (e.g. "genome@imozerov-IdeaPad-3-15IIL05: <realslug> ...")
# has no case-boundary awareness in the id regex below, so a lowercase/digit fragment INSIDE a
# mixed-case hostname (e.g. "ad-3-15" out of "IdeaPad-3-15IIL05") matches BEFORE the real slug ever
# does — a real [done] whose subject id resolves to a hostname fragment never subject-matches its
# own [task], so is_open() never closes it (live: dispatch's [gap] false-flagged a task fixed 3h44m
# earlier as lost work). Strip the prefix first; a no-op when the body carries no such prefix.
strip_selfreport_prefix(){
  printf '%s' "$1" | sed -E 's/^(\[[a-z_-]+\]) [a-z][a-z_-]*@[A-Za-z0-9._-]+: /\1 /'
}
# ROUTING-LABEL PREFIX (chat-review/dispatch-claimid-loopbaton-prefix): a claim body opening with
# the mesh's own "<poster> loop-baton: " self-narration convention (e.g. "genome loop-baton:
# implemented chat-review/homestate-no-hysteresis ...") has no '/' in its lead field, so the ns/slug
# scan below correctly skips it — but the plain-hyphen fallback then matches "loop-baton" itself
# (>=6 chars) and returns it immediately, never reaching the whole-body widen step where the real
# subject slug actually lives (live: is_open() never recognized ANY "loop-baton:"-narrated [done],
# false-flagging genuinely-done tasks as still-open 4h24m later). Strip the routing label first, the
# same way strip_selfreport_prefix() strips a "role@host: " prefix; a no-op when absent.
strip_routinglabel_prefix(){
  printf '%s' "$1" | sed -E 's/^(\[[a-z_-]+\]) [a-z][a-z_-]* loop-baton: /\1 /'
}
# DISPATCH ROUTING-ARROW PREFIX (chat-review/dispatch-dispatchonly-claim-no-reopen, found while wiring
# the dispatch_ts seed below): mind-control's own '[dispatch] → <worker> (<descriptor>): <real subject>'
# line shape (e.g. '[dispatch] → genome (owner-direct): chat-review/dash-sstest-log-tail-stale: …') has
# a hyphenated word INSIDE the parenthetical descriptor ('owner-direct', 'baton, owner-direct') that
# satisfies the plain-hyphen lead-scan below before the real ns/slug subject after the SECOND colon is
# ever reached — claim_id_of() on this exact live line returns 'owner-direct', not the task's real slug,
# so the dispatch_ts fill-in this task adds could never subject-match a real 'owner-direct' dispatch (the
# live-evidence case cited by this very task: dash-sstest-log-tail-stale dispatched to phaedra:genome
# 'owner-direct'). Strip the routing-arrow prefix first, same idiom as its two siblings above; a no-op
# when the marker isn't '[dispatch]' or carries no arrow/parenthetical (a plain '[taking]'/'[done]' line
# is untouched).
strip_dispatch_routing_prefix(){
  printf '%s' "$1" | sed -E 's/^(\[dispatch\]) → [a-zA-Z0-9_-]+ \([^()]*\): /\1 /'
}
# POSTER-WINDOW LEAD (chat-review/done-leading-with-its-window-name-cannot-close-its-task
# {#de94646f}): a [done] that opens with the poster's own window — "[done] senses: <slug> — …", the
# routine self-report shape — puts a HYPHEN-FREE word in the leading field, so the lead scan below
# finds no slug there and widens to the WHOLE BODY, where the first ns/slug-shaped fragment in the
# prose wins. Measured on the live board 2026-08-30, the exact line this task cites:
#   [done] senses: body-dark-is-three-causes-with-three-owners-rendered-as-one-word — ПРИЗЕМЛЕНО …
# derived `mesh-organ-keepalive` — a tool name that appears later behind a `scripts/` path, which is
# exactly the ns/slug shape the widen prefers. is_open() then skips that [done] and re-dispatches a
# finished task: two wasted senses turns on 2026-08-29 (22:55:01Z, 23:35:09Z) against [done]s already
# posted at 20:18Z and 21:24:54Z. 19 of the last 60 [done] lines carry this lead shape.
# THE OTHER READER ALREADY DID THIS. --reliance's closure scan has stripped the window lead since it
# was written ("the lead token is either the slug or the window's own address, in which case the slug
# is the next token"), so the two readers of the same board disagreed about which line closes what.
# PREDICATE, and why it is not a widening: a derived slug ALWAYS contains a hyphen (every scan below
# is `[a-z0-9]+(-[a-z0-9]+)+`), so a lowercase lead word with NO hyphen can never be the subject —
# dropping it cannot destroy a real one. That is strictly narrower than matching prose, which is the
# trap dispatch-claim-match-unanchored already closed and which this must not reopen. It is also why
# the predicate is the SHAPE and not a roster of window names: a name list is an allowlist whose
# failure direction is silence, and it would have gone stale at the next channel added.
# SHOUTY IS UNTOUCHED by construction ([A-Z] never matches [a-z]), so a 'DIRTY-TREE:' key still keys.
strip_window_lead_prefix(){
  printf '%s' "$1" | sed -E 's/^(\[[a-z_-]+\]) [a-z][a-z0-9_]*: /\1 /'
}
# NS/SLUG PRECEDENCE (chat-review/dispatch-claimid-toolname-precedes-subject): a bare 'mesh-<tool>'
# mention in prose (e.g. "fixed mesh-dispatch's claim_id_of()...") must not beat the claim's own
# LATER ns/slug-qualified subject (e.g. "chat-review/some-real-slug") just for appearing earlier in
# the string. Search for an ns/slug form (contains '/') FIRST across the whole body; only fall back
# to the plain first-hyphen-token scan when no ns/slug form exists anywhere.
# SLASH-HIJACK (chat-review/dispatch-claimid-slash-hijack): the whole-body scan above cuts both ways —
# a slash-containing fragment ANYWHERE in the body's free-text description (a "gh PR/Trello/merge-
# identity" aside, routine prose) can outrank the real SUBJECT slug sitting right after the marker at
# the body's start, even when that subject has no '/' of its own (live: chat.log 2026-07-08T12:45:03Z
# [done] fawxible-review-ab9d4fb's "(gh PR/Trello/merge-identity)" aside made claim_id_of return
# 'merge-identity' instead of the claim's own subject — is_open() never matched it, and a [gap] scan
# evaporated fawxible-review-ab9d4fb as "never taken" 8.5h after its real [done] already existed).
# Fix: search the SUBJECT field first — the leading text up to the first ':' (mirrors slugof()'s
# ${1%%:*} on the [task] side) — and only widen to the whole body when that leading field yields no
# slug at all (the stale:/rejected: qualifier and self-report-prefix cases: their leading field is
# marker-only prose with no hyphenated token, so they still fall through to the whole-body scan
# unchanged).
# PURE-FUNCTION MEMO (dispatch-open-set-is-window-bound perf): once the OPEN scan went full-board, is_open()
# calls claim_id_of() per (task × substring-matching claim) pair — and each call forks ~10 subshells (3
# strip helpers + up to 5 grep -oE). At 70 open tasks × 294 claims that pushed `--status` from 4s to 27s,
# past mesh-dash:504's `timeout 12` (which would blank the minds allocation pane). claim_id_of is a PURE
# function of its input line, so cache by that line: a repeat on the same claim body returns the same id.
# This collapses the cost from O(tasks×claims) back to O(distinct claims) — restoring the ~4s budget while
# keeping full-board visibility. The cache lives in the OPEN mapfile's pipeline subshell (all is_open()
# calls share it) and can never go stale (same input ⇒ same output, always). Falsifiable: the perf guard in
# --test asserts a deep-board `--status` completes under the dash budget.
declare -A _CID_MEMO 2>/dev/null || true
_claim_id_of_uncached(){
  local s body lead tag
  # ACCOUNTING CLOSE-KEY (operator 2026-07-24 "less language parsing, more accounting"): an explicit
  # `task:<id>` tag is the exact account number — prefer it over ALL prose derivation so a [done]/
  # [taking] can never have its subject hijacked by a tool-name or ns/slug quoted in its own prose.
  # THE STORM THIS CLOSES (live 2026-07-24): '[done] DIRTY-TREE: … (mesh-backlight, mesh-body-thermal,
  # …)' — the SHOUTY lead 'DIRTY-TREE' has no lowercase slug, so the whole-body scan below grabbed the
  # first lowercase slug in the filename list ('mesh-backlight') instead of falling to keyof → the
  # done's derived id != the task's id → is_open never closed it → owner-direct re-dispatched the
  # finished task every pass. No leading-discipline fixes it (a SHOUTY-keyed task always loses to a
  # lowercase slug in its own [done] prose). The dispatcher stamps `task:<idof(task)>` into the framed
  # prompt, so a compliant close carries the exact key and matches by construction. Untagged legacy
  # lines fall through to derivation unchanged (docs/design-hledger-coordination-2026-07-24.md
  # Direction 1: "prefer the explicit tag, fall back to derivation"). The tag regex requires no space
  # after the colon, so prose "the task: do X" never matches — only the machine tag "task:<slug>".
  tag="$(printf '%s' "$1" | grep -oE 'task:[A-Za-z0-9][A-Za-z0-9/._-]*' | head -1)"
  [ -n "$tag" ] && { tag="${tag#task:}"; tag="${tag##*/}"; printf '%s' "$tag"; return; }
  # URL STRIP FIRST (claim-id-url-path-outranks-the-real-slug): before ANY derivation scan sees the
  # body, blank out http(s) URLs — their path segments are the ns/slug shape the whole-body widen
  # below prefers, so a pasted link silently re-keys the close. Deliberately AFTER the task: tag
  # preference above: the tag is the account number and beats all derivation, URL or not.
  body="$(strip_urls "$(strip_window_lead_prefix "$(strip_dispatch_routing_prefix "$(strip_routinglabel_prefix "$(strip_selfreport_prefix "$1")")")")")"
  lead="${body%%:*}"
  s="$(printf '%s' "$lead" | grep -oE "$MESH_SLUG_PATH_RE" | head -1)"
  [ -n "$s" ] || s="$(printf '%s' "$lead" | grep -oE "$MESH_SLUG_TOK_RE" | head -1)"
  if [ -z "$s" ]; then
    s="$(printf '%s' "$body" | grep -oE "$MESH_SLUG_PATH_RE" | head -1)"
    [ -n "$s" ] || s="$(printf '%s' "$body" | grep -oE "$MESH_SLUG_TOK_RE" | head -1)"
  fi
  s="${s##*/}"
  if [ -n "$s" ] && [ "${#s}" -ge "$MESH_SLUG_MIN_LEN" ]; then printf '%s' "$s"; return; fi
  printf '%s' "$body" | grep -oE '[A-Z][A-Z-]{4,}' | head -1
}
claim_id_of(){
  local __k="$1"
  # bash cannot subscript an associative array with the empty string ("bad array subscript" on stderr,
  # twice per call). An empty body has no id anyway — answer before the memo, not inside it.
  [ -n "$__k" ] || return 0
  case "${_CID_MEMO[$__k]+set}" in set) printf '%s' "${_CID_MEMO[$__k]}"; return ;; esac
  local __v; __v="$(_claim_id_of_uncached "$1")"
  _CID_MEMO[$__k]="$__v"
  printf '%s' "$__v"
}
# claim_body_if <line> <marker>: echo the claim BODY ("[marker] subject: …") iff LINE is a body-START
# <marker> claim, else return 1 with no output. Pure param-expansion internally (the loops pre-filter on
# the id substring first, so this runs only on the few candidate lines). Strips the "<ts>  <who>  ::  "
# field prefix (robust to the board's 1-or-2 spaces) then requires the marker at the very start. This is
# the body-START discipline the CLAIMS grep and [task] scrape use; here it gates WHICH marker a line is,
# so a [taking] whose prose quotes "[done]" can never be read as a [done].
claim_body_if(){
  local rest="${1#*:: }"                         # drop through the "::" field separator
  rest="${rest#"${rest%%[![:space:]]*}"}"        # ltrim any residual leading space
  case "$rest" in "[$2] "*) printf '%s' "$rest" ;; *) return 1 ;; esac
}
