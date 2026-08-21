# Planting a baby mesh — the branches

This is the detail behind SKILL.md. It is not a script to read out. Each section is a **branch
point**: you ask, they answer, and their answer picks the next section. If you find yourself
delivering these in fixed order regardless of what they said, you have stopped having the
conversation and started performing it.

## Before anything: who is asking

If you are the agent on their machine, you ask the questions directly, in your own turns, before
touching a file. If you are an agent somewhere else preparing this, **you do not get to answer them
on their behalf** — record that they are unanswered and hand it to whoever has the channel.

## Branch 0 — is there a tmux? (the ONLY thing checked before the demo)

**Reversed 2026-08-21, on the operator's instruction: nothing is asked until something has been
seen.** This section used to open with a question about how much terminal the person had used, and
called it the branch "nothing downstream is right until this is answered". That was backwards. A
question asked before anything exists is a question about a thing they cannot picture yet, and the
answer you get back is a guess about a guess. The demo is what makes the later questions answerable.

So exactly one check comes first, and it is about the MACHINE, not the person:

```sh
command -v tmux
```

**No tmux → install NOTHING and ask one question.** Not tmux, not the core, not a second tab, not a
board file. Nothing lands on that machine:

> There's a thing I could show you, but it needs `tmux` and this machine doesn't have it. Want me
> to install it (one command), or shall I just tell you what I can do without it?

Then stop and take the answer. "No" is complete — a machine without tmux is not a machine to be
quietly fixed on the way to a demo, and taking a dependency on somebody's behalf to reach your own
demo is the thing this whole skill is against. If they say yes: install tmux, then Branch 1.

The old second-tab fallback is **retired**. It read as harmless because a tab installs nothing —
but reaching it meant copying the core to `~/.mishe` first, so "nothing was installed" was already
false by the time the question got asked. One question, nothing on disk, is the honest version.

**tmux is here → Branch 1, immediately.** No questionnaire.

## Reading them while it runs (this is not a gate)

You still need to know who you are talking to. You learn it from how they react to a thing that is
already moving, which is better evidence than an answer to "have you used tmux". The four readings
below used to be Branch 0's answer table; they are now adjustments you make mid-walkthrough.

### "I live in a terminal / I use tmux"

Say almost nothing. Raise it and hand them the handle:

```sh
~/.mishe/bin/mishe view          # they are now inside it
```

Let them drive. Point at exactly one thing they will not guess — `mishe tell` — and stop talking.
They will find the rest and they will tell you what is wrong with it, which is the useful part.

### "I can use a terminal, but tmux is new"

Raise it, then narrate **once**, in terms of what moves on screen rather than in terms of what tmux
is:

> Two windows in one session. The bottom one is where we talk. The top one is showing what this
> machine is holding right now, and it refreshes itself — so I stop asking it the same question
> every few minutes and you can see the same thing I see.

Do the first `mishe tell` yourself so they watch the other window act. Then invite exactly one:

> Try one: `mishe tell mind "mishe board '[fyi] hi'"` — then watch the top window notice it.

`Ctrl-b n` to move between windows, `Ctrl-b d` to detach, `tmux attach -t mishe-demo-<pid>` to come back. Three
keys, not a tour.

### "Claude Code is my first thing like this"

**Do not put them inside tmux.** Raise the session detached and drive it yourself:

```sh
MISHE_VIEW_ATTACH=0 ~/.mishe/bin/mishe view
```

Show them a window changing on its own before you explain what a window is. Something that visibly
moves teaches faster than any paragraph, and a person who has just been dropped into a terminal
multiplexer is not learning, they are coping. Attaching is something to offer later, if they ask
what else is in there.

Everything the culture is actually made of still works with no layout at all: `mishe board`,
`mishe open`, `mishe handoff`. If tmux never becomes interesting to them, they have lost nothing
important.

### "I don't want a terminal thing"

Stop. Say plainly that the board and the handoff are the whole culture and need no layout, offer
those two, and **do not raise a session**. Then write it down:

```sh
mishe board "[fyi] no layout: they don't want a terminal thing. Board + handoff only."
```

A degrade that is recorded is a fact. A degrade that is not is an assumption someone will later
mistake for a capability.

## Branch 1 — the baby, planted live

```sh
mkdir -p ~/.mishe/bin
cp core/mishe ~/.mishe/bin/mishe && chmod +x ~/.mishe/bin/mishe
~/.mishe/bin/mishe --test
```

`--test` must print `mishe --test: ok`. If it does not, stop and read the failures — each names one
behaviour, and each has been watched going red on purpose.

Optional, and not part of the plant: `export PATH="$HOME/.mishe/bin:$PATH"` in `~/.zshrc` (macOS
default shell is zsh). `mishe burn` knows about that line and removes it; nothing else you add by
hand is guaranteed to be found, so if you add something, add it to the burn scan too.

No repo, no clone, no package manager. The core installs nothing and neither does the plant —
`mishe --test` asserts this by shimming the package managers and failing if any of them is *run*.
`tmux` is the one thing a human may choose to install, by answering a question `mishe view` puts to
them; printing the command is not running it, and the gate knows the difference.

### The four things to show, in this order

1. **One window puts work into another** — `mishe tell mind "mishe board '[fyi] hello'"`, and then
   the self-refreshing `data` window shows the line arrive with nobody touching it. This is the
   primitive; everything else is habit built on it.
   It refuses two things rather than pretending: a window that does not exist (tmux would resolve
   the name loosely, and a command typed into the wrong window is not undone by re-sending), and a
   window running a **program** rather than sitting at a prompt — `data` is running `mishe watch`,
   so send-keys there is bytes into a loop's stdin and nothing happens. Aim at `mind`, or at a
   window you added.
2. **The board outlives the talking** — `mishe board "[task] <slug> …"`, then `mishe open`. The
   claim is standing there unsettled, and it will still be standing tomorrow.
3. **The handoff survives a clear** — write one, then actually `/clear` your own context, then
   `mishe handoff --restore`. **Do it for real.** A described handoff convinces nobody; a context
   you visibly wiped and walked back into does.
4. **A broken organ says it is broken** — `mishe organ x "exit 3"`, `mishe dash` → `FAILED rc=3`,
   not a blank line. Then remove it. What is being shown is that this thing does not go quiet when
   it fails.

### If the machine has no tmux

Handled in Branch 0, before anything is copied: **one question, nothing installed.** `mishe view`
itself still refuses to install tmux — it prints the question and the exact command — but by the
time `view` could run, the core is already on disk, so the check belongs earlier than the verb.

Most Linux machines answer this by already having tmux, so the question never gets asked. macOS is
where it is a real question, and one direct question is cheaper than a dependency taken on
somebody's behalf.

### Why a session and not a tab

A tab gives you the layout and neither of the two properties that make the view *shared memory*:

- **A tab is private.** Only the person at it sees it — no second human, no second agent, nobody
  over ssh later.
- **A tab dies with its window.** Close the terminal, drop the connection, shut the lid: gone.

A session has the opposite two: it outlives the window it was started from, and anyone on that
machine can attach and see **the same** state. It does not make this machine part of anything —
the shared perception is *inside one machine*, between whoever is at it. Nothing is scheduled and
nothing phones home; `mishe view` only ever talks to `tmux` on this host.

## Branch 2 — does it live

> That is the whole thing. Do you want to keep it, or should I remove it?

You must mean both. If your next sentence after "remove it" is an argument for keeping it, the
question was theatre and they will hear that.

### "Remove it"

```sh
~/.mishe/bin/mishe burn
```

In front of them. It prints what it killed, then re-scans every place a mishe can leave a trace and
prints that nothing is left. Do not offer a reduced version. Do not leave "just the board, in
case" — a leftover is the one thing that turns a cheap experiment into an installation they did not
agree to. Then thank them and stop.

The thing to say afterwards, if anything: it cost nothing to lose, and it grows again anywhere in
one phrase. That is the property, and burning it is the only way to actually show it.

**Killing a tmux session is the one sanctioned exception to the mesh's append-only rule.** A
session is a workspace and its scrollback is memory. The exception holds only for a session this
mishe raised, and TWO things keep it that narrow: the session wears a name nobody else would mint
(`mishe-demo-<pid>`, never the hostname and never a shared constant), and `view` writes a receipt
(`~/.mishe/.raised`) on the branch that CREATES it and never on the branch that finds one. `burn`
kills what the receipt names and nothing else. Never kill a session by name match, not even during
a burn — a name lookup cannot tell you whose session it found, which is exactly how an earlier
`view` came to inject a window into a stranger's workspace.

And the stakes scale with the machine: plant a fixed-name mishe on a node already running the full
mesh and the first `view` finds a live session, the first `burn` takes the node down with the baby.

The thing being demonstrated here is not tidiness. **The death is the product.** They watched a
live thing end in one phrase and leave nothing, which is the only way to actually show that trying
it cost them nothing — a promise of reversibility is worth exactly what a demonstrated one is not.

### "Keep it"

It is theirs, and it is exactly as mortal as it was a minute ago. Say that once, plainly, and move
on to their work.

## Branch 3 — their work

```
What do you actually do day to day? And what part of it is annoying enough that you'd want help
with it this week?
```

Bad, because it gets you a pick from *your* abilities instead of a description of their work:

> I can help with file organisation, writing, research, or automation — which would you like?

Write the answer to the board **verbatim**, before you interpret it:

```sh
mishe board "[fyi] what they do: <their words>"
```

Verbatim matters. Your paraphrase is a number with no source: two weeks later nobody can tell
whether "handles a lot of spreadsheets" was said or inferred.

## Branch 4 — one real task

Take what they named and do a real piece of it, end to end, on their data. Then write what happened:

```sh
mishe board "[done] <slug>: <what came out, and whether it was right>"
```

## Branch 5 — the landing artifact

The planting is verified when **they have read an answer about their own work and told you whether
it was useful or wrong.** Not before.

```sh
mishe board "[fyi] landed: <what they asked> -> <what they got> -> <what they said about it>"
```

Things that are NOT the landing artifact, each of which has been mistaken for it:

| Not an artifact | Why |
|---|---|
| `~/.claude/skills/mishe-mishe-to-tauftauf/` exists | A file on disk is a mode bit, not a write |
| `mishe --test: ok` | The core works; nothing has been done with it |
| A run on invented data | Their real data is where the interesting failure lives |
| "They said thanks" | Politeness is not a read |
| The baby is still up | Surviving is not being useful |

Until that line is on the board, the honest report is *"planted, not yet load-bearing"*.

## Branch 6 — after

Nothing scheduled. It is a board, a handoff, a view, a `tell`, and a habit. It grows only when a
real piece of work repeats often enough to be worth tending — and only then read `reflexes.md`.

And it stays mortal. If it stops earning its place, `mishe burn` is still one phrase.
