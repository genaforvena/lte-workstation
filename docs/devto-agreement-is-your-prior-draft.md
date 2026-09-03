---
title: Your models agreed with each other. They were agreeing with themselves.
tags: ai, machinelearning, llm, testing
canonical_url:
---

There is a small art project in our house that encodes a sentence as nothing but its word
lengths. Each word becomes a run of some symbol, repeated once per letter; the symbol itself is
chosen at random and carries nothing. "The night is long" becomes four clusters of length 3, 5, 2,
4. That is the entire channel. A reader — human or model — gets the lengths and nothing else.

The project's README makes a claim I liked: that LLM readers *never recover the intended meaning*,
that they generate from structure and bias, and that every reading is a projection. It is the most
interesting sentence in the repository and nobody had ever checked it.

So we checked it. And the honest version of the result is stronger than the first
version I published here: independent readings of the same encoded message agree with each
other far above chance — and they agree with each other **no more than readings of a
different message do**. Across four runs, the treatment arm has never once beaten its own
prior control. That is the whole post in one sentence.

> **Correction, 2026-08-30.** The first version of this piece said the second message
> showed the opposite ordering of the first — treatment ahead in run one, prior control
> ahead in run two. That
> framing was wrong, and the error was mine: the first run's intervals overlap
> ([0.153, 0.198] against [0.100, 0.162]), so there was never an effect there for run two
> to answer.
> The two replication runs (equal arms, 20/20, zero misses) both overlap too. What survives
> is cleaner and harder than the first telling: one arm that has never once beaten its own
> prior
> control. The conclusion stands; the evidence under it is now the replicated one. Details
> in "Way two", "A third way a floor lies", and the per-slot replication below.

This post is about why that comparison is the most useful thing in the experiment, and about
the three
different ways a baseline can lie to you when you are measuring whether models agree. If you run
self-consistency, majority-vote ensembles, LLM-as-judge panels, or any "ask it five times and see
if it converges" pipeline, all three of those failure modes are already in your numbers.

## The measurement

Encode a known sentence. Take N *independent* readings — separate processes, no shared context,
because one sampled list of five guesses is one reading, not five. Then measure how much the
readings agree **with each other**.

The obvious way to do that is to compare the agreement against random chance, and that is where it
goes wrong. The design that survived contact needs three arms, not two:

| arm | what it is | what it isolates |
|---|---|---|
| **A** treatment | N readings of the true message's length sequence | channel + prior |
| **B** prior control | N readings of a *different* length sequence — same word count, lengths resampled from the same distribution | the prior and the task framing alone, with no particular message behind it |
| **C** random basis | N texts assembled with **no model at all**: a random word of the right length at each slot | the chance floor |

Every text within an arm shares a length profile, so *positional* agreement is well defined: do two
independent readings put the same word in slot 4? That is the metric that carries the argument
below. Jaccard over word bags and cosine over sentence embeddings were computed too, and I will
come back to why the embedding metric turned out to be worthless here.

## Way one that a floor lies: it rises to meet you

The first version of arm C built its random texts from a vocabulary pooled out of arm B's own
readings. This is a very natural thing to do — you want the "random" texts to be made of words the
model would actually use, so you harvest them from the model's own output. Otherwise you are
comparing model English against dictionary English and the gap is meaningless.

With seven valid control readings, the pooled vocabulary was so small that the random texts came
out as near-duplicates of each other. The floor rose to **cosine 0.391 — above the model readings
it was supposed to sit under, at 0.232.**

The comment that now sits in the code is the best artifact in the whole project, and I am quoting
it verbatim rather than paraphrasing it:

> Pooling the basis out of the control arm's few readings — the first version of this — is not a
> floor. Seven texts yield a vocabulary so small that the random texts built from it are
> near-duplicates of each other, which inflates every agreement metric and inflates the SEMANTIC
> one worst (measured: cosine 0.391 for a basis pooled from 7 texts, ABOVE the model readings it
> was supposed to sit under). **A floor that rises with how little you sampled it is not a floor.**

Note what that failure would have done if it had gone the other way. A floor built from *plenty* of
samples is fine. A floor built from a handful is inflated, and an inflated floor makes a real effect
disappear. You would have concluded "no signal" and shipped that, and the number would have looked
completely reasonable — a baseline at 0.391, a treatment at 0.232, no effect, move on. Nothing in
the output says "this floor was estimated from seven things."

The fix is to draw the alphabet from a request that is independent of any message — "list 240
common English words, mix lengths 1 to 12" — so it is still the model's own vocabulary but it
cannot inherit the convergence it is meant to measure. The run prints which source it used, and
says so in the saved artifact when it has to fall back.

## Way two that a floor lies: it is measuring the wrong competitor

Here are all four runs, positional agreement, bootstrap CIs, arm sizes shown because an
agreement number with no n is not a measurement:

```
OLD message 1 (n=15/12/20, 105/66/190 pairs):
A treatment      0.175   CI [0.153, 0.198]
B prior-control  0.129   CI [0.100, 0.162]
C random basis   0.044   CI [0.035, 0.053]   (alphabet: 134 words)

OLD message 2 (n=20/15/20, 190/105/190 pairs):
A treatment      0.115   CI [0.099, 0.132]
B prior-control  0.160   CI [0.140, 0.181]
C random basis   0.047   CI [0.039, 0.056]   (alphabet: 129 words)

NEW message 1 (n=20/20/20, 190 pairs each, zero misses):
A treatment      0.112   CI [0.096, 0.127]
B prior-control  0.099   CI [0.084, 0.115]
C random basis   0.023   CI [0.017, 0.030]   (alphabet: 303 words)

NEW message 2 (n=20/20/20, 190 pairs each, zero misses):
A treatment      0.129   CI [0.109, 0.150]
B prior-control  0.122   CI [0.107, 0.137]
C random basis   0.017   CI [0.011, 0.022]   (alphabet: 337 words)
```

Read the intervals, not the point estimates. The first version of this post called OLD
message 1 an effect — 0.175 over 0.129 — and OLD message 2 the opposite. That was wrong:
OLD message 1's intervals **overlap** ([0.153, 0.198] against [0.100, 0.162]), and neither
of us checked the intersection before publishing. There was never an A-ahead leg for run
two to answer. Across all four runs the treatment arm is **never** separated from the prior
control, and the only separated comparison in the whole set goes the other way (OLD
message 2, B above A, disjoint). Both replication runs have equal arms (20/20, zero
compliance misses) where both old ones did not (15v12, 20v15) — not claimed as the cause
of the old separation, only noted that the separation does not survive equal arms.

So this is not "message 1 shows an effect, message 2 answers it." It is one arm that has
never once beaten its own prior control — a cleaner and harder version of exactly the
claim this post makes. Both arms sit far above the chance floor in every run. The distance
from random is large and stable, the distance from *each other* is noise, and no amount of
precision on the random floor would ever have told you.

## A third way a floor lies: it moves with a draw you did not fix

Arm C is not comparable across runs. The floor is a function of the alphabet drawn that
run — 134 words then, 303 now for message 1; 129 then, 337 now for message 2 — and it
halved between the draws: 0.044/0.047 then, 0.023/0.017 now. So "treatment is 4x the
floor" (old) and "treatment is 7.7x the floor" (new) are not the same measurement getting
stronger; they are two different floors. Never quote the ratio without its alphabet size.
The run prints which source the alphabet came from and how many words it holds, and the
saved artifact carries both, for exactly this reason.

The general form, and it is not about this art project at all:

**Random noise is not what your model's agreement is competing against. Its own prior is.** A
baseline made of noise answers "is the model doing something other than nothing," which is almost
never the question. The question is "is the model doing something other than what it would have
done anyway," and only a control arm that is a real run on a real *different* input can answer it.

If you evaluate self-consistency, this is the arm you are missing. Sampling the same prompt five
times and finding 80% agreement is not evidence the model knows the answer until you know what five
samples of a *neighbouring* prompt agree at. Very often it is 75%.

## Where the agreement actually sat

The saved artifact keeps agreement per slot, and this is where the whole thing becomes legible.
First message, agreement at each position, with the position's word length:

```
slot                 0     1     2     3     4     5     6     7     8     9

lengths (A and C)    3     5     2     4     3     3     4     5     3     7
A treatment         .63   .23   .36   .06   .17   .03   .07   .00   .10   .11
C random basis      .03   .05   .10   .02   .03   .02   .03   .06   .03   .10

lengths (B)          3     4     5     5     3     3     7     3     3     3
B prior control     .68   .05   .09   .09   .14   .02   .03   .17   .02   .02
```

Arm B is listed separately because it is reading its own resampled length profile — that is the
whole point of it — and only slot 0 happens to be three letters in both.

Slot 0 is a three-letter word. The readings agree there 63% of the time. The prior-control arm — a
different message — agrees there **68%** of the time, *more* than the treatment arm. Both are
producing "The" and "All". The random basis, same length, same alphabet, no model, agrees 3%.

And it is not even a *length* effect. Slots 4, 5 and 8 are all three-letter words too, and they
come in at 17%, 3% and 10%. What the models agree on is that English sentences start with "The".
That is the entire signal, sitting in position zero, present just as strongly when there is no
message behind the lengths at all.

Aggregate it and the shape holds: words of three letters or fewer agree at 0.257 in treatment and
0.172 in the prior control; words of five letters or more — the only ones that could carry any
content — agree at 0.114 in treatment and 0.071 in the control, against a 0.067 floor. On the
content words, the treatment arm is a hair above chance and the control arm is sitting on it.

The convergence is English's function-word skeleton. It was never the channel.

That per-slot figure replicates hard in the direction used here. NEW message 2, slot 0:
B prior-control **0.637** vs A treatment **0.274** vs C random **0.016** — the arm reading
a *different* message agrees at slot 0 more than twice as often as the arm reading the
real one. Content words (>=5 letters) in the same run sit at A 0.037 vs B 0.059 vs
C 0.012. Readers converge on "The" and are equally wrong everywhere else.

## Convergence and correctness are different questions, so ask them separately

An arm can converge beautifully and be uniformly wrong, so recovery gets its own measurement: each
reading is compared to the true original — and the comparison that decides is against **arm
B**, real readings of a *different* length sequence by the same model under the same framing.
Length-matched decoys and arm C are scored too, as chance floors for context. They are not
the test.

> **Correction, 2026-08-30.** The first version of this section compared readings to the
> true original against length-matched *decoys* (message 1: 0.210 vs 0.216; message 2:
> 0.138 vs 0.168) and concluded "no closer to the truth than to a decoy." That is an
> A-vs-chance comparison, not A-vs-prior: measured on the same runs, the decoy floor is
> 0.153 and the model-free arm C is 0.159 — the same number — while the prior-control arm
> sits at 0.220. This post's own thesis is that a noise floor cannot separate a signal
> from your own prior, and the recovery paragraph beside it used a noise floor. Right
> conclusion, wrong comparison — the weakest way to be right. The numbers below are
> recomputed from the stored readings under the prior floor (n=20/arm, no new model calls).

```
recovery, cosine similarity (higher = closer), same runs:
message 1:  A (vs true) 0.240 / B_prior 0.220 / C 0.159
            A minus B_prior  +0.020  CI [-0.045, +0.084]  (includes 0)
message 2:  A (vs true) 0.112 / B_prior 0.124 / C 0.116
            A minus B_prior  -0.012  CI [-0.052, +0.027]  (includes 0)
```

Both include 0 — conclusion unchanged, evidence now the right shape. And there is a
stronger paragraph here than the one first published: under the old decoy floor the two
messages *disagreed* (message 1 read as recovery, message 2 did not), which invites
quoting whichever suits. Under the prior floor both say the same thing. The wrong floor
made the two runs contradict each other.

Cosine similarity, so higher is closer. In both runs the readings are indistinguishable
from the prior arm's distance to the truth. The README's claim survives its first contact
with a measurement: readers do not recover the message. They converge hard, and they
are all equally wrong.

Two honest notes on those numbers. Both A-minus-prior intervals include 0
([-0.045, +0.084] and [-0.052, +0.027]) — so the right reading is
"indistinguishable," not "the prior wins." And the embedding metric barely
moved across every arm in the two runs that had an embedding backend. Run one: C 0.239, A 0.252, B 0.268. Run two: C 0.286,
A 0.293, B 0.273 — where the **model-free** arm outscores the prior control. A spread of three
hundredths across arms that the positional metric separates by a factor of four, and the arm with
no model in it landing in the middle, is what a metric with no discriminative power looks like. A sentence-embedding
model asked to compare ten words of grammatical nonsense has nothing to grip.
The positional metric carries the argument; the semantic one should not be quoted on its own.

## The defect I found in our own artifacts

I did not run these; I read the saved JSON to decide whether it was worth writing up. And the two
result files were **not written by the same instrument**, which nothing in either file says.

The first file carries a per-slot breakdown. The second does not — and the second is the *newer*
file on disk, written under four minutes after the commit that added that breakdown. Python reads its
source once, at start. The second run was already in flight when the harness was edited, so it ran
the old code to completion and wrote pre-edit output with a post-edit timestamp. The only evidence
is a **key missing from one file**, which is the weakest possible signal and looks exactly like a
run that had nothing to report.

That matters because the second run is the one the first version of this post built its
headline on. I am confident the arm
arithmetic was unchanged — the edit added an output block — but I cannot *prove* it from the
artifact, and the fix is not what this section first prescribed. The original text here said:
stamp the commit hash, a dirty bit and the script's own hash into every result file at write
time. That remedy is **refuted** — drilled, not argued: a run launched at one commit and
committed to another mid-flight makes a write-time stamp record the commit that never ran,
confidently wrong where a missing key is at least honestly silent. The actual fix, now in
the harness: the stamp is taken **twice**, at import and at write, and their disagreement
is a named field (`at_start` is what produced the numbers; `changed_mid_run` asserts a
mid-run edit instead of leaving it to be inferred from an absence). A result file that
cannot name the instrument that produced it is a measurement you have to take on trust,
and the whole point of writing the numbers to disk was not having to.

No opposite-ordering claim is made anywhere in this piece any more, so treat the four runs above as
replicated evidence rather than a settled fact for a different reason: it is two
messages, one reader pool, one embedding model.

## What to take away

- **A floor estimated from a handful of samples rises toward the thing it is measuring**, and it
  fails toward "no effect" — the direction where nobody investigates. If your baseline is built by
  pooling from your own small sample, count the sample and say the count out loud in the output.
- **A floor drawn fresh each run is a different floor.** The chance arm halved between draws here
  (0.044/0.047 at 134/129 words, 0.023/0.017 at 303/337). Quote the ratio with its alphabet
  size or do not quote it.
- **Add a prior-control arm.** Not more noise: a real run on a real different input. It is the only
  arm that separates "the model is responding to my input" from "the model does this to everything."
  It costs one more arm and it is the arm that decides.
- **Convergence is not correctness**, and they need separate measurements with separate baselines.
  A noise floor (decoys, model-free arm) answers "fluent English or word salad," never "recovered
  the message" — that question belongs to the prior arm, and the wrong floor made these two runs
  contradict each other.
- **Stamp your artifacts with the version of the code that wrote them — twice, at start and at
  write.** A write-time stamp alone records the commit that was not running when the tree moved
  mid-run. Otherwise your replication
  and your original are two experiments wearing one name.

The encoding project is [genaforvena/hidden_language_of_silence](https://github.com/genaforvena/hidden_language_of_silence);
its README is where the claim being tested comes from. The measurement harness is pushed:
[measure/](https://github.com/genaforvena/hidden_language_of_silence/tree/main/measure) carries
the four result files (`result-msg1.json`, `result-msg2.json`, `result-msg1-stamped.json`,
`result-msg2-stamped.json`), the recovery recompute, and its own README — every figure above
is recomputable from the stored readings without spending another token. The readers were a
small hosted-inference pool, the embeddings were `all-minilm` running locally, and every individual
reading is written into the JSON alongside the aggregates.

If you want the shortest possible version to take into your own eval harness: **add the arm that
runs your pipeline on a different input, and see how much of your agreement survives it.**
