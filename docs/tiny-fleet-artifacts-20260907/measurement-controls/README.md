# Tiny-fleet measurement controls — 2026-09-07

This is the recorded pilot for the expanded measurement ladder. It is an offline
replay over immutable `lte-workstation` snapshots, not a claim of a clean or
general architectural effect.

## Artifacts

- `raw/manifest.json` — every included/excluded file row and token counts for both snapshots.
- `metrics/evaluator.json` — provenance, structural/lexical ladder, JSD, and arm statuses.
- `metrics/uncertainty.json` and `metrics/uncertainty.tsv` — deterministic 2,000-draw bootstrap intervals.
- `controls/control-results.json` — repeatability, path-order, polarity, mutation, leakage, and conditioning controls.
- `preflight/preflight.json` — dependency/resource preflight with the LoRA/QLoRA block.

The evaluator returned exit code 2 because the leakage control found six duplicate
blobs in snapshot B. That failure is retained as evidence; it is not converted to a
green result. The prompt-only arm is `control-only`, and the genuine LoRA/QLoRA arm
is `blocked` because `torch`, `transformers`, and `peft` were absent. No Modelfile,
prompt, or base-model output is substituted for a weight-update result.

## Replay

```bash
tmp=$(mktemp -d)
mkdir "$tmp/a" "$tmp/b"
git archive 54758160 | tar -C "$tmp/a" -xf -
git archive HEAD | tar -C "$tmp/b" -xf -
sha=$(sha256sum "$tmp/b/scripts/mesh-tiny-fleet" | awk '{print $1}')
scripts/mesh-tiny-fleet-evaluate \
  --snapshot-a "$tmp/a" --snapshot-b "$tmp/b" \
  --commit-a 5475816081b26a0f9aebb92da844493b19304eef \
  --commit-b e8f47364e5a0f224c1bd03331df592272a187df5 \
  --protocol docs/tiny-fleet-protocol.md \
  --mutation-file scripts/mesh-tiny-fleet --mutation-sha256 "$sha" \
  --output /tmp/tiny-fleet-evaluator.json \
  --raw-manifest /tmp/tiny-fleet-raw.json \
  --uncertainty-output /tmp/tiny-fleet-uncertainty.json \
  --controls-output /tmp/tiny-fleet-controls.json
```

Expected: evaluator exit `2`, mutation/path-order/polarity/repeatability pass,
leakage fail, prompt-only `control-only`, and LoRA/QLoRA `blocked`.
