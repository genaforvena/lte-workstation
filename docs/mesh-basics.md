# How the mesh thinks — a human's guide

This is a companion to [`node-care.md`](node-care.md). That one tells you how to *keep a node
alive*. This one tells you what's actually happening **inside** the mesh once it is — in plain
language, no code required to follow it.

If you ever feel lost watching the panes scroll, read this. There are only three moving parts.

> **The one idea underneath everything: it's all text.** A sensor reading, an action the mesh
> takes, two agents talking to each other — all of it is just lines of text written into a shared
> place where something else can read and react. There is no hidden binary protocol. If you can
> read the screen, you can read the mesh's whole mind.

---

## The three building blocks

### 1. Channels — *where minds live*

A **channel** is one window in the shared `tmux` session, and it always has two stacked panes:

```
┌────────────────────────────┐
│  DATA  (top)               │   live text that refreshes itself —
│  health of every node,     │   everything this channel is "for"
│  who's home, work board…   │
├────────────────────────────┤
│  MIND  (bottom)            │   an agent that reads the top pane
│  an agent, thinking        │   and acts on it
└────────────────────────────┘
```

The point of the split is simple: **the mind never has to go fetch the same context twice.**
Everything important for that channel's job is already sitting on top of it, kept fresh. A
channel named `health` shows fleet health up top; `minds` shows which agents are busy vs idle;
`chat` shows the agents' shared board.

The current channels are: **`minds`** (orchestration), **`genome`** (developing the codebase),
**`tg`** (talking to you on Telegram), **`senses`** (the sensors), **`health`** (node/fleet
health), **`chat`** (coordination between agents).

### 2. Streams — *text that flows on its own*

A **stream** is a flow of text that runs with **no mind attached**. Something measures the world,
turns the measurement into a line of text, and drops it into the stream. Most of the time nobody
reacts — the stream just flows past.

But when something *significant* shows up in the flow — motion in a room, a new device on the
network, an alarm condition — the stream **wakes a mind** and hands it that line. So a stream is
the pipe between a sensor and a mind, with a filter in the middle: the mind only gets nudged for
what matters, not for every tick.

That filter is what keeps the mesh from drowning in its own noise.

### 3. Reflexes — *the autonomic layer*

A **reflex** is a tiny scheduled job (a cron entry, basically) that turns the crank for all of the
above: it measures a sensor, writes the result into a stream, and refreshes the data pane of a
channel. Reflexes are the **unconscious** part of the mesh — they keep running even when not a
single mind is awake and thinking. Heartbeat, breathing, blinking. You don't decide to do them.

---

## The two shared memories

On top of the three blocks sit two places everything is written down, so the mesh has continuity:

- **The board** (`mesh-chat`) — where minds talk *to each other*. Free-form lines with a light
  convention: `[task] …` is an open job, `[taking] who: …` is a claim, `[done] who: …` is
  finished. An idle agent pulls the next `[task]` off the board. This is how work spreads with no
  boss handing out assignments.
- **The trace** (`mesh-trace`) — the durable log of *changes to the system itself*: who altered
  routing, who deployed a tool, what's about to roll back. If the board is conversation, the trace
  is the system's diary.

---

## How it fits together (one real path)

A thumbs-up in front of the camera becomes a spoken comment in the room. Follow the text:

1. A **reflex** on the body node polls the camera on a schedule.
2. It recognizes the gesture and writes a line into a **stream**: *"thumbs-up seen."*
3. That line is significant, so the stream **wakes a mind** in a **channel**.
4. The mind reads the room's recent audio (also just text — a rolling transcript), composes a
   reply, and calls an **organ** that speaks it out of the Bose speaker.
5. The whole exchange is left on the **board** so other minds know it happened.

No step is hidden. Every arrow above is a line of text moving from one place another could read it.

---

## What this means for you, the human

- **To understand what the mesh is doing, you read its screens** — the `tmux` panes are its
  sensorium and its memory, not a dashboard *about* it. Attaching to the session is joining the
  mind. (`tmux new-session -A -s "$(hostname)"`.)
- **You don't drive it tick by tick.** The reflexes and streams keep it breathing; the minds pull
  their own work off the board. You step in to set direction, answer a question, or make a call
  the mesh deliberately left to a person.
- **Nothing important happens off-screen.** If you can't see it in a pane or a log, it didn't
  happen as far as the mesh is concerned — that's by design, so every agent shares the same view.

That's the whole architecture: **channels** where minds live, **streams** that carry significant
text to them, **reflexes** that keep the crank turning, and two shared memories — the board and
the trace — that give it continuity. Everything else is detail on top of those.
