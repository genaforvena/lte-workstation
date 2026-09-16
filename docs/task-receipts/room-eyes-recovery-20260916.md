# Room EYES/WAKE recovery — 2026-09-16

## Before

Bounded live probes at 14:16:11Z:

    timeout 30s mesh-imac-cam-watch --test       exit 0
    timeout 20s mesh-room-sense-loss --status    exit 0
    systemctl --user is-enabled ...              exit 1 (disabled)
    systemctl --user is-active ...               exit 3 (inactive)

The camera test itself ran one real cycle and returned `state=SEEING`, but room-sense-loss
reported `cam DEAD`, `wake DEAD`, and stored `LOST` for 8h.

## Recovery and verification

Ran the mesh-owned recovery:

    timeout 30s systemctl --user enable --now mesh-imac-cam-watch.service

It returned exit 0 and created the user-unit wants symlink. After a 3-second settle:

    systemctl --user is-enabled mesh-imac-cam-watch.service  -> enabled (exit 0)
    systemctl --user is-active mesh-imac-cam-watch.service   -> active (exit 0)
    timeout 30s mesh-imac-cam-watch --test                   -> exit 0, real cycle state=SEEING

Fresh producer artifacts observed at 14:16:33Z:

    ~/.mesh/imac-cam-watch.log       1943164 bytes, mtime 14:16:22Z
    ~/.mesh/cam/imac-cam-settle.log  1091477 bytes, mtime 14:16:33Z
    ~/.mesh/.imac-cam-last-motion    11 bytes, mtime 14:16:27Z
    ~/.mesh/.imac-cam-last-classify  11 bytes, mtime 14:16:27Z

## Residual state

`mesh-room-sense-loss --status` at 14:16:33Z still showed stored `LOST` for cam and wake,
despite the fresh producer artifacts. This is a remaining consumer/state propagation issue,
not evidence that the camera service failed to recover. No source or substrate routing change
was made. Next retry/action: run the room-loss status after its next state-refresh cadence;
if it remains `LOST`, inspect the wake/state writer rather than re-enabling the already-active
camera unit.
