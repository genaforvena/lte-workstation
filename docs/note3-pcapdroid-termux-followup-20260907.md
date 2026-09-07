# Note3 PCAPdroid / Redmi Termux follow-up — 2026-09-07

This follow-up records the owner-start attempt for the witness task. Existing files and routing
were left unchanged.

## Live reads

- Owner receipt and witness acknowledgement were posted at `2026-09-07T20:22:33Z`.
- USB ADB serial `4d00553d61ab90b7` answered as `SM-N900`, Android `5.0`.
- `adb -s 4d00553d61ab90b7 shell pm list packages` returned no package matching `pcap` or
  `pcapdroid`.
- A public-storage scan of `/sdcard` and `/storage/emulated/0` found no `.csv`, `.pcap`, or
  `.pcapng` export. `/storage/emulated/0` is absent on this Android 5.0 device.
- The four existing `~/.mesh/inbox/PCAPdroid*.csv` files remain untouched. They are pre-existing
  inbox artifacts and cannot be verified as a Note3 read from this ADB session.
- Redmi candidates `100.103.99.16:8022`, `192.168.8.203:8022`, and `192.168.8.146:8022` all
  timed out. `mesh-body-backup --where` classified the body as `NA off-lan` (exit 2).
- Tailscale reports `redmi-10` / `100.103.99.16` `offline`, last seen 4d ago.
- The route remains present and unchanged: `ip route get 100.103.99.16` resolves via
  `tailscale0`, table 52, source `100.81.222.19`.
- `mesh-phone-ip` returned its stale last-good address after explicitly refusing the unbound ADB
  fallback; this is not live reachability evidence and is not counted as an SSH success.

## Verdict

**BLOCKED — no complete Note3-sourced PCAPdroid CSV was obtained, and Redmi Termux sshd could not
be restored remotely because the body is off-lan/off-tailnet.** The prerequisite is a physical
handset wake/unlock plus PCAPdroid export on Note3; after that, repeat the ADB storage scan and
`ssh -p 8022 u0_a380@100.103.99.16 whoami`, then verify the CSV against
`docs/note3-pcapdroid-termux-routing-audit-20260907.md`.
