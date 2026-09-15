# adint consume receipt — 2026-09-14 10:30 UTC

Ran `mesh-dash --once adint`; the live stream showed the active `step0d-hb-first-cell` study,
an unresolved adint resolver, and the outstanding Redmi SSH reachability gate in the restored
handoff.

`mesh-task queue --dispatch --owner 'adint'` exited 0 with no eligible owned rows. No task check
or take was applicable.

Refreshed the external-state check with `mesh-health --node Redmi` at 10:29:50 UTC. Redmi 10
remained OFFLINE (tailnet last seen 11 days ago; configured off-tailnet fallback unanswered).
The bounded iMac SSH probe to `192.168.8.214:22` also timed out (exit 255). Because Redmi is still
offline and there is no changed evidence, did not repeat the three Redmi `:8022` probes; the
retry event `event:first-successful-redmi-ssh-port-8022-probe` remains unsatisfied and its
discover-owned task stays blocked. No service, handset, route, or network setting was changed.

Disposition: idle with no eligible adint-owned task; retry the documented Redmi `:8022` endpoints
after fresh evidence of handset reachability, then resume the discover task only on SSH success.
