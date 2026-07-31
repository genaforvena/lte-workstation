# Decay review: mesh-rns-offgrid & mesh-phone-beacon2 — both KEEP (false decay signals)

Date: 2026-07-31 · reviewer: genome@mesh-home · verdict: **KEEP both**, no genome change.

Two tools were queued as "unused+failing (decay candidate)". Both signals are **false positives** of
the naive decay heuristic (*not-in-cron-here + non-zero exit here = dead*). Neither is dead; each is
correctly node-bound / on-demand, documented, and carries a **real, passing `--test`**. Decaying either
would delete a working proof/organ on the strength of an artifact that describes the *wrong node*.

## mesh-rns-offgrid — KEEP

- **`--test` passes NOW with a real cryptographic artifact** (run twice, distinct nonces → live, not cached):
  ```
  PROOF OK: link up, 16-byte nonce round-tripped E2E over TCP (3bf92f5c…)   rc=0
  OFF-INTERNET-CAPABLE: 192.168.8.224 <-> ilya@100.107.198.111 round-tripped an E2E Link
  over LAN TCP, zero internet interface in the config.
  ```
- It is a **deploy shim** (13 lines) execing the real proof `scripts/reticulum/rns-offgrid-proof.sh`,
  which has a real gate: `--test` runs the plain proof, honest `exit 2` when the peer is unreachable
  (`na(){ … exit 2; }` :83). So "failing" on a peerless run = **honest n/a**, not a fault.
- Carries an explicit `# orphan-ok:` header (on-demand off-internet PROOF/demo, `--blackout` drops the
  uplink) — deliberately never cron-wired. Documented in `docs/reticulum-offgrid-proof.md`; memory
  `reticulum-offgrid-proof.md`, `reticulum-remote-shell.md`.
- **Verdict: proven worth. Keep.** Its worth *is* the on-demand proof, which reproduces on demand.

## mesh-phone-beacon2 — KEEP

- **The "failing" is a wrong-node interpreter, not a broken tool.** Shebang
  `#!/data/data/com.termux/files/usr/bin/sh` (it deploys ON THE PHONE via Termux:Boot). Exec'd on
  mesh-home the interpreter is absent → `cannot execute: required file not found`, **rc=127** — exactly
  the "failing" a mesh-home scanner sees. Run through an available shell it is green:
  ```
  $ sh scripts/mesh-phone-beacon2 --test   →   smoke-test: ok   (rc=0)
  ```
- Its `--test` is **substantial and RED-able**, not vacuous: a chaos network-fault drill that SHADOWS
  `curl`, asserts the armed fault short-circuits `push_one` *before* curl is reached, that clearing it
  restores the push, and that buffer-and-forward retains (kept=2) then drains (remain=0) the queue —
  the exact QUEUE→flush path that keeps an AWAY walk from being lost.
- **"Unused" is by-design node-binding.** Listed in `CLAUDE.md` on-demand canon (:460, "phone BODY /
  Termux") — runs only on the operator's phone, unwired everywhere else *by design*. From mesh-home the
  phone's cron is unobservable (tmux-is-the-only-way-to-see-into-a-node); absence-of-observation here is
  not absence-of-use there.
- **Verdict: proven worth. Keep.** Already satisfies "give it a real `--test`".

## Root cause (worth pinning)

Both are the recurring **false-decay** shape: a decay heuristic that reads *not-wired-here* +
*non-zero-exit-here* as *dead* will always fire on (a) `orphan-ok` on-demand tools and (b) node-bound
organs whose shebang/organ lives on another node. The artifact for "failing" must be the tool's own
`--test` run under a shell it can execute — not a bare exec on a node it was never meant to run on.
Sibling of `na-must-be-a-claim-about-the-node` and `invoked-by-is-not-ever-runs`.

## Addendum 2026-07-31 (re-dispatch): RED-ability DEMONSTRATED + why it re-queued

The idea-queue re-dispatched the identical `mesh-phone-beacon2` decay review. Re-verified, still **KEEP**,
and closed the two gaps the first pass left open:

**1. The `--test` is not just *asserted* RED-able — it was SEEN red.** Two scratch-copy mutants (genome
untouched):
- neuter the chaos short-circuit (`MESH_CHAOS_NETFAIL` guard → `:`) → `rc=1`, 4 FAILs incl.
  `netfail(env) did not crash the connection` and `armed fault lost buffered records (kept=0, want 2)`.
- break `flush_queue` retention (drop failed pushes) → `rc=1`, `flush_queue did not retain only failed
  pushes (kept=0 remaining=)`.
Both restore to `smoke-test: ok`. A gate that goes red for the right reason on the exact behaviours it
guards — non-vacuous, confirmed by observation, not inference.

**2. Root cause of the re-dispatch: a STALE candidate report, not a live signal.** `--candidates` still
listed beacon2 as `UNUSED + FAILS smoke [--test rc=127]` — but that answer comes from the persisted
report `~/.mesh/reflex-decay.log` stamped **04:41:01Z**, generated *before* the wrong-node guard landed
at **fe92b88 07:48:18Z**. The guard (deployed, in sync with genome) parses the shebang interpreter
(`/data/data/com.termux/files/usr/bin/sh`), finds it absent (`[ ! -x ]`), and classifies the tool
`UNASSESSABLE on this node (lives)` — never a smoke failure. Its own `--test` case **4c** asserts exactly
this and passes `rc=0`. So the class is permanently fixed at the lane; a fresh scan drops beacon2 from
candidates. **No genome change needed** — the fix already shipped; the re-dispatch was minted off a
report that predates it. (Sibling of `a-constant-outlives-its-reader`: a cached verdict outliving the
code that would now render it differently.)
