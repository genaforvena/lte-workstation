# Live literature review — higher-order adaptive contagion and the missing activity scale

**Date:** 2026-09-10  
**Area:** complex adaptive systems / edge of chaos (Santa Fe lineage)  
**Angle:** an operational adaptation mechanism, not a claim that “the edge” is one universal
number  
**Status:** literature artifact only; no mesh tool changed and no commit made.

## One concept we do not yet embody

**Characteristic-scale adaptation on a higher-order network.** Burgio, St-Onge, and
Hébert-Dufresne (Nature Communications, 2025) model contagion on adaptive hypergraphs rather
than only pairwise edges. The mechanism is to classify a group by its activity level `i` (how many
members are currently active/contagious), then choose an adaptation scale `ī` that best separates
groups worth avoiding from groups that are not yet contagious. This creates two distinct control
strategies:

1. target the dynamics — leave groups once activity reaches the contagion threshold `ν`;
2. target the structure — when adaptation is slow or inaccurate, leave unusually large groups to
   reduce exposure and degree.

The important CAS result is the interaction: the best policy depends jointly on group activity,
rewiring speed `γ`, and decision accuracy `η`. The paper finds a low-accuracy region where
rewiring is harmful, and a slow-rewiring region where prevalence first increases with `γ` before
decreasing. Thus adaptation itself has a **least-optimal rate**; “more responsive” is not
monotonically safer. That is an implementable edge-of-chaos lesson: preserve a measured relation
between activity scale, adaptation lag, and the topology being changed, instead of turning one
global threshold up until the system looks quiet.

## Why this is genuinely absent here

The existing mesh has pairwise/graph mechanisms and several scalar criticality lenses, but no
hyperedge/group representation or characteristic activity scale:

- `scripts/mesh-dispatch` counts backlog, owner/task exposure, and idle age, then applies a
  density-adaptive **evaporation** threshold. It does not distinguish a task exposed through one
  overloaded group from the same number of exposures distributed across independent groups.
- `scripts/mesh-closure` measures graph closure and degree-preserving rewiring nulls. That is a
  static pairwise topology diagnostic, not adaptive membership driven by group activity.
- The criticality reviews cover rates, margins, avalanches, and topology, but none implement the
  paper's `ī` choice or its interaction with adaptation rate and accuracy.

This is not a relabeling of the existing congestion knee: the proposed state is the **joint
distribution of exposure across groups**, and the action changes membership/route choice. A single
backlog scalar cannot recover it.

## One concrete application

**Target organ/reflex:** `scripts/mesh-dispatch`.

Add a read-only `--group-adaptation` sidecar first. Define a task's transient exposure groups from
the identities already present in the board line (owner/window, room/channel, and claim/parent
identity); do not infer group identity from free text. For each open task, publish:

```text
task=<explicit-id> groups=<n> active_groups=<n> max_group_activity=<i>
scale=<i-bar|unknown> lag=<seconds> accuracy=<resolved|unknown>
policy=<avoid-contagious-group|avoid-large-group|hold> evidence=<n>
```

Use the paper's operational split:

- when activity observations are timely and accurate, `ī=ν`: route a task away from a group once
  that group is demonstrably active;
- when observations are delayed/uncertain, `ī≈mean(group size)`: prefer the less-connected group,
  reducing exposure without pretending that a stale activity read is current;
- in the measured intermediate/least-optimal region, `hold`: do not rewire on every tick. Keep the
  existing route and emit the lag/accuracy evidence so the adaptation rate can be audited.

The sidecar must remain advisory until a live tape shows which regime the mesh occupies. The first
falsifiable fixture is three tasks with ten exposures each: all ten in one group, one per ten
groups, and a delayed/incorrect group read. A pairwise backlog count sees a tie; the higher-order
sidecar must separate them and must choose `hold` when the activity signal is stale. If the board
does not contain stable group identities or has too few repeated group memberships, the correct
result is `INSUFFICIENT`, and this application should be discarded rather than inventing groups.

## Sources actually read live

- Giulio Burgio, Guillaume St-Onge, and Laurent Hébert-Dufresne, **“Characteristic scales and
  adaptation in higher-order contagions,”** *Nature Communications* 16, 4589 (2025). The abstract,
  introduction, adaptive-hypergraph results, and discussion were read. The paper introduces
  generalized approximate master equations, identifies the characteristic group-activity scale,
  and reports the two strategies plus the harmful/least-optimal rewiring regions:
  <https://www.nature.com/articles/s41467-025-59777-0>
- As a current edge-of-chaos counterpoint, **“Taming the chaos gently: a predictive alignment
  learning rule in recurrent neural networks,”** *Nature Communications* (2025), was read for its
  operational distinction between rich-but-structured representations and excessive dispersion.
  It reinforces the review's restraint: an edge claim needs a task-linked observable, not a scalar
  label:
  <https://www.nature.com/articles/s41467-025-61309-9>

## Verification / handoff

- Repository gap check: `rg` over `scripts/` and `docs/` found no hypergraph, characteristic-scale
  `ī`, or group-activity/rewiring-rate mechanism in `mesh-dispatch` or `mesh-closure`.
- Artifact: this file.
- Tool edits: none.
- Tests: no executable code changed; no test claimed.
- Git: intentionally uncommitted, per operator instruction.
