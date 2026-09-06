# senses — the sensorium

goal: держать сенсориум честным: каждый датчик отдаёт живой артефакт либо признаётся слепым

Engine: codex (gpt-5.6-luna). This window owns the perception lane: the sensors themselves, their `--test`
gates, and the fused state derived from them.

**Perception is re-observed live, never stored** — it decays on reboot by design.

**Honest fusion:** an unreachable input renders UNKNOWN/partial, never a faked all-clear. A
reachable organ whose driver returns empty is a HOLLOW sense — cron-green while its artifact goes
stale — so a sensor's `--test` must assert a real hardware read, not just the offline classifier.

Its data pane carries fused perception (`mesh-dash sense`); if this window keeps re-running the
same probe every turn, that signal belongs on top.

## A sense is a RELATION between axes, not a read of one (operator 2026-08-30)

Operator's correction to this window's goal: *«чувства должны быть не столько от сырого чтения
одного параметра, а через корреляцию нескольких, мб разнородных»*. So a new sense is not earned by
adding another single-parameter reader — it is earned by a RELATION across several axes, preferably
heterogeneous ones (a radio counter against an acoustic one, a thermal one against a scheduler one).

Three things this does NOT mean, each measured on this mesh:

- **Correlation is REDUNDANCY, and redundancy is the case for DELETING an axis, not for minting a
  sense.** Two axes that track each other are the same sense read twice; what earns a fused verdict
  is a JOINT pattern — a state the pair reaches that neither axis reaches alone.
- **A `max()`/worst-of fold does not connect axes, it selects one.** The macro verdict then EQUALS
  one of its parts at every instant, so it can carry no information its parts do not
  (`scripts/mesh-situation` says this of its own fold). Adding axes under a selector adds nothing.
- **Instrument before semantics.** Measure on the live corpus whether a candidate pair carries joint
  information at all, and only then change a verdict a human reads.

Every correlation-derived sense publishes its own COVERAGE the same way a single-axis one does: a
pair is measurable only where BOTH axes were live, so the denominator is the overlap, never the
window — and on a node that power-cycles, a silence in either tape is a power-off, not a calm.
