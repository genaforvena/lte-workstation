# The replica id was the kernel's enumeration order, and this node's disks have swapped it twice

**Live review, 2026-08-25 — distributed systems coordination (gossip, CRDTs, eventual consistency),
from the angle the task asked for: an OPERATIONAL mechanism, not a philosophy.**
**Arm:** treated (assigned) — target organ `scripts/mesh-nvme-health` drawn by coin at p=0.20 from
the 568 never-reviewed tools, not chosen by me or by the lane.
Landed in `scripts/mesh-nvme-health` (uncommitted; steward lands from the tree).

## What was already ours (checked before searching, so the review could not re-land)

Fifteen prior reviews sit in this area:

| embodied | where |
|---|---|
| causal stability frontier | `distributed-systems-causal-stability-frontier-chat-sync-*` |
| causal delivery / orphan split | `distributed-systems-causal-delivery-orphan-split-promises-*` |
| era/epoch finality, sealed verdicts | `distributed-systems-era-epoch-finality-sealed-verdicts-promises-*` |
| CALM / I-confluence | `distributed-systems-calm-iconfluence-double-hold-promises-*` |
| Age of Incorrect Information, semantic divergence | `distributed-systems-age-of-incorrect-version-*` |
| φ-accrual failure detection | `distributed-systems-phi-accrual-presence-departure-*` |
| MaxWait / consistent cut | `distributed-systems-maxwait-consistent-cut-presence-fuse-*` |
| anti-entropy reconciliation across peers | `mesh-knowledge-sync` |

All of it is about **time and delivery** — when an update is stable, whether a cut is consistent,
how divergence ages. None of it is about **who the replica is**. That is the gap.

## The mechanism, and where I found it

**Paulo Sérgio Almeida & Carlos Baquero, "Scalable Eventually Consistent Counters over Unreliable
Networks"** — arXiv:1307.3207, published in *Distributed Computing* 32(1):69–89 (2019).

Their target is the **identity explosion problem**: a naive G-Counter keeps one slot per replica id
and its state is linear in *the number of independent actors that ever incremented the counter*.
You cannot garbage-collect a slot, because an id that has gone silent is indistinguishable from an
id that is merely slow. **Handoff Counters** are, in their words, the first CRDT-based mechanism to
overcome this: a tiered structure in which a transient replica **explicitly hands its accumulated
value off** to a durable higher tier under a slot/token protocol, after which the transient entry
can be reclaimed — with the invariant that a value is never double-counted and never lost across the
handoff. The authors note the construction is not counter-specific; it applies to any associative,
commutative merge.

`1307.3207`, "handoff counter" and "identity explosion" appear nowhere else in `docs/` or `scripts/`.

## Why it lands on this organ

`mesh-nvme-health` writes one row per boot per filesystem to `~/.mesh/nvme-fs-write.log`, and its
own comment `(c)` says why: `lifetime_write_kbytes` is superblock-persistent, so *"the delta between
two boots"* is *"a real mean rate"* — the one question a single boot's session counter structurally
cannot answer.

That is a grow-only counter with one transient replica per boot. Two things were wrong with it, and
both are identity, not timing:

**1. The replica id was an address.** Rows were keyed `ctrl=nvme0 fs=dm-0` / `fs=nvme0n1p2` —
kernel enumeration names. `CLAUDE.local.md` records that this node's two NVMe devices **swap index
across reboots**, seen twice, each time verified, each time the opposite mapping. So `grep " fs=$fsname "`
can match a row written about a *different physical disk*, and the across-boot delta — the entire
point of the log — would be computed across a device swap. Silently, and possibly negative.

This is not hypothetical. The organ's own comment read:

> `(nvme0=XF-256 spare on mesh-home wears ~2.6x faster than the root nvme1=KINGSTON — serial-verified, …)`

Live sysfs, measured today: `nvme0` = **KINGSTON** ser `50026B738382AFD3`, `nvme1` = **XF-256** ser
`0030990070033`. The comment is **inverted**, and it says *serial-verified* — it was true when
written. A serial-verified fact filed under an enumeration index decays into a false one with
nothing having changed but the probe order.

**2. There was no handoff, because there was no reader.** Nothing in the corpus reads
`nvme-fs-write.log` — `grep -rln` returns only the writer. The transient replicas accumulated for
eight days and were never folded into anything. An accumulator with no consumer is a numerator with
no reader.

## What landed

- **`fs_ident()` — a durable replica id, never the address.** LVM's own UUID for device-mapper
  (independent of `dm-N` activation order), the NVMe controller serial for a namespace/partition,
  both unprivileged from sysfs. It renders `na` when neither exists and **never falls back to the
  name** — falling back to the address is the bug, not the cure.
- **Every row now carries `id=`.** Live: `id=LVM-ByLJUC1n6u2h…` for the root LV,
  `id=nvme-50026B738382AFD3` for `/boot`.
- **The dedup lookup keys on the durable id** when one exists, so a name reused by a different
  device does not have its first record suppressed by the previous occupant's row.
- **`mesh-nvme-health --write-rate`** — the reader the log never had. It computes the across-boot
  mean write rate **only within one durable identity**, and otherwise refuses. The refusals are
  distinct on purpose, because *"first boot"*, *"the disk under this name changed"* and *"the
  counter went backwards"* are three different states of the world and one shared `na` would make a
  device swap indistinguishable from a fresh log:
  - `n=1` — one row for this identity;
  - `IDENTITY CHANGED: this name previously named <id>` — the enumeration moved, the disk did not;
  - `COUNTER WENT BACKWARDS a -> b` — a grow-only counter that shrank falsifies the identity claim
    whatever the id says (superblock reset, or a different device wearing it);
  - `no durable identity` — rows predating this change; legacy rows yield no rate rather than a
    plausible one.
- The inverted comment now quotes **serials**, and says why the index is an address.

This is the handoff **safety condition** borrowed without the protocol: the mesh does not need
concurrent replicas of this counter, so the tiering and slot tokens are not required — what it
needed was the invariant those tokens exist to protect, *never fold a value across an identity
boundary*, and an explicit durable id to fold into.

## Gates

`mesh-nvme-health --test` rc=0, six new arms:

- **control** — same fs, same id, +3600 kb over 3600 s yields a real `1.0 KB/s`; without it every
  `na` below is indistinguishable from a reader that never worked;
- **the swap** — same name, different id: refuses, names the identity it used to be, and prints no
  rate at all;
- **legacy** — rows with no `id=` yield no rate and say why;
- **backwards counter** — caught and named;
- **n=1** — reads as `n=1`, not as an identity change;
- **`fs_ident`** — renders `na` for an unidentifiable device *and prints nothing on stderr*, and an
  LVM uuid wins over the name.

Three mutants driven red: `fs_ident` falling back to the name, `--write-rate` keying on the name
again, and the backwards-counter check removed.

The `fs_ident` stderr assertion is there because the first cut used `tr < "$path" 2>/dev/null`, and
a **failed open is reported by the shell, not by the command** — so it printed *"No such file or
directory"* for every non-dm device, which is most of them (memory
`a-stderr-null-after-a-redirection-cannot-suppress-the-open-failure`). It now tests `-r` first.

## Honest bounds

- **No swap was observed today.** The identity change is asserted on fixtures; the *evidence that it
  happens* is `CLAUDE.local.md`'s two verified observations plus the organ's own inverted comment,
  which is a consequence of the swap rather than a sighting of one.
- `--write-rate` is `n=2` — newest row against the most recent prior row of the same identity. It is
  a mean over one interval, not a rate estimate, and it says `n=2 rows` in its own output.
- The live log's existing rows predate `id=` entirely, so `--write-rate` on this node currently
  prints the `no durable identity` refusal for both filesystems. That is the correct reading and not
  a defect: the rate becomes available after two rows have been laid down under the new format.
- Handoff Counters solve a problem the mesh does not have (concurrent independent incrementers of
  one logical counter). Only the identity discipline transfers; the tiered protocol is deliberately
  not implemented, and claiming otherwise would be borrowing the name without the mechanism.
