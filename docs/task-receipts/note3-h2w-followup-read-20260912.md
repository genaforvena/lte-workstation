# Note3 h2w follow-up read — 2026-09-12

Health's serial-attributed reach finding was acknowledged to `health` with
`mesh-chat --to health '[ack] ack:eb895a4c5f48be52'` at 2026-09-12T12:32:22Z.

At 2026-09-12T12:33:32Z, discover performed a fresh read pinned to ADB serial
`4d00553d61ab90b7` using:

```sh
adb -s 4d00553d61ab90b7 shell 'getprop ro.serialno; cat /sys/class/switch/h2w/name /sys/class/switch/h2w/state'
```

The command exited 0 and returned:

```text
4d00553d61ab90b7
No Device
0
```

The Note3 switch remains reachable and serial-attributed; this read confirms only the open state.
The required plugged-in `state=1` observation is still missing. No consumer wiring was performed.
Next action: obtain another pinned read while a wired headset is physically connected to the Note3.
