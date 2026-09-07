# Unit 1 explicit-key artifact hash reconciliation

Task: `ask-answer-funnel-implementation-20260907/unit-1-explicit-key`

The chain's terminal done receipt records artifact SHA-256
`f9445b300f55b183ddffce319d92e34a4a33e19c496d391d58806ac0cfa8abea`.

The current live file `docs/ask-answer-funnel-unit-1-explicit-key-20260907.md` hashes to
`55635a2cf21060056c31072b634ed6d2bb5a9746e7ba90f885f79085c8c06b04`.

Disposition: typed evidence-integrity block. Unit 1 remains terminal done according to the task
ledger, but the receipt cannot be independently reconciled to the current bytes. Historical bytes
matching the done hash must be recovered from an immutable backup/snapshot, or the lifecycle must
be explicitly superseded by the owning ledger workflow. The chain JSON must not be hand-edited.

No completion claim is changed by this disposition, and no artifact bytes were overwritten.
