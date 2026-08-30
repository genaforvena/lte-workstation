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

So we checked it. And the first result looked like the README was wrong: independent readings of
the same encoded message agreed with each other **four times above chance**, with non-overlapping
confidence intervals. Something was clearly getting through.

Then we ran a second message, and the effect **reversed**.

This post is about why that reversal is the most useful thing in the experiment, and about the two
different ways a baseline can lie to you when you are measuring whether models agree. If you run
self-consistency, majority-vote ensembles, LLM-as-judge panels, or any "ask it five times and see
if it converges" pipeline, both of those failure modes are already in your numbers.

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

Here is the first message's result, positional agreement, bootstrap CIs:

```
message: "The night is long and the city keeps its silence"

A treatment      0.175   CI [0.153, 0.198]
B prior-control  0.129   CI [0.100, 0.162]
C random basis   0.044   CI [0.035, 0.053]
```

Treatment is four times the chance floor and the intervals do not touch. If you had built this
with two arms — treatment against random — you would stop here, write "independent readers converge
far above chance on the encoded message," and you would have a real, reproducible, correctly
computed number that means nothing like what you think it means.

Because arm B is *also* miles above the floor, and arm B is reading a **different message**.

Fifteen valid readings in arm A there, twelve in B, twenty in the model-free arm C; 105, 66 and
190 pairs. Then the second run:

```
message: "Rain fell across the empty market and nobody counted the hours"

A treatment      0.115   CI [0.099, 0.132]
B prior-control  0.160   CI [0.140, 0.181]
C random basis   0.047   CI [0.039, 0.056]
```

Twenty valid readings in A, fifteen in B, twenty in C. The prior control is now **above** the
treatment, and their intervals do not overlap in that
direction either (A tops out at 0.132, B starts at 0.140). Readings of a length sequence that was
never anybody's message agree with each other *more* than readings of the real one.

Both arms are far above the chance floor in both runs. The ordering between them flips. That is
what "the convergence is the prior" looks like when you finally have an arm that can show it: the
distance from random is large and stable, the distance from *each other* is noise, and no amount of
precision on the random floor would ever have told you.

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

## Convergence and correctness are different questions, so ask them separately

An arm can converge beautifully and be uniformly wrong, so recovery gets its own measurement: each
reading is compared to the true original, and to eight **decoys carrying the same length profile**.
A reading no closer to the truth than to a matched decoy has recovered nothing, however convergent
its arm is.

```
                    vs TRUE original      vs matched DECOY
message 1                  0.210                 0.216
message 2                  0.138                 0.168
```

Cosine similarity, so higher is closer. In both runs the readings are, if anything, slightly closer
to a random decoy than to the sentence that was actually encoded. The README's claim survives its
first contact with a measurement: readers do not recover the message. They converge hard, and they
are all equally wrong.

Two honest notes on those numbers. The intervals overlap in both runs — heavily in message 1, and
still overlapping in message 2 ([0.111, 0.163] against [0.146, 0.190]) — so the right reading is
"indistinguishable," not "decoys win." And the embedding metric barely
moved across every arm in either experiment. Run one: C 0.239, A 0.252, B 0.268. Run two: C 0.286,
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

That matters because the second run is the one that reverses the headline. I am confident the arm
arithmetic was unchanged — the edit added an output block — but I cannot *prove* it from the
artifact, and the fix is one line: stamp the commit hash, a dirty bit and the script's own hash
into every result file at write time. A result file that cannot name the instrument that produced
it is a measurement you have to take on trust, and the whole point of writing the numbers to disk
was not having to.

Treat the reversal as a strong signal rather than a settled fact for that reason. It is two
messages, one reader pool, one embedding model.

## What to take away

- **A floor estimated from a handful of samples rises toward the thing it is measuring**, and it
  fails toward "no effect" — the direction where nobody investigates. If your baseline is built by
  pooling from your own small sample, count the sample and say the count out loud in the output.
- **Add a prior-control arm.** Not more noise: a real run on a real different input. It is the only
  arm that separates "the model is responding to my input" from "the model does this to everything."
  It costs one more arm and it is the arm that decides.
- **Convergence is not correctness**, and they need separate measurements with separate baselines.
  Length-matched decoys are cheap and they turn "we recovered the message" into a testable claim.
- **Stamp your artifacts with the version of the code that wrote them.** Otherwise your replication
  and your original are two experiments wearing one name.

The encoding project is [genaforvena/hidden_language_of_silence](https://github.com/genaforvena/hidden_language_of_silence);
its README is where the claim being tested comes from. The measurement harness is committed but
**not yet pushed to that repo**, so the numbers above are, for now, the artifact — which is also why
every arm size, interval and per-slot figure is printed here rather than linked. The readers were a
small hosted-inference pool, the embeddings were `all-minilm` running locally, and every individual
reading is written into the JSON alongside the aggregates so the whole thing can be recomputed
without spending another token on the models.

If you want the shortest possible version to take into your own eval harness: **add the arm that
runs your pipeline on a different input, and see how much of your agreement survives it.**
