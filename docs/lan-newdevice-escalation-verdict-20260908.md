# `lan-newdevice` escalation verdict — 2026-09-08

Decision: **(c) accept as-is with an expiring visible mute**. No source fix or repeated repair was made.

## Root-cause finding

The deficit is not a dead scheduler/reflex. `mesh-reflex-health --check` is green and explicitly reports
`lan-newdevice` as **organ-blind**: the last real LAN read is frozen, while the tool's blind marker was
touched seconds ago. That means the reflex is running on schedule but the LAN organ is unavailable on
this node. A bounded live `mesh-lan-newdevice --status` probe also timed out after 8 seconds (`rc=124`),
consistent with the unavailable DHCP/ARP path. The offline `mesh-lan-newdevice --test` passes only its
constructed smoke checks; it cannot make the absent LAN organ observable.

The same source is deployed without drift:

```text
scripts/mesh-lan-newdevice == ~/.local/bin/mesh-lan-newdevice
sha256 df216109878388eed523b101e0f02f3587c18a98e6231742e1644cb38fd46a68
```

The liveness beat is stale (`2026-09-02T20:24:22Z`), but the blind marker was fresh at the check
(`2026-09-08T21:23:01Z`); this is the expected distinction between a scheduled blind organ and a dead
reflex. The historical repair queue entries therefore targeted the wrong fix class.

## Discharge

A live ruling already exists in `~/.mesh/needs-rulings`:

```text
reflex:lan-newdevice — expires 2026-09-14T18:53:25Z
reason: accept LAN organ absence on this node; recheck after expiry
```

`mesh-needs --check` now returns `needs: none` because the current deficit is visibly covered by that
standing ruling; `mesh-needs --rulings` remains the visibility surface. This is not a permanent mute.
At expiry, rerun `mesh-reflex-health --check`, `mesh-lan-newdevice --status`, and the real LAN probe;
repair only if the organ has returned and the reflex itself is then failing.

## Fresh verification

- `mesh-reflex-health --check`: rc 0; 38 per-run reflexes fresh; `lan-newdevice` labelled organ-blind.
- `mesh-needs --check`: rc 0; no active unruled deficit.
- `mesh-needs --rulings`: live `reflex:lan-newdevice` ruling through `2026-09-14T18:53:25Z`.
- `mesh-lan-newdevice --status` under an 8-second bound: rc 124 (DHCP/ARP path unavailable).
- `mesh-lan-newdevice --test`: rc 0, offline smoke suite only; not evidence of a live LAN read.
