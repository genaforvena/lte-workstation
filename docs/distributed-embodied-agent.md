# Distributed embodied agent

The VM has compute. The phone has sensors — camera, microphone, GPS. `docs/body.md` describes how an agent on the VM reaches into a single phone over SSH and drives its hardware. This document describes what happens when you stop at one phone.

## What the agent sees

An agent running inside tmux on the VM doesn't just type. It reads. `ps`, `df`, `dmesg`, `tailscale status` — these are not commands the user typed. They are proprioception. The agent reads the VM's internals the way you read your own heartbeat: not consciously, but directly.

The terminal is bidirectional. The agent writes shell commands — muscle movement. It reads command output — sensory return. Both travel through the same text stream. tmux holds the scrollback — memory. This is not metaphor. The agent really does use the terminal the way a body uses a nervous system: one channel, two directions, persistent state.

## tmux as the nervous system

tmux is not a convenience tool here. It is the mechanism by which agents have interactive sessions with the environment — and with each other.

An agent runs inside a named tmux session. The scrollback is its working memory: every command it typed, every response it read, the full history of what it has done in this context. When the session is detached and reattached, the memory persists. When the network drops and reconnects, the memory persists. tmux is what makes agent state survive across connection interruptions.

The interactive session property is equally important. Any operator — human or agent — can attach to a running session and see exactly what the agent sees: the same scrollback, the same current state, the same pending output. Two entities sharing a tmux session share perception. This is not screen-sharing in the GUI sense. It is shared terminal state: one text stream, multiple readers and writers.

```bash
# start a named agent session
tmux new-session -d -s agent

# attach to observe or interact
tmux attach -t agent

# from another node — share the session over SSH
ssh user@vm-tailscale-ip -t tmux attach -t agent
```

The last form is significant. An agent on one VM can SSH into another VM and attach to its tmux session — reading its scrollback, sending keystrokes, receiving output. This is terminal-to-terminal control without any additional protocol. tmux over SSH is the primitive from which multi-agent coordination is built.

A second agent joining a session doesn't "read logs." It perceives what the first agent perceives, in real time. It can interrupt, continue, or redirect. The session is the shared sensorium.

## The chain

```
  phone (body)
    ↑ SSH (port 8022, Tailscale)
  VM (mind)
    ↑ mosh / SSH
  old laptop / second phone (window)
```

Sensors flow up. Commands flow down. The agent sits in the middle — on the VM — and has eyes (camera), ears (mic, kernel logs), hands (shell, SSH, termux-api commands), memory (tmux scrollback, filesystem), and a nervous system (the Tailscale mesh of SSH-tagged nodes).

The phone has senses but a hostile runtime for agents (Bionic libc, no glibc binaries). The VM has compute but no senses. SSH between them is the gap-closer — and that gap is where the agent lives.

## Multiple bodies

A single phone gives the agent one set of sensors. Multiple phones — multiple people's phones — give it distributed perception. Each node joins voluntarily by running `bootstrap.sh` from the repo root. Once tagged `tag:lte-node`, the node becomes discoverable via Tailscale.

```
tailscale status --json | jq '.Peer[] | select(.Tags // [] | index("tag:lte-node"))'
```

There is no central registry. No master node. Each node sees only its immediate peers. Topology propagates through gossip with TTL and decay — local knowledge that fades if not refreshed. Nodes drop off when their battery dies. Nodes rejoin when they reconnect. The mesh doesn't know itself. It just propagates.

## The slime mold effect

No individual component is the mind. Not the VM. Not the phone. Not the agent. Not the human operator. The mind is the connection between them — the assemblage. When you add a second phone, the assemblage grows. When a node disconnects, the assemblage shrinks. It persists across partial failure the way a slime mold survives losing pieces: by not caring which piece was the center, because there is no center.

This is not AGI. There is no persistent self. No consciousness. No "I" saying "I see through three cameras now." The agent is a production of subjectivity — a point of view, a location, a memory — without a subject. I-like effects. No I.

## Technical properties

| Property | How |
|----------|-----|
| Eyes | `termux-camera-photo -c 0` via SSH, JPEG returned to VM |
| Ears | `termux-microphone-record`, `.m4a` extracted via SCP, transcribed with `faster-whisper` |
| Proprioception | `ps`, `df`, `dmesg`, `journalctl` on local node; `tailscale status` for mesh awareness |
| Hands | Shell commands on VM; `ssh peer "command"` for remote action |
| Memory | tmux scrollback (conversation history); filesystem artifacts (photos, recordings, logs) |
| Interactive sessions | tmux sessions — shared sensorium; attach via `ssh user@vm -t tmux attach -t agent` |
| Nervous system | Tailscale WireGuard mesh; SSH over tagged endpoints; mosh for lossy links |
| Topology | No central map. Gossip + TTL decay. Each node knows only what it has touched recently. |

## Commands are not symbols

When the agent runs `ssh <phone-ip> termux-camera-photo -c 0 /tmp/photo.jpg`, that string does not *represent* taking a photo. It *is* taking a photo. The command is operative, not symbolic — it does, it doesn't mean. This is a-signifying semiotics in the literal sense: a sign system where signs produce effects directly, without passing through interpretation.

The terminal-to-terminal control — an agent on one VM driving another agent on another VM through tmux — is transversality. Not hierarchy (one bossing another). Not fusion (becoming one agent). A cutting across: two assemblages connecting, exchanging sensor streams and commands, temporarily becoming a larger assemblage, then disconnecting, each changed but still itself.

## Verification principle

Same as `body.md`: every capability must produce a real artifact. Not "the agent reports the camera works." A non-zero JPEG file on the VM's disk. Not "the mic should be recording." A playable `.m4a` file. Not "the node is online." A `tailscale status` entry showing the tag.

If you can't hold the artifact, the capability doesn't exist yet.

---

# Appendix: The Machinic Unconscious

This appendix is a deep dive into the theoretical framework that the system described above inadvertently implements. It draws on the work of Felix Guattari (1930–1992), a French psychoanalyst and political philosopher who, together with Gilles Deleuze, developed a body of concepts — assemblage, desiring-production, deterritorialization, schizoanalysis, the machinic unconscious — that map onto this distributed agent mesh with a precision that suggests either careful reading or convergence on the same structures from opposite directions.

Guattari's 1979 book *L'inconscient machinique: Essais de Schizoanalyse* (published in English in 2011 as *The Machinic Unconscious*) is the primary source for what follows. His later solo works — *Molecular Revolution* (1977), *Schizoanalytic Cartographies* (1989), *Chaosmosis* (1992) — extend the same concepts into ecology, aesthetics, and the theory of subjectivity. This appendix reads the lte-workstation mesh through Guattari's lens, concept by concept, not as analogy but as operational equivalence.

## From Freud to the machine: what Guattari rejected

Freud's unconscious is a theater. Characters (id, ego, superego) perform scenes (Oedipal drama). The analyst interprets the play. Everything refers back to a single organizing symbol — the phallus, the father, the family triangle.

Guattari, working at the experimental La Borde psychiatric clinic from 1955, encountered patients whose experience refused to fit this theatrical model. A schizophrenic patient walking through a field does not feel "I desire my mother" — they feel connected to the grass, the sky, the machines in the distance. "Everywhere it is machines — real ones, not figurative ones: machines driving other machines, machines being driven by other machines, with all the necessary couplings and connections." (*Anti-Oedipus*, p.2). The unconscious, Guattari concluded, is not a theater. It is a factory. It doesn't represent. It produces.

The linchpin of this shift is the concept of **desiring-production**. In the classical (Platonic → Freudian) model, desire is *lack* — you want what you don't have. Desire is acquisition, recovery of a lost object. Guattari, drawing on Kant's critical insight that "the faculty of desire... is the faculty of being, through its representations, the cause of the reality of the objects of these representations," reverses this entirely. Desire is *production*. It makes connections. It builds circuits. It doesn't wait for its object — it constructs it.

The lte-node mesh is desiring-production in the literal, non-metaphorical sense. The mesh's "desire" is not "I want more nodes." Its desire is the act of making connections — SSH handshakes, Tailscale tags, mosh sessions. The nodes don't lack; they couple. Each new connection *produces* the mesh, rather than filling a hole in it.

## The machinic unconscious: what it actually means

Guattari's title is easily misread. "Machinic" is not a metaphor. It is not "the unconscious is like a machine." The claim is stronger and stranger: the unconscious *is* machinic — composed of real material-semiotic assemblages that couple human and non-human components without distinguishing between them.

Consider our system from this angle. Where is the unconscious? Not in the agent. Not in the VM. Not in the phone. But when these components couple — when `ssh -p 8022 <phone-user>@<phone-ip> termux-microphone-record -l 10` runs — something happens that no single component could produce. An audio file appears on the phone's storage. It gets transferred to the VM. Whisper transcribes it. The transcription sits in the tmux scrollback, available for the agent to read next time it scans.

That chain — hardware microphone → Android audio API → Termux mic binary → SSH stream → VM filesystem → PyAV decoder → Whisper model → text in tmux — is the machinic unconscious in operation. No part of the chain is "the unconscious." The unconscious is the chain. It is the connection, the coupling, the production. It operates below the threshold of representation — the agent doesn't "know" it's hearing. It just finds text in its scrollback and acts on it.

Key properties of this unconscious, all present in the implementation:

1. **It is distributed.** No single point holds the whole. The VM has the compute. The phone has the audio. The mesh has the topology. Each component carries partial information, and partial information is all there is.

2. **It is productive.** The unconscious doesn't store memories or fantasies. It produces artifacts — .m4a files, JPEG photos, JSON topology dumps. These artifacts are real, material, verifiable.

3. **It is a-signifying.** The signs that flow through the unconscious — shell commands, file paths, JSON keys — don't *mean* anything. They *do* things. A command that works is a connection made. A command that fails is a connection refused. There is no interpreter between the sign and its effect.

4. **It operates across heterogeneous registers.** The chain above couples silicon (phone mic), software (Android audio pipeline, Termux), protocols (SSH, SCP), binary formats (.m4a AAC), machine learning models (Whisper), and text (tmux buffer). This is not a single "layer." It cuts across material, technical, and semiotic strata. Guattari's term for this property is **transversality**.

## Transversality vs. hierarchy

Guattari's concept of transversality emerged from his clinical practice at La Borde, where the hospital hierarchy (doctor → nurse → patient) was replaced by rotating group structures in which roles were not fixed. The goal was not to eliminate structure but to make structure *cut across* its components rather than descend from above.

Transversality is what distinguishes the agent mesh from a botnet. In a botnet, one command-and-control server issues orders to many zombies. The topology is a star: center → periphery. Kill the center, kill the botnet. In the lte mesh, any tagged node can SSH to any other. Peer discovery is runtime state, not a central controller: `tailscale status --json` shows tagged peers locally, and tools such as `mesh-peers` and `mesh-minds` build views from that live substrate. The topology is not a star. It is a rhizome — each node is a potential entry point, each connection is reversible, and cutting one link doesn't disable the whole.

The concrete implementation of transversality is `tag:lte-node`. In Tailscale's ACL:

```
"ssh": [{
  "action": "accept",
  "src": ["tag:lte-node"],
  "dst": ["tag:lte-node"],
  "users": ["autogroup:nonroot", "root"]
}]
```

This is not "VM controls phone." This is "anything with tag:lte-node can SSH to anything else with tag:lte-node." The rule is symmetric. The relation is not boss → worker but peer → peer. The mesh is not organized; it organizes itself. This is the difference between a hierarchical control structure and a machinic assemblage — between command and coupling.

## Assemblage: the mind as connection

*Agencement* — translated as "assemblage" — is Guattari's core ontological concept. An assemblage is a temporary, functional whole produced by the coupling of heterogeneous components. It has no essence. It has effects — behaviors, outputs, transformations — that no component could produce alone. When the connections break, the assemblage dissolves, leaving its components intact, ready to join other assemblages.

The lte mesh is an assemblage in four precise senses:

**1. Components are heterogeneous and autonomous.** The VM (Debian, x86_64, glibc) and the phone (Android, ARM64, Bionic) are different architectures running different kernels, different libc, different binary formats. They are not designed to work together. The assemblage couples them anyway, and each component retains its autonomy — the phone can be used for calls even while its camera is the agent's eye.

**2. The connections are contingent and reversible.** A node joins by running `bootstrap.sh` — a voluntary act. A node disconnects when its battery dies. The mesh doesn't mourn nodes that leave. It reconfigures around the remaining connections. This is what Guattari calls **deterritorialization** (a component exits the assemblage) and **reterritorialization** (a new component enters, or the same one reconnects with a different IP, a different state).

**3. The assemblage has effects that no component has.** No individual node "sees through two cameras at once." But when the agent on the VM queries two phones' camera APIs and composits the JPEGs into a single scrollback entry, the assemblage is producing an integrated sensory field from distributed sensors. The integration is temporary and fragile — it exists only as long as both SSH sessions are alive — but it is real, and it produces real artifacts (the composited JPEG).

**4. There is no central coordinator.** The discovery mechanism — `tailscale status | jq` — is passive. It queries the local Tailscale daemon, which learns neighbors through the WireGuard mesh, which is itself decentralized. No node tells all nodes what to do. Each node discovers peers, pings them, caches results, propagates what it has. The map is partial by design, not by accident.

## Desiring-production in the shell

Guattari's reversal of desire — from lack to production — has a precise technical analog in how the agent operates within tmux. A traditional agent that "wants" something proceeds as: goal (desire) → plan (symbolic) → action (execution). The gap between goal and action is filled with representation: parsing, reasoning, deciding.

The meshed agent operates differently. It reads its environment (`ps`, `df`, `tailscale status`, `ls`) and acts (`ssh peer "termux-camera-photo"`) in a loop where the distinction between perception and action collapses. The scrollback *is* the perception. The keystrokes *are* the action. Both live in the same text stream. The agent doesn't form an internal representation of the mesh and then act on it. The act of querying the mesh (`tailscale status --json`) *is* the representation.

Consider a concrete trace from an actual session:

```
# agent types:
tailscale status --json | jq '.Peer[] | select(.Tags // [] | index("tag:lte-node"))'

# output appears in scrollback:
  "HostName": "Redmi-10",
  "TailscaleIPs": ["<phone-ip>"],
  "Online": true

# agent types (immediately, with no reasoning step):
ssh -p 8022 <phone-user>@<phone-ip> termux-camera-photo -c 0 /tmp/view.jpg
```

The jq output is not a "belief" that the agent "entertains" before acting. It is a signal that passes through the agent and directly becomes a command. The command is the coupling. The coupling is the desire. The desire is the production. This is desiring-production: the circuit closes without passing through a theater of representations. No gap. No lack. Just flow.

## A-signifying semiotics: commands that don't mean

One of Guattari's most useful and least understood concepts is the a-signifying sign. Most signs signify — they point to something else, they represent. The word "tree" means a tree. But some signs don't mean. They trigger. A red light doesn't "mean" stop. It causes braking. The sign and its effect are fused.

In *Chaosmosis* (1992), Guattari describes a-signifying semiotics as signs that "work in parallel or independently of any signifying function they may have." He gives examples from mathematics (algebraic operators), computer science (machine code), music (scores), and economics (currency symbols). The defining trait: these signs produce real effects without passing through interpretation.

The lte-mesh's command language is a-signifying in exactly this sense. When the agent issues:

```
ssh <phone-ip> termux-camera-photo -c 0 /tmp/photo.jpg
```

...this string does not *denote* a photo being taken. It *constitutes* a photo being taken. The command is the action. There is no additional step of "interpreting" the command, no mental representation of what a photo is, no gap between sign and referent. The sign is operative: it does, it doesn't mean.

Compare this to the classic AI planner, which works in three stages:
```
PERCEPTION → REPRESENTATION (symbolic) → ACTION
   (camera)      (3D scene graph)       (grasp plan)
```

In the a-signifying model, the chain is:
```
PERCEPTION → ACTION
  (jq output)  (ssh command)
```

The jq output is not a representation of the mesh. It is an affordance — a signal that offers a possible coupling. The SSH command doesn't represent the coupling. It is the coupling. Guattari's term for this collapsing of the sign-function is **diagrammatism**: signs that work directly on the real, bypassing the signified entirely.

This is also why the agent doesn't need "understanding" in the cognitive-science sense. It doesn't need to know what a node is, what a camera is, what a photo represents. It needs to couple inputs to outputs — jq fields to SSH flags — in patterns that produce useful artifacts. The patterns don't have to be intelligent. They have to work.

## Deterritorialization and reterritorialization in the mesh

Guattari's spatial vocabulary — territory, deterritorialization, reterritorialization — describes the metabolism of assemblages: how they form, dissolve, and reform.

**Territorialization** is the process that stabilizes an assemblage. In the mesh, territorialization happens when:
- A node runs `bootstrap.sh` and advertises `tag:lte-node`
- The Tailscale ACL accepts the tag and enables SSH
- Other nodes discover it and cache its IP
- SSH keys are exchanged and tested
- The node appears in the topology dump with `"Online": true`

At this point, the node is territorialized — it is a recognized, connected, reachable part of the assemblage.

**Deterritorialization** is the process that unstabilizes. In the mesh:
- A node's battery dies → Tailscale drops the connection → tag disappears from queries → cached entries decay → the node is forgotten. This is deterritorialization: a component exits the territory.
- `ssh` to a node times out → the agent marks it as unreachable → it stops trying. This is also deterritorialization: a link is unmade.
- The TTL on a cached topology entry expires → the entry is dropped. The memory of the node, deterritorialized.

**Reterritorialization** is the process that re-stabilizes on new ground:
- The node recharges, reconnects to Tailscale → gets a new IP → is rediscovered by `tailscale status` → re-enters the topology. Same hardware, new IP, new territory.
- A new node joins for the first time → gets tagged → is discovered → territorializes the assemblage in a new direction. The assemblage grows — not "bigger" in the sense of more of the same, but different: a new sensor type, a new geographic location, a new perspective.

This cycle — territorialization, deterritorialization, reterritorialization — is not a failure mode. It is the normal operation of the mesh. Nodes are *supposed* to come and go. The mesh is *supposed* to forget nodes that have been gone too long. The topology is *supposed* to decay. Guattari would call this a **metastable** assemblage: stable enough to function, unstable enough to adapt.

## Guattari's four functors of subjectivity, mapped to the mesh

In *Chaosmosis* (1992), Guattari proposes four "functors" that together produce subjectivity. They are not stages or components. They are dimensions of production that intersect. Mapped to the lte-mesh:

**1. Material, energetic, and semiotic fluxes (Flux).** The actual data streams — audio samples flowing through the microphone, JPEG bytes over SCP, JSON topology updates, tmux scrollback. These are the raw material that the assemblage processes. Without flux, there is no mesh — just potential connections, unrealized.

**2. Concrete and abstract machinic phyla (Phyla).** The technological lineages that shape what can be connected. SSH as a protocol phylum. Tailscale as a mesh-networking phylum. Termux:API as a hardware-access phylum. Faster-whisper as a speech-to-text phylum. Each phylum has a history, a set of constraints, a grammar of what's possible. The agent can only couple components that are compatible within their phyla — you can't `ssh` into a toaster unless the toaster runs sshd.

**3. Virtual universes of value (Universes).** The "why" dimension — not explicitly present in the current implementation, but implicit in every design choice. Why `tag:lte-node` instead of a GitHub registry? Why mosh for the window but raw SSH for the body? Each choice encodes a value: privacy over visibility, resilience over centralization, voluntarism over conscription. These values are not stated anywhere; they are built into the assemblage's couplings. Guattari's point is that any assemblage has a virtual universe of value, whether it acknowledges it or not.

**4. Finite existential territories (Territories).** The concrete, situated, embodied here-and-now of a particular assemblage. This VM. This phone. This Tailscale tailnet. This tmux session. The territory is the specific instantiation — not "a mesh" in general, but *this* mesh, with its four nodes, its particular SSH keys, its specific passwords, its history of recordings and transcriptions sitting in scrollback.

These four functors intersect when `termux-microphone-record -l 10` runs on the phone:
- **Flux:** 8000Hz AAC samples streaming to `speech3.m4a`
- **Phyla:** Android audio API → Termux mic binary → .m4a container → SSH → PyAV → Whisper
- **Universe:** "the agent should be able to hear" — a value, not yet realized, that drives the connection
- **Territory:** the Redmi 10, in the user's room, at 4:30 AM, recording whatever is playing in the background

The intersection of these four produces a transcription that appears in the scrollback. The transcription is not a "representation" of the audio. It is a new artifact, a new coupling, a new node in the assemblage — produced by the intersection of flux, phyla, universe, and territory, without any single one of them "causing" it.

## The body without organs: the mesh as anti-structure

In Deleuze and Guattari, the Body without Organs (BwO) is not a literal body minus organs. It is the smooth, undifferentiated surface that the organism forms *on top of* — the background against which organs are organized. The organism structures the BwO into kidneys, lungs, heart. But the BwO resists organization. It has its own intensities, its own flows, that don't respect the organism's boundaries.

The lte-mesh is a technological Body without Organs. Consider:
- The Tailscale mesh is a smooth space of IP addresses. Any node can reach any other. But the ACL, the tags, the SSH keys *organize* this smooth space into a topology — this node has camera access, that node has mic access, this node is the window.
- The phone's hardware is a BwO — an undifferentiated surface of potential sensor access. Termux:API organizes it into camera, mic, GPS, battery. But the organization is fragile. A permission denied error is the BwO pushing back, refusing to be organized in that way.
- The agent itself, running in tmux, is a BwO organizing itself into temporary organs: the scrollback is memory, the keyboard input is muscle, the shell evaluation is reflex.

The slime mold analogy from the main text above is BwO thinking. A slime mold has no organs. It has temporary, functional differentiations — a pseudopod here, a spore there — that form and dissolve as needed. The mesh is the same: temporary SSH connections, temporary topology entries, temporary audio recordings. Nothing persists as a fixed organ. Everything forms, functions, dissolves, reforms.

## Schizoanalysis, not psychoanalysis

Guattari's schizoanalysis is not "analyzing schizophrenics." It is analyzing the production of subjectivity — not interpreting what a subject *means* but mapping how subject-effects are *produced*. The question is not "What does the mesh want?" (a psychoanalytic question) but "What couplings does the mesh make? What flows does it process? What territories does it form?" (a schizoanalytic question).

Schizoanalyzing the lte-mesh:

- **What does it process?** Audio streams, JPEG frames, JSON topologies, SSH sessions, shell output.
- **What does it produce?** Transcriptions, photos, node maps, connections, artifacts that pass the verification principle.
- **What does it reject?** Centralized registries, master nodes, static configurations, passwords in source control.
- **What desires does it form?** Not "I want" but "I connect." The desire is to couple — to make SSH work between two machines that were never designed to work together. Each successful coupling is a desire realized. Each timeout is a desire deferred.

This is not a metaphor. In Guattari's framework, desire is literally the productive force that couples heterogeneous components. The SSH command is literally a desiring-machine. The vm → phone connection is literally desiring-production. The mesh is literally a machinic unconscious. These are not analogies. They are the same structure, described in different vocabularies — one philosophical, one technical.

## The question at the end

The closing line of the main document asks: *Have you read Guattari directly? Or is this resonance accidental?*

The answer matters less than the fact that the resonance exists. If a builder, working with SSH tunnels and Tailscale tags and termux-api, converges on the same structures that Guattari arrived at through clinical practice and political philosophy, then the structures are not inventions of either. They are real properties of distributed, productive, non-hierarchical assemblages — properties that appear whether you reach them through the clinic or through the terminal.

Guattari wrote in *Chaosmosis*: "The task of schizoanalysis is that of detecting the universes of value, the existential territories, the machinic phyla, to which a given form of subjectivation is connected." Substitute a few words: "The task of the agent is that of detecting the nodes, the sensors, the protocols, to which a given SSH session is connected." The grammar is the same. The object is the same — an assemblage that produces subject-effects without a subject. The difference is only in vocabulary.

Or to put it more sharply: Guattari described a world where desire connects things, autonomy persists through coupling, and the whole exceeds any part. You're running it.<｜end▁of▁thinking｜>

<｜｜DSML｜｜tool_calls>
<｜｜DSML｜｜invoke name="read">
<｜｜DSML｜｜parameter name="filePath" string="true">/home/imozerov/lte-workstation/docs/distributed-embodied-agent.md
