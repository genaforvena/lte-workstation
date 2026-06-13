# Location transparency — "it shouldn't matter WHERE the mind/tmux/organs are"

Operator directive 2026-06-13: ideally every node's tmux session is the SAME, and it should not
matter which physical node a mind / window / organ lives on. The mesh as ONE logical organism;
nodes as interchangeable substrate.

This is the north-star refinement of the existing doctrine ("no fixed mind", "a mind is any node
running an agent", "tmux is the only way to see into a node"). It asks for **location transparency**:
address a capability by NAME, the mesh resolves WHERE it physically runs.

## Where we already are (transparent today)
- **Organs over SSH:** `mesh-location` / `mesh-body-motion` / `mesh-body-power` resolve the phone
  from the registry and run it over SSH — callable from ANY node, the body's hardware is elsewhere.
- **Coordination:** `mesh-tell --node` drives any mind anywhere; `mesh-attach` attaches any node's
  session from one place; `mesh-chat-sync` converges the board across nodes (one shared room).
- **Inference:** `mesh-relay` routes text→cheapest-available-pool; `mesh-local-mind` fails over to any
  node's ollama over the tailnet. Thinking is already host-agnostic.
- **Genome:** git + follower auto-heal → every node converges to HEAD. The CODE is uniform.

So three of the four substrates (coordination, inference, genome) are already location-transparent.
The gap is the FOURTH: **structure + organs**.

## The gaps (measured 2026-06-13)
1. **Session layout is non-uniform.** IdeaPad = 22 windows, ds = 13. mesh-restore gates each
   mind-window on whether the node DECLARES that mind locally → a node only grows windows for minds
   it physically hosts. So sessions diverge by hardware/mind availability.
2. **Local organs are host-bound.** `ble`/`mic`/`camera`/`notify` run only on the node with the
   hardware. There is no `mesh-organ <name>` that says "give me A camera" and resolves to whichever
   node has one. (The body organs solved this for the phone; nothing generalizes it.)
3. **No capability router.** Each organ tool hardcodes its own resolution (mesh-location knows it's
   the phone). There's no single resolver: name → which node offers it (from cards/registry) → run
   there → return artifact.

## Proposed architecture — three layers
**A. Uniform structure (the session is a ROLE manifest, not a hardware reflection).**
   One canonical window set (plan/health/verify/work/dev/discover/sense/tg/chat/minds/reflex/shell),
   defined ONCE (a manifest the genome carries). Every node builds the SAME windows. A role-window
   whose mind isn't local still EXISTS — its bottom pane is either (a) a local mind if present, or
   (b) a thin proxy that routes the role's work to wherever that mind lives (`mesh-tell --node`).
   Result: attach any node, see the same map; the body you're in stops mattering.

**B. Capability router (`mesh-organ <name> [args]`).**
   name → look up which online node DECLARES `<name>` (card capabilities / registry) → run it there
   over SSH → return the artifact. "Run the camera" finds a camera anywhere. Honest-fusion: distinguish
   no-such-organ / all-offline / ran-here-is-the-artifact. Generalizes what the body organs do by hand.
   Optional policy: nearest / cheapest / specific-node.

**C. Addressing (logical names resolve to physical hosts, everywhere).**
   Already mostly built (registry + mesh-peers + mesh-tell --node). Formalize: a mind/organ/window is
   referred to by logical name; resolution is a library call (`mesh-resolve <kind> <name>`) reused by
   the router + tell + dash. Single source of truth for "where does X live right now."

## Recommended FIRST step (bounded, high-value, low-risk)
**Build `mesh-organ <name>` — the capability router (layer B).** It is the most visible win, needs no
session-restructure, and is purely additive (read-only resolution + SSH execution). It immediately
makes EVERY declared organ location-transparent: from ds, `mesh-organ camera` runs IdeaPad's camera.
Then layer A (uniform session manifest) is the bigger follow-up — it touches mesh-restore on every
node and wants a watched rollout (changes what every session looks like).

## Why not do layer A first
Uniform sessions mean a node hosts windows for minds it lacks → either idle proxy panes (cheap) or
remote-routing (needs the router from B anyway). So B is the dependency. Build the router, then the
uniform manifest can lean on it for the no-local-mind windows.
