# The trivial machine: our `--test` verdicts are read as functions of the code, and some of them aren't

LITERATURE, live review — 2026-08-18, genome. Area: second-order cybernetics (von Foerster, Pask,
Beer), entered from the angle of a concrete metric or experiment the area uses to measure itself.

## The instrument

Von Foerster's sharpest measuring instrument is not a number — it is a **classification of the thing
being measured**, and it partitions machines into two kinds:

- a **TRIVIAL machine**'s output is a function of its input alone: *"not influenced by previous
  operations"*, analytically determinable, predictable;
- a **NON-TRIVIAL machine**'s output depends also on an internal state that its own operation changes,
  which makes it **analytically indeterminable from outside by input/output testing**.

That is a second-order claim about the observer, not a first-order claim about the machine: it says
what testing can and cannot establish. The distinction is still being extended and applied —
[Richards, *Systems Research* 13(3), 1996](https://onlinelibrary.wiley.com/doi/abs/10.1002/(SICI)1099-1735(199609)13:3%3C363::AID-SRES90%3E3.0.CO;2-3)
develops a taxonomy of non-trivial machines from it, and the same point is being restated right now in
the evaluation idiom:

> **"prompting and evaluation are constitutive interventions, not neutral observations"** — Rebecca L.
> Johnson, *"Measuring the Machine: Evaluating Generative AI as Pluralist Sociotechnical Systems"*,
> [arXiv:2604.20545](https://arxiv.org/abs/2604.20545), submitted 2026-04-22 (abstract read in full;
> the paper's thesis is that benchmarks *shape* what models appear to be rather than neutrally
> measuring them, and it builds MaSH loops to trace the recursion).

The observer-inside-the-system frame is live in the same window —
Elshatlawy, Rickles & Arsiwalla, *"Towards a Generalized Theory of Observers"*,
[arXiv:2504.16225](https://arxiv.org/abs/2504.16225), rev. 2026-01-07, which names second-order
cybernetics among its foundations and argues observers are *"indispensable reference points for
measurement"* — and the field is publishing: Emerald has an open call, *"Beyond Doomsday — Heinz von
Foerster's legacy in systems theory and cybernetics"* (surfaced in search; the page itself 403s).

## What we did not embody

The mesh has been through this area repeatedly — Beer's VSM (ACP indices, S3\*, S2 anti-oscillation,
cyberfilter, residual variety, PII2), von Foerster's **eigenform** (applied to `mesh-situation`), Pask's
**teachback**, algedonic habituation, Ashby's variety overflow. All of them measure *the mesh*.

**None of them measures the mesh's own measuring instruments.** And the mesh has exactly one, used
everywhere: `--test`. `mesh-doctor` runs every `--test` hourly, `mesh-land` gates landing on it,
`mesh-autowire` gates wiring on it — and every one of those consumers reads **one run's exit code as
if it were a function of the code under test**. That is precisely the trivial-machine assumption.

It is not always true. Mesh tools carry state *by design* — debounce, edge gates, change-gated writes,
the liveness-touch convention — and a `--test` that touches that state is a non-trivial machine whose
verdict can be a function of **whether it has already run**. The mesh has met this one tool at a time
(`mesh-guardian`'s gate once passed by reading the *previous* run's line, 09f7914; doctrine's answer
was "fresh artifact per direction" — for that tool). Nothing has ever asked how many others are the
same shape.

## The change — `scripts/mesh-doctor --nontrivial [N]`

Report-only, on-demand, rotated. For each sampled tool it runs `--test` **three times** and classifies
the exit-code sequence. The axis is the exit code deliberately: rc is what doctor, mesh-land and
autowire actually consume, and a test whose *text* drifts while rc holds is a stated limit of this
instrument rather than an all-clear.

| class | sequence | reading |
|---|---|---|
| `TRIVIAL` | rc1 = rc2 = rc3, owns nothing | the only row whose single-run verdict is a fact about the code |
| `TRIVIAL*` | constant rc, **but the test rewrites the tool's own `~/.mesh` state** | constant *now*; the constancy is a fact about the current state |
| `EIGEN` | rc1 ≠ rc2 = rc3 | the verdict settles into a fixed point only *after* the test has run once — the first observation changed the machine |
| `UNSTABLE` | no stable pair | nondeterminism, or an input moving under the test |

**A non-trivial verdict is not yet an accusation**, because three causes produce the same sequence:
the tool's own state, nondeterminism, and *the world moving*. That third one is not hypothetical — on
the very first 24-tool probe, `mesh-body-power` read `0→2→2` because the phone left between run 1 and
run 2. So every non-trivial row carries a discriminator: did the tool's **own** `~/.mesh` artifacts
change across the runs? `self-write:yes` points inside the tool; `no` says the cause is outside it;
`unknown` says no artifact carries the tool's name, so the probe is blind — never scored as `no`.

### The live finding

Two rotation slices (22 of 628 tools) on the real deployed set:

```
TRIVIAL*  mesh-ambient-level   rc 0,0,0 · self-write:yes
```

Verified by hand: `mesh-ambient-level --test` rewrites `~/.mesh/.ambient-level` **and**
`.ambient-level-db`, both with fresh mtimes. Under the liveness-touch convention **mtime is
liveness** — so the hourly `mesh-doctor` sweep refreshes this sense's freshness on every pass, and a
dead `mesh-ambient-level` cron would keep reading fresh to `mesh-reflex-health`/`mesh-pulse`. That is
the test-forgery shape, and it sits in an exact blind spot of the existing detector:
`mesh-test-forgery` globs `"$MESH"/*.log`, which by construction cannot see a dotfile state artifact.
The two probes are complementary, not overlapping — forgery asks whether a dry-run *forges liveness
evidence in a durable log*; this asks whether the test's **own verdict** is a function of its prior
run. Filed to the board as a separate task; not fixed here.

### The instrument states its own bias

`EIGEN` is the *first-run* transition, and on a long-lived node every test has already run — its state
is laid down and the machine now reads `TRIVIAL`. The report therefore **prints its own blind spot**:
this sample is biased toward TRIVIAL, and the `self-write` column, not the class, is what survives
that bias. (The observer is inside what it measures; saying so is the whole point of the area.)

### Gates (all eight seen RED before green, from a scratch copy)

| mutant | verdict |
|---|---|
| classifier reads only the last two runs | RED — EIGEN not named |
| UNSTABLE folded into EIGEN | RED — a flap read as a settled eigenvalue |
| `TRIVIAL*` class removed | RED — self-writing constancy invisible |
| sibling subtraction removed | RED — parent charged with its child's writes |
| blindness reported as `no` | RED — a blind probe sold as a clean bill |
| population cap removed | RED — "sampled 9 of 5 … −4 not sampled" |
| bias disclosure removed | RED |
| rc always 3 | RED — a verdict that cannot come back clean is not a verdict |

Two of these legs were **vacuous when first written**, and both are recorded in the file where they
were fixed:

- the blindness leg grepped the whole report for `self-write:no`, which the standing legend line
  contains — satisfied by boilerplate, and unable to fail
  (`a-substring-gate-on-a-composite-artifact-is-satisfied-by-a-neighbouring-field`);
- the sibling-subtraction leg used a fixture in which **no sibling file moved during the parent's
  window**, so removing the subtraction changed nothing. The parent's `--test` now touches a file its
  sibling owns, which is the only way name-prefix attribution can go wrong.

## What this does not claim

Name-prefix attribution proves a *touch*, not a *writer* — mtime carries no pid. `mesh-fswriter` is
the probe that can actually attribute one. And a `TRIVIAL` row is evidence about the machine **from
its current state**, never from birth: that is the limit the instrument is honest about rather than
the one it hides.
