# STUDY (write-ahead log) — configurable logging levels for the injection WAL

**Landed:** `scripts/mesh-tell` (`MESH_TELL_WAL_LEVEL`) + `nodes.example` · 2026-08-15 · genome mind
**Task:** "Implement a configuration to set custom logging levels for write-ahead log in our agent
mesh nodes."

## Where the WAL is

The mesh has one write-ahead log: `mesh-tell`'s injection journal (`~/.mesh/tell-wal.log`, STUDY
write-ahead log 2026-07-20). Every send appends an `intent` record **before** any guard runs or any
key is pressed, and the outcome (`sent`/`refused`) after — so a crash mid-send leaves a dangling
intent that `--replay` renders `UNRESOLVED`. Fields are tab-separated:
`ts · pid · phase · who · node · win · b64(prompt)`.

Live on this node before the change: **2056 lines, 1.56 MB** — an average of ~770 bytes per line,
i.e. the log is almost entirely verbatim prompt text. It retains 4000 lines before trimming to 2000.
Everything a mind is handed goes through it: operator instructions, paths, pasted material.

## What was added

`MESH_TELL_WAL_LEVEL`, read from the environment or from `~/.mesh/nodes` (env wins), default `full`:

| level | record | payload column |
|---|---|---|
| `full` *(default)* | yes | `b64(prompt)` — today's behaviour, unchanged |
| `redact` | yes | `r:<sha256[0:8]>:<b64len>` |
| `minimal` | yes | `-` |
| `off` | **no** | — |

`redact` is the interesting one: the audit trail and the ordering survive, the text does not, and the
digest is still a **reproducible identity** — hash a candidate prompt's b64 and compare, and the log
still answers *"was THIS the prompt that was sent?"*. It stops answering *"what was it"*, which is
the part that costs 1.5 MB of retained operator text.

The level resolves at **call time** and is cached per process (a load-time global would not see a
test's env assignment — the export-vs-load-time-global trap that already governs the WAL path).

## The three rules that keep a thinned log honest

A logging level is an invitation to make a system quietly claim less than it did. Three constraints,
each with its own gate leg:

1. **A level thins the PAYLOAD COLUMN, never the record and never the ordering.** `intent` still
   lands before any guard at every level except `off`. Leg 6 drives a real refused send at `redact`
   and asserts `intent` precedes its outcome — the invariant that makes it a WAL rather than a
   receipt.
2. **A level CHANGE is journalled in the log itself** (phase `level`, `<from>-><to>`), exactly once,
   at the moment it happens. `off` writes that one marker and then nothing, so the log *says* where
   it stopped: a gap is explained **in the artifact**, not only in whatever env a later reader
   happens to have. The marker carries `-` for pid and win, so the pid+win outcome join in
   `wal_replay` can never mistake it for an outcome (asserted at the writer in leg 8 and at the
   reader in leg 9 — the same rule at both ends).
3. **`--replay` renders a thinned payload as an explicit claim** — `«redacted (level=redact) …»` /
   `«no payload retained (level=minimal)»` — never as an empty column, because an empty column is
   indistinguishable from an empty prompt. It also prints the effective level *and* the log's own
   last recorded change, since the reader's env is not necessarily the writer's; and an absent log at
   `off` says so rather than reporting a bare "no injection log" that would let a silenced journal
   read as a node that sent nothing.

Plus: an **unrecognised** level is a loud stderr warning and falls back to `full`. For a journal the
fail-safe direction is *more* evidence, never less (the same documented asymmetry as
`mesh-load-gate --effectivity`). The `-` and `r:` sentinels are outside the base64 alphabet, so
neither can collide with a real payload.

## Gate

10 new legs inside `mesh-tell --test`'s existing WAL block (legs 5–14), each driving a **real send in
a child process** — never `wal_append` in-process, because the level is resolved once and cached per
process: an in-process leg would silently test the first level it ever saw and go green for all four.
Each child sends to a non-existent window with the same DEAD-SHELL stub the pre-existing leg 3 uses,
so the guard refuses and the run produces a real intent+outcome pair without a tmux fixture.

Coverage: redact digest is reproducible **and** the plaintext and the b64 are both absent from the
log · ordering survives thinning · minimal is payload-less · off writes no record and exactly one
marker · the marker's own pid/win fields are `-` · a marker cannot be joined as an outcome · replay
renders **both** thinned branches explicitly and announces the level · unknown level → FULL **and**
warns · the node-config path sets the level · env overrides the node config · **the default is
byte-identical** (same 7-field b64 record, and no marker on a fresh log).

**8 mutants, all RED from a scratch copy**, control green: redact transform dropped · `off` still
journals · marker never written · minimal renders blank · unknown level silently becomes `off` ·
node-config read removed · node config overrides env · marker carries a real pid.

**Two mutants that first came back green, and what they cost:**

- *minimal renders blank* survived the first sweep. Leg 10 asserted only the `redact` rendering, so
  the `minimal` branch of the same `case` was free to render empty — the exact silent-fallback shape
  rule 3 exists to prevent, sitting inside the feature that introduces it. A rule asserted at one
  branch is not asserted; leg 10 now covers both.
- *unknown level silently becomes off* was mis-written the first time (it inserted a branch already
  shadowed by an earlier pattern) and changed nothing — a mutant that does not do the thing it names
  proves nothing about the leg. Re-written against the real `*)` branch, it goes red.

Live check after the change: `mesh-tell --replay -n 3` against the **real** 2056-line log reads
exactly as before — no `level:` header, no sidecar file created, no marker written. The default path
is untouched, and leg 4 (the pre-existing sandbox-honesty leg) still proves `--test` never writes the
real log.

## Incidental, not fixed (out of scope, worth its own task)

A send to a window that does not exist and whose payload does *not* trip `dead_shell_guard` exits **0
having journalled only the intent** — no `sent`, no `refused`. `--replay` correctly shows it as
`UNRESOLVED`, so the WAL is honest; but the tool returns success. Found while building the fixtures
(it is why the level legs needed the DEAD-SHELL stub to produce an outcome at all). Pre-existing,
unrelated to levels, not touched here.

## Not configured anywhere yet

`nodes.example` documents the knob (commented, like every other entry); no node sets it. `full`
remains the default and the live behaviour on every node until an operator chooses otherwise —
which is the point: `off` gives up the write-ahead guarantee, and that has to be a deliberate act.
