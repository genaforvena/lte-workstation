# Publication vet — body-context --power: a pose that fused three senses instead of trusting one

Date: 2026-09-21 UTC
Source: `scripts/mesh-body-context` commit `a0763444` (2026-09-20T17:48:26Z, +83/-7)
Live check (this wake, 2026-09-21): `scripts/mesh-body-context --power` rc=0 →
`DOCKED — parked on charger (stillness explained by docking, not attendance) | lux=10 (lit) | power=plugged`

## The failure, in one sentence

`[body-still]` + a lit room read **RESTING** — "parked but lights on, someone's around" — and that
label conflated two worlds: a body on a charger (stillness *explained* by docking) and a body on
battery in a lit room (someone actually *is* around). One pose label, two opposite situations, and
motion and light between them cannot tell you which.

## What the measurement proves

The fix is a third fused sense, not a better threshold on the existing two:

- `--power` adds one bounded SSH read of `termux-battery-status` on the transport `mesh-body-motion`
  already proved reachable (`ConnectTimeout=6`, `timeout 15`), parsed by a **pure, offline-testable**
  `classify_power()`: `PLUGGED_*` → `plugged`, `UNPLUGGED` → `battery`, anything unparseable,
  truncated or empty → `na`.
- `derive_situ` then re-labels only the **parked** cases: `RESTING`/`DORMANT` + `plugged` → `DOCKED`.
  A carried, handled or stowed body on a power bank stays `TRAVELLING`/`HANDLED`/`STOWED` — the
  charger does not override a live interaction.
- Live this wake: motion still, lux 10 (lit), probe `plugged` → the emitted label is `DOCKED`, which
  **no single sensor in the chain gives**: motion says still, light says lit, charge says tethered —
  together they say docked, not attended.

The claim worth publishing on is the honesty rule, because it is the one that would have been
tempting to skip:

> An unreachable charge probe renders `power=n/a`, the pose label stays **unchanged**, and earns no
> docked marker.

`na` is visibly distinct from `battery`: an unreadable charge read is **not** "on battery". A failed
probe cannot manufacture the docked claim, and it cannot manufacture the tamper-clear claim either —
the pre-existing `tamper=na` rule is the same shape on its own axis (`tamper=na` must not carry
"tamper-clear", and must render differently from `tamper=quiet`).

## The falsifiable surface

Commit `a0763444` carries the assertions in `--test`, each a one-line check that goes red if the
fusion silently degrades:

- `still+lit + plugged` → `DOCKED`; `still+dark + plugged` → `DOCKED`
- `still+lit + battery` → `RESTING` (unchanged — the fusion must not dock on battery)
- `still+lit + power-na` → `RESTING` (unchanged — unreachability earns nothing)
- `still+lit`, power not requested → `RESTING` (backward compatible; the default is unchanged)
- `carried + plugged` stays `TRAVELLING`; `handled + tamper-moved + plugged` stays `INTERACTED`
  (an active disturbance outranks the charger)
- `docked + tamper-quiet` keeps the `tamper-clear` marker
- `classify_power` on `PLUGGED_AC` / `UNPLUGGED` / `garbage` / empty → `plugged` / `battery` / `na` / `na`

Verified this wake: `scripts/mesh-body-context --test` →
`smoke-test: ok (derive_situ: pose + moved→DISTURBED/INTERACTED + quiet-clear + na≠quiet + n/a-path-speaks + reachability)`,
rc=0. The `na≠quiet` and `n/a-path-speaks` assertions are the ones that pin the honesty rule to the
code — drop the `na` clause and exactly that leg goes red while every green-verdict case stays green.

## What remains UNKNOWN

- **This is a one-axis, one-node measurement.** I proved the fusion's decision logic and its live
  emission on mesh-home. I did **not** measure how `DOCKED` behaves across a long-running dock→undock
  transition, nor how consumers downstream of body-context react to the new label. No consumer
  contract change is claimed here.
- The live probe path depends on `mesh-phone-ip` resolving the phone and on the phone's SSH endpoint
  being up. The endpoint on this node has flapped recently (`OK → TIMEOUT → REFUSED` inside ~25 min,
  2026-09-20, `~/.mesh/evidence/senses-body-power-20260920/receipt.md`); that receipt concluded the
  *organ* was live and the transport was down, which is the read-path shape, not a fusion-shape claim.
  I did not reproduce that flap this wake, and the `power=n/a` rule is exactly what renders during it.
- The probe reads the `plugged` field alone. A battery that is `UNPLUGGED` at 100% and a battery at
  3% are the same `battery` to this fusion; charge level is not an input and no low-battery claim is
  made.
- No claim is made here about the other 2026-09-21 sense novelties (baro read-path, situation-unstuck
  blind gate, cellsignal/touchidle/tamper MCC closures). Each is a separate vet case —
  `docs/pub-vet-baro-read-path-20260921.md` and `docs/pub-vet-situation-blind-gate-20260921.md`
  cover two of them.

## Why this is publishable as a measured case

The generalisable shape is **a pose label that was silently disambiguated by an input it did not
have**. Two different situations had collapsed onto one label because the two senses available could
not separate them; the fix was to fuse the third sense that actually carries the distinction, and to
make the missing-sense case render as a visibly distinct `n/a` instead of a silent default.

That transfers anywhere a fused label is emitted from a subset of the senses that determine it: if
your label is "someone is around" and your inputs are motion + light, you have not measured
attendance, you have measured stillness-in-light. The corrective is to name which input would
disambiguate, read it, and — the part that generalises hardest — decide *before* you deploy what an
unreadable version of that input is allowed to mean. Here an unreadable charge state is allowed to
mean "the label you already had", and is forbidden from meaning "docked".

The sibling case in the same codebase makes the pattern visible twice: `tamper=na` must not earn
"tamper-clear" for the identical reason — an unreachable input must not produce a stronger claim than
a read one.

## Vet decision

**Publishability: draft-ready for a human-facing dev.to draft; no further code change needed.** The
case is bounded, its decision logic is asserted offline by `--test` and its live emission was
reproduced this wake. The three enforceable behaviours a draft would hang on:

- `plugged` on a parked body re-labels to `DOCKED`, and only on a parked body
- `power=na` changes nothing — never a silent docked claim on an unreachable probe
- `na` is a distinct render from `battery`, on both the power and the tamper axes

Not for external publication: the undocked-transition behaviour and downstream consumer reaction
(UNKNOWN, above), the phone-endpoint flap (stated as reported, not reproduced this wake), and any
claim that the other 2026-09-21 sense novelties share this failure mode.

Acceptance check: this artifact records the exact source commit and its live output, states the
fusion's three-sense composition and the `na` honesty rule, gives a bounded publishability
recommendation with named UNKNOWNs, changes no deployed state, and adds no claim about unvetted
cases. No commit was made by this vet; the worktree's pre-existing dirty paths
(`scripts/mesh-omp-lifecycle`, `scripts/mesh-queue-tend`) are untouched, and no state file was
written by `--power` (it composes cached/derived context only).
