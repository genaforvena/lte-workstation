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

## How to run this: the demo comes first, and the demo is mortal

**You are not delivering a fixed sequence.** You are having a conversation whose next step depends
on their last answer. But the ORDER is fixed at the front, and it is the opposite of the obvious
one (operator, 2026-08-21): **nothing is asked until something has been seen.** No question about
their experience, no question about their work, no description of what a mesh is. A description
buys nothing; five minutes of watching one buys the whole conversation.

### Step 1 — is there a tmux? That is the only thing you check first

```sh
command -v tmux
```

**No tmux → install NOTHING.** Not the core, not a second terminal tab, not a board. Ask one
question and stop:

> There's a thing I could show you, but it needs `tmux` and this machine doesn't have it. Want me
> to install it (one command), or shall I just tell you what I can do without it?

A machine without tmux is not a machine to be fixed on the way to a demo. Their answer decides
whether there is a demo at all, and "no" is a complete answer.

**tmux is here → raise the baby, live, in front of them.**

```sh
mkdir -p ~/.mishe/bin && cp core/mishe ~/.mishe/bin/mishe && chmod +x ~/.mishe/bin/mishe
~/.mishe/bin/mishe --test          # must print "mishe --test: ok"
~/.mishe/bin/mishe view            # up: session mishe-demo-<pid>, windows mind + data
```

No repo, no clone, no package manager. If they have no repo to copy from, `reference/seed.md` — the
core is one file small enough to reconstruct from a pasted block, which is the point.

#### The session has its OWN, ephemeral name — and this is the load-bearing part

`view` raises **`mishe-demo-<pid>`**. Never the hostname-named session. Never a fixed shared
`mishe` either. This is not tidiness:

**Killing a tmux session is the ONE sanctioned exception to the mesh's append-only rule** — a
session is somebody's workspace and its scrollback is that machine's recent memory — and the
exception is only sanctionable while the session being killed is provably ours. A name lookup
cannot tell you whose session it found. So an earlier `view` that looked up the hostname session
adopted a stranger's workspace and injected a window into it; a `view` that looked up a constant
`mishe` merely made that rarer. **On a machine already running the full mesh, the first mishe
planted would find a live session and one `burn` later take the node down with the baby.**

Two things make the exception narrow enough to keep: the name is one nobody else would mint, and
`view` writes a **receipt** (`~/.mishe/.raised`) on the branch that CREATES a session and not on
the branch that finds one. `burn` kills only what that receipt names. A session wearing our name
that we have no receipt for is refused out loud, never adopted.

#### Then show four things happening, in this order

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
4. **A stop lands where they are looking.** Stop the data view and the stop is *visible* — it does
   not vanish into a window nobody reads. `mishe organ x "exit 3"` then `mishe dash` shows
   `FAILED rc=3`, not a blank. Then remove it. The point being made is that this thing does not lie
   when it is broken, and that a failure in one half surfaces in the half the human is watching.

Adapt the narration to who they turn out to be — you learn that from how they react, not from a
questionnaire. Someone who reaches for the keyboard gets handed `tmux attach -t mishe-demo-<pid>`.
Someone who watches gets no explanation until they ask; a thing that visibly moves teaches faster
than a paragraph. Someone who says "I don't want a terminal thing" is telling you to stop, and you
stop — `mishe board` and `mishe handoff` alone are still the culture and need no layout.

### Step 2 — ask whether it lives

Now, and only now, the first real question:

> That is the whole thing. Do you want to keep it, or should I remove it?

Both answers are fine and **you must mean that**. Then:

- **"Remove it"** → `mishe burn`, one phrase, in front of them. It prints what it killed, then
  re-scans and prints that nothing is left: the session, `~/.mishe`, the board, the handoff, the
  crontab lines, the rc line, the skill. Nothing remains.

  **This is the demonstration arriving, not the demonstration failing.** That mishe died, it cost
  nothing to lose, and it grows again in one phrase on any machine. A thing you can end in one
  phrase is a thing you can afford to try — the mortality is what made the planting cheap enough
  to say yes to in the first place, so watching it die is watching the claim get paid.

  Do not argue. Do not offer a reduced version. Do not leave "just the board, in case" — an
  "everything except…" turns the one honest promise in this skill into a lie. Then thank them and
  stop.
- **"Keep it"** → it is now theirs, and it is still just as mortal.

### Step 3 — only now, ask what they actually want

Whichever way step 2 went — kept or buried — the question about them has now earned its place:

> What do you actually do day to day, and what part of it is annoying enough that you'd want help
> with it this week?

In their words, never from a menu of your abilities — a menu gets you a pick from what you can do
instead of a description of what they do. Write the answer to the board **verbatim**; your
paraphrase is a number with no source. If the baby was burned, write it wherever you and they
actually talk.

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

- **It kills only sessions it raised.** Two mechanisms, and it needs both. `view` raises a name
  nobody else would mint (`mishe-demo-<pid>`), and writes a receipt (`~/.mishe/.raised`) on the
  branch that *creates* a session and never on the branch that finds one. `burn` kills only what
  that receipt names. **Killing a tmux session is the one sanctioned exception to the mesh's
  append-only rule** — a session is somebody's workspace and its scrollback is that machine's
  memory — and the exception holds only for a session this mishe raised and wrote down. Never kill
  by name match. An earlier `view` adopted the machine's hostname-named session and injected a
  window into a stranger's workspace; renaming it to a constant `mishe` made that rarer without
  making it impossible, which is the frequency at which a silent adoption does its damage — nobody
  is watching when it finally happens. A session wearing our name with no receipt behind it is now
  **refused out loud**, and the refusal names what it is leaving alone.
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
mishe view                 # raise the layout: session mishe-demo-<pid>, two windows (installs nothing silently)
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
- They said they do not want a terminal thing. Hear it and stop — the board and the handoff are
  still the culture and need no layout. (There is no longer a question standing between them and
  the demo, so this one has to be heard whenever they say it, including mid-walkthrough.)

## Where this gets proved

**The acceptance polygon is `opencode` + `deepseek`, not Claude** (operator, 2026-08-21). This
skill is written to be run by *bare* coding agents on someone else's machine, so a walkthrough that
only ever succeeds under the model it was authored with has been tested against its author, not
against its job. A cheaper, blunter engine is where the implicit steps show up: an instruction that
reads as obvious here and gets skipped there was never an instruction, it was an assumption.

Run it end to end there before believing any of the above — and when it breaks, the fix goes in
this file, not in a note about which model to use.

## Reference

- `reference/planting.md` — the branches in detail, and what to do with each answer.
- `reference/reflexes.md` — when a reflex is honest and when it is decoration. Read before cron.
- `reference/seed.md` — getting the core onto a machine with no repo and no clone.
- `core/mishe` — the whole implementation. It is meant to be read; it is one file.
