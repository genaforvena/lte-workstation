# mesh-mind-compact: clear on claim START too, not just finish — design (2026-07-24)

Operator direction: "/clear of context should be tied to claims/finishing tasks — /clear is both
present for starting and finishing task" + "remove all crons there too." Scope: `mesh-mind-compact`
(the `/clear` sender, `scripts/mesh-mind-compact`). Small, focused addendum — reuses the exact
mechanism [[2026-07-24-promise-writeoff-reroute-design]] models as HOLD open/close (`[taking]`/
`[done]`); different tool, same underlying board events.

## What already exists (2026-07-14, `clear_has_completion`)

`mesh-mind-compact --high-tokens` already clears an idle window the moment it has posted a
completion marker (`[done]`/`[claim-done]`/`[yield]`) since its last clear — "the ideal moment to
reset: freshest context per unit of work," ahead of the interval/threshold backstops. This is the
**finish** half. It is not new; the operator's "and finishing task" half is already live.

## The gap: no clear-on-start

Nothing today clears a window when it *takes* a new claim (`[taking] <slug>: ...`). A mind can sit
idle carrying leftover context from unrelated prior chatter or investigation (nothing that counted
as a "completion," so `clear_has_completion` never fired) and then start a fresh task on top of that
stale context. Tying `/clear` to claim-start closes this — the moment a mind commits to a new unit of
work is exactly as good a reset point as the moment it finishes the last one, and it's the same event
family `mesh-promises`' HOLD commodity already tracks (opened by a slugged `[taking]`, same
"heartbeat, not a claim" carve-out for content-free `[taking]` lines with no slug).

## Design

### Component A — `clear_has_claim_start()`

Mirrors `clear_has_completion()` exactly (same awk scan, same last-clear cutoff, same
engine-agnostic `[ \t]win@...::` anchor), but matches a **slugged** `[taking]` line instead of a
completion marker: `[taking] <slug>: ...` — the same discipline `mesh-promises`'
`taking_slug_and_rest()` already enforces (a bare content-free `[taking]` with no `<slug>:` lead is
a heartbeat, never a claim, must not trigger a clear). Reuses the cutoff-advances-past-the-line
property `clear_has_completion` already has, so the same claim-start line can't re-fire the clear on
a later idle check.

### Component B — precedence in `clear_reason()`

```
1. post-claim   — clear_has_completion (existing) — state already externalized, strongest signal
2. claim-start  — clear_has_claim_start (new)
3. hold-leak    — NEW, replaces the wall-clock interval (Component C)
4. ctx %        — opencode-only backstop (existing, unchanged)
```
If a window shows both a start and a finish since its last clear (rare — implies a very fast claim
cycle within one idle-check window), `post-claim` wins and is logged as the reason; behavior is
identical either way (a clear fires), this only affects the logged reason string.

### Component C — the fallback becomes an hledger query, not a wall-clock timer

Operator pushback, and it lands: `MESH_COMPACT_INTERVAL` (a raw idle-seconds counter with no
relationship to what's actually happening) is exactly the kind of decision this session has been
moving OUT of ad hoc local state and INTO the ledger everywhere else. Revised design — **delete
`MESH_COMPACT_INTERVAL` entirely**; replace its two jobs with two hledger-native queries, each using
a ledger the mesh already keeps rather than a new counter:

**"A claim is stuck" → read it from `mesh-promises`, don't reinvent it.** `mesh-promises` already
computes, per open HOLD, `age_h` and `leaked` against its own `MESH_PROMISE_LEAK_H` threshold — the
exact "has this claim gone stale" fact `mesh-mind-compact` was approximating with its own unrelated
timer. New reason `hold-leak`: query `mesh-promises --json`, filter holds where `taker == win`, fire
if any is `leaked: true`. One shared definition of "stale" across the whole mesh instead of two
disconnected ones (`MESH_PROMISE_LEAK_H` vs `MESH_COMPACT_INTERVAL`) that could — and did, as two
independent constants always eventually do — drift apart.

**"Keep context lean regardless of claims" → read it from `mesh-labor`, not a clock.** The
interval's *other* job (proactive quota/context hygiene, independent of whether a claim is even
open — the header's original "keep every mind's CONTEXT lean... quota usage low") isn't about time
elapsed, it's about *work done*: a window doing many turns quickly bloats context fast; a window
sitting mostly idle for hours barely grows it. `mesh-labor --register expenses:labour:<win>
date:>=<last_clear_iso>` (hledger's own date-filtered register — no new counter, just an existing
query with a `date:` bound) gives TURNs-since-last-clear directly. New reason `turn-ceiling`: fires
when that sum crosses `MESH_COMPACT_TURN_CEILING` (default 40 — sized against `mesh-labor`'s
existing rolling-5h budget figures, tuned once real per-window burn is visible on the tape, same
"arm once measured" caveat the reactive-coordination spec already carries for its own budget knobs).

**What this does NOT claim:** eliminating *execution scheduling* is a different, and impossible,
ask from eliminating *decision authority*. Something must still periodically run these two queries
and act on the answer — a check that nothing ever invokes checks nothing, and CLAUDE.md's own
"never-wired-reflex" doctrine is precisely the failure mode of assuming a declared check runs itself.
What changes here is that the thing being checked is now 100% ledger-derived (mesh-promises' HOLD
leak state, mesh-labor's TURN register) — the outer `*/10 * * * * mesh-mind-compact --high-tokens`
poll (or eventually [[2026-07-24-hledger-reactive-coordination-design]]'s inotify reactor, once that
lands) is purely the invoker, carrying zero staleness opinion of its own. `mesh-clear-audit` (*/5)
and `mesh-clear-loss --canary` (daily) are unchanged — they're post-hoc quality instruments, not
decision points, and they're what caught the 2026-07-21 stale-handoff regression in the first place.

**Failure mode when the ledgers are absent/unreachable:** `hold-leak`/`turn-ceiling` are additive
fallback tiers under the two event triggers, which don't depend on either ledger at all. If
`mesh-promises`/`mesh-labor` are missing or error, these two reasons simply never fire (fail-open in
the *safe* direction here — a missing optional backstop means "no extra clear," never a false
"clear now" or a false "never clear"; per this codebase's own recurring fail-open/fail-safe framing,
absence must never manufacture a plausible-looking answer). A window with an active claim and no
ledger tooling installed still gets `post-claim`/`claim-start` exactly as before — those two never
depended on either ledger.

## What this does NOT do

- No change to `handoff_gate`, `bg_gate`, the render ladder, or any existing safety gate — the new
  trigger is purely an additional *reason* fed into the same already-gated `send_compact` path.
- No opencode-specific change — `clear_has_claim_start` is engine-agnostic like its sibling.
- No change to `mesh-clear` (the interactive gated `/clear` a mind runs on itself) — this only
  touches the cron-invoked `mesh-mind-compact --high-tokens` reflex path.

## Testing (extends the existing `--test` fixture set, same RED-first convention)

1. A window posts a slugged `[taking] widget-audit: ...` since its last clear, no completion marker
   → `clear_reason` returns `claim-start`.
2. A window posts a content-free `[taking]` (no `<slug>:` lead) since its last clear → **no** claim-
   start trigger (mirrors the existing HOLD content-free carve-out; regression guard against treating
   a heartbeat as a claim).
3. A window with both a `[taking]` and a later `[done]` since its last clear → reason is `post-claim`
   (precedence), not `claim-start` — proving the precedence order, not just that a clear fires either way.
4. `hold-leak`: a synthetic `mesh-promises --json` (via `MESH_COMPACT_PROMISES_CMD` test override,
   same override-injection pattern this tool already uses for `MESH_COMPACT_SNAPSHOT_CMD`/
   `MESH_COMPACT_BG_GATE_CMD`) reports a leaked HOLD for `taker == win` → `clear_reason` returns
   `hold-leak`. A second window with an open-but-**not**-leaked hold does not fire.
5. `turn-ceiling`: a synthetic `mesh-labor --register` output (same override pattern,
   `MESH_COMPACT_LABOR_CMD`) summing above `MESH_COMPACT_TURN_CEILING` since last-clear → fires
   `turn-ceiling`; below the ceiling → does not fire.
6. Ledger-absent fail-open: with both override commands pointing at a nonexistent binary (simulating
   `mesh-promises`/`mesh-labor` not installed), a window with no claim activity produces **no** clear
   reason at all (not a false positive, not a crash) — proving the two new tiers degrade to inert
   rather than to an unsafe guess.
7. Cutoff-advance: after a claim-start-triggered clear, the SAME `[taking]` line must not re-trigger
   a second clear on the next idle check (mirrors the existing post-claim cutoff-advance test).
