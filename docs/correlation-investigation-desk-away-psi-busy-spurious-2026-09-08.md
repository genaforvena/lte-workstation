# Correlation investigation: `desk=AWAY` → `psi=BUSY`

**Date:** 2026-09-08  
**Verdict:** **SPURIOUS / discard.** No fused sense or reflex.

## The queued claim and the live re-check

The queued snapshot says: lift **1.85**, 14 episodes / 8 occasions, since
`2026-08-15T17:40:01Z`, 15.2% of a 900.2-hour window. That exact snapshot is no
longer reproducible because the live tape has advanced and rotated its effective
window: it currently ends at `2026-09-08T19:50:01Z`.

Re-filtering the current real `~/.mesh/sensor-tape.tsv` from the claim's era
start gives 578.2 hours of data, 1,110 aligned usable rows, and:

| measure | current era |
|---|---:|
| `desk=AWAY` | 253 |
| `psi=BUSY` | 331 |
| joint rows | 93 |
| raw row lift | 1.23 |
| one-hour-collapsed joint episodes | 25 |
| hour-shadow expected joint rows | 77.14 |
| hour-shadow adjusted lift | 1.21 |

The current configured miner independently reaches the same disposition: it
does not emit `desk=AWAY ↔ psi=BUSY` from the live tape; its full-window
candidate is only a 2.23 lift and is marked `invariance=UNSTABLE` (1 of 9
environments clears 1.8), so no stable generalization or seed is justified.

## Reality check

`desk=AWAY` is not a direct person-presence sensor. In
`scripts/mesh-desk-state`, it is emitted when the iMac is `UNREACHABLE`, with
the reason “iMac off or asleep — operator away from desk.” Its own log also
records repeated “iMac unreachable + phone offline — cannot assess” cases. It is
therefore an availability/power proxy for the remote iMac, often during the
same night or network regime that changes what the rest of the mesh can read.

`psi=BUSY` is independent local kernel pressure on this workstation: the tool
classifies CPU/IO/memory PSI, with `BUSY` meaning some-pressure ≥25% or any
full pressure. Recent `psi.log` BUSY rows identify CPU pressure and
`who=user.slice`, while other BUSY/CALM transitions are held/debounced. This is
resource contention on the mind node, not evidence that a person has left the
iMac.

The relation also fails the miner's environment invariance test. The one
environment that clears the floor is `env17` (2.66); the other eight qualifying
environments range from 0.00 to 1.44. That is the signature of a local
workload/availability regime, not a repeatable desk-to-pressure coupling.

## Decision

**Discard in one line:** `AWAY` means remote-iMac unreachable/asleep while
`BUSY` means this node's kernel pressure; their overlap is an unstable
availability/night/workload regime, and the current hour-adjusted era lift is
only 1.21, so a fused sense or reflex would turn a proxy coincidence into an
action.

## Verification

Passed against the live source and wiring:

```text
bash scripts/mesh-correlate --test   # rc 0
bash scripts/mesh-desk-state --test # rc 0
bash scripts/mesh-psi --test        # rc 0
```

`scripts/mesh-correlate` and `~/.local/bin/mesh-correlate` have identical
SHA-256 (`b8ee…a2cb0a`); no source or deployed tool was edited. This artifact
is intentionally uncommitted for the steward.
