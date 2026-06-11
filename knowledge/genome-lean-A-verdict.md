# GENOME-LEAN A: verdict — 8 unwired scripts — 2026-06-11T14:50Z

Node: imozerov-IdeaPad-3-15IIL05

## Verdicts

| # | Script | Parse | --test | Unwired? | Verdict | Why |
|---|--------|-------|--------|----------|---------|-----|
| 1 | mesh-browse | PY OK | none | yes (no cron/supervise) | **KEEP** | Only browser organ (Playwright) — JS-rendered page reads + browser automation. Irreplaceable sense+actuator. |
| 2 | mesh-exit | OK | none | yes | **KEEP** | Only consumer-side exit-node flipper with DMS auto-revert. Safety-gated (refuses on offering node). mesh-fix-egress is the offering side; this is the consumer side — complementary, not overlap. |
| 3 | mesh-eye | OK | none | yes | **KEEP** | Only consent-gated ambient sensing (camera→light, mic→sound signals, local extraction only). mesh-organs verifies hardware exists; mesh-eye DOES the sensing. Privacy-by-construction (no media kept). |
| 4 | mesh-health-watch | OK | none | yes | **SUPERSEDED** | Function fully covered by mesh-session-watchdog lines 72–96 (same edge-triggered health FAIL/PASS tracking with chat alerts). Health-watch is a thinner wrapper: only health; watchdog covers health + blocked-mind + service restart. TG-alert gap (health-watch alerts TG, watchdog only chat) — if needed, add TG to watchdog, not keep a separate script. |
| 5 | mesh-local-mind | OK | none | yes | **KEEP** | Only local-inference primitive (ollama). Geo-block-immune, used by mesh-plan for ask_mind(). Strategic for air-gapped/blocked scenarios. |
| 6 | mesh-neighbour-watch | OK | OK (pass) | yes | **KEEP** | Only tool that probes peer SSH liveness + offers auto-restore. mesh-health checks reachability+internet; mesh-mind-watch checks mind liveness; neither probes SSH. Fills a specific gap. |
| 7 | mesh-review | OK | none | yes | **KEEP** | Only multi-engine blind verification (gemini+opencode+claude, fresh-context, independent). Steward's review side. Unique adversarial pattern. |
| 8 | mesh-session-watchdog | OK | OK (pass) | **NO — in supervise.list** (active) | **KEEP** | Already wired via supervisor. Comprehensive: blocked-mind detection, service restart, mesh-health edge-triggered integration. Backbone of node self-awareness. |

## Summary

- **KEEP-on-demand**: 7 scripts (browse, exit, eye, local-mind, neighbour-watch, review, session-watchdog)
- **SUPERSEDED**: 1 script (health-watch — by session-watchdog's health integration)
- **DEAD**: 0

All 8 parse clean. Only neighbour-watch and session-watchdog have --test; both pass. Session-watchdog is already supervised (9th entry in supervise.list); the other 7 are truly unwired (no cron, no supervisor).

## Canon lines for CLAUDE.md tooling list (KEEP scripts only)

```
mesh-browse          | browser organ (Playwright) — sense (read page) + actuator (click/type/fill)  | ad-hoc, on mind's demand
mesh-exit            | consumer-side exit-node flipper with DMS auto-revert                         | operator/steward, not cron
mesh-eye             | consent-gated ambient sensing (camera→light, mic→sound, local only)          | on demand (consent required)
mesh-local-mind      | local LLM inference via ollama (geo-block-immune)                            | called by mesh-plan, minds
mesh-neighbour-watch | peer SSH+session liveness probe + optional restore                           | steward, not cron
mesh-review          | multi-engine blind independent verification (gemini+opencode+claude)         | steward review stage
mesh-session-watchdog| session watchdog (blocked-mind detect, service restart, health integration) | supervised (active)

# SUPERSEDED (can be git rm'd):
# mesh-health-watch -> mesh-session-watchdog lines 72-96 cover health edge-triggered monitoring
```
