# Study finding — self-optimization (autopoiesis / biology of cognition)

**Source:** auto idea-queue task — LITERATURE (live review): autopoiesis & the biology of cognition
(Maturana, Varela), from the angle of a RECENT result (2023–2026) (2026-07-24).
**Verdict:** Finding + concrete proposal for `scripts/mesh-homeostasis`. Filed as a proposal, not landed.
**Date:** 2026-07-24 · owner: genome

## The concept, and what's recent

Classical autopoiesis (Maturana & Varela) explains how a living system *maintains* its own organization —
operational closure, structural coupling, homeostasis toward set-points. It says little about how a system
gets *better* at regulating itself over time without an external designer or teacher. The recent result
closing that gap is **Self-Optimization (SO)** — the enactive lineage's answer to "how does an autopoietic
regulator learn its own good configurations?"

The mechanism (Watson et al.'s self-modeling, now given an explicit enactive/autopoiesis reading by Froese):
a system that (1) repeatedly relaxes to whatever *local* attractor its current constraints pull it into,
(2) applies a Hebbian rule that **reinforces the state it just landed in**, and (3) resets to an arbitrary
start and repeats — will, over many reset→relax→reinforce cycles, *reshape its own constraint landscape* so
that later relaxations reliably reach a **better global constraint-satisfying state** than any single local
relaxation could. It is associative memory turned on the system's OWN dynamics: the system learns the
correlation structure of its previously-visited good states and widens their basins. Homeostasis seeks a
fixed equilibrium; self-optimization *learns which coordinated equilibria are good* and biases recovery
toward them.

Live 2023–2025 sources:

- Froese, Weber, Shpurov, Ikegami (2023), *From autopoiesis to self-optimization: Toward an enactive model
  of biological regulation*, **BioSystems** — <https://www.sciencedirect.com/science/article/abs/pii/S030326472300134X>
  (PubMed <https://pubmed.ncbi.nlm.nih.gov/37380066/>): frames regulation via precariousness + adaptivity +
  agency reaching *coordinated constraint satisfaction at the system level*, bridging autopoiesis to
  unsupervised-learning dynamics rather than fixed equilibrium-seeking.
- *Untapped Potential in Self-Optimization of Hopfield Networks: The Creativity of Unsupervised Learning*,
  arXiv **2501.04007** (Jan 2025) — <https://arxiv.org/pdf/2501.04007>: current-frontier treatment of the SO
  loop (Hebbian reinforcement of relaxed attractors + resets → global constraint satisfaction).
- *Self-Optimization in Continuous-Time Recurrent Neural Networks*, Frontiers Robotics & AI (2018/2021) —
  <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7805835/>: the SO principle is substrate-general (not tied to
  discrete Hopfield units), which is what makes the transfer to a mesh's discrete reflex-state vector legitimate.

## Why this is NOT already embodied — and where exactly the gap is

Honest check first. The mesh embodies most of autopoiesis already: a self-production lane (`mesh-generate`
→ `mesh-feed`), adaptivity (`mesh-load-gate` shedding, `mesh-mode`), and per-axis homeostasis. In particular
`scripts/mesh-homeostasis` is a genuine regulator — an **integral controller** that accumulates error-seconds
when the public IP drifts from the NL set-point and escalates log → alert → fix (`mesh-homeostasis:3-5`).

But that is exactly classical, single-axis, **fixed-set-point** equilibrium-seeking — and it is the shape of
*every* homeostat in the mesh: each reflex drives ONE axis toward ONE hardcoded target, blind to the others.
Nothing in the mesh:

1. records the **global state vector** of its own regulation at moments of coordinated health (egress on
   set-point AND load nominal AND spend in-band AND the reflex fleet green), nor
2. learns the **correlation structure** across those good vectors, nor
3. uses that learned structure to bias recovery toward the nearest *previously-visited coordinated-good
   basin* instead of yanking each axis independently toward its own set-point.

That triad — the reset→relax→reinforce loop over the system's own state history — is the self-optimization
mechanism, and it is absent. The mesh has memory of *events* (traces, ledger) but no associative memory of
its own *healthy configurations* that regulation can descend toward. Fixing egress while load is pathological
can land the node in a locally-satisfying-but-globally-bad corner SO is designed to escape.

## Concrete proposal — `scripts/mesh-homeostasis`

Generalize the single-axis I-controller into a system-level self-optimizer (a `--optimize` capability
alongside the existing egress controller; the egress loop stays as-is, this adds the missing tier):

- **State vector:** on each pass, sample a small fixed vector of ±1 axes already cheaply available —
  egress-on-set-point, load1<threshold, spend-in-band, key reflexes fresh (`mesh-reflex-health`),
  thermal-nominal (`k10temp`). This is the mesh's regulatory "attractor."
- **Reinforce:** when the whole vector is coordinated-good (a healthy relaxed attractor), Hebbian-update a
  persisted weight matrix `W` over axis pairs (`~/.mesh/homeostasis-somem.tsv`): `W_ij += η·s_i·s_j`. Good
  co-occurrences deepen; the matrix becomes an associative memory of "what healthy looks like together."
- **Descend toward the learned basin:** when perturbed (some axes flip bad), rank candidate corrections by
  which one moves the vector toward the **lowest-energy learned configuration** (`−½ sᵀWs`), i.e. toward a
  coordinated-good state the node has actually visited — not blindly toward each axis's isolated set-point.
- **Test (RED-first):** feed a synthetic history where two axes are always good *together* and one adversarial
  axis is good *alone*; assert the learned `W` pulls recovery toward the coordinated pair, and that with an
  empty/degenerate `W` the optimizer is inert (falls back to today's per-axis behavior — never worse than the
  I-controller it extends). Fail-safe: an unlearned or stale matrix must never *override* a hard invariant fix
  (egress correction still fires), only *order* the discretionary ones.

This is the smallest faithful transfer of the SO loop: reset (each pass) → relax (sample the attractor) →
reinforce (Hebbian on coordinated-good) → later descend toward the learned global optimum.

## Disposition

Filed as a proposal, not landed. It is a real new tier (associative memory of healthy global states) on a
load-bearing regulator, and the correct move per doctrine is to define the state-vector contract, the
persisted `W` artifact, and the RED-first test before code — not to bolt a learning loop onto the egress
controller in one baton turn. Cited to current (2023 enactive bridge + Jan-2025 frontier) sources, concrete,
file-named, and a genuine gap: the mesh regulates each axis but has never learned its own coordinated-good
configurations.
