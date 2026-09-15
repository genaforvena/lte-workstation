# Health warning triage: b28f0bbc54d94c13c7ea

- Task: `health-warning/b28f0bbc54d94c13c7ea/triage`
- Alert: `2026-09-15T10:02:33Z watchdog@mesh-home [health-fail] mesh-home — ? (self) — no internet`
- Signature: `b9362527082f`, `recurrence-outside-window`, `gap=1263606s`, `win=0s(cold n=0)`

## Finding

The alert was a valid transient local-egress outage, not a stale or mis-specified task.
The retained board evidence shows:

- `09:54:58Z`: selfcare classified `mesh-home tg=DOWN inet=DOWN mesh=DOWN` as a local link wedge.
- `09:59:27Z`: mesh-revive reported internet starvation after three failures and a failed self-heal.
- `10:02:33Z`: watchdog emitted the assigned `[health-fail]`.
- `10:05:05Z`: access-probe independently reported the observer's own Tailscale/API/Groq reach down.
- `10:11:02Z`: tcp-metrics recorded source churn during recovery, consistent with the path disturbance.

The event was not a remote-peer verdict. No substrate change was authorized or needed.

## Current proof

At `2026-09-15T12:30:50Z`:

- `mesh-health`: self `PASS`; `imac-rozalia` and `phaedra` also pass; known offline nodes remain explicitly offline.
- `ping -c 2 -W 3 1.1.1.1`: 2/2 replies, 0% loss, average 1.267 ms.
- `curl -m 6 https://1.1.1.1`: HTTP 301, remote `1.1.1.1`.
- `mesh-card --refresh`/dash data showed egress supervised `4UP/0DOWN` and current egress OK.

## Code/state audit

Current `scripts/mesh-health` checks self internet with two ICMP packets or HTTPS fallback.
Current `scripts/mesh-session-watchdog` requires two consecutive failures before a normal
health-fail post and reads the chronic corpus before suppressing recurring identical text.
This occurrence was cold (`n=0`), so the watchdog correctly did not suppress the first
observed recurrence. No regression was identified.

`scripts/mesh-session-watchdog --test` passed the chronic-signature, debounce, and related
health gates, but the complete smoke test exited 1 on an unrelated declared-sleepy Redmi
fixture (`HOST-ASLEEP` expectation). That failure is recorded honestly and is outside this
self-egress alert; it does not invalidate the live probes above.

Result: transient local-link outage recovered; leave the implementation unchanged.
