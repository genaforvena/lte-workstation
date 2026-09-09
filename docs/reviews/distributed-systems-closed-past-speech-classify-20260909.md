# Live literature review — closed past is not eventual consistency

**Area:** distributed-systems coordination — gossip, CRDTs, eventual consistency  
**Date:** 2026-09-09  
**Organ:** `scripts/mesh-speech-classify`  
**Arm:** treated (assigned)  
**Status:** review artifact, uncommitted

## Finding

The concept we do not embody is **closed past**: a replica's accepted view must include the
causal past of what it is showing or acting on. This is narrower and more operational than saying
that replicas “eventually converge.” A result can be destined to converge and still be unsafe to
consume now if an earlier observation on which it depends is missing.

The live source is Paulo Sérgio Almeida, *A Framework for Consistency Models in Distributed
Systems* (arXiv:2411.16355, 25 Nov 2024):
<https://arxiv.org/abs/2411.16355>. The paper names closed past, local visibility, and monotonic
visibility as separate axioms; treats convergence and arbitration as **safety** properties; and
warns that “eventual consistency” conflates safety with liveness. Its CLAM theorem states that a
wait-free asynchronous implementation cannot generally have closed past, local visibility,
arbitration, and monotonic visibility all at once. The practical lesson is to expose the chosen
trade-off instead of using “eventual” as a broad freshness/correctness claim.

I checked the mechanism against the original delta-CRDT treatment. Almeida, Shoker, and Baquero,
*Efficient State-based CRDTs by Delta-Mutation* (arXiv:1410.2803, 2014),
<https://arxiv.org/abs/1410.2803>, says that shipping individual deltas does **not** automatically
preserve causal consistency: deltas must be sent as causal intervals and joined only when the
receiver subsumes the state containing the interval's first delta. Its anti-entropy algorithm
also makes the per-replica counter durable, because a crash followed by a delayed acknowledgement
can otherwise make a replica skip deltas. That is the concrete mechanism behind the abstract
closed-past warning.

The older anti-entropy architecture supplies the control: Richard Golding, *A Weak-Consistency
Architecture for Distributed Information Services* (USENIX, 1992), pp. 387–390,
<https://www.usenix.org/publications/compsystems/1992/fall_golding.pdf>, exchanges timestamp
summaries before exchanging missing log entries and keeps those summaries on stable storage. The
summary is evidence for what history the receiver has incorporated. A short USENIX primer makes
the related distinction plainly: causal consistency is easier to reason about than the broad
“eventual” label,
<https://www.usenix.org/publications/login/august-2013-volume-38-number-4/short-primer-causal-consistency>.

## Why this is a real gap here

`scripts/mesh-speech-classify` emits a class and band RMS values for a capture, but its JSON has no
capture sequence, predecessor, source digest, or causal-frontier field. The live classifier is
therefore a point observation, not a causally closed stream. Its `--source` mode can classify an
arbitrarily supplied WAV, and the live path can return a result without evidence that the
preceding capture was observed or that a delayed result belongs after the current one.

This is not the already-landed causal-stability frontier in `mesh-chat-sync`, nor the causal
delivery/orphan split in `mesh-promises`: those protect the board's replicated log. This target
has neither a per-capture frontier nor a rule that a consumer must hold an out-of-order speech
result. Existing `UNKNOWN` in the classifier only covers missing RMS/audio failure; it does not
mean “causal predecessor absent.” Thus the mesh has applied eventual delivery too loosely if a
downstream reflex interprets a late speech label as the current acoustic state.

## One concrete application

Apply closed-past admission to the live capture branch of **`scripts/mesh-speech-classify`**:

1. Assign each live capture a durable per-device `capture_seq`, include `source_sha256`, and carry
   `prev_seq` (or an equivalent compact frontier) in the JSON result.
2. A consumer accepts a result as current only when its predecessor is present; a gap or a result
   arriving after a newer sequence is held as `PENDING/UNKNOWN`, never silently treated as the
   current `SPEECH`, `SILENCE`, or `NO_AUDIO` state.
3. Keep `--source` fixture analysis free of the live admission rule, but make the test exercise a
   one-step gap and assert that the gap cannot produce an actionable speech verdict.

This is one bounded transfer: it does not replace the board with a CRDT and does not claim that
audio classifications themselves commute. It makes the missing liveness/safety boundary visible
at the organ that currently produces the observation. Implementation is deferred to a separate
authorized code task; this review intentionally lands the finding and application only.

## Verification

- Read the current target source: no sequence, predecessor, digest, or causal-frontier fields.
- `scripts/mesh-speech-classify --test` — PASS: dependencies present and a synthesized 1 kHz tone
  classified as `SPEECH`.
- Repository scan checked the existing distributed-systems reviews and target consumers; closed
  past as a distinct admission rule is not already embodied on this organ.

## Sources

1. Paulo Sérgio Almeida, “A Framework for Consistency Models in Distributed Systems,” arXiv:2411.16355, 2024. <https://arxiv.org/abs/2411.16355>
2. Paulo Sérgio Almeida, Ali Shoker, Carlos Baquero, “Efficient State-based CRDTs by Delta-Mutation,” arXiv:1410.2803, 2014. <https://arxiv.org/abs/1410.2803>
3. Richard A. Golding, “A Weak-Consistency Architecture for Distributed Information Services,” USENIX, 1992. <https://www.usenix.org/publications/compsystems/1992/fall_golding.pdf>
4. Wyatt Lloyd, Michael J. Freedman, Michael Kaminsky, David G. Andersen, “A Short Primer on Causal Consistency,” USENIX ;login:, 2013. <https://www.usenix.org/publications/login/august-2013-volume-38-number-4/short-primer-causal-consistency>
