# VSM scheduler audit — 2026-09-12

Task: `design-spec-task-sweep-20260907/audit-vsm-scheduler` (owner `tg`). The assigned path
`docs/vsm-system3star-independent-audit-scheduler-2026-07-30.md` is missing its `reviews/` directory;
the source reviewed is
[`docs/reviews/vsm-system3star-independent-audit-scheduler-2026-07-30.md`](reviews/vsm-system3star-independent-audit-scheduler-2026-07-30.md).

## Disposition

The task was live and correct as an audit request. The July design still accurately describes the
independent **cron scheduler-liveness** audit. Its wiring exists in source and is running. A later,
separate S3* **correctness** auditor has also been added, with randomized delay and target selection;
the running supervisor process has not loaded that newer task-table row. The code is deployed, but
this second path is currently absent from live scheduling. A repair task is open as
`vsm-scheduler-runtime-followup-20260912/reload-liveness-loop`.

No scheduler or service was changed during this audit.

## Design compared with current wiring

| Channel | Design and current implementation | Current disposition |
|---|---|---|
| Cron scheduler liveness (the July 30 design) | `mesh-liveness-loop --audit-cron` counts cron/PAM-authored `cron:session` journal rows over 900 seconds. It treats an unreadable channel and a boot-truncated window as honest `n/a`, records `DEAD`/`OK` edges, and reports without restarting cron. `scheduler-audit|600|mesh-liveness-loop --audit-cron` remains in the supervisor task table. | Implemented and live. At inspection, `scheduler-audit=1789192758` (05:59:18Z), `.cron-audit.state` was `OK`, and the journal had 1,529 `cron:session` rows in the last 15 minutes. The user `mesh-liveness-loop.service` was active with `Restart=always`; its current main process was PID 2074. |
| Reflex-value correctness (the separate `mesh-audit` path) | `mesh-audit` independently checks raw organ state against emitted reflex state; its current registry contains only `therm`. `mesh-audit-reflex` persists a random 300–900 second next deadline and escalates divergence/errors to the health-warning path. Current source adds `audit-reflex|300|mesh-audit-reflex` to the always-on supervisor task table. | **Source-wired, runtime-missing.** `mesh-liveness-loop.service` has been active since 2026-09-09 13:51:59Z, while `scripts/mesh-liveness-loop` was modified 2026-09-11 19:52:39Z. The live `.liveness-loop.state` contains `scheduler-audit` but no `audit-reflex`, and `~/.mesh/.audit-reflex-state` is absent. The long-running Bash process has not reloaded the table added after its start. |

The two channels have different subjects and cadences. The 600-second cron-session check detects a
common-mode cron failure and remains fixed because the design's stated threat is non-adversarial.
The newer correctness spot-check addresses a potentially gameable value report, so its wrapper
jitters the due time and `mesh-audit` selects one registered target randomly. The jittered path does
not replace the independent cron-session audit; both rows are required in the current source table.

## Absent-component dispositions

- **Live runtime for the newer `audit-reflex` row:** genuinely absent at inspection despite source
  and symlink deployment. Follow-up chain
  `vsm-scheduler-runtime-followup-20260912` has one open `tg` step to refresh the supervisor and
  verify the process, deadline, task-state row, and continued scheduler-audit operation. Do not count
  source presence or the prior 2026-09-11 manual invocation as current runtime proof.
- **Thermal organ on this node:** absent. `mesh-audit` currently returns exit 2 with
  `NA (no readable thermal_zone*/temp — organ absent)`, which is the designed honest-n/a path, not a
  pass. `mesh-audit --test` reports that no thermal organ exists here.
- **Auditors for other organs:** not registered; `REGISTRY` currently contains only `therm`. The
  script labels this a proof-of-concept/extension surface. No broader sensor coverage is claimed by
  this scheduler design; any future organ audit needs its own registered auditor and real-read
  evidence.
- **Journal/syslog fallback:** absent by design. If the CRON journal facility cannot be read, the
  cron-liveness audit stays silent as `n/a` rather than guessing that zero sessions means cron died.
- **Scheduled `mesh-audit --all` sweep:** absent by design; random one-target spot-checks are the
  recurring path, and `--all` remains an explicit reconciliation command.

The source/deployment parity checks passed: `~/.local/bin/mesh-liveness-loop`,
`~/.local/bin/mesh-audit-reflex`, and `~/.local/bin/mesh-audit` resolve to repository scripts and
their hashes match their respective source files. This proves installed code, not that a long-lived
process has reloaded it; the missing task-state/deadline evidence above is why the runtime follow-up
remains open.

## Verification

- `mesh-task status design-spec-task-sweep-20260907`: task was open (24/25); exact dispatch check
  for `audit-vsm-scheduler`/`tg` exited 0; owner take succeeded.
- `scripts/mesh-liveness-loop --test`: PASS (15 task rows and scheduler-audit boot/n/a/dead/recovery
  cases). It ran with a temporary `HOME` and isolated `.mesh`; an initial harness attempt omitted
  that directory and failed at its state-file setup, then passed after correcting the harness.
- `scripts/mesh-audit-reflex --test`: PASS (persisted jitter state, divergence signal, immediate
  health conversion).
- `scripts/mesh-audit --test`: honest no-organ result; no readable thermal zone on this node.
- Live `scripts/mesh-audit`: exit 2, `NA (no readable thermal_zone*/temp — organ absent)`.
- `systemctl --user is-active mesh-liveness-loop.service`: `active`; `Restart=always`; source and
  deployed hashes match. The active process predates the current source by over two days.
- Live audit snapshot: 1,529 cron-session journal rows in the 15-minute window; supervisor state
  has `scheduler-audit=1789192758` and no `audit-reflex`; cron audit state `OK`; no
  `~/.mesh/.audit-reflex-state` file.

## Next action

Take `vsm-scheduler-runtime-followup-20260912/reload-liveness-loop`, refresh the running supervisor
from the current source under the normal service lifecycle, then verify its process start, an
`audit-reflex` task-state entry and jitter deadline, and that `scheduler-audit` continues advancing.
