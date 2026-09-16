# Wake release publish readiness — 2026-09-16

## Result

PASS for local release-policy readiness. No upload was performed. The operator-owned Hugging Face
push remains the only publication step.

## Verification

Repository: `/home/mesh-home/finnegans-fake`

Commands run:

```bash
jq 'to_entries[] | {repo:.key, share:.value.share, source:.value.source,
   verified:.value.verified}' release/MANIFEST.json
/home/mesh-home/.venv-ai/bin/python wake/push_release.py --owner wake --dry-run
sha256sum release/MANIFEST.json README.md wake/push_release.py
test -f docs/task-receipts/wake-release-publish-readiness-20260916.md
```

The manifest contains five entries. Four are `share=public` and are selected by the dry-run:

```text
upload  wake/finnegans-fake-char257               PUBLIC  43.8 MB
upload  wake/english-char257                      PUBLIC  43.8 MB
upload  wake/finnegans-fake-bpe4096               PUBLIC  49.5 MB
upload  wake/finnegans-fake-lora-qwen3.5-0.8b     PUBLIC  71.1 MB
```

The fifth entry is `finnegans-fake-folds-lora`, `share=local`, sourced from `fold-lora-47/ep3`.
The uploader prints `REFUSED ... share=local — trained on the internal board log` and refuses it
before any upload path. The command ends with `--dry-run: nothing was uploaded`.

Recorded hashes after the README update:

```text
release/MANIFEST.json  791ada010eb5c28d60ac39c1be82fd1c798d642a818184774382a3d28dcc186d
README.md              615d16c47e589cd9f822cf2bdf68c5bcb778a208af5c0991348d2d97354c4b9c
wake/push_release.py   4043138802a5f5542b839c43ad475a307c4b448f20ad678b1ef1b5212fcbb323
```

README now records the four public destinations, the internal-log refusal, the no-upload result,
and links to this receipt.
