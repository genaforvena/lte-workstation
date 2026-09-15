# Record-button design audit — 2026-09-12

Task: `design-spec-task-sweep-20260907/audit-record-button` (owner `tg`).
Source ask: `20260821T004511Z`, from `~/.mesh/voice-in.log` at 2026-08-21T00:45:11Z.

## Finding

The 2026-09-06 design note is stale as a disposition. Its statement that the
target repository is absent is true only of the `lte-workstation` checkout. The
application exists at `/home/mesh-home/grainneukeln`, and the original ask was
implemented, pushed, and reported to the operator. The ask should be treated as
delivered; the native APK is a separately and explicitly deferred decision.

Evidence for delivery:

- The source asks for a live record action, using the phone to control the
  application, and making the captured source available to Grainne Keln.
- Board records report the capture and phone pult landing in `grainneukeln`
  (`97e0ed6`, `41cec0a`), followed by recording-button/e2e fixes (`5604f3f`)
  and additional follow-up (`ed0b9d6`). The witness closure at
  `~/.mesh/chat.log:17075` explicitly links those commits to
  `ask:20260821T004511Z` and says the operator was told on Telegram.
- The repository is currently at `3f3826da79aa73cd2e8eda64806ac3dab745e50e`
  on `master`, equal to `origin/master`; both `5604f3f` and `41cec0a` are
  ancestors of that tip. The app has `capture/mic.py`, a mobile pult, and the
  human-key end-to-end script `tests/tui-record-e2e.sh`.
- `~/.mesh/chat.log:16742-16743` records the feature and final suite result;
  `~/.mesh/chat.log:16858` records the later real-keyboard e2e repair and push.
  `~/.mesh/chat.log:28548` records the historical ask answer, and
  `~/.mesh/chat.log:28838` is the later design-only classification that missed
  the already-existing delivery evidence.

## Gates and remaining decision

The product currently offers a phone-installable web pult. Its README says
`APK later` and explicitly limits the pult to LAN use: no TLS or rate limiting,
and do not port-forward it. Preserve that boundary. No APK build/sign/distribution
work and no remote-exposure changes are authorized by this historical ask after
the explicit deferral.

I created the owner-`tg` follow-up plan
`docs/plans/2026-09-12-record-button-deferred-decision.tsv` and task chain
`grainneukeln-phone-apk-deferral-20260912/reopen-native-apk-only-on-operator-ask`.
It is meant to remain blocked on a fresh operator request before any native APK
work. The immediate `mesh-task block` attempt was refused because the new step
must first be claimed. After this audit settled, canonical dispatch placed
`design-audit-task-sweep-20260907/design-audit-job-and-sync` ahead of the new
row; that first row passed `mesh-task check dispatch` (exit 0). The new row is
left open for its turn in dispatch order, where it can be taken and immediately
blocked on operator input.

## Verification and limit

- Read-only Git checks: `HEAD == origin/master`; `5604f3f` and `41cec0a` are
  ancestors of `HEAD`; the feature source and e2e script are present.
- Focused pytest attempt (`capture/test_mic.py`, `tui/test_record.py`,
  `pult/test_server.py`) did not run: this node's `/usr/bin/python3` has no
  `pytest` module. No test pass is claimed. The prior board completion reports
  the feature suite and e2e evidence; this audit did not rerun the physical-key
  tmux test.
- No source files in `grainneukeln` were edited. Its existing untracked shell
  scripts were left untouched.
