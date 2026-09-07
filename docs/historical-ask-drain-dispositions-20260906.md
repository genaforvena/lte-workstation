# Historical ask drain — disposition record

This artifact discharges the 191 source-backed historical asks enumerated in
`~/.mesh/evidence/historical-ask-drain-20260906.tsv`. Each source timestamp has
one corresponding row in `docs/historical-ask-decisions-20260906.tsv`; the
ledger is regenerated from that decision table by
`scripts/mesh-historical-ask-ledger`.

The audit is deliberately conservative. `DESIGN` means that the request has a
concrete direction, but its target or required side effect is outside this
checkout (external repository, service, device, private communication, or
research/product decision). It cites this per-row disposition artifact rather
than pretending that a design or acknowledgement is a landed implementation.
`DECLINED` means the source is an acknowledgement, correction, ambiguous
remark, transcription/music artefact, or an external side-effect request with
no safe repository artifact to land. No row is closed from a TG reply alone.

The three initial rows retain their more specific artifacts; all remaining
rows are listed individually in the decision table, with no bulk-close rule.
