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

Two cross-cutting observations that are not classes but govern all of them:

* **Liveness-touch**: a reflex that writes its state only when the value *changes* leaves mtime
  frozen on a long-stable-but-live value, so an mtime watchdog reads "value held" as "reflex dead".
  Decouple *ran* from *changed* (`f3f84c1`).
* **Honest n/a is free**, and therefore becomes a resting state: an organ that answers "cannot
  assess" forever is indistinguishable from a healthy quiet one on every axis a reflex-health tool
  computes. Five organs in this corpus had *never* emitted an informative line, all green.

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

## 4. Open work

1. Detectors for C3–C8 (each listed decidable above). C4 and C8 need the cadence header + crontab,
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
