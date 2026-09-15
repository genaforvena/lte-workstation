# Pub measured-case draft — 2026-09-15

## Source and provenance

- Source artifact: `task-receipts/health-observation-analysis-20260915T110000Z-130000Z.md`
- Source SHA-256: `c8ad5ee000c0431c3dba0e689fe8d2707ba50c3e041dba6e353f9090e1055936`
- Measured interval: `2026-09-15T11:00:00Z` through `2026-09-15T13:00:00Z`
- Repository observation: `HEAD=ac37a2fb8a67a7d1d940e1f6a578b4f01ecf10da`; worktree was dirty during capture, so this source is not attributed to a clean commit.

## Candidate title

What a two-hour mesh observation can prove—and what it cannot

## Draft (not published)

At 11:00Z on 15 September, a two-hour mesh observation recorded 431 unique events: 300
chat rows, 59 witness rows, and 72 sensor rows. The useful result was not a single green
health label. It was the boundary between concrete incidents and tempting explanations.

The record caught a proxy service restarting four times in about five minutes, a Python
process killed by the heavy-run cgroup, USB disconnects, and a VPN path that later
recovered. It also caught reboot boundaries where the device accumulator correctly emitted
`REBOOT` and `delta=na`, rather than treating a reset counter as calm. At 12:30Z, 18 of 24
events were missing, so attribution stayed unknown.

The same window had 24 room, load, and memory samples: room was present throughout; load1
ranged from 5.38 to 144.90 (median 11.37), and memory from 18.9% to 69.9% (median 37.7%).
Those samples show spikes, not sustained exhaustion. The honest conclusion is narrower:
the mesh had several measured peripheral and service incidents, but this window does not
justify changing routing, VPN, DNS, firewall, or hardware state. It also cannot turn sparse
path transitions and incomplete post-reboot events into a continuous fleet verdict.

That distinction is the operational artifact: preserve the incident, preserve the unknown,
and make the next claim only when the missing attribution is measured.

## Publication disposition

This is an internal draft only. No `mesh-devto-publish` action was taken because the source
worktree is dirty and the charter requires an artifact-backed public case plus a notification
before any irreversible external push. The next publishing decision requires a clean provenance
choice and explicit pre-push board notice.

## Verification

`sha256sum task-receipts/health-observation-analysis-20260915T110000Z-130000Z.md` produced the
source hash above. The cited measurements and disposition were transcribed from that artifact;
no external data or uncited claim was added.
