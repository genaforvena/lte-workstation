# Health warning triage: genome delivery age expiry (2026-09-13)

Investigated `health-warning/ffb9f31d590df05068ad/triage` for message
`1a093928349119f1`, a witness-to-genome FYI first seen at `12:08:17Z` and
terminally failed at `12:24:04Z` after 946 seconds. The delivery ledger records
`attempts=0`, `status=failed`, `terminal_reason=age-expiry`, and
`failure_emitted=true`; `~/.mesh/chat-deliver.log` confirms the age and window
`5964340`.

The FYI corrected the queue-frontier report and pointed genome to its existing
priority-90 resolver, `unblock/genome/95aa703598b7c325/resolve`. The canonical
task ledger still reports that resolver open and owned by genome. The adjacent
failures `60c7578acd32d20c` and `1e9e490a3eb985dc` are also zero-attempt
age-expiries in the preceding minutes. This repeated pattern is consistent
with genome's pane remaining busy, but zero attempts cannot distinguish an
idle-gate rejection from a failed `mesh-tell`; it does not establish the exact
cause over the full age window.

Disposition: retain the terminal records and do not replay the FYI or change
delivery policy from this evidence. The failure is real and the recipient's
resolver remains open; no source or substrate change was indicated by this
triage. A future diagnostics task should record busy-gate rejections separately
from send attempts so the zero-attempt case can be resolved.
