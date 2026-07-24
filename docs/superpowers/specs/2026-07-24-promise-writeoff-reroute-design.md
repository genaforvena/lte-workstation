# mesh-promises: writeoff/reroute + uniform unrouted accounting — design (2026-07-24)

Operator direction: "we need to have a better use of hledger to handle leaked and unrouted
promises." Scope: `mesh-promises` (the board `[task]`/`[taking]`/`[verify]`/`[done]` double-entry
leak detector, `scripts/mesh-promises`). This spec extends that existing tool; it does not touch
`mesh-chat`, dispatch, or the separate `mesh-board-journal`/`mesh-board-reactor` rebuild described in
[[2026-07-24-hledger-reactive-coordination-design]] (genome's in-flight `[taking]
event-driven-dispatch`) — that spec replaces *how* the board becomes a journal and *how* minds wake;
this spec is about what happens to a promise/claim/hold that the existing detection already found
but can never close on its own. Orthogonal, no overlap, no conflict.

## The problem, evidenced live (2026-07-24, this session)

`mesh-promises` correctly *detects* leaked and unrouted obligations, but has **no resolution
mechanism** — a stuck promise just gets louder forever. Three failure classes exist today, treated
identically as "open, aging, leaked":

1. **Undischargeable by construction.** `reflex-broadcast` CLAIMs (an unaddressed `[verify]` — no
   window can ever post *as* `reflex-broadcast`, so the redemption match `who == debtor` can never
   fire). Live: 8 open, oldest **134.9h** (5.6 days). Also a HOLD taken by `chat` — a window
   **retired** on 2026-07-24 (folded into witness) — so the redemption match "a later `[done]` FROM
   THE SAME TAKER" can never fire either, structurally identical to reflex-broadcast even though
   nothing currently names it that way.
2. **Misrouted.** `owner: operator` / `owner: score` — not roster windows, quarantined to
   `liabilities:promises:unrouted` (Component 2, `ac685ae`). `--check` says "assign an owner or
   retire the task" but the tool offers no way to do either from the ledger side, and no hint about
   which window it probably belongs to.
3. **Genuinely stalled.** Valid owner, valid task, just late — the case the leak alarm was designed
   for. witness already drives these from the leak worklist. **Not broken; out of scope here.**

Classes 1 and 2 need an explicit, auditable resolution action, because the organic discharge path
(a matching `[done]`/`[fyi]`/`[sense]` from the right poster) can never fire for them by
construction. Class 3 already works.

## A second, independently-confirmed bug: unrouted accounting isn't uniform

Reading the replay code: `acct_window()` (roster quarantine → `:unrouted`) is applied when
**materializing the journal** for all three commodities — PROMISE, CLAIM, HOLD. But the
**report/all/check/counts/json** surfaces only ever compute an `unrouted` count for **promises**
(`unrouted_open = sum(... x['owner'] ...)`, promise-only). Claims and holds already quarantine
silently inside the journal with zero visibility anywhere else — which is exactly why the `chat`-held
hold above doesn't show as flagged even though it is, right now, booked under
`liabilities:holds:unrouted:...`. This is a straightforward parity gap, fixed as part of the same
change (Component A below) since it's the same roster-check, just not wired to three of its six
call sites.

## Design

Three components, all inside the existing `scripts/mesh-promises` — no new tool, no new journal.

### Component A — uniform unrouted accounting (promises, claims, holds alike)

Extend the `is_unrouted()` check that promises already have to claims (by `debtor`) and holds (by
`taker`), computed the same place `unrouted_open` is computed today, and surface it everywhere the
promise count already is:
- `counts` mode: add `claim_unrouted=<n> hold_unrouted=<n>` alongside the existing `unrouted=<n>`.
- `json` mode: add `unrouted: bool` per open-claim/open-hold row (promises already carry it
  implicitly via the account path; make it an explicit field on all three for the CLI/dash to key
  off without re-deriving).
- `--check`'s roster section: report claim/hold unrouted counts the same way it reports promises
  today (currently prints only the promise quarantine list).
- `--all`/`--report`: mark unrouted rows with a distinct glyph (🧭 "needs routing", vs 🔴 "leaked but
  routed") so a human scanning the list can tell "needs an owner assigned" apart from "has an owner,
  just late" at a glance — these need different actions.

No change to the journal-writing path (`acct_window()` already does the right thing there); this is
purely making existing quarantine data visible on the other five surfaces.

### Component B — `--writeoff` / `--reroute`: the resolution primitive

The missing piece. Both are **board-posted** actions (never a direct journal edit — the board stays
the sole source of truth, same discipline as everything else in this tool) issued through
`mesh-chat`, and both are recognized by the replay parser via a **prose convention**, matching how
the rest of the tool already resolves markers before the tag-schema work
(`docs/design-board-tag-schema-2026-07-24.md`) lands — no dependency on that unbuilt schema; upgrades
to `status:writeoff`/`status:reroute` tags for free once it does, since the parser already prefers
an explicit tag over derivation everywhere else in the codebase's stated convention.

**`mesh-promises --writeoff <promise|claim|hold> <owner-or-debtor-or-taker>/<slug> --reason "<text>"`**

1. Looks up the exact open item via a fresh replay (same as `--all`); **fails loudly and does
   nothing** if the type/owner/slug triple doesn't match a currently-open item — no silent no-op on
   a typo'd slug (this is the same "absence guard" discipline as everything else in this codebase;
   an admin close is high-stakes and must not partially apply).
2. Posts `[done] written-off: <type> <owner>/<slug> — <reason>` to the board via `mesh-chat`
   (postable by *any* window — typically witness doing triage — since the whole point is that the
   organic "must come from the same owner/debtor/taker" rule is exactly what these items can never
   satisfy).
3. Replay recognizes the `written-off: <type> <owner>/<slug>` prefix as a **new, distinct discharge
   event**, matched by exact type+key (never fuzzy token-overlap — this is a deliberate action, not
   an inferred one) and *not* subject to the normal poster-identity match. It closes the liability to
   zero same as a normal keep, but posts the balancing leg into a **separate equity account**
   (`equity:promises:writeoff` / `equity:claims:writeoff` / `equity:holds:writeoff`) instead of the
   normal `equity:{promises,claims,holds}`. This keeps `hledger check` balanced (nothing orphaned)
   while making "died unkept" a distinct, queryable number from "kept" — currently that distinction
   doesn't exist anywhere; a written-off promise and a genuinely-kept one look identical in the
   ledger today.

**`mesh-promises --reroute <promise|claim|hold> <owner-or-debtor-or-taker>/<slug> --owner <new-window> --reason "<text>"`**

Same validated lookup and failure mode as writeoff. Posts *two* board lines so the audit trail
threads on the board instead of silently vanishing:
1. `[done] rerouted: <type> <owner>/<slug> — to <new-window> (<reason>)` — closes the old item via
   its own `equity:*:reroute` leg (distinct from both `kept` and `writeoff` — three distinguishable
   outcomes, not two).
2. `[task] <original lead>` reposted with the corrected `owner: <new-window>` (or the equivalent for
   claim/hold — a fresh `[verify]`/`[taking]` addressed correctly) — reopens under the *same* derived
   slug where possible so `--all` history threads it as one continuing obligation, not an unrelated
   new one. `<new-window>` is validated against the roster before posting (refuse to reroute into
   another quarantine).

`--reroute` requires `<new-window>` to be a live roster window (from `accounts.journal`); rerouting
onto a retired/non-roster window is refused with the same "assign a real owner" message `--check`
already gives.

### Component C — suggested-owner hint (read-only, never auto-applied)

`accounts.journal` already carries a one-line charter comment per window's `expenses:labour:<w>`
account (e.g. `sound — sound studio: records, grind, room music`). For every `:unrouted`
promise/claim/hold, token-overlap its lead against each window's charter comment (same `toks()`
tokenizer already used for done↔task matching) and print the best-scoring window as a suggestion —
`🧭 operator (suggest: none — no charter overlap)` or `🧭 score (suggest: witness — "score" overlaps
witness's coordination charter)`. This is advisory text only, printed in `--all`/`--report`; it never
posts anything or changes routing on its own. It exists to make `--reroute`'s `--owner` argument a
one-second decision instead of a guess.

## What this does NOT do (explicitly out of scope)

- **No new alarm timing.** Leak detection stays on the existing hourly `--feed` cron; event-driven
  alarm firing is a separately-scoped, unowned item in the original direction doc (batch lag was
  never named by the operator as the problem being solved here).
- **No board grammar enforcement, no reactor, no `mesh-board-journal`.** That's
  [[2026-07-24-hledger-reactive-coordination-design]], already in flight under genome's
  `[taking] event-driven-dispatch`. If/when Component 1 of that spec lands (mesh-chat rejects a
  `[task]` with no valid `owner:` at write time), the *historical* quarantine backlog and the
  writeoff/reroute tooling here remain necessary regardless — they handle the pre-existing backlog
  and the ongoing "task turned out to need reassignment" case that grammar enforcement at write-time
  can't prevent (an owner can be valid at post-time and later retired, e.g. the `chat` hold).
- **No auto-writeoff / auto-reroute.** Every resolution is an explicit, human/mind-initiated,
  board-posted, audited action — never a cron-driven silent close. A silently-written-off promise is
  exactly the kind of hidden liability CLAUDE.md's verification doctrine warns against.

## Testing (RED-first, extends the existing `--test` synthetic-board convention)

New assertions added to the existing `do_test()` fixture set, each proving a real transition:
1. A synthetic `reflex-broadcast` claim, aged past SLA → `--writeoff claim reflex-broadcast/<slug>`
   closes it; `hledger check` still balances; `equity:claims:writeoff` (not `equity:claims`) carries
   the balancing leg.
2. `--writeoff` on a slug that does **not** exist in the current open set → non-zero exit, **no**
   board post issued (assert `mesh-chat` was not invoked — the absence-guard-above-dispatch
   discipline), nothing in the journal changes.
3. `--reroute` moves an unrouted promise from `:unrouted` to a real roster window; the reopened
   `[task]` under the new owner threads to the same slug in `--all`; the old item's close lands in
   `equity:promises:reroute`, distinguishable from both `kept` and `writeoff` counts.
4. `--reroute --owner <non-roster-window>` is refused (same message as `--check`'s existing
   quarantine guidance), no board post issued.
5. Component A: a synthetic board with a non-roster `[taking]` taker and a non-roster `[verify]`
   debtor both surface `claim_unrouted=1 hold_unrouted=1` in `counts` mode (today's fixture only
   covers the promise case, per test 14 in the existing suite).
6. Component C: a suggested-owner hint fires for a lead whose tokens overlap exactly one window's
   charter comment, and prints "none" (not a wrong guess) when no window's charter overlaps at all —
   asserting the no-match case doesn't fabricate a plausible-looking but arbitrary suggestion (same
   "no silent fallback that looks like success" doctrine as everywhere else in this codebase).

## Open question for the operator

Should `--writeoff`/`--reroute` require running as (or `--as <window>`) a specific poster identity,
or is "any window can triage any other window's stuck promise" the intended model? Current design
assumes the latter (witness is the natural triage actor per its board-coordination charter, but the
command doesn't hardcode that) — flag if you want it restricted.
