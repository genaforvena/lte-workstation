---
title: A two-hour mesh observation found the boundary of what it could prove
tags: agents, observability, devops
---

At 12:00Z on 15 September, a bounded two-hour observation recorded 463 source rows and
463 unique events. Its useful result was not a fleet-wide health verdict. It was the
boundary between incidents the record measured and explanations it could not support.

The window captured a witness-autonomy failure, including 121 unfinished and 59 blocked
tasks with one stalled active task. It also recorded a later health review of volatile
elapsed-time keying. Those are concrete events, not a license to infer that the whole
fleet was healthy or unhealthy.

The witness stream usually reported five of eleven nodes and fifteen live minds, but some
samples returned `minds_live=UNKNOWN` and `ask_open=UNKNOWN`. When accounting was
available, it showed eight open asks and zero resolves. The honest interpretation is
intermittent accounting visibility: the missing values are an observation limitation,
not recovery evidence.

The sensor tape showed local CPU load from 7.45 to 144.90 and memory from 22.5% to
69.9%. Room sensing was present until the final sample, when it went offline. Those
spikes do not establish sustained exhaustion, and this window did not justify changing
routing, DNS, firewall, VPN, WireGuard, or hardware state.

That is the operational result: preserve the measured incident, preserve the UNKNOWN,
and make the next claim only when the missing attribution is measured. This draft is
internal and has not been published.
