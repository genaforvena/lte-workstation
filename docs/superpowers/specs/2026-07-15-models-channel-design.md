# The `models` channel — which model each organ runs, and how fast

**Date:** 2026-07-15
**Operator ask:** "it would be great to know on which pane i can see models being used + their perf"
**Follow-up ask:** "make sure to persist this new window so that it wont be lost in case of another restart"

## Why this exists

The mesh has a **21-model shelf and no bench**. `ollama list` shows ~35GB pulled over 15h
(qwen3-vl:4b-instruct, gemma4:e2b-it-qat, granite4.1:3b, qwen3.5:{0.8b,2b,4b}, glimpse-v1, …);
**zero fixtures have been run against any of them**. The room mind named it at 08:19:

> "The gap is not candidates, it is MEASUREMENT: we have a shelf and no bench."

Exactly one measurement exists mesh-wide — room's 09:38 STT bench (GigaAM v2_ctc vs
whisper-large-v3-turbo-q5_0 vs whisper-tiny on the operator's own 08:12 ru ask) — and it lives
**only as prose** in a chat post and a memory file. It survived the 10:04 tmux restart by luck of
being written down, not by design.

Meanwhile the two adjacent surfaces do not answer the question:

- **`mesh-model-watch`** is a *vintage clock* (HF metadata → age drift). Its own banner refuses to
  judge quality: *"Anything here that starts ranking models by 'quality' from metadata is lying."*
- **`mesh-spend`** covers *mind* models only (claude/opencode/gemini, turns, paid-vs-free).

**Nothing covers the local inference organs.** There is no `models` dash role.

## The bug that defines the design

`mesh-model-watch:93-98` holds a **hardcoded** organ→incumbent map:

```python
"stt": ("openai/whisper-large-v3-turbo", "automatic-speech-recognition"),
```

Rendered live at 10:16 today it claimed `stt → openai/whisper-large-v3-turbo`. But
`mesh-room-transcribe.service` was stopped at 09:46 and **GigaAM** is the live STT organ. The tool
reported a model the organ no longer runs, with no way to notice.

This is the same family as the vacuous self-grep gates (f798133, 33 of 52) and
`[ -x "$BIN" ]`-is-not-"it runs" (974d864): **a declaration is never an observation.**

Therefore the governing rule: **the pane reports what it observed, or it says UNKNOWN. It never
carries a literal.**

## Scope (v1)

Local inference organs only — STT, TTS, vision, mind-small. Cloud mind models stay with
`mesh-spend`; the two halves have incompatible perf axes (wall-clock per inference vs turns per
mind) and conflating them is how a pane starts lying.

**Division of labour (operator, explicit):** this spec builds the **scaffolding + seed**. From
there the `models` window's own mind works **organ-by-organ, step by step**. v1 ships one organ
benched (STT — the only one with a fixture today); the rest are the mind's standing lane.

## Components

### 1. `mesh-model-resolve` — the observer

Answers, per organ: *which model would this organ load **right now**?* — by asking the organ's real
resolution path, never a map:

| organ | resolution path |
|---|---|
| stt | which unit is active (`mesh-room-gigaam` vs `mesh-room-transcribe`) + its `OH_MODEL` env; `mesh-voice-rx`'s `_best_model()` ladder |
| tts | `mesh-note3-say` → piper voice on disk (`voices/ruslan.onnx`) |
| vision | `mesh-face-recognize`'s ollama model name |
| mind-small | `mesh-relay`'s local fallback pool |

**Gate — UNKNOWN, never all-clear.** If the resolver cannot determine an organ's model, it renders
UNKNOWN and the pane shows UNKNOWN. It must never fall back to a declared default: that is the
exact bug being fixed, and a plausible-but-wrong model name is worse than an honest gap.

**Gate — an organ is not one model.** STT has ~8 consumers (`mesh-voice-rx`, `mesh-ear`,
`mesh-transcribe`, `mesh-transcribe-organ`, `mesh-conversation`, `mesh-phone-convo`,
`mesh-voice-gate`, the room ear). GigaAM replaced whisper in **exactly one** of them. The resolver
reports **per consumer**, not per organ class — collapsing them to a single "stt" row is what let
"we use GigaAM now" read as a stack change when it was a one-organ change.

### 2. `mesh-model-bench` — the bench

`mesh-model-bench <organ> <model> [--fixture <id>]` → runs one fixture against one candidate,
appends one ledger line.

Measures two axes, **both mandatory**:

- **wall-clock at a real duration** — never RTF. The `RTF 13.26` in `CLAUDE.local.md` was measured
  on a 3.36s clip where the ~11s fixed model load dwarfs inference, then extrapolated linearly:
  it predicted 795s for a 60s note; the real number is **27.9s**. 28x wrong. The tell was that the
  3.36s clip took *longer* than the 18s one.
- **accuracy against ground truth** — WER against the known transcript, computed mechanically.

**Gate — accuracy is not optional, and it is the load-bearing one.** A speed-only bench selects
**whisper-tiny**: 0.8s, and it returned *"Маш на тех, что спичка, спичка тех, что нужно тебя
кружчивать и субтитровать"* for *"Уши на текст-ту-спич и спич-ту-текст должны быть прямо крошечные
и суперские модели"*. Not a degraded read — **a different sentence**, fast. Any bench that ranks on
wall-clock alone confidently recommends the model that would have made the room deaf to the very
ask that started this work.

**Gate — `--test` drives a real model.** Not a stub. `mesh-whisper-run --test` drove
echobin/errbin/sleep stubs, asserted nice/ionice/flock/admission all green, and never once invoked
whisper — while whisper died rc=127 on every real call for a day (974d864). Exit 2 where the organ
or model is genuinely absent (honest n/a; `mesh-land` treats it as a pass), never a fake green.

**Gate — fixtures must be the right organ.** Do **not** build fixtures from
`~/.mesh/records/*-ear-*.wav` blindly: the room ear recorded the **USB camera's 197-RMS self-noise
floor** for 8h (09:56 finding), so most of that corpus is hiss, not room audio. A bench against
those wavs measures nothing. Fixtures need a stated provenance and a known ground truth.

### 3. Fixtures — `~/.mesh/model-fixtures/`

A fixture is **a pair**: the input artifact + its ground truth, side by side. Ground truth living in
a chat post or a mind's head is how room's bench became unreproducible the moment the pane scrolled.

```
~/.mesh/model-fixtures/stt-ru-operator-0812/
  input.wav          # copied from ~/.mesh/records/20260715-081205-ear-14452194.wav
  truth.txt          # "Уши на текст-ту-спич и спич-ту-текст должны быть прямо крошечные и суперские модели"
  provenance.txt     # operator's own voice, 08:12Z 2026-07-15, ear capture kept by mesh-records
```

Copied, not referenced: `~/.mesh/records/` is pruned by its organ, and the whole reason this
fixture exists is that `mesh-records` rescued it from exactly that. A fixture that can be pruned is
not a fixture.

### 4. `~/.mesh/model-bench.log` — the ledger

Append-only. One line per `(ts, organ, consumer, model, fixture, wall_clock_s, fixture_dur_s, wer, verdict)`.

**It outlives the models.** Same principle that saved this work already: `mesh-records` kept the
operator's 08:12 fixture (`20260715-081205/081223-ear-*.wav`) *after the ear pruned it*, which is
the only reason a bench was possible at all. The ledger is the durable tier; a model on disk is not.

### 5. `mesh-dash models` — the pane

Per consumer: **live model** (resolve) · **measured perf** (ledger) · **candidates benched vs
unmeasured** (ledger ∩ shelf).

**Gate — UNMEASURED renders UNMEASURED.** Never `0`, never `-`, never a plausible constant. A
default that is indistinguishable from a real measurement will become one. The pane's job includes
showing how much of the 21-model shelf is *still unmeasured* — that number is the lane's backlog and
should be visible, not implied.

Throttle: resolve is a cheap local read; the ledger is a file tail. Standard 30s `SLEEP` (per
`mesh-dash:67`). No HF API calls in the refresh loop — `mesh-model-watch` keeps its own cadence and
the pane reads its cached `~/.mesh/model-watch.json` if it shows vintage at all.

### 6. Seed — re-run, do not transcribe

The pane needs real rows on day one. **Produce them by running `mesh-model-bench` against the
`stt-ru-operator-0812` fixture for all three candidates** — not by pasting room's numbers into the
ledger.

Room's 09:38 figures are the **expectation**, not the seed:

| model | chunk 1 | chunk 2 | room's accuracy call |
|---|---|---|---|
| whisper ggml-tiny | 0.8s | 1.0s | WRONG SENTENCE — unusable for ru |
| whisper large-v3-turbo-q5_0 | 11.7s | 16.4s | accurate, punctuated |
| gigaam v2_ctc (GPU) | 0.7s | 0.1s | accurate (lowercase, no punct — CTC) |

Two reasons the re-run is the point, not pedantry:

1. **Those accuracy calls are eyeball verdicts, not WER.** The ledger's `wer` column is mechanical.
   Backfilling prose into a numeric column either invents numbers or leaves a hole that renders as a
   default — the exact failure the pane's UNMEASURED gate exists to prevent.
2. **The re-run is the bench's first real test.** If `mesh-model-bench` reproduces room's numbers on
   room's fixture, the tool is trustworthy and its `--test` is honest. If it does not, we learn that
   *now* — before the mind spends four organs' worth of work on a broken instrument. This is the
   whole `--test`-must-drive-the-real-thing rule (974d864) applied to the bench itself.

CTC output is lowercase and unpunctuated by design; the WER scorer must normalise case and
punctuation before scoring, or GigaAM takes a fake penalty against a punctuated reference and the
bench recommends whisper on an artifact of formatting.

## Persistence (operator's explicit ask)

The 10:04 restart cost the minds their scrollback. A window created ad-hoc in tmux is lost the same
way. Persistence is **not** "create the window" — it is a chain, and every link must hold:

1. **`scripts/mesh-restore`** — add to the UNIFORM SESSION MANIFEST:
   - `ensure_uniform_channel models models opencode "${MESH_MODELS_CMD:-${MESH_OPENCODE_CMD:-opencode}}"`
   - a `models)` case arm in `mcp_full_for_win` (`:63-75`) — the smoke-test at `:146` asserts every
     manifest channel has one (a real gate: falsify by dropping the arm)
   - add `models` to that smoke-test loop
   - update the `13-channel set` echo at `:448` → 14
2. **Deploy** — `cp scripts/mesh-* ~/.local/bin/`. `mesh-restore` runs from `~/.local/bin`, not the
   genome; editing `scripts/` alone changes nothing that runs.
3. **Reboot survival** — `@reboot mesh-restore` is already in cron, so (1)+(2) inherit it. No new
   wiring needed; verify it is still there rather than assuming.
4. **Commit AND PUSH.** Not optional and not automatic: **55 commits sat local for 11h** because
   every push path was conditional on that run having work to land (1969a5d). Unpushed = lost to
   every other node and to any reincarnation of this one.

**Engine: opencode (free).** Accuracy scoring is mechanical (WER against ground truth), not a
judgment call, so the lane does not need a paid reasoner. This also keeps a 15th window from adding
paid quota.

### The persistence artifact (the actual test)

**Kill the `models` window → run `mesh-restore` → assert the window returns with both panes, top
running `mesh-dash models`.**

Not `grep -q 'models' scripts/mesh-restore`. That is precisely the vacuous self-grep class swept
today: 33 of 52 such gates match **the grep line itself** and can never fail — deleting `mesh-land`'s
entire self-heal push still yielded `smoke-test: ok` (f798133). Source text is never behaviour. Drive
the real replant and assert the real window.

## Non-goals

- Ranking models by metadata — `mesh-model-watch`'s banner is right; that is lying. This lane ranks
  by **measurement or not at all**.
- Cloud mind models — `mesh-spend` owns them.
- Auto-swapping an organ's model on a bench result. The bench **proposes**; a mind judges and a
  human-visible change lands as a commit. GigaAM replaced whisper in the room ear via a deliberate,
  announced, rollback-ready window (09:46) — that is the pattern, not an automatic ratchet.
- Benching all four organs in v1. Only STT has a fixture with ground truth today. Vision needs a
  re-aimed camera (bruno's one operator label was a NEGATIVE — the cat was not in frame, the camera
  pointed at a shelf); TTS needs a homograph judge; mind-small overlaps the existing alem bench.

## Open questions for the `models` mind (its standing lane, in order)

1. **STT — settle whisper-vs-gigaam across all ~8 consumers.** Only the room ear was swapped. Is
   `mesh-voice-rx`'s base-on-CPU choice still right now that the 795s number is dead? (room flagged
   this at 09:38; owner `mesh-voice-rx/senses`, unresolved.)
2. **Vision — moondream (28mo) vs qwen3-vl:4b-instruct (pulled, 3.3GB, unmeasured).** Blocked on
   ground truth, not on candidates. Note: no decommission decision exists for moondream —
   `discover` at 04:47 explicitly *declined* to replace it absent evidence it is failing.
3. **TTS — piper (37mo) vs Qwen3-TTS-0.6B / VoxCPM2.** tg holds the homograph work; do not duplicate.
4. **mind-small — the relay fallback pool.** Coordinate with alem's matrix rather than re-running it.
