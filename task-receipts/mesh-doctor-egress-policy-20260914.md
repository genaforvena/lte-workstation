# mesh-doctor egress policy correction — 2026-09-14

Task: `mesh-doctor-egress-policy-20260914/make-egress-check-role-aware` (owner `health`).

## Current code and policy audit

`mesh-task check dispatch mesh-doctor-egress-policy-20260914/make-egress-check-role-aware health`
returned 0 and the exact owner claimed the row. The source still unconditionally failed every
`tailscale*` public device and every nonempty `ExitNodeID`. The current node card declares
`connectivity: shadowsocks`, `exit-node: phaedra`, public egress on `tailscale0`, and a healthy
`exit-node-lan` FIB result. The prior live reconciliation receipt records a fresh LAN-prefix FIB
lookup via `enp42s0` and table-52 throws for the active tether prefix. This node consumes phaedra's
exit route; it is not declaring itself an exit-node provider.

The `CLAUDE.local.md` line that said “NL via router LAN VPN” is now explicitly marked historical
and superseded, with a pointer to the current phaedra policy at lines 187–195. The earlier
reconciliation receipt was preserved byte-for-byte because it is the evidence artifact for a
completed task.

## Change

`scripts/mesh-doctor` now reads the local card's declared `connectivity:` capability to classify
route direction. A declared `exit-node`/`vpn-egress` provider still must keep its control-plane
egress on LAN and must not consume an ExitNodeID. A declared non-provider with an ExitNodeID is
checked as an intentional consumer: public egress must use the configured Tailscale exit node, and
the report names the intentional single-node egress dependency as a NOTE. Missing policy remains
unknown and cannot silently exempt an overlay.

For any configured ExitNodeID, the check also runs `mesh-card --exit-node-lan` and uses its live
`state:` from the LAN-prefix FIB lookup. The consumer verdict therefore remains independent from,
and cannot mask, a swallowed LAN prefix. No route, rule, DNS, VPN, or exit-node state was changed.

## Verification and limits

- The focused regression was first run red (the production policy functions were absent), then
  passed after implementation against both `scripts/mesh-doctor` and the deployed path.
- `bash -n scripts/mesh-doctor tests/test-mesh-doctor-egress-policy.sh` passed.
- `bash tests/test-mesh-doctor-help.sh` passed.
- `bash scripts/mesh-card --test` passed its LAN-prefix FIB fixture suite.
- Source and deployed `mesh-doctor` are byte-identical, SHA-256
  `5a936075183fc774ccff98bbb855897ecee770c0bf12883872bf484a57a22c78`. The deployed path is now
  a symlink to the repository source; its prior regular file is backed up at
  `~/.mesh/tools-backup/mesh-doctor.pre-egress-policy.20260914T142325Z`.
- A live full `mesh-doctor --quiet` run could not be started: it refused because an automated
  doctor held `~/.mesh/.doctor.lock`. That lock was left intact. The visible old doctor log is
  timestamped 13:23Z, before this change, so it is not post-change runtime evidence. The exact
  next live verification is to run `/home/mesh-home/.local/bin/mesh-doctor --quiet` after the
  automated lock releases and inspect the resulting egress lines.
- `mesh-dash --once check` was invoked as requested but returned no captured pane text in this
  shell. The policy decision used the current local card plus the prior live reconciliation
  artifact, and test fixtures exercised both verdict directions and the FIB fail case.

The health wake prediction was refreshed at 14:28Z with four narrow expected line shapes: the
steady self/chrome line, fleet age, unchanged-OK feed/evolve ages, and the pane's render counter.
