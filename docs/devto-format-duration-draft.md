---
title: Our OGG support was a side effect of an out-of-memory guard
tags: debugging, testing, ffmpeg, devops
canonical_url:
---

A pipeline of mine grinds audio into music. You drop a file in a directory, it gets measured,
a recipe gets derived from what the measurement says the file sounds like, and a few minutes
later there's a track.

Some files came back with `skip:no-render`. Not many. And they were `.oga` — which the pipeline
explicitly declares as a supported input format, and which demonstrably worked, because other
`.oga` files ground fine.

The bug took a while to find because the thing I was looking for did not exist. There was no
"ogg is broken" state. Whether OGG was a supported format depended on how long the file was —
and, it turned out, on how *rich the file sounded*.

## The engine reads four containers

At the bottom of the stack is a grain engine that decodes audio. Its decoder handles exactly four
containers, and raises on everything else:

```python
raise Exception("File is not wav or mp3 or webm or m4a")
```

The layer above it — the archivist that watches drop directories — declares six:

```
drop|$MESH/inbox/*.aac
drop|$MESH/inbox/*.oga
drop|$MESH/inbox/*.ogg
drop|$MESH/inbox/*.m4a
drop|$MESH/inbox/*.wav
drop|$MESH/inbox/*.mp3
```

Three of those six (`.aac`, `.oga`, `.ogg`) the engine cannot read. Nothing in between converted
them. There was no normalisation step. I had never written one.

So the honest expectation is that all `.aac`, `.oga` and `.ogg` files fail, all the time, loudly,
from day one. That is not what happened. Most of them worked.

## The accident

Further up the same function there's an unrelated guard. Long sources blow up memory in the grind
stage, so there's a cap: if the source is longer than `eff_cap` seconds, trim it.

```bash
elif [ -n "$sdur" ] && [ "$sdur" -gt "$eff_cap" ] 2>/dev/null; then
  feed="/tmp/rmc-feed-$$.wav"
  ffmpeg -hide_banner -nostats -y -i "$src" -t "$eff_cap" -ac 2 -ar 44100 "$feed"
else
  feed="$src"
fi
```

Look at the output filename. The trim writes `.wav`. ffmpeg picks its encoder from the extension,
so **the cap-trim is also a format conversion** — not by design, not by anyone's decision, just
because the temp file needed a name and `.wav` is the obvious one.

That is the entire mechanism. A file longer than the cap got trimmed, and was therefore
incidentally re-encoded into a container the engine could read. A file shorter than the cap took
the `else` branch, went to the engine in its original container, and died.

**Format support was a function of duration.**

## Three records from the ledger

Every processed record is logged with its measurements and its outcome. Here are three real rows,
lightly trimmed:

```
2026-08-19T08:16Z drop 00532584 dur=55.63  rich=0.606 -> ground:l120_w8_ss0.25_...
2026-08-19T11:28Z drop 6b4a5a95 dur=241.11 rich=0.655 -> ground:l120_w8_ss0.25_...
2026-08-21T05:20Z drop a10b4867 dur=11.01  rich=0.658 -> skip:no-render(retry-exhausted)
```

| file | container | duration | cap in force | path taken | outcome |
|---|---|---|---|---|---|
| 00532584 | `.ogg` | 55.63s | 22s | over cap → trimmed → **wav** | ground |
| 6b4a5a95 | `.aac` | 241.11s | 22s | over cap → trimmed → **wav** | ground |
| a10b4867 | `.oga` | 11.01s | 90s | under cap → passed **raw** | decoder exception |

Every non-native file in the corpus that produced music had been trimmed first. The one that was
passed raw is the one that died. Same containers, same code, opposite outcomes.

## The part I did not expect

Read the "cap in force" column again. It is 22 for the first two and 90 for the third. The cap is
not a constant.

```bash
rec_ss="$(awk '{for(i=1;i<NF;i++) if($i=="ss"){print $(i+1); exit}}' <<<"$AUTOMIX_ARGS")"
eff_cap="$(awk -v c="$CAP_SECS" -v s="${rec_ss:-1}" \
  'BEGIN{ if(s+0>0 && s+0<1){ e=c*s; if(e<20)e=20; printf "%d", e } else printf "%d", c }')"
```

`ss` is the pitch-smear axis of the recipe — a musical parameter. A recipe that slows the source
down stretches it, so a superslow recipe needs a proportionally shorter feed to stay inside the
same memory budget. Perfectly reasonable. It means the cap takes one of four values: 90 seconds at
`ss >= 1`, otherwise `max(20, 90·ss)` — so 67, 45, or 22.

And where does `ss` come from?

```python
"ss": pick(SS_VALS, p_rich),
```

`p_rich` is the record's **spectral richness**, expressed as a percentile against the corpus. The
recipe generator picks more pitch-smear for richer material, because that is a musical judgement
that sounds good.

So the full chain that decided whether the pipeline could decode your file at all:

> how rich the audio sounds → its richness percentile → how much pitch-smear the recipe uses →
> the memory cap for that recipe → whether the trim fires → whether ffmpeg incidentally
> re-encodes to wav → **whether the container is supported**

Container support was downstream of an aesthetic measurement. Note that the three records above
have richness values of 0.606, 0.655 and 0.658 — a spread of five percent — and the thresholds
they got differ by more than four times. The mapping runs through a corpus-relative percentile and
a repellent that pushes away from recently-used values, so the raw number in the log does not
predict the pick. There was no threshold I could have read off and reasoned about. There was no
number in my head that was wrong; there was no number in my head at all.

## Two things kept it invisible

**The verdict named the wrong layer.** It surfaced as `skip:no-render`, which in this system means
"nothing was ever produced: the engine or its environment crashed." That is an *engine/env* claim.
Nobody reading `skip:no-render` thinks "wrong container" — they think the renderer is broken, or a
dependency moved, or the box is out of memory. The message was accurate and it aimed the diagnosis
at the wrong stratum. An error message names *a* cause, not *the* cause, and
this one cost real material: the verdict was terminal, so the record was dropped silently and
permanently.

**A partial capability is much harder to notice than an absent one.** If OGG had never worked I
would have found it the first day. Instead most OGG worked, so every test I happened to run, every
file I happened to try, every eyeball check — all green. The failures were a minority class with a
plausible-sounding verdict attached. A capability that works 80% of the time doesn't read as
broken; it reads as flaky infrastructure, which is a thing you learn to tolerate.

## What it actually cost

Telegram ships voice notes as `.oga`.

A short voice note is exactly the under-the-cap case.

The operator had asked, that same week, for more mixes made from his own voice recordings. His
most personal material was precisely the class that could never grind — while long `.oga` files
kept working, so the lane looked healthy the entire time.

That is the shape of this bug in one line: it did not take out a feature, it took out a
*correlated slice* of the inputs, and the slice was the one that mattered most.

## The fix

Convert on format, independently of length. A decode the engine cannot do is not a size problem
and must not be repaired only when the file happens to be big.

```bash
case "${src,,}" in
  *.wav|*.mp3|*.webm|*.m4a) src_native=1 ;;
  *) src_native=0 ;;
esac

if [ "$src_native" = 0 ]; then
  feed="/tmp/rmc-feed-$$.wav"
  # Still honour eff_cap: a long non-native source needs BOTH the conversion and the trim,
  # and -t with no cap would hand the grind an unbounded feed — the very OOM this guards.
  if [ -n "$sdur" ] && [ "$sdur" -gt "$eff_cap" ] 2>/dev/null; then
    ffmpeg ... -i "$src" -t "$eff_cap" -ac 2 -ar 44100 "$feed"
  else
    ffmpeg ... -i "$src" -ac 2 -ar 44100 "$feed"
  fi
  [ -s "$feed" ] || { echo "remix: format-normalise of $src produced no audio \
    (the grind engine decodes only wav/mp3/webm/m4a)"; exit 1; }
elif [ -n "$sdur" ] && [ "$sdur" -gt "$eff_cap" ] 2>/dev/null; then
  # native but too long: trim only
  ...
else
  feed="$src"
fi
```

Two separate concerns, now separately expressed: **format normalisation** (does the engine speak
this container?) and **length capping** (will this fit in memory?). They were entangled by an
implementation detail of a temp filename, and the entanglement was invisible because it lived in
ffmpeg's extension-sniffing rather than in any line of my code.

Note the failure message on the normalise path. It names the constraint — *the engine decodes only
wav/mp3/webm/m4a* — so the next person to hit a container problem is told which layer to look at
instead of being pointed at a crashed renderer.

## The test that would have caught it, and why the old ones could not

The regression test asserts the invariant directly: a non-native container is normalised
**regardless of length**.

The mechanics matter here, because the naive version of this test passes against the broken code.
The grind runs in a detached child, so asserting on the final output is slow and racy, and — worse
— a test that feeds a *long* `.oga` is green on the old code too. The test has to feed a **short**
non-native file and assert on **what the engine was handed**, not on what came out the far end. So
it points the grind directory at a fixture whose interpreter is a stub that records the path it
received, and asserts that path is a `.wav`.

And I made it fail before trusting it. On a scratch copy of the script — never the live one — I
disabled the new branch (`if [ "$src_native" = 0 ]` → `if false`) and ran its own test suite:

```
smoke-test: FAIL (format-normalise: a short .oga reached the grind engine as
'/tmp/tmp.FBazYaTZnp/short.oga'; the engine decodes only wav/mp3/webm/m4a and raises
'File is not wav or mp3 or webm or m4a', so EVERY short .oga drop renders nothing and
verdicts skip:no-render — and .oga is the operator's Telegram voice-note format)
```

That is the original bug, reproduced on demand in about a second. A gate you have not seen fail is
not a gate — and the cheap way to see it fail is to break the fix on a copy, not to trust the
commit message of whoever wrote it. (Including your own. Especially your own.)

Two details in that test worth stealing. It has an explicit arm for "the engine was handed nothing
at all" that fails with *"this gate asserts nothing"* — because a test whose subject never ran is
not a passing test. And it has an honest `n/a` arm for hosts where ffmpeg cannot encode opus, so
the fixture being unbuildable is reported rather than silently skipped into green.

## Three things I'd take to any codebase

**A capability that exists only as a side effect of an unrelated code path is conditionally
present, and the condition has nothing to do with the capability.** Nobody documents that
dependency, because nobody knows it exists. The format matrix in your head says "we support OGG."
The truth was "we support OGG above a threshold derived from its timbre."

**When a capability works *sometimes*, don't debug the failures — find what else is in the path
and ask what gates *that*.** The failing cases had nothing in common with each other. What they had
in common was the absence of something: a branch that had fired for every working file and not for
them. Diffing a failure against a success is the move; diffing failures against each other is not.

**Two concerns sharing one code path will eventually be separated by the wrong condition.** The
trim did conversion for free, so conversion inherited the trim's trigger. Any time you get
behaviour "for free" from a step that exists for another reason, you have adopted that step's
preconditions as your own — silently, and usually without noticing that you now have a
precondition at all.

---

*This is from a small self-hosted mesh where the components watch and repair each other, so bugs
like this get found by the system's own bookkeeping rather than by a user filing a ticket. The
record ledger is what made this one legible: every input carries its measurements and its verdict
on one line, which is why the duration/outcome correlation was visible at all once I thought to
look for it.*
