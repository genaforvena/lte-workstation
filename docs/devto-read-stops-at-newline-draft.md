---
title: read stops at the newline, and your delivery check will not tell you
tags: bash, testing, debugging, devops
canonical_url:
---

> Every number, log line and command below is a live read from the machine in question,
> captured while writing. The mutant reds are reproduced here, not remembered.

A bot on one of my machines sends me things. Mostly short: an alert, a status line, a number.
Occasionally something long — a command to paste, a block of config, a diff.

For weeks the long ones arrived wrong, and I want to be precise about *wrong*, because the
shape of the wrongness is the whole story. They did not fail. They did not error. They did not
get truncated at some suspicious round number of characters. They arrived as their **first
line**, and only their first line, with no indication that anything else had ever existed.

The message I finally got annoyed enough to chase was an SSH key install. What arrived was:

```
In Termux, paste this as one line:
```

That is the sentence introducing the command. The command was on the next line. The next line
never left the machine.

## The bug is one builtin, misread

Here is the chunker, in the shape it had. Telegram caps a message at 4096 characters, so long
text gets split and sent in pieces:

```bash
chunk_one(){ printf '%s\t%s' "${1:0:3900}" "${1:3900}"; }   # "chunk<TAB>rest"

send(){
  local text="$1" chunk
  while [ -n "$text" ]; do
    IFS=$'\t' read -r chunk text < <(chunk_one "$text")
    curl -s ... --data-urlencode "text=$chunk" ...
  done
}
```

The intent reads fine in English: emit the pair joined by a tab, split it back on the tab, send
the chunk, loop on the rest. `IFS=$'\t'` even says so out loud.

`read` does not do that.

`read` splits **fields** on `IFS`. It splits **records** on the newline, and that behaviour is
not governed by `IFS` at all — it is what `read` *is*. One invocation consumes one line. So on
a payload containing a newline:

- `chunk` gets everything up to the first `\n`
- everything after it is discarded, because it was never in the record `read` consumed
- `text` is assigned the empty string
- `while [ -n "$text" ]` is therefore false, and the loop exits having sent one line

Every message I send is one line long, whether or not I wrote it that way.

## Why nothing caught it

This is the part I actually want to talk about, because the builtin trivia is a five-minute fix
and the rest is a habit worth changing.

That `send()` function is *not* naive about delivery. It does not assume `curl` exiting 0 means
anything. It parses the response and checks Telegram's own `ok:true`. It logs every send. It has
a self-test that runs hourly under a health checker.

All of it passed, the entire time, because **the damage happened upstream of the network call**.

By the time `curl` ran, the truncated text was the only text there was. Telegram received a
perfectly well-formed one-line message and said `ok:true` — correctly. The response check
verified that response — correctly. The log recorded what was sent — and the log flattens
newlines into a single line for readability, so even a human reading the log could not see that
four lines had become one. The self-test drove chunk sizes and UTF-8 boundary handling, both of
which were fine.

Nothing lied. Every component reported accurately on the thing it was looking at. The delivery
receipt was real; it just attested the bytes I *handed over*, never the bytes I *meant*.

> A delivery receipt attests the bytes you handed over, never the bytes you meant.

That sentence generalises past this bug and past this language. Any time you verify at the
boundary — HTTP status, broker ack, `ok:true`, rows-affected — you are verifying transport, and
transport is downstream of every mistake you made assembling the payload. A green boundary check
narrows the search space to "before the boundary". It does not shrink it to zero, and it is very
easy to read it as though it does.

It also explains the failure's most annoying property: it looked like a *service* problem. The
message arrived. The bot was up. The obvious hypothesis is a remote-side quirk, and the obvious
hypothesis was aimed at a system that had done nothing wrong.

## The fix is not a better delimiter

The first instinct is to pick a delimiter that survives. Use a different byte. Use `\x1f`.
Base64 the payload.

That instinct is wrong here, and it's worth saying why, because it's the reusable half.

The payload is arbitrary user text. It may contain a tab as freely as a newline. It may contain
whatever exotic separator you pick next, on the day someone pastes a hexdump into a chat window.
**In-band framing over data you do not control is always eventually wrong; the only open question
is which byte betrays you and when.**

So the split moved out of band entirely — no shared channel between producer and consumer at all:

```bash
# chunk_one — split $1 into (first 3900 chars, rest), returned in the globals CHUNK / REST.
chunk_one(){ CHUNK="${1:0:3900}"; REST="${1:3900}"; }
```

and the caller reads the two globals:

```bash
chunk_one "$text"; chunk="$CHUNK"; text="$REST"
```

Globals are not elegant. They are, however, incapable of being confused by the contents of the
string, which is the entire requirement. As a bonus the function no longer runs in a subshell per
chunk.

## The test for a newline bug can itself be eaten by newlines

Now the gate. Drive `chunk_one` with a multi-line payload and assert a verbatim round-trip.

The obvious way to build the fixture is command substitution:

```bash
_nl="$(printf 'line1\n\nline2\ttabbed\nline3\n')"    # WRONG
```

`$(...)` **strips trailing newlines**. Your fixture no longer ends in `\n`, so the assertion
covers a payload that lacks precisely the byte class under test at precisely the position most
likely to be mishandled. It passes. It asserts less than it claims, and nothing about it looks
wrong.

```bash
printf -v _nl 'line1\n\nline2\ttabbed\nline3\n'      # right: no subshell, no stripping
chunk_one "$_nl"
[ "$CHUNK" = "$_nl" ] || { echo "smoke-test: FAIL (chunk_one truncated a multi-line/tabbed payload...)"; exit 1; }
[ -z "$REST" ]        || { echo "smoke-test: FAIL (chunk_one left a remainder on a short payload...)"; exit 1; }
```

The fixture deliberately carries a blank line (two adjacent newlines), an embedded tab — the
*other* byte an in-band delimiter would have eaten — and a trailing newline. A second leg drives
a payload straddling the 3900-character boundary and asserts `CHUNK + REST` reassembles the
original, so the loop's second iteration is covered too.

A gate nobody has watched fail is not a gate, so here it is failing. I copied the fixed script,
restored the old `read`-based consumption in the copy, and ran its self-test:

```
smoke-test: FAIL (chunk_one truncated a multi-line/tabbed payload:
                  sent line1, want $'line1\n\nline2\ttabbed\nline3\n')
```

`sent line1`. The whole bug, printed by the assertion that now stands in front of it.

## One honest limitation

I wanted an end-to-end assertion: send the fixture through the real API, read it back, compare
bytes. That works for newlines — a four-line payload with a blank line round-trips through
`sendMessage` verbatim, which is the wire artifact this fix rests on.

It cannot work for the tab. Telegram renders a tab in message text as a space, so the bytes that
come back are not the bytes that went out, and no end-to-end equality can ever hold for a tabbed
payload. The tab leg tests *our* split and nothing further. The comment in the file says so, and
I am saying so here, because a reader who tries to reproduce the tab case end-to-end will get a
false negative and conclude the fix is broken.

## What I would take from this

**`read` consumes a line, not a record of your choosing.** `IFS` picks the field separator
within that line. If your data can contain a newline, `read` is the wrong tool and no `IFS`
setting fixes it.

**Verify where the data is assembled, not only where it leaves.** A boundary check is cheap and
worth having, and it will confirm delivery of whatever damage you did upstream with total
sincerity.

**Check whether your log can physically represent the failure.** Mine flattened newlines. A
newline bug was invisible in the one artifact I would have consulted first — not because the log
was wrong, but because its formatting was lossy in exactly the dimension that broke.

**Build fixtures with `printf -v`, not `$(...)`,** whenever trailing whitespace is part of what
you're testing. Otherwise the shell quietly removes the interesting part of your test case and
hands you a green.

And the one that cost the most: **the person reporting it had been right for weeks.** "This
always happens" was a precise bug report about a reproducible failure with a deterministic cause.
It sounded like a complaint about flakiness because the failure mode — content silently missing,
delivery confirmed — has no vocabulary in the language people use for bugs.
