# Live literature review: rhizomatic deterritorialization → self-triggered sensing

**Review date:** 2026-09-10  
**Scope:** Deleuze & Guattari — assemblage, rhizome, machinic; cross-domain transfer to the
distributed sensor mesh.  
**Disposition:** applicable design lead; no code landed in this review.

## One new mechanism

The mechanism is **event-/self-triggered sensing with a local state estimator over a switching
topology**. An agent does not sample and communicate at one globally fixed period. It predicts the
state between contacts and emits when local error or uncertainty crosses a trigger; the graph may
also change, so the next useful coupling is discovered rather than prescribed.

I read Li, Chen, and Zhao, “Dual-channel event-triggered consensus of multi-agent systems under
DoS attacks over switching topologies,” *Complex Engineering Systems* 5 (2025), DOI
[10.20517/ces.2024.104](https://doi.org/10.20517/ces.2024.104), published 28 March 2025. The
paper's abstract and introduction describe: an estimator to avoid continuous communication,
event-triggered rather than fixed-period updates, separate communication and actuator triggers,
and distributed control under switching topologies and denial-of-service conditions. The paper
also explicitly identifies fixed-period sampling as resource-saving but inflexible, and validates
the design in simulation. This is a control result, not a philosophical claim; the transfer below
is my engineering inference.

For the D&G side I checked the rhizome/assemblage account in the [*A Thousand Plateaus* “Rhizome”
extract](https://warwick.ac.uk/fac/arts/english/currentstudents/postgraduate/masters/modules/worldlitworldsystems/dg-rhizome-norton-anthology.pdf)
and the recent organization scholarship chapter [“Assembling an Analytical Apparatus: CCO
Encounters Deleuzian New Materialism” (Oxford Academic)](https://academic.oup.com/policy-press-scholarship-online/book/59190/chapter-abstract/497525277),
which connects assemblage, machinic practices, dispersed agency, and rhizomatic rather than
arborescent organization.

## Why this is not already embodied here

The existing sensor organ is explicitly periodic: [`scripts/mesh-sensor-log`](../scripts/mesh-sensor-log)
declares `reflex-cadence: 3-59/5 * * * *` and collects the phone, Wi-Fi, thermal, BLE, and other
readings on each run. [`scripts/mesh-sensor-tape`](../scripts/mesh-sensor-tape) likewise declares
`*/10` and samples the latest state of every enrolled sense. Its room reflex already has hysteresis
and dwell, but those decide whether a **verdict** is emitted after samples; they do not decide when
the next sensor sample or phone contact should occur. The existing D&G work and the 2026-09-09
delta-CRDT review therefore do not cover this mechanism: this is a missing **sampling policy**, not
another merge or topology vocabulary.

## D&G → mesh translation

Treat the sensor/reflex coupling as a machinic assemblage whose territory is provisional. A quiet
room does not need to be re-established by an identical five-minute ritual; the local estimator
holds the current room hypothesis, while a new Wi-Fi fingerprint, light jump, step burst, or
phone-link change is a **line of flight** that deterritorializes that local territory and demands a
fresh coupling. Sustained low innovation reterritorializes it, but only temporarily and with a
hard freshness bound. The rhizomatic property is operational: any enrolled sense may become the
triggering edge, and no central sampler owns the whole map.

## One concrete application

Apply it to the real organ/reflex **`scripts/mesh-sensor-log --edge`**:

1. Keep the existing cron wake as a cheap watchdog, but add a per-sense next-due state for the
   phone/Wi-Fi room bundle. Maintain a tiny local estimate (dominant AP, RSSI drift, light, steps,
   and last successful phone contact).
2. At a wake, read the cheap local signals first. If innovation and estimator uncertainty are below
   threshold, extend that bundle's next contact up to a bounded maximum. If an AP changes, RSSI
   crosses a calibrated band, steps/light jump, or uncertainty ages, trigger the expensive phone
   read immediately and reset to the short interval.
3. Always write an unconditional run/health row and publish `UNKNOWN` when a deferred or failed
   contact cannot support a state. The adaptive interval must never turn silence into `SAME_ROOM`.
   Preserve the current dwell/hysteresis before posting `[room-moved]`.

The first measurable acceptance artifact should be a fixture replay of a quiet → movement → quiet
trace showing: fewer phone reads during quiet periods, a bounded detection delay after the movement
edge, no false move on a one-sample spike, and an explicit `UNKNOWN` on a missing phone contact.
This is a proposal only; implementation and wiring are intentionally deferred to a separate task.

## Decision

**Land the design lead:** self-triggered estimator-backed sampling is a genuinely absent mechanism
that gives the mesh a concrete machinic/rhizomatic behavior—local couplings form and dissolve in
response to events—while respecting its existing evidence rules. No deployed copy or `scripts/`
source was edited; this review artifact is the only change.
