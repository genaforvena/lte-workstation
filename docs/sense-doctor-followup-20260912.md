# Senses doctor follow-up — 2026-09-12

Resumed the senses handoff and ran `timeout -k 5 600 mesh-doctor` to completion.

- Exit status: 2; summary: **2 FAIL, 33 WARN**.
- FAILs: egress rides `tailscale0`; exit-node `n2sbt7yy6t11CNTRL` is set.
- Sensor organ evidence: camera capture PASS; microphone capture PASS on `plughw:1,0`; default mic remains WARN (broken/busy).
- Smoke tests: all applicable `--test` checks PASS. Doctor also reported 110 tools leaving temporary files, and 17 stale failures / 4 never assessed; those are not fresh confirmations.
- Orphan scan completed: 92 confirmed unwired/non-canonical tools, with new entries `mesh-band-gate`, `mesh-lease-gate`, `mesh-spearman`, and `mesh-uxn-hop`. It also reported invalid `orphan-ok` exemptions for `mesh-lease` and `mesh-sound-progress`.
- Other surfaced WARNs include 26 dead sign-vehicles, two inverse-orphans (`mesh-home`, `mesh-nic-tx-rate`), and topology leaks. These are substrate-owner work; this run did not change them.
- `mesh-task queue --dispatch --owner 'senses'` returned no rows, so there was no eligible owned task to validate or take.

No `[sense]` claim was posted: the full doctor did not PASS and found new orphan WARNs. The current senses lane is waiting on substrate owners to resolve the existing blockers before a passing doctor run.
