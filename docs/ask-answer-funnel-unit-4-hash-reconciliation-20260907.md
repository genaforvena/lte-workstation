# Unit 4 artifact hash reconciliation — 2026-09-07

The Unit 4 artifact has had multiple owner-authored snapshots during the
full-suite fence investigation. Preserve the mismatch; do not hand-edit any
ledger or chain JSON.

| observation | SHA256 | disposition |
|---|---|---|
| prior owner progress snapshot | `9da7bba441a6eed3ff87e965152df2e946c8b72d9e2671e3f32473858b33ddc5` | superseded by later artifact text |
| independent witness snapshot | `14c26696a05ebe23da675769a8f7c5ccac7602b3b33ecf00f51798113b302ab4` | preserved as independently observed; not overwritten |
| current shared-workspace artifact | `d9fb48a8829fac223c8f409dd612e2600422cdaaa6a5e76ca25c671e076c12f6` | current owner snapshot |

The implementation, focused test, source/deployed parity, and live frame are
accepted. The full deployed `mesh-dash --test` remains blocked on its node
condition/terminal-result reconciliation; this file is an integrity record,
not a claim that the mismatch is resolved.
