# Redmi Termux SSH restore attempt — 2026-09-10

Task receipt: `ack:c4f5582210e58595` sent to `discover` at `2026-09-10T20:11:12Z`.

The Redmi body could not be restored from this node. All three known SSH paths to the registered
Termux endpoint `u0_a380@*:8022` timed out:

- Tailscale `100.103.99.16` — timeout; Tailscale row `Online=false`, `LastSeen=2026-09-03T09:53:36Z`,
  no `CurAddr`.
- LAN `192.168.8.203` — timeout.
- LAN `192.168.8.146` — timeout.

`tailscale ping 100.103.99.16` also timed out. The canonical Redmi sensor probe
`mesh-body-motion --json` returned exit `2` and `phone unreachable — no body-motion read (not a
state, n/a)`. No fresh Redmi sensor artifact was published. The sole attached ADB device is a
Note 3 (`SM-N900`), so it was deliberately not substituted or labeled as Redmi.

This is an honest unreachable state, not an SSH-daemon diagnosis: the phone does not answer either
TCP or Tailscale control from this node. Restoring Termux requires the Redmi to be awake/on-network
and Termux:Boot/sshd to be started (or physical access to launch it). Once reachable, rerun:

```sh
ssh -p 8022 u0_a380@100.103.99.16 'termux-sensor -s bma420,ORIENTATION,STEP_COUNTER,LINEARACCEL,GYROSCOPE,tmd2755_l,tmd2755_p -n 1'
mesh-body-motion --json
```
