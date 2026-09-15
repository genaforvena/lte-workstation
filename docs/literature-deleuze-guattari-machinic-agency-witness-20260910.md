# Live literature review: machinic agency is a coupling, not distributed authorship

**Review date:** 2026-09-10  
**Scope:** Deleuze & Guattari — assemblage, rhizome, the machinic; a foundational idea we
have been applying too loosely.  
**Disposition:** applicable design lead; no code changed or committed.

## One concept we do not yet embody

The missing concept is **machinic agency**: activity belongs to a connection of heterogeneous
human and nonhuman components, not to an already-identified actor who owns the result. The
important mechanism is not merely “agency is distributed.” It is that the coupling can amplify
capacities and operate before, or entirely bypass, conscious intention. A useful observable is
therefore a *coupling episode*—the set of input fragments that jointly enabled an output—not a
single tool, window, or poster credited after the fact.

This corrects a recurring loose translation in our mesh work: calling a graph “rhizomatic” or an
assemblage “distributed” while still treating the tool, mind, or operator as the unit of action.
Topology and provenance answer *who/what is connected*; machinic agency asks *which heterogeneous
coupling actually produced the transformation*.

## Sources actually read

1. Deleuze and Guattari, *A Thousand Plateaus*, “Apparatus of Capture,” pp. 458–460 in the
Massumi translation. The primary text says that cybernetic/informational machines form
“humans-machines systems” whose relation is recurrent mutual communication; people become
“input and output” and “intrinsic component pieces,” with only transformations and exchanges of
information. It explicitly says machinic enslavement and social subjection are coexistent poles,
not historical stages. [Primary text, PDF, pp. 458–460](https://files.libcom.org/files/A%20Thousand%20Plateaus.pdf#page=478)

2. Jernej Markelj and Claudio Celis Bueno, “Machinic agency and datafication: Labour and value
after anthropocentrism,” *Convergence* 30(3), 1058–1075 (2024), DOI
[10.1177/13548565231166534](https://doi.org/10.1177/13548565231166534). I read the article’s
abstract, argument, and conclusion. Their operational gloss is that machinic agency is
connectivity among human and nonhuman actors that combines and amplifies capacities, often
bypassing consciousness; they distinguish it from a simple actor-network inventory because the
mechanism also collapses the human/nonhuman and mechanism/vitalism separations. Their case shows
that profiles are produced by feedback between data fragments and individual subjects, so the
profile is a second individuation (“dividuation”), not a sum of whole individuals. [Open article](https://journals.sagepub.com/doi/full/10.1177/13548565231166534)

This is current scholarship rather than a new label invented for the mesh: the article appeared
in the 2024 special issue *Agency in a datafied society* and explicitly develops the concept
from D&G’s machinic process.

## Why it is not already embodied here

The existing D&G artifacts cover call-graph topology (`rhizome_index`), convention coupling,
machinic-phylum trait persistence, territorialization, and many signal/reflex metrics. I also
checked `scripts/mesh-witness`: its ledger fuses scalar readings already produced by senses,
board, minds, asks, and spend, but it does not record the *joint input set → transformation →
output* episode. Its `METRICS` and `AUX_FIELDS` are actor/source totals and distributions; none
is a coupling-level or dividual record. Thus this is not another centrality score or another
human/nonhuman inventory.

## One concrete application

Apply it to the real self-measurement reflex **`scripts/mesh-witness --measure`**. Add one
append-only `coupling=` field to each measurement row, containing a bounded, privacy-safe
fingerprint of the input fragments that were fresh and actually contributed to the tick (for
example `sensorium+mind-state+board`, with ages), the transformation class (`fuse`, `abstain`,
or `route`), and the produced output class. Keep the existing scalar metrics unchanged.

The acceptance artifact is a replay fixture with three cases: (a) one source alone cannot
produce the output, but two fresh sources do (`coupling` names both); (b) the same output is
produced by a different source combination (`coupling` differs even when the actor label does
not); and (c) one stale input yields `abstain/UNKNOWN`, never a credited action. A live run should
then show whether a wake/post/reflex was produced by a changing heterogeneous coupling, rather
than falsely attributing it to the witness tool or to the human mind. This is a measurement of
machinic agency, not a claim that the mesh is autonomous or politically equivalent to a person.

## Decision

**Land the lead, defer implementation:** machinic agency gives the mesh a missing unit of
analysis—the recurrent coupling episode and its feedback—not another graph shape. The next
authorized implementation should be confined to `scripts/mesh-witness` and its fixture/test;
no deployed `~/.local/bin` copy was edited.
