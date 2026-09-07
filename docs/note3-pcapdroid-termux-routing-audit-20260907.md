# Note3 PCAPdroid / Termux SSH / routing audit — 2026-09-07

Scope is deliberately limited to the operator correction: PCAPdroid CSV source and
availability, Termux SSH reachability and identity label, and routing. No files were
moved, copied, overwritten, or deleted.

## Measurements

### PCAPdroid CSV on Note3

The USB ADB transport `4d00553d61ab90b7` answered as `SM-N900`, Android `5.0`,
serial `4d00553d61ab90b7`. `adb shell pm list packages` returned no package matching
`pcap`; public-storage scans found no `PCAPdroid` path, `.csv`, or pcap export. The
Note3 public-storage root listing showed no `Documents` or `PCAPdroid` directory.

Verdict: **BLOCKED / absent on the live Note3 surface**. The only PCAPdroid CSVs
found locally are pre-existing inbox artifacts, not a Note3 read:

```text
~/.mesh/inbox/PCAPdroid_15_Aug_17_39_56-AgADX6IAAnWWCUg.csv 449426 bytes
~/.mesh/inbox/PCAPdroid_15_Aug_16_26_33-AgADTaEAAnWWCUg.csv 133735 bytes
~/.mesh/inbox/PCAPdroid_15_Aug_16_46_53-AgADr6EAAnWWCUg.csv 242051 bytes
~/.mesh/inbox/PCAPdroid_15_Aug_15_52_08-AgAD0qAAAnWWCUg.csv 6302 bytes
```

Those existing files were left untouched and are not reclassified as Note3-canonical.

### Termux SSH identity and reachability

The node registry's correct label is `Redmi`, with user `u0_a380`:

```text
MESH_NODES ... Redmi:u0_a380@100.103.99.16 ...
PHONE_USER=u0_a380
```

Live SSH probes as `u0_a380` on port 8022 timed out for all configured candidates:

```text
100.103.99.16:8022  timeout
192.168.8.203:8022   timeout
192.168.8.146:8022   timeout
```

No `whoami` or device identity was obtained, so Termux SSH is **UNREACHABLE in this
sample**. The Note3 must not be used as the Redmi/Termux identity: its live ADB
serial is separately `4d00553d61ab90b7`.

### Routing

The live FIB sends the Tailscale peer address through `tailscale0`:

```text
ip route get 100.103.99.16
100.103.99.16 dev tailscale0 table 52 src 100.81.222.19 uid 1000
```

The route is present, but the current Tailscale peer row is `Redmi 10` /
`100.103.99.16`, `online:false`; this explains the SSH timeout without changing
routing. LAN candidates are not reached through the Tailscale table because the
current host route lookup for `192.168.8.1` resolves via the default gateway
`100.74.0.1` on `enp42s0`. No routing change was made.

## Required next action

The steward/operator must restore the Redmi Termux sshd or provide a live SSH address,
then place one complete PCAPdroid CSV on the Note3/source lane. Until both are real
reads, canonicalization remains blocked. Existing mesh artifacts and inbox files remain
where they are.
