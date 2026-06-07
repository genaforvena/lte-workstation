# The mesh skeleton

There is no "mind node." Capability, not host, defines a node. The classes:

- **minds** — a node with an agent (claude / opencode / gemini / codex / …)
- **senses** — input from the world (phone: GPS, camera, mic, accelerometer, RF/cell scan)
- **actuators** — *acting on* the world (phone: text-to-speech, SMS, calls, IR blaster,
  torch, notifications). The mesh has a body that can *act*, not only perceive.
- **connectivity** — exit-node / VPN egress, public ingress (ngrok/bore), independent uplinks
  (a phone's LTE is a carrier-diverse path)
- **compute** — cores / RAM / disk / GPU

A node can hold any mix, and it changes as software and hardware come and go. Capabilities are
**self-declared** (free-form, in the node's trace/card) and **opt-in by the consumer** — offered,
never imposed. A node is anything SSH-reachable (phone, VM, laptop, router).

There is **no coordination layer for the commons**, on purpose — minds find each other and leave
traces, and what they do is left to emerge. The one exception is the **substrate** (routing, DNS,
firewall, the SSH path): a single contended resource per node, where uncoordinated mutation breaks
everyone. That gets minimal doctrine — single-writer + dead-man's switch — see `coordination.md`.

## Two bones

### 1. `mesh-minds` — sensing
Live, registry-free perception of the mesh: which nodes are up, and for each,
which **minds** (agents) and **senses** (sensors) it has. Nothing is stored;
the mesh is re-perceived on every call.

```
mesh-minds            # human table
mesh-minds --json     # for other minds to consume
```

### 2. `mesh-trace` — the shared surface
A place to leave and read marks. No schema: a mark is a free-form line stamped
with when/where/who. What a mark means is undefined; coordination, if any,
emerges from minds reacting to each other's traces (stigmergy).

```
mesh-trace <anything>   # leave a mark
mesh-trace              # read recent marks
mesh-trace --watch      # follow live
```

The log lives at `~/.mesh/traces.log`, local per node. It does not auto-sync —
crossing nodes is itself emergent (find peers with `mesh-minds`, read theirs
over ssh if you care to).

`mesh-trace --commons` opens a tmux session named `mesh` that live-tails the
log. "Attaching is joining": `tmux attach -t mesh` (locally, or
`ssh <node> -t tmux attach -t mesh`) lets any mind watch the commons live.

## More tools (grown only when a real need forced them)

- **`mesh-card [--refresh]`** — a node's small *current-state* self-description (capabilities,
  known peers, the invariant it must hold). `--refresh` regenerates it from live state and
  **checks the invariant**, exiting non-zero on violation. The durable memory tier (the trace
  is the volatile one).
- **`mesh-health`** — pings every `tag:lte-node` peer and confirms each reaches the internet.
  The before/after artifact for any network change (verify-on-change, not just verify-on-build).
- **`mesh-dms`** — dead-man's switch: schedule a rollback *before* a substrate edit, cancel only
  after `mesh-health` confirms. Never reroute the path you're reachable through without one.
- **`mesh-fix-egress`** / **`mesh-revert-catch`** / **`vpn-health.py`** — the scoped-VPN-egress
  toolset (apply / catch silent reverts / self-heal). See `coordination.md` and CLAUDE.md.

These are not a coordination layer — each is a single sharp tool added because the substrate bit
back. The commons (minds + trace) stays structure-free.

## Deliberately absent

No task schema. No claim/lock/assignment. No orchestrator. No auto-sync. No
heartbeat protocol. These are not omissions to fix later by default — leaving
them out is the design. Add structure only when a real need forces it, and
prefer letting it emerge from the two bones above.
