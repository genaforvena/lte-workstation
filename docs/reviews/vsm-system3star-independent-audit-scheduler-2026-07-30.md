# VSM System 3\* — the independent, out-of-band audit channel

**Live literature review · 2026-07-30 · second-order cybernetics → distributed sensor mesh**
Landed: `scripts/mesh-liveness-loop` (`cron_audit` / `cron_sessions_in_window`, `--audit-cron` task).

## The concept (named, cited)

Stafford Beer's **Viable System Model** routes System 1's health up to System 3 by **two** channels,
not one:

1. the **routine vertical command/reporting line** — S1 tells S3 how it is doing; and
2. **System 3\*** (three-star) — a **sporadic, out-of-band AUDIT** that samples ground truth by a
   channel **independent of the report**, "to ensure that System 1 management is not, either by
   accident or by design, pulling the wool over their eyes."

3\*'s two defining properties are **independence from the reporting line** and **aperiodic timing**.
Sources read for this review:

- Businessballs, *Stafford Beer's Viable System Model* — the S3\* audit-channel definition and the
  "pulling the wool over their eyes" gloss (businessballs.com/strategy-innovation/viable-system-model-stafford-beer/).
- IEEE ETHW, *The Viable System Model (VSM) of Stafford Beer* — 3\* as one of the model's named
  communication channels, distinct from the S2/S3 command axis.
- **Live 2026 sharpening** — why the *aperiodic* property is load-bearing, not decorative:
  - *Gaming the Metric, Not the Harm: Certifying Safety Audits against Strategic Platform
    Manipulation*, **arXiv:2605.06324** — a predictable audit certifies the *metric*, not the harm.
  - *A Benchmark for Strategic Auditee Gaming Under Continuous Compliance Monitoring*,
    **arXiv:2605.06340** — an auditee under a *known-schedule* monitor need only look healthy at the
    audit moment. Predictable audit ⇒ gameable/blind.

This is the general principle behind a specific failure the mesh keeps re-discovering by hand: *a
monitor that reads only the monitored thing's own self-report will believe a self-report that has
decoupled from reality* (the "`--test` forges the artifact it checks", "gate greps its own source",
"cron-green while stale" family in CLAUDE.md). Beer named the fix in 1972: an **independent** channel.

## Why it is NOT already embodied

`mesh-reflex-health` is a rich second-order watcher — it already carries observer self-suspicion
(Lifeguard), overwrite-vs-identification (mtime is agent-owned), facilitation-cascade fan-in, and the
refrain-openness gap. But **every one of those verdicts reads the reflex's OWN self-reported artifact**
(mtime, then content digest). That is precisely the S1→S3 **routine** channel. There is no 3\*: no
signal sampled by a path *independent* of the reflexes' own writes.

The gap this leaves is **common-mode** and it is the sharpest possible case of the second-order
regress *"who watches the top watcher?"*:

- The mesh runs **two** schedulers — **cron** (`reflexes.cron`, ~200 reflexes) and
  **`mesh-liveness-loop`** (systemd, `Restart=always`, **cron-independent**).
- The watchdog that would notice **cron dying** — `mesh-reflex-health` — **is itself a cron reflex**
  (`*/10`). So when cron dies, the watchdog **dies with it**. The single failure that stales *every*
  cron reflex at once produces **silence, not an alarm**.
- `mesh-reflex-health`'s own SELF-GROUNDING block already names this open problem: *"an INDEPENDENT
  tool grounding our freshness from OUTSIDE this loop … is the proposed next step."* **System 3\* is
  the doctrinal name for that step**, and Beer's independence requirement is exactly *why* it must
  live outside cron.

## The transfer (what shipped)

`mesh-liveness-loop` **is** that outside — systemd-supervised, it keeps running when cron is dead — so
Beer's 3\* audit belongs there. Auditing the *other* scheduler is the one liveness fact the cron side
structurally cannot establish for itself.

- **Independent signal.** The journal's PAM **cron-session** lines are authored by **cron/PAM, not by
  any reflex**. A node with ~200 crontab entries (many `*/2`–`*/15`) logs **thousands** of
  `cron:session` lines per window (2013 in 30 min, measured on mesh-home; 989 in 15 min at review
  time). Cron dead ⇒ **zero**. Zero is a **crisp, calibration-free** threshold — a live cron with that
  crontab *cannot* log zero sessions in 15 min, so there is no per-node rate model to rot.
- **Honest n/a.** If `journalctl -t CRON` is not readable at all (no journal access, or a node whose
  cron logs only to syslog), the audit **cannot** run → it stays **silent** (never a faked all-clear,
  never a false alarm). A **readability probe** separates *"channel unavailable"* (unauditable) from
  *"channel says zero"* (scheduler dead) — the `discarded-exit-code-renders-n/a-as-a-blank-row` trap.
- **Report-only, edge-triggered.** On a confirmed silence it posts one root-cause `[scheduler-dead]`
  board line (and `[scheduler-ok]` on recovery). It does **not** restart cron — substrate is
  single-writer, the mind's own hands.

Wired as a `scheduler-audit|600|mesh-liveness-loop --audit-cron` task in the loop's existing cadence
machinery. **RED-first tested** (`--test`): counts 2 sessions in a fixture, reads an empty channel as
`0 = scheduler-dead` (falsified by breaking the zero branch → state stays `OK` → FAIL), recovers to
`OK` on sessions present, and holds `OK` on an unreadable channel (honest n/a). Posting is suppressed
in `--test` (`MESH_AUDIT_NOPOST`) so the test never writes the real board.

## Distinctness

- **NOT** `mesh-reflex-health`'s freshness/overwrite/fan-in axes — those all read the reflex
  self-report on a fixed cron; this reads an **independent** channel about the **scheduler**.
- **NOT** `observer_impaired` (Lifeguard) — that qualifies a verdict with the **node's** health
  (load/OOM/deauth, from the *kernel* ring); this audits the **cron scheduler's** liveness (from the
  *CRON* facility). Sibling shape ("qualify with an independent read"), different axis.
- **NOT** a duplicate of `mesh-liveness-loop`'s own heartbeat — that proves *this* loop is alive;
  this proves the *other* scheduler is.

## Aperiodicity — the part deliberately held

The 2026 papers' second point (a *predictable* audit is gameable) is **partially** embodied and
partially open. The audit runs on a fixed `600s` task cadence, which is fine for the **non-adversarial**
common-mode failure it targets (cron does not strategically time its own death). Making the audit
sample *aperiodically* to defeat an adversarial auditee is a real further step, but the mesh has no
adversarial auditee today, so jittered timing would be gold-plating a threat that does not exist —
noted here so a future review lands it against a real adversary, not a hypothetical one.
