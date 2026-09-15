# Sense liveness — proximity decay — 2026-09-09

## Disposition

`mesh-proximity` was cron-wired and smoke-green, but had no fresh real BLE artifact:

- `mesh-reflex-health --check` before action: rc 0, 38 fresh per-run reflexes; `proximity`
  was `BLIND`, with its real state frozen for about 866000s and its blind marker freshly touched.
- `mesh-proximity --scan`: `2026-09-09T08:17:45Z proximity: UNCERTAIN — BLE scan failed [devices=0]`, rc 2.
- `mesh-proximity --test`: rc 2, explicitly `proximity sense DECAYED` because `/sys/class/bluetooth`
  is empty/absent; the smoke classifier itself still passed its fixture leg.

The organ is marked honestly decayed. The source and deployed copy carry an `orphan-ok: DECAYED`
reason, and both active scheduler copies were tombstoned. No proximity state was fabricated or
refreshed.

## Sense probe matrix

| probe | result |
|---|---|
| sensorium | rc 0; smoke green; presence organ absent |
| location | timeout/unknown |
| light | timeout/unknown |
| body-motion | rc 2; phone unavailable |
| room-sense | timeout/unknown |
| wifi-motion | rc 0 |
| ambient-clock | rc 0 |
| operator-state | rc 0 |
| situation | timeout/unknown |
| sense-monitor | rc 0 |
| sensor-log | rc 0; no Wi-Fi scanner warning |
| arrivals | rc 0 |
| lan-newdevice | rc 0 smoke; live organ blind |
| macsocks-health | rc 0 |
| proximity | rc 2; DECAYED/no BT adapter |
| wifi-link | timeout/unknown |
| kbd-activity | rc 2; organ absent |
| wifi-rf | rc 2; organ absent |
| power | rc 0 |

## Post-action verification

- `scripts/mesh-proximity`: `bash -n` rc 0; deployed path is the same symlinked source.
- Active `mesh-proximity` launcher count: `reflexes.cron=0`, live `crontab=0`.
- `mesh-reflex-health --check` at `2026-09-09T08:19:38Z`: rc 0, 37 fresh reflexes; `proximity`
  no longer appears as scheduled/blind. Remaining `lan-newdevice` and `wifi-link` blindness is
  reported separately.
- Fresh real control artifact at `2026-09-09T08:19:38Z`: `mesh-power --status` →
  `power: MAINS status=no-battery`, rc 0.

No commit made.
