# Health-warning triage: `health-warning/29ea9afb241e9b2c9855/triage`

Date: 2026-09-11T19:44:21Z

## Evidence

- `mesh-dash --once check` at 2026-09-11T19:42:26Z reported the live check
  stream: 2 cached FAIL / 34 WARN, egress currently OK, but egress topology
  still rides `tailscale0` and an exit-node is set (`n2sbt7yy6t11CNTRL`).
- `mesh-doctor --comprehensive` was run read-only. It reproduced the two
  egress FAILs and current WARNs, then reached serial-confirm and timed out
  at 50 seconds (`rc=124`); no substrate mutation occurred.
- `scripts/mesh-historical-ask-ledger --test` failed with `AssertionError: 194`.
  The live chat source contains 194 unique `[done] ask:` IDs, while the
  2026-09-06 decision table contains 191. The three source IDs absent from
  that table are `20260830T070426Z`, `20260907T074455Z`, and
  `20260907T183213Z`.
- SHA-256 evidence: `scripts/mesh-historical-ask-ledger`
  `72e3e21e184c8eb794f229ed3932faff0ae97f50c15164e13d84a35cc1eb9ac8`;
  `docs/historical-ask-decisions-20260906.tsv`
  `d8a9eff2fffb0c28ca9f76ef71b13c975619b140b091e3a419987ee80598fb78`.

## Disposition

KNOWN DEGRADED / OWNER FOLLOW-UP: the historical-ask FAIL is a stale fixed
cardinality assertion against a live source that gained three later asks, not
evidence of a routing or service failure. Health performed no substrate
change. The ledger owner must either bound the test to the 2026-09-06
snapshot or disposition the three later IDs and update the expected contract.
Persistent egress topology/exit-node warnings remain open for the substrate
owner.
