# Green Lies — continuation manuscript draft

This is a continuation draft anchored to `docs/paper/green-lies-taxonomy.md`; it is not a
replacement manuscript and is not submission-ready.

## Proposed abstract

Autonomous systems depend on code that observes and repairs the system that runs it. We study a
failure mode in which that observation layer continues to emit a fresh, plausible green result
after the property under observation is absent, unexecuted, or outside the candidate set. From a
continuously operated multi-node agent mesh we derive ten recurring classes, document live cases,
and implement three decision-procedure detectors. The measured results are class-dependent: a
self-source-grepping defect appears in three of twenty decidable gates in the studied system and
in none of 1,296 bounded comparison files, while silent fallbacks occur in both populations with
a different exposure pattern. Interval-under-cadence analysis finds both under-covered samples
and honest coverage reporting. These results do not show that agent-written software is generally
worse; they show that “green self-observation failure” is not one mechanism and that detector
denominators, undecidable buckets, and failed controls are part of the result.

## Contribution statement

The paper contributes (i) a case-grounded vocabulary for green self-observation failures, (ii)
three mechanically exercised detectors with explicit decision procedures, (iii) bounded measured
comparisons that disagree across classes, and (iv) a reproducibility discipline that retains
blocked and failed arms rather than converting them into reassuring zeros.

## Results and limitation bridge

The main result is not the largest rate in any one table. It is the disagreement between tables.
C1 is structurally enabled by in-file self-testing and is absent from the bounded external corpus;
C2 is present in both populations, with public shell showing higher per-site exposure while the
studied mesh supplies far more opportunities and a documented all-clear asymmetry; C3 finds that
some tools publish a sample as a state while others publish coverage or span the interval with an
accumulator. A single “agent systems lie more” statistic would erase these distinctions.

The evidence also limits the paper. C4–C10 are documented taxonomy classes, not seven completed
detectors. The authorship comparison is confounded by test architecture and corpus composition.
The tiny-fleet expansion bundle is explicitly a blocked pilot: duplicate leakage remains, genuine
fine-tuning is unavailable, behavioural evidence is absent, and one measured repository cannot
support a cross-repository architecture claim. Those failures remain visible because hiding them
would reproduce the paper's subject matter.

## Closing paragraph for the eventual manuscript

The practical conclusion is modest: a green result is an observation claim, not an observation.
To trust it, the system must expose what was actually read, how much of the intended interval was
covered, which candidates were enumerated, whether the check executed the subject, and which arms
were unavailable. The taxonomy is useful precisely where it remains incomplete: it turns a vague
fear that self-monitoring may lie into failure classes that can be falsified by a real artifact.
