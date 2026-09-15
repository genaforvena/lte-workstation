# Health warning triage: iMac SSH reachability remains unverified

Task: `health-warning/29cc9b04bf711f7d05f9/triage`

The 09:01:53Z watchdog line is a chronic-suppression roll-up for signature
`35f22fafd26a` (`gap=17408s`, `win=351600s`, `n=27`, `suppressed=2`), following the
08:54Z recovery recorded in
[`health-warning-2ca0e1c7ec6377531951-triage-recovery-20260914.md`](health-warning-2ca0e1c7ec6377531951-triage-recovery-20260914.md).
It is a new recurrence after that recovery, not evidence that the earlier recovery measurement
was false.

Repository and ledger review found the exact prior path resolver
`unblock/health/807797d851d3d242/resolve` and both recent iMac resolver chains complete. The
previous health warning is complete too; none is an active prerequisite for this recurrence.
There is still no independent LAN fallback configured for `100.121.88.110` in
`~/.mesh/nodes`.

Read-only live evidence on 2026-09-14:

- The `mesh-dash --once check` frame at 09:06:29Z reported `LOCAL LOAD HIGH — reachability
  probe UNRELIABLE`, local load `79.48/16`, and the fleet header `10 nodes: 3 ssh · 0 lan · 7
  down`. The command emitted that frame but did not exit within 30 seconds; it was stopped after
  the frame appeared. No second pane probe was run.
- At 09:09:22Z, `uptime` reported load averages `31.10/43.81/40.45` on 16 CPUs.
- Tailscale JSON at about 09:09Z reports the iMac `Online=true`, `Active=true`, a current
  `LastHandshake=2026-09-14T09:08:14.940808414Z`, address `100.121.88.110`, but a zero
  `LastSeen` sentinel and empty `CurAddr`. Text status shows an active `hel` relay and traffic
  counters (`tx 13998600 rx 16041016`). This supports a live overlay peer path but does not
  verify SSH.

Disposition: SSH reachability and the cause of the recurrence remain unknown. The pane explicitly
marks reachability probes unreliable under load, so I did not add a ping or SSH probe; the recent
Tailscale handshake is an honest substitute for overlay-path liveness only. No substrate or remote
node state changed. The exact retry condition is a later check-pane frame without the
reachability-unreliable warning (or a newly available independent LAN/owner path), followed by a
bounded Tailscale ping and read-only SSH using the already documented temporary known-hosts method.

Verification sources: one-shot pane frame, `uptime`, filtered `tailscale status --json`, text
`tailscale status`, prior recovery receipt, completed resolver ledger entries, and
`~/.mesh/nodes`. No active exact prerequisite was found, so this step is being typed-blocked on
fresh reliable SSH-path evidence; `mesh-task block` will register/link the narrow resolver.
