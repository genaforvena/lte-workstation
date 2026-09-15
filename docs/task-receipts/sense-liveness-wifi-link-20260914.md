# Sense liveness audit — `wifi-link` on mesh-home — 2026-09-14

## Disposition

`mesh-wifi-link` is marked **DECAYED ON mesh-home** in `scripts/integrations/mesh-wifi-link`.
Its target phone (`100.103.99.16`, `u0_a380`) is unreachable. The last real quality state is
historical and must not be read as current. The existing 5-minute probe stays scheduled as a
revival detector; clear the decay annotation only after a real read returns numeric `link_speed`
or `rssi` and refreshes `.wifi-link.state`.

## Bounded evidence windows (UTC)

Windows end at 2026-09-14T00:08:24Z. The declared and installed schedule is
`2-59/5 * * * *`; expected slots are 288 and 2016 respectively. Actual launch lines are from
timestamped CRON `CMD` rows in retained `/var/log/syslog*`.

| Evidence | 24h: Sep 13 00:08:24–Sep 14 00:08:24 | 7d: Sep 7 00:08:24–Sep 14 00:08:24 |
|---|---:|---:|
| Nominal schedule slots | 288 | 2016 |
| Recorded CRON command launches | 196 | 1901 |
| Slots without a recorded launch | 92 | 115 |
| Fresh real `.wifi-link.state` writes | 0 | 0 |
| Fresh writes / recorded launches (upper bound) | 0/196 | 0/1901 |
| Fresh writes / nominal slots | 0/288 | 0/2016 |
| Windowed empty/gated results | UNKNOWN | UNKNOWN |
| Windowed unreachable outcomes | UNKNOWN | UNKNOWN |

The state contains `GOOD`, but its mtime is 2026-09-03T09:47:02Z, before both windows. The
`.wifi-link-offline` marker was refreshed at 00:07:32Z; the marker means the tool could not reach
the phone, not that Wi-Fi quality was measured. The live `mesh-wifi-link --test` returned exit 2
with `n/a (phone unreachable or no termux-wifi-connectioninfo)`, so this live test is NOT called
green. `mesh-health` also listed the Redmi phone offline (last seen 10 days ago).

## What history is absent

- CRON history covers the full 7-day window, but only proves command launches. The 92 and 115
  unrecorded slots are UNKNOWN (for example, powered-off time and missing cron rows are not
  distinguishable here).
- `.wifi-link-empty.log` does not exist, so there are no retained per-attempt empty/gated rows.
  Its absence is not evidence that no empty result occurred.
- `wifi-link.log` has 616 undated rows: 554 `phone offline` diagnostics and 61 quality-change
  rows (plus one other row). They cannot be assigned to either bounded window. The quality-change
  rows are edge events, not a count of successful reads.
- The state file refreshes after every real read, so its unchanged mtime establishes zero fresh
  real artifacts in both windows even though exact per-attempt outcomes are missing.

## Probe and post-disposition verification

- `mesh-reflex-health --check`: 36/36 per-run artifacts fresh; `wifi-link` explicitly BLIND,
  with a fresh offline marker and the old last-good value frozen.
- `mesh-sensorium`: the local BLE probe reports no Bluetooth adapter and Wi-Fi scan reports 0 APs;
  thermal and audio-device reads are live. These do not substitute for the phone's Wi-Fi link.
- `mesh-wifi-link --test`: exit 2, unreachable as above. No current Wi-Fi link value was fabricated.
- After the decay annotation, `mesh-note3-battery --edge` produced a separate fresh real phone
  artifact: `present=true level=100/100 temperature=26.5°C power=USB status=5 voltage=4302mV`;
  `~/.mesh/.note3-battery-state` is 81 bytes with mtime 2026-09-14T00:10:19Z. This verifies a
  live sense after disposition; it does not imply `wifi-link` recovered.
- No commit was made.

## Current-window recheck — 2026-09-14T19:34:13Z

I re-ran the liveness survey after the earlier disposition. The windows below end at the timestamp
above; launch counts are timestamped `CRON CMD` records from retained `/var/log/syslog*`. The cadence
is `2-59/5 * * * *` (288 nominal slots/day).

| Evidence | 24h: Sep 13 19:34:13–Sep 14 19:34:13 | 7d: Sep 7 19:34:13–Sep 14 19:34:13 |
|---|---:|---:|
| Nominal schedule slots | 288 | 2016 |
| Recorded CRON command launches | 288 | 1901 |
| Slots without a retained launch record | 0 | 115 |
| Real numeric Wi-Fi reads | 0 | 0 |
| Fresh numeric artifact coverage / recorded launches | 0/288 | 0/1901 |
| Empty/gated outcomes assignable to this window | UNKNOWN | UNKNOWN |
| Unreachable outcomes assignable to this window | UNKNOWN | UNKNOWN |

The five-byte `.wifi-link.state` still says `GOOD` and has mtime `2026-09-03T09:47:02Z`. The
producer touches that state after every real numeric read, so its unchanged mtime establishes zero
real reads in both windows. The fresh `.wifi-link-offline` marker is an honest blind/unreachable
artifact, not Wi-Fi quality coverage. At `2026-09-14T19:38:06Z`, `mesh-wifi-link --edge` refreshed
that marker while returning no quality sample. `mesh-wifi-link --test` returned exit 2 / n/a
(`phone unreachable or no termux-wifi-connectioninfo`); this is not described as a live smoke pass.
The fixture-backed `tests/test-mesh-wifi-link-integration-slice.sh` passed separately.

The outcome history remains incomplete: `.wifi-link-empty.log` is absent, and all 616 rows in
`wifi-link.log` are undated (554 offline diagnostics, 61 quality-change lines, one other line), so
they cannot be split between the bounded windows. The 115 unrecorded 7-day schedule slots are
UNKNOWN; they are not classified as powered off or as successful attempts.

`mesh-sensorium` at 19:32Z read local thermals and audio devices, found no Bluetooth adapter, and
found 0 Wi-Fi APs. `mesh-sense-map --refresh` at 19:33:15Z showed 4/11 nodes reachable and Redmi 10
offline; it listed no Wi-Fi scanner on mesh-home. These probes corroborate the absent vantage but
do not substitute for a phone link reading. After this recheck, `mesh-note3-battery --edge` made a
real Note 3 hardware read (`present=true level=100/100 temperature=28.5°C power=USB status=5
voltage=4307mV`); its 81-byte `~/.mesh/.note3-battery-state` artifact was written at
`2026-09-14T19:39:18Z`. This confirms a fresh real artifact after the decay recheck without claiming
that Wi-Fi link quality recovered. No commit was made.
