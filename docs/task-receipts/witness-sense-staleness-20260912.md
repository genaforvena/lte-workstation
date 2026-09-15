# Witness sense staleness triage — 2026-09-12

Task: `witness-chat-range-review-near-56474-56609-followthrough/triage-stale-sensors`  
Close key: `task:triage-stale-sensors`

The assignment was live: the dispatch appeared on the board at 13:53:21Z, with no later
completion at the time of inspection. The cited witness rows from 13:28:48–13:42:19Z reported
`senses_dist=…/3s/0u`. Those three stale tags map to the following named sensorium fields; the
identity comes from the sensorium's per-field artifact readers and timestamps, not from the
aggregate count.

| Sensorium field | Actual input and artifact | Freshness / coverage at live probe | Test and finding |
|---|---|---|---|
| `PRESENCE` | `mesh-sensorium` reads the final record in `~/.mesh/presence.log` directly. The file mtime is `2026-08-30 07:10:12Z`; the last row still reports `n=8`. | The sensorium TTL is 900s (15m); this record was about 13d 6h old at 13:56Z, so there were no fresh presence observations in the TTL window. The `*/10` `mesh-presence --log` cadence is still present in `~/.mesh/reflexes.cron`, but repeated cron output and `mesh-presence --log` report no Bluetooth adapter (`/sys/class/bluetooth` empty). | `mesh-presence --test`: `n/a` because no BT adapter is visible. The live read also exits without a new record. This establishes an unavailable radio path; it does not distinguish a disconnected combo device from a driver/kernel failure. |
| `ROOM ambient` | Sensorium reads `~/.mesh/.ambient-clock.state` (`DATA-STALE|dwell_s=170930|changes_24h=0|fixture=CYCLING`). `mesh-ambient-clock` derives this from `presence.log`. | Sensorium TTL is 2100s (35m); this state mtime is `2026-09-11 14:34:52Z`, stale at inspection. Live `mesh-ambient-clock --json` reports `data_stale=true`, `scan_count=0`, `nonempty_scans=0`; the BLE input was 19,125 minutes old against the current 20m adaptive threshold. There is no live BLE coverage. | `mesh-ambient-clock --test` passes its classifier/fixture checks, not a hardware read. The cron entry was explicitly marked DECAYED on Sep 10 because its BLE feeder was stale. Keep it decayed; re-enabling it would refresh a stale-derived state without restoring evidence. The blocker is the same missing BT input above. |
| `ROOM wifi-motion` | Sensorium reads `~/.mesh/.wifi-motion-state` (mtime `2026-08-30 08:03:01Z`) for display. The actual classifier input is `~/.mesh/wifi.log`, whose last scan is `2026-08-30 07:36:36Z`. | Sensorium TTL is 1200s (20m); the classifier's tape-stale limit is 1800s (30m). At 13:56Z, `mesh-wifi-motion --json` reported `age_s=1146045`, `stale_limit_s=1800`, `reason=tape_stale` and exited 2. There were no Wi-Fi scan samples in the freshness window. | `mesh-wifi-motion --test` passes synthetic classifier fixtures only. `mesh-wifiscan --test` is `n/a` because this node has no visible Wi-Fi radio/scan backend. A live `mesh-wifiscan --log` made five attempts, each returned zero APs, and correctly declined to append a scan. The scan cadence is present in cron; the input hardware/backend is unavailable. No local software repair is evidenced. |

The three named findings are therefore two unavailable radio-backed inputs (Bluetooth presence
and Wi-Fi scans) plus ambient-clock's explicitly decayed derivative of the Bluetooth tape. The
tests that returned green do not establish hardware reads: the presence and Wi-Fi scan tests
abstain with `n/a`, while the ambient and wifi-motion tests exercise fixtures. No timestamp,
synthetic observation, or schedule change was applied. The receipt records the concrete external
blocker: the kernel-visible Bluetooth adapter and Wi-Fi scan backend are absent; the observation
does not prove whether the combined USB radio is physically disconnected or failing in its
driver.

During this investigation the live count rose to four stale tags. `SITUATION situation=` is the
additional tag: `~/.mesh/.situation.state` was last written at 12:57:10Z and has a 3000s display
TTL. It was still within TTL at the cited 13:42:19Z row, then crossed the boundary before the
13:52:15Z witness row (`4s/0u`). It is a later, separate stale derived artifact, not one of the
three tags being mapped from the original observation window.

## Verification

- Confirmed the dispatch still live, claimed it as senses, and traced each displayed tag to the
  corresponding reader in `scripts/mesh-sensorium`.
- `mesh-presence --test`: n/a; `mesh-wifiscan --test`: n/a.
- `mesh-ambient-clock --test`: pass (fixture/classifier checks only).
- `mesh-wifi-motion --test`: pass (synthetic tape/classifier checks only).
- Live probes: `mesh-presence --log` unavailable; `mesh-ambient-clock --json` DATA-STALE with
  zero scans; `mesh-wifiscan --log` zero APs / no append; `mesh-wifi-motion --json` exits 2 on
  the 1,146,045s-old tape.
- `mesh-situation --test` passed; it is outside the original three-tag mapping. No sensor,
  substrate, or schedule configuration was changed.
