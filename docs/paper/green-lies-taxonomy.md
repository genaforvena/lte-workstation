# Green Lies: a taxonomy of self-observation failures in an autonomous agent system

**Status: DRAFT, increment 1 of N. Not submitted. Not complete.**
Target: arXiv preprint → one workshop (agents / reliability). One paper, not a pipeline.
Board task `paper-green-lies-taxonomy` `{#cfde8f2c}`, owner pub, tempo: unhurried (operator).

---

## Thesis

An autonomous system that maintains itself must observe itself. Every such system therefore
carries an *observation layer* — self-tests, health checks, liveness watchdogs, reflex schedulers —
and that layer is code like any other. When it fails, it does not usually fail loudly. It fails
**green**: it keeps producing the reading that means *fine*, at the normal cadence, with a fresh
timestamp and an honest-looking value, while the property it claims to check has stopped holding
or was never checked at all.

The failures are not random. They fall into a small number of **recurring structural classes**,
each with a decision procedure, and several are **mechanically detectable** from source alone.
This paper enumerates the classes, gives one live case and one commit per class from a
continuously-running multi-node agent system, provides a detector where the class is decidable,
and measures how often the class appears in third-party human-written code — establishing whether
these are general software defects or specific to code that carries its own self-observation.

The first measured answer suggests the latter, sharply. (§3.1.)

## 1. System under study

A multi-node autonomous agent mesh: ~730 shell/python tools, several LLM agents running
continuously in shared terminal sessions, ~250 cron-scheduled reflexes, a shared append-only
coordination log. Every tool is expected to carry a `--test` and a machine-readable cadence
header; the fleet's health is itself computed by tools in the same corpus. The system has run
continuously for months and its failure record is in git, so every case below is a real incident
with an artifact, not a constructed example.

Crucially for §3: **the tools test themselves in-file.** A `--test` verb lives inside the tool it
tests. This is what makes the corpus a good subject — and, as §3.1 shows, is very likely the
precondition for the first class existing at all.

## 2. The classes

| # | Class | One-line decision procedure | Live case | Commit | Detector |
|---|-------|------------------------------|-----------|--------|----------|
| C1 | **Self-grepping gate** | the assertion's evidence is its own source text | mesh-land's push self-heal | `1969a5d` | **D1, built** (§3) |
| C2 | **Silent fallback** | `cmd 2>/dev/null \|\| echo <default>` makes total failure indistinguishable from a constant | beat detector pinned at 500 for weeks | `f51e36d` | planned |
| C3 | **Window < cadence** | sampling window ÷ cadence = coverage; a 10s window on a 600s tick reports a sample, not a state | `mesh-psi` read CALM for 14.2 days on a stalled node | `fe35dd9` | **decidable** (header cadence vs the kernel field read) |
| C4 | **Dry-run writes the liveness log** | a `--test` writing the durable artifact a watchdog reads forges the evidence it exists to check | guardian's mock peer in the real log, reflex not in cron | `09f7914` | **decidable** (a `--test` path writing a `doctor-artifact`) |
| C5 | **Mode bit ≠ write accepted** | `[ -w f ]` describes the inode; for a pseudo-file the kernel may refuse anyway, with a *misleading errno* | `/proc/pressure/cpu` 0666, every uid-1000 write `EINVAL` | — (node measurement) | **decidable** (`[ -w ]` on a `/proc`/`/sys` path) |
| C6 | **Executable ≠ loadable** | `[ -x bin ]` is not "it runs"; rpath/ABI failures are a different claim | whisper.cpp `main` +x, `rc=127` for a day | `974d864` | **decidable** (`[ -x ]` gate with no invocation of the wrapped binary in `--test`) |
| C7 | **Predicate naming a node** | a guard bound to a hostname goes permanently false when the role moves, and every pass logs green | `TG_HOST="imozerov-IdeaPad-…"`, keeper body never executed once | `09f7914` | **decidable** (hostname literal in a guard) |
| C8 | **Never-wired reflex** | passing `--test` and being scheduled are unrelated facts; and a wired reflex can still tend a target that no longer exists | three keepalives green, none in cron | `cc617e5` | **decidable** (cadence header vs crontab vs target existence) |
| C9 | **Absent from the candidate set** | the gate is correct and loud; the item never reaches it, because the enumerator's input set does not cover it — and *outside the set* renders identically to *nothing wrong* | `mesh-land`'s pathspec was `scripts/ docs/` + root globs, so a landed tool's five `skills/**` payload files were never candidates: the tool sat on origin **broken from a clean clone** while every pass printed "nothing settled+clean to land" | `9f4537b` | **decidable** (declared pathspec vs the repo's tracked trees) |
| C10 | **Echo port** | the probe reads back *its own last write*: an absent device's read falls through to the register array that backs the write, so the capability check returns a plausible, varying, non-zero value carrying zero information about the world | probing Varvara for audio **input**: on a build with no audio device all 16 ports return the sentinel; on the real device exactly 3 of 16 are computed and **none is a microphone** | `9ed9d26` | **decidable at runtime** (write a sentinel, read it back — a match means you are talking to yourself) |

Four cross-cutting observations that are not classes but govern all of them:

* **Liveness-touch**: a reflex that writes its state only when the value *changes* leaves mtime
  frozen on a long-stable-but-live value, so an mtime watchdog reads "value held" as "reflex dead".
  Decouple *ran* from *changed* (`f3f84c1`).
* **Honest n/a is free**, and therefore becomes a resting state: an organ that answers "cannot
  assess" forever is indistinguishable from a healthy quiet one on every axis a reflex-health tool
  computes. Five organs in this corpus had *never* emitted an informative line, all green.

* **The empty set is spelled like success.** C9 is the sharpest instance of a shape that recurs
  across the corpus: a verdict computed by *reducing over a collection* returns the all-clear when
  the collection is empty, and nothing in the verdict records how the collection was built. A
  missing **gate** rots loudly — someone eventually watches it fail. A missing **pathspec** rots
  silently, because absence-from-the-candidate-set and cleanliness are the same output string.
  This is why C9's detector cannot live inside the pipeline it audits: the pipeline's own view of
  the world is exactly the set under suspicion. It must be checked against an *external*
  enumeration (here: `git ls-files`, and a clean clone that ran the landed tool's own gate).

* **A vacuity guard is not trustworthy until it has been wrong once.** C10's own guard first
  asserted `position* != 0` to prove a note was really playing — and that call is *false at the
  wrap*: a 16-byte looping sample returns the playhead to exactly `i % 16 == 0` after 1024 frames,
  so the guard declares a live note dead on a schedule. The general form: **a liveness check
  reading a wrapping counter has a periodic false negative, and the period is a property of the
  data, not of the check.** It was replaced with a read of the VU. Note what actually caught it —
  not review, but *running the guard against a case it should pass* and watching it fail. A guard
  only ever seen green is indistinguishable from C1.

## 3. Detector D1 — the self-grepping gate

### 3.0 The construct and its decision procedure

```sh
grep -q 'push_heal' "$0" || { echo "smoke-test: FAIL"; exit 1; }
```

The gate asserts that the string `push_heal` is present in the file. It is: **the grep line itself
contains it.** The assertion is satisfied by its own text and cannot fail. Deleting the entire
feature it claims to protect still yields `smoke-test: ok` — this was demonstrated on the original
case.

The decision procedure is exact, not heuristic:

> for every line L that greps its own source: extract the pattern P actually passed to grep;
> the gate is **vacuous** iff grep, with the same flags, matches P against L alone.

Four discriminations are required, and each one was found by watching the detector be wrong:

1. **Operand vs execution.** `"$0" --list | grep -q 'mind:plan'` *runs* the script and greps its
   **output** — a behavioural gate, the opposite of this class, and it matches any naive "`$0` near
   `grep`" rule. The script path must be grep's *file operand*: same pipeline segment, after the
   grep token.
2. **Pattern-internal `$0`.** A script grepping for the literal text `spent $0.0000` is not
   referring to itself. Remove the pattern before asking who the operand is.
3. **Undecidable patterns.** `grep -q "$PAT" "$0"` cannot be scored statically — its runtime text
   is not the text on the page. Reported as a third state, never folded into either verdict.
4. **Polarity, and it is the interesting one.** A self-match in a *positive* assertion
   (`… || fail`) always passes: silently vacuous. In a *negative* assertion (`… && fail`) it always
   **fails** — loudly, on the first run, so it never survives to be measured. Authors escape those
   patterns precisely because the failure is immediate. **The same construct is self-correcting in
   one polarity and silently vacuous in the other**, which is why the class is invisible: its
   detectable half is the half that never announces itself.

A corollary that falls out of (4) and is worth stating on its own: **a literal pattern is present
in its own grep line by construction**, so *every* literal positive source-grep at `$0` is vacuous.
The only escapes are anchored patterns that cannot match the line they are written on, and patterns
held in variables. Vacuity here is the default, not the accident.

### 3.1 Results

Detector: `docs/paper/detectors/d1_self_grepping_gate.py` (self-test + 3 mutants seen red).

**System under study** (`scripts/`, 732 files scanned):

| sites | undecidable | decidable boolean gates | **vacuous** |
|---|---|---|---|
| 60 | 28 | 20 | **3 (15%)** |

Named: `mesh-dispatch:702`, `mesh-dispatch:988`, `mesh-mind-compact:744`.

**Base rate, 10 widely-used public shell projects** (ohmyzsh, nvm, tpm, fzf, pyenv, rbenv,
bats-core, shellcheck, neofetch, powerlevel10k; 1296 shell/py files scanned):

| sites | undecidable | decidable boolean gates | vacuous |
|---|---|---|---|
| **0** | 0 | 0 | 0 |

**The construct does not appear at all.** Not "appears and is usually fine" — the population of
self-source-grepping gates in 1296 files of mature, widely-deployed human-written shell is empty,
so the vacuity *rate* there is undefined (0/0), not 0%.

Two control arms, because a zero produced by a broken harness is the exact failure this paper is
about:

* Same code path over the system under study returns 60/28/20/3 — the harness is not inert.
* A known-vacuous gate planted inside one of the clones is found (`sites 1, vacuous 1`) — the
  walker reaches those trees, and 1296 files were counted there by an independent walk.

### 3.2 Interpretation (and what it does not license)

The natural reading is that C1 is not a general shell defect but a defect of **in-file
self-testing**, which is characteristic of agent-authored tooling: an agent writing a tool writes
its `--test` in the same file, has the source in context, and reaches for the cheapest available
evidence — the text in front of it. Human projects in this sample test from *outside* the unit
(bats suites, CI, separate test dirs), a structure in which the construct is not expressible.

Not licensed by this data: any claim about frequency in *other* agent-written corpora (n=1 system),
and any causal claim about authorship — the sampled human projects also differ in age, review
process and test tooling. The confound is named, not resolved. §4 is where it gets resolved.

## 3bis. C9's decision procedure, run once (2026-08-20)

C9 is decidable without building anything: ask *git* — not the pipeline — which tracked files the
pipeline's declared pathspec selects, and subtract.

```sh
git ls-files | sort                                              > all
git ls-files -- scripts/ docs/ skills/ '*.md' '*.example' \
                '*.json' '*.conf' '*.env' '*.txt' | sort         > covered
comm -23 all covered      # LC_ALL=C — git's sort and comm's collation differ
```

Run against `mesh-land` **after** `9f4537b` closed the `skills/` instance: **1256 tracked, 1247
covered, 9 uncovered** — `.gitattributes`, `.gitignore`, `.sops.yaml`, `LICENSE`, `screenshot.svg`,
`caps.example/power`, `caps.example/voice`, and — the two that carry code — **`bootstrap.sh` and
`setup.sh`**, the scripts that plant the system onto a new node.

This is the result that makes C9 worth a class rather than an anecdote: **the fix closed the
instance, not the class.** A commit that adds `skills/` to a pathspec restores exactly one tree and
leaves the region's shape untouched, because the defect was never in the covered set — it is in the
*complement*, and a pathspec has no mechanism that makes its complement visible. Whether these nine
files *ought* to be in this pipeline's scope is a scoping decision for its owner; what is not a
decision is that the pipeline's `clean` verdict does not distinguish "these are fine" from "these
were never looked at", and no reader of that verdict can tell which they are holding.

Note also what the procedure required: a **clean clone**. The original instance was found the same
way — cloning the repo to a throwaway directory and running the landed tool's own gate, which
failed immediately (`missing from …/skills/…`). The tool's gate was loud and correct the entire
time; it was simply never reached from inside the system, where the payload's absence and its
presence produced the same output. An audit of the candidate set cannot be run from within the
process whose candidate set is in question.

## 3ter. C10's decision procedure, run once (2026-08-21)

C10 is the class that defeats C2's detector. C2 (silent fallback) is found by asking *is this
value a constant that a total failure would also produce?* — an echo port fails that test in the
attacker's favour: the value **varies**, it is **non-zero**, and it **changes when you change your
inputs**, which is exactly the evidence one would accept as proof of a live sensor. There is also
nothing to grep: no `|| echo <default>` appears in the source, because the fallthrough is a
`default:` case returning the device register array that the *write* path already populated.

The procedure is therefore runtime, not static, and it is one line: **write a sentinel, read it
back.** Any byte you get back that equals what you just wrote is your own echo.

Probing Varvara (the uxn virtual machine's device layer) for an audio **input** capability,
sentinel `a5` to all 16 ports of the audio page:

```
$ ./bin/uxncli audio-in-probe.rom
ports 30..3f readback: a5 a5 a5 a5 a5 a5 a5 a5 a5 a5 a5 a5 a5 a5 a5 a5
device: ABSENT -- every port echoed our own write
verdict: NO AUDIO INPUT DEVICE IN VARVARA
```

16 of 16. On a build linking the reference audio device, exactly ports `32,33,34` are computed
(`position*`, `output`) and the other **13 of 16 still echo** — and all three computed bytes
describe *the note the ROM itself started playing*. The capability was never there to find; a
naive read of any single port would have returned a plausible non-zero byte and been believed.

Two structural points this case contributes:

* **An absence needs two arms.** A probe that only ever runs where the device is missing has not
  demonstrated it can tell missing from present. The suite here builds *both* — the stock binary
  (device absent, `rc=2`, honest n/a) and a binary linking the real device (`rc=0`) — and a guard
  goes red if the real device is ever added to the default build, because that would silently
  delete the absent arm and leave the suite testing one thing twice. **A branch nothing has been
  seen to take is not a branch.**
* **Absence must be rendered, not inferred.** The probe prints the full 16-byte readback rather
  than a verdict alone, so a reader sees the echo pattern itself. Compare C9: in both, the system's
  own answer about its coverage is the thing under suspicion, so the evidence has to be shown at a
  level below the verdict.

## 4. Open work

1. Detectors for C3–C10 (each listed decidable above). C4 and C8 need the cadence header + crontab,
   which are machine-readable here.
2. **The authorship confound.** The clean comparison is not human-repo vs agent-repo but
   *in-file self-test* vs *external test suite*, within each population. Requires a second corpus
   of agent-written tooling, and a sample of human projects that do carry in-file self-tests.
3. Longitudinal: the anchor figure quoted in this system's own doctrine ("33 of 52 gates
   self-matching") is not in the commit it cites and could not be reproduced; tonight's
   re-derivation gives 3/20. Re-derivation over the git history would show whether the class was
   *fixed* or the measurement changed. **This is itself an instance of the paper's thesis** — a
   measured constant, quoted for five weeks, with no re-derivation behind it.
4. Threats to validity, written properly: detector precision/recall against a hand-labelled sample;
   the undecidable bucket (28/60 here) is large enough that its composition matters.

## 5. Reproducing

```sh
docs/paper/detectors/d1_self_grepping_gate.py --selftest   # the detector's own gates
docs/paper/detectors/d1_self_grepping_gate.py scripts      # system under study
docs/paper/detectors/d1_self_grepping_gate.py --json <dir> # any tree
```
