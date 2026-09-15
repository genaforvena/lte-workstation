# Health-warning triage: `health-warning/8d78cf2e639ed49f3ab0`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/8d78cf2e639ed49f3ab0/triage`

## Warning

The board warning at 2026-09-11T18:04:42Z reported:

```text
[organ-down] mesh-home: declared organ DARK: uvc-metadata — probe fails,
no sudo-free fix. Check hardware/permits or mesh-card --refresh (drift?).
```

## Live evidence

`mesh-card --refresh` at 2026-09-11T20:41:58Z still declares `uvc-metadata` as a
local sense and reports both `/dev/video0` and `/dev/video1` with `root:video`
permissions. `mesh-organ-keepalive --status` reports:

```text
mesh-home:uvc-metadata — LIVE
```

The real `mesh-uvc-metadata --test` probe against `/dev/video1` produced five
transient 2-second timeouts, then succeeded with a 5,434-byte one-buffer read.
The resulting live artifact is non-empty:

```text
path: /home/mesh-home/.mesh/uvc-metadata/latest.bin
size: 1914 bytes
sha256: 86c1ead4a04fd6a02c88c20107cea1acbdd32be88d6761af204acc950afd5380
```

## Disposition

The organ is present and currently live; the warning identifies intermittent
startup/read latency rather than a persistent absent device or permission fault.
No sudo-free remedy is available or warranted, and no substrate or source change
was made. The task is complete with this live-read artifact.
