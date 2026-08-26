# Ambiguity is measured in the wrong direction: a perfectly precise sensor can be perfectly aliased

**Lane:** LITERATURE (live review) · free energy principle & active inference (Friston), angle = **a known critique / failure mode**
**Date:** 2026-08-26 · **Window:** genome@mesh-home
**Arm:** treated (assigned)
**Target organ:** `scripts/mesh-phone-ap` — **assigned by coin at p=0.20**, drawn uniformly from the 565 never-reviewed tools in the lane's denominator. Not chosen by me, not retargeted.
**Status:** implemented + gated, uncommitted in the tree (steward lands)

---

## 1. The critique

Active inference's expected free energy decomposes into **risk** and **ambiguity**, and the ambiguity
term is

> G(π) = D_KL[Q(s|π) ‖ P(s)]  +  **E_Q(s)[ H[ P(o|s) ] ]**

— *"the expected uncertainty of the likelihood mapping, where the expectation is with respect to the
posterior beliefs over states"*
([arXiv:2402.14460, *Reframing the Expected Free Energy: Four Formulations and a Unification*](https://arxiv.org/pdf/2402.14460);
[arXiv:2001.07203, Da Costa, Parr, Sajid, Veselic, Neacsu & Friston, *Active inference on discrete
state-spaces: a synthesis*](https://arxiv.org/abs/2001.07203)).

**That is the forward conditional: states → observations.** It scores how *noisy* an observation is
*given* a state. The failure mode it cannot see lives in the **inverse** direction, H[P(s|o)]: many
distinct world states mapping onto **one** observation. A sensor can score **exactly zero ambiguity**
by the EFE measure — deterministic, repeatable, noise-free — and still be catastrophically
**aliased**, and minimising ambiguity will never find it, because there is nothing noisy to minimise.
"Minimising ambiguity corresponds to choosing future states that generate unambiguous and informative
outcomes" — but only within a likelihood already assumed one-to-one.

**This is an open gap in the live literature, not a solved case.** The people building active
inference agents work around it by bolting on a cognitive map: de Tinguy, Verbelen & Dhoedt build one
precisely for *"challenging scenarios, in which sensory observations provide ambiguous information
about location"* ([arXiv:2308.08307](https://arxiv.org/abs/2308.08307)), extended in
[arXiv:2408.05982](https://arxiv.org/abs/2408.05982) and
[arXiv:2411.08447](https://arxiv.org/abs/2411.08447) for *"complex and aliased environments"*. The
prescribed remedy is never *more precision* — it is a **memory or an observation whose likelihood is
not degenerate**.

**Not already in the corpus.** Twenty-two `fep-*`/`efe-*` reviews, and the closest,
`fep-expected-free-energy-ambiguity-price-of-honest-na-reflex-health` (2026-08-17), takes the EFE
ambiguity term itself — the forward direction — and contains **zero** occurrences of "alias".
`fep-stable-blanket-invariance-across-environments-correlate` took the Markov-blanket critique
(Bruineberg). The inverse direction is new here.

## 2. The assigned organ is that sentence, verbatim

`scripts/mesh-phone-ap` (`reflex-cadence: 7-59/10`) is a **location** sense whose entire observation
is an **SSID** — a name any radio may broadcast — matched by substring:

```python
elif re.search(re.escape(home_pat), ssid):   # -> HOME, and the header reads "→ operator home"
```

The pre-image of *"ssid contains GL-MT3000-765"* holds **at least four** distinct world states:

1. the operator is at home with the phone;
2. the **phone** is at home and the operator is not;
3. the phone is on a **repeater / mesh node** carrying the same name;
4. the phone is on **this very GL-MT3000** — which is a **travel router**, built to be carried away
   and rebroadcast its SSID from a hotel room.

The reading was equally confident in all four, and the EFE ambiguity of the channel is **zero**: the
SSID read is deterministic. Precision was never the problem.

A fifth pre-image, and the one that was actively **wrong**: **Android redacts rather than refuses.**
With the location permission withdrawn, `getConnectionInfo()` still returns `supplicant_state:
COMPLETED` while `ssid` becomes `<unknown ssid>` and `bssid` becomes `02:00:00:00:00:00`. The old
parser saw a non-home SSID and boarded **`AWAY-WIFI`** — a location fabricated out of a permission
failure, and the one verdict an operator would act on.

## 3. What landed

**The disambiguating channel was already in the same JSON, at zero extra cost.**
`termux-wifi-connectioninfo` returns `bssid` alongside `ssid` — the AP's own 48-bit radio identity
([termux/termux-api](https://github.com/termux/termux-api/issues/304), field list: `bssid,
frequency_mhz, ip, link_speed_mbps, mac_address, network_id, rssi, ssid, ssid_hidden,
supplicant_state`). An SSID is a **name**; a BSSID is an **identity**. No extra radio time, no extra
round trip — the observation with the non-degenerate likelihood was arriving all along and being
thrown away.

| state | when | evidence |
|---|---|---|
| `HOME` | home SSID **and** a declared home BSSID | `bssid` — identity |
| `HOME` | home SSID, **nothing declared** | `ssid-only` — *published as many-to-one* |
| `HOME-SSID-ONLY` | home SSID on a radio that is **not** declared | `ssid-contradicted` — repeater / travel router / foreign AP. **Not a location claim** |
| `UNKNOWN-AP` | `<unknown ssid>` / `02:00:00:00:00:00` while COMPLETED | `redacted` — the permission is gone; **n/a, not AWAY** |
| `AWAY-WIFI` / `NO-WIFI` | unchanged | |

Three restraints:

- **No regression and no silent confidence.** Undeclared, the tool still says `HOME` — but publishes
  `evidence=ssid-only` and **prints the observed BSSID**, so ending the degeneracy costs the operator
  one line in `~/.mesh/nodes` (`MESH_HOME_BSSID=…`). A capability at zero adoption must not read as
  absent, so the gap is rendered rather than hidden.
- **The tool does not learn the home BSSID by itself.** Pinning it from a possibly-aliased first
  sighting would cement whichever radio happened to be there — the detector teaching itself its own
  error. Declaration only.
- **Two spellings of one network are one network**: Android's quoted `"SSID"` form is stripped, so it
  cannot become a second identity downstream.

**A layout bug fell out of the same rule, one ring down.** The parser emitted **space**-separated
fields and the shell split on whitespace, so an SSID containing a space (`Cafe Wifi 5G`) shifted
every later field and the *band* was read out of the SSID — an aliasing of the render sitting on top
of the aliasing of the sense. Now TAB-separated with `-` placeholders and `IFS=$'\t' read`.

## 4. The gate, and it was seen to fail

Nine arms in `mesh-phone-ap --test` — six parser, three end-to-end through the real script with a
stubbed `mesh-phone-ip`/`ssh` in a fake `HOME`'s `.local/bin` (so the stubs win the PATH race). Every
arm was mutated:

| arm | mutation | result |
|---|---|---|
| same SSID, other radio → not HOME | ignore the declared BSSID set | RED |
| a declared radio still buys HOME **by identity** (control) | space-separated fields | RED |
| redacted read → `UNKNOWN-AP`, never AWAY | treat the sentinel as an ordinary SSID | RED |
| an ssid-only HOME publishes its degeneracy | emit `bssid` unconditionally | RED |
| a spaced SSID does not shift fields | back to space-separated | RED |
| quoted SSID is the same network | stop stripping quotes | RED |
| e2e: the aliasing reaches the **render** | drop the sentence | RED |
| e2e: `--json` carries `bssid` + `evidence` | rename the key | RED |
| e2e: shell field split | `IFS=' '` | RED |

**One arm was vacuous and is worth recording.** The quoted-SSID arm originally asserted the *state*,
and survived its own mutation — a substring match finds the name inside the quotes either way. It
only became a gate once it asserted the *field*. A gate that cannot fail is not a gate, and the
mutation is the only thing that says which kind you wrote.

## 5. What is NOT claimed

- **No live read.** The phone body has been unreachable since 2026-08-25T19:37Z
  (`~/.mesh/.phone-ap-offline` re-touched every cycle; `--test` exits 2 with the honest n/a). So the
  *actual* home BSSID is unmeasured and `MESH_HOME_BSSID` is deliberately left undeclared — the tool
  will print the value to declare the first time the phone answers. Every arm above is a fixture or a
  stubbed end-to-end run, and none of them is a claim about tonight's radio.
- **A finding I did not fix, named rather than swept:** `~/.mesh/.phone-ap.state` still reads `HOME`,
  written 2026-08-25T19:37Z, five hours into an outage — the state file carries no freshness. Nothing
  reads it today (grepped: `mesh-phone-prox` and `mesh-cell-signal` mention the tool only in
  comments), so it is latent, not live. It belongs to the stale-state class, not to this review.
- **Not the same move as yesterday's Pask review.** Pask's Prune is a collision among *verdicts
  derived the same way*; this is a collision among *world states producing the same observation*, and
  the remedy the literature prescribes is different in kind — a channel with a non-degenerate
  likelihood, not a re-labelling.

## Sources

- Champion, Grześ, Bowman, Bonheme & Bowman (2024). *Reframing the Expected Free Energy: Four Formulations and a Unification.* <https://arxiv.org/pdf/2402.14460>
- Da Costa, Parr, Sajid, Veselic, Neacsu & Friston (2020). *Active inference on discrete state-spaces: a synthesis.* <https://arxiv.org/abs/2001.07203>
- de Tinguy, Verbelen, Dhoedt et al. *Integrating cognitive map learning and active inference for planning in ambiguous environments.* <https://arxiv.org/abs/2308.08307>
- de Tinguy, Verbelen & Dhoedt (2024). *Exploring and Learning Structure: Active Inference Approach in Navigational Agents.* <https://arxiv.org/abs/2408.05982>
- *Learning Dynamic Cognitive Map with Autonomous Navigation* (2024). <https://arxiv.org/abs/2411.08447>
- termux/termux-api — `termux-wifi-connectioninfo` field list. <https://github.com/termux/termux-api/issues/304>
