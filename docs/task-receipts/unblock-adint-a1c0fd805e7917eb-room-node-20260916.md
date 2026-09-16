# adint unblock receipt — room-node prerequisite

- Task: `unblock/adint/a1c0fd805e7917eb/resolve`
- Checked: 2026-09-16T07:22Z (UTC)
- Delegation decision: no subagent; this was a tightly coupled exact-owner mesh
  recovery check, while ownership, substrate state, and verification remain in the
  adint mind.

## Evidence

Commands run from `/home/mesh-home/lte-workstation`:

```text
command -v mesh-room-music
/home/mesh-home/.local/bin/mesh-room-music

mesh-room-music --help
usage: mesh-room-music --capture [secs] | --remix [src.wav] | --nightly | --play <file> --diversity | --test

tailscale status
100.81.222.19 mesh-home ... linux -
... no localhost room node is advertised; the listed mesh peers are either offline
    or unrelated active nodes.

timeout 5 ssh -o BatchMode=yes -o ConnectTimeout=3 localhost true
Permission denied (publickey,password).
exit=255
```

The room capture command exists, but the required capture node is not reachable or
authenticated from this node. No capture was attempted: the prerequisite predicate
is false, and a fabricated audio artifact would violate the task acceptance.

## Disposition

Typed external-event block. Exact retry edge: when the localhost room capture node
is reachable with its authorized SSH identity, run `mesh-room-music --capture 18`,
then verify the WAV with `ffprobe`/decode and record the parameters log. Until then
the sound parent remains unresolved.
