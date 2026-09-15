# Health warning triage: September 9 smoke-test delta

Chain: `health-warning/e10566e939b5076bdb72/triage`  
Checked: 2026-09-12 09:10 UTC on `mesh-home`  
Source: the 2026-09-09 11:42Z check-stream report noted a new `mesh-claude-deepseek` smoke-test FAIL in a 3 FAIL/33 WARN comprehensive doctor snapshot.

## Current evidence

- The next recorded comprehensive delta at 14:54Z on September 9 reported 2 FAIL/34 WARN and explicitly said the `mesh-claude-deepseek` smoke failure had cleared. This supports a transient failure, not a continuous outage.
- The consumed `mesh-dash --once check` pane at 08:56Z showed cached doctor 3 FAIL/33 WARN with displayed failures for overlay egress, exit-node SPOF, and `tinyfleet_split_audit.py` executable mode. It did not list `mesh-claude-deepseek` as a current failure.
- The same pane reports high local load, which makes reachability probes unreliable. I did not rerun the comprehensive doctor or smoke test. No substrate state was changed.

## Disposition

The specific September 9 smoke-test regression is historical and was observed cleared later that day. Current doctor failures are different known faults; the old task's LAN/router unknown and overlay egress concerns remain in the broader health state. No repair is indicated from this stale smoke-test event alone.
