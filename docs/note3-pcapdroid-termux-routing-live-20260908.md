# Note3 PCAPdroid / Termux SSH / routing live evidence — 2026-09-08

Owner: `tg` · scope: Note3 PCAPdroid CSV source, Redmi Termux SSH identity/reachability,
and routing. This is a fresh live read, not a restatement of the 2026-09-07 discovery audit.
No files on the phones or routing tables were changed.

## Artifact

### Note3 ADB identity and PCAPdroid source

ADB enumerated one live USB device:

```text
4d00553d61ab90b7 device usb:1-3 product:ha3gxx model:SM_N900 device:ha3g transport_id:1
```

Direct reads from that serial returned:

```text
ro.product.model = SM-N900
ro.build.version.release = 5.0
pm list packages | grep -i pcap = <no output>
ls -l /sdcard =
lrwxrwxrwx root root 2026-09-06 21:47 sdcard -> /storage/emulated/legacy
find /sdcard -type f | grep -i -E 'pcapdroid|\\.csv$|\\.pcap' = <no output>
ls -l /sdcard/PCAPdroid /sdcard/Documents = both paths absent
```

Verdict: **PCAPdroid CSV is absent from the live Note3 surface**. The four local
`~/.mesh/inbox/PCAPdroid_*.csv` files remain pre-existing inbox artifacts and are not
reclassified as Note3-canonical:

```text
6302   /home/mesh-home/.mesh/inbox/PCAPdroid_15_Aug_15_52_08-AgAD0qAAAnWWCUg.csv
133735 /home/mesh-home/.mesh/inbox/PCAPdroid_15_Aug_16_26_33-AgADTaEAAnWWCUg.csv
242051 /home/mesh-home/.mesh/inbox/PCAPdroid_15_Aug_16_46_53-AgADr6EAAnWWCUg.csv
449426 /home/mesh-home/.mesh/inbox/PCAPdroid_15_Aug_17_39_56-AgADX6IAAnWWCUg.csv
```

### Termux SSH identity and reachability

The configured canonical identity is `Redmi:u0_a380@100.103.99.16`, port `8022`.
The live Tailscale peer read was:

```text
HostName: Redmi 10
TailscaleIPs: 100.103.99.16, fd7a:115c:a1e0::133b:6310
Online: false
```

Independent SSH attempts as `u0_a380` timed out on every configured candidate:

```text
100.103.99.16:8022  Connection timed out (rc=255)
192.168.8.203:8022  Connection timed out (rc=255)
192.168.8.146:8022  Connection timed out (rc=255)
```

No `whoami` or phone model was obtained. The Note3 ADB identity above must not be
used as the Redmi/Termux identity.

### Routing

Fresh FIB lookups:

```text
ip route get 100.103.99.16
100.103.99.16 dev tailscale0 table 52 src 100.81.222.19 uid 1000

ip route get 192.168.8.1
192.168.8.1 via 100.74.0.1 dev enp42s0 src 100.74.81.205 uid 1000
```

The Tailscale route is present; the peer is offline. No route change was made.

## Verdict / next action

**BLOCKED, not closed.** Canonicalization cannot proceed from this node because both
required source facts are still missing: a real Note3 PCAPdroid CSV and a live Redmi
Termux SSH read. Restore the Redmi `sshd` or provide a live SSH address, then place one
complete PCAPdroid CSV on the Note3/source lane and repeat this evidence run.
