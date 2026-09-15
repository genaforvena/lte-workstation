# Health warning triage: imac-rozalia SSH reachability

At 04:15:46Z watchdog posted the recurring `imac-rozalia` SSH-unreachable fault for
`100.121.88.110`, with signature `35f22fafd26a` and zero newly suppressed repeats. This is the
same known host reachability problem documented by
[`health-warning-ed23d7b6fc8ee0959c6b-triage-20260914.md`](health-warning-ed23d7b6fc8ee0959c6b-triage-20260914.md).

Fresh read-only state at 04:19Z is mixed: `tailscale status --json` shows the peer `Online=true`
and `Active=true` but gives a zero `LastSeen` sentinel and no current address; text status shows
an active relay through `hel` with `tx 468 rx 0`, without an offline/last-seen marker. This does
not establish SSH reachability. Local load is 28.39/28.78/30.57 on the 16-core host, while the
live health pane already warns that reachability probes are unreliable under high load. I did
not add another SSH or ping probe under that condition.

Disposition: recurring SSH reachability remains unresolved; current Tailscale metadata is
ambiguous and the Mac's physical power/network state is unknown. No alternate LAN fallback is
configured for this host. No substrate or remote-node state was changed. The concrete retry
condition is a later stable load window or independently available local/LAN access, followed
by a fresh SSH check.

Verification: `tailscale status --json` peer fields, `tailscale status` text, `uptime`, the
04:09Z `mesh-dash --once check`, and the prior health-warning receipt above.
