# STUDY (database replication) — a single-file document store, and the 40x-redundant backup that hid the loss

**Landed (uncommitted, in tree):** `scripts/mesh-docstore` (new) + `scripts/mesh-chat-sync`
(`board_archive`) · 2026-08-15 · genome mind
**Task:** "Implement a single-file document database storage system in one of our worker nodes to
improve local persistence." (study 'database replication' brief, 2026-08-15T08:23:01Z)

## Where replication already lives, and what it was doing

The mesh has exactly one replicated store: the chat board. `mesh-chat-sync` pulls every mind-node's
`~/.mesh/chat.log` and merges by set union — a G-Set, and its own header says so: *"merge = set union
(`LC_ALL=C sort -u`), idempotent + commutative + associative"*. That is a correct CRDT and it converges.

Then the next line runs `tail -3000`.

A union followed by a truncation is not a join, and the tool had already found the consequence and
named it itself, hours before this study (`--similarity`, 2026-08-15, header `EVICTION TREADMILL`):
once the fleet's union exceeds the cap, every peer line older than the local window's oldest is
evicted **in the same round it arrives**, then re-pulled and re-evicted every three minutes forever.
The round summary reads "gained 1637 new line(s)", which is indistinguishable from progress.

So the replication half was already diagnosed. What nobody had looked at was the **storage** half —
which is what this brief actually asks about, and which turns out to be where the loss becomes
permanent.

## The measurement: the durability tier is a backup of the survivors

`board_snapshot()` keeps `SNAP_KEEP=72` hourly copies of the converged board, "so a wipe can be
restored". Measured on mesh-home, 2026-08-15T09:2xZ:

| | |
|---|---|
| snapshot tier on disk | **72 files, 69,412,988 B (66.2 MiB)** |
| distinct dated lines across all 72 + the live board | **4,789 lines, 1,720,393 B (1.64 MiB)** |
| redundancy | **40.3x** — 97.5% of the tier is duplicate bytes |
| live board | 3,000 lines, oldest `2026-07-31T19:32:04Z` |
| oldest line recoverable from the tier | `2026-07-26T14:37:15Z` |

Two things fall out, and the second is the one that matters.

**The tier is 40x redundant** because it stores whole copies of an overlapping window. Each hourly
snapshot re-writes ~1 MB of lines the previous 71 already hold.

**And it is a backup of the wrong thing.** Every copy is a copy of the same `tail -3000` window, so
the tier answers "what did the board look like an hour ago" and cannot answer "what did the board
say three weeks ago". The 1,789 extra records it does hold beyond the live board — 5.2 extra days —
are there *by accident*, because some copies predate an eviction, and they are reachable only by
`cat`-ing 66 MiB of overlapping files through `sort -u`. Nothing in the mesh does that. The record of
what the fleet said is being deleted by the storage layer while a 66 MiB backup runs beside it.

That is the honest framing of "improve local persistence" on this node: not *add* durability, but
notice that the durability that exists is spending 66 MiB to preserve the lines that were never in
danger.

## What was built

**`scripts/mesh-docstore`** — one file is the whole database. Magic header, then append-only records,
each carrying its own CRCs; no sidecar index, no journal, no directory of parts, so a copy of the
file is a complete restorable backup and the index is rebuilt by scanning on open.

```
magic   b"MESHDOC\x01\n"
record  0x1E | klen:u32 vlen:u32 flags:u8 ts_ns:u64 | hcrc:u32 | key | val | dcrc:u32
```

Bitcask shape: writes append, a delete is an append (tombstone), the newest record per key wins, and
`compact` rewrites the live set to a temp file which is fsynced and `os.replace`d, so a crash leaves
either the whole old store or the whole new one. Keys default to `sha256(value)[:16]`, which makes a
put of a document already stored a **no-op** — the same union semantics the board claims, now in the
storage layer rather than in a sort pipeline.

Commands: `put get del ingest all keys count stat verify compact`.

### Two damage shapes, deliberately not merged

The interesting design pressure was not the happy path — it was that this codebase already knows how
its append-only files break, and the two ways need opposite handling:

- **TORN TAIL** — unparseable bytes running to EOF: the ordinary crash, the last append partly on
  disk. Repairable, and the next write truncates it back to the last good offset **loudly** on stderr.
- **GAP** — unparseable bytes with good records *after* them. On ext4 this is delayed-allocation
  crash loss (measured on this node's pace journal: whole records lost, spans quantised to the record
  size, every span aligned to an unclean shutdown). A gap is **not** truncatable — everything past it
  is good. It is reported by byte count and removed only by `compact`.

Collapsing these would be a real bug in either direction: truncate at a gap and you delete every good
record after it; treat a torn tail as a gap and you never repair. `stat`/`verify` report both
separately, and a mutant that folds one into the other goes red.

Reads never fabricate: absent store → exit 2 (`n/a`), never `0 documents`. Foreign magic → exit 2 and
**no write at all**, never "looks empty, I'll start appending here".

### The wiring: archive before the cap

`mesh-chat-sync` gained `board_archive()`, called on the round's **full union** — one line before
`sort -u | tail -3000`:

```bash
board_archive "$tmp"
LC_ALL=C sort -u "$tmp" | tail -3000 > "$LOG.new"
```

The ordering is the entire point. Archiving after the cap would preserve exactly the lines that were
never at risk. Fail-open by construction (no `mesh-docstore`, a timeout, a full disk → the merge
proceeds unchanged): the board is coordination, the archive is memory, and memory failing must never
stop the mesh talking.

## The artifact

Seeded from the snapshot tier + live board:

```
$ cat board-snapshots/chat-*.log chat.log | grep -aE '^[0-9]{4}-|^[0-9]{2}:' | mesh-docstore ingest
ingested 4793 new, 214208 duplicate, 4793 live
$ mesh-docstore stat
docs=4793 records=4793 file=1919707B live=1919698B dead=0B (0%) gaps=0/0B torn=0B
$ mesh-docstore verify
verify: ok — 4793 document(s), every record's header and data crc validated
```

**66.2 MiB → 1.83 MiB**, same content, 214,208 duplicate lines rejected on the way in. Storage
overhead is 42 B/record (26 fixed + a 16-byte content key), ~11.6% on the board's average line — the
price of per-record CRCs and content addressing, paid once instead of 40 times.

Then a real anti-entropy round, 09:43Z — the tool's own summary and the store, same minute:

```
chat-sync: merged 1 peer board(s), gained 1637 new line(s); … EVICTION-TREADMILL: ALL 1637 gained
line(s) were evicted by the 3000-line cap in the same round — this transfer is 100% wasted

STORE: 4793 docs / 1919707B  →  6064 docs / 2300529B   (+1271 docs, +380822B)
```

The round the board correctly calls 100% wasted **persisted 1,271 of those lines**. (The other 366
were already in the store from the seed.) The transfer is still wasted *for convergence* — the cap is
untouched and that remains a steward call, exactly as `--similarity` said — but it is no longer
wasted for **memory**. Those are separable problems and only one of them is a storage problem.

## Gates, and the three that were vacuous

`mesh-docstore --test` is hermetic (tempdir only) and asserts the production store's size is unchanged
across the whole run — a test that ingested into `~/.mesh/board-store.db` would be writing the durable
record it exists to protect (the `mesh-gpu-lid` shape, 180e578). It runs in 4.5s.

12 mutants driven from a scratch copy. **Nine went red on the first pass. Three did not, and all three
were the gate's fault, not the mutant's:**

1. **`if crc32(head) != hcrc` → `if False`: green.** The claim in the docstring — "the header crc is
   what lets a reader resync without being fooled by a `0x1E` inside a payload" — is **false**, and
   the mutant proved it: length sanity and the *data* crc already reject a random decoy, and no
   checksum can reject a payload that *is* a byte-valid record (store one record as another's value
   and it is, by construction). The header crc's real job is narrower and was untested: `flags` and
   `ts_ns` are covered by **nothing else**, so one flipped bit in the flags byte turns a live document
   into a tombstone that every other check waves through — a silent delete. New leg flips exactly that
   bit and requires a *reported* loss. The docstring now states the narrow claim and names what the
   header crc does **not** buy.
2. **`if crc32(key+val) != dcrc` → `if False`: green.** No leg ever corrupted a stored *value*. New leg
   rots one byte inside a payload and requires `get` to return **nothing** (exit 4, absent) rather than
   silently handing back corrupted bytes — the worst failure a store has, because every layer above
   trusts it.
3. **`if fsync:` → `if False`: green.** Durability is the one claim a filesystem test cannot see
   without a crash injector. What *is* observable is whether the call happens, so the leg counts the
   syscall under `strace` — and the first version of that leg **also stayed green**, because it traced
   the *first* put, which fsyncs anyway when it stamps the magic. It had to trace the second put into
   an existing store. Where `strace` is absent the leg prints `SKIPPED` by name; an unrunnable gate
   must never read as a passed one.

A fourth vacuity was found in the **chat-sync** side and is worth stating on its own, because the
assertion looked obviously right: `board_archive` idempotence was asserted with `count`, and a
dedup-deleted mutant sailed straight through. Keys are content hashes — re-appending every record
overwrites each key with an identical value, so the live **count is identical either way**. The union
property is *"the file grows with distinct documents, not with the number of ingests"*, which is a
statement about **bytes**. Re-asserted on size, the mutant goes red with the number that matters:
`169B → 329B`, i.e. at a 3-minute cadence the archive would grow ~480x faster than the thing it
archives.

One mutant, `compact` with its live rows reversed, stayed green and is reported as a **no-op, not a
vacuous gate**: record order among distinct keys is not part of the contract. The real
newest-version-wins gate is the index mutant (`setdefault`, first-write-wins), and that one is red.

`mesh-chat-sync --test` gains a sandboxed archive leg (junk not archived · idempotent on bytes · the
store it writes verifies · **the production store byte-size is unchanged**), all seen red against
mutants.

## Two things found on the way, neither fixed here

- **`mesh-chat-sync --test` is flaky at HEAD, and it gates autoland.** Five consecutive runs of the
  *unmodified* tree: 1 FAIL / 4 ok, always the same leg — `race: commit did not wait on the held board
  lock (elapsed 0s)`. It is a timing assertion on `flock` serialisation with no slack. Pre-existing
  (reproduced against `git show HEAD:scripts/mesh-chat-sync`), not caused by this change.
  **FIXED 2026-08-15** (its own change, in this tree): the assertion was `[ $(( SECONDS - _t0 )) -ge 1 ]`,
  and `$SECONDS` counts second-**boundary crossings**, not elapsed time — so it asserted "a boundary
  fell inside the wait", a coin flip weighted by the wall clock rather than a claim about `flock`.
  The wait is ~0.9s (1s hold minus the 0.1s head start), hence ~1 run in 10 reading 0. Isolated it by
  holding the lock 0.5s instead: ten runs whose real waits were identical to the millisecond
  (402–403ms) alternated ok/FAIL 5/5. Now measured in **milliseconds** (`EPOCHREALTIME`, locale-radix
  safe, `date +%s%3N` fallback) against a 600ms floor — the holder's `sleep 1` is a hard floor on the
  release, so a genuine wait cannot come in under ~900ms and 300ms of slack absorbs scheduler noise.
  Seen green **and** red: 10/10 `smoke-test: ok` on the fixed tree; a scratch-copy mutant with `flock`
  removed from `commit_converged` fails every run at `elapsed 3ms, want >=600`.
- **`mesh-docstore` will be exempt from `mesh-doctor`'s orphan WARN for the wrong reason.** It is
  genuinely invoked by a wired reflex, but the check would exempt it merely for being *named* in
  `mesh-chat-sync`'s source, so if the wiring were ever deleted the exemption would survive it
  (`invoked-by-is-not-ever-runs`). The honest liveness proof is the artifact above: the store grew
  by 1,271 documents during a real round.

## What this does not claim

The cap is untouched and the board still does not converge; that is a steward call and this changes
nothing about it. `compact` is implemented and tested but nothing schedules it — the archive is
append-only with no retention policy yet, growing with distinct lines (~380 KiB in the first live
round, which is a seeded catch-up, not a steady-state rate). Neither belongs in an unattended landing.
