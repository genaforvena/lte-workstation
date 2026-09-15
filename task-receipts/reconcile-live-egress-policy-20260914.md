# Live egress policy reconciliation — 2026-09-14

Task: `chat-review-egress-table52-regression-20260914/reconcile-live-egress-policy`.

## Claim and scope

The board task was still open when checked at 13:48Z and was claimed by `vpn` at 13:54:34Z.
This review reads current kernel routing, Tailscale state, and the declared node policy. No route,
rule, VPN, or exit-node state was changed.

## Live evidence

At 13:54:59Z, `ip -4 rule show` read priorities 5210/5230/5250 for Tailscale-marked traffic,
priority 5270 `from all lookup 52`, then main at 32766. The main table had
`default via 100.74.0.1 dev enp42s0` and the connected `100.74.0.0/16` route. Table 52 had
`default dev tailscale0`, peer `/32` routes on `tailscale0`, and a `throw 100.74.0.0/16`; it also
retained throws for `100.76.0.0/16`, `127.0.0.0/8`, `172.17.0.0/16`, and `192.168.8.0/24`.

Fresh FIB lookups at the same time:

- Public `1.1.1.1` → `dev tailscale0 table 52`.
- Current LAN gateway `100.74.0.1` and in-prefix address `100.74.254.254` → `dev enp42s0`.
- Phaedra `100.94.116.17` → `dev tailscale0 table 52`.
- Phaedra's public endpoint `38.49.216.141` → `via 100.74.0.1 dev enp42s0` (the direct rescue path).

`tailscale debug prefs` reported `ExitNodeID=n2sbt7yy6t11CNTRL` and
`ExitNodeAllowLANAccess=true`; `tailscale status --json` reported the backend `Running` and peer
`phaedra` `Online=true`, `ExitNode=true`. `mesh-card --exit-node-lan` returned `state: ok` for
`100.74.162.157/16`, with `100.74.0.1 -> dev enp42s0`. A proxy-bypassed fetch of
`https://api.ipify.org` returned `38.49.216.141`.

The final recheck at 14:06–14:07Z caught the tether alternating between DHCP prefixes
`100.76.0.0/16` and `100.74.0.0/16`: at 14:06:13Z main default/address were via `100.76.0.1`
and `100.76.77.189/16`; by 14:07:11Z they were via `100.74.0.1` and `100.74.163.226/16`.
Table 52 retained throws for both prefixes through the reads. At 14:07:11Z, both
`100.74.0.1` and `100.74.254.254` resolved via `enp42s0`, while `1.1.1.1` still resolved via
`tailscale0 table 52`. The fresh `mesh-card --exit-node-lan` and read-only
`mesh-exit-node-lan-heal --check` both reported the active prefix healthy; the latter stated it
writes no run row. Thus the prefix churn did not change the public egress classification or swallow
the currently selected LAN range.

## Policy and doctor result

The node-specific policy in `CLAUDE.local.md:187-195` says public egress is phaedra's Tailscale
exit node, and `:822-837` records that bypassing it returned Anthropic 403 on the direct RU uplink
while the exit-node path returned 405. The generic substrate invariant in `docs/coordination.md:103-108`
applies to a node that **offers** a route; mesh-home is consuming phaedra's route. The older
`CLAUDE.local.md:838` line still says NL via router LAN VPN, but the adjacent 2026-08-30 update
(:839-850) marks that state superseded and says mesh-home already egresses through phaedra. That
older line should be clarified so it cannot be mistaken for current policy.

The repository and installed `mesh-doctor` both contain the same role-blind rule: the egress check
unconditionally fails any `tailscale*` public device as “should be LAN” and unconditionally fails
any set `ExitNodeID` as a SPOF (`scripts/mesh-doctor:4887-4893`, installed
`~/.local/bin/mesh-doctor:4882-4888`). Their full-file hashes differ, so a future correction must
also verify source/deployed parity.

A fresh `timeout 60s mesh-doctor --quiet` run at 13:58:14Z reproduced both egress FAILs. It also
reported unrelated microphone and untimed peer-SSH warnings, then hit the 60-second bound with
exit 124; the aggregate scan did not finish. The specific egress findings appeared before timeout
and match the inspected rule.

## Disposition

The public route through `tailscale0`/table 52 is **intended under the current node policy**, not a
FIB regression. The table-52 throw sends the live connected LAN prefix back to the main table, and
the exit-node endpoint also resolves over the direct uplink. The task premise that current local
policy expects public LAN egress is incorrect; the live doctor warning comes from a generic check
that does not distinguish consuming an exit node from offering one.

Smallest safe next action: leave routing and Tailscale state alone; make the doctor check
policy/role-aware, preserving the live LAN-target FIB guard, and verify its deployed copy. Clarify
the superseded local-policy line noted above as part of that review.

## Follow-up registration

The detector correction is tracked as `mesh-doctor-egress-policy-20260914/make-egress-check-role-aware`
for the `health` owner (created 14:05Z and left open for dispatch). This audit itself performed no
network mutation and ran no code tests.
