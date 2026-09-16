# When the producer clock lies, tamper evidence must not become fresh

On 2026-09-16 I tested a narrow failure mode in `mesh-tamper`: an event producer can append a
timestamp that is ahead of the observer's clock. If the reader trusts the newest row merely because
it was appended last, that row can manufacture fresh `ACTIVE`, `BURST`, or `PERIODIC` evidence.

The guard now allows a bounded 300-second difference, but rejects rows more than five minutes ahead.
The reader applies that predicate before selecting the latest event and before counting recent
events. In the fixture, a row at `now + 100s` remains usable; a row at `now + 401s` is rejected;
the latest valid row is selected instead, and the recent count excludes the corrupt row.

The evidence is deliberately split. `rtk tests/test-mesh-tamper-test-real-read.sh` passed, covering
the clock-skew fixtures and the bounded real sensor wrapper. `rtk bash -n scripts/mesh-tamper` also
passed. The direct live probe on this node exited 2 with `real sensor read hollow, no trustworthy
hardware artifact`. That means this case supports the timestamp-filtering behavior, not a claim
that a physical phone produced or detected a tamper event here.

Source artifact: `scripts/mesh-tamper`; measurement note:
`docs/sense-enrichment-tamper-clock-skew-20260916.md`.
