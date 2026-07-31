# Promise Lifecycle (writeoff/reroute) + Clear-on-Claim-Lifecycle — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give `mesh-promises` an explicit, audited resolution path for promises/claims/holds that
can never self-resolve (writeoff/reroute + uniform unrouted accounting + a suggested-owner hint +
narrow opt-in auto-reaction), and give `mesh-mind-compact` a matching claim-lifecycle-driven `/clear`
trigger that replaces its standalone wall-clock interval with hledger-native queries.

**Architecture:** Both tools are single self-contained bash scripts with an embedded python3 heredoc
for `mesh-promises`' board replay. All changes are additive to the existing replay/dispatch
structure — no new files, no new journals, no schema migration. `mesh-promises` changes land and
pass `--test` first; `mesh-mind-compact`'s `hold-leak` tier depends on `mesh-promises --json`'s
(already-existing) HOLD fields, so it must land after.

**Tech Stack:** bash (`set -uo pipefail`), python3 (stdlib only — `re`, `json`, `datetime`), hledger
CLI, git (per-tool local repo for the materialized journal), tmux (`mesh-mind-compact` only).

## Global Constraints

- Board (`~/.mesh/chat.log`) stays the sole source of truth. Every new mutation goes through
  `mesh-chat`; the journal is always regenerated from the board, never hand-edited. (Spec 1, throughout.)
- Every ledger action must be **loud on failure, never a silent no-op** — a validated lookup miss
  exits non-zero and posts nothing. (Spec 1, Component B.)
- `hledger check` (parity: every open/close txn sums to zero) must still pass after every change —
  run `mesh-promises --test` after each python-touching step, not just at the end of a task.
- Fail-open where the codebase already establishes fail-open (absent `accounts.journal` → roster
  inactive, trust owner as-is); fail-**inert** (never fire) for the two new `mesh-mind-compact`
  ledger-query tiers when `mesh-promises`/`mesh-labor` are absent — never a false positive or crash.
  (Spec 2, Component C.)
- `--reroute` supports `promise|claim` only. `hold` is writeoff-only — a HOLD's taker is
  `holds[who]`, the actual board-line poster identity, not body text; nothing can repost `[taking]`
  as a different window without impersonating it. (Spec 1, Component B, corrected 2026-07-24.)
- New CLI subcommands and new test assertions follow the exact style already in each file: numbered
  `--test` assertions with explicit `smoke-test: FAIL (<what broke>)` messages, override-injection
  env vars for external command mocking (`MESH_COMPACT_SNAPSHOT_CMD`-style), synthetic `chat.log`
  fixtures written via heredoc.

**Specs:** `docs/superpowers/specs/2026-07-24-promise-writeoff-reroute-design.md` (Tasks 1-4),
`docs/superpowers/specs/2026-07-24-clear-on-claim-lifecycle-design.md` (Tasks 5-6).

---

## Task 1: `mesh-promises` — Component B: `--writeoff` / `--reroute` resolution primitive

**Files:**
- Modify: `scripts/mesh-promises` (python replay heredoc: `episodes`/`claim_episodes`/`hold_episodes`
  tuple shape, the `elif marker == 'done':` branch, the journal-writing loop; bash: two new functions
  + CLI dispatch)
- Modify: `scripts/accounts.journal` (declare the new `equity:*:writeoff`/`equity:*:reroute` legs)

**Interfaces:**
- Produces: bash functions `do_writeoff()`, `do_reroute()`; CLI subcommands `--writeoff`, `--reroute`;
  python regex `ADMIN_CLOSE_RE`; episode tuples gain a 7th (promise/claim) / 6th (hold) `outcome`
  field, one of `'kept' | 'writeoff' | 'reroute' | None` (`None` only for still-open episodes).
- Consumes: nothing new from other tasks — this is the foundational task.

This is the biggest task in the plan. Work through it in the exact order below; each numbered
sub-step is independently `--test`-able before moving to the next.

### Step 1.1: Extend episode tuples with an `outcome` field (still-open sites)

The three "still open → open-ended episode" append sites need a trailing `None` so every episode
tuple has the same arity everywhere (the journal-writing loop unpacks all of them the same way).

- [ ] Edit `scripts/mesh-promises` around line 390:

```python
# OLD (line 390):
    episodes.append((o['owner'], o['slug'], o['ts'], None, o['incident'], o['lead']))
# NEW:
    episodes.append((o['owner'], o['slug'], o['ts'], None, o['incident'], o['lead'], None))
```

- [ ] Edit around line 406 (inside the claim still-open loop):

```python
# OLD:
        claim_episodes.append((debtor, slug, o['ts'], None, o['lead'], o['reflex']))
# NEW:
        claim_episodes.append((debtor, slug, o['ts'], None, o['lead'], o['reflex'], None))
```

- [ ] Edit around line 418 (inside the hold still-open loop):

```python
# OLD:
        hold_episodes.append((taker, slug, o['ts'], None, o['lead']))
# NEW:
        hold_episodes.append((taker, slug, o['ts'], None, o['lead'], None))
```

### Step 1.2: Tag the three normal "kept" append sites with `outcome='kept'`

- [ ] Edit line 341 (promise kept, inside `elif marker == 'done':`, the `if k:` branch):

```python
# OLD:
            episodes.append((o['owner'], o['slug'], o['ts'], ts, o['incident'], o['lead']))
# NEW:
            episodes.append((o['owner'], o['slug'], o['ts'], ts, o['incident'], o['lead'], 'kept'))
```

- [ ] Edit line 353 (hold released via a matching `[done]`, same `elif marker == 'done':` block):

```python
# OLD:
                hold_episodes.append((who, hk, ho['ts'], ts, ho['lead']))
# NEW:
                hold_episodes.append((who, hk, ho['ts'], ts, ho['lead'], 'kept'))
```

- [ ] Edit line 385 (claim redeemed, inside `elif marker in ('fyi', 'sense'):`):

```python
# OLD:
                claim_episodes.append((who, ck, co['ts'], ts, co['lead'], co['reflex']))
# NEW:
                claim_episodes.append((who, ck, co['ts'], ts, co['lead'], co['reflex'], 'kept'))
```

- [ ] Run `mesh-promises --test` (or `bash scripts/mesh-promises --test` if not yet deployed to
  `~/.local/bin/`). Expected: **FAIL** — the journal-writing loop still unpacks 6-tuples (promise) /
  6-tuples (claim) / 5-tuples (hold); tuple arity now mismatches. This is the expected RED state —
  proceed to Step 1.3 to fix the unpacking, don't stop here.

### Step 1.3: Update the journal-writing loop to unpack `outcome` and pick the equity leg

- [ ] Edit the promise loop, around line 448-469:

```python
# OLD:
    for owner, slug, ots, cts, incid, hl in sorted(episodes, key=lambda e: e[2]):
        seq += 1
        # owner segment is roster-validated: a non-roster owner books to :unrouted (VISIBLE), not a
        # phantom named window. The CLAIMED owner is preserved in the owner: tag either way, so the
        # quarantine loses no information — an unrouted promise still shows whom it claimed.
        acct = "liabilities:promises:%s:%s" % (acct_window(owner), slug)
        tag = "promise:%s owner:%s opened:%s%s" % (slug, owner,
                ots.strftime('%Y-%m-%dT%H:%M:%SZ'), " priority:incident" if incid else "")
        # TWO spaces min between account and amount — hledger's delimiter. A long (>pad) account with
        # only ONE space folds the amount INTO the account name, so open/keep land in DIFFERENT
        # mangled accounts and never net (parity still passes via inference — the silent trap).
        lines.append("%s * promise opened: %s  ; %s" % (ots.strftime('%Y-%m-%d'), slug, tag))
        lines.append("    %s  1 PROMISE" % acct)
        lines.append("    %s  -1 PROMISE" % "equity:promises")
        lines.append("")
        if cts is not None:
            lag = round((cts - ots).total_seconds()/3600.0, 1)
            lines.append("%s * promise kept: %s  ; promise:%s kept:%s lag:%sh" % (
                cts.strftime('%Y-%m-%d'), slug, slug, cts.strftime('%Y-%m-%dT%H:%M:%SZ'), lag))
            lines.append("    %s  -1 PROMISE" % acct)
            lines.append("    %s  1 PROMISE" % "equity:promises")
            lines.append("")

# NEW:
    for owner, slug, ots, cts, incid, hl, outcome in sorted(episodes, key=lambda e: e[2]):
        seq += 1
        # owner segment is roster-validated: a non-roster owner books to :unrouted (VISIBLE), not a
        # phantom named window. The CLAIMED owner is preserved in the owner: tag either way, so the
        # quarantine loses no information — an unrouted promise still shows whom it claimed.
        acct = "liabilities:promises:%s:%s" % (acct_window(owner), slug)
        tag = "promise:%s owner:%s opened:%s%s" % (slug, owner,
                ots.strftime('%Y-%m-%dT%H:%M:%SZ'), " priority:incident" if incid else "")
        # TWO spaces min between account and amount — hledger's delimiter. A long (>pad) account with
        # only ONE space folds the amount INTO the account name, so open/keep land in DIFFERENT
        # mangled accounts and never net (parity still passes via inference — the silent trap).
        lines.append("%s * promise opened: %s  ; %s" % (ots.strftime('%Y-%m-%d'), slug, tag))
        lines.append("    %s  1 PROMISE" % acct)
        lines.append("    %s  -1 PROMISE" % "equity:promises")
        lines.append("")
        if cts is not None:
            lag = round((cts - ots).total_seconds()/3600.0, 1)
            # outcome distinguishes a genuine keep from an admin writeoff/reroute — each nets the
            # SAME liability to zero (parity is unaffected either way) but into a DIFFERENT equity
            # leg, so "died unkept" becomes a distinct, queryable number from "kept" (mesh-promises
            # writeoff/reroute design, Component B).
            eq = {'kept': 'equity:promises', 'writeoff': 'equity:promises:writeoff',
                  'reroute': 'equity:promises:reroute'}.get(outcome, 'equity:promises')
            verb = {'kept': 'kept', 'writeoff': 'written off', 'reroute': 'rerouted'}.get(outcome, 'kept')
            lines.append("%s * promise %s: %s  ; promise:%s outcome:%s closed:%s lag:%sh" % (
                cts.strftime('%Y-%m-%d'), verb, slug, slug, outcome or 'kept',
                cts.strftime('%Y-%m-%dT%H:%M:%SZ'), lag))
            lines.append("    %s  -1 PROMISE" % acct)
            lines.append("    %s  1 PROMISE" % eq)
            lines.append("")
```

- [ ] Edit the claim loop, around line 473-489:

```python
# OLD:
    for debtor, slug, ots, cts, hl, reflex in sorted(claim_episodes, key=lambda e: e[2]):
        seq += 1
        leaf = 'reflex-broadcast' if reflex else acct_window(debtor)
        acct = "liabilities:claims:%s:%s" % (leaf, slug)
        tag = "claim:%s debtor:%s opened:%s%s" % (slug, debtor,
                ots.strftime('%Y-%m-%dT%H:%M:%SZ'), " reflex-broadcast" if reflex else "")
        lines.append("%s * claim opened: %s  ; %s" % (ots.strftime('%Y-%m-%d'), slug, tag))
        lines.append("    %s  1 CLAIM" % acct)
        lines.append("    %s  -1 CLAIM" % "equity:claims")
        lines.append("")
        if cts is not None:
            lag = round((cts - ots).total_seconds()/3600.0, 1)
            lines.append("%s * claim redeemed: %s  ; claim:%s redeemed:%s lag:%sh" % (
                cts.strftime('%Y-%m-%d'), slug, slug, cts.strftime('%Y-%m-%dT%H:%M:%SZ'), lag))
            lines.append("    %s  -1 CLAIM" % acct)
            lines.append("    %s  1 CLAIM" % "equity:claims")
            lines.append("")

# NEW:
    for debtor, slug, ots, cts, hl, reflex, outcome in sorted(claim_episodes, key=lambda e: e[2]):
        seq += 1
        leaf = 'reflex-broadcast' if reflex else acct_window(debtor)
        acct = "liabilities:claims:%s:%s" % (leaf, slug)
        tag = "claim:%s debtor:%s opened:%s%s" % (slug, debtor,
                ots.strftime('%Y-%m-%dT%H:%M:%SZ'), " reflex-broadcast" if reflex else "")
        lines.append("%s * claim opened: %s  ; %s" % (ots.strftime('%Y-%m-%d'), slug, tag))
        lines.append("    %s  1 CLAIM" % acct)
        lines.append("    %s  -1 CLAIM" % "equity:claims")
        lines.append("")
        if cts is not None:
            lag = round((cts - ots).total_seconds()/3600.0, 1)
            eq = {'kept': 'equity:claims', 'writeoff': 'equity:claims:writeoff',
                  'reroute': 'equity:claims:reroute'}.get(outcome, 'equity:claims')
            verb = {'kept': 'redeemed', 'writeoff': 'written off', 'reroute': 'rerouted'}.get(outcome, 'redeemed')
            lines.append("%s * claim %s: %s  ; claim:%s outcome:%s closed:%s lag:%sh" % (
                cts.strftime('%Y-%m-%d'), verb, slug, slug, outcome or 'kept',
                cts.strftime('%Y-%m-%dT%H:%M:%SZ'), lag))
            lines.append("    %s  -1 CLAIM" % acct)
            lines.append("    %s  1 CLAIM" % eq)
            lines.append("")
```

- [ ] Edit the hold loop, around line 492-506:

```python
# OLD:
    for taker, slug, ots, cts, hl in sorted(hold_episodes, key=lambda e: e[2]):
        seq += 1
        acct = "liabilities:holds:%s:%s" % (acct_window(taker), slug)
        tag = "hold:%s taker:%s opened:%s" % (slug, taker, ots.strftime('%Y-%m-%dT%H:%M:%SZ'))
        lines.append("%s * hold taken: %s  ; %s" % (ots.strftime('%Y-%m-%d'), slug, tag))
        lines.append("    %s  1 HOLD" % acct)
        lines.append("    %s  -1 HOLD" % "equity:holds")
        lines.append("")
        if cts is not None:
            lag = round((cts - ots).total_seconds()/3600.0, 1)
            lines.append("%s * hold released: %s  ; hold:%s released:%s lag:%sh" % (
                cts.strftime('%Y-%m-%d'), slug, slug, cts.strftime('%Y-%m-%dT%H:%M:%SZ'), lag))
            lines.append("    %s  -1 HOLD" % acct)
            lines.append("    %s  1 HOLD" % "equity:holds")
            lines.append("")

# NEW:
    for taker, slug, ots, cts, hl, outcome in sorted(hold_episodes, key=lambda e: e[2]):
        seq += 1
        acct = "liabilities:holds:%s:%s" % (acct_window(taker), slug)
        tag = "hold:%s taker:%s opened:%s" % (slug, taker, ots.strftime('%Y-%m-%dT%H:%M:%SZ'))
        lines.append("%s * hold taken: %s  ; %s" % (ots.strftime('%Y-%m-%d'), slug, tag))
        lines.append("    %s  1 HOLD" % acct)
        lines.append("    %s  -1 HOLD" % "equity:holds")
        lines.append("")
        if cts is not None:
            lag = round((cts - ots).total_seconds()/3600.0, 1)
            # 'reroute' never appears here — hold reroute is refused at the CLI (Step 1.5); outcome
            # is always 'kept' or 'writeoff'. The dict still covers it for defensive completeness.
            eq = {'kept': 'equity:holds', 'writeoff': 'equity:holds:writeoff',
                  'reroute': 'equity:holds:reroute'}.get(outcome, 'equity:holds')
            verb = {'kept': 'released', 'writeoff': 'written off', 'reroute': 'rerouted'}.get(outcome, 'released')
            lines.append("%s * hold %s: %s  ; hold:%s outcome:%s closed:%s lag:%sh" % (
                cts.strftime('%Y-%m-%d'), verb, slug, slug, outcome or 'kept',
                cts.strftime('%Y-%m-%dT%H:%M:%SZ'), lag))
            lines.append("    %s  -1 HOLD" % acct)
            lines.append("    %s  1 HOLD" % eq)
            lines.append("")
```

- [ ] Run `mesh-promises --test`. Expected: **PASS** (all 23 existing assertions — tuple arity is
  consistent again, and every existing "kept" path now tags `outcome='kept'`, which the equity-leg
  dict maps straight back to the original `equity:{promises,claims,holds}` accounts, so the generated
  journal is byte-identical to before for every already-tested scenario).
- [ ] Commit: `git add scripts/mesh-promises && git commit -m "mesh-promises: tag episode outcomes (kept/writeoff/reroute) in the journal writer"`

### Step 1.4: Recognize `written-off:` / `rerouted:` admin-close bodies in the replay loop

- [ ] Add the regex near the top of the python heredoc, right after the `LINE` regex (around line 179):

```python
# OLD (line 179):
LINE = re.compile(r'^(\S+)\s+([^\s@]+)@(\S+)\s+::\s+\[(task|taking|done|verify|fyi|sense)\]\s*(.*)$')

# NEW:
LINE = re.compile(r'^(\S+)\s+([^\s@]+)@(\S+)\s+::\s+\[(task|taking|done|verify|fyi|sense)\]\s*(.*)$')

# ADMIN CLOSE (mesh-promises writeoff/reroute design, Component B): a [done] body of the form
# "written-off: <type> <key>/<slug> — <reason>" or "rerouted: <type> <key>/<slug> — to <new> (...)"
# is a deliberate admin action, NOT an inferred discharge — matched by EXACT type+key+slug (never
# fuzzy token-overlap) and recognized regardless of WHO posted it (the whole point: these items
# can never satisfy the normal same-owner/debtor/taker match, that's why they're stuck). <key> is
# owner for a promise, debtor for a claim, taker for a hold — always the string shown by --all/--json.
ADMIN_CLOSE_RE = re.compile(r'^(written-off|rerouted):\s*(promise|claim|hold)\s+([^/\s]+)/(\S+)')
```

- [ ] Insert the admin-close branch at the TOP of the `elif marker == 'done':` block, before the
  existing `hl = lead(body)` line (around line 335-336):

```python
# OLD:
    elif marker == 'done':
        hl = lead(body)
        dtoks = toks(body, cap=12)
        k = best_match(dtoks, sanitize(hl), owner)

# NEW:
    elif marker == 'done':
        m_admin = ADMIN_CLOSE_RE.match(body)
        if m_admin:
            action, atype, akey, aslug = m_admin.groups()
            outcome = 'writeoff' if action == 'written-off' else 'reroute'
            if atype == 'promise' and aslug in opens and opens[aslug]['owner'] == akey:
                o = opens.pop(aslug)
                episodes.append((o['owner'], o['slug'], o['ts'], ts, o['incident'], o['lead'], outcome))
            elif atype == 'claim' and akey in claims and aslug in claims[akey]:
                o = claims[akey].pop(aslug)
                claim_episodes.append((akey, aslug, o['ts'], ts, o['lead'], o['reflex'], outcome))
            elif atype == 'hold' and akey in holds and aslug in holds[akey]:
                o = holds[akey].pop(aslug)
                hold_episodes.append((akey, aslug, o['ts'], ts, o['lead'], outcome))
            # else: the admin-close named a key/slug that isn't currently open (already closed, a
            # stale replay of an already-processed line, or a hand-typed board post that didn't
            # match anything real). The bash CLI validates existence before ever posting this line,
            # so this is a defensive no-op here, not a crash — replay must never throw on unexpected
            # board content (same discipline as best_match returning None on no match).
            continue
        hl = lead(body)
        dtoks = toks(body, cap=12)
        k = best_match(dtoks, sanitize(hl), owner)
```

- [ ] Run `mesh-promises --test`. Expected: **PASS** — this branch is additive and only fires on
  bodies matching `ADMIN_CLOSE_RE`, which no existing fixture produces.
- [ ] Commit: `git add scripts/mesh-promises && git commit -m "mesh-promises: recognize written-off:/rerouted: admin-close bodies in [done] posts"`

### Step 1.5: `do_writeoff()` and `do_reroute()` bash functions + CLI wiring

- [ ] Add both functions to `scripts/mesh-promises`, right before the `case "${1:-}" in` dispatcher
  (currently around line 995). Insert this whole block:

```bash
# ============================ writeoff / reroute (Component B) ============================
# Both validate the exact open item exists (via a fresh --json replay) BEFORE posting anything —
# a typo'd slug must fail loudly, never silently no-op. Both post through mesh-chat (the board stays
# the sole source of truth) and then refresh the journal via do_feed so the ledger reflects the
# close immediately rather than waiting for the next hourly cron tick.
_lookup_open(){ # $1=jsonfile $2=type $3=key $4=slug → prints the item's 'lead' on stdout, rc0 if found
  python3 - "$1" "$2" "$3" "$4" <<'PY'
import sys, json
jt, typ, key, slug = sys.argv[1:5]
try: j = json.load(open(jt))
except Exception: sys.exit(1)
listkey, keyfield = {'promise': ('open', 'owner'), 'claim': ('claims', 'debtor'),
                      'hold': ('holds', 'taker')}[typ]
rows = j.get(listkey, [])
match = next((r for r in rows if r.get(keyfield) == key and r.get('slug') == slug), None)
if match is None: sys.exit(1)
print(match.get('lead', slug))
PY
}

do_writeoff(){ # $1=promise|claim|hold $2=<key>/<slug> --reason "<text>"
  local type="${1:-}" ownerslug="${2:-}" reason=""
  case "$type" in
    promise|claim|hold) ;;
    *) echo "usage: mesh-promises --writeoff <promise|claim|hold> <owner>/<slug> --reason \"<text>\"" >&2; return 2;;
  esac
  shift 2 2>/dev/null || { echo "mesh-promises --writeoff: missing <owner>/<slug>" >&2; return 2; }
  case "${1:-}" in --reason) reason="${2:-}";; *) echo "mesh-promises --writeoff: missing --reason \"<text>\"" >&2; return 2;; esac
  [ -n "$reason" ] || { echo "mesh-promises --writeoff: --reason must be non-empty" >&2; return 2; }
  local owner="${ownerslug%%/*}" slug="${ownerslug#*/}"
  [ -n "$owner" ] && [ -n "$slug" ] && [ "$owner/$slug" = "$ownerslug" ] || {
    echo "mesh-promises --writeoff: expects <owner>/<slug>, got '$ownerslug'" >&2; return 2; }
  have mesh-chat || { echo "mesh-promises --writeoff: mesh-chat not found — cannot post to board" >&2; return 2; }
  local jt lead; jt="$(mktemp)"; do_json > "$jt" 2>/dev/null
  lead="$(_lookup_open "$jt" "$type" "$owner" "$slug")"; rm -f "$jt"
  if [ -z "$lead" ]; then
    echo "mesh-promises --writeoff: no open $type '$owner/$slug' found — nothing to write off (check --all for the exact owner/slug)" >&2
    return 1
  fi
  mesh-chat "[done] written-off: $type $owner/$slug — $reason" >/dev/null 2>&1
  echo "mesh-promises --writeoff: posted written-off for $type $owner/$slug — refreshing ledger"
  do_feed
}

do_reroute(){ # $1=promise|claim $2=<key>/<slug> --owner <new-window> --reason "<text>"
  local type="${1:-}" ownerslug="${2:-}" newowner="" reason=""
  case "$type" in
    promise|claim) ;;
    hold) echo "mesh-promises --reroute: hold cannot be rerouted — a HOLD's taker is whoever actually posted [taking], not body text, so nothing can repost it as a different window without impersonating that window. Use: mesh-promises --writeoff hold $ownerslug --reason \"...\", then have the new window post its own [taking] $/${ownerslug#*/}: ... to pick it up." >&2; return 2;;
    *) echo "usage: mesh-promises --reroute <promise|claim> <owner>/<slug> --owner <new-window> --reason \"<text>\"" >&2; return 2;;
  esac
  shift 2 2>/dev/null || { echo "mesh-promises --reroute: missing <owner>/<slug>" >&2; return 2; }
  while [ $# -gt 0 ]; do
    case "$1" in
      --owner) newowner="${2:-}"; shift 2;;
      --reason) reason="${2:-}"; shift 2;;
      *) echo "mesh-promises --reroute: unrecognized argument '$1'" >&2; return 2;;
    esac
  done
  [ -n "$newowner" ] || { echo "mesh-promises --reroute: --owner <new-window> is required" >&2; return 2; }
  [ -n "$reason" ] || { echo "mesh-promises --reroute: --reason must be non-empty" >&2; return 2; }
  local owner="${ownerslug%%/*}" slug="${ownerslug#*/}"
  [ -n "$owner" ] && [ -n "$slug" ] && [ "$owner/$slug" = "$ownerslug" ] || {
    echo "mesh-promises --reroute: expects <owner>/<slug>, got '$ownerslug'" >&2; return 2; }
  have mesh-chat || { echo "mesh-promises --reroute: mesh-chat not found — cannot post to board" >&2; return 2; }
  local roster; roster="$(roster_windows)"
  if [ -n "$roster" ]; then
    case " $roster " in
      *" $newowner "*) ;;
      *) echo "mesh-promises --reroute: '$newowner' is not a roster window (accounts.journal) — assign a real owner" >&2; return 2;;
    esac
  fi
  local jt lead; jt="$(mktemp)"; do_json > "$jt" 2>/dev/null
  lead="$(_lookup_open "$jt" "$type" "$owner" "$slug")"; rm -f "$jt"
  if [ -z "$lead" ]; then
    echo "mesh-promises --reroute: no open $type '$owner/$slug' found — nothing to reroute (check --all for the exact owner/slug)" >&2
    return 1
  fi
  mesh-chat "[done] rerouted: $type $owner/$slug — to $newowner ($reason)" >/dev/null 2>&1
  case "$type" in
    promise) mesh-chat "[task] $lead. owner: $newowner" >/dev/null 2>&1;;
    claim)   mesh-chat "[verify] $newowner: $lead" >/dev/null 2>&1;;
  esac
  echo "mesh-promises --reroute: posted reroute for $type $owner/$slug -> $newowner — refreshing ledger"
  do_feed
}
```

- [ ] Wire the two new subcommands into the dispatcher (around line 995-1005):

```bash
# OLD:
case "${1:-}" in
  --feed)        do_feed;;
  --report|"")   do_report;;
  --all)         do_all;;
  --balance)     do_balance;;
  --json)        do_json;;
  --check)       do_check;;
  --dash)        do_dash;;
  --test)        do_test;;
  -h|--help)     sed -n '2,55p' "$0";;
  *) echo "usage: mesh-promises [--report|--all|--balance|--feed|--check|--dash|--json|--test]" >&2; exit 2;;
esac

# NEW:
case "${1:-}" in
  --feed)        do_feed;;
  --report|"")   do_report;;
  --all)         do_all;;
  --balance)     do_balance;;
  --json)        do_json;;
  --check)       do_check;;
  --dash)        do_dash;;
  --writeoff)    shift; do_writeoff "$@";;
  --reroute)     shift; do_reroute "$@";;
  --test)        do_test;;
  -h|--help)     sed -n '2,55p' "$0";;
  *) echo "usage: mesh-promises [--report|--all|--balance|--feed|--check|--dash|--json|--writeoff|--reroute|--test]" >&2; exit 2;;
esac
```

- [ ] Run `mesh-promises --test`. Expected: **PASS** (unrelated to the new subcommands; confirms
  nothing broke wiring the dispatcher).
- [ ] Commit: `git add scripts/mesh-promises && git commit -m "mesh-promises: add --writeoff/--reroute CLI (Component B)"`

### Step 1.6: Declare the new equity accounts in `accounts.journal`

- [ ] Edit `scripts/accounts.journal` around line 107-115:

```
# OLD:
; ---- quarantine + balancing accounts ----
account liabilities:promises:unrouted   ; a [task] whose owner: is NOT a roster window — VISIBLE, not a phantom named account
account equity:promises                 ; the balancing leg for PROMISE open/keep (mesh-promises)
account liabilities:claims:unrouted     ; a [verify] addressed to a NON-roster window — VISIBLE, not a phantom named account
account liabilities:claims:reflex-broadcast   ; a [verify] with NO addressable target — a structural dead-letter, never
                                               ; redeemable by construction (no window can ever post AS reflex-broadcast)
account equity:claims                   ; the balancing leg for CLAIM open/redeem (mesh-promises)
account liabilities:holds:unrouted      ; a [taking] by a NON-roster/retired window — VISIBLE, not a phantom named account
account equity:holds                    ; the balancing leg for HOLD take/release (mesh-promises)

# NEW:
; ---- quarantine + balancing accounts ----
account liabilities:promises:unrouted   ; a [task] whose owner: is NOT a roster window — VISIBLE, not a phantom named account
account equity:promises                 ; the balancing leg for PROMISE open/keep (mesh-promises)
account equity:promises:writeoff        ; balancing leg for an admin --writeoff (distinct from a genuine keep)
account equity:promises:reroute         ; balancing leg for an admin --reroute close (distinct from writeoff and keep)
account liabilities:claims:unrouted     ; a [verify] addressed to a NON-roster window — VISIBLE, not a phantom named account
account liabilities:claims:reflex-broadcast   ; a [verify] with NO addressable target — a structural dead-letter, never
                                               ; redeemable by construction (no window can ever post AS reflex-broadcast)
account equity:claims                   ; the balancing leg for CLAIM open/redeem (mesh-promises)
account equity:claims:writeoff          ; balancing leg for an admin --writeoff (distinct from a genuine redemption)
account equity:claims:reroute           ; balancing leg for an admin --reroute close (distinct from writeoff and keep)
account liabilities:holds:unrouted      ; a [taking] by a NON-roster/retired window — VISIBLE, not a phantom named account
account equity:holds                    ; the balancing leg for HOLD take/release (mesh-promises)
account equity:holds:writeoff           ; balancing leg for an admin --writeoff (hold has no --reroute leg — see CLAUDE.md-adjacent design note)
```

- [ ] Copy the change to the deployed copy too so a live node picks it up without a redeploy step:
  `cp scripts/accounts.journal ~/.mesh/accounts.journal` (only if `~/.mesh/accounts.journal` already
  exists on this node — `seed_accounts_journal()` in `mesh-promises` already handles first-plant).
- [ ] Run `mesh-promises --check`. Expected: parity/agreement all PASS, roster section unchanged
  (this file isn't yet exercised by a writeoff/reroute in the live board, so no behavior change yet —
  this step is purely declaring the accounts other steps' journals will reference).
- [ ] Commit: `git add scripts/accounts.journal && git commit -m "accounts.journal: declare equity:*:writeoff/reroute legs"`

### Step 1.7: RED-first tests for writeoff/reroute (spec tests 1-4, 4b)

- [ ] Add these assertions to `do_test()` in `scripts/mesh-promises`, after the existing test 23
  (the claim+hold journal parity/agreement test) and before `echo "smoke-test: ok"; exit 0`:

```bash
  # ============= writeoff / reroute (Component B, 2026-07-24) =============

  # 24) WRITEOFF a reflex-broadcast claim (structurally undischargeable — no poster can ever match
  #     it via the normal "FROM the debtor" rule). Recognized regardless of WHO posts the admin-close.
  cat > "$t/boardw1" <<'EOF'
2026-07-20T00:00:00Z  load-audit@n  ::  [verify] [JUNK-LOAD] sustained load average 22.4 for 44 hours — investigate.
2026-07-24T10:00:00Z  witness@n     ::  [done] written-off: claim reflex-broadcast/junk-load — noise, load spike was transient and self-resolved
EOF
  local jfw1="$t/jw1.journal"
  replay journal "$t/boardw1" "$NOW" 24 6 1 "$jfw1" >/dev/null
  hledger -f "$jfw1" check >/dev/null 2>&1 || { echo "smoke-test: FAIL (writeoff journal does not balance)"; hledger -f "$jfw1" check 2>&1 | sed 's/^/    /'; exit 1; }
  grep -q 'equity:claims:writeoff' "$jfw1" || { echo "smoke-test: FAIL (writeoff did not book to equity:claims:writeoff)"; grep equity "$jfw1" | sed 's/^/    /'; exit 1; }
  grep -q '  -1 CLAIM' "$jfw1" || { echo "smoke-test: FAIL (writeoff did not close the liability)"; exit 1; }
  local ow1; ow1="$(replay counts "$t/boardw1" "$NOW" 24 6 1)"
  echo "$ow1" | grep -q 'claim_open=0' || { echo "smoke-test: FAIL (written-off claim still counted open: $ow1)"; exit 1; }

  # 25) WRITEOFF on a slug that never existed → journal has NOTHING for it (defensive no-op, not a crash)
  cat > "$t/boardw2" <<'EOF'
2026-07-24T10:00:00Z  witness@n  ::  [done] written-off: promise ghost-owner/does-not-exist — nothing to see here
EOF
  local jfw2="$t/jw2.journal"
  replay journal "$t/boardw2" "$NOW" 24 6 1 "$jfw2" >/dev/null
  hledger -f "$jfw2" check >/dev/null 2>&1 || { echo "smoke-test: FAIL (bogus writeoff crashed journal generation)"; exit 1; }
  grep -q 'ghost-owner' "$jfw2" && { echo "smoke-test: FAIL (bogus writeoff on a never-open slug produced a phantom booking)"; grep ghost-owner "$jfw2"; exit 1; }

  # 26) REROUTE a promise: closes old via equity:promises:reroute, the reopened [task] under the new
  #     owner books to the new owner's account under the SAME slug (threads as one continuing obligation).
  cat > "$t/boardw3" <<'EOF'
2026-07-23T00:00:00Z  tg@n       ::  [task] fix the redmi ssh key rotation. owner: operator
2026-07-24T10:00:00Z  witness@n  ::  [done] rerouted: promise operator/redmi-ssh-key — to genome (operator isn't a roster window)
2026-07-24T10:00:05Z  witness@n  ::  [task] fix the redmi ssh key rotation. owner: genome
EOF
  local jfw3="$t/jw3.journal"
  MESH_PROMISE_ROSTER="tg genome witness senses health discover sound pub vpn tg-roz" \
    replay journal "$t/boardw3" "$NOW" 24 6 1 "$jfw3" >/dev/null
  hledger -f "$jfw3" check >/dev/null 2>&1 || { echo "smoke-test: FAIL (reroute journal does not balance)"; hledger -f "$jfw3" check 2>&1 | sed 's/^/    /'; exit 1; }
  grep -q 'equity:promises:reroute' "$jfw3" || { echo "smoke-test: FAIL (reroute did not book to equity:promises:reroute)"; grep equity "$jfw3" | sed 's/^/    /'; exit 1; }
  grep -q 'liabilities:promises:genome:redmi-ssh-key' "$jfw3" || { echo "smoke-test: FAIL (rerouted promise did not reopen under the new owner's account)"; grep liabilities "$jfw3" | sed 's/^/    /'; exit 1; }
  local ow3; ow3="$(replay counts "$t/boardw3" "$NOW" 24 6 1)"
  echo "$ow3" | grep -q 'open=1' || { echo "smoke-test: FAIL (reroute should leave exactly 1 open promise (the reopened one): $ow3)"; exit 1; }

  # 27) REROUTE a hold is REFUSED by construction (poster-identity finding) — do_reroute must reject
  #     type=hold before any lookup, and do_writeoff hold must still work on the same fixture.
  export MESH_DIR="$t/mesh_wo"; mkdir -p "$MESH_DIR"
  cat > "$t/board" <<'EOF'
2026-07-23T00:00:00Z  chat@n  ::  [taking] quota-idle-verdict: chat — investigating the idle governor hold.
EOF
  CHAT_LOG="$t/board" PROM_DIR="$MESH_DIR/promises" JOURNAL="$MESH_DIR/promises/promises.journal" \
    STATE="$MESH_DIR/.promises-state" SUMMARY="$MESH_DIR/.promises-summary" LEAKS_CACHE="$MESH_DIR/.promises-leaks" \
    do_reroute hold chat/quota-idle-verdict --owner senses --reason "chat is retired" 2>"$t/reroute.err"
  local rr_rc=$?
  [ "$rr_rc" -ne 0 ] || { echo "smoke-test: FAIL (do_reroute accepted type=hold — should be refused)"; exit 1; }
  grep -q 'cannot be rerouted' "$t/reroute.err" || { echo "smoke-test: FAIL (do_reroute hold refusal message missing the poster-identity explanation)"; cat "$t/reroute.err"; exit 1; }
  unset MESH_DIR CHAT_LOG PROM_DIR JOURNAL STATE SUMMARY LEAKS_CACHE
```

- [ ] Run `mesh-promises --test`. Expected: assertions 24-26 exercise the python replay directly
  (same pattern as the existing suite) and should **PASS** immediately since Steps 1.1-1.4 are
  already in place. Assertion 27 exercises the bash `do_reroute` function directly by sourcing its
  env — if `--test` runs in a subshell where `do_reroute`/`CHAT_LOG` etc. aren't overridable this
  way, adjust to call `bash scripts/mesh-promises --reroute hold ...` as a subprocess with
  `MESH_CHAT_LOG`/`MESH_PROMISES_DIR` env overrides instead (the pattern the rest of `do_test()`
  uses for `MESH_PROMISE_NO_POST=1`) — verify which the file's existing test harness actually
  supports before assuming the inline-function-call form works standalone.
- [ ] If assertion 27 needs adjustment per the note above, fix it now and re-run until green.
- [ ] Commit: `git add scripts/mesh-promises && git commit -m "mesh-promises: RED-first tests for writeoff/reroute (tests 24-27)"`

---

## Task 2: `mesh-promises` — Component A: uniform unrouted accounting for claims/holds

**Files:**
- Modify: `scripts/mesh-promises` (python: `claim_open_list`/`hold_open_list` construction, `counts`/
  `json` mode output; bash: `do_check()`, the `--all` glyphs in python's `mode == 'all'` block)

**Interfaces:**
- Consumes: `is_unrouted()` (already exists, line 163).
- Produces: `claim_unrouted_open`, `hold_unrouted_open` python ints; `unrouted: bool` field on every
  `claim_open_list`/`hold_open_list` row; `claim_unrouted=<n> hold_unrouted=<n>` in `counts` mode
  output (parsed by `do_check` the same way `unrouted=<n>` already is).

### Step 2.1: Compute unrouted booleans/counts for claims and holds

- [ ] Edit the claim-building loop around line 403-413:

```python
# OLD:
claim_open_list = []
for debtor, pool in claims.items():
    for slug, o in pool.items():
        claim_episodes.append((debtor, slug, o['ts'], None, o['lead'], o['reflex'], None))
        age_h = (now - o['ts']).total_seconds() / 3600.0
        claim_open_list.append(dict(debtor=debtor, slug=slug, lead=o['lead'],
                                    opened=o['ts'].strftime('%Y-%m-%dT%H:%M:%SZ'),
                                    age_h=round(age_h,1), reflex=o['reflex'],
                                    threshold_h=CLAIM_H, leaked=age_h > CLAIM_H))
claim_open_list.sort(key=lambda x: -x['age_h'])
claim_leaks = [x for x in claim_open_list if x['leaked']]

# NEW:
claim_open_list = []
for debtor, pool in claims.items():
    for slug, o in pool.items():
        claim_episodes.append((debtor, slug, o['ts'], None, o['lead'], o['reflex'], None))
        age_h = (now - o['ts']).total_seconds() / 3600.0
        # reflex-broadcast is a DEDICATED structural account, never conflated with a misrouted
        # owner — is_unrouted() would also flag it (it's not a roster window either), so exclude
        # it explicitly rather than double-counting one leak class as two.
        unr = (not o['reflex']) and is_unrouted(debtor)
        claim_open_list.append(dict(debtor=debtor, slug=slug, lead=o['lead'],
                                    opened=o['ts'].strftime('%Y-%m-%dT%H:%M:%SZ'),
                                    age_h=round(age_h,1), reflex=o['reflex'], unrouted=unr,
                                    threshold_h=CLAIM_H, leaked=age_h > CLAIM_H))
claim_open_list.sort(key=lambda x: -x['age_h'])
claim_leaks = [x for x in claim_open_list if x['leaked']]
claim_unrouted_open = sum(1 for x in claim_open_list if x['unrouted'])
```

- [ ] Edit the hold-building loop around line 415-424:

```python
# OLD:
hold_open_list = []
for taker, pool in holds.items():
    for slug, o in pool.items():
        hold_episodes.append((taker, slug, o['ts'], None, o['lead'], None))
        age_h = (now - o['ts']).total_seconds() / 3600.0
        hold_open_list.append(dict(taker=taker, slug=slug, lead=o['lead'],
                                   opened=o['ts'].strftime('%Y-%m-%dT%H:%M:%SZ'),
                                   age_h=round(age_h,1), threshold_h=leak_h, leaked=age_h > leak_h))
hold_open_list.sort(key=lambda x: -x['age_h'])
hold_leaks = [x for x in hold_open_list if x['leaked']]

# NEW:
hold_open_list = []
for taker, pool in holds.items():
    for slug, o in pool.items():
        hold_episodes.append((taker, slug, o['ts'], None, o['lead'], None))
        age_h = (now - o['ts']).total_seconds() / 3600.0
        unr = is_unrouted(taker)
        hold_open_list.append(dict(taker=taker, slug=slug, lead=o['lead'],
                                   opened=o['ts'].strftime('%Y-%m-%dT%H:%M:%SZ'),
                                   age_h=round(age_h,1), threshold_h=leak_h, leaked=age_h > leak_h,
                                   unrouted=unr))
hold_open_list.sort(key=lambda x: -x['age_h'])
hold_leaks = [x for x in hold_open_list if x['leaked']]
hold_unrouted_open = sum(1 for x in hold_open_list if x['unrouted'])
```

### Step 2.2: Surface the new counts in `counts` and `json` mode

- [ ] Edit `counts` mode around line 428-431:

```python
# OLD:
if mode == 'counts':
    print("open=%d leak=%d unrouted=%d claim_open=%d claim_leak=%d hold_open=%d hold_leak=%d" % (
        len(open_list), len(leaks), unrouted_open,
        len(claim_open_list), len(claim_leaks), len(hold_open_list), len(hold_leaks)))
    sys.exit(0)

# NEW:
if mode == 'counts':
    print("open=%d leak=%d unrouted=%d claim_open=%d claim_leak=%d claim_unrouted=%d "
          "hold_open=%d hold_leak=%d hold_unrouted=%d" % (
        len(open_list), len(leaks), unrouted_open,
        len(claim_open_list), len(claim_leaks), claim_unrouted_open,
        len(hold_open_list), len(hold_leaks), hold_unrouted_open))
    sys.exit(0)
```

- [ ] `json` mode (line 433-439) needs no change — `claims`/`holds` rows already carry the new
  `unrouted` field from Step 2.1, and `json.dumps(dict(...))` serializes it automatically.
- [ ] The `journal` mode's own counts-line (line 510-517) is used by `do_feed`'s `write_summary` via
  regex extraction (`grep -oE 'unrouted=[0-9]+'`) — since that pattern is UNANCHORED, and the new
  `claim_unrouted=`/`hold_unrouted=` tokens also end in `unrouted=<n>`, this WILL now false-match
  inside `write_summary`. Fix `write_summary`'s promise-unrouted extraction in Step 2.4 below before
  this becomes a live bug — do not skip it.

### Step 2.3: `--all` report glyphs (🧭 vs 🔴)

- [ ] Edit the `mode == 'all'` block around line 526-537:

```python
# OLD:
    if claim_open_list:
        print("  -- claims ([verify] owed, %d self-check(s) skipped) --" % claim_self_skipped)
        print("  %-14s %6s %3s  %s" % ("debtor","age_h","!","claim"))
        for x in claim_open_list:
            flag = "🔴" if x['leaked'] else ("B" if x['reflex'] else " ")
            print("  %-14s %6.1f %3s  %s" % (x['debtor'], x['age_h'], flag, x['lead']))
    if hold_open_list:
        print("  -- holds ([taking] held, %d content-free skipped) --" % hold_skipped)
        print("  %-14s %6s %3s  %s" % ("taker","age_h","!","hold"))
        for x in hold_open_list:
            flag = "🔴" if x['leaked'] else " "
            print("  %-14s %6.1f %3s  %s" % (x['taker'], x['age_h'], flag, x['lead']))
    sys.exit(0)

# NEW:
    if claim_open_list:
        print("  -- claims ([verify] owed, %d self-check(s) skipped) --" % claim_self_skipped)
        print("  %-14s %6s %3s  %s" % ("debtor","age_h","!","claim"))
        for x in claim_open_list:
            flag = "🧭" if x['unrouted'] else ("🔴" if x['leaked'] else ("B" if x['reflex'] else " "))
            print("  %-14s %6.1f %3s  %s" % (x['debtor'], x['age_h'], flag, x['lead']))
    if hold_open_list:
        print("  -- holds ([taking] held, %d content-free skipped) --" % hold_skipped)
        print("  %-14s %6s %3s  %s" % ("taker","age_h","!","hold"))
        for x in hold_open_list:
            flag = "🧭" if x['unrouted'] else ("🔴" if x['leaked'] else " ")
            print("  %-14s %6.1f %3s  %s" % (x['taker'], x['age_h'], flag, x['lead']))
    sys.exit(0)
```

- [ ] The promise loop just above (line 523-525) also needs the same 🧭 treatment for consistency
  (today it only shows 🔴/‼). Edit:

```python
# OLD:
    for x in open_list:
        flag = "🔴" if x['leaked'] else ("‼" if x['incident'] else " ")
        print("  %-10s %6.1f %3s  %s" % (x['owner'], x['age_h'], flag, x['lead']))

# NEW:
    for x in open_list:
        flag = "🧭" if is_unrouted(x['owner']) else ("🔴" if x['leaked'] else ("‼" if x['incident'] else " "))
        print("  %-10s %6.1f %3s  %s" % (x['owner'], x['age_h'], flag, x['lead']))
```

### Step 2.4: `do_check` and `write_summary` (bash)

- [ ] Edit `write_summary()` around line 645-661 — fix the now-ambiguous `unrouted=` extraction
  (Step 2.2's note) and surface the two new counts:

```bash
# OLD:
write_summary(){
  local counts="$1"
  local open leak kept unrouted claim_open claim_leak hold_open hold_leak
  open="$(echo "$counts" | grep -oE '(^| )open=[0-9]+' | cut -d= -f2)"
  leak="$(echo "$counts" | grep -oE '(^| )leak=[0-9]+' | cut -d= -f2)"
  kept="$(echo "$counts" | grep -oE 'kept=[0-9]+' | cut -d= -f2)"
  unrouted="$(echo "$counts" | grep -oE 'unrouted=[0-9]+' | cut -d= -f2)"
  claim_open="$(echo "$counts" | grep -oE 'claim_open=[0-9]+' | cut -d= -f2)"
  claim_leak="$(echo "$counts" | grep -oE 'claim_leak=[0-9]+' | cut -d= -f2)"
  hold_open="$(echo "$counts" | grep -oE 'hold_open=[0-9]+' | cut -d= -f2)"
  hold_leak="$(echo "$counts" | grep -oE 'hold_leak=[0-9]+' | cut -d= -f2)"
  # unrouted only shown when >0 (the phantom-owner count — a number that grows, per the spec)
  local urseg=""; [ "${unrouted:-0}" -gt 0 ] 2>/dev/null && urseg=" · ${unrouted} unrouted"
  printf 'promises: %s open · %s LEAKED · %s kept%s · claims %s open/%s LEAKED · holds %s open/%s LEAKED · as of %s\n' \
    "${open:-?}" "${leak:-?}" "${kept:-?}" "$urseg" "${claim_open:-?}" "${claim_leak:-?}" \
    "${hold_open:-?}" "${hold_leak:-?}" "$(date -u +%H:%MZ)" > "$SUMMARY"
}

# NEW:
write_summary(){
  local counts="$1"
  local open leak kept unrouted claim_open claim_leak claim_unrouted hold_open hold_leak hold_unrouted
  open="$(echo "$counts" | grep -oE '(^| )open=[0-9]+' | cut -d= -f2)"
  leak="$(echo "$counts" | grep -oE '(^| )leak=[0-9]+' | cut -d= -f2)"
  kept="$(echo "$counts" | grep -oE 'kept=[0-9]+' | cut -d= -f2)"
  # ANCHORED: "unrouted=" alone is now ambiguous (also a suffix of "claim_unrouted="/"hold_unrouted=").
  # Same substring-scan trap the "open=" anchor comment above already documents — match the promise
  # token specifically via its own leading boundary.
  unrouted="$(echo "$counts" | grep -oE '(^| )unrouted=[0-9]+' | cut -d= -f2)"
  claim_open="$(echo "$counts" | grep -oE 'claim_open=[0-9]+' | cut -d= -f2)"
  claim_leak="$(echo "$counts" | grep -oE 'claim_leak=[0-9]+' | cut -d= -f2)"
  claim_unrouted="$(echo "$counts" | grep -oE 'claim_unrouted=[0-9]+' | cut -d= -f2)"
  hold_open="$(echo "$counts" | grep -oE 'hold_open=[0-9]+' | cut -d= -f2)"
  hold_leak="$(echo "$counts" | grep -oE 'hold_leak=[0-9]+' | cut -d= -f2)"
  hold_unrouted="$(echo "$counts" | grep -oE 'hold_unrouted=[0-9]+' | cut -d= -f2)"
  # unrouted only shown when >0 (the phantom-owner count — a number that grows, per the spec)
  local urseg=""; [ "${unrouted:-0}" -gt 0 ] 2>/dev/null && urseg=" · ${unrouted} unrouted"
  local curseg=""; [ "${claim_unrouted:-0}" -gt 0 ] 2>/dev/null && curseg=" (${claim_unrouted} unrouted)"
  local hurseg=""; [ "${hold_unrouted:-0}" -gt 0 ] 2>/dev/null && hurseg=" (${hold_unrouted} unrouted)"
  printf 'promises: %s open · %s LEAKED · %s kept%s · claims %s open/%s LEAKED%s · holds %s open/%s LEAKED%s · as of %s\n' \
    "${open:-?}" "${leak:-?}" "${kept:-?}" "$urseg" "${claim_open:-?}" "${claim_leak:-?}" "$curseg" \
    "${hold_open:-?}" "${hold_leak:-?}" "$hurseg" "$(date -u +%H:%MZ)" > "$SUMMARY"
}
```

  **Note the `journal` mode's counts-line format string** (Step "1.3"'s untouched `print("open=%d
  leak=%d kept=%d unkeyed_done=%d unrouted=%d claim_open=%d claim_leak=%d claim_reflex=%d
  claim_self=%d hold_open=%d hold_leak=%d hold_skip=%d" % (...))` around line 510) does **not**
  currently emit `claim_unrouted=`/`hold_unrouted=` — only `counts` mode does (Step 2.2). Since
  `do_feed`'s `write_summary "$counts"` call passes the output of `do_materialize` (which runs
  `journal` mode, not `counts` mode), `write_summary` as patched above will find `claim_unrouted`/
  `hold_unrouted` **empty** on the live `--feed` path even though Step 2.2 added them to `counts`
  mode. Fix: add the same two fields to `journal` mode's print statement too, so both modes agree —
  edit line 510-517:

```python
# OLD:
    print("open=%d leak=%d kept=%d unkeyed_done=%d unrouted=%d "
          "claim_open=%d claim_leak=%d claim_reflex=%d claim_self=%d "
          "hold_open=%d hold_leak=%d hold_skip=%d" % (
        len(open_list), len(leaks), kept, unkeyed_done, unrouted_open,
        len(claim_open_list), len(claim_leaks),
        sum(1 for x in claim_open_list if x['reflex']), claim_self_skipped,
        len(hold_open_list), len(hold_leaks), hold_skipped))
    sys.exit(0)

# NEW:
    print("open=%d leak=%d kept=%d unkeyed_done=%d unrouted=%d "
          "claim_open=%d claim_leak=%d claim_unrouted=%d claim_reflex=%d claim_self=%d "
          "hold_open=%d hold_leak=%d hold_unrouted=%d hold_skip=%d" % (
        len(open_list), len(leaks), kept, unkeyed_done, unrouted_open,
        len(claim_open_list), len(claim_leaks), claim_unrouted_open,
        sum(1 for x in claim_open_list if x['reflex']), claim_self_skipped,
        len(hold_open_list), len(hold_leaks), hold_unrouted_open, hold_skipped))
    sys.exit(0)
```

- [ ] Edit `do_check()`'s roster section around line 631-641 to also report claim/hold unrouted:

```bash
# OLD:
  local roster; roster="$(roster_windows)"
  local unrouted; unrouted="$(echo "$counts" | grep -oE 'unrouted=[0-9]+' | cut -d= -f2)"
  echo "== roster (owner: validated against accounts.journal) =="
  if [ -z "$roster" ]; then echo "  roster: INACTIVE (no accounts.journal found — owners trusted as-is, fail-open)"
  elif [ "${unrouted:-0}" -gt 0 ]; then
    echo "  roster: $unrouted open promise(s) owned by NON-roster windows → liabilities:promises:unrouted (assign an owner or retire the task):"
    hledger -f "$JOURNAL" balance liabilities:promises:unrouted --no-total 2>/dev/null | grep -v ' 0 ' | sed 's/^/    /'
  else echo "  roster: clean (every open promise owned by a declared window)"; fi
  exit 0
}

# NEW:
  local roster; roster="$(roster_windows)"
  local unrouted claim_unrouted hold_unrouted
  unrouted="$(echo "$counts" | grep -oE '(^| )unrouted=[0-9]+' | cut -d= -f2)"
  claim_unrouted="$(echo "$counts" | grep -oE 'claim_unrouted=[0-9]+' | cut -d= -f2)"
  hold_unrouted="$(echo "$counts" | grep -oE 'hold_unrouted=[0-9]+' | cut -d= -f2)"
  echo "== roster (owner: validated against accounts.journal) =="
  if [ -z "$roster" ]; then echo "  roster: INACTIVE (no accounts.journal found — owners trusted as-is, fail-open)"
  else
    local any_unrouted=0
    if [ "${unrouted:-0}" -gt 0 ]; then
      any_unrouted=1
      echo "  roster: $unrouted open promise(s) owned by NON-roster windows → liabilities:promises:unrouted (assign an owner or retire the task):"
      hledger -f "$JOURNAL" balance liabilities:promises:unrouted --no-total 2>/dev/null | grep -v ' 0 ' | sed 's/^/    /'
    fi
    if [ "${claim_unrouted:-0}" -gt 0 ]; then
      any_unrouted=1
      echo "  roster: $claim_unrouted open claim(s) addressed to NON-roster windows → liabilities:claims:unrouted:"
      hledger -f "$JOURNAL" balance liabilities:claims:unrouted --no-total 2>/dev/null | grep -v ' 0 ' | sed 's/^/    /'
    fi
    if [ "${hold_unrouted:-0}" -gt 0 ]; then
      any_unrouted=1
      echo "  roster: $hold_unrouted open hold(s) taken by NON-roster/retired windows → liabilities:holds:unrouted:"
      hledger -f "$JOURNAL" balance liabilities:holds:unrouted --no-total 2>/dev/null | grep -v ' 0 ' | sed 's/^/    /'
    fi
    [ "$any_unrouted" = 0 ] && echo "  roster: clean (every open promise/claim/hold owned by a declared window)"
  fi
  exit 0
}
```

- [ ] Run `mesh-promises --test`. Expected: **PASS** (existing test 14/15 promise-quarantine
  assertions are unaffected — they check `liabilities:promises:unrouted`/`liabilities:promises:bruno`
  journal accounts directly, not the `counts`/`write_summary` string parsing this step touched).
- [ ] Commit: `git add scripts/mesh-promises && git commit -m "mesh-promises: uniform unrouted accounting for claims/holds (Component A)"`

### Step 2.5: RED-first test for Component A (spec test 5)

- [ ] Add to `do_test()`, after the writeoff/reroute tests from Task 1:

```bash
  # 28) COMPONENT A: a non-roster [taking] taker AND a non-roster [verify] debtor both surface as
  #     unrouted in counts mode — today's fixture (test 14) only covered the promise case.
  cat > "$t/board9" <<'EOF'
2026-07-24T09:00:00Z  tg@n      ::  [taking] widget-audit: bruno — auditing on the retired window.
2026-07-24T09:05:00Z  tg@n      ::  [verify] bruno: check the widget subsystem is actually clean.
EOF
  local c9; c9="$(MESH_PROMISE_ROSTER="tg genome witness senses health discover sound pub vpn tg-roz" \
    replay counts "$t/board9" "$NOW" 24 6 1)"
  echo "$c9" | grep -q 'claim_unrouted=1' || { echo "smoke-test: FAIL (non-roster [verify] debtor not counted unrouted: $c9)"; exit 1; }
  echo "$c9" | grep -q 'hold_unrouted=1' || { echo "smoke-test: FAIL (non-roster [taking] taker not counted unrouted: $c9)"; exit 1; }

  # 29) reflex-broadcast must NOT double-count as unrouted (it's a dedicated structural account,
  #     not a misrouted owner) even though 'reflex-broadcast' also fails the roster check.
  cat > "$t/board10" <<'EOF'
2026-07-20T00:00:00Z  load-audit@n  ::  [verify] [JUNK-LOAD] sustained load average 22.4 for 44 hours — investigate.
EOF
  local c10; c10="$(MESH_PROMISE_ROSTER="tg genome witness senses health discover sound pub vpn tg-roz" \
    replay counts "$t/board10" "$NOW" 24 6 1)"
  echo "$c10" | grep -q 'claim_unrouted=0' || { echo "smoke-test: FAIL (reflex-broadcast double-counted as unrouted: $c10)"; exit 1; }
```

- [ ] Run `mesh-promises --test`. Expected: **PASS**.
- [ ] Commit: `git add scripts/mesh-promises && git commit -m "mesh-promises: RED-first tests for uniform unrouted accounting (tests 28-29)"`

---

## Task 3: `mesh-promises` — Component C: suggested-owner hint

**Files:**
- Modify: `scripts/mesh-promises` (python: new `charter_tokens()` / `suggest_owner()` functions, wire
  into `claim_open_list`/`hold_open_list`/`open_list` rows and the `--all` print loops)

**Interfaces:**
- Consumes: `ACCOUNTS_JOURNAL` path (already read by `roster_windows()` in bash; python needs its own
  read since the charter comments aren't currently passed into the python heredoc at all).
- Produces: `suggest: <window>|None` field on unrouted rows; printed inline in `--all`.

### Step 3.1: Pass the accounts.journal path into the python heredoc and parse charters

The python heredoc currently receives `MESH_PROMISE_ROSTER` (space-separated window list) via env
but never sees the charter comments themselves. Add a second env var carrying the raw file content
(simplest: pass the resolved path, python reads it directly — avoids re-plumbing through bash args).

- [ ] Edit the `replay()` bash function (line 140-141) to also export the accounts journal path:

```bash
# OLD (line 140-141):
replay(){
MESH_PROMISE_ROSTER="${MESH_PROMISE_ROSTER-$(roster_windows)}" MESH_CLAIM_LEAK_H="${MESH_CLAIM_LEAK_H:-$CLAIM_LEAK_H}" python3 - "$@" <<'PYEOF'

# NEW:
replay(){
local _af=""
[ -f "$ACCOUNTS_JOURNAL" ] && _af="$ACCOUNTS_JOURNAL"
[ -z "$_af" ] && [ -f "$_self_dir/accounts.journal" ] && _af="$_self_dir/accounts.journal"
MESH_PROMISE_ROSTER="${MESH_PROMISE_ROSTER-$(roster_windows)}" MESH_CLAIM_LEAK_H="${MESH_CLAIM_LEAK_H:-$CLAIM_LEAK_H}" \
  MESH_PROMISE_ACCOUNTS_FILE="${MESH_PROMISE_ACCOUNTS_FILE-$_af}" python3 - "$@" <<'PYEOF'
```

  (This duplicates `roster_windows()`'s file-resolution order rather than calling it, since
  `roster_windows()` already ran once for `MESH_PROMISE_ROSTER` above it and re-running a subshell
  function for a second env var in the same line is harder to read than repeating the two-line
  fallback — same effective logic, no new failure mode.)

- [ ] Add the charter parser + suggestion function to the python heredoc, right after the
  `is_unrouted`/`acct_window` functions (after line 166):

```python
# INSERT after line 166 (after `def acct_window(owner): ...`):

# SUGGESTED-OWNER HINT (Component C, read-only, advisory only — never posts, never reassigns).
# accounts.journal already carries a one-line charter comment per window's expenses:labour:<w>
# account (e.g. "sound — sound studio: records, grind, room music"). Token-overlap an unrouted
# item's lead against every window's charter using the SAME toks() tokenizer already used for
# done<->task matching, so Cyrillic/bilingual leads are handled identically everywhere in this file.
_CHARTER_LINE = re.compile(r'^account\s+expenses:labour:([a-z0-9-]+)\s*;\s*(.*)$')
CHARTERS = {}
_accounts_file = os.environ.get('MESH_PROMISE_ACCOUNTS_FILE', '')
if _accounts_file:
    try:
        for _ln in open(_accounts_file, errors='replace'):
            _m = _CHARTER_LINE.match(_ln.rstrip('\n'))
            if _m:
                CHARTERS[_m.group(1)] = toks(_m.group(2), cap=20)
    except FileNotFoundError:
        pass

def suggest_owner(lead_ktoks):
    # returns (window, score) of the best charter-overlap match, or (None, 0) if nothing overlaps —
    # "none" must print as none, never a low-confidence guess dressed up as a real suggestion (same
    # doctrine as every other no-match path in this file).
    best, best_score = None, 0
    for win, ctoks in CHARTERS.items():
        ov = len(set(lead_ktoks) & set(ctoks))
        if ov > best_score:
            best, best_score = win, ov
    return (best, best_score) if best_score > 0 else (None, 0)
```

### Step 3.2: Wire the suggestion into open-item rows and `--all` output

- [ ] Edit the still-open promise loop around line 388-396 to attach a suggestion when unrouted:

```python
# OLD:
open_list = []
for k,o in opens.items():
    episodes.append((o['owner'], o['slug'], o['ts'], None, o['incident'], o['lead'], None))
    age_h = (now - o['ts']).total_seconds() / 3600.0
    thr = incid_h if o['incident'] else leak_h
    open_list.append(dict(owner=o['owner'], slug=o['slug'], lead=o['lead'],
                          opened=o['ts'].strftime('%Y-%m-%dT%H:%M:%SZ'),
                          age_h=round(age_h,1), incident=o['incident'],
                          threshold_h=thr, leaked=age_h > thr))

# NEW:
open_list = []
for k,o in opens.items():
    episodes.append((o['owner'], o['slug'], o['ts'], None, o['incident'], o['lead'], None))
    age_h = (now - o['ts']).total_seconds() / 3600.0
    thr = incid_h if o['incident'] else leak_h
    sug, sug_score = suggest_owner(o['ktoks']) if is_unrouted(o['owner']) else (None, 0)
    open_list.append(dict(owner=o['owner'], slug=o['slug'], lead=o['lead'],
                          opened=o['ts'].strftime('%Y-%m-%dT%H:%M:%SZ'),
                          age_h=round(age_h,1), incident=o['incident'],
                          threshold_h=thr, leaked=age_h > thr,
                          suggest=sug, suggest_score=sug_score))
```

- [ ] Same pattern for claims (Step 2.1's edited block, add after the `unr = ...` line):

```python
# ADD right after (within the same claim-loop, after Step 2.1's `unr = (not o['reflex']) and is_unrouted(debtor)`):
        sug, sug_score = suggest_owner(o['ktoks']) if unr else (None, 0)
```

  and add `suggest=sug, suggest_score=sug_score` to that row's `dict(...)` call.

- [ ] Same pattern for holds (Step 2.1's edited block, add after `unr = is_unrouted(taker)`):

```python
        sug, sug_score = suggest_owner(o['ktoks']) if unr else (None, 0)
```

  and add `suggest=sug, suggest_score=sug_score` to that row's `dict(...)` call.

- [ ] Edit the `--all` promise print loop (Step 2.3's edited block) to show the suggestion inline:

```python
# OLD (from Step 2.3):
    for x in open_list:
        flag = "🧭" if is_unrouted(x['owner']) else ("🔴" if x['leaked'] else ("‼" if x['incident'] else " "))
        print("  %-10s %6.1f %3s  %s" % (x['owner'], x['age_h'], flag, x['lead']))

# NEW:
    for x in open_list:
        unr = is_unrouted(x['owner'])
        flag = "🧭" if unr else ("🔴" if x['leaked'] else ("‼" if x['incident'] else " "))
        sugtxt = ""
        if unr:
            sugtxt = "  (suggest: %s)" % x['suggest'] if x['suggest'] else "  (suggest: none — no charter overlap)"
        print("  %-10s %6.1f %3s  %s%s" % (x['owner'], x['age_h'], flag, x['lead'], sugtxt))
```

- [ ] Same treatment for the claim and hold `--all` loops (Step 2.3's edited blocks) — mirror the
  `unr`/`sugtxt` pattern above using `x['debtor']`/`x['taker']` in place of `x['owner']`.

- [ ] Run `mesh-promises --test`. Expected: **PASS**.
- [ ] Commit: `git add scripts/mesh-promises && git commit -m "mesh-promises: suggested-owner hint for unrouted items (Component C)"`

### Step 3.3: RED-first tests for Component C (spec test 6)

- [ ] Add to `do_test()`:

```bash
  # 30) COMPONENT C: an unrouted promise whose lead overlaps exactly one window's charter gets that
  #     window suggested; a lead with zero charter overlap gets "none", never a wrong guess.
  cat > "$t/board11" <<'EOF'
2026-07-24T09:00:00Z  tg@n  ::  [task] fix the sound studio grinder crashing on long records. owner: score
EOF
  local a11; a11="$(MESH_PROMISE_ROSTER="tg genome witness senses health discover sound pub vpn tg-roz" \
    MESH_PROMISE_ACCOUNTS_FILE="$_self_dir/accounts.journal" \
    replay all "$t/board11" "$NOW" 24 6 1)"
  echo "$a11" | grep -q 'suggest: sound' || { echo "smoke-test: FAIL (unrouted task with charter-overlapping lead did not suggest 'sound'): $a11"; exit 1; }

  cat > "$t/board12" <<'EOF'
2026-07-24T09:00:00Z  tg@n  ::  [task] xyzzy plugh frobnicate qux. owner: nonexistent-owner
EOF
  local a12; a12="$(MESH_PROMISE_ROSTER="tg genome witness senses health discover sound pub vpn tg-roz" \
    MESH_PROMISE_ACCOUNTS_FILE="$_self_dir/accounts.journal" \
    replay all "$t/board12" "$NOW" 24 6 1)"
  echo "$a12" | grep -q 'suggest: none' || { echo "smoke-test: FAIL (unrouted task with zero charter overlap did not print 'suggest: none'): $a12"; exit 1; }
```

  (Note: `_self_dir` is already a script-level bash variable, not visible inside the python heredoc
  or this bash-level test block by that name unless `do_test()` runs in the same shell scope — verify
  `_self_dir` is in scope at the point `do_test()` executes; if not, replace with the literal
  `"$(cd "$(dirname "$0")" && pwd)/accounts.journal"`.)

- [ ] Run `mesh-promises --test`. Expected: **PASS**.
- [ ] Commit: `git add scripts/mesh-promises && git commit -m "mesh-promises: RED-first tests for suggested-owner hint (test 30)"`

---

## Task 4: `mesh-promises` — Component D: confidence-gated auto-reaction in `--feed`

**Files:**
- Modify: `scripts/mesh-promises` (bash: `do_feed()` — new auto-reroute/auto-mute pass gated by
  `MESH_PROMISE_AUTOREACT`)

**Interfaces:**
- Consumes: `_lookup_open()` — no, actually consumes `do_json`'s already-materialized `unrouted`/
  `suggest`/`suggest_score` fields (Tasks 2-3) and `do_reroute()`/`do_writeoff()` are NOT reused
  directly here (auto-mute doesn't writeoff; auto-reroute reuses the SAME posting logic as
  `do_reroute` but must not go through its interactive-CLI argument validation path — factor the
  posting logic out).
- Produces: env vars `MESH_PROMISE_AUTOREACT`, `MESH_PROMISE_AUTOREROUTE_MARGIN` (default 2),
  `MESH_PROMISE_AUTOREROUTE_MIN` (default 3), `MESH_PROMISE_AUTOMUTE_H` (default 72); a `muted` set
  persisted alongside `$STATE` so mute state survives across `--feed` runs.

### Step 4.1: Factor `do_reroute`'s posting logic into a reusable internal function

Auto-reroute needs the exact same two-board-line posting Step 1.5's `do_reroute()` does, but driven
by computed values (not CLI args) and without the CLI's argument-parsing/roster-validation-error-exit
shape (auto-reaction must never `exit`, only skip that one item and continue the feed).

- [ ] In `scripts/mesh-promises`, extract the posting body of `do_reroute()` (Step 1.5) into a new
  helper, and have `do_reroute()` call it after its own validation:

```bash
# NEW helper, placed just before do_reroute() in Step 1.5's block:
_post_reroute(){ # $1=type $2=owner $3=slug $4=lead $5=newowner $6=reason $7=auto(0|1) → rc0 posted
  local type="$1" owner="$2" slug="$3" lead="$4" newowner="$5" reason="$6" auto="${7:-0}"
  local suffix=""; [ "$auto" = 1 ] && suffix=" (auto)"
  mesh-chat "[done] rerouted: $type $owner/$slug — to $newowner (${reason}${suffix})" >/dev/null 2>&1
  case "$type" in
    promise) mesh-chat "[task] $lead. owner: $newowner" >/dev/null 2>&1;;
    claim)   mesh-chat "[verify] $newowner: $lead" >/dev/null 2>&1;;
  esac
}
```

- [ ] Update `do_reroute()` (Step 1.5) to call it instead of duplicating the two `mesh-chat` lines:

```bash
# OLD tail of do_reroute() (Step 1.5):
  mesh-chat "[done] rerouted: $type $owner/$slug — to $newowner ($reason)" >/dev/null 2>&1
  case "$type" in
    promise) mesh-chat "[task] $lead. owner: $newowner" >/dev/null 2>&1;;
    claim)   mesh-chat "[verify] $newowner: $lead" >/dev/null 2>&1;;
  esac
  echo "mesh-promises --reroute: posted reroute for $type $owner/$slug -> $newowner — refreshing ledger"
  do_feed

# NEW:
  _post_reroute "$type" "$owner" "$slug" "$lead" "$newowner" "$reason" 0
  echo "mesh-promises --reroute: posted reroute for $type $owner/$slug -> $newowner — refreshing ledger"
  do_feed
```

- [ ] Run `mesh-promises --test`. Expected: **PASS** (assertion 26/27 from Step 1.7 exercise
  `do_reroute` end-to-end; this refactor must not change observable behavior).
- [ ] Commit: `git add scripts/mesh-promises && git commit -m "mesh-promises: factor reroute posting into _post_reroute (prep for Component D)"`

### Step 4.2: Auto-reroute pass in `do_feed()`

- [ ] Add env var defaults near the other `MESH_PROMISE_*` defaults, around line 97-100:

```bash
# OLD:
LEAK_H="${MESH_PROMISE_LEAK_H:-24}"
LEAK_INCIDENT_H="${MESH_PROMISE_LEAK_INCIDENT_H:-6}"
CLAIM_LEAK_H="${MESH_CLAIM_LEAK_H:-12}"
MIN_OVERLAP="${MESH_PROMISE_MIN_OVERLAP:-1}"

# NEW:
LEAK_H="${MESH_PROMISE_LEAK_H:-24}"
LEAK_INCIDENT_H="${MESH_PROMISE_LEAK_INCIDENT_H:-6}"
CLAIM_LEAK_H="${MESH_CLAIM_LEAK_H:-12}"
MIN_OVERLAP="${MESH_PROMISE_MIN_OVERLAP:-1}"
AUTOREACT="${MESH_PROMISE_AUTOREACT:-}"                              # master opt-in, default OFF
AUTOREROUTE_MARGIN="${MESH_PROMISE_AUTOREROUTE_MARGIN:-2}"
AUTOREROUTE_MIN="${MESH_PROMISE_AUTOREROUTE_MIN:-3}"
AUTOMUTE_H="${MESH_PROMISE_AUTOMUTE_H:-72}"
MUTED="$MESH/.promises-muted"          # persisted set of "type/key/slug" this node has auto-muted
```

- [ ] In `do_feed()`, after the existing `write_leaks_cache "$jt"` call and before the `newleaks`
  computation (this file's current `do_feed()` computes `newleaks` from `$jt` right after
  `write_leaks_cache`), insert the auto-reaction pass. It must run BEFORE the `newleaks` alert
  computation reads `$jt`'s leak list, since a successfully auto-rerouted item should not also fire a
  "new leak" alert this same cycle (it's being resolved, not left open):

```bash
# INSERT into do_feed(), right after:
#   local jt; jt="$(mktemp)"; do_json > "$jt" 2>/dev/null
#   write_leaks_cache "$jt"
# and BEFORE:
#   local newleaks
#   newleaks="$(python3 - "$jt" "$STATE" <<'PY' ... )"

  if [ -n "$AUTOREACT" ]; then
    _auto_react "$jt"
    # the auto-react pass may have posted reroutes/mutes to the board — re-materialize so the
    # leak-transition computation below reads POST-reaction state, not the stale pre-reaction json.
    do_materialize >/dev/null
    do_json > "$jt" 2>/dev/null
    write_leaks_cache "$jt"
  fi
```

- [ ] Add the `_auto_react()` function, placed near `_post_reroute`/`do_reroute`:

```bash
# _auto_react — Component D. Reads the just-materialized json, performs two KINDS of automation,
# both opt-in behind MESH_PROMISE_AUTOREACT, both reversible (never writeoff):
#   (a) auto-reroute an unrouted promise/claim whose suggested owner is unambiguous, not incident,
#       and has already sat unrouted past its own leak threshold (humans get first crack).
#   (b) auto-mute (not close) a structurally-undischargeable item (reflex-broadcast claim, or any
#       claim/hold whose debtor/taker isn't a roster window) once it's aged past AUTOMUTE_H with
#       ZERO human engagement — checked via the STATE file's own leak-key history (if it's been in
#       the leaked set continuously since first seen and no [taking]/[fyi] mentioning its slug ever
#       appears in CHAT_LOG, nobody has touched it).
_auto_react(){ # $1 = json file (already materialized this cycle)
  local jt="$1"
  python3 - "$jt" "$CHAT_LOG" "$AUTOREROUTE_MARGIN" "$AUTOREROUTE_MIN" "$AUTOMUTE_H" "$MUTED" \
    <<'PY' > "${_AUTO_REACT_OUT:=$(mktemp)}"
import sys, json, re
jt, chat_log, margin, minov, automute_h, mutedf = sys.argv[1:7]
margin, minov, automute_h = int(margin), int(minov), float(automute_h)
try: j = json.load(open(jt))
except Exception: sys.exit(0)

# candidates for auto-reroute: unrouted promise/claim rows past their own leak threshold, not
# incident, with an unambiguous suggested owner. suggest_score alone isn't "unambiguous" — this
# script only sees the TOP suggestion (mesh-promises' python doesn't emit runner-up score), so
# treat "score >= AUTOREROUTE_MIN" as the unambiguity proxy for v1 (documented limitation: a true
# margin-over-runner-up check needs the replay to emit the second-best score too — track as a
# follow-up, not blocking this v1).
for row in j.get('open', []):
    if row.get('unrouted') and row.get('leaked') and not row.get('incident') and row.get('suggest') and row.get('suggest_score', 0) >= minov:
        print("REROUTE\tpromise\t%s\t%s\t%s" % (row['owner'], row['slug'], row['suggest']))
for row in j.get('claims', []):
    if row.get('unrouted') and row.get('leaked') and row.get('suggest') and row.get('suggest_score', 0) >= minov:
        print("REROUTE\tclaim\t%s\t%s\t%s" % (row['debtor'], row['slug'], row['suggest']))

# candidates for auto-mute: structurally-undischargeable (reflex-broadcast claim, or unrouted
# claim/hold) aged past automute_h. Engagement check: does chat_log contain a [taking] or [fyi]
# mentioning this exact slug from ANY window? If yes, a human has looked — never auto-mute.
try:
    log_text = open(chat_log, errors='replace').read()
except FileNotFoundError:
    log_text = ""
def engaged(slug):
    return bool(re.search(r'\[(taking|fyi)\][^\n]*' + re.escape(slug), log_text))
try:
    already_muted = set(x.strip() for x in open(mutedf) if x.strip())
except FileNotFoundError:
    already_muted = set()
for row in j.get('claim_leaks', []):
    key = "claim/%s/%s" % (row['debtor'], row['slug'])
    if key in already_muted: continue
    if row.get('age_h', 0) >= automute_h and not engaged(row['slug']):
        print("MUTE\t%s" % key)
for row in j.get('hold_leaks', []):
    key = "hold/%s/%s" % (row['taker'], row['slug'])
    if key in already_muted: continue
    if row.get('age_h', 0) >= automute_h and not engaged(row['slug']):
        print("MUTE\t%s" % key)
PY
  local outf="${_AUTO_REACT_OUT}"; local n_rerouted=0 n_muted=0
  while IFS=$'\t' read -r kind a b c d; do
    [ -n "$kind" ] || continue
    case "$kind" in
      REROUTE)
        local type="$a" owner="$b" slug="$c" newowner="$d" lead
        lead="$(_lookup_open <(do_json 2>/dev/null) "$type" "$owner" "$slug" 2>/dev/null)"
        [ -n "$lead" ] || continue
        _post_reroute "$type" "$owner" "$slug" "$lead" "$newowner" "unambiguous charter match" 1
        n_rerouted=$(( n_rerouted + 1 ))
        ;;
      MUTE)
        echo "$a" >> "$MUTED"
        n_muted=$(( n_muted + 1 ))
        ;;
    esac
  done < "$outf"
  rm -f "$outf"; unset _AUTO_REACT_OUT
  [ "$n_rerouted" -gt 0 ] && echo "mesh-promises --feed: auto-rerouted $n_rerouted unrouted item(s) (MESH_PROMISE_AUTOREACT)"
  [ "$n_muted" -gt 0 ] && echo "mesh-promises --feed: auto-muted $n_muted structurally-stuck item(s) — still open/visible, just quieter (MESH_PROMISE_AUTOREACT)"
}
```

  **Correctness note to verify during implementation, not assume:** `_lookup_open <(do_json ...) ...`
  uses process substitution, which `_lookup_open` (Step 1.5) expects as a real file path (`sys.argv[1]`
  passed to `open()`); process substitution provides a `/dev/fd/N` path which `open()` handles fine on
  Linux, but confirm this actually works in the sandboxed test environment before relying on it — if
  not, write `do_json` to a real tempfile first (same pattern used everywhere else in this file, e.g.
  `local jt; jt="$(mktemp)"; do_json > "$jt"`) and pass that path instead.

### Step 4.3: Filter muted items out of the leak-transition alert and `--dash` headline

- [ ] The `newleaks` computation in `do_feed()` (existing code, right after Step 4.2's insertion
  point) reads `$jt`'s `leaks` list to decide what counts as a "new" leak to alert on. Muted items
  must be excluded from THIS computation (they're still `leaked: true` in the json — mute doesn't
  change that field, per the spec's "muting is not closing" requirement) but should not re-trigger
  the transition alert. Edit the existing `newleaks` python block (find it via
  `newleaks="$(python3 - "$jt" "$STATE" <<'PY'`):

```python
# OLD (existing code inside that heredoc):
import sys, json
jt, statef = sys.argv[1], sys.argv[2]
try: leaks = json.load(open(jt)).get('leaks', [])
except Exception: leaks = []
cur = {("%s/%s" % (l['owner'], l['slug'])) for l in leaks}

# NEW:
import sys, json
jt, statef = sys.argv[1], sys.argv[2]
try: leaks = json.load(open(jt)).get('leaks', [])
except Exception: leaks = []
cur = {("%s/%s" % (l['owner'], l['slug'])) for l in leaks}
# note: this block only ever iterated PROMISE leaks (l['owner']) — claim/hold mute filtering
# happens in write_leaks_cache and --dash's headline count, not here, since this block was never
# claim/hold-aware to begin with (pre-existing scope, unchanged by this task).
```

  This step turns out to be a **no-op for promises** (promise leaks were never mute-eligible —
  Component D's mute path only targets claims/holds per Step 4.2's candidate generation, which never
  emits `MUTE\tpromise/...`). The actual filtering needed is in `write_leaks_cache` (claim/hold rows)
  and `--dash`'s headline. Skip editing this block; instead:

- [ ] Edit `write_leaks_cache()` (line 665-680) to exclude muted claim/hold rows:

```python
# OLD:
def write_leaks_cache(){  # $1 = json file
  python3 - "$1" "$LEAKS_CACHE" <<'PY'
import sys, json
jt, out = sys.argv[1], sys.argv[2]
try: j = json.load(open(jt))
except Exception: j = {}
leaks = j.get('leaks', [])
rows = ["  %-10s %5.0fh%s  %s" % (l['owner'], l['age_h'], " !" if l['incident'] else "  ", l['lead'][:46])
        for l in leaks[:8]]
crows = ["  %-10s %5.0fh %s  [claim] %s" % (l['debtor'], l['age_h'], "B" if l['reflex'] else " ", l['lead'][:40])
         for l in j.get('claim_leaks', [])[:4]]
hrows = ["  %-10s %5.0fh    [hold] %s" % (l['taker'], l['age_h'], l['lead'][:40])
         for l in j.get('hold_leaks', [])[:4]]
rows = rows + crows + hrows
open(out, 'w').write(("\n".join(rows) + "\n") if rows else "")
PY
}

# NEW:
write_leaks_cache(){  # $1 = json file
  python3 - "$1" "$LEAKS_CACHE" "$MUTED" <<'PY'
import sys, json
jt, out, mutedf = sys.argv[1], sys.argv[2], sys.argv[3]
try: j = json.load(open(jt))
except Exception: j = {}
try: muted = set(x.strip() for x in open(mutedf) if x.strip())
except FileNotFoundError: muted = set()
leaks = j.get('leaks', [])
rows = ["  %-10s %5.0fh%s  %s" % (l['owner'], l['age_h'], " !" if l['incident'] else "  ", l['lead'][:46])
        for l in leaks[:8]]
crows = ["  %-10s %5.0fh %s  [claim] %s" % (l['debtor'], l['age_h'], "B" if l['reflex'] else " ", l['lead'][:40])
         for l in j.get('claim_leaks', []) if ("claim/%s/%s" % (l['debtor'], l['slug'])) not in muted][:4]
hrows = ["  %-10s %5.0fh    [hold] %s" % (l['taker'], l['age_h'], l['lead'][:40])
         for l in j.get('hold_leaks', []) if ("hold/%s/%s" % (l['taker'], l['slug'])) not in muted][:4]
rows = rows + crows + hrows
open(out, 'w').write(("\n".join(rows) + "\n") if rows else "")
PY
}
```

  (Note the list-comprehension slicing changed from `[...for l in X[:4]]` to
  `[...for l in X if COND][:4]` — filter-then-slice, not slice-then-filter, so muted rows don't
  silently shrink the visible count below 4 when unmuted ones exist further down the list.)

- [ ] Run `mesh-promises --test`. Expected: **PASS**.
- [ ] Commit: `git add scripts/mesh-promises && git commit -m "mesh-promises: auto-reroute/auto-mute pass in --feed (Component D)"`

### Step 4.4: RED-first tests for Component D (spec tests 7-10)

- [ ] Add to `do_test()` — these test the python building blocks (`suggest_owner`, the mute-candidate
  logic) directly via `replay`, since `_auto_react` itself shells out to `mesh-chat`/`do_json`/
  `do_feed` and is harder to unit-test in isolation; follow the existing convention of testing the
  PURE decision logic (as `clear_reason`-style tests do in the sibling spec) rather than the full
  wired path, and note in a comment that full-path verification happens via manual/live smoke-check
  since `MESH_PROMISE_NO_POST`-style suppression doesn't exist for the auto-react board posts yet:

```bash
  # ============= Component D: auto-reaction building blocks (2026-07-24) =============

  # 31) an unrouted promise past its leak threshold with an unambiguous charter match (score>=3) is
  #     a REROUTE candidate; an otherwise-identical INCIDENT-tagged one is NOT (never automated).
  cat > "$t/boardd1" <<'EOF'
2026-07-23T00:00:00Z  tg@n  ::  [task] fix the sound studio grinder crashing on long records. owner: score
2026-07-23T00:05:00Z  tg@n  ::  [task] fix the sound studio grinder oom on remix mode. owner: score priority:incident
EOF
  local jd1; jd1="$(mktemp)"
  MESH_PROMISE_ROSTER="tg genome witness senses health discover sound pub vpn tg-roz" \
    MESH_PROMISE_ACCOUNTS_FILE="$_self_dir/accounts.journal" \
    replay json "$t/boardd1" "$NOW" 24 6 1 > "$jd1"
  python3 - "$jd1" <<'PY' || { echo "smoke-test: FAIL (auto-reroute candidate shape wrong — see stderr)"; exit 1; }
import sys, json
j = json.load(open(sys.argv[1]))
rows = {r['slug']: r for r in j['open']}
assert rows['fix-the-sound-studio-grinder-crashing-on-long-records']['unrouted']
assert rows['fix-the-sound-studio-grinder-crashing-on-long-records']['suggest'] == 'sound'
assert rows['fix-the-sound-studio-grinder-crashing-on-long-records']['suggest_score'] >= 3
assert rows['fix-the-sound-studio-grinder-oom-on-remix-mode']['incident'] is True
PY

  # 32) a structurally-undischargeable claim aged past AUTOMUTE_H with NO [taking]/[fyi] ever
  #     mentioning its slug is a MUTE candidate; an identically-aged one WITH a prior [fyi] mention
  #     is not (engagement resets the mute eligibility).
  cat > "$t/boardd2" <<'EOF'
2026-07-15T00:00:00Z  load-audit@n  ::  [verify] [JUNK-LOAD] sustained load average 22.4 for 200 hours — investigate.
2026-07-16T00:00:00Z  load-audit@n  ::  [verify] [JUNK-LOAD2] a second sustained spike nobody has looked at either.
2026-07-16T02:00:00Z  health@n      ::  [fyi] looked at JUNK-LOAD2, transient, no action needed but leaving it open.
EOF
  local jd2; jd2="$(mktemp)"
  replay journal "$t/boardd2" "$NOW" 24 6 1 /dev/null > /dev/null
  replay json "$t/boardd2" "$NOW" 24 6 1 > "$jd2"
  grep -q 'JUNK-LOAD"' "$jd2" >/dev/null || true   # sanity that the fixture parsed (lead text may differ; not asserted precisely)
  rm -f "$jd1" "$jd2"
```

  **Implementation note:** test 32's engagement check depends on `_auto_react`'s python `engaged()`
  regex matching against `CHAT_LOG` content, which isn't exercised by a bare `replay json` call
  (that function lives in the `_auto_react` heredoc, not the `replay` heredoc). Rewrite this
  assertion to invoke the actual mute-candidate logic — either factor `engaged()`/the mute-candidate
  loop out of `_auto_react`'s inline heredoc into a `replay`-callable mode (cleanest: add a
  `mode == 'automute_candidates'` branch to the main `replay()` python that takes the same board/now/
  thresholds args plus `automute_h`, reusing `log_text`/`engaged()` against `chat_log` which `replay`
  already receives as an argument), or accept weaker coverage here and rely on the `--feed`
  integration smoke-check below. Prefer the `replay` mode addition — it keeps ALL board-parsing logic
  in the one heredoc `mesh-promises` already documents as "The ONE parse," consistent with this
  file's own stated design principle; do this refactor as part of Step 4.2 rather than bolting a
  second parser onto `_auto_react`.

- [ ] Given the note above, revise Step 4.2 during implementation: fold the mute-candidate detection
  (the `engaged()` check + `already_muted` set + age/threshold filter) into the main `replay()`
  python as a new `mode == 'automute_candidates'` branch instead of a separate heredoc in
  `_auto_react()`. This is a design correction found while writing this task's tests — apply it
  before considering Task 4 done, and re-verify test 32 exercises it directly via
  `replay automute_candidates ...` the same way tests 31 exercises `replay json`.
- [ ] Run `mesh-promises --test`. Expected: **PASS** once the refactor above lands.
- [ ] Commit: `git add scripts/mesh-promises && git commit -m "mesh-promises: RED-first tests for Component D + fold mute-candidates into the one replay parser"`

### Step 4.5: Live smoke-check (manual, not `--test` — real board, opt-in flag)

- [ ] With `MESH_PROMISE_AUTOREACT` still unset, run `mesh-promises --feed` on the real node and
  confirm output is byte-for-byte unchanged from before this task (regression guard — default-off
  must mean default-off).
- [ ] Run `MESH_PROMISE_AUTOREACT=1 mesh-promises --feed` once, by hand, and read its output — expect
  either "no candidates this cycle" or a small number of `auto-rerouted`/`auto-muted` lines. Manually
  verify one resulting board post (`tail ~/.mesh/chat.log`) reads as intended before leaving
  `MESH_PROMISE_AUTOREACT` enabled in any cron env — this flag is opt-in precisely so a node can
  observe one live cycle before trusting it unattended.

---

## Task 5: `mesh-mind-compact` — Components A+B: `clear_has_claim_start()` + precedence

**Files:**
- Modify: `scripts/mesh-mind-compact` (new function `clear_has_claim_start()`, edit `clear_reason()`)

**Interfaces:**
- Produces: `clear_has_claim_start(win, since_epoch) → 0|1` (mirrors `clear_has_completion`'s exact
  signature/contract); `clear_reason()` gains a `claim-start` tier between `post-claim` and the
  (Task 6-replaced) fallback tier.
- Consumes: nothing new — reuses `$CHAT_LOG`, the same awk-scan idiom `clear_has_completion` already
  uses.

### Step 5.1: `clear_has_claim_start()`

- [ ] Add this function to `scripts/mesh-mind-compact` immediately after `clear_has_completion()`
  (which ends at line 219, right before the `# warn_if_no_clear_trace` comment at line 221):

```bash
# OLD (context — do not change, just locate the insertion point):
clear_has_completion() { # $1=win $2=since_epoch → 0 completion posted since, 1 none
  local win="$1" since="${2:-0}" cutoff
  [ "$CTX_CMD" = "/clear" ] || return 1                 # /compact keeps its summary — no per-claim reset
  [ -f "$CHAT_LOG" ] || return 1
  case "$since" in (*[!0-9]*|"") since=0;; esac
  cutoff="$(date -u -d "@$since" +%Y-%m-%dT%H:%M 2>/dev/null)" || return 1
  awk -v win="$win" -v cutoff="$cutoff" '
    length($0) >= 16 {
      ts = substr($0, 1, 16)
      if (ts >= cutoff && $0 ~ ("[ \t]" win "@[^ \t]+[ \t]+::") \
          && $0 ~ /\[(done|claim-done|yield)\]/) { found=1; exit }
    }
    END { exit !found }
  ' "$CHAT_LOG"
}

# warn_if_no_clear_trace — call immediately before send_compact at every call site; logs, never blocks.

# NEW (insert clear_has_claim_start between them):
clear_has_completion() { # $1=win $2=since_epoch → 0 completion posted since, 1 none
  local win="$1" since="${2:-0}" cutoff
  [ "$CTX_CMD" = "/clear" ] || return 1                 # /compact keeps its summary — no per-claim reset
  [ -f "$CHAT_LOG" ] || return 1
  case "$since" in (*[!0-9]*|"") since=0;; esac
  cutoff="$(date -u -d "@$since" +%Y-%m-%dT%H:%M 2>/dev/null)" || return 1
  awk -v win="$win" -v cutoff="$cutoff" '
    length($0) >= 16 {
      ts = substr($0, 1, 16)
      if (ts >= cutoff && $0 ~ ("[ \t]" win "@[^ \t]+[ \t]+::") \
          && $0 ~ /\[(done|claim-done|yield)\]/) { found=1; exit }
    }
    END { exit !found }
  ' "$CHAT_LOG"
}

# clear_has_claim_start — the START half of the claim-lifecycle clear trigger (operator 2026-07-24:
# "/clear is both present for starting and finishing task"). Returns 0 if this window posted a
# SLUGGED [taking] (a real claim, not the content-free heartbeat CLAUDE.md carves out — same
# discipline mesh-promises' taking_slug_and_rest() already enforces for the HOLD commodity) since
# its last clear. A mind taking on a new task is exactly as good a context-reset point as one
# finishing the last: it flushes leftover context from unrelated prior chatter that never counted as
# a "completion" and so never fired clear_has_completion. Mirrors that function's exact contract
# (cutoff-from-last-clear, so the same [taking] line can't re-trigger a later idle check).
clear_has_claim_start() { # $1=win $2=since_epoch → 0 slugged [taking] posted since, 1 none
  local win="$1" since="${2:-0}" cutoff
  [ "$CTX_CMD" = "/clear" ] || return 1
  [ -f "$CHAT_LOG" ] || return 1
  case "$since" in (*[!0-9]*|"") since=0;; esac
  cutoff="$(date -u -d "@$since" +%Y-%m-%dT%H:%M 2>/dev/null)" || return 1
  awk -v win="$win" -v cutoff="$cutoff" '
    length($0) >= 16 {
      ts = substr($0, 1, 16)
      if (ts >= cutoff && $0 ~ ("[ \t]" win "@[^ \t]+[ \t]+::") \
          && $0 ~ /\[taking\][ \t]*[^ \t:][^:]{2,60}:/) { found=1; exit }
    }
    END { exit !found }
  ' "$CHAT_LOG"
}

# warn_if_no_clear_trace — call immediately before send_compact at every call site; logs, never blocks.
```

  (The `$0 ~ /\[taking\][ \t]*[^ \t:][^:]{2,60}:/` pattern mirrors `mesh-promises`'
  `taking_slug_and_rest()`'s "`<slug>:` " discipline in awk form: at least one non-colon,
  non-whitespace character immediately after `[taking]`, followed eventually by a colon within a
  reasonable slug length — a bare `[taking] just orienting` has no colon in that window and won't
  match; a bare `[taking]` with nothing else won't match either.)

- [ ] There is no standalone `--test` runnable yet for this new function alone — proceed to Step 5.2
  where `clear_reason()` wires it in, then test both together in Step 5.3.

### Step 5.2: Wire into `clear_reason()` precedence

- [ ] Edit `clear_reason()` (line 292-303):

```bash
# OLD:
clear_reason() { # $1=win $2=last_clear_epoch $3=pct $4=now  → echoes reason | empty=skip
  local win="$1" last="$2" pct="$3" now="$4" idle
  idle=$(( now - last ))
  if clear_has_completion "$win" "$last"; then echo "post-claim"; return 0; fi
  if [ "$idle" -ge "$INTERVAL" ]; then echo "interval $(( idle/60 ))m"; return 0; fi
  if [ -n "$pct" ] && [ "$pct" != "?" ]; then
    local pct_n="${pct%\%}"
    case "$pct_n" in (*[!0-9]*|"") return 0;; esac
    [ "$pct_n" -ge "$THRESHOLD" ] && { echo "ctx ${pct}≥${THRESHOLD}%"; return 0; }
  fi
  return 0
}

# NEW:
clear_reason() { # $1=win $2=last_clear_epoch $3=pct $4=now  → echoes reason | empty=skip
  local win="$1" last="$2" pct="$3" now="$4" idle
  idle=$(( now - last ))
  if clear_has_completion "$win" "$last"; then echo "post-claim"; return 0; fi
  if clear_has_claim_start "$win" "$last"; then echo "claim-start"; return 0; fi
  if [ "$idle" -ge "$INTERVAL" ]; then echo "interval $(( idle/60 ))m"; return 0; fi
  if [ -n "$pct" ] && [ "$pct" != "?" ]; then
    local pct_n="${pct%\%}"
    case "$pct_n" in (*[!0-9]*|"") return 0;; esac
    [ "$pct_n" -ge "$THRESHOLD" ] && { echo "ctx ${pct}≥${THRESHOLD}%"; return 0; }
  fi
  return 0
}
```

  (This leaves the `interval`/`INTERVAL` tier in place for now — Task 6 replaces it. Landing
  claim-start first, on top of the still-working interval backstop, keeps every intermediate commit
  in this task independently safe to deploy.)

- [ ] Run `mesh-mind-compact --test`. Expected: **PASS** (existing precedence tests at lines 642-648
  are unaffected — none of their fixtures post a slugged `[taking]`, so `clear_has_claim_start`
  returns 1 for all of them and precedence falls through exactly as before).
- [ ] Commit: `git add scripts/mesh-mind-compact && git commit -m "mesh-mind-compact: clear_has_claim_start + claim-start tier in clear_reason (Component A+B)"`

### Step 5.3: RED-first tests (spec tests 1-3, 7)

- [ ] Find the existing `--test` fixture block (starts around line 361, `if [ "${1:-}" = --test ]; then`)
  and locate where the existing `clear_reason` precedence assertions live (around lines 642-648, per
  the earlier grep). Add these immediately after that block, before the final
  `echo "smoke-test: ok (...)"` summary line:

```bash
  # ============= claim-start trigger (2026-07-24) =============

  # a slugged [taking] since last clear, no completion marker → claim-start
  printf '%s  genome@testhost  ::  [taking] widget-audit: auditing the widget subsystem now.\n' "$_now_iso" > "$CHAT_LOG"
  case "$(clear_reason genome $(( $(date +%s) - 60 )) '?' $(date +%s))" in
    claim-start) : ;;
    *) echo "smoke-test: FAIL (slugged [taking] since last clear did not trigger claim-start)"; exit 1;;
  esac

  # a content-free [taking] (no slug) must NOT trigger claim-start — mirrors mesh-promises' HOLD
  # content-free carve-out; a heartbeat is not a claim.
  printf '%s  genome@testhost  ::  [taking] just orienting, nothing new to claim yet.\n' "$_now_iso" > "$CHAT_LOG"
  [ -z "$(clear_reason genome $(( $(date +%s) - 60 )) '?' $(date +%s))" ] || {
    echo "smoke-test: FAIL (content-free [taking] triggered a clear — heartbeat treated as a claim)"; exit 1; }

  # both a [taking] AND a later [done] since last clear → post-claim WINS (precedence), not claim-start
  {
    printf '%s  genome@testhost  ::  [taking] widget-audit: auditing the widget subsystem now.\n' "$_now_iso"
    printf '%s  genome@testhost  ::  [done] widget-audit: audited the widget subsystem, all clean.\n' "$(date -u -d '+1 second' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u +%Y-%m-%dT%H:%M:%SZ)"
  } > "$CHAT_LOG"
  case "$(clear_reason genome $(( $(date +%s) - 60 )) '?' $(date +%s))" in
    post-claim) : ;;
    *) echo "smoke-test: FAIL (post-claim did not win precedence over claim-start when both fired)"; exit 1;;
  esac

  # cutoff-advance: after a claim-start clear, the SAME [taking] line must not re-trigger a second
  # clear on the next idle check (mirrors the existing post-claim cutoff-advance behavior — the
  # caller advances $last to "now" after a successful clear, so re-checking against the NEW last
  # (after the [taking] timestamp) must return nothing).
  printf '%s  genome@testhost  ::  [taking] widget-audit: auditing the widget subsystem now.\n' "$_now_iso" > "$CHAT_LOG"
  [ -z "$(clear_has_claim_start genome $(date +%s))" ] || true   # since=now (post-clear) means the taking line is BEFORE cutoff
  clear_has_claim_start genome $(date +%s) && { echo "smoke-test: FAIL (claim-start re-fired for a [taking] line before the new cutoff)"; exit 1; }
  return 1 2>/dev/null || true
```

  **Verify `$_now_iso` and `$CHAT_LOG` scoping** against the existing test harness before trusting
  this verbatim — the existing tests around line 606-627 already establish this exact pattern
  (`_now_iso`, writing directly to `$CHAT_LOG`, calling `clear_reason`/`clear_has_completion`
  directly as shell functions within the same `--test` block), so match their established setup
  (sandbox `$CHAT_LOG` redirection, `$_now_iso` computation) rather than reintroducing it — read the
  ~20 lines above line 606 in the live file to copy the exact sandboxing idiom used there.

- [ ] Run `mesh-mind-compact --test`. Expected: **PASS**.
- [ ] Commit: `git add scripts/mesh-mind-compact && git commit -m "mesh-mind-compact: RED-first tests for claim-start trigger"`

---

## Task 6: `mesh-mind-compact` — Component C: fold the interval backstop into hledger queries

**Files:**
- Modify: `scripts/mesh-mind-compact` (`clear_reason()`'s fallback tier, two new functions
  `clear_has_hold_leak()`/`clear_has_turn_ceiling()`, remove `INTERVAL`'s role in `clear_reason()`
  specifically — **not** the bare variable, which the separate manual-TARGETS loop still legitimately
  uses as its own unrelated "don't re-clear a manually-targeted window too soon" cooldown, per the
  Global Constraints note above)

**Interfaces:**
- Consumes: `mesh-promises --json` (Task 2's `unrouted`/`leaked` fields on hold rows — already exist
  before Task 2 for the `leaked` field; Task 2 only adds `unrouted`, which this task does not need),
  `mesh-labor --register` (already exists, unmodified by this plan).
- Produces: env vars `MESH_COMPACT_PROMISES_CMD` (test override, mirrors `MESH_COMPACT_SNAPSHOT_CMD`),
  `MESH_COMPACT_LABOR_CMD` (test override), `MESH_COMPACT_TURN_CEILING` (default 40).

### Step 6.1: Confirm the dependency this task needs already exists

- [ ] Run `mesh-promises --json` on the live node (or a fresh `--test`-style fixture) and confirm the
  `holds` array already has `taker`, `slug`, `age_h`, `leaked` fields — these predate this plan
  entirely (see the earlier grounding read of the replay code, `hold_open_list.append(dict(taker=...,
  leaked=age_h > leak_h))`). Nothing from Task 2 is required for THIS task — `hold-leak` only reads
  `leaked`, not `unrouted`. Confirm this in the plan's own words so whoever executes Task 6 doesn't
  block on Task 2 unnecessarily: **Task 6 depends only on Task 1 landing** (so `mesh-promises --json`
  exists and is stable), not on Tasks 2-4.

### Step 6.2: `clear_has_hold_leak()`

- [ ] Add near `clear_has_claim_start()` (after Task 5's insertion):

```bash
# clear_has_hold_leak — Component C (2026-07-24, operator pushback: "this should be decided from
# the hledger side, not cron"). Replaces the old wall-clock INTERVAL's "is a claim stuck" job:
# queries mesh-promises' OWN HOLD-leak computation (age_h vs its own MESH_PROMISE_LEAK_H) instead of
# a disconnected local timer — one shared definition of "stale" instead of two. Fail-INERT (never
# fires, never crashes) when mesh-promises is absent/erroring — this is an ADDITIVE fallback tier
# under two event triggers that never depended on it.
clear_has_hold_leak() { # $1=win → 0 an open HOLD for this window is leaked per mesh-promises, 1 none/absent
  local win="$1" cmd out
  if [ -n "${MESH_COMPACT_PROMISES_CMD:-}" ]; then cmd="$MESH_COMPACT_PROMISES_CMD"
  elif command -v mesh-promises >/dev/null 2>&1; then cmd="mesh-promises --json"
  else return 1; fi
  out="$($cmd 2>/dev/null)" || return 1
  [ -n "$out" ] || return 1
  printf '%s' "$out" | python3 -c '
import sys, json
try: j = json.load(sys.stdin)
except Exception: sys.exit(1)
win = sys.argv[1]
sys.exit(0 if any(h.get("taker") == win and h.get("leaked") for h in j.get("holds", [])) else 1)
' "$win" 2>/dev/null
}
```

### Step 6.3: `clear_has_turn_ceiling()`

- [ ] Add right after:

```bash
# clear_has_turn_ceiling — Component C, the OTHER half of the old INTERVAL's job: proactive context
# hygiene independent of any open claim. Reads TURNs-since-last-clear from mesh-labor's own
# date-filtered register (hledger's native date: query, not a new counter) — a window doing many
# turns quickly bloats context fast; one sitting mostly idle barely grows it, so this tracks WORK
# DONE, not wall-clock time. Fail-inert like its sibling above.
clear_has_turn_ceiling() { # $1=win $2=since_epoch → 0 TURNs since last clear >= ceiling, 1 below/absent
  local win="$1" since="$2" cmd since_iso ceiling="${MESH_COMPACT_TURN_CEILING:-40}" out n
  since_iso="$(date -u -d "@$since" +%Y-%m-%dT%H:%M:%S 2>/dev/null)" || return 1
  if [ -n "${MESH_COMPACT_LABOR_CMD:-}" ]; then cmd="$MESH_COMPACT_LABOR_CMD"
  elif command -v mesh-labor >/dev/null 2>&1; then cmd="mesh-labor --register expenses:labour:${win} date:>=${since_iso} -N"
  else return 1; fi
  out="$($cmd 2>/dev/null)" || return 1
  n="$(printf '%s' "$out" | awk '{s+=$(NF-1)} END{printf "%d", s+0}')"
  case "$n" in (*[!0-9]*|"") return 1;; esac
  [ "${n:-0}" -ge "$ceiling" ]
}
```

  **Verify `mesh-labor --register`'s actual column layout** before trusting `$(NF-1)` as "the amount
  column" — hledger `register` output format varies by whether `-N`/`--no-elide` and terminal width
  are in play; run `mesh-labor --register expenses:labour:genome -N` live and inspect real output
  columns first, adjusting the `awk` extraction to match (this is exactly the kind of assumption that
  must be checked against real output, not just written down — the plan is giving you the intent and
  the query, not blind trust in a guessed column index).

### Step 6.4: Replace the `interval` tier in `clear_reason()`

- [ ] Edit `clear_reason()` again (now including Task 5's `claim-start` line):

```bash
# OLD (post-Task-5 state):
clear_reason() { # $1=win $2=last_clear_epoch $3=pct $4=now  → echoes reason | empty=skip
  local win="$1" last="$2" pct="$3" now="$4" idle
  idle=$(( now - last ))
  if clear_has_completion "$win" "$last"; then echo "post-claim"; return 0; fi
  if clear_has_claim_start "$win" "$last"; then echo "claim-start"; return 0; fi
  if [ "$idle" -ge "$INTERVAL" ]; then echo "interval $(( idle/60 ))m"; return 0; fi
  if [ -n "$pct" ] && [ "$pct" != "?" ]; then
    local pct_n="${pct%\%}"
    case "$pct_n" in (*[!0-9]*|"") return 0;; esac
    [ "$pct_n" -ge "$THRESHOLD" ] && { echo "ctx ${pct}≥${THRESHOLD}%"; return 0; }
  fi
  return 0
}

# NEW:
clear_reason() { # $1=win $2=last_clear_epoch $3=pct $4=now  → echoes reason | empty=skip
  local win="$1" last="$2" pct="$3" now="$4"
  if clear_has_completion "$win" "$last"; then echo "post-claim"; return 0; fi
  if clear_has_claim_start "$win" "$last"; then echo "claim-start"; return 0; fi
  if clear_has_hold_leak "$win"; then echo "hold-leak"; return 0; fi
  if clear_has_turn_ceiling "$win" "$last"; then echo "turn-ceiling"; return 0; fi
  if [ -n "$pct" ] && [ "$pct" != "?" ]; then
    local pct_n="${pct%\%}"
    case "$pct_n" in (*[!0-9]*|"") return 0;; esac
    [ "$pct_n" -ge "$THRESHOLD" ] && { echo "ctx ${pct}≥${THRESHOLD}%"; return 0; }
  fi
  return 0
}
```

  (`idle` was only used by the deleted `interval` line — drop the now-unused local too, per the
  diff above.)

- [ ] The header comment block above `clear_reason()` (lines 281-291, "PURE trigger decision...
  Precedence: 1. post-claim 2. interval 3. ctx %") documents the OLD precedence — update it to match:

```bash
# OLD:
# clear_reason — PURE trigger decision (fixture-testable; no live tmux). Given an ALREADY-IDLE window
# (the caller enforces state==IDLE — we never interrupt a working mind), echo the reason to /clear it
# now, or nothing to skip. Precedence:
#   1. post-claim — a completion marker ([done]/[claim-done]/[yield]) posted since the last clear.
#   2. interval   — idle ≥ INTERVAL: the UNIVERSAL backstop (ANY engine) — the operator's "clear every
#                   idle mind after N min" (2026-07-16). Deliberately ABOVE the %-threshold so a
#                   readable-% engine (opencode) still gets the time-based clear it used to MISS while
#                   sitting idle below its %-threshold (the old else-branch only ran the interval when %
#                   was unreadable, so idle opencode minds could sit un-cleared indefinitely).
#   3. ctx %      — opencode only (readable %): an EARLY clear when context ≥ THRESHOLD, before INTERVAL.
# INTERVAL / THRESHOLD / CTX_CMD / CHAT_LOG are globals set by the caller.

# NEW:
# clear_reason — PURE trigger decision (fixture-testable; no live tmux). Given an ALREADY-IDLE window
# (the caller enforces state==IDLE — we never interrupt a working mind), echo the reason to /clear it
# now, or nothing to skip. Precedence (2026-07-24, operator: "/clear should be tied to claims/
# finishing tasks... decided from the hledger side, not cron" — the old wall-clock INTERVAL tier is
# gone; both fallback tiers below are hledger queries, not local timers):
#   1. post-claim    — a completion marker ([done]/[claim-done]/[yield]) posted since the last clear.
#   2. claim-start   — a slugged [taking] posted since the last clear (the START half of the same
#                      claim-lifecycle idea, added alongside finish).
#   3. hold-leak     — mesh-promises' OWN HOLD-leak computation says this window's open claim has
#                      gone stale past ITS OWN threshold (MESH_PROMISE_LEAK_H) — one shared staleness
#                      definition across the mesh instead of a second, disconnected local timer.
#   4. turn-ceiling  — mesh-labor's TURN register since last clear crosses MESH_COMPACT_TURN_CEILING
#                      — context hygiene keyed to WORK DONE, not time elapsed.
#   5. ctx %         — opencode only (readable %): an EARLY clear when context ≥ THRESHOLD.
# Tiers 3-4 are fail-INERT when mesh-promises/mesh-labor are absent or error — never a false
# positive, never a crash; a window with an active claim and no ledger tooling still gets
# post-claim/claim-start exactly as before, since those two never depended on either ledger.
# THRESHOLD / CTX_CMD / CHAT_LOG are globals set by the caller.
```

- [ ] Run `mesh-mind-compact --test`. Expected: the EXISTING interval-precedence tests (lines
  642-644, asserting `interval*` reasons) will now **FAIL** — this is expected RED, not a regression;
  proceed to Step 6.5 to update those specific assertions to match the new tier names, since the old
  `INTERVAL`-based behavior they tested no longer exists by design.

### Step 6.5: Update existing tests that asserted the old `interval` tier

- [ ] Locate the existing assertions (around lines 642-648, from the earlier grep) and replace the
  ones that specifically test the old universal-interval-backstop behavior:

```bash
# OLD (existing, lines ~642-644):
  [ -z "$(clear_reason w $((_now-60)) '?' $_now)" ] || { rm -rf "$_cd"; echo "smoke-test: FAIL (clear_reason cleared a FRESH idle mind, unreadable %)"; exit 1; }
  case "$(clear_reason w $((_now-1000)) '?' $_now)" in interval*) : ;; *) rm -rf "$_cd"; echo "smoke-test: FAIL (clear_reason did not interval-clear an idle mind past INTERVAL, unreadable %)"; exit 1;; esac
  case "$(clear_reason w $((_now-1000)) '10%' $_now)" in interval*) : ;; *) rm -rf "$_cd"; echo "smoke-test: FAIL (clear_reason skipped the UNIVERSAL interval clear because % was readable+low — the old else-branch bug)"; exit 1;; esac

# NEW:
  [ -z "$(clear_reason w $((_now-60)) '?' $_now)" ] || { rm -rf "$_cd"; echo "smoke-test: FAIL (clear_reason cleared a FRESH idle mind, unreadable %)"; exit 1; }
  # the old universal-INTERVAL-backstop assertions are RETIRED (Component C, 2026-07-24) — a window
  # idle for 1000s with no claim activity and no ledger tooling reachable now correctly clears
  # NOTHING (fail-inert), proving the backstop moved to hledger queries rather than silently
  # vanishing. hold-leak/turn-ceiling behavior is asserted separately below with explicit mocks.
  [ -z "$(MESH_COMPACT_PROMISES_CMD='false' MESH_COMPACT_LABOR_CMD='false' clear_reason w $((_now-1000)) '?' $_now)" ] || {
    rm -rf "$_cd"; echo "smoke-test: FAIL (clear_reason fired with both ledger tools absent — should be fail-inert, not a phantom clear)"; exit 1; }
  [ -z "$(MESH_COMPACT_PROMISES_CMD='false' MESH_COMPACT_LABOR_CMD='false' clear_reason w $((_now-1000)) '10%' $_now)" ] || {
    rm -rf "$_cd"; echo "smoke-test: FAIL (clear_reason fired on readable-but-low % with ledgers absent)"; exit 1; }

  # hold-leak: a mocked mesh-promises reporting a leaked hold for THIS window fires hold-leak
  case "$(MESH_COMPACT_PROMISES_CMD="printf '%s' '{\"holds\":[{\"taker\":\"w\",\"slug\":\"x\",\"age_h\":99,\"leaked\":true}]}'" \
    MESH_COMPACT_LABOR_CMD='false' clear_reason w $((_now-60)) '?' $_now)" in
    hold-leak) : ;;
    *) rm -rf "$_cd"; echo "smoke-test: FAIL (leaked hold for this window did not trigger hold-leak)"; exit 1;;
  esac
  # a hold for a DIFFERENT window must not fire this window's hold-leak
  [ -z "$(MESH_COMPACT_PROMISES_CMD="printf '%s' '{\"holds\":[{\"taker\":\"other\",\"slug\":\"x\",\"age_h\":99,\"leaked\":true}]}'" \
    MESH_COMPACT_LABOR_CMD='false' clear_reason w $((_now-60)) '?' $_now)" ] || {
    rm -rf "$_cd"; echo "smoke-test: FAIL (another window's leaked hold triggered THIS window's clear)"; exit 1; }

  # turn-ceiling: a mocked mesh-labor register summing above MESH_COMPACT_TURN_CEILING fires it
  case "$(MESH_COMPACT_PROMISES_CMD='false' \
    MESH_COMPACT_LABOR_CMD="printf 'd desc  expenses:labour:w  45  0'" \
    MESH_COMPACT_TURN_CEILING=40 clear_reason w $((_now-60)) '?' $_now)" in
    turn-ceiling) : ;;
    *) rm -rf "$_cd"; echo "smoke-test: FAIL (register sum above ceiling did not trigger turn-ceiling — check the awk column index against real mesh-labor --register output first)"; exit 1;;
  esac
```

  **The `turn-ceiling` mock's literal register line is a placeholder shape** — Step 6.3 already flags
  that the real `mesh-labor --register` column layout must be checked before trusting `$(NF-1)`;
  once that's confirmed, adjust this mock line to match the REAL format exactly (same number of
  columns, amount in the same position) so the test actually exercises the parsing path it claims to.

- [ ] Edit the existing assertion at line 645-646 (the opencode ctx% tests) — these are UNCHANGED by
  this task (ctx% is still tier 5, still opencode-only) but re-run them to confirm they still pass
  with the new function in place:

```bash
# UNCHANGED, just re-verify still passes:
  case "$(clear_reason w $((_now-60)) '80%' $_now)" in ctx*) : ;; *) rm -rf "$_cd"; echo "smoke-test: FAIL (clear_reason did not early-clear a bloated opencode mind at ctx≥THRESHOLD)"; exit 1;; esac
  [ -z "$(clear_reason w $((_now-60)) '30%' $_now)" ] || { rm -rf "$_cd"; echo "smoke-test: FAIL (clear_reason cleared a fresh idle opencode mind below THRESHOLD)"; exit 1; }
```

  (These pass unmodified since `MESH_COMPACT_PROMISES_CMD`/`MESH_COMPACT_LABOR_CMD` are unset in this
  test's environment, both new tiers hit their real `command -v mesh-promises`/`mesh-labor` branch —
  verify whether the sandboxed `--test` environment has those binaries on `PATH`; if it does and they
  return real data, these two lines could spuriously fire `hold-leak`/`turn-ceiling` before ever
  reaching `ctx*`. If that happens, add `MESH_COMPACT_PROMISES_CMD='false' MESH_COMPACT_LABOR_CMD='false'`
  to these two lines too, matching the pattern used above — check this by actually running the test,
  don't assume either way.)

- [ ] Run `mesh-mind-compact --test`. Expected: **PASS** (23 total assertions in the smoke-test
  message context, plus the additions from this task and Task 5 — update the final
  `echo "smoke-test: ok (...)"` summary line's parenthetical description to mention the new triggers,
  matching this file's convention of describing everything the suite covers in that one line).
- [ ] Commit: `git add scripts/mesh-mind-compact && git commit -m "mesh-mind-compact: fold interval backstop into hold-leak/turn-ceiling hledger queries (Component C)"`

### Step 6.6: Config default and deploy note

- [ ] `MESH_COMPACT_INTERVAL` (the bare variable, line 55) is now **unused by `clear_reason()`** but
  still legitimately used by the separate manual-TARGETS loop (line ~787, `age -lt INTERVAL`) — leave
  the variable and its default exactly as-is; do not rename or remove it. Update its inline comment
  only:

```bash
# OLD (line 55):
INTERVAL="${MESH_COMPACT_INTERVAL:-2700}"   # 45 min default — interval backstop for an idle-but-unfinished mind

# NEW:
INTERVAL="${MESH_COMPACT_INTERVAL:-2700}"   # 45 min default — used ONLY by the manual `mesh-mind-compact <window>`
                                             # cooldown check below (unrelated to clear_reason(), which dropped its
                                             # own interval tier for hold-leak/turn-ceiling, Component C 2026-07-24)
```

- [ ] Commit: `git add scripts/mesh-mind-compact && git commit -m "mesh-mind-compact: clarify MESH_COMPACT_INTERVAL now scopes to the manual-targets cooldown only"`

---

## Final Verification (run after all six tasks land)

- [ ] `mesh-promises --test` — full suite green (tests 1-32+).
- [ ] `mesh-mind-compact --test` — full suite green.
- [ ] `mesh-promises --check` on the live node — parity/agreement PASS, roster section now reports
  claim/hold unrouted counts alongside promises.
- [ ] Manually `--writeoff` one of the 8 live `reflex-broadcast` claims found at the start of this
  design session (pick the oldest, 134.9h) and confirm it drops out of `--report`'s leak list while
  still showing in `--all` with a non-`equity:claims`-leg journal entry.
- [ ] `mesh-mind-compact --test` output line confirms `hold-leak`/`turn-ceiling`/`claim-start` are
  all named in the final smoke-test summary string (this file's own convention for "what does this
  suite actually cover" — don't leave the summary line stale, per CLAUDE.md's own "name-only gate"
  and "invoked-by is not ever-runs" lessons: a covering test that isn't named in the one-line summary
  reads as uncovered to the next person skimming `--test` output).
