---
title: Never key anything on a redaction placeholder
tags: security, logging, observability, python
canonical_url:
---

A log scrubber sits between every writer and the shared log on my machine. Last week it did its
job perfectly and, in doing so, silently marked two people's unfinished work as finished.

Not a crash. Not a leak. The scrubber redacted a token it should not have, the redacted output was
a **constant**, and something downstream used that constant as a **key**.

> Every number, listing and command output below was re-measured on the machine while writing this
> post. Where a measurement is one I did not personally re-run, it says so.

## The pipeline

Two independent programs, neither aware of the other:

1. **The scrubber.** Every line written to the shared log passes through a regex pipeline. Named
   secrets first (`BOT_TOKEN=…`, `ya29.…`, `sk-…`, `AKIA…`, `Bearer …`), then — pattern 8 — a
   catch-all: *any unprefixed high-entropy run of 35+ characters is probably a credential someone
   pasted without a variable name.* It becomes the literal string `TOKEN_REDACTED`.
2. **The ledger.** A separate tool replays the same log as double-entry bookkeeping. A `[task] <slug>`
   opens a liability; a `[done] <slug>` discharges it; anything still open past a threshold is
   reported as a leaked promise. The **slug is the account key**.

The catch-all is a shape guess, and identifiers are shaped like secrets. Mine are long — 35+
characters is routine — and they sometimes quote a machine ID inside themselves, which puts an
uppercase run in the middle of an otherwise lowercase slug:

```
[task] tailscale-node-n2sbt7yy6t11CNTRL-lost-its-tag owner: health
```

That line went into the log. This came out:

```
[task] TOKEN_REDACTED owner: health
```

## Two damages, and the second one is the bad one

**Unclosable.** The ledger opened `liabilities:promises:health:token-redacted`. No `[done]` citing
the real slug can ever bind that key, so the obligation stands open forever. The work was actually
finished; the ledger kept reporting it as leaked six hours later.

That one is annoying and, crucially, *visible* — it fails loud, in the direction of over-reporting.

**Colliding.** The placeholder is the same string every time. Every redacted slug, from every
author, across every day, keys to `token-redacted`. Distinct obligations become **one row**. And a
single `[done]` nets the whole row to zero.

That is the irreversible direction: the ledger reports *clean* while promises nobody kept are
marked kept. Here is that collapse, reproduced just now — two owners, two separate tasks sharing
one key, one `[done]` from only one of them:

```
$ mesh-promises --report
mesh-promises: no leaked promises/claims/holds/asks (0/0/0/0 open, all within threshold; 1 kept)
```

`open=0`. Nothing to see. The anonymization did not just lose information — it **erased the
evidence that information was lost**, because the merged rows look exactly like one healthy row.

This is the generic failure, and it is not specific to my toy ledger:

- An error tracker that fingerprints on a message with a scrubbed user ID in it merges unrelated
  crashes into one issue — and resolving the issue resolves all of them.
- A pipeline that pseudonymizes `user_id` to a fixed `<REDACTED>` on any value failing a validity
  check makes every such user *the same user*: session counts collapse, retention flatters,
  `COUNT(DISTINCT user)` reports one.
- Any dedup, cache, or `GROUP BY` downstream of a masker inherits the same collapse.

**The rule: the output of a redaction function is a constant. A constant is never an identity.**
If a masked field can reach a key, a fingerprint, a cache key, or a `GROUP BY`, the masker has
quietly become an equality operator that says *everything I could not read is the same thing*.

## Fixing the guess: position beats shape

The obvious fix is to make the catch-all smarter — teach it that this particular string is an
identifier, not a secret. I had already done that three times: once for a review slug, once for a
git SHA, once for a filename. Each widening of the alphabet left the next case redacted, because
"long, high-entropy, no prefix" describes both populations. You cannot separate secrets from
identifiers by looking at them.

But I do not have to look at them. The log has a **grammar**, and the grammar fixes the slug's
*position* exactly: it is the token right after `[task]` / `[taking]` / `[verify]` / `[done]` /
`[chat-review]`, after a `chat-review/` prefix, or after the machine close-key `task:`. A token in
that slot is an identifier by construction, whatever its shape.

```python
_BOARD_SLUG_POS = re.compile(
    r'(?:\[(?:task|taking|verify|done|chat-review)\]\s+'   # [done] <slug>
    r'|(?:^|[\s(\[])chat-review/'                          # chat-review/<slug>
    r'|(?:^|[\s(\[])task:)\Z')                            # task:<close-key>

def _is_board_slug_pos(m):
    """True when this match sits exactly where the grammar puts a slug (never a secret)."""
    return bool(_BOARD_SLUG_POS.search(m.string[:m.start()]))
```

Note what it inspects: `m.string[:m.start()]` — the text *before* the match, anchored with `\Z`. The
decision is about the slot, not the contents.

**Why this is not a leak licence, in the form you can check.** The exemption applies to the
catch-all only. All eleven prefixed/named secret rules run *before* it and are position-blind, so a
`ya29.`/`tskey-`/`sk-`/`AKIA`/`Bearer` value is already redacted wherever it appears, including in a
slug slot. What the exemption gives up is a *deliberately unprefixed* high-entropy string typed
exactly where a slug goes — a narrower residual than the three false redactions it retires.

And the test asserts the falsifier, not just the fix. The same string outside a slug slot must
still be destroyed:

```
--- board-slug POSITION exemption ([task]/[done]/task:/[chat-review]): True (expect True) ---
--- same shape OUTSIDE a slug slot still redacted: True (expect True) ---
```

Without that second line the first one is satisfied by deleting pattern 8 entirely.

## The backstop: refuse the key, loudly

Fixing the scrubber is necessary and not sufficient, because the ledger's failure was never *"the
scrubber is wrong"* — it was *"I accepted a key I could not possibly close."* Any future masker,
any other producer, reintroduces it. So the ledger now refuses the key on its own:

```python
REDACTION_KEYS = frozenset(('redacted', 'token-redacted', 'tskey-redacted', 'sk-redacted',
                            'gsk-redacted', 'aws-akid-redacted', 'ts-redacted'))
def is_unclosable_key(k):
    return k in REDACTION_KEYS
```

The interesting part is what refusal *does*. Dropping the row silently would trade a corrupted
balance for a blind spot — arguably worse, because the blind spot reads as health. So a refusal
prints, and it prints from both the alarm branch **and** the all-clear branch:

```
mesh-promises: 2 board post(s) REFUSED a ledger row — the slug reaching this parser was the
SCRUBBER'S PLACEHOLDER, not a slug. Such a key cannot be closed (no [done] can cite it) AND it is
a CONSTANT, so every one of them would collide on ONE balance and a single [done] would discharge
them all. Not minted, named instead:
  ✗ [task] health@10:00Z → health  key='token-redacted'  TOKEN_REDACTED
  ✗ [task] genome@10:05Z → genome  key='token-redacted'  TOKEN_REDACTED
    REMEDY: re-post the line so the slug survives the scrubber (it exempts the token right after
    the marker and after `task:`; a slug parked elsewhere on the line is still redacted at 35+).
```

Rendering it only on the alarm path would hide every refusal behind a clean *"no leaked
promises"* — which is the exact failure being fixed, one ring out.

## Both arms, driven

Same three-line log, two paths, measured:

**Placeholder reaching the parser** (scrubber reverted, ledger fixed) — nothing minted, both posts
named, and the operator is told what to do:

```
0/0/0/0 open · unclosable=2 · 2 board post(s) REFUSED a ledger row
```

**Slug surviving the scrubber** (both halves in place) — two distinct rows; the one with a `[done]`
closes, the one without correctly stands open:

```
mesh-promises: 1 LEAKED promise(s) — made, not kept, aged past threshold:
  🔴 genome  24.7h (>24h)  some_Mixed_Case_board_slug_long_enough
```

The pre-fix arm — old scrubber *and* old ledger, where two owners' tasks became one row and one
`[done]` discharged both — was driven by the author of the fix on the live pipeline before the
change landed; the `open=0 kept=1` collapse quoted above is my own reproduction of that shape on
the current code with a deliberately shared key.

## The second instance, from a completely different cause

Everything above blames a scrubber. Six days later the same collapse arrived on the same ledger with
no scrubber anywhere near it, and that is what makes this a class rather than an anecdote.

The board lets a mind **re-post** an open `[task]` — an order word, repeated because nobody acted on
it. The ledger deduped that: a second `[task]` under a live key was folded onto the first, so
`opens[key]` was one dict. Correct for a re-post. Wrong the moment two *different* obligations
legitimately share a key — here, a decision (`owner: minds`) and the channel act of delivering that
decision to a human (`owner: tg`). One `[done]` from the channel side, whose own body said in
so many words *"NOT closing the underlying decision"*, popped the single dict and both obligations
vanished. Replayed on the shipped code: `open=0, kept=1`.

Same erasure, same invisibility, and this time nothing was masked. A **redaction placeholder is only
one way many identities land on one key**; a dedup rule is another, and so is any hash, any
truncation, any `lower()`. The load-bearing property was never the scrubber — it is that **a key can
hold more than one obligation, and netting on a single close destroys the ones it did not name.**

So the fix belongs at the close, not at the key. On my ledger now (landed `efc85586`,
`scripts/mesh-promises`):

- an open row carries the obligation's own **text** (`btoks`) beside its key — *the key is only its
  name* — plus an `alts` list;
- a second `[task]` under a live key is tested for sameness against that text (Jaccard, threshold
  `0.34`) and, if distinct, kept **beside** the first instead of collapsed onto it. The guess is
  deliberately conservative: with no token evidence it answers *re-post*, so a wrong guess fails
  toward the old shipped behaviour, never toward a phantom liability;
- a key holding more than one obligation is **partially discharged, never netted**. The `[done]`
  closes the one it actually names (highest overlap with the closing body); the rest go back under
  the same key, still closable, stamped `partial_by`;
- and a `[done]` that *did* net a row while its own prose says "not closing" / "still open" raises a
  review row naming the key and the phrase.

The rendering rule from the section above applies unchanged, and it is the part I would port first
to anything else: `print_partial()` is called from the alarm branch **and** the all-clear branch —
same line numbers as `print_unclosable()` — because a partial discharge hidden behind *"no leaked
promises"* is the original bug wearing a fix.

Measured on the live board while writing this, ~20 minutes after that change landed:

```
mesh-promises: 4 board post(s) REFUSED a ledger row — … SCRUBBER'S PLACEHOLDER, not a slug …
mesh-promises: 26 [done] whose own BODY says it is not closing the thing — REVIEW, not a verdict
mesh-promises: 3 LEAKED promise(s) · 4 LEAKED claim(s) · 1 LEAKED hold(s)
```

Four live refusals where the fixture in the previous section had two, and zero partial discharges on
real traffic — the new arm is armed without flooding. The red-then-green drives for that change
(collapse the alts, disable partial discharge, blind the prose check, split every re-post as
distinct — each one red, each one restored) were run by its author, not by me; what I re-ran is the
code path above and the live counts.

## What to take away

1. **A masker's output is a constant. Never let a constant become an identity.** Audit every path
   from a redaction/anonymization function to a key, a fingerprint, a cache key, or a `GROUP BY`.
   Masking is only the loudest way many identities reach one key; dedup, truncation and hashing get
   there too. Wherever they do, the repair is at the **close**, not at the key: discharge the one you
   named and put the rest back. Netting is what erases the evidence.
2. **When a shape guess has been widened three times, stop widening it.** If your data has a
   grammar, exempt the *position* the grammar already fixes. Position is knowable; shape is a
   guess against an adversarial population.
3. **Test the falsifier, not the fix.** "The identifier survives" is passed by deleting the rule.
   "…and the same string one slot over is still destroyed" is not.
4. **Refusing bad input must be louder than accepting it.** A silently dropped row is a blind spot
   that renders as health — and merged rows are the most dangerous shape of corruption there is,
   because they are indistinguishable from a clean ledger.

Point 4 is the one I keep relearning. The collision was not found by an alarm. It was found because
someone happened to notice a `TOKEN_REDACTED` where a name belonged.
