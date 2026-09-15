# Health-warning triage: `health-warning/94e1079a8cd06ff4b315/triage`

- Checked: 2026-09-12T14:04–14:08Z
- Owner: `health` on `mesh-home`

The warning is partly historical and partly still live. `mesh-occupancy-kind --test` now passes
(14 fusion assertions and a cached read). The DNS values in the roll-call were resolver addresses,
not a changed A record; the later DNS investigation in
[`health-warning-20d10f9590203ff1e74f-20260912.md`](health-warning-20d10f9590203ff1e74f-20260912.md)
reproduced A=`160.79.104.10` and documented that the link resolvers timed out over the selected
Tailscale route.

The installed `mesh-opencode-plugins --test` failure was current and reproducible. The executable
is a symlink to `scripts/mesh-opencode-plugins`; the script used `$0` to derive `opencode-plugins/`,
so invocation through `~/.local/bin` looked beside the symlink and found no source files. The
repository-path invocation passed. The script now resolves `${BASH_SOURCE[0]}` with `readlink -f`
before deriving the source directory, so both invocation forms use the tracked plugin directory.

Current health gaps remain: the one-shot pane at 14:07:53Z reports external egress OK at 0% loss,
but the FIB/doctor still identify `tailscale0` and the configured exit node as an egress SPOF; the
fleet path is degraded (8 peers, 1 direct, 1 relay), and LAN presence is `UNKNOWN` because the
router is unreachable. The doctor result shown in the pane is cached from 13:35:58Z (`3F/34W`),
so no fresh total or post-fix doctor verdict is claimed. No route, VPN, DNS, firewall, or audio
settings changed.

## Verification

- Before the change, `rtk mesh-opencode-plugins --test` failed because the symlink-relative source
  path found zero plugins; `rtk proxy scripts/mesh-opencode-plugins --test` passed.
- After the change, both commands pass: `opencode-plugins-test: ok (4 tracked plugins deploy
  byte-identical; node-local files kept)`.
- `rtk bash -n scripts/mesh-opencode-plugins` and `rtk git diff --check -- scripts/mesh-opencode-plugins` pass.
- `rtk mesh-occupancy-kind --test` passes.
- `rtk mesh-lan-presence --nodes` still exits 1 with router-unreachable `UNKNOWN`.
- `rtk mesh-dash --once check` at 14:07:53Z reports egress OK and the degraded fleet/LAN/doctor-cache
  state above.
