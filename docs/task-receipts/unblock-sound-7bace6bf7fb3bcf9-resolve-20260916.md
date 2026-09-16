# Sound capture blocker resolution — 2026-09-16

Task: `task:unblock/sound/7bace6bf7fb3bcf9/resolve`
Parent: `sound-ear-render-20260916/render-fresh-ear`
Owner: `sound`

## Eligibility and current evidence

The resolver was claimed before work with:

```text
mesh-task status unblock/sound/7bace6bf7fb3bcf9
unblock/sound/7bace6bf7fb3bcf9 [active] (1/1)
  1. unblock/sound/7bace6bf7fb3bcf9/resolve [active] owner=sound priority=90 lease=2026-09-16T06:04:42Z
```

The parent task remains explicitly blocked as `external-event` and names the needed
capture and verification edge. The live resolver attempt therefore had a valid target;
it did not manufacture a duplicate or bypass the parent block.

## Fresh live probe

Captured at `2026-09-16T05:37:59Z` UTC.

```text
$ ROOM_NODE=localhost mesh-room-music --capture 18
capture: room node unreachable (localhost)

$ tailscale status --json | jq -r '.Peer[] | [.HostName, (.TailscaleIPs[0] // ""), (.Online|tostring)] | @tsv' | grep -iE 'imo|room|zerov'
imozerov-Default-string	100.125.157.75	false

$ ssh -o StrictHostKeyChecking=no -o ConnectTimeout=6 -o BatchMode=yes imozerov@100.125.157.75 'hostname; command -v pw-record'
ssh: connect to host 100.125.157.75 port 22: Connection timed out

$ nc -vz -w 3 100.125.157.75 22
nc: connect to 100.125.157.75 port 22 timed out: Operation now in progress

$ curl -sS -m 3 -i http://127.0.0.1:8388/
curl: (28) Operation timed out after 3003 milliseconds with 0 bytes received
```

The configured script path is `/home/mesh-home/lte-workstation/scripts/mesh-room-music`;
its capture lane records `ROOM_NODE` as `localhost` from the active environment and
reports the SSH hop as unreachable. The Tailscale peer inventory independently maps the
room identity to `100.125.157.75` and reports it offline. No new capture file was created,
so there is no honest ffprobe/decode result to claim.

## Exact retry packet

This is the irreducible external atom. When the room node is reachable again (Tailscale
peer online and its SSH/pw-record lane responding), run:

```bash
mesh-room-music --capture 18
```

Then verify the newly printed capture path is non-empty and genuine audio, and verify its
corresponding fresh `room-music-params.log` entry; for the parent render, run the requested
ffprobe/decode checks and retain their output beside the render artifact. Retry edge:
`localhost room capture node reachable` (equivalently, the room peer is online and the
capture SSH hop succeeds).

Result: no mesh-internal fix can restore an offline external room node. The resolver is
typed-blocked on `external-event`; exact result tokens intentionally do not claim
`unblock=cleared`, because the capture prerequisite is unsatisfied.
