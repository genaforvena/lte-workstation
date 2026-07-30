# LITERATURE review — Viable System Model (Stafford Beer), cross-domain transfer to a distributed sensor mesh: **System 2 is not System 3** (2026-07-28)

**Area:** the Viable System Model / management cybernetics (Stafford Beer), entered from the task's
angle — a **cross-domain transfer** of one VSM mechanism, applied concretely to a real contended organ
on this node. Landing on a concept the mesh does **not** embody.

## The concept — System 2 (anti-oscillatory coordination), distinct from System 3 (audit/allocation)

Beer's VSM decomposes any viable system into five recursive subsystems. The one this review lands on is
**System 2 — the coordination function**, which Beer explicitly names the *sympathetic nervous system*.
Its single job is **anti-oscillation**: when several autonomous **System 1** units share a **constrained
resource**, S2 damps the destabilising swing where unit A seizes the resource, then B, then A —
"the oscillating pattern where one unit gains resources, then another, creating destabilizing swings"
(vsm-docs, *Subsystems*). S2 owns no operations and issues no orders; it **harmonises timing** between
peers so their competition does not thrash.

The load-bearing distinction — and the reason this is a genuine gap rather than a rename of something we
have — is that **System 2 is not System 3**:

- **System 3** is *vertical*: resource-allocation and **audit/accounting** of the S1 units — "how much
  did each unit spend, is each staying inside its resource bargain." It looks **down and after**.
- **System 2** is *horizontal*: it sits **between** the S1 units and **prevents** the oscillation
  **before** it costs anything. It looks **sideways and ahead**.

Beer's whole point is that these are **different organs**. A system can have a perfect audit channel
(S3) and still oscillate itself to death because it has **no S2**. The MDPI 2025 survey formalises this
as a named **organisational pathology**: *missing System 2 → uncontrolled oscillation between operational
units*, diagnosable structurally (units contending for one resource with no coordinator between them),
independent of whether S3's books balance.

**Sources (read 2026-07-28, live literature):**
- *VSM Subsystems* — https://viable-systems.github.io/vsm-docs/subsystems/ — states the S2 anti-oscillation
  mechanism directly ("dampen resource conflicts … prevents the oscillating pattern … one unit gains
  resources, then another"), and the algedonic channel as a separate event-driven bypass. This is the
  active *viable-systems* project (2025, VSM as modular Elixir packages: distributed event systems,
  algedonic signals, an added *temporal variety channel*) — Beer's model as **live, worked** code, not a
  fixed citation.
- Rezaee et al., *The Viable System Model and the Taxonomy of Organizational Pathologies in the Age of
  AI*, **Systems 13(9):749, MDPI, 2025** — https://www.mdpi.com/2079-8954/13/9/749 — catalogues VSM
  structural pathologies (missing/blocked S2, S3 over-centralisation crushing S1 autonomy, blocked
  algedonic channel) as **diagnosable signatures**, which is what makes "missing S2" a checkable claim
  about a system and not a metaphor.

## The cross-domain transfer — the GPU is our contended resource, and it has an S3 but no S2

On mesh-home the **RTX 3060 (12 GB VRAM)** is the mesh's *sole* local-inference organ and its most
contended resource. The autonomous **System 1 units** competing for it are real and already enumerated in
our own code — `mesh-vram-watch:8` names them verbatim: *"ollama (moondream, qwen2.5:3b, qwen3.5:0.8b),
gigaam + resemblyzer (venv-ai), moondream vision — all contend for 12GB."* Add the warm **XTTS
voice-clone daemon** holding VRAM resident. These organs fire on **independent triggers** (a room
utterance wakes gigaam; a vision ask wakes qwen3-vl; a TTS call wakes XTTS) with **no coordinator between
them**.

What we already have maps cleanly onto VSM — and the map is exactly what exposes the hole:

| VSM organ | Mesh tool | What it does |
|---|---|---|
| **System 3 — audit/accounting** | `scripts/mesh-gpu-ledger` | Charges each organ its post-mortem GPU-ms (per-PID accounting ring). Looks **down and after**: the *bill* for GPU time. |
| **System 3 — resource sense** | `scripts/mesh-vram-watch` | Watches VRAM pressure / spill / throttle; fires CRITICAL at ≥90% used — *"about to evict / spill"* (`:67`). A **pain sensor** for contention. |
| **System 2 — anti-oscillation** | **— absent —** | Nothing serialises or damps contention *across* organs. |

The only serialisation that exists is **intra-organ**: `mesh-voice-clone-daemon:82`
(`_lock = threading.Lock()  # GPU is single-writer; serialize synth`) serialises XTTS's own calls — but
that lock is **invisible to gigaam, ollama and vision**. Each S1 unit is single-writer *to itself* and
blind to its peers. That is precisely Beer's missing-S2 pathology: **we built the audit (S3) and the pain
sensor, and skipped the sympathetic nervous system.** `mesh-vram-watch` can only *name the pressure after
the swing has started*; `mesh-gpu-ledger` can only *bill the thrash after it has been paid for*. Neither
is S2, because **a meter is not a governor** — measuring an oscillation is not damping it.

The failure mode is concrete and matches VSM's prediction exactly: two large models triggered within the
same window on a 12 GB card → VRAM headroom exceeded → the driver/ollama evicts one warm model to load
the other → the evicted organ's next trigger reloads it, evicting the first → **load→evict→reload
oscillation**, each reload paying the multi-second cold model-load our own notes measure (gigaam 2.7 s
one-time load; whisper ~11 s; XTTS warm-resident). This is the `gigaam-warm-daemon-degrades` /
`writer-redundancy-blinds-mtime` family seen from the resource side: every organ stays cron-green, the
*bill* (`mesh-gpu-ledger`) simply rises, and nothing ever reports **"we are thrashing."** The pathology is
silent to an S3-only system by construction.

## Proposed concrete application — a System-2 admission gate (name the file)

**One concrete organ:** a horizontal **GPU anti-oscillation coordinator** — proposed
`scripts/mesh-gpu-coord` — that any big-model GPU organ calls to **acquire before loading a model** and
releases after. It is *not* another meter and *not* a load ceiling; it is Beer's S2:

- **A single cross-organ lock/lease keyed on live VRAM headroom** read from `mesh-vram-watch` (the sense
  already exists; wire it as the S2 *input*). An organ requesting a load that would push used-VRAM past
  the evict threshold **waits** for headroom instead of racing the driver into an eviction.
- **Hysteresis / a minimum hold** on a just-loaded model, so a warm model cannot be evicted-and-reloaded
  inside one short window — the direct anti-oscillation term. This is the *timing harmonisation* S2 is
  for, not priority and not accounting.
- **Peers, not a boss.** S2 coordinates autonomous units; it must not become S3. It does **not** decide
  *which* organ is more important (that would be the S3/algedonic lane — `priority:incident`, already
  ours); it only prevents the *swing*. Keeping S2 and S3 separate is the whole lesson.
- **Verification (house doctrine):** the gate is a **non-trivial machine** — its behaviour is the
  *sequence* (acquire A → B blocks on headroom → A releases → B proceeds; and: reload within the hold
  window is refused). Per `nontrivial-machine-test-a-sequence`, its `--test` must drive that **sequence**
  under a mocked `nvidia-smi`/vram source, not one shot — and must be seen to go RED when the hysteresis
  hold is removed. Exit 2 where no GPU is present (honest n/a), so `mesh-land` still lands it on
  GPU-less nodes.

**Minimal-surface alternative** (if a new organ is judged too heavy): fold the acquire/hold into the
existing warm daemons that already own a GPU lock — extend `mesh-voice-clone-daemon`'s `_lock` into a
**shared, cross-organ file-lock** that gigaam and the ollama callers also honour. Same S2 semantics, no
new cron organ; the cost is that the coordination logic lives scattered across organs instead of in one
named S2. The clean-VSM answer is the dedicated coordinator; the cheap answer is the shared lock.

## Honest scope

- **The oscillation is a structural risk our own `mesh-vram-watch` comment already anticipates
  (`:8`, `:67`), not a logged incident I measured today.** I did not catch the GPU mid-thrash; I am
  transferring Beer's *prediction* onto a contention our code already names. The S2 gate is worth adding
  because an S3-only design **cannot see** the thrash to log it — but the honest claim is "predicted +
  structurally present," not "observed firing." First step before building: have `mesh-vram-watch` or
  `mesh-gpu-ledger` **log evict/reload events** so the oscillation becomes an *artifact*, then size the
  hysteresis against real data rather than a guess.
- **Not the algedonic channel.** VSM's algedonic signal (event-driven bypass straight to policy/System 5)
  is *partially* embodied already — `priority:incident` on the board bypasses FIFO dispatch, and TG pokes
  reach the operator directly. That lane is S3/S5, not S2; conflating them is the exact error this review
  is about. S2 is the piece we do **not** have.
- **Temporal variety channel** (the 2025 vsm-docs extension: predictive, time-series variety management)
  is largely **already ours** — CSD/critical-slowing-down (`allostasis-love-the-noise-viability-csd`),
  two-timescale predictive processing, `mesh-criticality`. That extension would be re-treading covered
  ground; **System 2 is the untrodden one.**
