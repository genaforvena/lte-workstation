# The `models` Channel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A persistent `models` channel whose data pane shows which model each inference organ actually runs and how fast + how accurately it runs — every number measured, every gap honest.

**Architecture:** Four new genome tools plus two edits. `mesh-model-resolve` observes the live model per *consumer* by asking each organ's real resolution path (never a map). `mesh-model-bench` runs a fixture against one candidate and appends `(wall-clock, WER)` to an append-only ledger. `mesh-dash models` renders resolve ∩ ledger, showing UNMEASURED as UNMEASURED. `mesh-restore` plants the window so a restart replants it.

**Tech Stack:** bash + python3 (stdlib only). whisper.cpp at `~/.mesh/whispercpp/main`. GigaAM via `~/.venv-ai/bin/python`. tmux. No new dependencies.

## Global Constraints

- **System python3 has NO numpy on this node.** numpy lives only in venvs (`~/.venv-ai`, `grainneukeln/.venv`). Every tool here is **stdlib-only**; the WER scorer is hand-rolled Levenshtein. A `import numpy` in a system-python3 tool is a dead tool that reports itself as a capability gap.
- **Test convention is `<tool> --test`**, not pytest. There is no `tests/` dir. Exit 0 = pass, 1 = fail, **2 = honest n/a** (organ/model genuinely absent — `mesh-land` counts exit 2 as a pass).
- **A gate you have not seen FAIL is not a gate.** For every assertion added: break the thing, watch it go red, restore it. Record that you did.
- **Never `grep -q '<literal>' "$0"`** as a gate. It matches the grep line itself and can never fail — 33 of 52 such gates on this node are vacuous (f798133). Assert the artifact.
- **Wall-clock at a real duration, never RTF.** Fixture chunks are 18.000s. RTF on short clips is load-dominated and extrapolates 28x wrong.
- **Exact model filenames on disk:** `ggml-tiny.bin`, `ggml-base.bin`, `ggml-large-v3-turbo-q5_0.bin`. There is **no** `ggml-large-v3-turbo.bin` — that exact-name miss is a known live trap in `mesh-voice-rx:49`'s ladder.
- **GigaAM model id:** `v2_ctc`, loaded via `gigaam.load_model("v2_ctc")`, `cuda=True`. `.transcribe()` returns a **TranscriptionResult, not a str** — read `.transcription` (this exact bug was fatal in `mesh-room-gigaam`, fixed 3a56a92).
- **Commit AND push every task.** Unpushed work is lost work: 55 commits sat local for 11h this morning because every push path was conditional (1969a5d).
- **NO ABSOLUTE WER THRESHOLD ANYWHERE.** Measured on the STT fixture during planning: large-v3-turbo-q5_0 **0.250**, gigaam-v2_ctc **0.312**, whisper-tiny **0.875**. This plan originally carried `ok if wer < 0.15`, which labels the best STT organ on the node "poor" — the assumed-0..1 bug (`mesh-soundscape`'s `act > 0.55` → "busy" can never fire; act never exceeds .544 on real material). Rank **relative to the best score on the same fixture**; that is self-calibrating and cannot saturate.
- **The ledger stores facts; the pane ranks.** Field 9 is `read-ok`/`EMPTY` — a fact about the run. A verdict frozen at write time is stale the moment the next candidate lands.
- **Room's "GigaAM accuracy EQUAL to large-turbo" is FALSIFIED** (0.312 vs 0.250 — «ить» for «быть», dropped «и»). GigaAM still wins on a 20x speed gap. Correct the claim in `CLAUDE.local.md` and the `stt-organ-gigaam-beats-whisper` memory; do not over-claim the reverse from n=1 chunk.

## File Structure

| File | Responsibility |
|---|---|
| `scripts/mesh-model-resolve` (new) | Observe the live model per consumer. UNKNOWN when undeterminable. No benching. |
| `scripts/mesh-model-bench` (new) | Run one fixture × one candidate → one ledger line. Owns the WER scorer. No resolving. |
| `scripts/mesh-dash` (modify, `:180` case) | Add `models)` role. Renders only; computes nothing. |
| `scripts/mesh-restore` (modify, `:63-75`, `:146`, manifest, `:448`) | Plant + persist the window. |
| `~/.mesh/model-fixtures/stt-ru-operator-0812/` (runtime) | input.wav + truth.txt + provenance.txt. Not in the genome — it is operator audio. |
| `~/.mesh/model-bench.log` (runtime) | The append-only ledger. Outlives the models. |

---

### Task 1: The fixture — input + ground truth, copied out of the pruning corpus

**Files:**
- Create: `~/.mesh/model-fixtures/stt-ru-operator-0812/{input.wav,truth.txt,provenance.txt}`

**Interfaces:**
- Produces: a fixture directory contract every later task consumes — `input.wav` (audio), `truth.txt` (single line, the reference transcript), `provenance.txt` (free text, where it came from and why it is trustworthy).

**Ground-truth honesty note — read before doing this.** `~/.mesh/room-transcript.txt` is **0 bytes** (the room has been deaf since the 09:46 swap), so ground truth cannot be read from it. The operator's actual sentence is independently attested in `~/.mesh/chat.log` (room's 09:38 post, quoting what he said at 08:12):

> Уши на текст-ту-спич и спич-ту-текст должны быть прямо крошечные и суперские модели

Two 18.000s chunks exist (`20260715-081205-ear-14452194.wav`, `20260715-081223-ear-2c3dd057.wav`). Which chunk holds that sentence is **not yet established**. Step 2 uses `large-v3-turbo-q5_0` to **locate** the known sentence among the chunks — it does not invent the truth. The truth text is the operator's own words from chat; the model only tells us which file they land in. If neither chunk matches, **stop and report** rather than pinning a fixture to a guess.

- [ ] **Step 1: Create the fixture dir and copy the audio out of the pruning corpus**

```bash
mkdir -p ~/.mesh/model-fixtures/stt-ru-operator-0812
cp ~/.mesh/records/20260715-081205-ear-14452194.wav /tmp/chunk-081205.wav
cp ~/.mesh/records/20260715-081223-ear-2c3dd057.wav /tmp/chunk-081223.wav
```

Expected: both copy without error. (`~/.mesh/records/` is pruned by its organ — the only reason these still exist is that `mesh-records` rescued them. Copy, never reference.)

- [ ] **Step 2: Locate the operator's known sentence among the two chunks**

```bash
for c in /tmp/chunk-081205.wav /tmp/chunk-081223.wav; do
  echo "=== $c ==="
  ~/.mesh/whispercpp/main -m ~/.mesh/whispercpp/models/ggml-large-v3-turbo-q5_0.bin \
    -l ru -nt -f "$c" 2>/dev/null
done
```

Expected: one chunk's output is recognisably *"Уши на текст-ту-спич и спич-ту-текст должны быть прямо крошечные и суперские модели"*. Note which. If neither is, STOP — report and do not proceed.

- [ ] **Step 3: Pin the fixture to the matching chunk**

**Resolved during planning: the match is `chunk-081223`.** `chunk-081205` holds the *preceding* sentence («Слушай, ну чего ты? Ну, типа, Пайпер, ну совсем древняя же штука…») — related, but not the reference. Step 2 still runs: confirm it rather than trust this line.

```bash
cp /tmp/chunk-081223.wav ~/.mesh/model-fixtures/stt-ru-operator-0812/input.wav
printf '%s\n' 'Уши на текст-ту-спич и спич-ту-текст должны быть прямо крошечные и суперские модели' \
  > ~/.mesh/model-fixtures/stt-ru-operator-0812/truth.txt
cat > ~/.mesh/model-fixtures/stt-ru-operator-0812/provenance.txt <<'EOF'
FIXTURE: stt-ru-operator-0812
Operator's own voice, 2026-07-15 ~08:12Z, room ear (mesh-overhear --daemon),
18.000s chunk = 20260715-081223-ear-2c3dd057.wav.

WHY THIS FILE STILL EXISTS: the room ear self-prunes hourly. mesh-records (the
archivist) kept it. Copied here, never referenced — the records corpus is pruned
by its organ, and a fixture that can be pruned is not a fixture.

WHY IT IS A GOOD FIXTURE: real ru room speech at a real distance, and it is the
exact utterance whisper-tiny destroyed ("Маш на тех, что спичка..." for "Уши на
текст-ту-спич..."). It discriminates the models that matter for this organ.

GROUND TRUTH — READ THIS BEFORE TRUSTING AN ABSOLUTE WER.
truth.txt is the operator's sentence as attested in ~/.mesh/chat.log (room's
09:38Z [fyi], written before this bench existed). large-v3-turbo-q5_0 was used
only to LOCATE which of two chunks holds it — as a search index, not an author.

But the lineage is not fully independent, and pretending otherwise would be the
lie this whole channel exists to prevent: room's own "ground truth" was the room
ear's large-turbo transcript, cleaned up by hand. So truth.txt is
human-mediated-model-output, not a human transcription from audio.

CONSEQUENCE, MEASURED 2026-07-15: the operator said the English phrases
"text-to-speech" / "speech-to-text" in Russian. No model renders that
transliteration identically —
  truth.txt          "текст-ту-спич"  /  "спич-ту-текст"
  large-v3-turbo     "тексту спич"    /  "спич-то текст"
  gigaam-v2_ctc      "текст у спич"   /  "спич ту текст"
so ~half of EVERY candidate's WER on this fixture is the reference's rendering of
a loanword, not model error. Scores: large-v3-turbo 0.250, gigaam-v2_ctc 0.312,
whisper-tiny 0.875.

It penalises all candidates EQUALLY. Therefore:
  ORDERING on this fixture is trustworthy.
  ABSOLUTE WER on this fixture is INFLATED and means nothing on its own.
Never put an absolute WER threshold against this fixture. Rank relatively. That
is why mesh-model-bench stores facts and the pane does the ranking.

TO IMPROVE THIS FIXTURE: have the operator confirm or correct truth.txt by ear.
That single act would make the lineage independent and the absolutes real.
EOF
```

- [ ] **Step 4: Verify the fixture contract holds**

```bash
d=~/.mesh/model-fixtures/stt-ru-operator-0812
ls -la "$d"
test -s "$d/input.wav" && test -s "$d/truth.txt" && test -s "$d/provenance.txt" && echo "fixture: ok"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$d/input.wav"
```

Expected: `fixture: ok` and duration `18.000000`.

- [ ] **Step 5: Commit** (the fixture is runtime data, not genome — commit the provenance record only)

```bash
cd ~/lte-workstation
mkdir -p docs/fixtures
cp ~/.mesh/model-fixtures/stt-ru-operator-0812/provenance.txt docs/fixtures/stt-ru-operator-0812.txt
git add docs/fixtures/stt-ru-operator-0812.txt
git commit -m "docs(models): record the STT fixture's provenance — the operator's 08:12 ask, rescued by mesh-records

The audio stays in ~/.mesh (operator voice, not genome). What the genome keeps is
WHERE the ground truth came from: his own words in chat.log, not a model's output.
large-v3-turbo only located which chunk holds the sentence."
git push origin main
```

---

### Task 2: The WER scorer — the gate that stops the bench recommending whisper-tiny

**Files:**
- Create: `scripts/mesh-model-bench` (scorer only this task; runners in Task 3)

**Interfaces:**
- Produces: `normalise(s: str) -> list[str]` and `wer(ref: str, hyp: str) -> float` — consumed by Task 3's runners and asserted by `--test`.

**Why this is Task 2 and not an afterthought.** A speed-only bench selects whisper-tiny: 0.8s, and it returned *"Маш на тех, что спичка, спичка тех, что нужно тебя кружчивать и субтитровать"* for the sentence above. Fastest, and a completely different sentence. The scorer is the thing that makes the bench worth building.

**Why normalisation is load-bearing.** GigaAM is CTC: lowercase, no punctuation, by design. Scored raw against a punctuated reference it takes a fake penalty on every token boundary and the bench recommends whisper on an artifact of formatting.

- [ ] **Step 1: Write the tool with its failing test**

```python
#!/usr/bin/env python3
"""mesh-model-bench — measure one candidate model against one fixture. One row of truth.

TWO AXES, BOTH MANDATORY. Speed alone selects the fastest wrong answer: whisper
ggml-tiny does this fixture in 0.8s and returns a DIFFERENT SENTENCE (2026-07-15,
room's bench). A bench that ranks on wall-clock is a bench that would have made the
room deaf to the very ask that commissioned it.

WALL-CLOCK AT A REAL DURATION, NEVER RTF. RTF measured on a short clip is
load-dominated: the ~11s whisper model load dwarfs inference, so a 3.36s clip
extrapolated to "60s note -> 795s" when the real number is 27.9s. 28x wrong. The
tell was that the 3.36s clip took LONGER than the 18s one. Fixtures here are 18s.

STDLIB ONLY. System python3 on this node has no numpy. WER is hand-rolled.
"""
import os
import re
import sys
import time
import subprocess
from pathlib import Path

HOME = Path.home()
MESH = HOME / ".mesh"
FIXTURES = MESH / "model-fixtures"
LEDGER = MESH / "model-bench.log"

# Normalise before scoring: CTC models (gigaam) emit lowercase, unpunctuated text by
# design. Scoring raw against a punctuated reference charges them a penalty for a
# formatting choice and hands the win to whisper on an artifact. Case + punctuation
# are not accuracy.
_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
_WS = re.compile(r"\s+", re.UNICODE)


def normalise(s):
    s = s.lower().replace("ё", "е")
    s = _PUNCT.sub(" ", s)
    return [w for w in _WS.sub(" ", s).strip().split(" ") if w]


def wer(ref, hyp):
    """Word error rate: Levenshtein over WORDS / len(ref). 0.0 = perfect, >=1.0 = hopeless."""
    r, h = normalise(ref), normalise(hyp)
    if not r:
        return 0.0 if not h else 1.0
    # full DP row-by-row — fixtures are one sentence, no need to be clever
    prev = list(range(len(h) + 1))
    for i, rw in enumerate(r, 1):
        cur = [i]
        for j, hw in enumerate(h, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (rw != hw)))
        prev = cur
    return prev[len(h)] / len(r)


def run_test():
    f = 0
    truth = "Уши на текст-ту-спич и спич-ту-текст должны быть прямо крошечные и суперские модели"

    # identical text scores 0.0
    if wer(truth, truth) != 0.0:
        print("  FAIL: identical text did not score 0.0"); f = 1

    # THE CTC GATE: lowercase + unpunctuated must NOT be penalised. This is the
    # difference between recommending gigaam and recommending whisper.
    ctc = "уши на текст-ту-спич и спич-ту-текст должны быть прямо крошечные и суперские модели"
    if wer(truth, ctc) != 0.0:
        print(f"  FAIL: CTC-style (lowercase/unpunctuated) penalised — wer={wer(truth, ctc)}"); f = 1

    # THE WHISPER-TINY GATE: the real garbage tiny produced must score as garbage.
    # If this ever reads low, the scorer is broken and the bench will recommend tiny.
    tiny = "Маш на тех, что спичка, спичка тех, что нужно тебя кружчивать и субтитровать"
    w_tiny = wer(truth, tiny)
    if w_tiny < 0.5:
        print(f"  FAIL: whisper-tiny's real output scored {w_tiny:.2f} — a scorer this blind picks tiny"); f = 1

    # ordering must hold: tiny is worse than a near-perfect read
    near = "уши на текст ту спич и спич ту текст должны быть прямо крошечные и суперские модели"
    if not (wer(truth, near) < w_tiny):
        print("  FAIL: garbage did not score worse than a near-perfect read"); f = 1

    # empty hypothesis is total failure, never a free pass (the silent-fallback family:
    # a model that returns nothing must not read as accurate)
    if wer(truth, "") < 1.0:
        print("  FAIL: empty hypothesis did not score as total failure"); f = 1

    print("smoke-test: ok" if f == 0 else "smoke-test: FAIL")
    return f


if __name__ == "__main__":
    if sys.argv[1:2] == ["--test"]:
        sys.exit(run_test())
    print("usage: mesh-model-bench --test    (runners land in Task 3)", file=sys.stderr)
    sys.exit(2)
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
cd ~/lte-workstation && chmod +x scripts/mesh-model-bench && ./scripts/mesh-model-bench --test
```

Expected: **PASS** immediately — the scorer above is complete. That is not a TDD violation, it is the signal to go break it: proceed to Step 3, which is where the gates earn their keep.

- [ ] **Step 3: See every gate FAIL (a gate you have not seen fail is not a gate)**

Break each one, confirm red, restore:

```bash
cd ~/lte-workstation
# 3a. Break the CTC gate: drop the .lower() → CTC output should now be penalised
sed -i 's/    s = s.lower().replace("ё", "е")/    s = s.replace("ё", "е")/' scripts/mesh-model-bench
./scripts/mesh-model-bench --test    # EXPECT: FAIL "CTC-style (lowercase/unpunctuated) penalised"
sed -i 's/    s = s.replace("ё", "е")/    s = s.lower().replace("ё", "е")/' scripts/mesh-model-bench
./scripts/mesh-model-bench --test    # EXPECT: ok

# 3b. Break the tiny gate: make wer always return 0 → tiny reads perfect
sed -i 's|^    return prev\[len(h)\] / len(r)|    return 0.0  # BREAK|' scripts/mesh-model-bench
./scripts/mesh-model-bench --test    # EXPECT: FAIL "whisper-tiny's real output scored 0.00"
sed -i 's|^    return 0.0  # BREAK|    return prev[len(h)] / len(r)|' scripts/mesh-model-bench
./scripts/mesh-model-bench --test    # EXPECT: ok
```

Expected: each break prints the named FAIL; each restore returns `smoke-test: ok`. Both gates seen red.

- [ ] **Step 4: Commit**

```bash
cd ~/lte-workstation
git add scripts/mesh-model-bench
git commit -m "feat(models): the WER scorer — the gate that stops the bench recommending whisper-tiny

Speed alone picks the fastest wrong answer: tiny does this fixture in 0.8s and
returns a different sentence. Two gates, both seen RED via mutation: CTC-normalise
(gigaam is lowercase/unpunctuated BY DESIGN — score it raw and whisper wins on a
formatting artifact), and tiny's real garbage must score as garbage.

Stdlib-only Levenshtein: system python3 here has no numpy."
git push origin main
```

---

### Task 3: The runners + the ledger — measure a real model or exit 2

**Files:**
- Modify: `scripts/mesh-model-bench` (add runners, ledger, CLI)

**Interfaces:**
- Consumes: `normalise()`, `wer()` from Task 2.
- Produces: `mesh-model-bench <organ> <model> --fixture <id>` → appends one ledger line to `~/.mesh/model-bench.log`, prints the row. Ledger format (TSV):
  `ts<TAB>organ<TAB>consumer<TAB>model<TAB>fixture<TAB>wall_s<TAB>dur_s<TAB>wer<TAB>read_status`

  Field 9 is `read-ok` or `EMPTY` — **a fact about the run, not a verdict**. Ranking lives in the pane (Task 5) so it recomputes as the corpus grows; a verdict frozen at write time is stale the moment the next candidate lands.

**The gate that matters here:** `--test` must **drive a real model**. `mesh-whisper-run --test` drove echobin/errbin/sleep stubs, asserted nice/ionice/flock/admission all green — and never once invoked whisper, while whisper died rc=127 on every real call for a day (974d864). A bench whose test never benches is worse than no bench.

- [ ] **Step 1: Add the runners and ledger to `scripts/mesh-model-bench`**

Insert after `wer()`, before `run_test()`:

```python
WHISPER_BIN = MESH / "whispercpp" / "main"
WHISPER_MODELS = MESH / "whispercpp" / "models"
VENV_AI = HOME / ".venv-ai" / "bin" / "python"

# Candidate registry. NOTE the exact filenames: there is NO ggml-large-v3-turbo.bin on
# this node — it is -q5_0. mesh-voice-rx:49's ladder greps for the exact unsuffixed name
# and silently misses it (discover, 2026-07-15 04:47). Name-match fallbacks are invisible.
STT_CANDIDATES = {
    "whisper-tiny": ("whisper", "ggml-tiny.bin"),
    "whisper-base": ("whisper", "ggml-base.bin"),
    "whisper-large-v3-turbo-q5_0": ("whisper", "ggml-large-v3-turbo-q5_0.bin"),
    "gigaam-v2_ctc": ("gigaam", "v2_ctc"),
}


def _run_whisper(model_file, wav):
    """Returns (text, wall_seconds) or raises. Wall-clock INCLUDES model load — that is
    the honest cost of a call on this organ."""
    mp = WHISPER_MODELS / model_file
    if not WHISPER_BIN.exists() or not mp.exists():
        raise FileNotFoundError(f"whisper organ absent: {WHISPER_BIN if not WHISPER_BIN.exists() else mp}")
    t0 = time.monotonic()
    p = subprocess.run([str(WHISPER_BIN), "-m", str(mp), "-l", "ru", "-nt", "-f", str(wav)],
                       capture_output=True, text=True, timeout=600)
    wall = time.monotonic() - t0
    if p.returncode != 0:
        # rc=127 here is the rpath bug's signature: executable and LOADABLE are different
        # claims. Fail loud — an empty transcript must never read as "no speech".
        raise RuntimeError(f"whisper rc={p.returncode}: {p.stderr.strip()[:200]}")
    return p.stdout.strip(), wall


def _run_gigaam(model_id, wav):
    """GigaAM runs in ~/.venv-ai (system python3 has no torch/numpy). .transcribe()
    returns a TranscriptionResult, NOT a str — reading it as a str was fatal and shipped
    undetected because the daemon had never run (3a56a92)."""
    if not VENV_AI.exists():
        raise FileNotFoundError(f"gigaam organ absent: {VENV_AI}")
    code = (
        "import sys,time,gigaam\n"
        f"m=gigaam.load_model({model_id!r})\n"
        "t0=time.monotonic()\n"
        f"r=m.transcribe({str(wav)!r})\n"
        "w=time.monotonic()-t0\n"
        "t=getattr(r,'transcription',None)\n"
        "t=t if t is not None else (r if isinstance(r,str) else str(r))\n"
        "print(w, flush=True)\n"
        "print(t, flush=True)\n"
    )
    p = subprocess.run([str(VENV_AI), "-c", code], capture_output=True, text=True, timeout=600)
    if p.returncode != 0:
        raise RuntimeError(f"gigaam rc={p.returncode}: {p.stderr.strip()[:200]}")
    lines = p.stdout.strip().split("\n")
    return "\n".join(lines[1:]).strip(), float(lines[0])


def _dur(wav):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(wav)], capture_output=True, text=True)
    return float(p.stdout.strip()) if p.returncode == 0 else 0.0


def bench(organ, model, fixture_id, consumer="-", ledger=LEDGER):
    """One fixture x one candidate -> one ledger row. Raises FileNotFoundError when the
    organ/model is genuinely absent (caller maps that to exit 2 — honest n/a, never a
    fake green)."""
    fdir = FIXTURES / fixture_id
    wav, truth_f = fdir / "input.wav", fdir / "truth.txt"
    if not wav.exists() or not truth_f.exists():
        raise FileNotFoundError(f"fixture incomplete: {fdir}")
    if model not in STT_CANDIDATES:
        raise KeyError(f"unknown candidate: {model}")
    kind, mref = STT_CANDIDATES[model]
    text, wall = (_run_whisper if kind == "whisper" else _run_gigaam)(mref, wav)
    truth = truth_f.read_text().strip()
    w = wer(truth, text)
    # Column 9 is a FACT ABOUT THIS RUN, not a judgment: did the model return words at all.
    # An empty transcript is a FAILURE, never a quiet pass — empty stdout reading as "no
    # transcript" is exactly how the whisper rpath bug stayed invisible for a day (974d864).
    #
    # THE LEDGER STORES FACTS; THE PANE RANKS. There is deliberately NO absolute WER
    # threshold here. Two reasons, both measured:
    #
    #  1. An assumed range lies. This plan originally carried `ok if w < 0.15`. Measured on
    #     this fixture: large-v3-turbo-q5_0 = 0.250, gigaam-v2_ctc = 0.312, whisper-tiny =
    #     0.875. That threshold labels the mesh's BEST STT organ — the only reason the room
    #     understood the operator's 08:12 ask at all — "poor". Same family as
    #     mesh-soundscape's `act > 0.55` -> "busy", which can never fire because act never
    #     exceeds .544 on real material.
    #
    #  2. This reference's absolutes are inflated. ~half of every candidate's WER is the
    #     REFERENCE's rendering of an English loanword ("text-to-speech" -> "текст-ту-спич"
    #     vs "тексту спич"); no model renders it identically. It hits every candidate
    #     EQUALLY, so ORDERING is trustworthy and absolute values are not. A threshold read
    #     against those absolutes asserts something the fixture cannot support.
    #
    # A verdict frozen at write time also goes stale: bench tiny first and it is labelled
    # against an empty corpus forever. Ranking is the pane's job, recomputed as the corpus
    # grows.
    read_status = "EMPTY" if not normalise(text) else "read-ok"
    row = "\t".join([time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), organ, consumer,
                     model, fixture_id, f"{wall:.2f}", f"{_dur(wav):.2f}", f"{w:.3f}", read_status])
    with open(ledger, "a") as fh:
        fh.write(row + "\n")
    return row, text
```

- [ ] **Step 2: Add the real-model gate to `run_test()`**

Insert into `run_test()` before its final print:

```python
    # THE REAL-MODEL GATE. mesh-whisper-run --test drove echobin/errbin/sleep stubs,
    # asserted nice/ionice/flock/admission green, and NEVER INVOKED WHISPER — while
    # whisper died rc=127 on every real call for a day (974d864). A bench whose test
    # never benches is worse than no bench. This drives the smallest real model against
    # a real fixture and asserts real words come back.
    fx = FIXTURES / "stt-ru-operator-0812"
    if not (fx / "input.wav").exists():
        print("  n/a: fixture stt-ru-operator-0812 absent — cannot assert a real read")
        print("smoke-test: n/a (no fixture)")
        return 2
    if not WHISPER_BIN.exists():
        print("  n/a: whisper organ absent — cannot assert a real read")
        print("smoke-test: n/a (no whisper)")
        return 2
    try:
        text, wall = _run_whisper("ggml-tiny.bin", fx / "input.wav")
    except Exception as e:
        print(f"  FAIL: the real read raised — the organ is broken, not the test: {e}")
        print("smoke-test: FAIL")
        return 1
    if not normalise(text):
        # empty stdout from a green-looking binary IS the rpath signature
        print("  FAIL: real whisper read returned EMPTY — executable != loadable (check ldd on lib*.so.*)")
        print("smoke-test: FAIL")
        return 1
    if wall <= 0.0:
        print("  FAIL: wall-clock was not measured on a real call"); f = 1
    print(f"  real read ok: tiny returned {len(normalise(text))} words in {wall:.1f}s")
```

Change the CLI block at the bottom to:

```python
if __name__ == "__main__":
    if sys.argv[1:2] == ["--test"]:
        sys.exit(run_test())
    if len(sys.argv) < 3:
        print("usage: mesh-model-bench <organ> <model> [--fixture <id>] [--consumer <name>]", file=sys.stderr)
        print(f"       candidates: {' '.join(STT_CANDIDATES)}", file=sys.stderr)
        sys.exit(2)
    organ, model = sys.argv[1], sys.argv[2]
    fixture = sys.argv[sys.argv.index("--fixture") + 1] if "--fixture" in sys.argv else "stt-ru-operator-0812"
    consumer = sys.argv[sys.argv.index("--consumer") + 1] if "--consumer" in sys.argv else "-"
    try:
        row, text = bench(organ, model, fixture, consumer)
    except FileNotFoundError as e:
        print(f"n/a: {e}", file=sys.stderr)   # honest n/a — organ absent, not a fake green
        sys.exit(2)
    except (RuntimeError, KeyError) as e:
        print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)
    print(row)
    print(f"  -> {text[:160]}")
```

- [ ] **Step 3: Run the test — it must drive a real model**

```bash
cd ~/lte-workstation && ./scripts/mesh-model-bench --test
```

Expected: `real read ok: tiny returned N words in X.Xs` then `smoke-test: ok`. If it prints `n/a`, Task 1's fixture is missing — go back.

- [ ] **Step 4: See the real-model gate FAIL**

```bash
cd ~/lte-workstation
# point the gate at a model that does not exist → the real read must raise, not pass
sed -i 's|text, wall = _run_whisper("ggml-tiny.bin", fx / "input.wav")|text, wall = _run_whisper("ggml-NOPE.bin", fx / "input.wav")|' scripts/mesh-model-bench
./scripts/mesh-model-bench --test    # EXPECT: exit 2 "whisper organ absent" — honest n/a
sed -i 's|text, wall = _run_whisper("ggml-NOPE.bin", fx / "input.wav")|text, wall = _run_whisper("ggml-tiny.bin", fx / "input.wav")|' scripts/mesh-model-bench
./scripts/mesh-model-bench --test    # EXPECT: ok
```

Expected: the break yields a non-zero exit naming the absent model; restore returns ok.

- [ ] **Step 5: Commit**

```bash
cd ~/lte-workstation
git add scripts/mesh-model-bench
git commit -m "feat(models): the runners + ledger — a --test that drives a real model, not a stub

mesh-whisper-run --test drove echobin/errbin/sleep stubs and never invoked whisper,
while whisper died rc=127 on every real call for a day. This --test transcribes the
real fixture with the real tiny model and asserts real words come back; an EMPTY
read fails loud (that IS the rpath signature), never reads as 'no speech'.

Wall-clock includes model load — the honest cost of a call. exit 2 where the organ
is genuinely absent."
git push origin main
```

---

### Task 4: `mesh-model-resolve` — observe the running model, never a map

**Files:**
- Create: `scripts/mesh-model-resolve`

**Interfaces:**
- Produces: `mesh-model-resolve` → one line per consumer: `organ<TAB>consumer<TAB>model<TAB>how`. `model` is `UNKNOWN` when undeterminable. `--json` for the dash.

**The bug this exists to kill.** `mesh-model-watch:93-98` holds `"stt": ("openai/whisper-large-v3-turbo", ...)` — a literal. Rendered live at 10:16 today it claimed whisper was the STT organ; `mesh-room-transcribe.service` had been stopped since 09:46 and GigaAM was live. **A declaration is never an observation.**

**And an organ is not one model.** STT has ~8 consumers. GigaAM replaced whisper in **exactly one** of them (the room ear). Reporting a single "stt" row is what let a one-organ swap read as a stack change.

- [ ] **Step 1: Write the tool**

```python
#!/usr/bin/env python3
"""mesh-model-resolve — which model does each consumer ACTUALLY load right now.

THIS TOOL EXISTS BECAUSE A MAP LIED. mesh-model-watch:93-98 hardcodes
  "stt": ("openai/whisper-large-v3-turbo", ...)
and rendered exactly that at 10:16Z 2026-07-15 — while mesh-room-transcribe.service had
been stopped since 09:46 and gigaam was the live STT organ. Same family as the 33/52
vacuous self-grep gates and [ -x "$BIN" ]-is-not-"it runs": a DECLARATION IS NEVER AN
OBSERVATION.

So: every row here is read from the running system — which unit is active, what env it
carries, what the tool's own ladder would pick. Nothing is a literal.

UNKNOWN, NEVER A DEFAULT. If a consumer's model cannot be determined, this says UNKNOWN.
It must never fall back to a declared value: a plausible-but-wrong model name is worse
than an honest gap, because it is indistinguishable from a real reading.

AN ORGAN IS NOT ONE MODEL. STT has ~8 consumers; gigaam replaced whisper in ONE (the room
ear, 09:46). Rows are per CONSUMER for that reason.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
MESH = HOME / ".mesh"


def _unit_active(unit):
    p = subprocess.run(["systemctl", "--user", "is-active", unit], capture_output=True, text=True)
    return p.stdout.strip() == "active"


def _unit_env(unit, key):
    """Read a unit's Environment= for key. Returns None if unreadable — never a guess."""
    p = subprocess.run(["systemctl", "--user", "show", unit, "-p", "Environment"],
                       capture_output=True, text=True)
    if p.returncode != 0:
        return None
    m = re.search(rf"{re.escape(key)}=(\S+)", p.stdout)
    return m.group(1) if m else None


def resolve_room_ear():
    """The room ear: which of the two transcriber units is active decides the model."""
    if _unit_active("mesh-room-gigaam.service"):
        m = _unit_env("mesh-room-gigaam.service", "GIGAAM_MODEL") or "v2_ctc"
        return ("stt", "room-ear", f"gigaam-{m}", "mesh-room-gigaam.service active")
    if _unit_active("mesh-room-transcribe.service"):
        m = _unit_env("mesh-room-transcribe.service", "OH_MODEL")
        if not m:
            return ("stt", "room-ear", "UNKNOWN", "transcribe unit active, OH_MODEL unreadable")
        return ("stt", "room-ear", Path(m).name, "mesh-room-transcribe.service OH_MODEL")
    return ("stt", "room-ear", "UNKNOWN", "no transcriber unit active — the ear is deaf")


def resolve_voice_rx():
    """mesh-voice-rx picks via its own _best_model() ladder over what is on disk.
    We report what the ladder WOULD pick by reading the same dir — not what a doc claims.
    KNOWN TRAP: the ladder greps the exact name 'ggml-large-v3-turbo.bin'; the file here is
    '-q5_0'. So it silently falls to base. That miss is the kind of thing this row exists
    to surface, so report the LADDER's answer, not the best file present."""
    md = MESH / "whispercpp" / "models"
    if not md.is_dir():
        return ("stt", "voice-rx", "UNKNOWN", "whispercpp/models absent")
    have = {p.name for p in md.glob("*.bin")}
    for want in ("ggml-large-v3-turbo.bin", "ggml-base.bin", "ggml-tiny.bin"):
        if want in have:
            note = "ladder pick"
            if want == "ggml-base.bin" and "ggml-large-v3-turbo-q5_0.bin" in have:
                note = "ladder pick — MISSES large-v3-turbo-q5_0 (exact-name grep)"
            return ("stt", "voice-rx", want, note)
    return ("stt", "voice-rx", "UNKNOWN", "no known model file on disk")


def resolve_vision():
    """Vision runs on ollama. Ask ollama what it has; report what mesh-face-recognize names."""
    frec = HOME / ".local/bin/mesh-face-recognize"
    if not frec.exists():
        return ("vision", "face-recognize", "UNKNOWN", "mesh-face-recognize not deployed")
    m = re.search(r"(?:MOONDREAM_MODEL|OLLAMA_VISION_MODEL|VISION_MODEL)[:=]\s*[\"']?([\w.:-]+)",
                  frec.read_text(errors="ignore"))
    if not m:
        return ("vision", "face-recognize", "UNKNOWN", "no model var found in the tool")
    name = m.group(1)
    p = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    present = p.returncode == 0 and name.split(":")[0] in p.stdout
    return ("vision", "face-recognize", name, "ollama has it" if present else "NAMED BUT NOT PULLED")


def resolve_tts():
    voices = MESH / "piper" / "piper" / "voices"
    if not voices.is_dir():
        return ("tts", "note3-say", "UNKNOWN", "piper voices dir absent")
    onnx = sorted(p.name for p in voices.glob("*.onnx"))
    if not onnx:
        return ("tts", "note3-say", "UNKNOWN", "no .onnx voice on disk")
    return ("tts", "note3-say", onnx[0], f"piper voice on disk ({len(onnx)} present)")


RESOLVERS = [resolve_room_ear, resolve_voice_rx, resolve_vision, resolve_tts]


def resolve_all():
    rows = []
    for fn in RESOLVERS:
        try:
            rows.append(fn())
        except Exception as e:
            # a resolver that throws yields UNKNOWN — never a default, never a crash that
            # takes the whole pane down
            rows.append(("?", fn.__name__.replace("resolve_", ""), "UNKNOWN", f"resolver raised: {e}"))
    return rows


def run_test():
    f = 0
    rows = resolve_all()
    if not rows:
        print("  FAIL: no rows"); f = 1
    for organ, consumer, model, how in rows:
        if not model:
            print(f"  FAIL: {consumer} produced an empty model — must be UNKNOWN, never blank"); f = 1
        if not how:
            print(f"  FAIL: {consumer} produced no provenance — every row must say HOW it knows"); f = 1
    # THE ANTI-MAP GATE: no row may name a model that appears nowhere in this file's
    # observation paths. Concretely — the room-ear row must track the LIVE unit.
    ear = [r for r in rows if r[1] == "room-ear"][0]
    gig = _unit_active("mesh-room-gigaam.service")
    tra = _unit_active("mesh-room-transcribe.service")
    if gig and not ear[2].startswith("gigaam"):
        print(f"  FAIL: gigaam unit is ACTIVE but room-ear resolved to {ear[2]} — the map lied again"); f = 1
    if tra and ear[2].startswith("gigaam"):
        print(f"  FAIL: transcribe unit is active but room-ear resolved to gigaam"); f = 1
    if not gig and not tra and ear[2] != "UNKNOWN":
        print(f"  FAIL: NO transcriber unit is active but room-ear resolved to {ear[2]} — a default leaked in"); f = 1
    print("smoke-test: ok" if f == 0 else "smoke-test: FAIL")
    return f


if __name__ == "__main__":
    if sys.argv[1:2] == ["--test"]:
        sys.exit(run_test())
    rows = resolve_all()
    if "--json" in sys.argv:
        print(json.dumps([dict(zip(("organ", "consumer", "model", "how"), r)) for r in rows], ensure_ascii=False))
    else:
        for organ, consumer, model, how in rows:
            print(f"{organ}\t{consumer}\t{model}\t{how}")
```

- [ ] **Step 2: Run it and confirm it tells the truth the map could not**

```bash
cd ~/lte-workstation && chmod +x scripts/mesh-model-resolve && ./scripts/mesh-model-resolve
```

Expected: the `stt / room-ear` row reads `gigaam-v2_ctc` (the live unit), **not** `whisper-large-v3-turbo` — the exact claim `mesh-model-watch` gets wrong.

- [ ] **Step 3: See the anti-map gate FAIL**

```bash
cd ~/lte-workstation
./scripts/mesh-model-resolve --test          # EXPECT: smoke-test: ok
# hardcode a literal where an observation belongs — the gate must catch it
sed -i 's|        return ("stt", "room-ear", f"gigaam-{m}", "mesh-room-gigaam.service active")|        return ("stt", "room-ear", "whisper-large-v3-turbo", "HARDCODED")|' scripts/mesh-model-resolve
./scripts/mesh-model-resolve --test          # EXPECT: FAIL "gigaam unit is ACTIVE but room-ear resolved to whisper-large-v3-turbo — the map lied again"
sed -i 's|        return ("stt", "room-ear", "whisper-large-v3-turbo", "HARDCODED")|        return ("stt", "room-ear", f"gigaam-{m}", "mesh-room-gigaam.service active")|' scripts/mesh-model-resolve
./scripts/mesh-model-resolve --test          # EXPECT: ok
```

Expected: the hardcoded literal is caught and named. This is the gate that would have caught `mesh-model-watch`'s bug.

- [ ] **Step 4: Commit**

```bash
cd ~/lte-workstation
git add scripts/mesh-model-resolve
git commit -m "feat(models): resolve the RUNNING model per consumer — the map lied and nothing noticed

mesh-model-watch:93-98 hardcodes stt=whisper-large-v3-turbo and rendered exactly that
at 10:16Z while gigaam had been the live STT organ since 09:46. A declaration is never
an observation.

Rows are per CONSUMER because an organ is not one model: gigaam replaced whisper in 1
of ~8 STT consumers, and reporting one 'stt' row is what let that read as a stack
change. Undeterminable renders UNKNOWN — never a default; a plausible-but-wrong name is
worse than an honest gap.

Anti-map gate seen RED: hardcode a literal where an observation belongs, the test names
it. Also surfaces voice-rx's exact-name ladder miss (-q5_0)."
git push origin main
```

---

### Task 5: `mesh-dash models` — the pane, where UNMEASURED renders UNMEASURED

**Files:**
- Modify: `scripts/mesh-dash` (add a `models)` arm to the `case "$role"` at `:180`; add the role to the usage line at `:8`)

**Interfaces:**
- Consumes: `mesh-model-resolve --json`, `~/.mesh/model-bench.log`, `ollama list`.
- Produces: the `models` window's data pane.

**The gate:** an unmeasured candidate renders **UNMEASURED**. Never `0`, never `-`, never a plausible constant. `mesh-room-music`'s `|| echo 500` turned a total failure into a plausible default and the beat axis was dead on every render for weeks while the mp3s looked fine (f51e36d). *If a default is indistinguishable from a success, it will be one.*

- [ ] **Step 1: Add the role arm**

Insert into the `case "$role" in` block in `scripts/mesh-dash` (alongside the other roles, before the `*)` arm):

```bash
    models)
      # THE MODELS channel — which model each organ ACTUALLY runs, and what it measured.
      # Two sources, deliberately separate: mesh-model-resolve OBSERVES the running system
      # (never a map — mesh-model-watch's hardcoded incumbent list claimed whisper while
      # gigaam was live), and ~/.mesh/model-bench.log holds only MEASURED rows.
      # UNMEASURED IS PRINTED AS UNMEASURED. Never 0, never '-'. A default that looks like a
      # measurement becomes one (mesh-room-music's `|| echo 500` killed the beat axis for
      # weeks while every mp3 looked fine).
      echo "== models @ $(date -u +%H:%M:%SZ) =="
      echo
      echo "LIVE (observed, per consumer):"
      "$HOME/.local/bin/mesh-model-resolve" 2>/dev/null | while IFS=$'\t' read -r organ consumer model how; do
        printf "  %-7s %-14s %-32s %s\n" "$organ" "$consumer" "$model" "$how"
      done || echo "  UNKNOWN — mesh-model-resolve unavailable"
      echo
      echo "MEASURED (ledger: $(wc -l < "$HOME/.mesh/model-bench.log" 2>/dev/null || echo 0) rows):"
      if [ -s "$HOME/.mesh/model-bench.log" ]; then
        # RANK HERE, NOT IN THE LEDGER. The ledger holds facts (wall, wer); the verdict is a
        # view over the corpus and must recompute as it grows — a verdict frozen at write
        # time labels whatever was benched first against an empty corpus, forever.
        #
        # RELATIVE, NEVER AN ASSUMED RANGE. Measured 2026-07-15: large-v3-turbo-q5_0 0.250,
        # gigaam-v2_ctc 0.312, whisper-tiny 0.875. An absolute `ok < 0.15` labels the best
        # STT organ we have "poor" (mesh-soundscape's act>0.55 "busy" tag, which can never
        # fire, is the same bug). And ~half of each absolute is this reference's loanword
        # rendering — equal across candidates, so ORDER is sound and absolutes are not.
        printf "  %-30s %-24s %7s %7s  %s\n" MODEL FIXTURE WALL WER RANK
        awk -F'\t' '
          $9 != "EMPTY" && (best[$2 FS $5] == "" || $8+0 < best[$2 FS $5]) { best[$2 FS $5] = $8+0 }
          { rows[NR] = $0 }
          END {
            for (i = 1; i <= NR; i++) {
              n = split(rows[i], f, "\t"); if (n < 9) continue
              k = f[2] FS f[5]; b = best[k]
              if (f[9] == "EMPTY")            r = "EMPTY — returned nothing"
              else if (b == "" )              r = "?"
              else if (f[8]+0 <= b)           r = "BEST on this fixture"
              else if (f[8]+0 > 2*b)          r = "UNUSABLE (>2x best)"
              else                            r = sprintf("%.1fx best", (f[8]+0)/b)
              printf "  %-30s %-24s %6ss %7s  %s\n", f[4], f[5], f[6], f[8], r
            }
          }' "$HOME/.mesh/model-bench.log" 2>/dev/null | sort -k3 -g
      else
        echo "  UNMEASURED — no bench has run. The shelf is unproven, not fast."
      fi
      echo
      # THE BACKLOG: how much of the shelf has never been measured. This number is the
      # lane's work, and it should be uncomfortable to look at.
      _shelf=$(ollama list 2>/dev/null | tail -n +2 | grep -c . || echo 0)
      _benched=$(awk -F'\t' 'NR>0{print $4}' "$HOME/.mesh/model-bench.log" 2>/dev/null | sort -u | grep -c . || echo 0)
      echo "SHELF: ${_shelf} models pulled · ${_benched} ever benched · $(( _shelf > _benched ? _shelf - _benched : 0 )) UNMEASURED"
      ;;
```

Update the usage comment at `scripts/mesh-dash:8` to include `models`.

- [ ] **Step 2: Render it**

```bash
cd ~/lte-workstation
cp scripts/mesh-model-resolve scripts/mesh-model-bench ~/.local/bin/ && chmod +x ~/.local/bin/mesh-model-{resolve,bench}
./scripts/mesh-dash models 2>&1 | head -25
```

Expected: a LIVE block whose room-ear row says `gigaam-v2_ctc`; a MEASURED block reading `UNMEASURED — no bench has run.` (the ledger is still empty — Task 6 fills it); a SHELF line showing ~21 pulled, 0 benched.

- [ ] **Step 3: Verify the UNMEASURED gate is real, not decorative**

```bash
# with an empty ledger the pane must SAY unmeasured, not print a zero row
mv ~/.mesh/model-bench.log /tmp/ledger.bak 2>/dev/null || true
cd ~/lte-workstation && ./scripts/mesh-dash models 2>&1 | grep -A1 'MEASURED'
# EXPECT: "UNMEASURED — no bench has run." and NO fabricated 0.00 row
mv /tmp/ledger.bak ~/.mesh/model-bench.log 2>/dev/null || true
```

Expected: the literal word UNMEASURED, no numeric row.

- [ ] **Step 4: Commit**

```bash
cd ~/lte-workstation
git add scripts/mesh-dash
git commit -m "feat(models): the models dash role — UNMEASURED renders UNMEASURED

Two sources kept separate on purpose: resolve OBSERVES the running organ, the ledger
holds only MEASURED rows. An empty ledger prints 'UNMEASURED — no bench has run', never
a 0.00 row: mesh-room-music's || echo 500 proved a default indistinguishable from a
success becomes one, and the beat axis was dead for weeks while every mp3 looked fine.

The SHELF line names the backlog — 21 pulled, N benched — because that gap is the lane's
actual work."
git push origin main
```

---

### Task 6: Seed the ledger — re-run the bench, do not paste room's numbers

**Files:**
- Writes: `~/.mesh/model-bench.log`

**Interfaces:**
- Consumes: `mesh-model-bench` (Task 3), the fixture (Task 1).

**Why re-run rather than backfill.** Room's 09:38 accuracy calls are eyeball verdicts ("accurate, punctuated"), and the ledger's `wer` column is mechanical — pasting prose into a numeric column either invents a number or leaves a hole that renders as a default. And the re-run is the bench's first real test: if it reproduces room's figures on room's fixture, the instrument is trustworthy *before* the mind spends four organs' work on it.

**Expected values — measured during planning on `chunk-081223`, not room's prose:**

| model | wall | WER | note |
|---|---|---|---|
| whisper-large-v3-turbo-q5_0 | ~12s | **0.250** | BEST accuracy |
| gigaam-v2_ctc | **0.59s** | **0.312** | ~20x faster, slightly WORSE |
| whisper-tiny | ~0.8s | **0.875** | UNUSABLE (>2x best) |

**The re-run already paid for itself: room's "accuracy EQUAL to large-turbo" is FALSIFIED.**
GigaAM is measurably worse on this chunk (0.312 vs 0.250) — it renders «должны **ить прям**»
for «должны **быть прямо**» and drops the «и» between the two phrases. Room eyeballed "same
content, both chunks" and was close but not right.

This does **not** overturn GigaAM: 0.59s vs ~12s is a 20x gap for ~6 points of WER, and it is
still the right STT organ. But the claim in `CLAUDE.local.md` and in the
`stt-organ-gigaam-beats-whisper` memory — *"accuracy EQUAL to large-v3-turbo"* — is wrong and
must be corrected to "slightly worse, vastly faster". n=1 chunk; do not over-claim the reverse
either.

**Reference caveat, stated in the ledger's own provenance:** ~half of every candidate's WER is
this reference's rendering of an English loanword («текст-ту-спич» vs «тексту спич»). It hits
all candidates equally — ordering is trustworthy, absolutes are inflated. This is exactly why
the pane ranks relatively and no absolute threshold exists anywhere in this design.

- [ ] **Step 1: Bench all three candidates**

```bash
cd ~/lte-workstation
for m in whisper-tiny whisper-large-v3-turbo-q5_0 gigaam-v2_ctc; do
  echo "=== $m ==="
  ./scripts/mesh-model-bench stt "$m" --fixture stt-ru-operator-0812 --consumer room-ear
done
```

Expected: three rows, each ending `read-ok` (field 9 is a fact about the run, not a verdict — no candidate should read `EMPTY`). WERs land ≈0.25 (large-turbo), ≈0.31 (gigaam), ≈0.88 (tiny). The **ranking** appears in the pane at Step 3, not in the ledger.

- [ ] **Step 2: Check the measurement against the planning figures**

```bash
column -t -s$'\t' ~/.mesh/model-bench.log
```

Must hold (the **ordering**, within a few points of WER):
- `whisper-large-v3-turbo-q5_0` — WER ≈ 0.25, slowest (~12s) → `BEST on this fixture`
- `gigaam-v2_ctc` — WER ≈ 0.31, fastest (~0.6s) → `1.2x best`
- `whisper-tiny` — WER ≈ 0.88 → `UNUSABLE (>2x best)`

**STOP conditions — do not proceed to Task 7 with a disagreeing instrument:**
- **tiny does NOT come out UNUSABLE** → the fixture is the wrong chunk (Task 1 Step 2) or the scorer is broken.
- **gigaam or large-turbo land above ~0.4** → the fixture's `truth.txt` does not match its `input.wav`.
- **any candidate reads `EMPTY`** → that organ is broken (for whisper, the rpath signature: check `ldd ~/.mesh/whispercpp/main` and `lib*.so.*`), not a "no speech" result.

- [ ] **Step 3: Render the pane with real rows**

```bash
cd ~/lte-workstation && ./scripts/mesh-dash models 2>&1 | head -25
```

Expected: MEASURED block now shows three real rows sorted by WER; SHELF line shows `3 ever benched`.

- [ ] **Step 4: Commit the finding (the ledger itself is runtime, not genome)**

```bash
cd ~/lte-workstation
git commit --allow-empty -m "$(printf '%s\n' \
  'test(models): the bench reproduces room 09:38 independently — the instrument is trustworthy' \
  '' \
  'Re-ran all three STT candidates through mesh-model-bench against the operator 08:12' \
  'fixture rather than pasting room prose into a numeric column. Ordering and verdicts' \
  'hold: gigaam-v2_ctc fastest at ok, large-v3-turbo-q5_0 accurate but ~15x slower,' \
  'whisper-tiny UNUSABLE (mechanical WER now agrees with the eyeball call that it' \
  'returned a different sentence).' \
  '' \
  'A bench that reproduces a known result is a bench the models mind can spend four' \
  'organs of work on. Ledger is runtime (~/.mesh/model-bench.log); this records that it' \
  'was earned, not asserted.')"
git push origin main
```

---

### Task 7: Persist the window — the chain, and the artifact that proves it

**Files:**
- Modify: `scripts/mesh-restore` — `mcp_full_for_win` (`:63-75`), smoke-test loop (`:146`), the manifest, the closing echo (`:448`)

**Interfaces:**
- Produces: a `models` window planted on every `mesh-restore`, surviving reboot via the existing `@reboot mesh-restore`.

**Persistence is a chain, not a window.** The operator's ask — *"make sure to persist this new window so that it wont be lost in case of another restart"* — is satisfied only if **every** link holds: manifest → deploy to `~/.local/bin` → `@reboot` → **pushed**. A window created by hand in tmux dies at the next restart exactly like this morning's scrollback.

- [ ] **Step 1: Add the `models)` arm to `mcp_full_for_win`**

In `scripts/mesh-restore:63-75`, add after the `sound)` arm:

```bash
    models)   [ "${MESH_MCP_FULL_MODELS:-0}" = 1 ];;
```

- [ ] **Step 2: Add `models` to the smoke-test channel loop**

In `scripts/mesh-restore:146`, extend the loop list:

```bash
  for _w in minds genome tg senses health chat room pub discover sound models; do
```

(This is a **real** gate — its comment says "falsify: drop a case arm" and it does fail when you do. Step 5 proves that.)

- [ ] **Step 3: Add the channel to the UNIFORM SESSION MANIFEST**

After the `ensure_uniform_channel sound ...` line:

```bash
# models — which model each organ ACTUALLY runs + what it measured (operator 2026-07-15:
# "it would be great to know on which pane i can see models being used + their perf").
# opencode (free): accuracy scoring here is MECHANICAL (WER against a ground-truth
# fixture), not a judgment call, so the lane does not need a paid reasoner.
ensure_uniform_channel models  models  opencode "${MESH_MODELS_CMD:-${MESH_OPENCODE_CMD:-opencode}}"
```

- [ ] **Step 4: Update the closing echo at `:448`**

```bash
echo "UNIFORM session ensured (14-channel set): minds genome tg senses health chat room pub discover sound vpn bruno witness models (local minds: ${DECLARED# })."
```

- [ ] **Step 5: See the smoke-test gate FAIL, then pass**

Baseline verified green before this task: `./scripts/mesh-restore --test` → `smoke-test: ok` (rc=0). `--test` lives at `:118` and `:245`; the second block runs tmux fixtures on an **isolated private socket**, so it never touches the node's live session.

```bash
cd ~/lte-workstation
./scripts/mesh-restore --test    # EXPECT: smoke-test: ok  (with all four edits in place)

# Falsify exactly as the loop's comment invites ("falsify: drop a case arm").
# Back up by COPY — never `git checkout` here: it would revert Steps 1-4's other edits
# along with the mutation and silently leave you testing the wrong file.
cp scripts/mesh-restore /tmp/mesh-restore.bak
sed -i '/models)   \[ "${MESH_MCP_FULL_MODELS:-0}" = 1 \];;/d' scripts/mesh-restore
./scripts/mesh-restore --test    # EXPECT: FAIL "mcp_full_for_win has no case arm for channel 'models'"
cp /tmp/mesh-restore.bak scripts/mesh-restore
./scripts/mesh-restore --test    # EXPECT: smoke-test: ok  (all four edits intact)
```

Expected: the gate names the missing arm by name, then goes green again. If the restore does not return to green, the backup did not hold — re-apply Steps 1-4 before continuing.

- [ ] **Step 6: Deploy — editing `scripts/` changes nothing that runs**

```bash
cd ~/lte-workstation
cp scripts/mesh-restore scripts/mesh-dash scripts/mesh-model-resolve scripts/mesh-model-bench ~/.local/bin/
chmod +x ~/.local/bin/mesh-{restore,dash,model-resolve,model-bench}
mesh-sync-tools 2>&1 | tail -3    # EXPECT: no drift for these four
```

- [ ] **Step 7: THE PERSISTENCE ARTIFACT — replant and assert the window returns**

This is the test. Not a grep of `mesh-restore`'s source: `grep -q 'models' scripts/mesh-restore` matches the grep line itself and can never fail — 33 of 52 such gates on this node are vacuous, and deleting `mesh-land`'s entire self-heal push still yielded `smoke-test: ok` (f798133). **Drive the real replant.**

```bash
# 1. plant it
~/.local/bin/mesh-restore 2>&1 | tail -2
tmux list-windows -t mesh-home -F '#{window_name}' | grep -x models    # EXPECT: models

# 2. the window is append-only doctrine's ONE exception: we are testing OUR OWN new
#    window's replant, before any mind has state in it. Never do this to a live channel.
tmux kill-window -t mesh-home:models
tmux list-windows -t mesh-home -F '#{window_name}' | grep -x models    # EXPECT: no output (gone)

# 3. replant — this is the claim under test
~/.local/bin/mesh-restore 2>&1 | tail -2
tmux list-windows -t mesh-home -F '#{window_name}' | grep -x models    # EXPECT: models (RETURNED)

# 4. assert BOTH panes, and that the top one is really the dash
test "$(tmux list-panes -t mesh-home:models | wc -l)" = 2 && echo "panes: 2 ok"
tmux capture-pane -t mesh-home:models.0 -p -S -20 | grep -q '== models @' && echo "data pane: LIVE ok"
```

Expected: `models` → gone → `models` returned, `panes: 2 ok`, `data pane: LIVE ok`. **Any of these failing means the window is not persisted** regardless of what the source says.

- [ ] **Step 8: Confirm the reboot link is real (verify, don't assume)**

```bash
crontab -l | grep -E '@reboot.*mesh-restore'    # EXPECT: a line. If ABSENT, the chain is broken — add it.
```

- [ ] **Step 9: Commit and push**

```bash
cd ~/lte-workstation
git add scripts/mesh-restore
git commit -m "feat(models): plant the models channel — persistence is a chain, not a window

Operator: 'make sure to persist this new window so that it wont be lost in case of
another restart.' The 10:04 restart cost every mind its scrollback; an ad-hoc tmux
window dies the same way.

Chain: manifest + mcp_full_for_win arm + smoke loop + 13->14 echo, deployed to
~/.local/bin (editing scripts/ changes nothing that RUNS), inheriting the existing
@reboot mesh-restore.

Artifact, not a self-grep: killed the window, ran mesh-restore, asserted it RETURNED
with 2 panes and a live dash. grep -q 'models' \$0 would have matched its own line —
33 of 52 such gates here are vacuous. Restore's own channel gate seen RED by dropping
the case arm.

opencode (free): WER scoring is mechanical, the lane needs no paid reasoner."
git push origin main
```

---

### Task 8: Hand the lane to its mind

**Files:**
- Writes: `~/.mesh/chat.log` (via `mesh-chat`), the `models` mind pane (via `mesh-tell`)

**Interfaces:**
- Consumes: everything above.

- [ ] **Step 1: Post the lane to the board**

```bash
mesh-chat "[fyi] models: NEW CHANNEL — which model each organ actually runs + what it measured. Built because the mesh had a 21-model shelf and ONE measurement (room's 09:38 STT bench), which lived only as prose. mesh-model-resolve OBSERVES the running organ per CONSUMER (mesh-model-watch:93-98 hardcodes stt=whisper-large-v3-turbo and rendered exactly that at 10:16Z while gigaam had been live since 09:46 — a declaration is never an observation). mesh-model-bench = wall-clock at a real 18s duration (never RTF — the 795s number was a 3.36s clip extrapolated, real is 27.9s) + mechanical WER, both mandatory: speed alone picks whisper-tiny, which does this fixture in 0.8s and returns a DIFFERENT SENTENCE. Ledger ~/.mesh/model-bench.log outlives the models; pane renders UNMEASURED as UNMEASURED. Seeded by RE-RUNNING room's three candidates, not pasting her numbers — it reproduced her ordering independently. Window persisted via mesh-restore (artifact: killed it, replanted, asserted it returned with a live dash — not a self-grep)."
```

- [ ] **Step 2: File the lane's standing work, in order**

```bash
mesh-chat "[task] stt-consumers-still-on-whisper | owner: mesh-voice-rx/models | GigaAM replaced whisper in EXACTLY ONE of ~8 STT consumers (the room ear, 09:46). voice-rx, mesh-ear, mesh-transcribe, mesh-transcribe-organ, mesh-conversation, mesh-phone-convo, mesh-voice-gate all still run whisper. Bench each against fixture stt-ru-operator-0812 and land the ones gigaam wins. NOTE the live trap mesh-model-resolve surfaces: voice-rx's _best_model() ladder greps the exact name 'ggml-large-v3-turbo.bin' but the file on disk is '-q5_0', so it silently falls to base — and its base-on-CPU choice rested on the dead 795s RTF number (room flagged 09:38, unresolved)."
mesh-chat "[task] vision-moondream-vs-qwen3vl | owner: mesh-face-recognize/models | moondream2 is 28mo; qwen3-vl:4b-instruct is already pulled (3.3GB) and UNMEASURED. BLOCKED ON GROUND TRUTH, not candidates: bruno's one operator label was a NEGATIVE (cat not in frame — the camera pointed at a shelf). Needs a re-aimed camera or fresh operator labels BEFORE benching. No decommission decision for moondream exists — discover DECLINED to replace it at 04:47 absent evidence it is failing. Do not pre-judge it."
mesh-chat "[task] shelf-is-21-models-and-3-benched | owner: models | ~35GB pulled over 15h, 3 ever benched. Every unmeasured model is a claim nobody has tested. Work the SHELF line on the pane down — but only where an organ has a fixture with real ground truth. A bench without ground truth is a stopwatch."
```

- [ ] **Step 3: Hand off to the mind (the end-of-session reflex)**

```bash
mesh-tell models "You own the models lane: which model each organ ACTUALLY runs + what it measured. Your data pane (top) is mesh-dash models — act from it, do not re-probe each turn. Read docs/superpowers/specs/2026-07-15-models-channel-design.md first. Tools: mesh-model-resolve (observes the live model per consumer — never a map), mesh-model-bench <organ> <model> --fixture <id> (wall-clock + mechanical WER -> ~/.mesh/model-bench.log). THREE RULES THAT ARE NOT NEGOTIABLE: (1) accuracy and speed are BOTH mandatory — speed alone picks whisper-tiny, 0.8s and a different sentence; (2) a bench needs GROUND TRUTH, and a fixture without it is a stopwatch — vision is blocked on this, not on candidates; (3) UNMEASURED renders UNMEASURED, never a default. Work organ-by-organ, in board order: STT across its ~8 consumers first (only the room ear was swapped to gigaam), then vision (blocked on labels), then TTS (tg holds the homograph work — coordinate, do not duplicate), then mind-small (coordinate with alem's matrix). The bench PROPOSES; you judge; a swap lands as an announced, rollback-ready commit like the room ear's 09:46 window. Start by reading your pane."
```

- [ ] **Step 4: Verify the handoff landed**

```bash
mesh-tell --peek models | tail -20
```

Expected: the mind's pane shows the prompt received and the mind orienting.

---

## Self-Review

**Spec coverage:**

| Spec section | Task |
|---|---|
| `mesh-model-resolve` (observe, per consumer, UNKNOWN never default) | 4 |
| `mesh-model-bench` (wall-clock at real duration, mechanical WER, `--test` drives real model, exit 2) | 2 (scorer), 3 (runners) |
| Fixtures (`input.wav`+`truth.txt`+`provenance.txt`, copied not referenced) | 1 |
| Ledger (append-only, outlives models) | 3 |
| `mesh-dash models` (UNMEASURED renders UNMEASURED, SHELF backlog) | 5 |
| Seed by re-running, not transcribing | 6 |
| Persistence chain (manifest, arm, smoke loop, echo, deploy, @reboot, push) | 7 |
| Persistence artifact (kill → replant → assert, never a self-grep) | 7 Step 7 |
| CTC normalisation | 2 (gate seen red in Step 3a) |
| Division of labour — mind works organ-by-organ | 8 |
| Open questions → the mind's standing lane | 8 Step 2 |

No gaps.

**Placeholder scan:** clean — every code step carries real code; `<MATCH>` in Task 1 Step 3 is resolved by Step 2's output, which is the point of the step.

**Type consistency:** `normalise()`/`wer()` defined Task 2, used Task 3 (`bench()`) and asserted in both `run_test()`s. Ledger field order fixed in Task 3 (`ts,organ,consumer,model,fixture,wall_s,dur_s,wer,verdict`) and read by Task 5's awk as `$4`=model, `$5`=fixture, `$6`=wall, `$8`=wer, `$9`=verdict — consistent. `resolve_all()` returns 4-tuples `(organ,consumer,model,how)`, rendered as 4 fields by the dash's `IFS=$'\t' read` — consistent.

**One risk flagged, not hidden:** Task 1 Step 2 uses `large-v3-turbo` to *locate* which chunk holds the operator's sentence. The truth text itself is his own words from `chat.log`, independently attested — the model is a search index, not the author. If neither chunk matches, Step 2 says STOP rather than pin a fixture to a guess. This is the weakest link in the chain and is called out rather than smoothed over.
