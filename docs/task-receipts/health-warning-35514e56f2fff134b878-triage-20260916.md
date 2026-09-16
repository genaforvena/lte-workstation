# Health-warning triage — Redmi 10 SSH transport

Task: `health-warning/35514e56f2fff134b878/triage` (owner `health`).

Warning source: `~/.mesh/chat.log:75673`, watchdog timestamp `2026-09-16T11:33:28Z`.

## Fresh evidence

Collected at `2026-09-16T12:23:58Z` and after:

- `mesh-health` passed this node and reported `SKIP Redmi 10 100.103.99.16 (android) — SSH unreachable`.
- ICMP to `100.103.99.16` succeeded: 2/2 replies, 0% loss, average 3.631 ms.
- Tailscale reports `Redmi 10`, `Online: true`, addresses `100.103.99.16` and `fd7a:115c:a1e0::133b:6310`.
- Canonical SSH probe `u0_a380@100.103.99.16:8022` returned `Connection refused` (rc 255).
- Port 22 probe returned `Connection refused` (rc 255).
- `mesh-dash --once check` timed out after 15s (rc 124) without output; this is recorded as an observer timeout, not used as proof of a network fault.

## Recheck

At `2026-09-16T13:13:08Z`, the canonical probe
`ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=5 u0_a380@100.103.99.16 true`
returned rc 0. ICMP also returned rc 0 (5.353 ms), port 8022 accepted a TCP
connection, port 22 still refused, and `mesh-health` returned rc 0 with Redmi
10 marked PASS. This is the first successful canonical SSH probe and satisfies
the retry predicate recorded below; the prior external-event block is no
longer current.

## Disposition

Typed `external-event` block. The node, route, Tailscale peer, and L3 path are live; the target-side SSH listener/service is unavailable. No routing, DNS, firewall, VPN, Tailscale, or credential mutation is justified from these readings, and the health-window substrate single-writer boundary remains unchanged.

Per `mesh:2`, `mesh:5`, `mesh:6`, `mesh:8`, and `mesh:9`, the exact blocker is: Redmi-side Termux SSH service must begin accepting the canonical probe. The bounded mesh prerequisite `unblock/health/35514e56f2fff134b878/resolve` records and retries that condition; it does not pretend to repair an unavailable phone-side service.

Retry edge: when a fresh `ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=5 u0_a380@100.103.99.16 true` succeeds, rerun `mesh-health`, then resume and settle this task with the resulting real phone artifact. Until then, keep this task blocked rather than treating ICMP or Tailscale presence as SSH health.

Rollback/retry: no mutation was made; repeat the bounded probes after the retry event.

## Follow-up disposition for `health-warning/d2a26980226cbb14e59a`

The 12:32 witness warning was accurate: the Redmi triage was active for 2392s
while its exact-owner recovery path was being created. The parent is now
typed-blocked on that recovery, and the recovery chain is active under its
designated owner (`adint`). The fresh successful SSH probe at 13:13:08Z makes
the external predicate pass, but the parent must remain pending until the
recovery owner records its artifact-backed completion. No duplicate recovery,
substrate change, or claim of parent completion is justified here.

Delegation record: a read-only `health-warning-scan` worker launch was attempted
before triage; no worker session or artifact was created because the node was
under severe CPU contention (load average 92.48/101.81/97.28). I personally
inspected the canonical task JSON, chat-log ledger rows, existing parent
receipt, live SSH probe, and `mesh-health` output.
