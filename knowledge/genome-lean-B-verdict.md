# GENOME-LEAN B: verdict — 8 unwired scripts — 2026-06-11T15:20Z

Classified by planner (gemini was stacked behind the sanitizer task). Evidence: live
process table, callers grep (scripts/ docs/ cron systemd), log activity, doctrine.

## Verdicts

| # | Script | Evidence | Verdict |
|---|--------|----------|---------|
| 1 | mesh-since | codex reality-verified earlier today; landed 2a121da | **KEEP** (canon: on-return brief — "what changed while away") |
| 2 | mesh-textin | RUNNING now (2 bash instances); routed operator text today (textin.log 15:08:19 WOKE steward); core of "text over any channel" doctrine | **KEEP-WIRED** (runtime-launched; ⚠ 2 instances — possible duplicate, flagged to check-stream) |
| 3 | mesh-tg-recv | built for the ds-can't-reach-telegram era (per its own header); mesh-voice-rx is the live receiver (python3 process up, voice-in.log active today); no callers/cron | **SUPERSEDED** by mesh-voice-rx + mesh-textin |
| 4 | mesh-transcribe | consent-gated continuous transcription; NOT superseded — mesh-hear / mesh-transcribe-organ (the operator's audio-organ split, assigned 2026-06-10 23:22) were never built; only transcription-exercise tool | **KEEP-on-demand** (consent gate mandatory; organ-split task re-queued) |
| 5 | mesh-watch | CLAUDE.md core tooling ("wait on a pane"); called from docs/operating-model.md flows | **KEEP-canon** |
| 6 | mesh-zone | room-zone map from STORED presence logs; overlaps live mesh-presence-fuse (nearest-node zonal) + mesh-presence-trends (history); conflicts with perceive-don't-store | **SUPERSEDED** by presence-fuse/trends |
| 7 | node-join-android.sh | phone onboarding — plantability doctrine (genome must plant new nodes); on-demand by nature | **KEEP-canon** |
| 8 | test-whisper-filter | the 21/21 verification artifact for mesh-whisper-filter (cited in PLAN) | **KEEP** (test) |

## Summary
- KEEP: 6 (since, textin, transcribe, watch, node-join-android, test-whisper-filter)
- SUPERSEDED: 2 (mesh-tg-recv → voice-rx+textin; mesh-zone → presence-fuse/trends)
- DEAD: 0

## Pass-2 running total (A + B + C)
- KEEP: 7 (A) + 6 (B) + 9 (C) = 22
- SUPERSEDED: mesh-health-watch (A), mesh-tg-recv (B), mesh-zone (B)
- DEAD: vpn-hub.py (C)
→ Pass 3 decay commit: git rm 4 files + canon lines into CLAUDE.md tooling section.

## Side-findings
- mesh-textin runs TWICE — verify single-instance invariant (check-stream).
- Operator's audio-organ split (mesh-hear per-node capture + source-agnostic
  mesh-transcribe-organ, consent-gated) was assigned 2026-06-10T23:22Z and never
  built — re-queued to ideas-queue.
