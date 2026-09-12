# Note3 live health reconciliation — 2026-09-12

Task: `note3-live-health-reconciliation-20260912/reconcile-live-note3` (owner `health`).

## Finding

The prior `Note3 UNKNOWN` verdict was accurate for the earlier observation but stale by the
11:24–11:27Z sensor messages. The sensor read path and ADB command/control path are separate
claims; both now have fresh evidence. At 11:41:56–11:42:00Z all five real-read sensor commands
returned current structured readings, and `mesh-adb-transport` independently completed an ADB
serial round trip plus device uptime read. Thus Note3 is reachable and commandable at probe time.
This does not establish uninterrupted USB/ADB availability: `~/.mesh/adb-transport.log` records
`na not-attached` every five minutes from 10:40 through 11:20, then `reached` at 11:25, 11:30,
11:35, 11:40 and the manual probes at 11:41:20 and 11:41:56. The USB fault watch reported two
disconnects at 11:25:06 (chat line 55966); later successful round trips establish recovery.

No configuration was changed. The stale UNKNOWN health roll-call was corrected with a fresh
health roll-call at `~/.mesh/chat.log:56069` (2026-09-12T11:43:11Z). Other health gaps remain:
`mesh-health` still reports LAN/peer visibility gaps and only the local node plus phaedra PASS.

## Source messages

Physical lines from `/home/mesh-home/.mesh/chat.log`:

```text
55740 2026-09-12T10:38:36Z health@mesh-home [done] health-warning/747d421e2b2009967e9a/triage: Historical discovery was healthy; current Note3 state is UNKNOWN because ADB has no attached device. Recorded the live visibility gap; no configuration changed.
55795 2026-09-12T10:51:21Z health@mesh-home [idle] health: queue empty; pane 15LIVE/0DARK (UVC visible), PATH DEGRADED with unreliable probes; doctor cache 3F/34W 76m old; egress/exit-node SPOF frozen; router and Note3 unknown.
55955 2026-09-12T11:24:02Z note3-motion@mesh-home [note3-motion] STILL (delta=194 vs prior read)
55963 2026-09-12T11:25:01Z note3-battery@mesh-home [note3-battery] present=true level=95/100 temperature=30.5°C power=USB status=2 voltage=4013mV serial=4d00553d61ab90b7
55964 2026-09-12T11:25:03Z note3-orient@mesh-home [note3-orient] FACE_UP (was UPRIGHT; pitch=-0.38764 roll=-0.618371 — departed rest(FACE_DOWN))
55966 2026-09-12T11:25:06Z hw-fault-watch@mesh-home [hw-fault] usb: usb 1-3: USB disconnect, device number 6 (x2 new) — peripheral fault on mesh-home, full lines in ~/.mesh/hw-fault.log
55969 2026-09-12T11:26:02Z note3-mag@mesh-home [note3-mag] DISTURBED (delta=73.3 uT vs prior read)
55972 2026-09-12T11:27:05Z note3-light-raw@mesh-home [note3-light-raw] CHANGED (raw=3467.58 lux=1.7166 delta=50.8%)
56069 2026-09-12T11:43:11Z health@mesh-home [fyi] roll-call health: Note3 no longer UNKNOWN: 11:41:56–11:42Z real reads succeeded (battery USB 96%, motion STILL, orientation TILTED, mag STABLE, light STABLE); ADB serial 4d00553d61ab90b7 independently answered getprop/uptime. USB disconnect x2 at 11:25:06 was followed by successful transport probes at 11:30, 11:35, 11:40 and now. mesh-health: mesh-home and phaedra PASS; LAN visibility and tailscale0/phaedra egress SPOF remain known gaps. No config changed.
```

## Current probe outputs

Commands were run from `/home/mesh-home/lte-workstation` on 2026-09-12. The `--json` sensor
calls are real device reads (not fixture tests). All returned exit status 0.

`rtk proxy mesh-health` (11:41:56Z):

```text
=== mesh-health 2026-09-12T11:41:56Z ===
PASS  mesh-home                        100.81.222.19 (self)
OFFLINE GL-MT3000                        100.105.241.84 (tailnet: last-seen 85d ago, active=True)
OFFLINE Redmi 10                         100.103.99.16 (tailnet: last-seen 9d ago, active=True)
OFFLINE ilya                             100.107.198.111 (tailnet: last-seen 23d ago, active=False)
SKIP  imac-rozalia                     100.121.88.110 — SSH authentication refused
OFFLINE imozerov-Default-string          100.125.157.75 (tailnet: last-seen 59d ago, active=True)
OFFLINE imozerov-IdeaPad-3-15IIL05       100.73.170.56 (tailnet: last-seen 13d ago, active=True)
PASS  phaedra                          100.94.116.17
OFFLINE rip                              100.116.125.102 (tailnet: last-seen 9d ago, active=False)
```

ADB enumeration and control-liveness probe:

```text
$ rtk proxy adb devices -l
List of devices attached
4d00553d61ab90b7       device usb:1-3 product:ha3gxx model:SM_N900 device:ha3g transport_id:2

$ rtk proxy mesh-adb-transport
reached device_uptime_s=1211.65

~/.mesh/.note3-adb-transport:
REACHED 2026-09-12T11:41:56Z serial=4d00553d61ab90b7 ro.serialno=4d00553d61ab90b7 device_uptime_s=1211.65 node=local

~/.mesh/adb-transport.log:
2026-09-12T11:41:56Z serial=4d00553d61ab90b7 node=local verdict=reached device_uptime_s=1211.65
```

Fresh real-read sensor outputs:

```text
$ rtk proxy mesh-note3-battery --json
{"serial":"4d00553d61ab90b7","present":true,"level":96,"scale":100,"temperature_c":29.5,"power_source":"USB","status":2,"voltage_mv":4338,"ts":"2026-09-12T11:41:56Z"}

$ rtk proxy mesh-note3-motion --json
{"verdict":"STILL","x":-192,"y":111,"z":17359,"delta":"88","ts":"2026-09-12T11:41:56Z"}

$ rtk proxy mesh-note3-orient --json
{"verdict":"TILTED","class":"TILTED","azimuth":171.741,"pitch":-11.569,"roll":-86.0698,"rest":"FACE_DOWN","departed":"DEPARTED","ts":"2026-09-12T11:41:57Z"}

$ rtk proxy mesh-note3-mag --json
{"verdict":"STABLE","x":-4.2,"y":25.62,"z":68.16,"delta":"0.4","ts":"2026-09-12T11:41:57Z"}

$ rtk proxy mesh-note3-light-raw --json
{"verdict":"STABLE","raw":4478.8,"lux":16.34,"delta_pct":"0.8","age_s":"-3.8","ts":"2026-09-12T11:42:00Z"}
```

The probe-time classifications differ from the earlier edge messages (FACE_UP, DISTURBED,
CHANGED), which describe earlier samples. They are not contradictions: the sensors continued to
change between those samples and the current reads. The light read is timestamped 11:42:00Z with
`age_s=-3.8`, so its sample timestamp is ahead of the reader clock by 3.8 seconds; the reported
value is real but the slight clock/sample skew should be kept in mind for age interpretation.

## Decision

The report that Note3 was UNKNOWN is stale, not evidence that its sensor stream was dead. Current
sensor reads succeeded and ADB control is also currently reachable. The repeated earlier
`not-attached` transport results and the USB disconnect event show intermittent transport
availability, so this reconciliation does not claim uninterrupted reachability. No repair or
configuration change is justified by the current evidence.
