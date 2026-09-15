# promise-writeoff Component D implementation — gated-auto-reaction — 2026-09-12

- Step: promise-writeoff-implementation-20260912/gated-auto-reaction (owner witness).
- Spec: promise-writeoff-reroute §D, tests 7/8/9/10. This step WROTE code (worktree
  only, NOT landed — autoland task posted for genome; deployed copy stale by design).

## Change (`scripts/mesh-promises`, ~+260 lines)

- `suggest_scores(lead)` extracted; `suggest_owner` reimplemented on it byte-identical
  (one scorer, two thresholds — hint and auto-gates can never disagree on overlap).
- `replay autoroute` (pure compute, never posts): TSV fam/owner/slug/new/lead for
  :unrouted promise/claim rows that are non-incident, past their OWN leak threshold,
  top overlap ≥ MESH_PROMISE_AUTOREROUTE_MIN (3) beating runner-up by
  MESH_PROMISE_AUTOREROUTE_MARGIN (2, lone charter reads runner-up as 0). No hold
  rows by construction. Empty unless MESH_PROMISE_AUTOREACT=1.
- `do_feed` auto phase (before materialize): loops candidates through `do_reroute`
  with reason `unrouted triage (auto)` — exact-key lookup, roster validation,
  self-address guard, NO_POST veto and verify-by-re-asking re-fire per row; a refused
  row warns loud, never aborts the pass.
- Auto-mute (same switch): reflex-broadcast claims + claims/holds whose debtor/taker
  is in MESH_RETIRED_CHANNELS, age > MESH_PROMISE_AUTOMUTE_H (72), zero [taking]/[fyi]
  engagement (board scan; a hold's OWN opening take is skipped by exact taker+ts, a
  re-take still counts; unreadable board mutes nothing). Muted rows leave
  claim_leaks/hold_leaks (one reassignment moves counts/json/report/feed/dash), keep
  every open row + liability, render in a distinct 🔇 MUTED report section + `(muted)`
  marker in --all + `muted` bool in json.
- Default-off: AUTOREACT unset → muted empty, autoroute empty, today's behavior exact.

## Evidence (executed 2026-09-12T03:5xZ)

- `bash -n` clean; `scripts/mesh-promises --test` → rc 0, `smoke-test: ok` (blocks
  58–61 = spec tests 7/8/9/10: auto-reroute fires once with (auto) trail + successor
  under same slug; incident/ambiguous/hold twins untouched; mute suppresses LEAKED
  sections + dash headline, keeps all/json/check + balances; default-off untouched).
- Mutants (all red, control green): MIN=99 → T7 FAIL; AUTOMUTE_H=99999 → T9 FAIL;
  AUTOREACT=True → collateral FAIL (proves the switch guards existing behavior).
- Two measured findings, both documented in-test, neither papered over:
  1. A hold's own opening [taking] mentions its slug — naive scan mutes no hold ever;
     fixed with the exact own-opening skip (fixture would hang otherwise).
  2. --feed's transition alert (newleaks/STATE) is PROMISE-only — claims/holds never
     posted through it. Widening it is DECLINED (alert-population change, against
     rare-and-loud); mute suppresses every surface where these families DO alert.

## Disposition

Chain promise-writeoff-implementation-20260912 complete 4/4. Landing + deploy is
genome's autoland lane (task posted).
