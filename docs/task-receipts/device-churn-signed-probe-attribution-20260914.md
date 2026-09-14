# Device-churn signed-probe attribution — 2026-09-14

Task: `device-churn-signed-probe-attribution-20260914/separate-signed-probe-events-from-device-churn`

## Change

`scripts/mesh-device-churn` now joins the udev stream to the exact counter interval
`(baseline_seq, current_seq]` for the current boot. It excludes only events carrying an exact
registered mesh-probe signature. Unsigned, kernel, foreign, unknown, conflicting, and missing
sequence events remain in the conservative `possible-nonprobe` upper bound. The raw seqnum delta
remains visible; neither burst size nor an observed-source ratio is used to classify an event.

The learned idle floor uses `possible-nonprobe` on attributed rows and retains the raw basis for
historical rows. The age-based USB candidate scan remains independent evidence and keeps its
conservative behavior. CHURN prose now describes elevated activity without asserting external
enumeration from a global counter alone. Attribution completeness and per-source counts are included
in the local row.

## Historical interval replay

The deployed attribution function replayed both retained intervals against
`/home/mesh-home/.mesh/udev-stream.log.1` plus `udev-stream.log`:

| Sequence interval | Raw delta | Observed | Signed probes | Unsigned | Missing/unknown | Possible non-probe |
|---|---:|---:|---|---:|---:|---:|
| `(10837, 10921]` | 84 | 84 | `mesh-devcd-catch:82`, `mesh-udev-stream:1` | 1 | 0 | 1 |
| `(10921, 11023]` | 102 | 84 | `mesh-devcd-catch:78`, `mesh-udev-stream:3` | 3 | 18 | 21 |

The second interval is partial. Its missing seqnums remain unknown:
`10924–10926`, `10931–10939`, `10948–10950`, and `10952–10954`. The 81 signed events are
attributed individually; the three unsigned events plus 18 missing events remain possible external
activity. The complete first interval likewise retains its single unsigned event. The fixture suite
checks that one unsigned event still crosses `MIN=1` with no learned floor.

## Verification

- `rtk bash scripts/mesh-device-churn --test`: pass, including complete and incomplete stream
  fixtures, unsigned-event retention, floor learning, and durable-artifact immutability.
- `rtk bash -n scripts/mesh-device-churn`: pass.
- `rtk proxy git diff --check -- scripts/mesh-device-churn`: pass.
- After landing, `rtk mesh-device-churn --test`: pass.
- Read-only live `rtk mesh-device-churn --check` at `2026-09-14T12:20:12Z`: exit 0,
  `QUIET delta=0`, `source-attribution=complete observed=0/0`, and `possible-nonprobe=0`.
- Source and installed-tool SHA-256 match:
  `d06a9d8519880400c4dee41f98615a49e8e00c03a139682e0b3851c207cf4d02`.
  The shared signature helper and installed helper also match:
  `c578ee938bd0209394ddd1972ffca895ae810f1f59749f54e50db902778b1b7a`.
- Before/after hashes around the live `--check` were identical:

| Artifact | SHA-256 |
|---|---|
| `.device-churn.baseline` | `bfd983261f46cec2fad9df743d44c7a37d16642e59d530091a1accba75e893df` |
| `.device-churn.state` | `75f8186f65941e5adaa8070ba89b19317c6be71209f2e98e997f62b8953957c6` |
| `device-churn.log` | `f1b2c33449d1afd57c3ec7e0ffeab0390d58b804edb6fc6d19db026a54cec5cd` |
| `.device-churn.posted` | `ee2b4e71a238c80529d4639ee31880a3a3167d418c6c3c49edbbde43f2541d80` |
| `.device-churn.tally` | `66f282e37d5156b2d1f89b9f696facbd690e231fe3afcf6007165e02c35c1895` |
| `udev-stream.log` | `f7de3633d5acdbc3700950f9b9436374c724a95d425dcd9252941d0cf45eff02` |
| `udev-stream.log.1` | `e7748ecc9b239528c515091dff9c5e7508dbf607110da52297de37d247172aa2` |
| `~/.mesh/reflexes.cron` | `bbca23da301a2b9a2e078ade7163de91fd3b9cad2d5cad712726ad48cf164fcb` |

The existing crontab line remains `*/5 * * * * $HOME/.local/bin/mesh-device-churn >>
$HOME/.mesh/device-churn.cron.log 2>&1 # autowired 2026-08-18`; no schedule or service change was
made. No radio, network, firewall, or external-device action was taken.

## Landing

MeshLand committed the source as `8b0f1565e4c1a325115839cbef72810e18daaa07` with subject
`Classify exact signed probes in device-churn while preserving unknown events`, then deployed it.
The source and installed path hashes above match.
