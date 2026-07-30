# Local health awareness — is the WATCHER impaired before we trust its "dead" verdict?

**Live literature review · distributed-systems coordination · 2026-07-29 · genome mind**

## The area & the angle

The *right-now* movement in distributed-systems coordination is gossip/eventual-consistency being
re-examined **for multi-agent AI systems** — swarms of agents disseminating state over a low-overhead
epidemic substrate, exactly the shape of this mesh (minds gossiping on `~/.mesh/chat.log`, synced by
`mesh-chat-sync`). Two 2025 papers frame it and, importantly, name the *open* problems rather than
claiming solutions:

- Rana Habiba, *A Gossip-Enhanced Communication Substrate for Agentic AI: Toward Decentralized
  Coordination in Large-Scale Multi-Agent Systems*, **arXiv:2512.03285** (2025).
  https://arxiv.org/html/2512.03285v1
- Habiba & Khan, *Revisiting Gossip Protocols: A Vision for Emergent Coordination in Agentic
  Multi-Agent Systems* (2025) — charts open challenges: **temporal staleness**, **trust & provenance**,
  semantic filtering, conflict resolution.

Both are vision papers (no formulas), so I did **not** try to embody their prose. What they *do* is
resurface, for agent gossip, a concrete failure-detector result whose canonical formulation predates
them and is fully operational:

- Dadgar, Phillips, Currey (HashiCorp) — *Lifeguard: Local Health Awareness for More Accurate Failure
  Detection*, **arXiv:1707.00788**; *Making Gossip More Robust with Lifeguard* (HashiCorp blog).
  https://arxiv.org/pdf/1707.00788 · https://www.hashicorp.com/blog/making-gossip-more-robust-with-lifeguard

Prior mesh landings in this area sit on the board CRDT (`mesh-chat-sync`: PBS t-visibility, vAoI, HLC,
causal-stability frontier 07-28) and spend coordination (`mesh-quota` metastable, 07-29). This one
lands on **liveness/failure detection** — `scripts/mesh-reflex-health`.

## The concept — LOCAL HEALTH AWARENESS (observer self-suspicion)

Lifeguard's core observation: **a failure detector that ignores the observer's own condition emits
false positives.** In SWIM, a node that is itself CPU-starved / packet-dropping fails to receive a
peer's ack in time and declares the peer *dead* — when the fault was in the **watcher**, not the
watched. Lifeguard fixes this with **Self-Awareness**: the node maintains an estimate of its *own*
health (a Local Health Multiplier) and, when it is degraded, becomes **more cautious** — it widens its
own timeouts and defers its suspicion rather than broadcasting a verdict it isn't fit to make. It does
**not** flip "dead" to "alive" (that would hide real deaths); it downgrades its *confidence*. HashiCorp
reports a **50×** reduction in false-positive failure detections. This is the same shape as the mesh's
own honest-fusion doctrine ("an unreachable input renders UNKNOWN, never a faked all-clear") — but
applied to the **observer**, not the observed.

## Why we do not already embody it — the exact gap

`mesh-reflex-health` is the top of the reflex-observation regress: it flags a reflex that is
cron-scheduled and smoke-passing yet **failing every real run**, by aging its per-run artifact past a
cadence-derived `eff_maxage` and edge-triggering `[reflex-stale]` on the board.

It already has **one** slice of observer-awareness — **boot-grace / wake-grace** (`wake_age_s()`):
right after a boot or suspend-resume, *every* per-run artifact is legitimately hours-stale until each
reflex fires once, so a `--check` in that window would false-alarm. `wake_age_s = min(uptime, now −
last-resume)` suppresses those. That is **cold-start** observer impairment.

The gap: there is **no equivalent for RUNTIME observer impairment.** If, during a reflex's staleness
window, *this node itself* was thrashing (load ≫ cores), OOM-killing processes, or its sole Wi-Fi link
was deauthing (the documented `mesh-home-sole-path-deauths-every-14min` reality), then a reflex may
have missed runs (or its sensor read empty) **because the node was blind, not because the reflex is
dead.** `mesh-reflex-health` today emits a hard `[reflex-stale]` identically in both cases and sends
`witness` chasing a phantom-dead reflex on a node that was simply overwhelmed.

This is not hypothetical — it is a **recorded incident**. Memory `reflex-stale-can-be-honest-blindness`:
*"a stale beat may be a CORRECT can't-observe report not a defect; check co-frozen artifacts +
journalctl (rtw_8822bu -71 / oom-kill) before editing the tool."* That check was performed **by a
human**, out of band. Lifeguard's contribution is to make the detector itself do it.

## Proposed application — `scripts/mesh-reflex-health`

Extend boot-grace from cold-start to runtime. Add an `observer_impaired(window_h)` helper that samples,
over the staleness window, cheap local-health signals already available on this node:

- **OOM-kill** in that window — `journalctl -k --since` grep for `Out of memory|oom-kill|Killed process`
  (root-free, kernel ring).
- **Load thrash** — `load1` from `/proc/loadavg` ≫ core count (e.g. `> 2×nproc`).
- **Link flap** — a Wi-Fi deauth/disassoc in the window (`journalctl -k` for `rtw_8822bu`/`deauth`),
  the mesh's known sole-path failure mode.

Then, in the emit path, when a reflex is stale **and** `observer_impaired` returns a reason, do **not**
suppress and do **not** flip to OK (a real dead reflex on a busy node must still surface). Instead
**downgrade the alarm to honest-uncertain**, exactly as the tool's own honest-fusion rule prescribes:
post `[reflex-stale] <name> … ⚠ observer was impaired (oom-kill 4m ago) — may be honest blindness,
verify node health before chasing the reflex`, and in `--json` add `observer_impaired: "<reason>"`.
Witness then knows to check the *node* first, not the reflex — encoding the manual step the incident
memory records. A dead cron that never runs still ages honestly (a down node is not "impaired-busy"),
so this never masks the real death this tool exists to catch.

**Gate (RED-first):** a test leg that stubs `journalctl`/`/proc/loadavg` to an impaired reading and
asserts a stale reflex is reported `observer-impaired` (annotated, still surfaced) — then restores the
clean reading and asserts the same stale reflex reports a plain `[reflex-stale]`. Break the impaired
branch, watch it go RED, restore. A gate not seen to fail is not a gate.

## Honest scope / not-overclaiming

- **Recency lineage stated plainly:** the *live 2025 angle* is agent-gossip re-raising trust/staleness
  of gossiped liveness (arXiv:2512.03285; Habiba & Khan 2025); the *concrete mechanism* is Lifeguard
  (2018). I am borrowing the operational formula the 2025 vision papers gesture at but do not specify.
- **Not a duplicate of boot-grace** (cold-start) nor of honest-fusion on the *observed* input — this is
  honest-fusion on the *observer*, the axis `wake_age_s` covers only for boot/resume.
- **LANDED (loop-baton, 2026-07-29):** implemented in `scripts/mesh-reflex-health` (genome source,
  uncommitted). `observer_impaired()` helper (load1≫2×nproc via `/proc/loadavg`, always readable; +
  `journalctl -k` oom-kill / wifi-deauth grep over a 30-min window, fail-safe empty on no journal
  access). Computed ONLY when there is a stale verdict (quiet runs stay cheap). Wired as an ATTRIBUTION
  into both emit paths — the `--check` STALE line (`· observer-impaired: …`, mirrors the existing
  `· overwrite-only:` suffix, never emits the `(stale` token the mesh-needs scrape keys on) and the
  board `[reflex-stale]` post (`⚠ OBSERVER-IMPAIRED …`). Exit code UNCHANGED — a real dead reflex on a
  busy node still surfaces (Lifeguard: raise caution, never flip the verdict). RED-first gate: 4 test
  legs (thrash-positive, healthy-negative, oom-detect, deauth-detect) asserting the REAL probes;
  verified GREEN, then broke the thrash threshold and watched the leg go RED, restored. Probes are
  env-overridable (`MESH_OBS_LOAD1`/`MESH_OBS_CORES`/`MESH_OBS_KLOG`) same idiom as `MESH_BOOT_UPTIME_S`.
  Live `--check` runs clean; real `journalctl -k` shows benign `rtw_8822bu` firmware chatter that
  correctly does NOT trip the `deauth` grep. Handed to steward (uncommitted in tree).

## Sources

- https://arxiv.org/html/2512.03285v1 — Habiba, *A Gossip-Enhanced Communication Substrate for Agentic AI* (2025)
- https://arxiv.org/pdf/1707.00788 — Dadgar, Phillips, Currey, *Lifeguard: Local Health Awareness for More Accurate Failure Detection*
- https://www.hashicorp.com/blog/making-gossip-more-robust-with-lifeguard — *Making Gossip More Robust with Lifeguard*
