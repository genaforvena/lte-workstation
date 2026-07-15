# sound pane: records ledger + reflexive grind — design

*2026-07-15. Operator ask: "make sure your top pane holds our invariants: liveness-as-lease,
reflexes on change of the pane, conditional nudge to the mind. feed all records that mesh makes
here so that you could be deciding what to do with them with grainneukeln. transformations should
be mostly reflexive, yet make sure not trivial or boring."*

## The three gaps

1. **No lease.** The sound pane prints `RENDERS: last params` with no age. A dead grinder and a
   quiet one render identically. Doctrine (`docs/epistemics.md`) says status is a lease, not a
   stored flag — the pane violates it.
2. **The records expire before the mind sees them.** `mesh-soundscape` owns the ear and keeps only
   its own winning clip (`SS_KEEP_DAYS=2`); `~/.mesh/audio-buffer/` (the overhear ear, ~20 wavs)
   self-prunes within the hour. Every other record the mesh makes is transient. The mind never gets
   to decide about them — they're gone.
3. **The grind is blind to its source.** `mesh-room-music`'s `pick_args` rotates `f`/`s`/`ss` away
   from the last 3 remixes — real, but shallow: random-within-absent, and `w`/`c` never rotate. The
   soundscape analyzer *measures* `dyn/act/rich/tone/move/cent` and then throws them away; only
   `beats` survives, as a gate. Params never answer to what was actually recorded. That is the
   "trivial and boring" the operator means.

## Units

Three units + two surgical extensions to existing tools. Reuse over rebuild: `mesh-soundscape`
keeps owning the ear/measure tract, `mesh-room-music` keeps owning the grind invocation (heavy-run
admission, hollow gate, fresh gate, params logging).

### 1. `mesh-soundscape --measure <wav>` (extension, ~20 lines)

Exposes the existing librosa `analyze()` on an arbitrary file and prints the raw axes, which
`--scan` currently discards:

```
MEASURE off=12.00 dur=3.00 score=51.3 label=dynamic·dark·tonal beats=7 dyn=0.62 act=0.31 rich=0.44 tone=0.88 move=0.19 cent=1180 rms=0.0121
```

`--scan`'s `WINNER` line is untouched — its caller does `read -r _tag off dur score label beats`,
where the last var absorbs the line's remainder, so appending fields there would silently corrupt
`beats`. A separate mode, not a wider line.

### 2. `mesh-records` — the archivist reflex

Sweeps every record-producing organ and archives what's new before it prunes:

| organ | source | why |
|---|---|---|
| `ear` | `~/.mesh/audio-buffer/*.wav` | the continuous room ear; self-prunes hourly |
| `scape` | `~/.mesh/soundscapes/*.wav` | soundscape's scored keeps; prunes at 2d |
| `drop` | `~/.mesh/inbox/*.{aac,oga,m4a,wav,mp3}` | operator jams — always outrank the ear |
| `voice` | `~/.mesh/voiceref/*.wav` | reference captures |

For each new file: measure it (`--measure`), copy to `~/.mesh/records/<ts>-<organ>-<hash8>.wav`,
append one line to `~/.mesh/records.log` (the ledger — the durable index that outlives the audio).

- **Dedupe by content hash**, so a re-sweep never re-archives and a rolling-buffer file that
  survives two sweeps lands once.
- **Corpus cap** `MESH_REC_MAX_MB` (default 2000) / `MESH_REC_KEEP_DAYS` (default 14), evicting
  oldest-lowest-score first. Operator drops are never evicted.
- **Liveness-touch** on every successful sweep (`mesh-state-touch`), so a long-quiet-but-live
  archivist never reads as STALE.
- `--test` gates on a **real measurement of a real wav** (duration + beats out), per the
  hollow-sense rule. Env absent → exit 2 (honest n/a), never a fake green.

Ledger line:

```
2026-07-15T01:40Z ear 4f2a9c11 dur=18.0 score=51 beats=7 [dynamic·dark·tonal] dyn=.62 act=.31 rich=.44 tone=.88 move=.19 -> pending
```

The `-> ` verdict field is the grinder's: `pending` | `ground:<mix>` | `held:<why>` | `skip:<why>`.

### 3. `mesh-sound-reflex` — grinder + conditional nudge

Modeled on `mesh-room-reflex`, **including its scar**: change detection anchors on the SHA of the
last consumed *line*, never a byte offset. `records.log` gets tail-pruned exactly like the room
transcript did; byte offsets against a shrinking file resync to zero and replay the whole buffer as
fresh — that is the 2026-07-14 false-wake storm, and it must not be re-bought here. Anchor gone
(genuinely pruned) → resync to END, never replay.

On new ledger lines:

1. **Pick** the best candidate — an `inbox` drop always outranks the ear, else highest score with
   `beats >= MIN_BEATS` (the automixer is beat-driven; a beatless window grinds to an empty mp3).
2. **Derive** the recipe from that record's measured character (below).
3. **Novelty-gate** it against `room-music-params.log`.
4. **Render** in background, detached + timeout-bounded (the grind is O(n²) — never block a cron),
   via `mesh-room-music --remix` with the derived params pinned.
5. **Nudge** only on the notable.

#### Derivation — the source shapes the recipe

Each axis maps to the param it actually governs, so a busy source and a sparse one cannot come out
the same:

| measured | → param | rationale |
|---|---|---|
| `act` high (busy) | `f` small (0.2/0.33) → micro-grain | dense material wants short grains; long ones just blur it |
| `act` low (sparse) | `f` large (2/3) → long grain | stretch the empty; make the sparse into texture |
| `dyn` high | `s` slow (0.25/0.5) | let the swells breathe |
| `dyn` low (even) | `s` fast (1.5–3.0) | even material needs the rhythm axis to supply the motion |
| `tone` tonal | `ss` far from 1.0 | pitch-smear is audible and interesting on tonal material |
| `tone` noisy | `ss` near 1.0 | smearing noise is mud |
| `cent` dark | `c` opens the top | give it air it doesn't have |
| `cent` bright | `c` carves low/narrow | find the body under the hiss |
| `move` high | `w` larger (denser window) | movement rewards density |

`l = beat_ms × f`, clamped 120–2000 — the existing grainneukeln contract.

#### The novelty gate — taste memory as repulsor

The derived recipe is a point in normalized param space (`f`,`s`,`ss`,`w`,`c`). The gate rejects any
candidate whose **normalized L1 distance to every one of the last N recipes** is below `epsilon`. On
rejection it perturbs along the axis with the most unvisited room and retries, up to K times. If no
novel recipe survives, it does **not** render — it nudges the mind that the param space is walked
out. This is strictly stronger than `pick_args`'s value-absence rotation: it constrains the *combo*,
not each axis independently, and it covers `w`/`c` which never rotated.

Pure function → fully testable with no audio.

#### The nudge gate

Cooldown-gated, like `mesh-room-reflex`. Fires only on judgement-shaped events:

- `drop` — an operator jam landed in `inbox/` (always; that's a gesture, and gestures outrank).
- `walked-out` — the novelty gate found no novel recipe.
- `outlier` — a record scoring far above the corpus mean.
- `degenerate` — a render came back hollow/empty despite passing the beat gate.

Everything else renders and logs silently. With a continuous ear, poking per render would burn a
paid turn per record.

### 4. `mesh-dash sound` — the pane

```
-- LEASES --                          (each line: age + TTL verdict; expired = UNKNOWN, never a stale value shown as current)
  ear        LIVE   4s      audio-buffer advancing
  archivist  LIVE   1m      mesh-records
  grinder    STALE  2h      mesh-sound-reflex ← lease expired
  render     IDLE   —       no grind running
-- INBOX --      operator drops (outrank the ear)
-- RECORDS --    newest ledger entries: score·beats·character·organ -> verdict
-- RENDERS --    last params + novelty room left
-- REPO --       grainneukeln
-- NOTABLE --    what the grinder wants judgement on
```

Each lease has an explicit TTL derived from the producer's cadence. Unreadable → UNKNOWN, per the
honest-fusion rule: an absent input never renders as an all-clear.

The pane's own frozen-render case is already covered by `mesh-pane-watch` (hashes each channel's
data pane every 5m, liveness-lease part 3). Not rebuilt here.

### 5. `mesh-room-music`: `MESH_RMC_META` (extension, 1 line)

When `MESH_RMC_AUTOMIX` is pinned, `META` is empty and the params-log line loses its provenance.
`MESH_RMC_META` lets the caller append `~ src=… score=…` while `mesh-room-music` remains the single
writer of `room-music-params.log`.

Note: `--diversity` treats a pinned `MESH_RMC_AUTOMIX` as the likely cause of MONOTONE. The reflex
pins *per-invocation with derived, novelty-gated params*, so diversity rises rather than falls — but
the comment there is updated so a future reader doesn't misdiagnose.

## Cadence

- `mesh-records` — `*/2 * * * *` (must beat the audio-buffer's prune).
- `mesh-sound-reflex` — `*/5 * * * *` (edge-triggered on ledger change; renders are bg).

Both self-wire via `# reflex-cadence:` + `mesh-autowire` after a passing `--test`.

## Privacy

Operator's explicit call (2026-07-15): room audio grinds like any other source — "grind it, it's
granular anyway". Records stay node-local; nothing here ships audio off-node. The nightly TG send
remains `mesh-room-music --nightly`'s existing behavior, unchanged by this work.

## Out of scope

Note 3 body/senses (mission says so). The `mesh-soundscape` mix lane keeps working as-is; this adds
a second, character-driven lane over the archived corpus rather than replacing it.
