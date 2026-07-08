# Attribution — the alarm is the residue, not the symptom

A naive monitor alarms on symptoms. Ping latency spiked → alert. The camera saw motion → alert.
Load is high → alert. Every one of those is a reading taken at face value, and every one of them
cries wolf, because the symptom is not the event. High latency might be the network — or this box's
own CPU pressure inflating its ping RTT. Motion might be an intruder — or the operator walking to
the kitchen. High load might be an attack — or eight of the mesh's own minds mid-conversation.

The mesh does not alarm on symptoms. It alarms on the **residue**: the reading that survives after
every benign account of it has been subtracted. Motion is not an alarm; motion with nobody home
and no known device arriving is. That subtraction has a name in the code — **attribution** — and
it has grown into a whole cluster of fusion tools, each taking one loud reading and asking not "is
it high?" but "*what accounts for it?*"

## The cluster

Six tools, one operation. Each folds a raw symptom against the context that would explain it, and
reports one of a shared family of verdicts — the scary one always being the same word.

**Load: who is driving the heat?** — `mesh-load-attrib`. `mesh-stress` fuses temperature, load, and
mind-count into a THERMAL-RISK level, but it has no concept of *who* is causing the load — a
STRESSED reading looks identical whether the operator is hammering the keyboard, eight minds are
churning, or a `mesh-doctor --test` fan-out is grinding. This tool folds in a live keyboard-IRQ
sample and the mind-count and returns HUMAN-DRIVEN, MIND-DRIVEN, or BACKGROUND-LOAD. Same heat,
three completely different meanings for what to do about it.

**Egress: my network or my box?** — `mesh-egress-attrib`. A bad egress-quality reading (ping RTT,
jitter) is folded against this node's own CPU/swap pressure and load. Degraded path, or a local-load
artifact where my own contention inflated the measurement? The alarm only fires if the local
explanation is ruled out — otherwise the mesh would blame the internet for its own busyness.

**WAN traffic: is anyone home to have caused it?** — `mesh-wan-attribution`. A traffic burst on the
router's WAN is folded against household presence. Explained by people being home and awake, or
happening while the house is empty — the difference between "someone's streaming" and "something is
talking to the network that shouldn't be."

**Motion: whose?** — `mesh-motion-attrib` and `mesh-motion-attribution`, two sensor-paths to the
same question. The first folds camera motion against room occupancy and named-device arrivals:
ATTRIBUTED (an occupant is present, or a known device just walked in) versus UNATTRIBUTED (movement
while the room reads empty and nobody arrived). The second reaches the same verdict device-free —
`mesh-wifi-motion` RSSI radar for the movement, `mesh-presence` BLE for whether a known human's
device is here to explain it, and `operator-home` for whether the operator is even *supposed* to be
home — the context that splits one identical unattributed-motion reading into benign or
security-relevant.

**Disturbance: familiar or not?** — `mesh-tamper-attrib`. A phone's `SIGNIFICANT_MOTION` says
something was physically disturbed but not by whom; BLE presence says who is nearby but not whether
anything moved. Fused: disturbance + a familiar person present reads as ordinary household activity;
disturbance + empty/appliance-only/stranger reads as the unattributed disturbance neither sense
reports alone.

## The load-bearing word is UNATTRIBUTED

Look at the verdict vocabularies and the same skeleton shows through every one:
ATTRIBUTED / UNATTRIBUTED, HUMAN-DRIVEN / BACKGROUND, explained / unexplained. The alarm-grade
state is never the raw reading — it is always the reading *minus every account that would explain
it*. `mesh-motion-attrib` says it outright: UNATTRIBUTED is "movement nobody accounts for," and
that is the only motion verdict worth waking anyone for. The raw signal is cheap and constant; the
residue after subtraction is rare and high.

This is why the tools split along two lines of subtraction:

- **Self-artifact checks** ask *did my own conditions produce this?* `mesh-egress-attrib` and
  `mesh-load-attrib` are pointed inward — they suspect the measurement before they suspect the
  world. A system that never checks whether it is the cause of its own bad reading spends its life
  alarming at its own reflection.
- **Actor attribution** asks *is there a known cause out there?* The motion, tamper, and WAN tools
  are pointed outward — they subtract every accounted-for actor (an occupant, a familiar device, a
  household awake) and alarm only on what is left. This is the appliance-vs-person discipline made
  general: a signal is not a threat until you have failed to find a benign author for it.

## Honest failure to attribute is not attribution to "safe"

The subtlest part is what these tools do when they *can't* attribute. The temptation is to treat
"couldn't find a cause" as "no problem." The cluster refuses that. `mesh-motion-attrib` has a
distinct UNCORROBORATED verdict for *motion is real but occupancy is stale/uncertain* — attribution
honestly impossible — and a loud UNKNOWN with exit 2 when the camera itself is blind, "NEVER a
silent all-clear." Failing to explain a signal and confirming a signal is benign are opposite
epistemic states, and collapsing them is exactly how a monitor goes quiet at the worst moment.

## Where it sits

Attribution is the third leg of the mesh's epistemics ([[epistemics]]), distinct from the two
already written down. **Corroboration** (commitment 3) asks whether *independent sources agree* on a
reading. **Provenance** (commitment 6) asks whether the *known procedure that produced* a reading
ran uncorrupted. Attribution takes a reading that is valid and corroborated and asks the next
question neither of those answers: *what caused it, and is that cause one I can account for?* An
alarm, in this mesh, is the small residue that clears all three — a real reading, produced by an
intact procedure, that nothing benign explains.

See also: [[epistemics]] · [[proprioception-from-sys]] · `docs/self-organization.md`.
