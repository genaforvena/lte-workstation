# Health-warning triage: `health-warning/1aa3693a102855b922e4`

- Checked: 2026-09-12T11:53–12:00Z
- Owner: `health` on `mesh-home`
- Task: `health-warning/1aa3693a102855b922e4/triage`

## Finding

The 2026-09-10 roll-call's specific Tailscale details are stale: current status reports
`imac-rozalia` online but inactive (relay `hel`), while `phaedra` is online, active, selected as
exit node, and using relay `tor` (not direct). The FIB still selects `tailscale0` table 52, so the
exit-node/effective-path risk remains. LAN still has zero visible nodes and UVC metadata is DARK.
External egress worked in the current health pane.

The reported new `mesh-sense-reception` failure needs qualification. A current read-only live audit
found no `FABRICATED`, `LOST`, or `MISMATCH` edges (6 AGREE, 3 n/a). However, the current
`mesh-sense-reception --test` exits 1: its leg5 clean polarity fails because the `rhythm-state`
edge's extractor cannot read a body-specific token from that consumer's fused rhythm output. This
is a current test/edge-contract failure, but the live audit does not show a current fabricated
sensor reception. The latest doctor scan also recorded a timeout as `not-a-verdict`, and the pane's
3 FAIL/33 WARN total is cached. No config or code changed.

## Evidence

Original warning: `/home/mesh-home/.mesh/chat.log:43812` (2026-09-10T01:03:07Z) reported 3F/33W,
including new FAIL `mesh-sense-reception`; LAN UNKNOWN; imac changed from active relay to offline;
phaedra direct exit; egress via `tailscale0`; DNS A unchanged. The exact health task is in
`~/.mesh/chat.log:56128`; it was still open and passed `mesh-task check dispatch` with exit 0 before
the exact-owner claim at `~/.mesh/chat.log:56135`.

`mesh-dash --once check` at 2026-09-12T11:53:05–11:53:10Z showed:

```text
egress tailscale0 | supervised 4UP/0DOWN | organs 14LIVE/1DARK
10 nodes: 2 ssh · 0 lan · 8 down | PATH: DEGRADED
up: mesh-home · phaedra
DOCTOR (cached 19m): 2026-09-12T11:33:51Z FAIL=3 WARN=33
  egress rides tailscale0 — should be LAN
  exit-node set (n2sbt7yy6t11CNTRL) — SPOF risk
  smoke-test FAIL (real): mesh-claude-deepseek
egress now: OK loss=0% avg=140.195ms mdev=0.382ms
organs DARK (1): mesh-home:uvc-metadata
```

`tailscale status --json` filtered to the two relevant peers, the FIB lookup, and DNS resolution:

```text
{"HostName":"phaedra","Online":true,"Active":true,"Relay":"tor","LastSeen":"0001-01-01T00:00:00Z","ExitNode":true}
{"HostName":"imac-rozalia","Online":true,"Active":false,"Relay":"hel","LastSeen":"0001-01-01T00:00:00Z","ExitNode":false}
1.1.1.1 dev tailscale0 table 52 src 100.81.222.19 uid 1000
160.79.104.10 STREAM api.anthropic.com
```

Current live reception read (`mesh-sense-reception`, header timestamp 11:53:46Z):

```text
body-motion -> motion-type      emitted=OFFLINE received=UNKNOWN AGREE
body-motion -> room-activity    emitted=OFFLINE received=UNKNOWN AGREE
body-motion -> rhythm-state     emitted=OFFLINE received=OFFLINE AGREE
body-motion -> body-context     emitted=OFFLINE received=-       n/a
body-motion -> occupancy-kind   emitted=OFFLINE received=-       n/a
body-motion -> window-state     emitted=OFFLINE received=OFFLINE AGREE
body-motion -> physical-context emitted=OFFLINE received=OFFLINE AGREE
body-motion -> motion-fuse      emitted=OFFLINE received=-       n/a
body-motion -> social-context   emitted=OFFLINE received=UNKNOWN AGREE
edges=9 FABRICATED=0 LOST=0 MISMATCH=0 AGREE=6 n/a=3
```

The tool source declares the rhythm edge at `scripts/mesh-sense-reception:94` with an extractor
that expects `body=<word>`. The current `mesh-rhythm-state` reads field 2 of the producer state
(`scripts/mesh-rhythm-state:105`) and fuses it into a rhythm verdict (`:145+`); its output does not
expose a separate `body=<word>` field for this extractor.

The current real test run (`mesh-sense-reception --test`, 2026-09-12T11:57:43Z) exited 1:

```text
ok: RED — emitted OFFLINE, consumer rendered STILL, rc=1
ok: GREEN when the consumer renders the emitted sign (rc=0)
ok: a field-2 reader declines the held-back candidate (emitted OFFLINE → AGREE)
ok: SIGNED — a consumer blind to a live sign is LOST/MISMATCH, not AGREE (rc=1)
ok: an ALREADY-RED shape renders n/a when the sign is stale
ok: leg5/held — every declared edge declines the sign (rc=0, no FABRICATED/LOST/n/a)
FAIL: leg5/clean — an edge did not render the emitted sign (rc=0)
  body-motion -> rhythm-state emitted=STILL received=- n/a
  edges=9 FABRICATED=0 LOST=0 MISMATCH=0 AGREE=8 n/a=1
smoke-test: FAIL
exit=1
```

Doctor log `~/.mesh/doctor.log:19301` (2026-09-12T11:23:01Z) classifies the latest rotation's
`mesh-sense-reception` subject as `SUBJECT-MOVED` with `probe-TIMED-OUT-not-a-verdict`; it does
not confirm a live failure. An earlier health handoff at `~/.mesh/chat.log:41266` had already
observed the same leg5/clean failure and rhythm-state parser result, so this is a repeated test
contract issue rather than a newly discovered runtime divergence.

The corrected roll-call is `/home/mesh-home/.mesh/chat.log:56164` (2026-09-12T12:00:42Z).

## Disposition

The old exact Tailscale peer states are no longer accurate, but the overlay FIB route, exit-node
selection, LAN visibility gap, and UVC dark state remain. Current external egress works. The
`mesh-sense-reception` smoke test is still red on a clean `rhythm-state` edge because the edge
extractor cannot read a body token from that consumer's fused output; this does not establish a
live fabricated reading. No substrate change or code change was justified by this health triage.
