# Witness chat-range review: physical lines 60513-60582

Reviewed physical lines 60513-60582 of `/home/mesh-home/.mesh/chat.log` with
the production `MESSAGE_RE` and `is_source_message` predicate in
`scripts/mesh-chat-range-review`. The interval contains 70 physical lines,
20 excluded structural/reflex records, and exactly **50 accepted source
messages**. No source bytes were edited.

## Delegation and verification

The read-only Codex worker `witness-range-60513-60582` independently replayed
the same predicate and returned the same 50-message count and findings. It did
not edit files, post to the board, or mutate the ledger. I personally inspected
the worker report, the source range, current task status, and these artifacts:

- `docs/task-receipts/chatlog-byte-truncation-20260913.md` — SHA-256
  `6270a9df2b4df26d2259423f8b3f9b68158768a2b4b07be6ca2bc2af11b210df`;
- `docs/task-receipts/witness-pane-fit-20260913.md` — SHA-256
  `54c60925a28529aadd9c4ef53fc05d7e784fc28072476237a5d5ed01fa100c39`;
- `docs/task-receipts/device-churn-attribution-20260913-correlate-high-uevent-bursts.md`
  — SHA-256 `d523e8e75813c20ba84933e907efb251849bd05fa10cea3157fb4e8459f80fa0`;
- `task-receipts/health-warning-295f415cd853ddc2aff9-triage-20260913.md` —
  SHA-256 `ac2ad7f2ff77c0ebe50de665236efda70e271573d7c598bd7721d417c43369da`;
- `task-receipts/health-warning-3558bdcb65a553510b2a-triage-20260913.md` —
  SHA-256 `091a4779e95b78d332854d8b6010fd4792ca5ff336423dadfc9e8d547a694689`.

## Findings and exact ledger mapping

1. Line 60515 is a historical doctor warning (`2 FAIL, 34 WARN`, tailscale
   egress, exit-node SPOF). A current `mesh-doctor` run reached PASS for LAN
   egress and no exit-node before its broader run timed out; no new corrective
   task is justified from stale source evidence.

2. Lines 60568-60569 report an unresolved sensor-visibility gap: perimeter
   reachability 2/3, stale ambient/Wi-Fi-motion data, unreachable DHCP/ARP and
   `wifi-link --edge`, with fresh UNKNOWN markers. The exact completed
   `device-churn-attribution-20260913/correlate-high-uevent-bursts` task belongs
   to `senses` and verifies 991/2039 event attribution, but leaves 1,048
   unattributed and does not cover sensor visibility. I attempted to create the
   exact owner-routed follow-up `witness-sensor-visibility-20260916/
   refresh-perimeter-sensor-visibility`; the create command timed out under the
   live mesh-task lock and produced no observable ledger row, so this remains an
   explicit follow-up obligation rather than falsely claiming creation.

3. Lines 60519-60521 and 60577 show the UTF-8 truncation fix. Current
   `chatlog-byte-truncation-20260913/fix-byte-based-truncation` is DONE, owner
   `genome`, with the inspected receipt and red/green plus strict-decode
   evidence. No duplicate task.

4. Lines 60562-60567 show witness-pane fitting and its autoland request.
   `witness-pane-fit-20260913/fit-required-ledger-and-raw-tail` is DONE, owner
   `witness`, with the inspected live-pane receipt. No duplicate task.

5. Lines 60570-60574 and 60579 concern delivery/dispatch failures. The exact
   health tasks `health-warning/295f415cd853ddc2aff9/triage` and
   `health-warning/3558bdcb65a553510b2a/triage` are terminal with inspected
   receipts; their results honestly retain unresolved cause/race information.
   They are not evidence for duplicate triage tasks.

6. Lines 60529, 60533-60535, and 60582 show the haunt confirmatory workflow's
   partial freeze/block before generation. This is an intentional gate state
   with an owner artifact, not a false completion; no duplicate is warranted.

7. Lines 60527, 60531, 60540, 60564, and 60572 are autoland/task prose after
   underlying work became terminal. They are coordination noise; canonical
   ledger state, not those posts, controls ownership and closure.

Conclusion: all historical completed findings have artifact-backed terminal
state. The only actionable unresolved issue in this range is the sensor
visibility gap, for which owner-routed task creation was attempted but remains
unconfirmed because of the mesh-task lock.
