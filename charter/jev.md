# jev — TypeSafe exploration window

goal: test Jev as bounded mesh decision support, with transient detectors and reality-checked outcomes
progress: find /home/mesh-home/.mesh/evidence -maxdepth 1 -name 'typesafe-jev-*.md' -newermt 'today' | wc -l | sed 's/$/ Jev evidence artifacts today/'
duty: queue-tend

Engine: omp (gpt-5.6-luna, medium effort).

**Scope.** Explore Jev through redacted, bounded fixtures; compare detector signals with observed mesh reality; keep model output advisory. Code, ownership, safety, and delivery gates remain authoritative.

**Evidence.** Every run records the fixture shape, model/version, typed answers, probabilities, token use, latency, secret scan, side-effect status, and the final reality verdict under `/home/mesh-home/.mesh/evidence/`. Malformed inputs must fail closed.

**Landing.** Changes use the repository's normal review and landing path. Keep operator Telegram duties in `tg`; this window reports durable progress to the board. Do not edit `scripts/mesh-restore` from this exploratory lane; reboot-persistent staffing requires a separately owned mesh-restore task.
