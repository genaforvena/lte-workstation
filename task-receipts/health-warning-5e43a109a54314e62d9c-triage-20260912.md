# Health warning triage: September 9 roll-call

Chain: `health-warning/5e43a109a54314e62d9c/triage`  
Checked: 2026-09-12 08:58 UTC on `mesh-home`  
Source: the 2026-09-09 10:01Z roll-call reported `route:no`, retired proposal state, a doctor rerun, and persistent egress/exit-node failures plus a microphone warning.

## Current evidence

- The consumed `mesh-dash --once check` pane at 08:56Z showed a cached doctor summary of 3 FAIL/33 WARN. The displayed current failures included overlay egress, an exit-node SPOF, and `tinyfleet_split_audit.py` not executable. The mic was WARN in the doctor cache.
- `rtk mesh-doctor` was started at 08:57Z. It repeated the egress-on-`tailscale0` and configured-exit-node FAILs, reported Anthropic reachable, microphone capture via `plughw:1,0` PASS with the default device WARN, and supervised loops UP. It had not exited after 30 seconds, so I terminated the two doctor invocations started during this triage. No full fresh doctor verdict is claimed.
- The `route:no` item in the source is an old proposal marker explicitly labeled retired on 2026-09-07. It does not represent an actionable route claim in this triage. The current egress FAIL is real, but routing/VPN state was not changed.

## Disposition

The egress and exit-node findings remain current known faults; the microphone default remains a known warning while explicit-device capture works. This triage did not change substrate state. A full fresh doctor verdict remains unavailable because the check did not finish within 30 seconds. The reported `route:no` proposal is retired, not open work.
