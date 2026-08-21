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

No repo. No clone. No package manager. The core installs nothing and neither does the plant —
`mishe --test` asserts it by shimming the package managers and failing if any of them is *run*.
`tmux` in step 3 is the one thing a human may choose to install, by answering a question that
`mishe view` puts to them; printing the command is not running it, and the gate knows the
difference.

## Step 3 — the layout, in one verb

```sh
~/.mishe/bin/mishe view
```

That is the whole step. It raises a `tmux` session named `mishe` with **two windows**: `mind` (where
the thinking happens) and `data` (running `mishe watch` — what is held, what is unsettled, what the
organs say, the tail of the board). Run it again later and it attaches to the same session instead
of rebuilding it.

This is the one habit that is easiest to skip and most expensive to skip: without the second window,
every turn re-derives state a file already knows, and the conversation's room goes on re-fetching.

### If the machine has no tmux

`mishe view` **does not install it.** It prints one question for you to ask the human, in their
terms, and the exact command. Ask it — do not decide for them, and do not quietly fall back:

> I can keep the data view in a second terminal tab — that works, but only you can see it and it
> dies with the window. Or I can install tmux (one command) and the view lives in a session that
> survives the window and that anyone on this machine can attach to. Want me to install it?

- **Yes** → they (or you, with their word) run `brew install tmux` / `sudo apt-get install -y tmux`,
  then `mishe view` again.
- **No** → a second terminal tab running `~/.mishe/bin/mishe watch`, and **write the degrade to the
  board** so the missing property is a recorded fact rather than an assumption:
  `mishe board "[fyi] view: no tmux, second tab only — private to one screen, dies with it"`.

Most machines answer this question by already having tmux: on Linux it is nearly always there, so
the question never gets asked and nothing gets installed. macOS is where it is a real question, and
one direct question is cheaper than a dependency taken on someone's behalf.

### Why a session and not a tab — the two properties

A tab gives you the layout. It does not give the two things that make the view *shared memory*, and
those are properties, not habits:

- **A tab is private.** Only the person sitting at it sees it. No second human, no second agent,
  nobody over ssh later can look at the same state.
- **A tab dies with its window.** Close the terminal, drop the connection, shut the lid: gone.

A session has the opposite two. It outlives the window it was started from, and anyone on that
machine can attach and see **the same** state — the scrollback becomes the machine's recent memory
instead of one person's screen.

It does not make this machine part of anything. The shared perception is **inside one machine**,
between whoever is at it — not between machines. One mishe is still one. Nothing is scheduled and
nothing phones home; `mishe view` only ever talks to `tmux` on this host.

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
