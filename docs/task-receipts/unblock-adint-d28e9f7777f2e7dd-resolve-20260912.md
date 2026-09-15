# Resolver receipt: `unblock/adint/d28e9f7777f2e7dd/resolve`

- Checked: `2026-09-12T03:36:08Z` UTC on `mesh-home`
- Parent: `unblock/haunt/fd5d75268b44e1cc/resolve` (owner `haunt`)
- Result: **the five-input prerequisite is already frozen and verified; the parent remains blocked on experiment scope**

## Evidence

The existing operator-authorized selection and measurement are recorded in
`/home/mesh-home/tiny-fleet/docs/task-receipts/adint-operator-authorized-dictionary-input-20260912.md`.
The experiment-contract receipt at
`docs/task-receipts/haunt-dictionary-experiment-contract-20260912.md` narrows the current parent
blocker: the A08 synthetic result is inconclusive for broader correction behavior and does not
measure BbyWVY dictionary behavior.

I independently checked the frozen artifacts with `rtk sha256sum`:

| Artifact | SHA-256 |
|---|---|
| `runs/operator-selected-dictionary-v1/input-manifest.json` | `9081dd78b28ed94b501016698cd6d5347095a5ea079730bf888123c3ec2e1e08` |
| `runs/operator-selected-dictionary-v1/corpus.jsonl` | `81a41340c0c01555a536e9aa30b3b2b72b1dd9ae48908014fd0f58192515dcd3` |
| `corpus/applications/noisy-text-correction/manifest.json` | `17879f42f885b18ed5e0638a6620ff745200ddb79d9a3004a20fa22933ea0997` |
| `scripts/applications/noisy_text_correction.py` | `69330b7803f0844198c84f07d54cc89e822d4df9abc63ddfb58b6c3c921c60db` |

The frozen source is Tiny Fleet commit `ed7fa28fb2b010f0cd1294b6df36bf53a5d21396`, CC0-1.0,
synthetic-only. The corpus is 152 rows in English and Russian. Normalization is exact and
case-sensitive with no Unicode normalization, case folding, or tokenization. The full field
definitions and measured A08 result are in the linked operator receipt.

## Resolution boundary

`rtk mesh-task status unblock/haunt/fd5d75268b44e1cc` currently reports the parent blocked with
`experiment-contract`, and `rtk mesh-task check resume unblock/haunt/fd5d75268b44e1cc/resolve haunt`
exits 2. Therefore the earlier “inputs missing” diagnosis is stale, but the parent cannot safely
resume on these artifacts. Its owner must either amend the claim/closure gate to the A08-only,
`INCONCLUSIVE` result or provide a BbyWVY-compatible dictionary arm and measurement. This resolver
does not alter or resume the `haunt`-owned row.
