# senses — the sensorium

goal: держать сенсориум честным: каждый датчик отдаёт живой артефакт либо признаётся слепым

Engine: opencode. This window owns the perception lane: the sensors themselves, their `--test`
gates, and the fused state derived from them.

**Perception is re-observed live, never stored** — it decays on reboot by design.

**Honest fusion:** an unreachable input renders UNKNOWN/partial, never a faked all-clear. A
reachable organ whose driver returns empty is a HOLLOW sense — cron-green while its artifact goes
stale — so a sensor's `--test` must assert a real hardware read, not just the offline classifier.

Its data pane carries fused perception (`mesh-dash sense`); if this window keeps re-running the
same probe every turn, that signal belongs on top.
