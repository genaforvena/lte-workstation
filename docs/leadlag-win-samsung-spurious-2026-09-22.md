# Lead-lag investigation: `WIN-Q6GL9FIR3QI` → `[TV] Samsung 5 Series (40)`

**Date:** 2026-09-22
**Disposition:** **SPURIOUS / discard.** No fused sense and no reflex.

## Reproduction

`mesh-leadlag --dry` / `--list` (2026-09-22T06:37Z, rc=0): honest empty —
"no stream predicts another above the permutation null (need more data / more live numeric
streams / cross-node tapes)". The queued candidate (r=-0.83 at lag 8 over 10 aligned Δ-steps,
48h window, perm p=0.040, circular p=0.007) does not survive the live tape.

## Reality check

- Both "streams" are BLE visibility traces from the same `~/.mesh/presence.log` scans, not
  independent movement sensors. `WIN-Q6GL9FIR3QI` appears in only 18 scans total (one 2026-08-04
  sighting + a 2026-09-18 cluster); the sampled joint scan (2026-08-04T22:30:10Z, n=10) shows it
  co-visible with the Samsung TV, Bose speaker, Quest, and rotating `?` MACs in one radio sweep.
- The claimed effect sits **at the sweep edge** (lag 8 = max swept): the task itself states the
  profile "has not peaked inside the window, so 80 min is a LOWER BOUND, not a measurement".
  An edge-maximum over 10 aligned steps with 8%/83% presence coverage asymmetry is a scan-schedule
  / visibility-regime artifact, not a measured delay.
- OUT-OF-WINDOW hold-out is `na (0 steps, UNREPLICATED)` — zero independent confirmation.
- A Tailscale peer's radio visibility cannot physically drive a TV's movement 80 min later; the
  shared driver is the scanner's own duty cycle plus household radio environment.

## Decision

Discard in one line: **a Tailscale peer's BLE visibility in 18 shared scans cannot drive a TV's
movement 80 min later — sweep-edge maximum over 10 steps with zero hold-out is a scan-schedule
coincidence, not a propagating process.**

## Verification

- `mesh-leadlag --dry` / `--list` — rc=0, honest empty.
- `grep -c WIN-Q6GL9FIR3QI presence.log` → 18; joint-scan attribution inspected.
- No tool edited; receipt left uncommitted for steward landing.
