---
name: mishe-mishe-to-tauftauf
description: Use when planting the mesh's working culture on a new machine through bare Claude Code — a shared written board, a handoff that survives /clear, a data view beside the thinking, and the rule that a claim is not an artifact. Also use when tending an already-planted node (adding its first organ, deciding whether a reflex has anything to tend, or checking that the planting actually took).
---

# mishe mishe to tauftauf

*Finnegans Wake 3.9. "mishe mishe" — is mise, I am; "tauftauf" — to baptise. The network says its
own name and christens a new node. It also, said aloud, is nearly "mesha".*

## What this plants

Not a system. A **working culture**, and a hundred-line script that makes the culture writable.

The mesh this comes from runs ~200 `mesh-*` tools. **None of them travel.** Almost all of them
drive organs — phones, radios, a GPU, a room microphone — that this machine does not have. A tool
that reads an organ you do not have is not a capability, it is a reflex that will go green forever
while tending nothing.

Five things travel, and they are all habits:

1. **One main channel to the human.** Pick exactly one place where you and they talk. Everything
   goes through it. A second channel does not add reach, it adds a place for a message to be
   missed in.
2. **Data beside the thinking.** A second terminal running `mishe watch` holds what you would
   otherwise re-fetch every turn. The test is mechanical: if you keep running the same probe turn
   after turn, that probe belongs in the view, not in your context.
3. **Handoff before clear.** `/clear` drops your uncommitted work-state — what was half-done, what
   is next, which files. Write it down first (`mishe handoff "…"`), read it back after
   (`mishe handoff --restore`). A clear that drops work-state is a fault, not a fresh start.
4. **The board is the shared memory.** `mishe board "…"` — the log outlives the session, the
   scrollback does not. A decision made in a conversation and never written down is real only to
   the two people who had it.
5. **A verifiable artifact instead of a claim.** Not "the script works" — the output, on disk, that
   you looked at. Not "it's installed" — the thing it was installed to do, done once, end to end.
   A permission bit is not a write; a file existing is not a file working.

## Planting: the order matters

**Step 1 is not code. Step 1 is a question.**

Ask the human what they actually spend their days on, in their words. Do not offer a menu of what
you can do — that makes them pick from your abilities instead of describing their work. Something
like: *"Before I set anything up — what do you actually do day to day, and what part of it is
annoying enough that you'd want help with it this week?"*

Until that is answered, **any first organ is a guess.** You may plant the core (step 2) without the
answer, because the core is organ-neutral. You may not pick what it tends.

**Step 2 — put the core on disk.** `core/mishe` from this skill goes to `~/.mishe/bin/mishe`,
`chmod +x`. It has no dependencies beyond what macOS and Linux ship. Nothing is scheduled, nothing
is installed system-wide, nothing runs unless run by hand. Then:

```sh
~/.mishe/bin/mishe --test          # must print "mishe --test: ok"
~/.mishe/bin/mishe board "[fyi] planted"
```

If the human is not standing there with a repo to copy from, see `reference/seed.md` — the core is
small enough to be reconstructed from a single pasted block, which is the point. Cloning a
repository is deploying a system; that is a different thing and they will not do it.

**Step 3 — one real task, end to end.** Take the thing they named in step 1 and do a real piece of
it. Small is fine. It must be their work, not a demo.

**Step 4 — the landing artifact.** The planting is not verified by `~/.claude/skills/` containing a
file. It is verified by **an answer about their real work that they actually read** and can say was
useful or wrong. Write that moment to the board with what it was. Until such a line exists, the
skill is installed and the culture is not planted, and you should say exactly that rather than
report success.

**Step 5 — reflexes, later, one at a time, and only if.** Read `reference/reflexes.md` before
scheduling anything at all. The short version: on day one there is nothing to tend, and a
scheduled thing with nothing to tend reports green forever.

## The commands

```sh
mishe board "<text>"      # write to the shared memory
mishe board -n 40         # read it
mishe open                # claims opened and never settled
mishe handoff "<state>"   # BEFORE /clear
mishe handoff --restore   # AFTER /clear
mishe dash                # the data view, once
mishe watch               # the data view, in a second terminal tab
mishe idea "<text>"       # an idea, reported
mishe drop "<text> — why" # an idea rejected, with the reason
mishe organ <name> "<cmd>" # register something worth tending
```

## Board markers

Free-form lines, but four words carry weight, because `mishe open` reads them:

- `[task] <slug> …` — an open job. The slug is the machine key.
- `[taking] <slug> …` — claimed.
- `[done] <slug> …` — settled. **The slug closes it, not the prose.** A `[done]` whose first word
  is a different slug closes a different claim, or nothing.
- `[handoff]`, `[idea]`, `[dropped]`, `[fyi]` — everything else.

A `[task]` or `[taking]` that never gets its `[done]` is a promise nobody is holding. `mishe open`
is the whole detector.

## How to act, once planted

- **Act, then report.** No paragraph explaining what you are about to do. Do it, then one sentence
  on what came out.
- **Ideas do not need approval — they need to be reported.** If you think of something, say it and
  go. The mirror of that: if you consider an idea and reject it, **write down why** (`mishe drop`).
  A rejection that is only silence is indistinguishable from never having thought of it.
- **When you are unsure, ask on the one channel** rather than guessing and building.
- **State results plainly.** If it failed, say so with the output. If you skipped part of it, say
  which part. Do not report a claim in the shape of an artifact.

## When NOT to use this

- The machine already runs the full mesh (`~/.local/bin/mesh-*`). This is the seed of that culture,
  not a second copy of it — planting it there gives you two boards.
- Someone wants a specific tool built. Build the tool. The culture is for ongoing work, not for a
  one-off.

## Reference

- `reference/planting.md` — the step-by-step, including what to do when the human answers step 1.
- `reference/reflexes.md` — when a reflex is honest and when it is decoration. Read before cron.
- `reference/seed.md` — getting the core onto a machine with no repo and no clone.
- `core/mishe` — the whole implementation. It is meant to be read; it is one file.
