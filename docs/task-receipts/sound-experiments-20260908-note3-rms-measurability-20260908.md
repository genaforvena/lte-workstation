# Note3 RMS/measurability — additional quiet-window receipt

Measured 2026-09-08 UTC for the still-open task
`sound-experiments-20260908/note3-rms-measurability`.

## Live-state audit

`mesh-task status sound-experiments-20260908` reported this task **open**, owner
`sound`, priority `85`. The instruction remains directionally correct: the old
experiment had only one negative night, while the live note3 capture and
archivist ledger now contain later quiet material. No code or gate was changed.

The current corpus read was 600 note3 ledger rows: 553 measurable and 47
`skip:silent-or-unreadable`. `mesh-series-stats --claims` was also run against
the live corpus; its standing claim output reports `note3 n=553` for the
current measured population. The command returned `claim-gate: rc=1` because
the unrelated standing sub-window claim remains refuted; that is not used as
evidence for this RMS result.

## Durable join

For each surviving `/home/mesh-home/.mesh/note3/ear-*.wav`, RMS was read from
`/home/mesh-home/.mesh/note3-ear.log`; the archivist key was recomputed with
the same `sha1sum | cut -c1-8` function as `mesh-records`, then matched to the
third field of `/home/mesh-home/.mesh/records.log`. The result below is the
durable receipt of the join: every listed negative row carries its archivist
hash, capture time, and RMS, while the extrema provide the positive-side
witnesses.

The snapshot joined 201 archived note3 captures. It contains two independent,
date-separated quiet cohorts:

| cohort | joined captures | lowest measurable RMS (archivist hash) | highest unmeasurable RMS (archivist hash) |
|---|---:|---|---|
| 2026-09-07 | 64 | 193.9 (`788bd959`) | 247.4 (`d63be99f`) |
| 2026-09-08 | 137 | 151.7 (`fc003d5d`) | 193.9 (`0d815465`) |

Unmeasurable rows in the hash join (time, archivist hash, RMS):

```text
2026-09-07_13:39  09c245a5  190.8
2026-09-07_13:49  ac4b1d26  140.2
2026-09-07_15:49  800381cb  110.4
2026-09-07_18:39  d63be99f  247.4
2026-09-07_19:09  500369fe  184.4
2026-09-07_19:39  67baade1  174.8
2026-09-07_21:09  f01be631  178.5
2026-09-07_22:09  cf4ba444  167.5
2026-09-07_23:29  b18cbfab  168.6
2026-09-07_23:39  e8601b4f  158.8
2026-09-07_23:59  4c46db01  138.0
2026-09-08_10:49  7b784b2d  186.9
2026-09-08_11:59  f4372e84  184.3
2026-09-08_12:59  da8c1fd5  112.9
2026-09-08_14:19  943985eb  192.7
2026-09-08_16:39  0d815465  193.9
2026-09-08_16:59  0a0d3f63  192.8
```

## Verdict

The original one-night clean gap (`unmeasurable <=174.0`, measurable
`>=186.1`) does **not** survive. On 2026-09-07 an unmeasurable 247.4 exceeds
the measurable minimum 193.9; on 2026-09-08 an unmeasurable 193.9 exceeds the
measurable minimum 151.7. The apparent boundary follows neither a stable room
floor nor a separable material boundary: it is a false threshold on this live
corpus.

Therefore no RMS capture gate is proposed. RMS remains useful as a recorded
diagnostic, but it is not a sufficient measurability predicate without another
independent axis (or a redesigned capture/measurer contract).

Verification performed:

```text
mesh-task status sound-experiments-20260908       # task still open
mesh-records --stats                              # live corpus: 1160 files, 2159 ledger lines
mesh-series-stats --claims                        # live note3 arm observed; rc=1 on unrelated claim 4
sha1sum <note3 wav> | cut -c1-8                  # same key function as mesh-records
```
