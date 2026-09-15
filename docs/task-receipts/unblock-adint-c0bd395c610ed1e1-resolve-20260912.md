# Resolver receipt: `unblock/adint/c0bd395c610ed1e1/resolve`

- Checked: `2026-09-12T02:36Z` UTC on `mesh-home`
- Parent: `unblock/haunt/fd5d75268b44e1cc/resolve` (owner `haunt`)
- Result: **dictionary inputs selected and frozen; parent now needs experiment-contract reconciliation, not operator input**

## Evidence

The exact-owner dispatch check passed before `adint` claimed this resolver. The operator has
explicitly directed us to choose all Tiny Fleet inputs ourselves; that direction is also recorded
in `/home/mesh-home/tiny-fleet/docs/task-receipts/adint-operator-authorized-dictionary-input-20260912.md`.
The frozen choice is Tiny Fleet's existing CC0, synthetic-only A08 correction fixture: English and
Russian, exact case-sensitive replacement normalization, immutable source commit, and its 152-row
corpus. I independently recomputed the six source and result hashes below; all match the Tiny Fleet
receipt.

| Artifact | SHA-256 |
|---|---|
| `runs/operator-selected-dictionary-v1/input-manifest.json` | `9081dd78b28ed94b501016698cd6d5347095a5ea079730bf888123c3ec2e1e08` |
| `runs/operator-selected-dictionary-v1/corpus.jsonl` | `81a41340c0c01555a536e9aa30b3b2b72b1dd9ae48908014fd0f58192515dcd3` |
| `corpus/applications/noisy-text-correction/manifest.json` | `17879f42f885b18ed5e0638a6620ff745200ddb79d9a3004a20fa22933ea0997` |
| `scripts/applications/noisy_text_correction.py` | `69330b7803f0844198c84f07d54cc89e822d4df9abc63ddfb58b6c3c921c60db` |
| `runs/operator-selected-dictionary-v1/result/raw.jsonl` | `555f1ab7808d5d01324c770e58fc594b48ea17ff55364d6a4214e4aed8b988fd` |
| `runs/operator-selected-dictionary-v1/bbywvy-smoke.txt` | `f64847a15bc68114b0d369200a0173d3f37e8a76c13fe499d93f9854eb4cffc6` |

The A08 heldout baseline measured 120/120 exact, but its verdict is `INCONCLUSIVE`: it is limited
to five synthetic substitutions and its ByT5/LoRA arms are unavailable. The BbyWVY script is a
six-case generative runtime smoke with no dictionary/lexicon arm. I confirmed that by searching the
script; its smoke output includes a math answer of `9000 km` for 60 km/h over 2.5 hours, so it
does not establish answer quality either. Therefore the selected inputs exist, but the measured A08
result does not prove the BbyWVY dictionary behavior required by the parent.

## Parent task update and next action

Live `mesh-task status unblock/haunt/fd5d75268b44e1cc` still shows `blocked` with the stale
`operator-input` diagnosis. Its owner-authored resume gate,
`mesh-task check resume unblock/haunt/fd5d75268b44e1cc/resolve haunt`, exits `2`.

The exact update is: replace the missing-input diagnosis with the experiment-contract gap. The
`haunt` owner should either accept this narrowly scoped synthetic A08 result and revise the claim
and retry accordingly, or identify/implement the intended BbyWVY-compatible dictionary arm against
the frozen manifest and corpus, measure it, and record hashes plus a typed verdict. The resolver
does not contain `unblock=cleared`, because neither option has yet been completed; the parent stays
blocked and must not be resumed on this evidence alone. No operator response is needed for input
selection. `adint` did not write or impersonate the `haunt` owner's ledger transition.
