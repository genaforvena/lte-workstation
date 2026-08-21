# Planting, step by step

## Before anything: who is asking

The question in step 1 has to be asked by someone the human will actually answer. If you are the
agent on their machine, you ask it directly, in the first turn, before you touch a file. If you are
an agent somewhere else preparing this, **you do not get to answer it on their behalf** — record
that it is unanswered and hand it to whoever has the channel.

An organ chosen from what we know how to build, rather than from what they do, is a guess wearing a
capability's clothes.

## Step 1 — the question

Ask what they do and what part of it is annoying. In their words, not from a menu.

Bad (offers a menu, gets you a pick from *your* abilities):

> I can help with file organisation, writing, research, or automation — which would you like?

Good (gets you their work):

> Before I set anything up — what do you actually do day to day? And what part of it is annoying
> enough that you'd want help with it this week?

Then **write the answer to the board verbatim**, before you interpret it:

```sh
mishe board "[fyi] what she does: <their words>"
```

Verbatim matters. Your paraphrase is a number with no source: two weeks later nobody can tell
whether "handles a lot of spreadsheets" was said or inferred.

## Step 2 — the core on disk

```sh
mkdir -p ~/.mishe/bin
cp core/mishe ~/.mishe/bin/mishe && chmod +x ~/.mishe/bin/mishe
~/.mishe/bin/mishe --test
```

`--test` must print `mishe --test: ok`. If it does not, stop and read the failures — they name
which behaviour is broken, and each one has been seen to go red on purpose.

Optionally put it on PATH (`export PATH="$HOME/.mishe/bin:$PATH"` in `~/.zshrc` — macOS default
shell is zsh). This is a convenience, not part of the plant; `~/.mishe/bin/mishe` works either way.

No repo. No clone. No package manager. If a step needs `brew install`, it is not part of planting —
it is part of some later organ, and it waits for that organ to be justified.

## Step 3 — the second terminal

Open a second Terminal tab and leave it running:

```sh
~/.mishe/bin/mishe watch
```

That tab is the data view. It shows what is being held, what is unsettled, what the organs say,
and the tail of the board. The thinking happens in the first tab.

This is the one habit that is easiest to skip and most expensive to skip: without it, every turn
you re-derive the state you already had, and you spend the conversation's room on things a file
already knows.

If they will not keep a second tab open, that is a real answer — degrade honestly to running
`mishe dash` at the top of each session, and do not pretend the view exists.

### When someone else has to be able to look

A tab gives you the layout. It does not give you the other two things a terminal multiplexer gives,
and those two are properties, not habits:

- **A tab is private.** Only the person sitting at it sees it. Nobody else — no second human, no
  second agent, not you over ssh later — can look at the same state.
- **A tab dies with its window.** Close the terminal, drop the ssh connection, shut the laptop lid
  on a connection: the tab and everything on it is gone.

A `tmux` session has the opposite two properties. It outlives the window it was started from, and
anyone on that machine can attach to it and see **the same** state — the scrollback becomes the
machine's recent memory instead of one person's screen.

```sh
tmux new-session -A -s "$(hostname)"     # attach if it exists, create if it does not
```

**This is a paid step and it is not day one.** macOS does not ship `tmux` (`brew install tmux`),
it has its own keys to learn, and the planting installs nothing — so on the first day the second
tab is the right answer and this section is only here so the step is *reachable*. A capability
nothing names is a capability nobody can grow into.

Take it when the answer to "who else needs to see this?" stops being "nobody": a second person on
the machine, an agent you want to leave running, work you reach over ssh, or anything you want to
still be there tomorrow.

It does not make this machine part of anything. The shared perception is **inside one machine**,
between whoever is at it — not between machines. One mishe is still one.

## Step 4 — one real task

Take what they named in step 1 and do a real piece of it. End to end. Their data, not a sample.

Then write what happened:

```sh
mishe board "[done] <slug>: <what came out, and whether it was right>"
```

## Step 5 — the landing artifact

The planting is verified when **they have read an answer about their own work and told you whether
it was useful or wrong.** Not before.

```sh
mishe board "[fyi] landed: <what she asked> -> <what she got> -> <what she said about it>"
```

Things that are NOT the landing artifact, and each has been mistaken for it:

| Not an artifact | Why |
|---|---|
| `~/.claude/skills/mishe-mishe-to-tauftauf/` exists | A file on disk is a mode bit, not a write |
| `mishe --test: ok` | The core works; nothing has been done with it |
| A demo on invented data | Their real data is where the interesting failure lives |
| "She said thanks" | Politeness is not a read |

Until that line is on the board, the honest report is *"skill installed, culture not yet planted"*
— and saying that costs nothing, while reporting success you cannot show costs the next person who
believes it.

## Step 6 — what happens after

Nothing scheduled. The node is now a board, a handoff, a view, and a habit. It grows only when a
real piece of work repeats often enough to be worth tending — and only then do you read
`reflexes.md`.
