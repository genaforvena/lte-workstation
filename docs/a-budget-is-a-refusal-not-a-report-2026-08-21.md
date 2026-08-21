# A budget is a REFUSAL, not a report — and three ways the meter lies while it reports

Operator, 2026-08-21: *«имеет смысл ставить какой-то бюджет на вообще всё, задача потратить минимум»*
— and the binding half of it: *«цифры назначать только после суток измерения — потолок раньше
измерения это гадание»*.

Landed as `scripts/mesh-budget` (+ the gate wired into `mesh-cam-lock`, + the panel block in
`mesh-dash minds`). What follows is what the work actually taught, not a description of the tool.

## The premise was one-third wrong, and the wrong third was the expensive one to "fix"

The task named three uncapped axes. Measured against the current tree they were in three different
states, and building three new ceilings would have been the wrong move on one of them:

| axis | before | done |
|---|---|---|
| **frames** | nothing counted them at all. `grep -rlniE 'frames_per_hour\|frame_count\|MAX_FRAMES' scripts/` → empty. Five openers, each with its own cooldown, which bounds ONE organ's cadence and says nothing about the sum. | **built** — counted at `mesh-cam-lock`, the one chokepoint every local `/dev/video*` capture passes |
| **gpu** | counted, but only CUMULATIVELY (`mesh-gpu-ledger` reads the driver's post-mortem ring). A cumulative counter is not a rate, and the ring evicts, so it also goes DOWN. | **built** — sampled on cron, window delta'd, ring reset counted 0 and flagged |
| **paid** | **already capped, and better than the task assumed.** `MESH_LABOR_BUDGET_USD=900` per rolling 5h is armed in `~/.mesh/restore.env`; `mesh-labor` prices the window ($511/$900 = 57% while this was written) and `mesh-pace`'s hard-$-cap branch HOLDS every paced lane at spent≥cap, with a double-entry decision ledger and a named fail-open. | **delegated** — read-through only |

**A second authority over one axis is not a second safeguard; it is a race about which one gets
consulted.** `mesh-budget` therefore stores no paid cap at all — `budget.conf` deliberately has no
key for it, and `--test` GATE7b FAILS if one ever appears. `mesh-labor --propose-cap` stays the way
that number is revised.

## Blindness is not zero — and the renderer that says so is not the gate

`--test` GATE5 asserted that a gpu axis with no samples prints `na` on the panel. A mutant that made
the accumulator return **0** instead of `na` **survived it**: `fmt_axis` prints the literal `na` on
any non-zero rc, so the panel stayed honest while the accumulator underneath had started lying. The
same 0 came straight out of `--json`, where every machine consumer reads it.

> **A gate on a renderer's hardcoded string tests the renderer. Assert the value the ACCUMULATOR
> returned, in the surface that carries it raw.** GATE5 now asserts `"spent":null` in `--json`, and
> the mutant goes red.

This is the sibling of *non-empty-is-not-correct*: the display layer had exactly enough hardcoding
to keep looking right after the layer beneath it broke.

## One sample is not a measurement (found by a live read, not by the suite)

The first real `--status` after wiring printed `gpu 0.0 / unset(measuring 0.0h/24h)`. Every stub in
the suite was green. **A delta needs two points**, and with one in-window sample and no earlier
baseline the walk printed `sum=0` — which renders on a budget panel as *a ceiling with room under
it*, the most expensive possible reading of "we have not measured an interval yet". Now BLIND, with
GATE6b/6c asserting both directions (a lone sample is blind; a pair still measures).

## Two sample kinds on one tape: key on the FIELD NAME, not on the row kind

The worse one, and again found only by a live read. The ledger carries two sample kinds —
`sample gpu_ms=<n>` and `sample paid_usd=<n>` — and the delta walk matched `$2=="sample"` and then
split field 3 blindly. So a **$511.62 paid row was read as a GPU counter of 511**, differenced
against the real 10,808,842-ms counter, and the panel published **180.2 gpu-min derived from a dollar
figure**. Nothing about it looked wrong: the number was plausible, positive, and correctly formatted.

The suite could not catch it *by construction*: every stub ledger `--test` wrote held exactly one
kind of row, so the blind split was never given a heterogeneous tape to be wrong about.

> **When one append tape carries more than one row shape, a matcher keyed on the shared token is not
> a matcher.** Key on the field that identifies the kind. And write at least one fixture that
> INTERLEAVES the kinds — a single-kind fixture cannot fail this, which is why a green suite meant
> nothing here (GATE6e now does exactly that, and goes red on the un-keyed walk).

## The frames number says out loud that it is a lower bound

`mesh-cam-lock` covers the four openers that use it (`mesh-bruno-watch`, `mesh-eye`, `mesh-light`,
`mesh-misha-wake`). `mesh-cam-watch`, the iMac camera and the phone cameras do **not** pass through
it. A frames figure that did not declare this would be read as the node's whole frame spend and would
size the cap too low — so every render carries `LOWER BOUND: counts only captures routed through
mesh-cam-lock`, and GATE6d fails if that caveat is dropped.

## The sampler saw a different world than the shell that wired it

Two more, both found by reading the **live ledger** rather than the suite:

**The ceiling vanished on the sampler's own cadence.** `MESH_LABOR_BUDGET_USD=900` is armed in
`~/.mesh/restore.env` — which **cron does not source**. So the interactive run booked
`paid_cap=900` and the cron sample four minutes later booked `paid_cap=unset`, and the panel
alternated between *"$511 / $900 · 57%"* and *"report-only"* every five minutes. Nothing errored;
both rows were honest reports of what their process could see.

> **A reflex reads a smaller world than the shell you wired it from.** Any knob that lives in
> `restore.env` must be resolved BY THE TOOL when the environment lacks it (`mesh-pace:48` is the
> established idiom), and the gate must be driven with `env -u` against a stub file — otherwise it
> asserts the node's environment, not the resolution.

**One blind axis blinded the other.** `--sample` returned early on an unreadable GPU counter and
never reached the paid sample. A driver whose accounting mode had reset would therefore have
silently stopped the *$-cache* too, and the paid axis would have aged past its lease and read BLIND
for a reason with nothing to do with the labour meter — a fault in one organ presenting as a fault
in another. Each accumulator now books what it can testify to, independently.

(Also: `set -u` + `export PATH="$HOME/..."` placed one line ABOVE that same script's `HOME` fallback
kills the tool under any environment without HOME. The fallback existed; it was just unreachable.)

## Two shared-code notes

- **A 47s meter has no business in a gate.** `mesh-labor --json` measured **46.7s** on this node; the
  first version's 30s timeout turned a healthy meter into "BLIND". The paid axis now reads a cache
  that `--sample` books on its `3-59/5` cron, under a **900s lease = 3× the producer's cadence** — a
  lease shorter than its producer's period manufactures blindness between two healthy samples. Past
  the lease the row is not served as current: a stale $-figure wearing the live label is fabricated
  calm on the axis that costs actual money.
- **`grep -c` prints `0` AND exits 1**, so the idiomatic `|| echo 0` emits a *second* line. It split
  the status summary across two rows before anyone noticed the arithmetic was fine.

## What is deliberately NOT done

**No number is armed.** `FRAMES_PER_HOUR` and `GPU_MIN_PER_DAY` ship empty; the gate allows and
renders `unset(measuring Xh/24h)` — never ∞, never a guess. `--propose` REFUSES to name a number
until 24h of coverage exists (GATE9), then reports max×1.2 for the operator to arm by hand. The
counting that starts today is the whole point: it is what makes the cap measurable tomorrow.
