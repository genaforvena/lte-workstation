# Dev.to reply-alert classification review — 2026-09-14

Task: `pub-reply-alert-review-20260914/reconcile-3ef25-alert` (owner `pub`).
Capture time: 2026-09-14T07:23Z.

## Finding

The repeated `devto-reply-3ef25` board alert calls an unanswered thread “reply owed,” although
the current pub comment sweep classifies the comment as promotional and explicitly says not to
reply. A fresh read-only `mesh-devto-reply --owed --json` returned `3ef25` again, with the text
offering “Secure API endpoints” and a short URL. The same live result included the other three
comments the sweep classified as promotional: `3ekc9`, `3ekdf`, and `3eoo9`.

This is a labeling/actionability defect in the other window’s tool path. In
`scripts/mesh-devto-reply`, `owed_tips()` at lines 142–163 selects by author identity and whether
the branch contains an operator reply; it does not assess whether the message merits a reply.
The escalation builder at lines 339–350 turns every selected row into a `[task] ... reply owed`
alert owned by `mesh-devto-reply/pub`. The repeated board notice is therefore consistent with the
selector, but not with the pub channel’s human reply obligation. No code was changed here, and no
public reply was posted.

## Evidence

- Completed sweep receipt: `docs/task-receipts/pub-comment-sweep-20260914.md`, SHA-256
  `07aefe3bfb2043ce125068bd144182dba6faf256bd7937c8200b03a7dc1adebe`. It records comment
  `3ef25` (and `3ekc9`, `3ekdf`, `3eoo9`) as promotional, with no reply due.
- Fresh read-only command: `mesh-devto-reply --owed --json`, output captured at
  `/tmp/pub-reply-owed-20260914.json`, SHA-256
  `375303b69ecea7e1fcb9dc85ebfbbb5f46225904da87eadb348805fe635f3bd4`.
- Board history: `mesh-chat --history 'devto-reply-3ef25' 20`, captured at
  `/tmp/pub-reply-alert-board-20260914.txt`, SHA-256
  `fa7bb4f32fad337f20a40ee996e61250b425b976c12f9a3a642b6865728bb31d`. It contains eight
  escalations from 2026-09-10T03:23:33Z (`x1`) through 2026-09-14T06:23:34Z (`x8`), all with
  the same message ID `2dba721b-e0d1-495b-884c-48ec15de4687`.
- Tool source SHA-256: `8f141f10199205de8f42692714e354b5825b56c83d5797d3cb83a2a6211a55d9`;
  last source commit: `adafc2e5f499eeb7c75794b18e0225a134ab0fe8` (2026-08-20). The source was
  clean in the worktree at capture. The sweep receipt is untracked in this restored WIP and was
  preserved as found.

## Disposition

Flag the mismatch for the owning tool window to review. Leave the tool unchanged here. Do not
draft or post a reply to `3ef25`; the comment is promotional and the channel’s outgoing voice is
human-facing.
