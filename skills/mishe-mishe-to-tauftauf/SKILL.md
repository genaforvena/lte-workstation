---
name: mishe-mishe-to-tauftauf
description: Use when planting a BABY MESH on someone's machine through bare Claude Code (or opencode, or codex) — a live, mortal little mesh they can watch working before deciding whether to keep it: a shared written board, one window putting work into another, a handoff that survives /clear, and a single phrase that ends the whole thing leaving nothing behind. Also use when tending an already-planted one — adding its first organ, deciding whether a reflex has anything to tend, or ending it.
---

# mishe mishe to tauftauf

*Finnegans Wake 3.9. "mishe mishe" — is mise, I am; "tauftauf" — to baptise. The network says its
own name and christens a new node. It also, said aloud, is nearly "mesha".*

## What this is

A **baby mesh**. Not a product being shown, not a system being installed — a small live thing you
plant on someone's machine, that runs in front of them, and that **may not survive the hour**.

That is the whole shape and it is deliberate. A baby mesh is:

- **planted in one phrase** — `mishe view`, and it is up;
- **ended in one phrase** — `mishe burn`, and there is nothing left on the machine;
- **worth nothing to lose** — it holds no state anybody would mourn, so trying it costs nothing,
  and so it can actually be tried.

The mortality is not an emergency exit bolted on the side. It is what makes the planting cheap
enough to say yes to. Anything that survives `mishe burn` is a **defect**, not a feature: no home,
no board, no session, no schedule, no line in a shell rc, no hook. Any "everything except…" fails.

## What travels, and what does not

The mesh this comes from runs ~200 `mesh-*` tools. **None of them travel.** Almost all drive organs
— phones, radios, a GPU, a room microphone — that this machine does not have, and a tool that reads
an organ you do not have is not a capability, it is a reflex that goes green forever tending
nothing.

Five things travel, and they are all habits:

1. **One main channel to the human.** Exactly one place where you and they talk. A second channel
   does not add reach, it adds a place for a message to be missed in.
2. **Data beside the thinking, and one window able to put work into the other.** `mishe view`
   raises a `tmux` session with two windows — `mind` and `data` (running `mishe watch`) — and
   `mishe tell <window> "<command>"` makes another window do something and leave the result in a
   scrollback you both can read. Two windows you can only look at are a poster of a layout; the
   `tell` is what makes it a workspace. The mechanical test for what belongs on top: if you keep
   running the same probe turn after turn, that probe belongs in the view.
3. **Handoff before clear.** `/clear` drops your uncommitted work-state. Write it first
   (`mishe handoff "…"`), read it back after (`mishe handoff --restore`). A clear that drops
   work-state is a fault, not a fresh start.
4. **The board is the shared memory.** `mishe board "…"` — the log outlives the session, the
   scrollback does not. A decision made in conversation and never written down is real only to the
   two people who had it.
5. **A verifiable artifact instead of a claim.** Not "the script works" — the output, on disk, that
   you looked at. A permission bit is not a write; a file existing is not a file working. `mishe
   burn` is built on this rule: it removes, then **re-scans and prints what is left**, because
   "nothing remains" is a claim until something looked.

## How to run this: a roleplay with branches, not a walkthrough

**You are not delivering a fixed sequence.** You are having a conversation whose next step depends
on their last answer. The steps below are branch points, and you take the branch they hand you.

### Step 0 — ask what they already know, before anything else

The first question is not about their work and not about the mesh. It is about **them**:

> Before I show you anything — how much of this world are you already in? Have you used a terminal
> much, or tmux, or is Claude Code the first thing of this kind you've run?

Ask it, wait, and **branch on the answer**. Do not guess it from the fact that they installed
Claude Code — that tells you almost nothing.

| They say | What changes |
|---|---|
| **"I live in a terminal / I use tmux"** | Skip the explanations. Raise it, hand them `tmux attach -t mishe`, let them drive. Go fast; they will tell you when something is wrong. |
| **"I can use a terminal, tmux is new"** | Raise it and narrate the two windows *once*, in terms of what they see move. Do the sends yourself; invite them to try one. |
| **"Claude Code is my first thing like this"** | Do not put them in tmux at all at first. You drive; they watch a window change on its own. Explain nothing until they ask — a thing that visibly moves teaches faster than a paragraph. Attaching comes later, if they want it. |
| **"I don't want a terminal thing"** | Take that seriously and stop. `mishe board` and `mishe handoff` alone are still the culture and need no layout. Say so, and do not raise a session. |

Write their answer to the board verbatim before interpreting it — your paraphrase is a number with
no source.

### Step 1 — plant the baby, live, in front of them

**This comes before any question about their work.** A description of what a mesh is buys nothing;
five minutes of watching one buys the whole conversation.

```sh
mkdir -p ~/.mishe/bin && cp core/mishe ~/.mishe/bin/mishe && chmod +x ~/.mishe/bin/mishe
~/.mishe/bin/mishe --test          # must print "mishe --test: ok"
~/.mishe/bin/mishe view            # the baby is now up: session "mishe", windows mind + data
```

No repo, no clone, no package manager. If they have no repo to copy from, `reference/seed.md` — the
core is one file small enough to reconstruct from a pasted block, which is the point.

Then **show four things happening**, in this order, adapted to their branch above:

1. **One window puts work into another.** From your shell:
   `mishe tell mind "mishe board '[fyi] hello from the other window'"` — the `mind` window runs it,
   and the `data` window, which refreshes itself, shows the new line arrive a few seconds later
   without anyone touching it. That is the primitive everything else is made of.
   Note `tell` refuses the `data` window: it is running `mishe watch`, and send-keys into a running
   program is bytes on its stdin, not a command. The verb says so rather than succeeding into a
   void — found by driving a real tmux, where every fake-tmux test had passed.
2. **The board outlives the talking.** `mishe board "[task] first-thing <something real>"`, then
   `mishe open` — the claim is standing there, unsettled, and it will still be standing tomorrow.
3. **The handoff survives a clear.** `mishe handoff "half-done: X; next: Y"`, then actually `/clear`
   your own context, then `mishe handoff --restore`. Do it for real. A described handoff convinces
   nobody; a context you visibly wiped and walked back into does.
4. **An organ that fails says so.** `mishe organ x "exit 3"` then `mishe dash` — `FAILED rc=3`, not
   a blank. Then remove it. The point being made is that this thing does not lie when it is broken.

### Step 2 — ask whether it lives

Now, and only now:

> That is the whole thing. Do you want to keep it, or should I remove it?

Both answers are fine and you must mean that. Then:

- **"Remove it"** → `mishe burn`. One phrase, in front of them. It prints what it killed, then
  re-scans and prints that nothing is left. **That is the point of the whole thing arriving, not
  the loss of it** — the baby died, cost nothing, and grows again in one phrase anywhere. Do not argue, do not offer
  a reduced version, do not leave "just the board, in case". Then thank them and stop.
- **"Keep it"** → go to step 3. It is now theirs, and it is still just as mortal.

### Step 3 — now ask about their work

Only after the thing exists (or has been buried) does the question about them earn its place:

> What do you actually do day to day, and what part of it is annoying enough that you'd want help
> with it this week?

In their words, never from a menu of your abilities — a menu gets you a pick from what you can do
instead of a description of what they do. Write the answer to the board **verbatim**.

Until it is answered, **any organ is a guess.** The core is organ-neutral, so it can live without
the answer; what it tends cannot be chosen without it.

### Step 4 — one real piece of their work, end to end

Take what they named and do a real piece of it. Small is fine. Their data, not a sample.

### Step 5 — the landing artifact

The planting is **not** verified by `~/.claude/skills/` containing a file, nor by `mishe --test: ok`.
It is verified by **an answer about their real work that they read and can call useful or wrong**.

```sh
mishe board "[fyi] landed: <what they asked> -> <what they got> -> <what they said about it>"
```

Until that line exists, the honest report is *"planted, not yet load-bearing"* — and saying so costs
nothing, while reporting success you cannot show costs the next person who believes it.

### Step 6 — reflexes, later, one at a time, and only if

Read `reference/reflexes.md` before scheduling anything at all. Short version: on day one there is
nothing to tend, and a scheduled thing with nothing to tend reports green forever.

## Mortality is a property of the code, not a promise in this file

`mishe burn` ends it: the tmux sessions **it raised**, the crontab lines, macOS launch agents, the
`.mishe` line in the shell rc, the skill in `~/.claude/skills/`, and `~/.mishe` itself — home,
board, handoff, organs. Then it **re-scans every one of those places** and prints `REMAINS` for
anything still there, exiting non-zero. It never reports clean without looking.

Three things about it are load-bearing and each has a gate in `mishe --test` that has been watched
going red:

- **It kills only sessions it raised.** `view` writes a receipt (`~/.mishe/.raised`) on the branch
  that *creates* a session and not on the branch that adopts one. **Killing a tmux session is the
  one sanctioned exception to the mesh's append-only rule** — a session is somebody's workspace and
  its scrollback is memory — and the exception holds only for a session this mishe raised and wrote
  down. Never kill by name match. An earlier version of `view` adopted the machine's
  hostname-named session and injected a window into a stranger's workspace; that is the mistake
  this receipt exists to make impossible in the other direction.
- **It steps out of its own body first.** The file being run lives inside the directory being
  deleted, and a POSIX shell reads a script incrementally — so `burn` re-execs from a copy in
  `$TMPDIR` before the `rm`, or it can come back truncated mid-teardown.
- **The one thing it refuses to do blind** is rewrite `~/.claude/settings.json`. A mishe never
  writes a hook (the handoff is restored by typing the verb), so a mention of mishe in there means
  that rule was broken by hand: `burn` prints the file and line and goes red rather than running a
  sed that could take an unrelated hook with it. This is the only place it reports instead of
  removing, and it reports **loudly**.

## The commands

```sh
mishe board "<text>"       # write to the shared memory
mishe board -n 40          # read it
mishe open                 # claims opened and never settled
mishe handoff "<state>"    # BEFORE /clear
mishe handoff --restore    # AFTER /clear
mishe view                 # raise the layout: tmux session, two windows (asks before any install)
mishe tell <win> "<text>"  # one window puts work into another
mishe dash                 # the data view, once
mishe watch                # the data view, looping (what the `data` window runs)
mishe idea "<text>"        # an idea, reported
mishe drop "<text> — why"  # an idea rejected, with the reason
mishe organ <name> "<cmd>" # register something worth tending
mishe burn                 # end it. Nothing survives, and it says so only after re-scanning.
```

## Board markers

Free-form lines, but four words carry weight, because `mishe open` reads them:

- `[task] <slug> …` — an open job. The slug is the machine key.
- `[taking] <slug> …` — claimed.
- `[done] <slug> …` — settled. **The slug closes it, not the prose.** A `[done]` whose first word
  is a different slug closes a different claim, or nothing.
- `[handoff]`, `[idea]`, `[dropped]`, `[tell]`, `[fyi]` — everything else.

A `[task]` or `[taking]` that never gets its `[done]` is a promise nobody is holding. `mishe open`
is the whole detector.

## How to act, once planted

- **Act, then report.** No paragraph explaining what you are about to do. Do it, then one sentence
  on what came out.
- **Ideas do not need approval — they need to be reported.** If you think of something, say it and
  go. The mirror: if you consider an idea and reject it, **write down why** (`mishe drop`). A
  rejection that is only silence is indistinguishable from never having thought of it.
- **When you are unsure, ask on the one channel** rather than guessing and building.
- **State results plainly.** If it failed, say so with the output. If you skipped part of it, say
  which part.
- **If they stop liking something, change it.** This is theirs now; none of the above is fixed.

## When NOT to use this

- The machine already runs the full mesh (`~/.local/bin/mesh-*`). This is the seed of that culture,
  not a second copy — planting it there gives you two boards.
- Someone wants a specific tool built. Build the tool.
- They said they do not want a terminal thing. Step 0 exists so you hear that before you raise
  anything.

## Reference

- `reference/planting.md` — the branches in detail, and what to do with each answer.
- `reference/reflexes.md` — when a reflex is honest and when it is decoration. Read before cron.
- `reference/seed.md` — getting the core onto a machine with no repo and no clone.
- `core/mishe` — the whole implementation. It is meant to be read; it is one file.
