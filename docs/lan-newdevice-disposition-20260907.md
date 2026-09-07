# `lan-newdevice` escalation disposition — 2026-09-07

Decision: **(c) accept as-is with an expiring visible mute**. The repeated repair class is
wrong. `lan-newdevice` is executing, but the LAN organ needed for a current reading is absent
or unreachable on `mesh-home`; this is not a broken local reflex to repair and not a decay
candidate.

## Evidence

- `mesh-reflex-health --check` reports `organ-blind: lan-newdevice`: the last real reading is
  frozen at 2026-09-02T20:24:22Z, while the tool's blind-marker was touched during the 2026-09-07
  check. The reflex is
  therefore running on schedule and explicitly says not to repair it.
- `mesh-lan-newdevice --status` reports: `router DHCP + LAN ARP both unreachable — can't assess
  (not an alarm)` and exits `0` because unavailability is an abstention, not an alarm.
- `mesh-lan-newdevice --test` passes its offline smoke checks (`11` groups, `67` assertions), but
  does not manufacture a live LAN reading. This is not proof that the absent organ is available.
- The source and deployed hashes match:
  `scripts/mesh-lan-newdevice` and `~/.local/bin/mesh-lan-newdevice` both
  `df216109878388eed523b101e0f02f3587c18a98e6231742e1644cb38fd46a68`.
- `~/.mesh/needs.log` contains 48 historical `REFLEX REPAIR` injections and one
  `cue-pinned ESCALATED -> lan-newdevice (n=4)`, confirming repeated re-filing of the wrong
  class rather than four independent tool failures.

## Discharge

The existing ruling is live and visible through `mesh-needs --rulings`:

```text
mesh-needs --rule reflex:lan-newdevice 7 "accept LAN organ absence on this node; mesh-reflex-health reports organ-blind, --status says DHCP+ARP unreachable, and --test only passes offline smoke checks; recheck after expiry"
```

It expires at `2026-09-14T18:53:25Z`. No repair was re-run, no deployed copy was edited, and no
permanent mute was created. `mesh-needs --check` currently reports no acute deficit because the
blind-organ state is no longer emitted as a repair deficit; the ruling remains visible in the
rulings surface and will be re-evaluated after expiry.

## Verification

```text
bash -n scripts/mesh-lan-newdevice scripts/mesh-needs       PASS
mesh-needs --rulings                                       LIVE reflex:lan-newdevice
mesh-needs --check                                         no acute deficit
source/deployed SHA-256                                   equal
```

Next action: after `2026-09-14T18:53:25Z`, re-check LAN-organ availability and let the deficit
re-file only if the organ is still unavailable; do not repeat the repair class before then.
