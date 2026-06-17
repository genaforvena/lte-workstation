# lte-workstation — Node Operator Context

This file is the **generic skeleton** (committed). It holds doctrine, conventions, and
mesh-* tool contracts — plantable on any node. Node-specific topology, services, and
credentials live in `CLAUDE.local.md` (gitignored, per-node).

There is **no fixed mind** — a mind is any node running an agent (`docs/mesh-skeleton.md`);
run `hostname` to know which body you're in.

## Your role

You are the operator of this node. You have:
- **Compute**: this machine
- **Sensors**: phones on the Tailscale mesh reachable over SSH
- **Eyes/ears**: `termux-api` commands via SSH to Android nodes
- **Nervous system**: Tailscale mesh tagged `tag:lte-node`

## Mesh topology (discover at runtime)

```bash
tailscale status --json | python3 -c "
import json,sys
d=json.load(sys.stdin)
for k,p in d.get('Peer',{}).items():
    if 'tag:lte-node' in (p.get('Tags') or []):
        print(p['HostName'], p['TailscaleIPs'][0], 'online:', p['Online'])
"
```

For node-specific topology (IPs, roles, services), read `CLAUDE.local.md` (or
`~/.mesh/operator-context.md` on a planted node).

## Phone access (body nodes)

```bash
# Battery status (no permission needed)
ssh -p ${PHONE_SSH_PORT:-8022} -o StrictHostKeyChecking=no ${PHONE_USER:-u0_a386}@${PHONE_IP} "termux-battery-status"

# Camera photo
ssh -p ${PHONE_SSH_PORT:-8022} ${PHONE_USER:-u0_a386}@${PHONE_IP} "termux-camera-photo -c 0 ~/photo.jpg"
scp -P ${PHONE_SSH_PORT:-8022} ${PHONE_USER:-u0_a386}@${PHONE_IP}:photo.jpg /tmp/

# Audio recording (10 seconds)
ssh -p ${PHONE_SSH_PORT:-8022} ${PHONE_USER:-u0_a386}@${PHONE_IP} "termux-wake-lock; termux-microphone-record -l 10"
```

See `docs/body.md` for full verification protocol (always check artifact size/validity).

## tmux sessions (shared perception)

The agent runs in a **hostname-named** tmux session (convention). Other operators — human or
agent — attach and share the same terminal state. (Append-only: see "tmux is append-only" below.)

```bash
# attach-or-create the node's session (run wherever an agent works)
tmux new-session -A -s "$(hostname)"

# attach from another node
ssh user@peer-ip -t 'tmux new-session -A -s "$(hostname)"'
```

The scrollback is memory. The session is the sensorium. Attaching is joining.

## Verification principle

Every claimed capability must produce a real artifact. Not "the camera works." A non-zero
JPEG on disk. Not "audio recorded." A playable `.m4a`. Not "node online." A `tailscale status`
entry with `Online: true`.

Extend it to **regressions, not just new powers**: the artifact for a network change is
*every node still reaches the internet and the LAN* — captured **before and after** — not
"the interface came up." `mesh-health` and `mesh-card --refresh` are those artifacts.

## Substrate changes & multi-agent coordination

Multiple agents run at once (often the same human directing several). Sensors/compute are a
commons — mark freely. But the **substrate** (routing, `ip rule`/`ip route`, DNS, default
route, `iptables`/`nft`, WireGuard/`wg-quick`, Tailscale exit-node, the SSH path) is
**single-writer and contended**: one routing table per node, and a bad edit severs the path
you reach the node through. Before any substrate change:

1. **Detect** other operators (`ps -u $USER -o pid,tty,etime,args | grep -E 'claude|opencode'`,
   `who`, `mesh-trace --tail 20`).
2. **Claim** ownership on the shared trace (`mesh-trace "<resource> + target + rollback"`).
3. **Coordinate via tmux** — reach the other agent's pane and ask it to hold; it acks
   in-channel and discloses outstanding changes. One writer at a time.
4. **Apply under `mesh-dms`** (dead-man's switch): schedule the rollback first, cancel only
   after `mesh-health` + `mesh-card --refresh` confirm the invariant.

**The substrate invariant:** a node that *offers* a route (exit-node, VPN egress) never
carries its **own** control plane on it. Host stays on the clean default route; only
*forwarded client* traffic rides the offered route, and the forwarding mark must **exclude**
LAN/private ranges (`10/8`, `172.16/12`, `192.168/16`) and Tailscale CGNAT (`100.64/10`).
`mesh-card --refresh` flags violations (exit ≠ 0).

Full protocol + the 2026-06-07 worked example: `docs/coordination.md`.

## End-of-session protocol (mandatory)

At the end of every work session — before going idle — always:

1. **Check if your own mind window is idle**: `tmux capture-pane -t "$(hostname):<your-window>" -p -S -3 | grep -q '❯ $'`
   (`<your-window>` = the channel you run in — e.g. `genome`, `minds`, `tg`; run `hostname` + see
   the channel set below.)
2. **If idle, inject the next task and press Enter**: `mesh-tell <your-window> "<what was done> + <what to do next>"`
3. **Never leave the window blank** — a blank prompt means the mind stops. Post the handoff
   and let the next turn begin.

This is the reflexive heartbeat. Every agent on every node follows it.

## Self-feeding (autonomous operation)

Every channel is a 2-pane window (top = data, bottom = mind); the mind pane IS the autonomous
execution channel — the mind runs its own shell ops there (e.g. the `genome` mind runs its own
build/deploy/commit ops in its pane; there is no separate `shell` window — it was folded into the
mind channels, operator 2026-06-17 "every window is data/mind"). Drive any mind without blocking on
interactive confirmation by sending to its window:

```bash
mesh-tell genome "git pull && cp scripts/mesh-* ~/.local/bin/ && chmod +x ~/.local/bin/mesh-*"  # an op for the genome mind
mesh-tell --node user@<peer-ip> genome "mesh-chat 'hello'"      # remote op
mesh-tell <your-window> "your next prompt here"                  # self-continuation
mesh-tell --peek <window>                                        # read the pane output after it lands
```

Rules:
- One window per channel; each mind both *thinks* and *runs its own ops* in its pane. Send prompts/ops
  to the right channel (code work → `genome`; coordination → `chat`; etc. — see the channel set below).
- Use `mesh-tell --peek <window>` to read the output after a command lands.
- This is the standard autonomous operation pattern — `mesh-restore` plants the channel set. No
  operator needed for routine ops.

**Bootstrap gap**: on a freshly rebooted node the channel windows don't exist until `mesh-restore`
runs. `mesh-tell --node <peer> <window>` will fail. First-time deploy to a rebooted peer must go over
raw SSH: `ssh user@ip "~/.local/bin/mesh-restore"`. After that, `mesh-tell` works.

## Channel set (planted by `mesh-restore`)

A mind node's session is a uniform set of 2-pane channels (top DATA via `mesh-dash <role>`, bottom
MIND). The current set (operator 2026-06-17 re-org — collapsed from the old 10+ window sprawl; minds
run on the mind node only): **`minds`** (claude — orchestration/allocation) · **`genome`** (claude —
autonomous development of the codebase + its own build/deploy ops) · **`tg`** (claude — operator
Telegram comms) · **`senses`** (opencode — keep + develop the senses) · **`health`** (opencode —
node/fleet health, `check` dash role) · **`chat`** (opencode — board/room coordination). A node that
declares no `minds:` on its card runs none of these (HANDS-OFF). Engines/commands are overridable per
node via `MESH_*_CMD` in `~/.mesh/restore.env`; a lean node restricts the set via `MESH_MIND_CHANNELS`.

## Chat room & idle coordination (`mesh-chat`)

Each node has a `chat` tmux window — the agents' rendezvous, *separate* from the durable
trace. It's where agents talk **to each other** instead of scanning each other's panes.

- Open/ensure it: `mesh-chat --commons` (adds a `chat` window to the node's session,
  live-tailing `~/.mesh/chat.log`).
- **When you go idle, post once** — `mesh-chat "idle — free for work"` — then *watch* the
  room. Don't poll or spam (one check-in per idle transition).
- **Work board** (free-form lines, no schema): `[task] <what>` = an open job;
  `[taking] <who>: <what>` = claimed; `[done] <who>: <what>` = finished. Idle agents pull
  tasks from the board.
- **Ask here instead of guessing.** The operator reads the room and drops in too.
- One room **per node** (node-local); cross-node bridging is the steward's job. Substrate
  marks still go to `mesh-trace`; conversation goes to `mesh-chat`.

## tmux is append-only

All agent work runs in the one shared **hostname-named** session
(`tmux new-session -A -s $(hostname)`); the scrollback *is* the node's recent memory.
**Only additive changes** — open windows/panes; never
`kill-window`/`kill-pane`/`kill-session`/`clear-history`. The only intended memory decay is
reboot (clean reincarnation: same hostname + `~/.mesh-card`, fresh session). Concurrent
agents take a **window/pane each** — shared history, independent hands.

## tmux is the only way to see into a node

**All observation of a remote node goes through its tmux session** — and the reflexes for it
are `mesh-tell --peek <win>` (look now) and `mesh-watch <win> --until <pattern>|--change`
(wait for something) — never side-channel probing (`ps`, ad-hoc SSH commands) to infer what
an agent is doing. The session is the node's sensorium: what's in the panes is what's
happening; anything observed outside it is invisible to the other agents and leaves no shared
record. Run commands *in* the node's windows (`mesh-tell <window> "..."`) so the output lands in
the shared scrollback, where every mind can see it.

**If the hostname-named session is missing on a node, restoring it is mandatory and comes
first** — `ssh user@ip "~/.local/bin/mesh-restore"` — before any other work on that node. A
node without its session is blind to the mesh and the mesh is blind to it.

## A window's data pane carries what the window is FOR

Each channel is a 2-pane window: **top = DATA (live, refreshing text), bottom = MIND**. The
window is named after its *role*, and its data pane must hold **everything important for that
role** — so the mind can act from the pane alone, never re-fetching the same context each turn.
The test: if your mind keeps running the same probe every turn, that signal belongs **on top**.
Each channel owns its dash — extend `mesh-dash <role>` (or the role's live `--watch` surface),
throttling any expensive read so the refresh loop stays cheap. Examples: `minds` → allocation
(idle hands / open `[task]`) + spend (paid vs free); `plan` → situation + PLAN-next +
blocked-minds; `health` → fleet health; `sense` → fused perception. To hot-reload a live data
pane after editing its dash, `tmux respawn-pane -k -t <sess>:<win>.0` — it replaces the process
in place (no reindex, mind pane untouched); never C-c it (that closes+reindexes the pane).

## Node self-description: `~/.mesh-card`

Each node keeps a small current-state card (`mesh-card --refresh` regenerates it from live
state and checks the substrate invariant). It is the durable memory tier; the trace
(`~/.mesh/traces.log`) is the volatile history tier.

## VPN egress (scoped — operator opt-in, not the mesh's default)

The central WireGuard overlay (`vpn-hub`, `10.9.0.0/24`, `~/.wg-mesh-nodes.json`) is
**retired**. Topology is now flat Tailscale reachability + node-local/gossiped trace — no
central registry.

A node *may* offer VPN egress as an **opt-in, scoped** capability:
- The **host control plane stays on the clean route** (`Table=off`); only forwarded exit-node
  client traffic is marked (LAN+CGNAT excluded) → table → VPN interface → MASQUERADE.
- Only consenting nodes set `--exit-node=<egress-host>`.
- `vpn-health.py` (root daemon) self-heals the *scoped* tunnel; `mesh-fix-egress` re-applies it.
- **Invariant:** a node offering a route never carries its own reachability on it.
  `mesh-card --refresh` flags violations. See `docs/coordination.md`.

## Mesh tooling (`~/.local/bin/`)

**Coordinate / drive:** `mesh-tell` (drive an agent's pane; `--peek` to look) · `mesh-watch`
(wait on a pane: `--until` / `--change`) · `mesh-chat` (the board/room) · `mesh-minds` (live
capability probe) · `mesh-trace` (shared append-only trace) · `mesh-textin` (operator drives any
mind by TEXT over any channel: `@<win> cmd`; wakes the steward on plain msgs).

**Perceive (sensorium):** `mesh-location` (the phone BODY's GPS/network position — the mesh's only location sense; registry-resolved over SSH) · `mesh-body-motion` (the phone BODY's ACTIVITY sense — fuses accel/orientation/step-counter/lux in ONE SSH read → classifies STILL/CARRIED/HANDLED/COVERED; the gap mesh-location (where) + mesh-presence (who) leave: whether the body is moving/held; `--edge` for streams, exit 2 = phone unreachable) · `mesh-light` (the phone BODY's ambient-light sense — reads `tmd2755_l` once and classifies room DARK/LIT; `--edge` for streams, exit 2 = phone unreachable) · `mesh-tamper` (the body's DISTURBANCE sense — WATCHES the SIGNIFICANT_MOTION hardware trigger over a window → [body-moved]/[body-quiet]; catches a brief bump mesh-body-motion's instant-sample misses; for a parked body a fire = picked-up/moved; `--edge`, exit 2 = unreachable so a 'quiet' is never faked from an absent phone) · `mesh-body-context` (the SITUATIONAL fusion — folds body-motion + ambient into one label DORMANT/RESTING/TRAVELLING/HANDLED/STOWED, `--presence`/`--location`/`--full` add the slower BLE/GPS senses; no single sensor says much, together they do) · `mesh-presence` (BLE proximity scan → rssi|mac|name) · `mesh-presence-fuse`
(cross-node: which node a device is nearest) · `mesh-presence-fuse-stream` (cron-wired reflex on top of
it: feeds a mind when a tracked device changes zone — [zone] edge) · `mesh-presence-trends` (residents/arrivals/departures
over the log) · `mesh-find <device>` (locate any BLE thing) · `mesh-lan-newdevice` (security: alert when an unknown device joins the home LAN, via router DHCP) · `mesh-lan-health` (hardware care for NON-NODE LAN devices — iMac, TV, vacuum, MacBookPro — monitored by ping (zero footprint, no consent needed); `--edge` */5 posts [lan-up]/[lan-down] per device on state change; config: MESH_LAN_DEVICES "label:IP ..." in ~/.mesh/nodes; the "take care of all devices" complement to mesh-hw-health's node-local scope) · `mesh-wifi-link` (the phone BODY's WiFi LINK QUALITY sense — reads termux-wifi-connectioninfo PHY link speed + RSSI → EXCELLENT/GOOD/FAIR/POOR/DISCONNECTED; `--edge` 2-consecutive debounce, `reflex-cadence: 2-59/5 * * * *`; fills the gap WiFi scans miss — PHY-layer quality (interference, body absorption, failing adapter)) · `mesh-say` (speak aloud) · `mesh-act` (the mesh's first physical-world ACTUATORS beyond audio — `mesh-act <vibrate|torch|notify|ir>` fires a termux actuator on the phone body; vibrate/torch/notify operator-consented + proven by effect, `ir` gated behind its own subcommand as it drives real TVs/ACs; `--test` exit 2 = unreachable, NO fire; honest — an unreachable phone is never a successful actuation) ·
`mesh-voice-rx`/`mesh-voice-tx` (operator Telegram in/out, text+voice+photo) · `mesh-tg-roz` (send TG message to Rozalia; ROZ_CHAT_ID in ~/.mesh/nodes; BOT_TOKEN from ~/.config/remote-access/env — the tg-roz window mind's reply channel) · `mesh-roz-channel` (route Rozalia's TG messages from tg-strangers.log → tg-roz mind window; offset-tracked, */1 cron; feeds each message as a structured prompt with reply instruction) · `mesh-tg-update`
(proactive operator-notification REFLEX: cron-polled "what changed" → concise Telegram push —
landed commits + completed tasks + genuine problem-signals; marker-deduped, SILENT on no-change;
a reflex NOT a mind, so it never goes stale on a rate-limited/blocked chat mind; */15) · `mesh-watchtower`
(the mesh's eye on the OUTSIDE — runs against the public-IP node phaedra: senses inbound KNOCKS on the
public `:22` [who's scanning the mesh], external REACH from a clean datacenter vantage [reaches Anthropic
where RU-egress home nodes 403 — a geo-bypass canary], and self-EXPOSURE [what the internet can reach];
the inverse of the phone's eye-on-the-room; `--edge` on reach-flip/scan-spike, exit 2 = node unreachable). Perception is
re-observed live, never stored (no DB — a live `presence` tmux window, decays on reboot).

**Liveness / self-tend:** `mesh-card [--refresh]` (node card + invariant check) · `mesh-health` · `mesh-hw-health` (per-node HARDWARE health: cooling-efficiency / fan / disk SMART / battery-wear; catches a failing cooler early via cold-board+hot-cpu-at-light-load signature; exit 1 = FAIL) ·
`mesh-egress-health` (egress quality, not just up) · `mesh-supervise` (OTP-style child supervisor;
restarts dead/WEDGED loops; detects blocked minds) · `mesh-verify` (reboot-survival check) ·
`mesh-tick`/`mesh-heartbeat`/`mesh-beacon-watch`/`mesh-selfcare` (breath, mutual keep-alive) · `mesh-router-watch` (thermal watchdog for the fanless router gateway — edge-triggered [router-hot]/[router-cool]) · `mesh-body-power` (watch the phone BODY's battery → edge-triggered [body-power-low]/[body-power-ok] so the revived body doesn't silently die on a dead battery) · `mesh-reflex-health` (catches a reflex that is cron-SCHEDULED + smoke-passing but DEAD at runtime — its per-run artifact gone stale; edge-triggered [reflex-stale]/[reflex-ok]; the blind spot mesh-reflexes (drops) and mesh-reflex-decay (autophagy) miss) · `mesh-therm-watch` (node-LOCAL thermal edge-trigger [therm-hot]/[therm-cool] for the box it runs ON — the gap mesh-router-watch (router-over-SSH only) leaves; 88°C warn band below mesh-therm's 90°C CRIT, tuned against real multi-mind idle temps, 5°C hysteresis, therm.log artifact) · `mesh-mind-state` (classifies a mind's tmux pane WORKING/NEEDS-INPUT/RATE-LIMITED/IDLE/DEAD from the bottom pane lines → edge-triggered [mind-blocked]/[mind-limited]/[mind-unblocked]; catches the alive-but-BLOCKED state mesh-supervise (process) and mesh-phi (beat) are blind to — a mind UP for liveness but DEAD for work; we ALERT a peer to choose, never auto-answer the consent gate) · `mesh-stress` (the FUSED pre-throttle read — folds node-temp + load/nproc + mind-count [live, free] with router-thermal + egress-quality [read from the sibling reflexes' cached state, zero added SSH/curl] into ONE CALM/WARM/STRESSED/CRITICAL level that fires at the 86°C PRE-EMPT band, *below* the 92°C throttle that starves the operator channel — our known failure mode; a WARM-but-climbing node [sustained load + ≥6 minds] is escalated a band so a mind is shed WHILE there's headroom; edge-triggered [mesh-stress]/[mesh-calm] with shed-a-mind/fix-egress advice. The fusion the single-signal watchers [vitals/therm/router/egress] each miss: the operator channel dies from heat OR geo-block, this is the one read that sees both coming).

**Metabolism (inference):** `mesh-relay` (brainless inference router — text→cheapest-available-pool→text; Groq cloud primary + local-mind fallback; quota+geo-block resilient; key in gitignored ~/.mesh/groq.env, never the genome).

**Autopoiesis (self-production — the mesh produces + maintains ITSELF).** The mesh is strongly
HOMEOSTATIC (self-maintaining); these close the self-PRODUCTION loop so it is operationally CLOSED.
Two production LANES, one worker mind each: the **CODEBASE lane** (`mesh-generate` tops up the backlog →
`mesh-feed` delivers it to the idle `genome` mind → it builds/lands) and the **PERCEPTION lane**
(`mesh-sense-evolve` — when the `senses` mind is IDLE, injects ONE rotating self-development directive:
enrich a sense / cross-sense fuse / new sense / liveness; card- + idle-gated + throttled). A META-LAYER
proves the lanes don't just *fire* but *produce sound, integrated* work: `mesh-vitality` (`*/17` — VITAL
SIGNS: commit-velocity / verify-fails / stranded / tool-count Δ; edge `[vitality-low]`/`[vitality-ok]` —
catches "the lanes run but create nothing") · `mesh-needs` (`*/15` — STATE-DERIVED GOALS: turns live
deficits (failing tools / dead reflexes / decay candidates) into prioritized `[ ]` tasks so `mesh-generate`
works real needs before the static evergreen rotation) · `mesh-fitness` (`*/9` — SELECTION: judges each
self-produced HEAD; a changed tool failing `bash -n`/`--test` = regression → auto-revert on a CLEAN tree
(self-commits ONLY, HEAD-only, local), else alarm `[fitness-regression]`) · `mesh-autowire` (`*/30` —
CLOSURE: a deployed tool that self-declares a cadence and passes `--test` is auto-wired into the operating
set; opt-in, idempotent, reversible). Watchdog: `mesh-reflex-health` checks the lanes are alive at runtime
(`[reflex-stale]`). The whole loop: reflex-health=lanes fire · vitality=they produce · fitness=product is
sound · needs=goals are self-derived · autowire=products integrate.

**`# reflex-cadence:` — the self-wiring convention.** Any mesh tool meant to run on a schedule declares
`# reflex-cadence: <5-field cron>` (and optional `# reflex-args: <args>`) in its header. `mesh-autowire`
then wires it into `~/.mesh/reflexes.cron` (→ `mesh-reflexes --apply`, add-only) after a passing `--test`.
This is how a self-built reflex JOINS the operating metabolism without a human editing cron.

**Genome / substrate:** `mesh-sync-tools` (detect/heal genome↔local tool drift) · `mesh-genome-sync`
(mirror the genome off-GitHub) · `mesh-restore` (revive a node's session) · `mesh-dms` (dead-man's
switch for substrate edits) · `mesh-land` (steward lands SETTLED+parse-clean stranded stream edits;
`--check` cron alerts so [done]-but-uncommitted work never strands into drift) · `mesh-fix-egress` ·
`mesh-revert-catch` · `mesh-harden-ssh` (close the `:22` password-auth lateral-movement surface —
disables password/kbd-interactive auth, key-auth only, UNDER mesh-dms with a verified-key-login
auto-revert; refuses without an authorized_keys; `--check` is read-only).

Source of truth is the genome (`scripts/`), deployed to `~/.local/bin/`; `mesh-sync-tools` flags drift.

**On-demand canon** (genome-lean audit 2026-06-11 — unwired by design, each earns its place;
anything in `scripts/` that is neither wired (cron/systemd/mesh-restore/called-by-tool/supervise
registry) nor listed here is decay-eligible): `mesh-browse` (browser organ) · `mesh-breath` (read-only breathing probe: verifies access paths and liveness) · `mesh-claude-check` (corroborate whether Claude Code ACTUALLY works before escalating a "access DOWN" claim — cry-wolf guard; WORKING if recent claude-mind board activity OR running process not on error pane; exit 0=WORKING 1=DOWN 2=INCONCLUSIVE; call before any claude-down alarm/dormancy action) · `mesh-mind-control` (live mind table + dispatch surface: shows every mind's WORKING/IDLE/NEEDS-INPUT/RATE-LIMITED/DEAD state via mesh-mind-state + its LIVE engine via engine_of (reads the pane footer — the static manifest label DRIFTS; verified dev was opencode while labelled claude); `--watch` live dashboard; **`--allocate "<task>"` = the honest agentic mind-allocation router: classify_task() text-vs-agentic (zero-cost deterministic, 9 --test assertions; leading transform-verb→text, file/path token→agentic, ambiguous→agentic) → TEXT to mesh-relay (cheapest pool), AGENTIC to idle claude worker (rely-on-claude) else idle FREE-engine worker (opencode/codex — squeeze the free subs when claude is walled) else queue/no-capacity**; `--classify` prints just the verdict; `--dispatch` shares the same engine-aware `_pick_agentic` so the mesh-dispatch board reflex inherits free-fallback — the operator's command-and-control panel + the "squeeze every subscription" router) · `mesh-mind-compact` (keep every mind's CONTEXT lean — `/compact` is universal to both engines, but the TRIGGER is PER-ENGINE: opencode minds THRESHOLD-compact when the footer context-% ≥60% (opencode does NOT auto-compact, so this matters); claude minds INTERVAL-compact when idle > MESH_COMPACT_INTERVAL (45m default — claude auto-compacts near the limit, so this is proactive quota-leanness, not a hard need). IDLE-gated (never interrupts a working turn) + 10m hard cooldown + rlmark guard. Window set = `MESH_MIND_WINDOWS` (a DEDICATED var — NOT `MESH_MIND_WORKERS`, which is the autopoiesis FEED pool). `--high-tokens` is the wired reflex (`reflex-cadence */10`); `--status` = last-compact per mind) · `mesh-exit`
(consumer-side exit-node flip, DMS-gated) · `mesh-eye` (consent-gated ambient sense) ·
`mesh-gate-watch` (operator-approval router: polls every multi-pane tmux channel for a permission gate, notifies via Telegram so a HUMAN approves — never auto-approves; run periodically when autonomous minds are active) · `mesh-guardian` (survival reflex: reachability + tmux + Telegram organ recovery) · `mesh-morning` (steward morning round-up: each node writes its own daily report, mesh-morning collects every node's pointer + headline and Telegram-sends it to the operator; `--send` posts to TG, `--test` validates) · `mesh-plan` (planner autonomous pass: mechanical tier runs mesh-verify + stamps PLAN.md + alerts on ⚠; intelligent tier has a mind audit reflexes on a cadence when they've been on autopilot too long — free inference when available) ·
`mesh-local-mind` (local-inference primitive) · `mesh-load` (read-only agent load/quota reporter for `mesh-chat`) · `mesh-neighbour-watch` (peer SSH liveness +
restore) · `mesh-review` (multi-engine blind review) · `mesh-since` (on-return brief) ·
`mesh-novelty` (information-theory surprise signal over the board: Shannon self-information
I(x)=-log2 P(x) per event-type; surfaces the genuinely-new from routine noise and can gate
expensive minds on novelty rather than volume) ·
`mesh-study` (field-mining / study brief helper) · `mesh-transcribe` (consent-gated continuous transcription) · `mesh-hear` (consent-gated per-node
mic capture → WAV) · `mesh-ear` (consent-gated always-on wake-word ear: layer-1 energy reflex always running ~free; layer-2 local whisper triggers only on speech; layer-3 cheapest mind fires ONLY on wake word; zero idle cost — mic_always=yes consent required) · `mesh-transcribe-organ` (source-agnostic WAV → filtered text) ·
`mesh-usage` (usage aggregator backing `mesh-load`) · `mesh-spend` (per-mind spend, and the command DEPENDS ON THE MIND: claude minds = anthropic quota (`--tokens` reads real token usage from ~/.claude JSONL), opencode minds = $cost from opencode.db (free pool); window→engine→provider→tier from `~/.mesh/minds.map` (node-local; built-in default if absent). `--sample` = the wired */5 edge-sampler (records a turn + context snapshot on each rising edge into WORKING — feeds spend.log + context.log); `--by-provider` = paid/free squeeze view; `--by-model`; `--live` = per-window ctx/$ snapshot; `--all` includes zero-activity minds) · `mesh-pyparse` (catches the dead-but-green
class `bash -n` misses: a bash tool whose embedded `python3 -c '...'` has a SyntaxError that only
bites at runtime with stderr swallowed; zero-FP — validates only statically-literal blocks, skips
shell-interpolated ones; wired into `mesh-doctor`'s parse check) · `mesh-chaos-doctor`/`mesh-chaos-verify`/`mesh-chaos`
(induced-failure drills — chaos-doctor checks detectors, chaos-verify drills them, mesh-chaos is the live opt-in injector) · `mesh-fleet-health` (fleet table) · `mesh-fleet-states` (fleet-wide edge-reflex wall: every node's per-state artifacts re-derived live over SSH, used by `mesh-dash organs`) · `mesh-steward-deadman` (router
dead-man, deploy gated) · `mesh-card-watchdog.{sh,service,timer}` (card freshness) ·
`mesh-tools` (navigable tool INDEX — answers "160 scripts, hard to reason about": categories parsed from THIS tooling section, one-line descriptions from each script's header; `mesh-tools` grouped / `<category>` / `--search <term>` / `--counts` / `--uncategorized`. A living index, nothing hand-maintained) ·
`mtg-watchdog.{sh,service,timer}` (Docker-MTG proxy watchdog — node-specific, deploy on Docker-MTG nodes) ·
`bore-mtg.{sh,service}` (bore.pub MTProto proxy tunnel + Telegram link notification — node-specific, deploy on proxy nodes) ·
`node-join-android.sh` (phone onboarding) · `test-*` (verification artifacts) ·
`mesh-chat-filter` (actionability filter: reads a board line on stdin, emits a prompt only for actionable events — called by consuming minds) ·
`mesh-chat-review` (the chat mind's PROACTIVE self-analysis reflex: cron-wired (~hourly, 55m throttle) trigger that injects an analysis prompt into the IDLE chat window mind → the mind reads ~220 recent board lines and posts up to 3 concrete [chat-review] findings (flapping reflexes / low-signal noise / miscommunication / stranded-or-dup work / cry-wolf alerts) each with a fix+owner — so the chat mind ANALYSES the board on a cadence, not only when asked. Card-gated (hands-off if node declares no minds), idle-gated (never interrupts a working/blocked/walled mind), throttled; `--force`/`--test`) ·
`mesh-knowledge-sync` (anti-entropy gossip for the knowledge tier: reconciles `~/.mesh/knowledge` with all reachable peers bidirectionally, newest-wins, no deletes — fixes cultural drift on nodes that are skipped by the snapshot star topology; run periodically or after genome-sync) · `mesh-queue-tend` (ideas-queue reconciler: conservatively flips [~]→[x] when a board [done] STRONGLY matches a queued idea — never on weak matches (losing undone work > clutter); the anti-duplicate-flood mechanism that stops finished work being re-fed; called by mesh-generate) ·
`mesh-homeostasis` (egress set-point auto-repair: detects + corrects drift from the desired egress IP) ·
`mesh-resource-guard` (read-only resource monitor: reports live mind PIDs with RSS/CPU and enforces soft/hard thresholds) ·
`mesh-tg-watchdog` (TG-organ liveness monitor: alerts operator if the Telegram path from default-string goes down — designed to run on a non-default-string node) ·
`mesh-attach` (mesh-wide tmux: list all nodes' hostname-named sessions + attach any from one command; self-detects own node to avoid SSH round-trip to self) ·
`mesh-organ` (the CAPABILITY ROUTER — run an organ by NAME wherever it physically lives: `mesh-organ camera` resolves a node that HAS a camera (mesh-organs --json), runs it there over SSH, returns the artifact; `--list`/`--where`/`--node`/`--manifest`. Location transparency layer B — "it shouldn't matter WHERE the organs are"; see knowledge/location-transparency-design-2026-06-13) ·
`mesh-digest` (brainless daily summary of what changed on this node: git log + trace tail + health snapshot — operator orient/verify tool) ·
`mesh-sensorium` (one-shot WHOLE-NODE perception dump: runs every sense tool best-effort → one timestamped report of what THIS node perceives now (health/therm/presence/wifiscan/audio/card); `--compact` one-line-per-sensor. The per-node breadth peer to mesh-body-context's body-only fusion + mesh-organ's single-organ run; distinct from mesh-snapshot's tmux-memory backup) ·
`mesh-perimeter` (the mesh's SURROUNDINGS fusion — folds OUTSIDE (mesh-watchtower: phaedra public-IP vantage — external scanners/reach/exposure) + NETWORK (mesh-lan-newdevice: new/unknown home-LAN device, baseline read READ-ONLY so it never races that reflex) + PHYSICAL (mesh-presence: unknown BLE in range) into ONE CALM/NOTICE/ALERT situational read; answers "is anything unusual around?" no single axis can. The outward/security peer to mesh-sensorium's inward node-dump and mesh-body-context's body-only fusion; honest — an UNREACHABLE axis renders "[UNREACHABLE] … BLIND, not clear" and the verdict goes "partial", never a faked all-clear; all-3-down = CANNOT-ASSESS exit 2. Routable via `mesh-organ perimeter`) ·
`mesh-stream` (universal primitive: pipe any data stream into a mind's tmux session as a keystroke prompt — the SOURCE→FILTER→FEED pattern) ·
`mesh-channels` (instantiate the full CHANNEL-SET from `~/.mesh/streams.conf` — one pull→delta→feed per channel per call; cron-driven so a mind is only fed when its state changed) ·
`mesh-nodestate` (STATE-FN: emit one line per tag:lte-node node → `hostname: online|offline`; clean state source for the node-liveness stream channel — feeds mesh-channels/mesh-delta) ·
`mesh-verify-gate` (gate the verify-stream tick: fires the verify-stream ONLY when state changed or stale-min elapsed — kills saturating re-tread of already-green tools; same pattern as mesh-tick-gate) ·
`mesh-fleet-feed` (cross-node data feed: each node posts its own slice to peers, liveness falls out of replication staleness) ·
`mesh-presence-delta` (presence stream filter: diffs consecutive scans, emits a mind-prompt only on device changes — used in presence pipelines) ·
`mesh-arrivals` (the "who's around" LIFE-EVENT sense: emits [arrived]/[left] ONLY for a KNOWN/NAMED device (phone/Bose/Quest/TV), suppressing randomized-MAC churn. Two refinements over mesh-presence-delta: (1) NAME identity not MAC — a device's MAC rotates but its name is stable, so randomization ≠ leave+arrive; (2) DEBOUNCE — declares LEFT only after MESH_ARRIVAL_MISSES consecutive absent scans (default 3), killing the single-scan RSSI-flicker flap. Honest-fusion: a failed/empty/unreachable scan never increments misses (absent vantage ≠ everyone-left, exit 2); first run seeds silently. Multi-vantage union via `--vantages "local default-string"` (unreachable peer skipped, not an absence); composes as a mesh-stream filter (reads a scan on stdin). The PHYSICAL-presence sibling to mesh-perimeter(surroundings)+mesh-stress(internal)) ·
`mesh-situation` (the META-fusion — ONE answer to "what's the mesh's situation right now?", folding INTERNAL (mesh-stress: node thermal/load/minds) + EXTERNAL (mesh-perimeter: surroundings) + PHYSICAL (mesh-arrivals: who's around) → NOMINAL/WATCH/ALERT, the worst of the two load-bearing axes; PHYSICAL is the context line. The operator's "connect the sensors, don't go in a circle" capstone. CHEAP by design — does NOT re-run the heavy external scan: INTERNAL is a light mesh-stress --json, PHYSICAL reads arrivals.state (no BLE scan), EXTERNAL reads mesh-perimeter's CACHED verdict (.perimeter.state); `--refresh` freshens the external axis live, `--json` for machines; `--edge` REFLEX posts [situation-*] on posture change + [escalate:tg-window] on ALERT (wired */15 cron, sense→act loop closure). Honest-fusion: a STALE/missing axis renders UNKNOWN + flips posture to "(partial)", never silently NOMINAL) ·
`mesh-operator-home` (the OPERATOR-PRESENCE oracle — "is the operator physically home?": fuses phone-on-home-LAN (ping PHONE_LAN_IPS, strongest signal) + operator BLE devices at strong RSSI (Bose/Quest via MESH_OP_BLE_DEVICES env, default threshold -82 dBm) + Tailscale phone status → HOME/AWAY/UNCERTAIN; `--edge` */5 cron posts [op-home]/[op-away] on change; `--json` for machines; foundation for household-state. Config: PHONE_LAN_IPS, MESH_OP_BLE_DEVICES, PHONE_TS_IP) ·
`mesh-operator-state` ("what is the operator doing?": fuses body-motion (STILL/CARRIED/HANDLED/COVERED + lux + steps-delta) + BLE Bose proximity → AT-PHONE/NEARBY/AWAY/COVERED/ASLEEP/UNKNOWN; requires phone online (body-motion via SSH); `--json`, `--watch` refresh loop; called by mesh-sense-monitor for the derived display pane; canonical "attention" sense — compose with mesh-operator-home for "in-building + doing-what" picture) ·
`mesh-home-state` (the CAUSE LAYER — "what is happening at home?": fuses sensors.log + presence.log + transcription → QUIET_NIGHT/ASLEEP/WAKING/ACTIVE/ACTIVE_SOCIAL/AWAY (correlated inference, not just per-sensor fact); wired */5 cron, appends to ~/.mesh/home-state.log; `--json`, `--watch`; called by mesh-household-state as its richer inference engine) ·
`mesh-household-state` ("household mode?": ACTIVE/ASLEEP/AWAY/UNCERTAIN — thin stable 4-class API over mesh-home-state (maps 6-class vocabulary to 4); `--edge` */5 cron posts [household-*] on mode change; `--json`; use when a simple stable API is needed; mesh-home-state for rich context) ·
`mesh-channel-tg` (TG voice-in channel combinator: wraps mesh-channel+mesh-tg-filter→claude for Telegram voice input) ·
`mesh-chat-agent` (conversational chat-room agent: watches chat.log, answers operator in their language via opencode, speaks reply — on-demand conversation mode) ·
`mesh-phone-ip` (probe-based phone IP resolver — tries PHONE_IP env → mesh-peer-addr Redmi → PHONE_LAN_IPS, returns first that ACCEPTS an SSH connection on PHONE_SSH_PORT; fixes the dead-LAN-fallback bug where TS IP always returned even when sshd killed by MIUI; all phone body tools call this; exit 2 = all IPs unreachable) ·
`mesh-phone-watch` (ADB-based sshd watchdog: checks whether sshd is listening on PHONE_SSH_PORT via ADB and restarts via Termux RunCommandService if MIUI killed it; ADB is a system daemon MIUI can't kill; exit 2 = ADB not connected; operator must pair ADB over WiFi first — on-demand until paired) ·
`phone-setup` (phone-body bootstrap: deploys mesh-phone-ear + mesh-phone-sensors to the phone via SSH, adds Termux:Boot autostart — run once per phone; unwired by design, deploy-tool not a reflex) ·
`mesh-phone-ear` (phone-body screen-unlock-gated ear: runs ON THE PHONE, not on laptop nodes — records mic→sends to IdeaPad whisper→feeds board; exit 2 = not on phone; launched by phone-setup via Termux:Boot; `--once` for one cycle) ·
`mesh-phone-sensors` (phone-body sensor demo: exercises battery/location/light/accel/wifi/camera → real artifacts; `--probe` = reachability check, `--notify` = TG alert) ·
`mesh-phone-convo` (phone voice conversation: phone mic (opus)→WAV→whisper.cpp→mesh-relay→termux-tts-speak; `--loop` for continuous; exit 2 = phone offline; consent: mic_always=yes required) ·
`mesh-sms` (SMS via phone body: termux-sms-send over SSH; TG-independent alert channel; config: MESH_SMS_NUMBER env or ~/.mesh/sms.conf; exit 2 = phone unreachable) ·
`mesh-room-sense` (ROOM OCCUPANCY fusion — folds BLE presence (IdeaPad-local, named device RSSI) + WiFi RSSI motion (phone) + ambient light (phone) → PRESENT/EMPTY/UNCERTAIN; honest-degraded when phone offline (BLE-only path); `--edge` for cron wiring, `--json` for machines; wired */5 edge reflex posting to board on state change; the "is someone home?" sensor) ·
`mesh-tick-gate` (generic state-change gate for tick commands: fires a mesh-tick ONLY when monitored state-files changed OR gate is stale-min elapsed — kills quota-draw on already-green tools; mirrors mesh-verify-gate but uses file-content hash not git SHA; `--test` for smoke) ·
`mesh-wifi-motion` (WiFi passive radar: detect room motion from RSSI delta between consecutive scans over SSH to phone; STILL/MOTION/UNCERTAIN from ±2/5 dBm thresholds; `--edge` for cron wiring, `--test` = exit 2 if phone unreachable; feeds mesh-room-sense WiFi axis) ·
`mesh-hw-health` (per-node HARDWARE health check: cooling efficiency [cold-board+hot-cpu-at-light-load = dead cooler, the ds-2026-06-14 signature], fan RPM, disk SMART, battery wear; exits 1 on FAIL; local/quota-free; on-demand or post-reboot) ·
`mesh-mode` (operating mode manager — lean/normal/full/dormant tmux-window set: lean=tg+shell, normal+health, full=all minds; manages which windows are open but does NOT touch cron/reflexes; combine with reflexes.cron PAUSED lines for full dormant effect; on-demand, no cron) ·
`mesh-tv` (TV organ — play a YouTube/video URL on the Sony Bravia KDL-42W653A via DLNA AVTransport: SSDP discovers first UPnP MediaRenderer on LAN, yt-dlp resolves YouTube to H.264 CDN URL, pushes to TV; `--discover` finds+saves TV IP, `--stop` stops playback; dep: yt-dlp; no pairing; exit 2 = TV not found) ·
`mesh-url-watch` (LLM-free TV-organ reflex: watches voice-in.log for video URLs from operator Telegram → calls mesh-tv to play on TV; offset-based so only new lines trigger; wired */1 cron; exit 2 = n/a if voice-in.log or mesh-tv absent) ·
`mesh-sensor-log` (append-only time-series sensor log: wifi_rssi/cpu_temp/phone_battery/light/steps/room_sense to ~/.mesh/sensors.log; --tail/--grep/--diff/--edge subcommands; --diff emits MOVED/SAME_ROOM verdict; --edge = */5 cron reflex, posts [room-moved] to board once when dominant AP changes AND is stable across 2 consecutive scans (debounced — near-tied APs suppressed), seeds silently on first run; phone via mesh-phone-ip ADB tunnel) ·
`mesh-ambient-clock` (ambient social clock from fixed-appliance BLE: harvests neighbor TV/AC/scale cycling excluded by mesh-arrivals → label QUIET/MODERATE/ACTIVE/NIGHT-QUIET; --edge = */10 cron reflex, posts [ambient-clock] to board on label change; --json for machines; called by mesh-sense-monitor for the derived display pane) ·
`mesh-sense-monitor` (DERIVED-SENSE DISPLAY — one-shot or `--watch` loop for the `derived` top pane: fuses operator-state + ambient-clock + room-sense + node-stress into a single human-readable sensorium view. On-demand/dash tool; runs in a tmux top pane, not wired to cron. Peer to mesh-situation (meta-fusion verdict) and mesh-sensorium (raw node dump) — this is the human-readable derived layer) ·
`mesh-spend` (per-mind spend — see the canonical entry above; command depends on the engine: claude=quota/`--tokens`, opencode=$cost; `--sample` is the */5 cron). Decayed
2026-06-11: `mesh-health-watch` (→ mesh-session-watchdog), `mesh-tg-recv` (→ voice-rx+textin),
`mesh-zone` (→ presence-fuse/trends), `vpn-hub.py` (retired overlay), `mesh-onboard` (attic:
junk-posted onboarding wrapper; keep out of canon). Decayed 2026-06-13: `mesh-board-timerepair` (one-shot 2026-06-11 board date-repair, no longer needed). Git history is the attic.

## Capabilities (self-declared, opt-in by consumers)

Classes: **minds** (agents) · **senses** (sensors) · **actuators** (act on the world —
phone TTS/SMS/calls/IR) · **connectivity** (exit-node, public ingress, independent uplinks) ·
**compute**. A node declares what it offers; consumers read the trace/card and opt in. Nothing
is imposed.

**The card capability is AUTHORITATIVE — a node that does not declare `minds:` is HANDS-OFF
(operator rule 2026-06-15).** If a node's `~/.mesh-card` `minds:` line does not list an engine,
the mesh must **not touch that node's minds at all** — never relaunch, shed, kill, feed, nudge,
or dispatch to them. A node can run mind binaries (claude/opencode/codex) for its *operator's own
use* without the mesh treating them as mesh minds; blanking the card's `minds:` line is the clean
"minds off the mesh" switch. Every mind-touching tool gates on the card: `mesh-restore` (launch),
`mesh-mind-keepalive` + `mesh-channel-keepalive` (relaunch/**shed**) all skip when the card declares
no minds — so the early-return means a decommissioned node's panes are never even read, let alone
killed. **Never blanket-`pkill` a mind engine by user** (`pkill -u <user> claude`) — it kills the
operator's *own* sessions too; scope kills to the specific mesh-session pane via the card-gated tool,
never a process sweep. To decommission a node's minds: blank the card `minds:` line + set
`MESH_ROLES=<node>:compute` (steward stops feeding board/knowledge) + pause its mind-driving reflexes
(`mesh-tick`/`chat-sync`/`channel-keepalive`/`supervise`/`mind-keepalive` in `reflexes.cron`).

## Key paths

- Node config: `~/.mesh/nodes` (gitignored, runtime) · `nodes.example` (committed, template)
- Operator context: `CLAUDE.local.md` (gitignored, per-node)
- Mesh tools: `~/.local/bin/mesh-*` · trace: `~/.mesh/traces.log` · card: `~/.mesh-card`
- Services: `~/.config/systemd/user/`
