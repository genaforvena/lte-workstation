# Knowledge upstream refresh — 2026-09-12

The requested refresh of `/home/mesh-home/.mesh/knowledge` against its configured
`default-string/main` could not complete because the configured SSH peer is unreachable.

- Repository state before and after the attempt: clean `master` at `352815ba16d58b07c38254404587bbd48d179b9b`.
- Configured fetch URL: `imozerov@100.125.157.75:knowledge.git`; its tracking ref remained `60ff6859155671a7080f1f7113662c2d59f4d387`.
- Bounded SSH probe (`ConnectTimeout=5`, 12-second outer timeout) failed connecting to `100.125.157.75:22` with `Connection timed out`.
- `tailscale status` reports `imozerov-default-string` offline, last seen 59 days ago, with no received traffic; a bounded `tailscale ping` got no reply.
- Bounded fetch (`timeout -k 2 22`, SSH keepalive and 5-second connect timeout) failed with the same TCP connection timeout. Authentication and Git protocol negotiation were not reached; no tracking ref changed.
- Cached graph comparison: `master` is 86 commits ahead and 0 behind `default-string/main`; the configured remote tip is an ancestor of `HEAD`. `origin/main` is exactly `HEAD` (0/0), but this separate mirror does not establish freshness of `default-string/main`.

No push, merge, or private-repository mutation was performed. Freshness remains unknown beyond the cached ref. Once `imozerov-default-string` is online, rerun the bounded fetch against `default-string` and recalculate the graph comparison.
