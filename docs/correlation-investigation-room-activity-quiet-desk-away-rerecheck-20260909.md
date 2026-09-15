# room_activity=QUIET ↔ desk=AWAY — current reality check

**Date:** 2026-09-09 22:30Z · **Verdict:** discard; no fused sense or reflex.

## Evidence

The live `scripts/mesh-correlate --dry --lift` run over the current sensor tape
(`2026-07-14T22:40:01Z`–`2026-09-09T22:30:01Z`, 1367.8 h) produced:

```text
lift 2.32 (37 episodes), hour-stratified ... shadow 1.52;
26 distinct occasions / 37 episodes of 1335;
invariance=UNSTABLE: clears the 1.8 floor in 2 of 4 environments;
seed withheld
```

The same run says the uncorrected full-window lift is 2.8 and labels it
confounded. The environment lifts are 1.50, 2.04, 1.22, and 4.56; this is not
stable enough to generalize or wire into behavior.

The raw aligned tape has 4943 rows, 207 `room_activity=QUIET`, 253
`desk=AWAY`, and 64 joint rows. The naive all-row lift is 6.04, but restricting
to both senses' real readings still gives 4.71, while the all-phone-real subset
has only 45 rows and 2 joint rows (lift 1.13; 1.23 in the desk era). The latter
is the honest reality check: the apparent association collapses when the shared
phone availability gate is not allowed to manufacture observations.

The live organs confirm that this is an availability artifact, not a discovered
room/desk mechanism:

```text
room-activity: UNCERTAIN ... degraded=body:unreachable,wifi:unreachable,light:unreachable,...
desk-state: iMac unreachable + phone offline — cannot assess
body-motion: phone unreachable — no body-motion read
wifi-link: phone offline ...
```

`mesh-desk-state` explicitly fuses phone body-motion and phone availability,
and defines `AWAY` from an unreachable iMac; `mesh-room-activity` also consumes
phone-dependent body, Wi-Fi, light, BLE, and media signals. Thus the two labels
can co-occur when the phone/iMac observation path is unavailable, even though
the physical room and desk have not supplied corroborating evidence.

## Decision

Discard in one line: **the lift is environment-unstable and collapses to ~1.1
after removing the shared phone/availability gate; it is spurious sensor
co-occurrence, not a useful fused sense or reflex trigger.**

No mesh tool was edited. Source and deployed `mesh-correlate` remain byte-identical
(SHA-256 `b8eeef061ec3f15f0d9a965b558c4dd562399a3b2be421cc8bc8c71983a2cb0a`).

## Verification

- Fresh `scripts/mesh-correlate --dry --lift` run: pair present, corrected lift and
  unstable invariance reported, seed withheld.
- Direct current-tape counts and phone-real subset calculation recorded above.
- Source/deployed parity checked with `sha256sum`.
- No commit made; unrelated pre-existing worktree changes were preserved.
