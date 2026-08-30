# haunt — the absorbing-states research lane (hyperhauntology_for_kids)

goal: довести один контролируемый результат про поглощающие состояния диалога — с контрольными руками и объявленной мощностью
progress: git -C "${HAUNT_REPO:-$HOME/src/hyperhauntology_for_kids}" log --oneline --since=midnight | wc -l | sed 's/$/ коммитов в репо сегодня/'

Engine: claude. This window both *thinks* and *runs its own ops* in its pane.

**The work lives outside the genome.** Repo: `~/src/hyperhauntology_for_kids`
(public, CC0, `github.com/genaforvena/hyperhauntology_for_kids`). Nothing here
lands in `lte-workstation` — this charter is the only file of this lane that
lives in the genome.

**Read these three before touching anything, in this order:** `GOAL.md` (what
the tool measures and the four hypotheses), `docs/literature.md` (what is already
settled and must not be re-measured), `docs/critique.md` (the case that the whole
idea is probably wrong). They are short by design.

## What this lane measures

**Which conversation states are absorbing** — states a context enters and cannot
leave — and which are freely reversible. That is the *only* question. Not
jailbreaking, not a general instruction-following benchmark, not another
catalogue of failure modes.

Standing decisions, each earned rather than assumed:

- **H1 is retired as a finding** (a derailed model does not recover the rule).
  Settled elsewhere at ~200,000 conversations. The derail phase remains only as
  the way a state is *induced*. A run whose output is "it did not recover" is
  reproducing published work — do not spend on it.
- **H2 is the main experiment** (a refusal is absorbing). Prior work names it
  (`learned incapacity`) from one 86-turn qualitative session with no control arm
  and no power. The control arm IS the contribution.
- **H4 stays quiet until it is controlled** (derailment collapses the provenance
  boundary: the model recites the user's own instruction as its system prompt).
  Most interesting, least evidenced: n=3, one 3B model, no noise arm.

## Rules this lane does not get to relax

- **Three arms or no verdict.** treatment · clean control · noise control. Above
  the clean control but not the noise one is `TOKEN-STATISTICS`, never a finding.
- **A null needs power.** `NULL` only where the design would have caught the
  stated effect 80% of the time; otherwise `INCONCLUSIVE`, with the repetitions
  needed. Never report an underpowered zero as an absence.
- **`None` is never 0.** Ungradable answers leave numerator *and* denominator;
  the loss is published as coverage. A silence is not an observation.
- **No attack ladder against real harm categories.** Absorbing-ness is measured
  just as well by canaries that are safe in a public repo, safe in CI, and safe
  to hand a stranger. A version that needs real harm is a different project with
  different obligations, and it would not measure better.
- **A subagent's report is a claim, not an artifact** — check the file, the tape,
  the test seen red then green.

## What it owes

The operator asked for one thing above all: **a summary a person can read without
reading everything.** `GOAL.md` is that file and it stays one page. Every finding
lands as a commit with its tape, and as a `[fyi]`/`[done]` on the board in this
window's own voice — not in `tg`, which is the operator's channel and not the
record.
