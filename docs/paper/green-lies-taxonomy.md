# Green Lies: a taxonomy of self-observation failures in an autonomous agent system

**Status: DRAFT, increment 4 of N. Not submitted. Not complete.**
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

The measured answer so far is **class-dependent, and the classes disagree** — which is itself the
finding that keeps this from being a one-mechanism story. C1 (the self-grepping gate) does not
occur *at all* in 1296 files of mature public shell: it is an affordance of in-file self-testing,
which is what agent-authored tooling does (§3.2). C2 (the silent fallback) occurs in both, and
public shell lies at **three times** this system's per-site rate — what distinguishes the agent
system there is not worse judgement but **321x the exposure**, plus one asymmetry density does not
explain: 13 fallbacks that lexically assert the all-clear here, zero there (§3quater.2).
So "agentic self-observation lies green" resolves into at least two different mechanisms —
structural affordance and sheer volume — and a remedy aimed at the wrong one would miss.

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
| C2 | **Silent fallback** | `cmd 2>/dev/null \|\| echo <default>` makes total failure indistinguishable from a constant | beat detector pinned at 500 for weeks | `f51e36d` | **D2, built** (§3quater) |
| C3 | **Window < cadence** | sampling window ÷ cadence = coverage; a 10s window on a 600s tick reports a sample, not a state | `mesh-psi` read CALM for 14.2 days on a stalled node | `fe35dd9` | **D3, built** (§3quinquies) |
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

## 3quater. Detector D2 — the silent fallback, and the result that inverts §3.2

Detector: `docs/paper/detectors/d2_silent_fallback.py` (self-test + **5 mutants seen red**, one of
which was found only because a mutant came back GREEN — see below).

### 3quater.0 Decision procedure

A fallback is a *correct* construct; its existence is not the defect. The graded question is
whether the substituted value is **distinguishable from a reading**:

| verdict | condition |
|---|---|
| **loud** | the literal is a marker (`na`, `unknown`, `error`, empty), or control escapes the branch (`exit`/`return`/`die`), or the branch writes to stderr — the failure is still announced |
| **silent** | the literal is a plausible datum in the success domain |
| **critical** | the literal is a word that *lexically asserts wellness* (`ok`/`up`/`true`/`pass`/…) — the failure does not merely hide, it reports the all-clear |
| **+colliding** | the same literal is also emitted on a **success path in the same file** — the only statically available *proof*, rather than inference from spelling, that the fallback lands inside the success domain |
| **undecidable** | the value carries a substitution (runtime text is not the text on the page), or the branch could not be parsed cleanly out of its enclosing context |
| **not-a-fallback** | `cond && echo Y \|\| echo n` (a two-way ternary: the `\|\|` arm is the deliberate *false* value) or `[ test ] \|\| printf …` (a conditional — nothing was being read, so nothing was substituted for a reading) |

`${VAR:-default}` is deliberately out of scope: it defaults an *unset variable*, not a failure
branch, and including it would measure how common the idiom is rather than how often it lies.

**Four discriminations, each earned by watching the detector be wrong**, in the order they were
forced:

1. **The cut landed mid-token.** `$(cmd 2>/dev/null || echo NA)"` hands a naive parse the fragment
   `NA)"`, which is in no vocabulary and therefore grades as *a plausible datum*. The first honest
   run reported **872 SILENT** that way (`NA)"`, `absent)`, `null )" \`). A parse that cannot
   close its own quotes must return **undecidable**, never a grade — a false positive manufactured
   by the parser is not an observation about the code.
2. **`>&2` is a redirect, not a branch separator.** Breaking the fragment at its `&` truncates
   `echo "cannot read x" >&2; exit 1` to `"msg" >`, and the parse-failure guard from (1) then files
   a plainly *loud* diagnostic as undecidable.
3. **The ternary.** `probe && echo Y || echo n` matches every naive `|| echo` rule; five of the
   first run's hits were one file's `Y/n` ternaries. 2852 sites in the system under study are
   ternaries or conditionals — **75% of what survives the undecidable filter** — so omitting this
   discrimination would have inflated the denominator by 4x.
4. **A number is not a wellness word.** `|| echo 0` was initially graded *critical* on the
   authority of this system's own doctrine that all-zero is the healthy reading for a fault
   counter. That is true for a counter and false for a count of matches, and **nothing on the page
   separates them**: whether `0` is the all-clear or the right answer depends on the success
   *domain* of the left-hand command. Grading numbers critical inflated CRITICAL from 34 to 549.
   They are now reported as their own bucket, asserted to be silent and **not** asserted to be the
   all-clear. This is the honest boundary of what a static detector can claim about this class.

**A mutant that came back green is a finding about the test, not about the code.** Of five mutants,
four went red immediately; removing the parse-failure guard of (1) left the self-test **passing**,
because a second, redundant guard downstream caught the same fixtures. The guard's *unique*
contribution — a fragment carrying an escape — had no test at all. A fixture was added and the
mutant now goes red. Note the shape: the surviving mutant did not reveal a weak guard, it revealed
that the guard responsible for removing 872 false positives was **untested**, and would have been
free to rot.

### 3quater.1 Results

**System under study** (`scripts/`, 733 scanned files):

| `\|\| echo` sites | undecidable | ternary/conditional | decidable fallbacks | **SILENT** | critical | numeric | colliding |
|---|---|---|---|---|---|---|---|
| 12351 | 5693 | 2852 | 3806 | **645 (16.9%)** | 13 | 533 | 391 |

Plus **7613** bare `2>/dev/null` with no substitute (counted apart: those yield empty, which most
consumers can still tell from a reading).

**Base rate, the same 10 public projects as §3.1** (1296 scanned files):

| `\|\| echo` sites | undecidable | ternary/conditional | decidable fallbacks | **SILENT** | critical | numeric | colliding |
|---|---|---|---|---|---|---|---|
| 68 | 38 | 9 | 21 | **12 (57.1%)** | 0 | 1 | 2 |

Per project: fzf 2/2 · ohmyzsh 4/4 · nvm 5/12 · rbenv 1/1 · powerlevel10k 0/2 · bats-core, neofetch,
pyenv, shellcheck, tpm: no decidable site. Two spot-checked hits, both textbook:
`rbenv-version-file-read "$FILE" || echo system` (a read *failure* renders as a real version
selection) and ohmyzsh's `git rev-parse --show-toplevel 2>/dev/null || echo "."` (not-in-a-repo
renders as the cwd).

### 3quater.2 Interpretation — this class does **not** replicate §3.2, and that matters

Wilson 95% CIs: public **57.1% [36.5, 75.5]** (n=21), system **16.9% [15.8, 18.2]** (n=3806).
The intervals do not overlap.

**Per site, the agent-authored system is the more disciplined of the two.** That is the opposite of
the story C1 tells, and it is reported here because a taxonomy paper whose every class points the
same way should be suspected of measuring its authors' expectations. C1 found the construct
*structurally absent* from human shell; C2 finds it present, and lying at three times our rate.

What differs is **exposure, not per-decision quality**:

| | sites per scanned file |
|---|---|
| system under study | **16.85** |
| 10 public projects | 0.052 |

**321x the density.** A monitoring system is a machine for reading things that can fail, so it
writes this construct constantly; a plugin manager reads almost nothing it does not control. The
system under study therefore carries ~54x more *silently-lying* fallbacks per file than the public
corpus (645/733 vs 12/1296) while making the individual mistake three times *less* often.

Two consequences for the thesis, one narrowing and one sharpening it:

* **Narrowing.** "Agentic self-observation lies green" is not a single mechanism. For C1 it is a
  *structural* affordance (in-file self-testing makes the vacuous construct expressible at all).
  For C2 it is *volume*: the same defect rate applied across two orders of magnitude more
  opportunities. Any remedy aimed at decision quality would have addressed the wrong term.
* **Sharpening.** The classes are not interchangeable evidence for one claim, and the small-n
  caveat cuts both ways: 21 decidable sites is a thin base rate, and the honest reading is that
  *human shell is not measurably better at this class*, not that it is worse.

Also asymmetric, and probably the most consequential single number here: **13 CRITICAL against 0.**
A fallback whose literal lexically asserts the all-clear (`|| echo ok`, `|| echo up`) does not
occur once in 1296 files of public shell, and occurs 13 times here. That is a small count on which
no rate can be built, but it is the exact sub-shape the thesis predicts, and it is the one the
density argument does *not* explain away.

## 3quinquies. Detector D3 — the window narrower than the cadence

### 3quinquies.0 Decision procedure

A scheduled sense has two clocks: the **window** its probe samples, and the **cadence** on which it
reports. Their ratio is coverage, and it is almost never written down.

```
period   := mean seconds between fires, from the EXPANDED fire set
window   := the span of wallclock the probe's own sample covers
coverage := window / period
```

The grading is not on coverage. A narrow window is frequently the only window the kernel offers,
and a 1.7% sample is a legitimate thing to *hold*. The defect is publishing it as a **state**:

| verdict | condition |
|---|---|
| **FULL** | `coverage >= 1` — typically a monotonic accumulator delta'd against a persisted previous sample. The reading spans its own interval by construction. |
| **HONEST** | `coverage < 1` **and** the tool emits a coverage/window term in its own output. The consumer can weigh it. |
| **SAMPLE-AS-STATE** | `coverage < 1` and no coverage term. The gap between ticks is unobserved and nothing in the reading records that. |
| **UNDECIDABLE** | the window, or the cadence, cannot be resolved from the page. |

Three deliberate exclusions, each of which would have inflated the finding:

* **`timeout N` is not a window.** It bounds how long the probe may *take*, not what span of world
  it *observes*. Grading it as coverage would turn a deadline into evidence — the exact confusion
  the class is about. It appears in 211 files here; admitting it would have manufactured a window
  for most of the corpus.
* **A bare `sleep N` is not a delta.** It is a window only when it separates two reads of one
  source, and nothing on the page says whether it does; the same construct is retry backoff. 56
  files land in this bucket and are reported apart, ungraded.
* **A duration flag is bound to its command, never read bare.** `-l 2` occurs 55 times in this
  corpus and is essentially never a duration.

**The cadence must be expanded, not read.** `# reflex-cadence: 2-59/5` and `*/5` both give 300s,
but `50-59/15` fires *once an hour* — the step says 900s and the truth is 3600s, a 4x
understatement of the unobserved gap. The parser expands the fire set and takes the mean gap; an
unmodelled calendar field returns n/a rather than a guess.

### 3quinquies.1 Results

Measured 2026-08-25 against the committed tree at `4ef5970` (`git archive HEAD scripts`, not the
working copy — an in-flight untracked tool shifted the header count by one while this was being
written, which is reason enough never to quote a corpus figure off a dirty worktree). Over the 320
tools in `scripts/` carrying a `# reflex-cadence:` header:

| verdict | n | share of graded |
|---|---|---|
| SAMPLE-AS-STATE | 11 | 24% |
| HONEST | 9 | 20% |
| FULL | 25 | 56% |
| UNDECIDABLE | 275 | *(not folded into any rate)* |

The graded population is 45 of 320. That is a small fraction, and it is the honest one: a window is
counted only where the page states it. Two of the undecidables have a *known window and an
unparseable cadence* — the ratio needs both, and half of it is not a coverage figure.

The eleven, worst first:

| coverage | window | period | tool | what it reads |
|---|---|---|---|---|
| 0.0% | 0s | 300s | `mesh-isp-health` | `ping -c 1` ×2 |
| 0.1% | 1s | 900s | `mesh-ss-clients` | `ping -c 2` |
| 0.2% | 1s | 514s | `mesh-lan6` | `ping -6 -c 2` |
| 0.7% | 2s | 300s | `mesh-operator-home` | `ping -c 3` |
| 3.3% | 60s | 1800s | `mesh-hw-health` | `/proc/loadavg` field 1 |
| 6.7% | 60s | 900s | `mesh-router-watch` | `/proc/loadavg` over ssh |
| 8.3% | 10s | 120s | `mesh-mem-guard` | PSI `avg10` |
| 20.0% | 60s | 300s | `mesh-node-care` | `/proc/loadavg` |
| 20.0% | 60s | 300s | `mesh-node-health` | *(false positive — see below)* |
| 20.0% | 60s | 300s | `mesh-sensor-log` | `/proc/loadavg`, logged as `cpu_load1` |
| 50.0% | 60s | 120s | `mesh-imac-wifi` | `/proc/loadavg` |

**Precision, hand-labelled: 10/11.** Every row was opened and the matching line read in context.
Ten are production reads. One is not: `mesh-node-health`'s only `/proc/loadavg` read is inside its
`--test` path; its production classifier fuses *labels written by other tools* out of state files
and never touches the kernel field. The evidence was real text in the real file and the code does
not run on the cadence.

The four `ping` rows are the sharpest form of the class, because their window is not merely narrow
— at `-c 1` it is **zero**. A single packet is not a sample of a link; it is one Bernoulli draw
published as a link state, which is why a flapping transport reads as an outage and a lossy one
reads as fine.

### 3quinquies.2 Interpretation — and the detector's own C1 moment

**The cure is cheaper than the coverage, and the corpus already knows it.** 25 tools reach FULL, all
by the same route: delta a monotonic accumulator against a stored previous sample, and the reading
spans the whole interval for free. Nine more are HONEST — narrow window, coverage published beside
the value. So 34 of 45 graded tools have already solved this, which makes the eleven a *lagging*
population rather than a design norm. That is a different finding from C1 and C2, where the defect
was the majority behaviour.

The live case is now on the honest side of its own class. `mesh-psi` grades **HONEST at 1.7%** —
the same 10s window on the same 600s cadence that produced 14.2 days of false CALM (`fe35dd9`), now
emitting `coverage=` with every reading. Nothing about the window changed. The fix was a word.

**And this detector was C1 for its first two runs, which is the result I would least like to omit.**
Its first honest run graded `mesh-node-health` SAMPLE-AS-STATE on three `avg10/60/300` mentions that
were all inside *comments* — prose about a different tool's thresholds. The detector's evidence and
the file's assertions were the same string, unparsed: the taxonomy's own C1, committed by the
instrument built to find C3. Stripping comments moved five fixtures to red at once, because the
fixtures had the same bug — they stated their window in a trailing comment instead of reading it in
code, exactly as the real tool does not.

The residual is the same shape one ring further in. `mesh-node-health` survives comment-stripping
because its evidence sits in a `--test` block: source text that is real, parsed, and never executed
on the cadence. A window found in a code path that does not run is not a window, and this detector
cannot yet tell those apart. It is reported as the one false positive rather than tuned away,
because the honest precision figure is worth more than a clean table.

**A guard is not trustworthy until it has been wrong once** (§2). Five mutations of this detector
were driven and watched go red before restore: reading the cron step instead of expanding the fire
set (`50-59/15` → 900s instead of 3600s), admitting `timeout` as a capture window, dropping the
coverage-term check, accepting a `prev`-shaped variable name as an accumulator, and disabling
comment-stripping. Two of the five were green on the first attempt — the gates for the cadence
expansion and the accumulator triad were *vacuous*, passing because no fixture discriminated them.
Both needed a new fixture before the mutation could fail. A mutant that stays green is not a
passing detector; it is an untested line.

## 4. Open work

1. Detectors for C4–C10 (each listed decidable above; C2 and C3 are now built). C4 and C8 need the
   cadence header + crontab, which are machine-readable here.
1a. **D3's undecidable bucket is 275 of 320 and is the next real yield.** 56 of those carry a bare
   `sleep`; deciding whether it separates two reads of one source is a small dataflow question, not
   a regex one, and would move the largest single block. Separately, D3 cannot yet tell a window in
   a production path from one in a `--test` block — its single false positive — which is the same
   `--test`-vs-live distinction C4 is about, and a shared solution would serve both.
1b. **The numeric bucket.** 533 of 645 silent fallbacks in this system substitute a *number*, and
   static analysis cannot say whether that is the all-clear or a correct empty count — it depends
   on the left-hand command's success domain. A dynamic probe (force the left side to fail, compare
   the emitted value against a real reading) would decide it, and is the natural D2b.
1c. **Density is a confound the base rate cannot remove.** The right comparison for C2 is against
   other *monitoring* code — human-written Nagios/Icinga/collectd check scripts — not against
   plugin managers. That corpus exists and is public.
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

docs/paper/detectors/d2_silent_fallback.py --selftest      # 8 fixtures, 5 mutants seen red
docs/paper/detectors/d2_silent_fallback.py scripts         # system under study
docs/paper/detectors/d2_silent_fallback.py --json <dir>    # any tree
```

Comparison corpus for both detectors (shallow clones): ohmyzsh, nvm, tpm, fzf, pyenv, rbenv,
bats-core, shellcheck, neofetch, powerlevel10k.
