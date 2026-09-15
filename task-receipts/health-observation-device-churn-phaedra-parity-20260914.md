# Phaedra device-churn attribution parity — 2026-09-14

Task: `health-observation-device-churn-phaedra-parity-20260914/verify-phaedra-attribution-parity`

## Verdict

The four Phaedra `CHURN delta=6` reports are six-step global uevent-counter advances, not verified
external device enumerations. For each interval the matching `mesh-udev-stream` summary reports
`GAP events=0`, `coverage=100%`, and `seqdelta=6`. Applying the conservative rule in
[`device-churn-signed-probe-attribution-20260914.md`](docs/task-receipts/device-churn-signed-probe-attribution-20260914.md),
all six seqnums in each interval are missing from the retained event tape and therefore unknown;
they remain in the possible-nonprobe upper bound. No event can be classified as a matched signed
probe or an observed unsigned event from these records.

Phaedra's installed tool matches its own source, but both are older than the current landed Genome
source and lack its per-seqnum source-attribution join. The old reports' phrase “real enumeration
event” overstates what the global counter establishes. The logs support recurrent, unattributed
counter activity; the known non-init-net visibility gap is a plausible explanation, not an
event-level attribution.

## Source and deployment identity

Read-only SSH verified the host as `phaedra.tail3e4555.ts.net` (`root`). At 2026-09-14 15:19Z:

| Artifact | SHA-256 |
|---|---|
| Phaedra `/root/lte-workstation/scripts/mesh-device-churn` | `fd15b0996528971b3ec1fe8043693c2afd5a4d1ad114152d397ef9e7ee508c3c` |
| Phaedra `/root/.local/bin/mesh-device-churn` | `fd15b0996528971b3ec1fe8043693c2afd5a4d1ad114152d397ef9e7ee508c3c` |
| Genome `scripts/mesh-device-churn` | `d06a9d8519880400c4dee41f98615a49e8e00c03a139682e0b3851c207cf4d02` |
| Phaedra source and installed `mesh-uevent-sig.sh` | `c578ee938bd0209394ddd1972ffca895ae810f1f59749f54e50db902778b1b7a` |

Phaedra repository HEAD was `6e7a7826b1650e7f280c708f95fa493d4adf6a27`; its last commit touching
`mesh-device-churn` was `7b641adf02f59bb2b072944cd4fc038d8ab9ed25`. Genome's current landed source is
commit `8b0f1565e4c1a325115839cbef72810e18daaa07` (`Classify exact signed probes in device-churn
while preserving unknown events`). The Phaedra copy is byte-identical to its install but differs
from Genome's landed source. The shared signature helper matches, but the Phaedra script does not
contain the current `source_interval_attribution` implementation or its `source-attribution` /
`possible-nonprobe` output fields.

## Four reported intervals

The `device-churn.log` rows expose each baseline and ending counter. The corresponding
`udev-stream.cron.log` GAP row is timestamped 14–17 seconds later.

| CHURN report UTC | Exact counter interval `(baseline,current]` | Sequence numbers | Matching udev summary UTC | Observed rows | Missing / unknown | Possible nonprobe |
|---|---:|---|---|---:|---:|---:|
| 11:05:03 | `(17903,17909]` | 17904–17909 | 11:05:17 | 0/6 | 6 | 6 |
| 11:35:03 | `(17909,17915]` | 17910–17915 | 11:35:19 | 0/6 | 6 | 6 |
| 12:05:03 | `(17915,17921]` | 17916–17921 | 12:05:20 | 0/6 | 6 | 6 |
| 12:35:03 | `(17927,17933]` | 17928–17933 | 12:35:20 | 0/6 | 6 | 6 |

Each matching udev summary has `events=0`, `unattributed=0`, `coverage=100%`, `seqdelta=6`, and
the matching `seq-total`; its source breakdown has zero observed signed, unsigned, kernel, foreign,
and unknown event rows. Those zero row counts do not classify the six counter increments: the six
sequence numbers are absent from the event tape. The summaries label each window `GAP` and report
`gap-floor=6`, `gap-floor-n=400`, `gap-floor-src=measured-p95`. This is consistent with the known
global-counter/non-init-net observer mismatch, but does not identify the source of any individual
sequence number.

The retained raw event input `/root/.mesh/udev-stream.log` has no rows for any of the 24 target
seqnums. Phaedra has no `/root/.mesh/udev-stream.log.1` rotation to supplement it. The summaries
are retained in `/root/.mesh/udev-stream.cron.log`. Thus the current attribution rule yields, for
each target interval: `observed=0/6`, `probes=none`, `unsigned=0`, `kernel=0`, `foreign=0`,
`unknown=6`, `missing=6`, `possible-nonprobe=6`. This is an upper bound, not proof that six external
events occurred.

## Read-only live check and no-change evidence

At `2026-09-14T15:22:25Z`, `/root/.local/bin/mesh-device-churn --check` exited 0 and rendered
`QUIET delta=0 interval=141s`, with the same boot ID `e42f5e4e`. SHA-256 values immediately before
and after the check were identical:

| Phaedra artifact | SHA-256 before and after |
|---|---|
| `/root/.mesh/.device-churn.baseline` | `eabf0f36d3bd0394729928650d4ffa48d5a06f7d479f94231482c1111532a06f` |
| `/root/.mesh/.device-churn.state` | `25a7e0bf271fa8349e517b33ec908af6e7183083e647bbc1601b6aa21fcaf07b` |
| `/root/.mesh/.device-churn.posted` | `4248a9b568b7231c684c280ec021abfc101af2503918ff6b6a5b48472431c942` |
| `/root/.mesh/.device-churn.tally` | `e014176684c5e9487c8135d68cb27c81cfcb3e5cdccf5813f1f98028e1b35861` |
| `/root/.mesh/device-churn.log` | `ade8e68b6f355f2dd30dcba3c0ff15d8008d54e3ddf6b3dc413d407d1448a574` |

Commands used included `sha256sum` on both source/install paths and those five artifacts,
`git -C /root/lte-workstation rev-parse HEAD`, `git -C /root/lte-workstation log -1 --format=... --
scripts/mesh-device-churn`, and exact timestamp queries against `device-churn.log`,
`udev-stream.cron.log`, and `chat.log`. The four `[fyi]` chat rows reproduce the same report times and
values. No source or runtime file was changed; no USB/hardware, network, route, DNS, firewall, VPN,
service, or exit-node action was taken.

## Retry condition

Keep the source mismatch visible. Re-run this parity check after Phaedra's source and installed
`mesh-device-churn` both match Genome's landed source. Preserve per-event rows from
`/root/.mesh/udev-stream.log` (including each `seqnum=` and signed `synth=` value) through each full
`(baseline,current]` interval; retry attribution when a future nonzero interval has retained raw rows
covering its sequence numbers. Until then, retain the six missing values in each of these four
intervals as unknown and possible nonprobe; do not label them external enumeration or signed probes.
