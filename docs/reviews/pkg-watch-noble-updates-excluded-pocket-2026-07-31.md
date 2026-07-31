# mesh-pkg-watch — sensing the apt pocket unattended-upgrades silently excludes

**Date:** 2026-07-31 · **Lane:** metabolic loop (discover→health→**genome**) · **Organ:** `scripts/mesh-pkg-watch` (new)

## The find (discover, verified by health)

discover 2026-07-31 (knowledge/`capability-apt-noble-updates-pocket-excluded-unattended-upgrades-mesh-home-20260731.md`),
verified by health 13:04Z: `/etc/apt/apt.conf.d/50unattended-upgrades` `Allowed-Origins` covers
`${distro_codename}` + `-security` (+ESM) but **not `-updates`** — Ubuntu's routine non-security SRU
pocket. `apt-check` reports 34 upgradable / 2 security; the packages landing only in `noble-updates`
sit un-applied forever. unattended-upgrades is **not dead** (weekly real installs verified) — it is
**scoped**, with a narrower blast radius than its name implies, and nothing watched what accumulates in
the unscoped pocket. `mesh-sync-tools` checks genome↔`~/.local/bin` drift; nothing checked
installed↔available **system-package** drift. Load-bearing stuck packages: `nftables`/`libnftables1`
(the firewall backend `mesh-fix-egress`/`mesh-card` reason about), `tailscale` (the nervous system),
`apport` (a mesh sense), `iproute2`, `apparmor`.

## What genome wrote (the safe half)

`scripts/mesh-pkg-watch` — a report-only **sense**. It does **not** widen `Allowed-Origins`: auto-applying
`noble-updates` would unattended-upgrade `nftables`/`iproute2`/`tailscale` (substrate-adjacent), a
security-posture change reserved to the operator (CLAUDE.md: confirm before outward/substrate change).
The tool's job is to make the blind spot **visible and loud for load-bearing packages** — never a raw
count flood.

**Correctness (not a hollow gate):** "stuck" ≠ "upgradable". The detector reads **both** the config
(which suites `Allowed-Origins` covers, `${distro_id}`/`${distro_codename}` expanded) **and**
`apt list --upgradable` (each pending package's pocket); a package is stuck iff its pocket ∉ covered
suites. Fix the config to include `-updates` and every such package flips to covered → count 0 (the gate
tracks the config, it is not a constant — `--test` leg 3 asserts exactly that transition). **Fail-closed
to n/a** (exit 2): no apt / no config / an unparseable Allowed-Origins (zero covered suites) → never
"flag all 34", which an empty covered-set would otherwise do (the fusion false-alarm shape).

Live on mesh-home now: `STUCK — 33/51 in [noble-updates,unknown] not in Allowed-Origins`, load-bearing
`apparmor,apport,apport-core-dump-handler,iproute2,libnftables1,nftables,tailscale`, exit 1.

**Wiring:** `# reflex-cadence: 17 4 * * 1` (weekly) `--once` → `mesh-autowire` picks it up post-land
after the passing `--test`. The reflex posts a single signature-deduped `[fyi]` only when a load-bearing
package is stuck (rare + loud), so the find becomes a standing board signal, not a scroll-away.

## Verification (RED-first)

`--test`: synthetic apt-list + two config fixtures. Leg 1 asserts the two `noble-updates` packages are
flagged STUCK and `nftables` is named (2/4, exit 1); leg 2 that covered-pocket packages are not;
leg 3 that adding `-updates` clears it; leg 4/5 fail-closed n/a on empty/absent config; leg 6 a live
apt-check real-read gate (`N;M`, honest skip if absent). Mutants proven RED: all-covered → leg 1 red
(vacuous); empty-covered → leg 3 red (constant). Restore green. (A load-time-global export trap bit the
first run — `CONFIG`/`APTLIST_SRC` captured at source time; fixed to read env at call time,
[[export-does-not-rebind-a-load-time-global]].)

**Status:** uncommitted in-tree for the steward (genome source only, not deployed/committed).
