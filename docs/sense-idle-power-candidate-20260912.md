# Candidate relation instrument: package energy during CPU idle residency — 2026-09-12

Added the on-demand instrument `scripts/mesh-idle-power`. It measures package energy from RAPL and
per-CPU idle residency from cpuidle counters over the same one-second interval. Both axes must be
reachable, counters must advance, and every online CPU must have readable idle counters; otherwise
it exits 2. It reports the raw pair and coverage without thresholds or a human-facing verdict.

The candidate joint pattern is package energy while the cores are in deep idle. Package watts alone
do not say whether cores were resting; deep-idle residency alone does not say what the package drew.
The tool is an instrument only: the samples below do not calibrate a threshold or change any fusion
verdict. Existing `mesh-stress` relates C-state residency to low scheduler load, but does not combine
the RAPL energy axis with that residency in an aligned window.

The script is executable and available through `~/.local/bin/mesh-idle-power`. Its header declares
`orphan-ok` because there is no scheduled consumer or calibrated cadence. It writes no state file,
so change-gated liveness touching is not applicable.

Live evidence from `scripts/mesh-idle-power --test` at 2026-09-12T11:23:42Z:

```text
package_watts=80.061 cpu_idle_pct=57.68 cpu_deep_idle_pct=43.52
deep_share_of_idle_pct=75.45 window_ms=1000.1 cpu_coverage=16/16
```

Eight additional one-second windows from 11:23:53–11:24:00Z:

| package watts | CPU idle % | CPU deep-idle % |
|---:|---:|---:|
| 103.716 | 0.24 | 0.24 |
| 103.354 | 0.05 | 0.04 |
| 103.512 | 0.18 | 0.17 |
| 102.204 | 0.74 | 0.42 |
| 103.452 | 23.87 | 16.24 |
| 97.525 | 39.91 | 35.62 |
| 91.824 | 46.02 | 37.17 |
| 95.160 | 48.12 | 33.06 |

The axes vary in the same window, so the pair remains available for later corpus analysis. No
correlation or semantic claim is made from this short sample.

## Verification and publication gate

- Python AST parse — PASS.
- `scripts/mesh-idle-power --test` — PASS, including fixtures for parsing, pair math, missing CPU
  coverage, malformed/non-advancing counters, plus a real aligned hardware read. Final rerun at
  2026-09-12T11:27:46Z measured 89.736 W with 54.89% CPU idle, 46.77% deep idle, and 16/16 CPU
  coverage.
- `mesh-autowire --test` — PASS.
- Invocation through `~/.local/bin/mesh-idle-power --json` — PASS with 16/16 CPU coverage.
- Full `mesh-doctor --quiet` — returned “skipped” because another automated doctor held
  `~/.mesh/.doctor.lock`.
- Full interactive `timeout -k 5 240 mesh-doctor` — timed out with rc=124 before completion. Its live
  output reported FAIL for `egress rides tailscale0` and `exit-node set`, WARN for the default mic
  despite `plughw:1,0` capturing, and PASS for supervised loops, cron integrity, and tool parsing. It
  stopped after printing the source-executable check heading; no summary or orphan result for this
  candidate was produced. An automated invocation's log also contains a syntax error at line 4899;
  the current repository copy passes `bash -n scripts/mesh-doctor`. Therefore no `[sense]` board post
  was made; the publication gate remains unsatisfied.

At the time this candidate was first recorded, no commit was made and the publication gate remained
open because the doctor was locked/timed out. The completed gate and fresh verification are recorded
below.

## Publication gate completed — 2026-09-14

The pending doctor gate was rerun to completion from the repository root. `mesh-doctor` reported
`0 FAIL, 33 WARN` and exited 0. Its orphan census reported the same 94 confirmed orphans as before
(`orphans: 94 ... stable`), with no `+new` orphan delta; `mesh-idle-power` is intentionally on-demand
via its source `orphan-ok` header. The remaining WARNs are existing repository findings, including
the two long-standing orphan exemptions whose claimed callers are absent. No source or schedule edit
was needed, and nothing was committed.

Fresh live verification at 2026-09-14T15:01:24Z:

```text
mesh-idle-power --test: PASS
package_watts=101.255 cpu_idle_pct=0.41 cpu_deep_idle_pct=0.35
deep_share_of_idle_pct=86.56 window_ms=1000.1 cpu_coverage=16/16
mesh-idle-power --json at 2026-09-14T15:01:25Z: PASS, cpu_coverage=16/16
```

The `--test` includes fixture parsing/math, incomplete-CPU and malformed/non-advancing-counter
rejection, and the aligned live RAPL + cpuidle read. Source remains executable (`775`) and carries
the explicit on-demand `orphan-ok` declaration. Doctor's node-aware sweep reported all applicable
smoke checks passing.
