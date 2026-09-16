# Live mesh capability census checkpoint — 2026-09-16T14:28Z

This is a bounded continuation artifact for the literature-capability frontier. It records fresh
reachability and an attached-phone read; it does not promote declarations to verified capabilities.

## Fresh observations

From `mesh-home`, `tailscale status --json` reported these peers online:

| node | address | state | current evidence |
|---|---|---|---|
| Redmi 10 | 100.103.99.16 | online | direct Termux/SSH evidence in `docs/mesh-capability-census-live-20260916-1410.md` |
| imac-rozalia | 100.121.88.110 | online | direct SSH/system-profiler evidence in the 14:10 census extension |
| phaedra | 100.94.116.17 | online | direct SSH/service evidence in the 14:10 census extension |
| WIN-Q6GL9FIR3QI | 100.101.237.87 | online | reachability only; credential/tool surface is unknown and therefore unverified |

Offline peers were also returned for GL-MT3000, ilya, IdeaPad, default-string, rip, and two
unnamed mobile/tablet entries. They remain in scope but are not treated as currently reachable.

The attached USB device remained present:

```text
adb devices -l
4d00553d61ab90b7 device usb:1-3 product:ha3gxx model:SM_N900 device:ha3g transport_id:5
```

Bounded ADB read:

```text
adb shell getprop ro.product.model
SM-N900
```

The attempted feature formatting pipeline failed on the phone because its shell lacks `printf`,
`tr`, and `cut`; that is a tool-environment limitation, not evidence that the features are absent.
The earlier complete Note3 feature/sensor capture remains the authoritative capability artifact:
`docs/mesh-capability-census-20260916.md`.

## Consequence for the frontier

The census now has a named, reachable Windows node that is explicitly `reachable / capability
unknown`, preventing silent omission. The next safe census action is credential-free surface
discovery or a steward-owned Windows probe; do not infer camera, audio, display, or compute
capabilities from Tailscale reachability alone.

## Ledger note

The canonical frontier step `literature-capability-frontier-20260916/census-and-evidence` remains
open. Three bounded `mesh-task take` attempts have emitted board `[taking]` lines but no structured
active ledger revision; the current `mesh-task take` process is still live under sustained
coordinator contention. This artifact is therefore progress evidence, not a false task completion.

## Fresh Note3 environmental sample — 2026-09-16T14:38Z

Command: `MESH_BARO_ADB_NODE=local scripts/mesh-baro --json`

```json
{"hpa":992.21,"trend":"STABLE","alt_delta_m":-3.0,"baseline_hpa":991.88,"prev_hpa":992.23,"temp_c":23.5,"humidity_pct":49.2,"ts":"2026-09-16T14:38:12Z"}
```

Exit status was `0`. This is one fresh end-to-end Note3 `sensorcat` reading through the existing
mesh-baro consumer: pressure, ambient temperature, and relative humidity all parsed. It upgrades
those fields from merely declared/wired to freshly verified at this timestamp, while leaving the
unrelated thermalservice probe correctly rejected as unavailable. The reading is a concrete input
for the literature-backed event-triggered multimodal context proposal; no new capability claim or
new knowledge file is made here.

## Fresh iMac media-state sample — 2026-09-16T14:40:58Z

Command: `MESH_IMAC_HOST=ilya@100.121.88.110 MESH_IMAC_MEDIA_TIMEOUT=12 scripts/mesh-imac-media --json`

```json
{"media":"NONE","user_active":1,"by":"-","ts":"2026-09-16T14:40:58Z"}
```

Exit status was `0`. The remote `pmset -g assertions` path produced a parseable playback/activity
record without capturing content or invoking speech. This verifies the iMac media-state sense over
the Tailscale SSH path and preserves the distinct camera/microphone organs as unverified.

## Fresh mesh-home capability-card sample — 2026-09-16T14:46:01Z

Command: `mesh-card --refresh` (exit `0`). The live card reported:

```text
node=mesh-home tailscale=100.81.222.19 lan=192.168.8.197
default-egress=enp42s0 public-ip=38.49.216.141 exit-node=none ip-forwarding=on wireguard-ifaces=none
services=mesh-imac-cam-watch,mesh-liveness-loop,mesh-overhear,mesh-phaedra-proxy,
         mesh-reticulum,mesh-textin,mesh-voice-rx
invariant-check=OK power=MAINS disk=31% mem=46% load=95.23/16 temp=73C upstream=ok
identity-coherence=CONFLICTED (27)
capabilities=compute:primary; minds:claude,opencode,codex,ollama;
             senses:camera,display-link,irq,light,link-flap,mic,uvc-metadata;
             actuators:dlna-tv,docker-compute,imac-notify,imac-say,shadowsocks,speaker,tv,volume;
             connectivity=shadowsocks
```

This is fresh mesh-home evidence, including the active service set and persistent 27-conflict
identity issue. The card confirms clean default egress and `invariant-check=OK`; it does not
promote declarations beyond the separately verified artifacts in this census.

## Fresh Redmi reachability/admission-control check — 2026-09-16T14:47Z

Command: `timeout 15s ssh -o BatchMode=yes -o ConnectTimeout=6 -p 8022 u0_a380@100.103.99.16 termux-battery-status`

```text
ssh: connect to host 100.103.99.16 port 8022: Connection refused
exit=255
```

This is a useful state transition: Tailscale still lists Redmi online, but its Termux SSH service
is currently refusing connections. The previously verified battery/charging sample is therefore
stale for current consumers; the event-triggered collector must render Redmi battery and sensor
coverage as `UNKNOWN` until the exact SSH retry succeeds. Online status alone is not capability
availability.

## Fresh full census — 2026-09-16T15:19:32Z

Command: `timeout -k 5 120s scripts/mesh-census --json --no-log` (exit `0`). This is a
credential-free, no-side-effect census of the currently reachable tagged nodes. The machine
readout reported surface totals `minds=6`, `senses=11`, `actuators=12`, `connectivity=1`,
`compute=3`, with three reachable/verified invariant rows: `mesh-home`, `imac-rozalia`, and
`phaedra`. `mesh-home` and `phaedra` returned command-level capability lists; `imac-rozalia`
returned reachability, internet, invariant, and disk evidence but no parsed mind/sense/actuator
list. Redmi was Tailscale-online but not reached by the probe, so its capability fields remain
UNKNOWN; five other peers were offline and likewise remain UNKNOWN. This preserves the distinction
between reachable, declared, verified, and unavailable rather than inferring capabilities.

Delegation record: worker `audioflinger-evidence-review` was launched for an independent read-only
acceptance review; its inspected result was that the AudioFlinger receipts do not contain the
required all-node capability matrix. Worker event evidence is in `/tmp/csd-workers/homes/` and the
two personally inspected source receipts are `docs/task-receipts/discover-note3-audioflinger-20260916.md`
and `docs/task-receipts/discover-note3-audioflinger-handoff-20260916.md`.

Next action: extend this matrix with the missing physical-device credential/data-store and
existing-but-unwired-tool fields for each reachable node, preserving UNKNOWN where access is absent;
then run the literature synthesis step. The current full census is progress evidence, not completion.

## Credential, data-store, and unwired-tool extension — 2026-09-16T15:34Z

This extension is a bounded inventory, not an authorization to consume private data or fire
actuators. `command -v`, directory existence, and a successful SSH/ADB transport prove only the
named surface; they do not prove that a consumer is wired or that a credential grants every
operation.

| node | physical-device credential/data-store surface | existing but not represented by the generic census | state and evidence |
|---|---|---|---|
| mesh-home | Local operator account `mesh-home`; mesh-owned stores include `~/.mesh/gmail-note3/gmail.db` plus WAL/SHM, job-board/log stores, and the local knowledge corpus. The Note3 is physically attached and its rooted ADB lane is the credential for Gmail/phone reads; no password is copied into this artifact. | `mesh-tcp-metrics`, `mesh-mlme-tap`, and `mesh-drop-reason` are installed executables; they are specialized network/802.11/drop diagnostics and are not emitted as the 11 generic `mesh-census` senses. `mesh-gmail-note3`, `mesh-job-mail`, and `mesh-note3-say` are also present consumer/actuator paths. | **verified / wired or callable**, with per-consumer predicates still separate. Evidence: `adb devices -l` returned serial `4d00553d61ab90b7` as `device`; `command -v` returned `/home/mesh-home/.local/bin/...` for all named tools; filesystem listing found `gmail-note3/gmail.db`, `job-board.tsv`, and `knowledge/`. |
| Note3 / SM-N900 | Physical USB/rooted-ADB lane; `mesh-gmail-note3` reads the sliding Gmail cache and `mesh-note3-say` is the phone speaker delivery path. SMS/contacts are physically available through the same device lane, but freshness depends on the phone and must be re-read. | Declared/installed Android surfaces not proven in this pass include consumer IR transmit, NFC/HCE, telephony call/SMS actuation, and several Termux API verbs; the full declaration list is in `docs/mesh-capability-census-20260916.md`. | **reachable + attached, mixed verified/UNKNOWN**. Fresh transport evidence is the ADB row above and `getprop ro.product.model` → `SM-N900`; no destructive or private-content read was performed in this continuation. |
| imac-rozalia | SSH credential lane `ilya@100.121.88.110` succeeded. The remote account has Mail and Messages directories, but their contents were not read. | `/usr/bin/say` is a callable speech actuator and `/usr/sbin/system_profiler` is a hardware-discovery tool; camera/mic capture, notifications, and local data consumers are not established by directory/command presence. | **reachable; say verified; Mail/Messages presence verified; content and additional I/O UNKNOWN**. Fresh command: `hostname; command -v say; command -v system_profiler; test -d "$HOME/Library/Mail"; test -d "$HOME/Library/Messages"` over bounded SSH, exit `0`, output `iMac-Rozalia.lan`, both paths, and both directories present. |
| phaedra | SSH credential lane `root@100.94.116.17` succeeded. `mesh-loc-collector.service` is active; its private inputs/retention and any operator credential stores were not opened. | `mesh-loc-collector.service` and the fallback port-80 service are node roles absent from the generic sense/actuator vocabulary; `docker` was not found in the bounded remote probe, so container compute remains UNKNOWN. | **reachable; location service active; data retention and extra compute UNKNOWN**. Fresh command over bounded SSH returned hostname `phaedra`, `active`, no `docker` path, exit `0`. |
| Redmi 10 | Physical Android/Termux credential lane is known from earlier successful readings, but it is not currently usable. | Termux API, SMS, telephony, camera, microphone, sensors, and notification paths cannot be recounted while the SSH service refuses the connection. | **Tailscale online but capability UNKNOWN for this run**. Fresh `ssh -p 8022 ... termux-battery-status` returned `Connection refused`, exit `255`; this is the exact retry edge: rerun the bounded Termux probe after port 8022 accepts a connection. |
| WIN-Q6GL9FIR3QI | No credential or physical-device lane discovered. | Windows hardware, data stores, and local tools are not probed. | **reachable by Tailscale only / UNKNOWN**; retain as an explicit census row rather than infer capabilities from online status. |

### Disposition

The generic census is intentionally narrower than the frontier inventory. The specialized tools
above are **candidate existing-but-unwired or separately wired surfaces**, not new verified organs;
their owning stewards must inspect callers before wiring. Redmi and Windows remain explicit UNKNOWN
rows. No prerequisite block was found for this step: the artifact was extended using local files and
credential-free/metadata-only probes. The next exact action is to run the literature synthesis step,
with the census rows above as its capability boundary.
