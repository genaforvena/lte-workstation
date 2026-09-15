# Live literature review: autopoiesis → `scripts/mesh-say`

**Arm:** treated (assigned)  
**Target organ/reflex:** `scripts/mesh-say` local voice / `--deliver` reflex  
**Assignment:** randomized re-entry, p=0.20; target fixed by the assignment and not retargeted.

## Review result

The new operational mechanism is **history-dependent structural coupling**: a perturbation does not
merely select an immediate response; it can reorganize the system so that later perturbations are
metabolized differently. In the current literature, Wong et al., *A Biological Learning Theory: How
We Learn in the Era of AI* (2026), explicitly characterizes learning as history-dependent change
that modifies responses to future perturbations and changes the system's structural relation to its
environment ([Springer, DOI 10.1007/s10956-026-10340-6](https://link.springer.com/article/10.1007/s10956-026-10340-6)).
That is a usable control mechanism, not merely the claim that a system is “autopoietic”.

As a second check on the operational reading, Heylighen & Busseniers, *Modeling autopoiesis and
cognition with reaction networks* (2023), describes an autopoietic organization as operationally
closed and self-maintaining, and argues that resilience to perturbation requires compensation—an
action selected for the particular perturbation ([Biosystems 230, 104937](https://doi.org/10.1016/j.biosystems.2023.104937)).
The older review by Razeto-Barry also grounds the Maturana–Varela bridge in selective coupling,
where environmental perturbations are selected and triggered by the unit's own organization
([Biological Research 36, 2003](https://pubmed.ncbi.nlm.nih.gov/12590297/)).

## Novelty check and landed application

Before this change, `mesh-say --deliver` used only instantaneous `OCCUPIED × PROVEN` routing. It
already had audibility fail-safe behavior and a self-speech marker, but it did not retain a failed
local TTS outcome to change the next delivery decision. The landed mechanism is therefore a new
history axis, not a rename of the existing senses:

- a real local TTS engine failure during `--deliver` writes a timestamp to
  `$HOME/.mesh/mesh-say-coupling` (overrideable with `MESH_SAY_COUPLING_FILE`);
- for 300 seconds, a later `OCCUPIED + PROVEN` event is rerouted through `mesh-voice-tx` and reports
  `coupling=quarantined`, avoiding repeated expenditure on the recently failed voice path;
- a later proven local delivery clears the marker; expired or unreadable state is treated as no
  memory, and ambient non-`--deliver` speech is unchanged.

This is deliberately bounded and reversible: it changes one reflex's response history, never the
global routing substrate. The implementation and behavior assertions are in
`scripts/mesh-say`; the test proves both quarantine and release after expiry.

## Verification

```text
bash -n scripts/mesh-say
scripts/mesh-say --test
smoke-test: ok (... history-dependent coupling quarantine/release ...)
```

The randomized target was `scripts/mesh-say`; no alternate organ was substituted.
