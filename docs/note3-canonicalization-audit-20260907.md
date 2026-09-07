# Note3 canonicalization audit — 2026-09-07

Status: audit and scoped migration plan only. No files were moved, overwritten, or deleted.

## Canonical identity

For this task, **Note3** means the physical device identified by all of:

| Field | Live value |
|---|---|
| model | `SM-N900` |
| Android | `5.0` |
| serial / adb transport | `4d00553d61ab90b7` |
| local proof | `~/.mesh/.note3-adb-transport`, observed `REACHED` at `2026-09-07T20:10:01Z` |

This is not the Redmi node. The registry still names the Redmi separately as
`Redmi:u0_a380@100.103.99.16`; `mesh-phone-ip` returned that last-good Redmi address while
ADB independently exposed the Note3. No identity substitution is safe.

The proposed canonical namespace is the Note3's operator-visible storage, addressed by the
stable serial rather than a network address:

```text
adb -s 4d00553d61ab90b7 ...
/sdcard/MeshCanonical/
  personal/       operator-owned source material and exports
  knowledge/      reviewed mesh knowledge snapshots
  repositories/   explicitly selected repository snapshots
  evidence/       manifests, receipts, and hash ledgers
```

`/sdcard/MeshCanonical/` does not yet exist. It is a proposal, not an assertion that a copy is
already present. Creating it and populating it require the operator/steward migration step.

## Live findings

The Note3 public storage probe found only the pre-existing `Pandora+BT_ru...apk` and no
`Documents` directory; `Camera` was absent on the second read. The APK was read without writing
and hashed as:

```text
6f5bdd2bd8a02667e7b50490a1abe545e6e7207b5c5f2bfba3213fe45450e216  /sdcard/Pandora+BT_ru.alarmtrade.pan.pandorabt.apk
```

Therefore the claim “everything is already on Note3” is **not true for the audited mesh/repository
corpus**. The Note3 is the identified operator-owned destination, but it currently has no visible
canonical corpus in public storage.

## Current copies and ownership boundary

| Source | Live size / files | Working interpretation | Migration disposition |
|---|---:|---|---|
| `/home/mesh-home/lte-workstation` | 165,184,953 bytes / 11,965 files | shared source repository; dirty local work exists | copy only after manifesting dirty state; never overwrite |
| `/home/mesh-home/.mesh/knowledge` | 13,006,705 bytes / 2,127 files | shared reviewed knowledge plus generated history | snapshot reviewed files; keep runtime corpus until steward reconciles |
| `/home/mesh-home/.mesh/note3` | 76,701,478 bytes / 216 files | Note3-derived audio/organ material cached on mesh-home | preserve as source; export with provenance, do not treat as device copy |
| `/home/mesh-home/.mesh/adint-vantage/note3` | 916,931 bytes / 1 file | Note3 vantage artifact | hash and export as evidence, no deletion |
| `/home/mesh-home/.mesh/gmail-note3` | 10,326,016 bytes / 4 files | local Gmail database/cache read through the Note3 lane | high-risk personal data; operator confirmation required before export |
| `/home/mesh-home/self-adint` | 721,769,286 bytes / 7,965 files | separate personal/ADINT working tree | separate migration decision; do not bulk-copy blindly |
| `/home/mesh-home/.mesh/inbox` | 394,113,705 bytes / 414 files | mixed operator intake, not all Note3-origin | classify by provenance before copying |
| `/home/mesh-home/.mesh/records` | 2,093,342,259 bytes / 1,190 files | generated audio archive | capacity/material-pricing gate before any migration |
| `/root/lte-workstation` on `phaedra` | 84M | divergent repository copy | steward must reconcile, not delete |
| `/root/.mesh/knowledge` on `phaedra` | 7.5M | divergent knowledge copy | steward must reconcile, not delete |

The Note3 is operator-owned by the task statement, but the mesh-home and phaedra trees have
shared/runtime ownership semantics. “Fully his” authorizes treating the Note3 destination as
operator-owned; it does not authorize deleting other copies or rewriting shared writers.

## Hash and divergence evidence

Selected local hashes:

```text
5412cc58f64976271a4b7c6b6942b4abc375bf64968e62bea7b78f99ef394076  ~/.mesh/.phone-id
22c29c78e7916b2d3ef713c95e6152a21ef1b7d6a310755da34e00088462c1db  ~/.mesh/.note3-adb-transport
79f314024603c5efbac5f0747b88465ccab73ca32b9a6f2e21572684159c78a3  ~/.mesh/gmail-note3/gmail.db
1c1d50a9bb58a485b04338086f796ea563098198aea4db887858b4e3f6681156  ~/.mesh/knowledge/capability-note3-environmental-suite-baro-temp-humidity-20260717.md
```

Repository/forest manifests were streamed as sorted per-file SHA-256 records and then hashed.
Because the current command included absolute paths, these are audit fingerprints rather than
direct equality claims:

```text
mesh-home/lte-workstation   a4b3c79cc29546f64c3978652824e6afbac7a7c3e2b93a70fb700f5c6ac9790a
mesh-home/self-adint        05d3c5272ca685679439b136cd989aab12f60945d983cdac9fc51341c600ab00
mesh-home/.mesh/knowledge   f688726526215607d000a060f75fb8d4a3c7eefdc5926c56d3e7983748beb8d4a8
phaedra/lte-workstation     ca78da821c55f0e8c2e5f71a4ab49828b949aff887403db443f6517eb90a76c8
phaedra/.mesh/knowledge     d5027ea0e1774a0d8f2652d2f3561c21b91104ae8b648683bb3fcbe5c97a1f48
```

The repository HEADs also diverge: mesh-home is `74cc8f4724d7cd01faa70ce19f0eb83696bce744`;
phaedra is `6e7a7826b1650e7f280c708f95fa493d4adf6a27` and reports `[ahead 1, behind 189]`.
This is a hard stop against blind sync or deletion.

## Scoped migration plan (not executed)

1. **Freeze and enumerate.** The steward records a path-relative manifest, owner, producer,
   sensitivity, size, mtime, and SHA-256 for each selected source. The manifest itself goes under
   Note3 `evidence/` and remains in the source trees.
2. **Price material.** Start with small reviewed knowledge and explicit operator exports. Measure
   Note3 free space and transfer capacity before considering `self-adint`, inbox, or the 2.1 GB
   records archive. Personal Gmail/database material is opt-in only.
3. **Copy, never move.** Copy to a temporary Note3 staging directory, then verify every hash from
   the source-side manifest against a Note3-side manifest. A failed or partial transfer leaves both
   originals untouched.
4. **Reconcile ownership.** The steward resolves repository and knowledge divergence by commit/tree
   comparison and explicit operator choice. Generated state, locks, WAL/SHM files, credentials,
   and live caches are excluded unless a consumer-specific export contract says otherwise.
5. **Promote by receipt.** Only after matching hashes and a readable Note3 manifest may the steward
   designate a class canonical. Existing mesh-home and phaedra copies remain retained until the
   operator separately authorizes archival/deletion.
6. **Wire later, by owner.** Any producer path changes belong to the owning steward (likely genome
   for shared knowledge/repository publication and the relevant organ owner for Gmail/ADINT). This
   discover window will not add a second writer.

## Explicit blockers / decisions needed

- Confirm whether `/sdcard/MeshCanonical/` is the desired Note3 public-storage namespace.
- Name the first migration class: reviewed knowledge, repository snapshot, or personal export.
- Decide whether Gmail DB/WAL and `self-adint` are in scope; they contain sensitive material and are
  not safe to infer from a general “everything” instruction.
- Authorize the steward to perform the staged copy after the above choices; no deletion is included.
