# Erratum — device-churn attribution receipt

This corrects the final Docker-history bullet in
`device-churn-attribution-20260913-correlate-high-uevent-bursts.md` without changing that
artifact, whose SHA-256 is `d523e8e75813c20ba84933e907efb251849bd05fa10cea3157fb4e8459f80fa0` and is
already recorded in the completed task ledger.

Docker history contains 14 container `create` events in the analyzed interval, 13 `die` events, and
13 `destroy` events. `goofy_meninsky` was created at 17:33:28Z and had not died or been destroyed by
the end of the interval. The original wording incorrectly implied every create had a matching
terminal event in the retained range. This count correction does not change the interval event
counts, the 991/2,039 stream-to-counter overlap, or the bounded attribution: Docker veth lifecycle
is a strong contributor, while per-container veth ownership and the remaining count are unresolved.
