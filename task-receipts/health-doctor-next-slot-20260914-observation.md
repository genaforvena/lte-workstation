# Natural doctor cron observation — 2026-09-14


This observer does not invoke, signal, or attach to mesh-doctor.


### 03:00Z preflight 2026-09-14T03:00:00+00:00
lock-file: present
lock-holder:
(none reported)
doctor-process: none
doctor.log mtime=2026-09-14T02:23:01.676306+00:00 size=5563724
doctor.log tail:
2026-09-14T01:23:01Z  [33mWARN[0m topology leak: mesh-vpn-node-watch:100.94.116.17 (hardcoded IP — use env var / config instead)
2026-09-14T01:23:01Z  [33mWARN[0m topology leak: mesh-watchtower:100.94.116.17 (hardcoded IP — use env var / config instead)
2026-09-14T01:23:01Z  mesh-doctor: 2 FAIL, 34 WARN | serial-confirm 0/161 assessed, 17 FAIL(stale), 161 stale-verdict
mesh-doctor: skipped — another automated doctor holds /home/mesh-home/.mesh/.doctor.lock


Wired entry: 32:23 * * * * $HOME/.local/bin/mesh-doctor --cron >> $HOME/.mesh/doctor.log 2>&1   # autowired 2026-07-14

### natural invocation sample 2026-09-14T03:23:02+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  754744: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  754755: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  754759: 0 curl curl -s -m8 -o /dev/null -w %{http_code} https://api.anthropic.com/v1/messages
doctor pid=754744 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  754744: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  754755: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  754759: 0 curl curl -s -m8 -o /dev/null -w %{http_code} https://api.anthropic.com/v1/messages
doctor pid=754755 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  754755: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  754759: 0 curl curl -s -m8 -o /dev/null -w %{http_code} https://api.anthropic.com/v1/messages
doctor.log mtime=2026-09-14T03:23:02.037600+00:00 size=5563900
doctor.log tail:
2026-09-14T01:23:01Z  mesh-doctor: 2 FAIL, 34 WARN | serial-confirm 0/161 assessed, 17 FAIL(stale), 161 stale-verdict
mesh-doctor: skipped — another automated doctor holds /home/mesh-home/.mesh/.doctor.lock
2026-09-14T03:23:01Z  [31mFAIL[0m egress rides tailscale0 (overlay/VPN) — should be LAN
2026-09-14T03:23:01Z  [31mFAIL[0m exit-node set (n2sbt7yy6t11CNTRL) — SPOF risk

### 30-second sample 2026-09-14T03:23:02+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  754744: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  754755: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  754759: 0 curl curl -s -m8 -o /dev/null -w %{http_code} https://api.anthropic.com/v1/messages
doctor pid=754744 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  754744: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  754755: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  754759: 0 curl curl -s -m8 -o /dev/null -w %{http_code} https://api.anthropic.com/v1/messages
doctor pid=754755 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  754755: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  754759: 0 curl curl -s -m8 -o /dev/null -w %{http_code} https://api.anthropic.com/v1/messages
doctor.log mtime=2026-09-14T03:23:02.037600+00:00 size=5563900
doctor.log tail:
2026-09-14T01:23:01Z  mesh-doctor: 2 FAIL, 34 WARN | serial-confirm 0/161 assessed, 17 FAIL(stale), 161 stale-verdict
mesh-doctor: skipped — another automated doctor holds /home/mesh-home/.mesh/.doctor.lock
2026-09-14T03:23:01Z  [31mFAIL[0m egress rides tailscale0 (overlay/VPN) — should be LAN
2026-09-14T03:23:01Z  [31mFAIL[0m exit-node set (n2sbt7yy6t11CNTRL) — SPOF risk

### 30-second sample 2026-09-14T03:23:32+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 30 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
doctor pid=836579 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  836579: gone
doctor.log mtime=2026-09-14T03:23:06.408587+00:00 size=5563987
doctor.log tail:
mesh-doctor: skipped — another automated doctor holds /home/mesh-home/.mesh/.doctor.lock
2026-09-14T03:23:01Z  [31mFAIL[0m egress rides tailscale0 (overlay/VPN) — should be LAN
2026-09-14T03:23:01Z  [31mFAIL[0m exit-node set (n2sbt7yy6t11CNTRL) — SPOF risk
2026-09-14T03:23:01Z  [33mWARN[0m mic DEFAULT device broken/busy (use -D plughw:N,M)

### 30-second sample 2026-09-14T03:24:02+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 61 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  889628: 8 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  889630: 8 python3 python3 - /home/mesh-home/lte-workstation/scripts
doctor pid=889628 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  889628: 8 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  889630: 8 python3 python3 - /home/mesh-home/lte-workstation/scripts
doctor.log mtime=2026-09-14T03:23:54.076444+00:00 size=5564458
doctor.log tail:
2026-09-14T03:23:01Z  [31mFAIL[0m exit-node set (n2sbt7yy6t11CNTRL) — SPOF risk
2026-09-14T03:23:01Z  [33mWARN[0m mic DEFAULT device broken/busy (use -D plughw:N,M)
2026-09-14T03:23:01Z  [33mWARN[0m untimed peer-SSH — hangs on a dead peer:mesh-load-audit
2026-09-14T03:23:01Z  [33mWARN[0m 6 bypass(es) of 1 declared sole-path funnel(s) — the rule is recited but the arrangement is broken: librosa-analysis<- mesh-song-verify:94 librosa-analysis<- mesh-song-verify:95 librosa-analysis<- mesh-song-verify:102 librosa-analysis<- mesh-song-verify:109 librosa-analysis<- mesh-song-verify:111 librosa-analysis<- mesh-song-verify:114

### 30-second sample 2026-09-14T03:24:33+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 91 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  908001: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  908447: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  908548: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  909261: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  911151: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  912063: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  912183: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  914728: 28 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  916328: 28 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  918922: 27 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  919072: 27 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  919602: 27 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  919858: 27 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  922697: 26 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  922914: 26 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  923695: 26 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  924422: 26 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  926600: 25 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  928299: 25 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  930963: 24 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  931737: 24 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  933663: 24 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  936756: 23 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  937324: 23 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  937922: 22 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  938134: 22 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  941696: 21 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  942095: 21 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  942502: 21 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  943114: 21 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  945108: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  945385: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  946547: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  948376: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  949052: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  949775: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  950281: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  952479: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  953694: 18 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  958551: 17 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  961127: 16 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  962788: 16 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  963655: 16 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  964028: 15 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  965887: 15 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  971756: 14 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  973768: 13 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  973921: 13 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  974193: 13 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  975033: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-activity-tempo --test
  975053: 12 bash bash /home/mesh-home/.local/bin/mesh-activity-tempo --test
  975164: 12 bash bash /home/mesh-home/.local/bin/mesh-activity-tempo --test
  975433: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-algedonic --test
  975454: 12 bash bash /home/mesh-home/.local/bin/mesh-algedonic --test
  975486: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-ambient-clock --test
  975498: 12 bash bash /home/mesh-home/.local/bin/mesh-ambient-clock --test
  975722: 12 bash bash /home/mesh-home/.local/bin/mesh-ambient-clock --test
  975885: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-approach --test
  975911: 12 bash bash /home/mesh-home/.local/bin/mesh-approach --test
  975993: 12 bash bash /home/mesh-home/.local/bin/mesh-approach --test
  976228: 12 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  976851: 12 bash bash /home/mesh-home/.local/bin/mesh-approach --test
  976853: 12 bash bash /home/mesh-home/.local/bin/mesh-approach --test
  976856: 12 timeout timeout 20 mesh-wifi-motion
  976858: 12 bash bash /home/mesh-home/.local/bin/mesh-wifi-motion
  976965: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-audio-route --test
  976976: 12 bash bash /home/mesh-home/.local/bin/mesh-audio-route --test
  977017: 12 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  977271: 12 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  977530: 11 timeout timeout 20 /home/mesh-home/.local/bin/mesh-autowire --test
  977563: 11 bash bash /home/mesh-home/.local/bin/mesh-autowire --test
  977808: 11 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  977885: 11 timeout timeout 20 /home/mesh-home/.local/bin/mesh-awaydigest --test
  977922: 11 python3 python3 /home/mesh-home/.local/bin/mesh-awaydigest --test
  978071: 11 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  978085: 11 timeout timeout 12 /home/mesh-home/.local/bin/mesh-hire-scan --test
  978104: 11 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --test
  978279: 11 timeout timeout 12 /home/mesh-home/.local/bin/mesh-hire-submit --test
  978311: 11 bash bash /home/mesh-home/.local/bin/mesh-hire-submit --test
  978346: 11 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  978600: 11 bash bash /home/mesh-home/.local/bin/mesh-hire-submit --test
  978608: 11 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --repo trovu/trovu
  979004: 11 timeout timeout 45 mesh-wifiscan --log
  979011: 11 bash bash /home/mesh-home/.local/bin/mesh-wifiscan --log
  979572: 11 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  979576: 11 timeout timeout 20 /home/mesh-home/.local/bin/mesh-ble-recut-arm --test
  979670: 11 bash bash /home/mesh-home/.local/bin/mesh-ble-recut-arm --test
  979732: 11 timeout timeout 12 /home/mesh-home/.local/bin/mesh-homeostasis --test
  979771: 11 bash bash /home/mesh-home/.local/bin/mesh-homeostasis --test
  979986: 11 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  980195: 11 timeout timeout 12 /home/mesh-home/.local/bin/mesh-home-state --test
  980225: 11 bash bash /home/mesh-home/.local/bin/mesh-home-state --test
  980421: 11 bash bash /home/mesh-home/.local/bin/mesh-audio-route --test
  980541: 11 timeout timeout 20 /home/mesh-home/.local/bin/mesh-body-backup --test
  980558: 11 bash bash /home/mesh-home/.local/bin/mesh-body-backup --test
  981059: 10 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  981298: 10 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  981299: 10 timeout timeout 12 /home/mesh-home/.local/bin/mesh-hw-fault-watch --test
  981327: 10 bash bash /home/mesh-home/.local/bin/mesh-hw-fault-watch --test
  981540: 10 timeout timeout 12 /home/mesh-home/.local/bin/mesh-hw-health --test
  981558: 10 bash bash /home/mesh-home/.local/bin/mesh-hw-health --test
  982019: 10 timeout timeout 20 /home/mesh-home/.local/bin/mesh-bruno --test
  982041: 10 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  982046: 10 bash bash /home/mesh-home/.local/bin/mesh-bruno --test
  982256: 10 timeout timeout 20 /home/mesh-home/.local/bin/mesh-bruno-watch --test
  982282: 10 bash bash /home/mesh-home/.local/bin/mesh-bruno-watch --test
  982317: 10 timeout timeout 12 /home/mesh-home/.local/bin/mesh-ideate --test
  982340: 10 bash bash /home/mesh-home/.local/bin/mesh-ideate --test
  982602: 10 timeout timeout 20 /home/mesh-home/.local/bin/mesh-bt-lock-verdict --test
  982614: 10 bash bash /home/mesh-home/.local/bin/mesh-bt-lock-verdict --test
  982721: 10 timeout timeout 20 /home/mesh-home/.local/bin/mesh-budget --test
  982771: 10 bash bash /home/mesh-home/.local/bin/mesh-budget --test
  983105: 10 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  983402: 10 timeout timeout 12 /home/mesh-home/.local/bin/mesh-imac-cam-watch --test
  983431: 10 bash bash /home/mesh-home/.local/bin/mesh-imac-cam-watch --test
  984152: 10 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  984527: 9 timeout timeout 12 /home/mesh-home/.local/bin/mesh-imac-notify --test
  984547: 9 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --test
  984830: 9 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  984942: 9 timeout timeout 20 /home/mesh-home/.local/bin/mesh-card --test
  985001: 9 bash bash /home/mesh-home/.local/bin/mesh-bt-lock-verdict --test
  985027: 9 bash bash /home/mesh-home/.local/bin/mesh-bt-lock-verdict --test
  985028: 9 grep grep -cx 11
  985043: 9 timeout timeout 12 /home/mesh-home/.local/bin/mesh-imac-say --test
  985048: 9 journalctl journalctl --since @1787137200 -o short-iso _TRANSPORT=kernel
  985051: 9 grep grep Opcode 0x0401 failed
  985052: 9 awk awk {split($1,a,"T"); print substr(a[2],4,2)}
  985069: 9 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --test
  985090: 9 bash bash /home/mesh-home/.local/bin/mesh-card --test
  985405: 9 timeout timeout 20 /home/mesh-home/.local/bin/mesh-card-watchdog --test
  985425: 9 bash bash /home/mesh-home/.local/bin/mesh-card-watchdog --test
  985556: 9 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  985578: 9 bash bash /home/mesh-home/.local/bin/mesh-card-watchdog --test
  985806: 9 timeout timeout 12 /home/mesh-home/.local/bin/mesh-imac-wifi --test
  985807: 9 bash bash /home/mesh-home/.local/bin/mesh-hw-health
  985838: 9 bash bash /home/mesh-home/.local/bin/mesh-imac-wifi --test
  985878: 9 timeout timeout 20 /home/mesh-home/.local/bin/mesh-cell-signal --test
  985902: 9 bash bash /home/mesh-home/.local/bin/mesh-card-watchdog --test
  985905: 9 bash bash /home/mesh-home/.local/bin/mesh-ideate --test
  985909: 9 bash bash /home/mesh-home/.local/bin/mesh-cell-signal --test
  985920: 9 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  986121: 9 timeout timeout 20 /home/mesh-home/.local/bin/mesh-claude-deepseek --test
  986123: 9 bash bash /home/mesh-home/.local/bin/mesh-ideate --test
  986174: 9 bash bash /home/mesh-home/.local/bin/mesh-claude-deepseek --test
  986208: 9 bash bash /home/mesh-home/.local/bin/mesh-claude-deepseek --test
  986209: 9 claude /home/mesh-home/.local/bin/claude --permission-mode bypassPermissions -p reply with exactly: deepseek-ok
  987046: 9 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  987266: 9 timeout timeout 12 /home/mesh-home/.local/bin/mesh-interruptibility --test
  987306: 9 timeout timeout 20 /home/mesh-home/.local/bin/mesh-channel-keepalive --test
  987315: 9 bash bash /home/mesh-home/.local/bin/mesh-channel-keepalive --test
  987329: 9 bash bash /home/mesh-home/.local/bin/mesh-interruptibility --test
  987477: 9 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  989134: 8 timeout timeout 20 /home/mesh-home/.local/bin/mesh-chat --test
  989167: 8 bash bash /home/mesh-home/.local/bin/mesh-chat --test
  990627: 8 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  990858: 8 bash bash /home/mesh-home/.local/bin/mesh-hw-health
  990971: 8 timeout timeout 12 /home/mesh-home/.local/bin/mesh-job-apply --test
  991009: 8 python3 python3 /home/mesh-home/.local/bin/mesh-job-apply --test
  991299: 8 timeout timeout 20 /home/mesh-home/.local/bin/mesh-chat-review --test
  991315: 8 bash bash /home/mesh-home/.local/bin/mesh-chat-review --test
  991489: 8 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  991919: 8 timeout timeout 12 /home/mesh-home/.local/bin/mesh-job-ats --test
  991949: 8 python3 python3 /home/mesh-home/.local/bin/mesh-job-ats --test
  992264: 8 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  992582: 8 timeout timeout 12 /home/mesh-home/.local/bin/mesh-job-calls --test
  992606: 8 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  992627: 8 bash bash /home/mesh-home/.local/bin/mesh-job-calls --test
  992796: 7 bash bash /home/mesh-home/.local/bin/mesh-job-calls --test
  992806: 7 bash bash /home/mesh-home/.local/bin/mesh-job-calls --test
  992840: 7 timeout timeout 10 mesh-phone-ip
  992846: 7 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  992856: 7 timeout timeout 12 /home/mesh-home/.local/bin/mesh-job-chatwatch --test
  992903: 7 python3 python3 /home/mesh-home/.local/bin/mesh-job-chatwatch --test
  994370: 7 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  994465: 7 timeout timeout 20 /home/mesh-home/.local/bin/mesh-clear-audit --test
  994499: 7 bash bash /home/mesh-home/.local/bin/mesh-clear-audit --test
  994620: 7 timeout timeout 12 /home/mesh-home/.local/bin/mesh-job-mail --test
  994648: 7 python3 python3 /home/mesh-home/.local/bin/mesh-job-mail --test
  995068: 7 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  995242: 7 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  995381: 7 timeout timeout 12 /home/mesh-home/.local/bin/mesh-job-market-analysis-weekly --test
  995423: 7 python3 python3 /home/mesh-home/.local/bin/mesh-job-market-analysis --test
  995457: 7 bash bash /home/mesh-home/.local/bin/mesh-bruno-watch --test
  995501: 7 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  995579: 7 timeout timeout 12 /home/mesh-home/.local/bin/mesh-job-reply --test
  995586: 7 python3 python3 /home/mesh-home/.local/bin/mesh-job-reply --test
  995620: 7 timeout timeout 12 /home/mesh-home/.local/bin/mesh-job-scan --test
  995643: 7 python3 python3 /home/mesh-home/.local/bin/mesh-job-scan --test
  996008: 7 timeout timeout 20 /home/mesh-home/.local/bin/mesh-closure --test
  996024: 7 bash bash /home/mesh-home/.local/bin/mesh-closure --test
  996139: 6 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  996543: 6 timeout timeout 12 /home/mesh-home/.local/bin/mesh-job-scan-getmatch --test
  996561: 6 python3 python3 /home/mesh-home/.local/bin/mesh-job-scan-getmatch --test
  997211: 6 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  997425: 6 timeout timeout 12 /home/mesh-home/.local/bin/mesh-job-track --test
  997443: 6 python3 python3 /home/mesh-home/.local/bin/mesh-job-track --test
  997529: 6 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  997764: 6 timeout timeout 12 /home/mesh-home/.local/bin/mesh-journal-watch --test
  997789: 6 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --test
  998643: 6 bash bash /home/mesh-home/.local/bin/mesh-imac-wifi
  998672: 6 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  998675: 6 timeout timeout 20 /home/mesh-home/.local/bin/mesh-conversation --test
  998686: 6 bash bash /home/mesh-home/.local/bin/mesh-conversation --test
  998909: 6 timeout timeout 12 /home/mesh-home/.local/bin/mesh-kernel-taint --test
  998949: 6 bash bash /home/mesh-home/.local/bin/mesh-kernel-taint --test
  999388: 5 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  999563: 5 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  999583: 5 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  999584: 5 sed sed s/^$/(none)/
  999596: 5 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  999710: 5 timeout timeout 20 /home/mesh-home/.local/bin/mesh-convexity --test
  999767: 5 bash bash /home/mesh-home/.local/bin/mesh-convexity --test
  999874: 5 npm exec @z_ai/ npm exec @z_ai/mcp-server
  999890: 5 timeout timeout 12 /home/mesh-home/.local/bin/mesh-kill-events --test
  999913: 5 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  999948: 5 bash bash /home/mesh-home/.local/bin/mesh-kill-events --test
  1000210: 5 timeout timeout 12 /home/mesh-home/.local/bin/mesh-knowledge-publish --test
  1000292: 5 bash bash /home/mesh-home/.local/bin/mesh-knowledge-publish --test
  1000300: 5 timeout timeout 20 /home/mesh-home/.local/bin/mesh-cooscillate --test
  1000338: 5 bash bash /home/mesh-home/.local/bin/mesh-cooscillate --test
  1000570: 5 timeout timeout 20 /home/mesh-home/.local/bin/mesh-correlate --test
  1000608: 5 bash bash /home/mesh-home/.local/bin/mesh-correlate --test
  1000643: 5 node [node]
  1000664: 5 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1000846: 5 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  1000871: 5 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  1000911: 5 timeout timeout -k 2 8 mesh-imac-notify --probe
  1000939: 5 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --probe
  1001016: 5 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --probe
  1001023: 5 timeout timeout 12 /home/mesh-home/.local/bin/mesh-labor --test
  1001101: 5 bash bash /home/mesh-home/.local/bin/mesh-labor --test
  1001490: 5 timeout timeout 25 ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=accept-new ilya@192.168.8.214 sh -s
  1001527: 5 ssh ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=accept-new ilya@192.168.8.214 sh -s
  1001589: 5 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1001842: 5 bash bash /home/mesh-home/.local/bin/mesh-convexity --test
  1001867: 5 bash bash /home/mesh-home/.local/bin/mesh-convexity --test
  1001926: 5 python3 python3 -
  1001934: 5 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1002198: 5 bash bash /home/mesh-home/.local/bin/mesh-hh-drive --goto https://hh.ru/applicant/negotiations
  1002240: 5 timeout timeout 12 /home/mesh-home/.local/bin/mesh-land --test
  1002282: 5 bash bash /home/mesh-home/.local/bin/mesh-land --test
  1002692: 5 sleep sleep 8
  1002715: 5 mesh-tg-user [mesh-tg-user]
  1003507: 4 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1003745: 4 timeout timeout 12 /home/mesh-home/.local/bin/mesh-lan-jitter --test
  1003814: 4 bash bash /home/mesh-home/.local/bin/mesh-lan-jitter --test
  1003970: 4 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1004151: 4 bash bash /home/mesh-home/.local/bin/mesh-conversation --test
  1004218: 4 timeout timeout 20 /home/mesh-home/.local/bin/mesh-criticality --test
  1004220: 4 bash bash /home/mesh-home/.local/bin/mesh-criticality --test
  1004288: 4 timeout timeout 12 /home/mesh-home/.local/bin/mesh-lan-newdevice --test
  1004293: 4 bash bash /home/mesh-home/.local/bin/mesh-labor --feed
  1004331: 4 bash bash /home/mesh-home/.local/bin/mesh-lan-newdevice --test
  1004502: 4 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1004566: 4 bash bash /home/mesh-home/.local/bin/mesh-criticality --test
  1004609: 4 bash bash /home/mesh-home/.local/bin/mesh-hh-drive --goto https://hh.ru/search/vacancy?text=team%20lead%20Go&page=0&order_by=publication_time&search_field=name&search_field=description&items_on_page=50
  1004613: 4 python3 python3 -
  1004627: 4 timeout timeout 20 /home/mesh-home/.local/bin/mesh-cron-catchup --test
  1004656: 4 sleep sleep 5
  1004676: 4 python3 python3 /home/mesh-home/.local/bin/mesh-cron-catchup --test
  1004840: 4 timeout timeout 12 /home/mesh-home/.local/bin/mesh-lan-presence --test
  1004868: 4 bash bash /home/mesh-home/.local/bin/mesh-lan-presence --test
  1004983: 4 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1005105: 4 timeout timeout 20 /home/mesh-home/.local/bin/mesh-cstate --test
  1005125: 4 bash bash /home/mesh-home/.local/bin/mesh-autowire --test
  1005129: 4 bash bash /home/mesh-home/.local/bin/mesh-autowire --test
  1005131: 4 awk awk -F \t $4 == "tool" && $5 == "install" { print $1 }
  1005157: 4 bash bash /home/mesh-home/.local/bin/mesh-cstate --test
  1005227: 4 sleep sleep 8
  1005372: 4 timeout timeout 12 /home/mesh-home/.local/bin/mesh-leadlag --test
  1005406: 4 bash bash /home/mesh-home/.local/bin/mesh-leadlag --test
  1005428: 4 timeout timeout 20 /home/mesh-home/.local/bin/mesh-dash --test-fast
  1005470: 4 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1005519: 4 bash bash /home/mesh-home/.local/bin/mesh-dash --test-fast
  1005626: 4 bash bash /home/mesh-home/.local/bin/mesh-light --test
  1005783: 4 timeout timeout 12 /home/mesh-home/.local/bin/mesh-lease --test
  1005823: 4 bash bash /home/mesh-home/.local/bin/mesh-dash --test-fast
  1005833: 4 bash bash /home/mesh-home/.local/bin/mesh-lease --test
  1006080: 4 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1006169: 4 sleep sleep 5
  1006276: 4 bash bash /home/mesh-home/.local/bin/mesh-cell-signal --test
  1006312: 4 bash bash /home/mesh-home/.local/bin/mesh-cell-signal --test
  1006349: 4 bash bash /home/mesh-home/.local/bin/mesh-cell-signal --test
  1006361: 4 bash bash /home/mesh-home/.local/bin/mesh-leadlag --test
  1006369: 4 bash bash /home/mesh-home/.local/bin/mesh-peer-addr Redmi
  1006370: 4 python3 python3 -
  1006407: 4 timeout timeout 12 /home/mesh-home/.local/bin/mesh-ledger --test
  1006447: 4 bash bash /home/mesh-home/.local/bin/mesh-ledger --test
  1006631: 4 sleep sleep 5
  1006795: 3 sleep sleep 5
  1006933: 3 sleep sleep 5
  1007139: 3 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1007250: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-devcd-catch --test-fast
  1007311: 3 bash bash /home/mesh-home/.local/bin/mesh-devcd-catch --test-fast
  1007433: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-device-churn --test
  1007478: 3 bash bash /home/mesh-home/.local/bin/mesh-device-churn --test
  1007543: 3 bash bash /home/mesh-home/.local/bin/mesh-imac-cam-watch --test
  1007545: 3 bash bash /home/mesh-home/.local/bin/mesh-imac-cam /tmp/tmp.NTTk7NXyOO/td.mesh-imac-cam-watch/imac-cam-now-Otxs.jpg
  1007581: 3 timeout timeout 12 /home/mesh-home/.local/bin/mesh-link-flap --test
  1007618: 3 bash bash /home/mesh-home/.local/bin/mesh-link-flap --test
  1007726: 3 ssh ssh -o StrictHostKeyChecking=no -o ConnectTimeout=8 ilya@100.121.88.110 grep -qiE '^[[:space:]]*camera[[:space:]]*=[[:space:]]*(yes|true|1)' ~/.mesh/consent 2>/dev/null
  1008385: 3 piper /home/mesh-home/.mesh/piper/piper/piper -m /home/mesh-home/.mesh/piper/voices/ruslan.onnx -f /tmp/tmp.NTTk7NXyOO/td.mesh-conversation/conv-tts-test-Yrn0.wav
  1008414: 3 bash bash /home/mesh-home/.local/bin/mesh-labor --feed
  1008425: 3 bash bash /home/mesh-home/.local/bin/mesh-labor --feed
  1008441: 3 bash bash /home/mesh-home/.local/bin/mesh-ledger --price-window 5
  1008542: 3 sleep sleep 5
  1008732: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-digest --test
  1008766: 3 bash bash /home/mesh-home/.local/bin/mesh-digest --test
  1008920: 3 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1009043: 3 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --test
  1009047: 3 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --scope
  1009141: 3 bash bash /home/mesh-home/.local/bin/mesh-spend --tokens --json
  1009143: 3 bash bash /home/mesh-home/.local/bin/mesh-ledger --price-window 5
  1009172: 3 bash bash /home/mesh-home/.local/bin/mesh-digest --test
  1009180: 3 bash bash /home/mesh-home/.local/bin/mesh-digest
  1009307: 3 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --scope
  1009309: 3 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --scope
  1009310: 3 awk awk -F\t -v idcap=4 -v sfloor=0.90 -v minsig=8 -v fminsig=4        # FAMILY SKELETON — the message with every VARIABLE token dropped: a family is the set of signatures       # that are the same sentence differing only where the message carries a value. Two properties earn it:       #   - it is computed from the RAW message, NEVER the normalized one. After normalize() a digit-derived       #     N is indistinguishable from a literal N (`Network`, `HNC`), so keying on the normalized text       #     would drop real words and merge unrelated messages. The raw still has actual digits.       #   - it drops variable tokens rather than taking a leading PREFIX. A prefix rule was tried first and       #     measured FALSE against the live journal here (2026-08-28): every rtw_8822bu 1-3:1.0 line begins       #     with a digit-bearing word, so seven genuinely DIFFERENT driver faults (leave idle state failed,       #     h2c queue mismatch, failed to configure mac, ...) all landed in one catch-all bucket and were       #     reported as a storm. They are seven real faults, correctly given seven signatures. Under the       #     skeleton they have seven distinct skeletons and no family fires.       function famkey(ident, raw,   i, w, nw, out) {         nw = split(raw, w, /[ \t]+/); out = ""         for (i=1; i<=nw; i++) {           if (w[i] ~ /[0-9]/) continue                 # carries a value -> not part of the skeleton           out = (out=="" ? w[i] : out " " w[i])         }         if (out == "") out = "<all-variable>"         return ident "|||" out       }       {         sig=$1; raw=$2; total++         n[sig]++         k=sig SUBSEP raw; c[k]++         if (c[k]==1) d[sig]++          # distinct raw messages absorbed by this signature         if (c[k]==2) r[sig]++          # ... of which RECUR (a stable, re-visited value, not a fresh counter)         if (!(sig in fam)) fam[sig] = famkey(substr(sig, 1, index(sig,"|||")-1), raw)       }       END{         if (total==0) { print "NO-DATA"; exit }         sigs=0; single=0; degen=0; idfold=0         for (s in n) {           sigs++           if (n[s]==1) single++           f=fam[s]; fs[f]++; if (n[s]==1) fsingle[f]++           body=substr(s, index(s,"|||")+3)           # DEGENERATE: a signature body with no alphabetic character discriminates NOTHING — every fault           # that lands in it after the first is silent forever.           if (body !~ /[A-Za-z]/) {             degen++             printf "  DEGENERATE     n=%-5d raws=%-3d  [%s]  <- no alphabetic content: absorbs anything\n", n[s], d[s], s | "sort"             continue           }           # IDENTITY-FOLD: >=2 distinct raws, a SMALL set (<=idcap), and >=2 of them RECUR. A small           # re-visited value set is an enumerable identity (device/port/instance index), not an unbounded           # counter — so normalize() folded away WHICH thing faulted, and only the first ever alerted.           if (d[s]>=2 && d[s]<=idcap && r[s]>=2) {             idfold++             printf "  IDENTITY-FOLD  n=%-5d raws=%-3d  [%s]  <- %d distinct raws, %d recurring: an enumerable identity was folded\n", n[s], d[s], s, d[s], r[s] | "sort"           }         }         # FAMILY-STORM — the per-family twin of the global singleton rate (2026-08-28, same task). ONE         # global rate over the whole alphabet is a MAJORITY VOTE: the UUID family above was storming five         # signatures wide beside ~26 healthy repeating ones, and 5/31 = 0.16 can never reach SFLOOR 0.90,         # so the guard shipped for exactly this pole could not see the pole in its own normalizer. A rate         # computed over signatures SHARING A STEM lets one storming family trip it while the rest is         # healthy. It is an ADDED arm, not a replacement: an alphabet that is globally all-singleton has         # every family at size 1, below fminsig, so a pure per-family rule would go BLIND to the shape         # case (12) asserts. Report-only, like everything in --scope — it names a stem whose residue never         # converges and leaves it to a human to say whether that residue is identity or noise, which is         # the one question the normalizer structurally cannot answer about itself.         storm=0; fams=0         for (f in fs) {           fams++           # the all-variable bucket is a CATCH-ALL, not a family — it holds messages that share no fixed           # text at all, so a high singleton rate in it says nothing about any one stem. Excluded loudly           # rather than silently: it is counted in families= and never in family-storm=.           if (f ~ /\|\|\|<all-variable>$/) continue           if (fs[f] >= fminsig && (fsingle[f]+0)/fs[f] >= sfloor) {             storm++             printf "  FAMILY-STORM   sigs=%-5d singletons=%-3d  [%s]  <- this stem mints a fresh signature nearly every time: normalize() leaves a per-event residue here\n", fs[f], fsingle[f]+0, f | "sort"           }         }         close("sort")         rho = 1 - (sigs/total)         srate = single/sigs         printf "records=%d  signatures=%d  compression=%.3f  singleton-rate=%.2f  degenerate=%d  identity-fold=%d  families=%d  family-storm=%d\n", total, sigs, rho, srate, degen, idfold, fams, storm         gpart = (sigs>=minsig && srate>=sfloor)         fpart = (storm>0)         if (degen>0 || idfold>0) { verdict="OVER-COMPRESSED"; rc=3 }         else if (gpart || fpart) { verdict="OVER-PARTICULARIZED"; rc=4 }         else { verdict="BALANCED"; rc=0 }         # WHICH arm fired is part of the verdict — the two have different remedies (a global storm means         # the normalizer is too fine everywhere; a family storm means one stem carries an unfolded residue).         why = ""         if (gpart) why = sprintf("global singleton-rate %.2f >= %s over %d signatures", srate, sfloor, sigs)         if (fpart) why = why (gpart ? "; " : "") sprintf("%d storming famil%s (>=%d sigs each, singleton-rate >= %s)", storm, (storm==1?"y":"ies"), fminsig, sfloor)         # both poles can hold at once; the silent pole wins the verdict (a blind sense outranks a loud one)         also=""         if (rc==4) also=" (" why ")"         if (rc==3 && (gpart || fpart)) also=" (+ over-particularized: " why ")"         print "scope: " verdict also         exit rc       }
  1009319: 3 journalctl journalctl -b 0 -p err -o json
  1009320: 3 jq jq -r ((.SYSLOG_IDENTIFIER // ._COMM // "kernel")|tostring) + "|||" + ((.MESSAGE // "")|tostring)
  1009336: 3 python3 python3 /tmp/tmp.NTTk7NXyOO/td.mesh-labor/mesh-ledger.riHZqPAF/tmp.nHg8qhSQub 2026-09-14 2026-09-13T22:24:30Z 2026-09-14T03:24:30Z /tmp/tmp.NTTk7NXyOO/td.mesh-labor/mesh-ledger.riHZqPAF/tmp.fp4Q5J8EAv
  1009518: 3 python3 python3 - /tmp/tmp.NTTk7NXyOO/td.mesh-labor/tmp.qL0F88PFAH/task-feed/spend.log /home/mesh-home/.mesh/tick.log 5 --tokens /tmp/tmp.NTTk7NXyOO/td.mesh-labor/tmp.cvGPRM6yGn /home/mesh-home/.claude/projects 1
  1009733: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-heavy-run --test
  1009749: 3 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1009765: 3 bash bash /home/mesh-home/.local/bin/mesh-heavy-run --test
  1010002: 3 timeout timeout 12 /home/mesh-home/.local/bin/mesh-load-attrib --test
  1010017: 2 bash bash /home/mesh-home/.local/bin/mesh-load-attrib --test
  1010069: 2 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1010301: 2 timeout timeout 20 /home/mesh-home/.local/bin/mesh-dispatch --test
  1010329: 2 bash bash /home/mesh-home/.local/bin/mesh-dispatch --test
  1010383: 2 timeout timeout 12 /home/mesh-home/.local/bin/mesh-load-audit --test
  1010396: 2 bash bash /home/mesh-home/.local/bin/mesh-interruptibility --test
  1010436: 2 bash bash /home/mesh-home/.local/bin/mesh-load-audit --test
  1010704: 2 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1010789: 2 python3 python3 /home/mesh-home/.local/bin/mesh-task --test
  1011022: 2 timeout timeout 12 /home/mesh-home/.local/bin/mesh-load-gate --test
  1011049: 2 timeout timeout 20 /home/mesh-home/.local/bin/mesh-dms --test
  1011080: 2 bash bash /home/mesh-home/.local/bin/mesh-load-gate --test
  1011085: 2 bash bash /home/mesh-home/.local/bin/mesh-dms --test
  1011130: 2 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1011357: 2 bash bash /home/mesh-home/.local/bin/mesh-load-attrib --test
  1011363: 2 bash bash /home/mesh-home/.local/bin/mesh-load-attrib --test
  1011384: 2 bash bash /home/mesh-home/.local/bin/mesh-stress --json
  1011428: 2 sleep sleep 5
  1011473: 2 bash bash /home/mesh-home/.local/bin/mesh-audio-route --test
  1011489: 2 timeout timeout 4 ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@192.168.8.203 echo ok
  1011520: 2 ssh ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@192.168.8.203 echo ok
  1011573: 2 timeout timeout 12 /home/mesh-home/.local/bin/mesh-local-mind --test
  1011644: 2 bash bash /home/mesh-home/.local/bin/mesh-local-mind --test
  1011914: 2 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1011936: 2 timeout timeout 4 ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@100.103.99.16 echo ok
  1011959: 2 ssh ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@100.103.99.16 echo ok
  1012001: 2 python3 python3 /home/mesh-home/.local/bin/mesh-novelty --window 60
  1012003: 2 grep grep -aE ^[[:space:]]+[0-9]
  1012004: 2 head head -5
  1012011: 2 grep grep -a .
  1012067: 2 timeout timeout 20 /home/mesh-home/.local/bin/mesh-docstore --test
  1012086: 2 timeout timeout 20 /home/mesh-home/.local/bin/mesh-doctor --test
  1012129: 2 bash bash /home/mesh-home/.local/bin/mesh-doctor --test
  1012135: 2 python3 python3 /home/mesh-home/.local/bin/mesh-docstore --test
  1012212: 2 python3 python3 /home/mesh-home/lte-workstation/scripts/mesh-manifest --list
  1012230: 2 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1012593: 2 timeout timeout 12 /home/mesh-home/.local/bin/mesh-lock-holder --test
  1012615: 2 bash bash /home/mesh-home/.local/bin/mesh-lock-holder --test
  1012839: 2 sleep sleep 45
  1012909: 2 python3 python3 - /tmp/tmp.NTTk7NXyOO/td.mesh-local-mind/tmp.QbijHPZIbG/payloads
  1012942: 2 bash bash /home/mesh-home/.local/bin/mesh-doctor --test
  1013016: 2 python3 python3 /home/mesh-home/lte-workstation/scripts/mesh-manifest --check
  1013126: 2 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-task create demo /tmp/tmp.NTTk7NXyOO/td.mesh-dispatch/tmpzztq7jed/plan.tsv ask:20260907-demo
  1013177: 2 bash bash /home/mesh-home/.local/bin/mesh-load-audit --test
  1013213: 2 bash bash /home/mesh-home/.local/bin/mesh-load-audit --json
  1013214: 2 sed sed -n s/.*"node_conn":\([01]\).*/\1/p
  1013465: 2 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1013777: 1 timeout timeout 12 /home/mesh-home/.local/bin/mesh-looper --test
  1013812: 1 bash bash /home/mesh-home/.local/bin/mesh-looper --test
  1013841: 1 sleep sleep 5
  1014277: 1 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --test
  1014279: 1 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --probe
  1014302: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-edge-gate-audit --test
  1014349: 1 bash bash /home/mesh-home/.local/bin/mesh-edge-gate-audit --test
  1014416: 1 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --probe
  1014545: 1 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --test
  1014564: 1 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --probe
  1014686: 1 bash bash /home/mesh-home/.local/bin/mesh-local-mind --test
  1014700: 1 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1014717: 1 bash bash /home/mesh-home/.local/bin/mesh-local-mind --no-think --model stub:1b ping
  1014728: 1 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --probe
  1014912: 1 bash bash /home/mesh-home/.local/bin/mesh-ambient-clock --test
  1014931: 1 bash bash /home/mesh-home/.local/bin/mesh-ambient-clock --json
  1014996: 1 timeout timeout 25 ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=accept-new ilya@192.168.8.214 sh -s
  1015011: 1 ssh ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=accept-new ilya@192.168.8.214 sh -s
  1015030: 1 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-job-apply --reasons
  1015056: 1 timeout timeout 12 /home/mesh-home/.local/bin/mesh-mains-hum --test
  1015092: 1 python3 python3 /home/mesh-home/.local/bin/mesh-mains-hum --test
  1015103: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-egress-health --test
  1015107: 1 timeout timeout 25 ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=accept-new ilya@192.168.8.214 sh -s
  1015127: 1 bash bash /home/mesh-home/.local/bin/mesh-egress-health --test
  1015144: 1 ssh ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=accept-new ilya@192.168.8.214 sh -s
  1015373: 1 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1015812: 1 timeout timeout 12 /home/mesh-home/.local/bin/mesh-mca --test
  1015823: 1 bash bash /home/mesh-home/.local/bin/mesh-mca --test
  1015883: 1 bash bash /home/mesh-home/.local/bin/mesh-ble-recut-arm --test
  1015892: 1 bash bash /home/mesh-home/.local/bin/mesh-ble-recut-arm --test
  1016017: 1 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1016140: 1 bash bash /home/mesh-home/.local/bin/mesh-chat [verify] can someone check whether the artifact exists?
  1016284: 1 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1016366: 1 timeout timeout 12 /home/mesh-home/.local/bin/mesh-mdns-census --test
  1016380: 1 bash bash /home/mesh-home/.local/bin/mesh-land --apply mesh-land: add focused test artifact
  1016389: 1 bash bash /home/mesh-home/.local/bin/mesh-mdns-census --test
  1016391: 1 python /home/mesh-home/grainneukeln/.venv/bin/python -c import numpy
  1016566: 1 sleep sleep 5
  1016628: 1 bash bash /home/mesh-home/.local/bin/mesh-cam-lock --dev /dev/video0 --why bruno-watch -- fswebcam -q -S 25 -d /dev/video0 -r 1280x720 --no-banner /tmp/tmp.NTTk7NXyOO/td.mesh-bruno-watch/tmp.yRinpIkIik/w.jpg
  1016697: 1 timeout timeout 12 /home/mesh-home/.local/bin/mesh-media-scene --test
  1016713: 1 bash bash /home/mesh-home/.local/bin/mesh-body-backup --test
  1016747: 1 bash bash /home/mesh-home/.local/bin/mesh-body-backup --where
  1016766: 1 bash bash /home/mesh-home/.local/bin/mesh-media-scene --test
  1016818: 1 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1016825: 1 bash bash /home/mesh-home/.local/bin/mesh-land --apply mesh-land: add focused test artifact
  1016826: 1 bash bash /home/mesh-home/.local/bin/mesh-body-backup --where
  1016835: 1 bash bash /home/mesh-home/.local/bin/mesh-body-backup --where
  1016896: 1 sleep sleep 5
  1016970: 1 bash bash /home/mesh-home/.local/bin/mesh-budget --gate frames --why bruno-watch
  1017041: 1 bash bash /home/mesh-home/.local/bin/mesh-devcd-catch --sweep
  1017237: 1 timeout timeout 12 /home/mesh-home/.local/bin/mesh-membership-crdt --test
  1017242: 1 bash bash /home/mesh-home/.local/bin/mesh-membership-crdt --test
  1017255: 1 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1017263: 1 sleep sleep 5
  1017347: 1 bash bash /home/mesh-home/.local/bin/mesh-edge-gate-audit --test
  1017354: 1 bash bash /home/mesh-home/.local/bin/mesh-edge-gate-audit
  1017382: 0 bash bash /home/mesh-home/.local/bin/mesh-chat [verify] can someone check whether the artifact exists?
  1017395: 0 bash [bash] <defunct>
  1017409: 0 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --repo trovu/trovu
  1017428: 0 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --repo trovu/trovu
  1017449: 0 gh gh api repos/trovu/trovu/contents/.github/pull_request_template.md
  1017586: 0 timeout timeout 12 /home/mesh-home/.local/bin/mesh-mem-guard --test
  1017604: 0 bash bash /home/mesh-home/.local/bin/mesh-mem-guard --test
  1017713: 0 bash bash /home/mesh-home/.local/bin/mesh-stress --json
  1017755: 0 timeout timeout 4 mesh-nic-rx-loss --json
  1017769: 0 bash bash /home/mesh-home/.local/bin/mesh-nic-rx-loss --json
  1017828: 0 bash bash /home/mesh-home/.local/bin/mesh-devcd-catch --sweep
  1017833: 0 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --test
  1017843: 0 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --test
  1017861: 0 pgrep pgrep -u 1000 -f -- (mesh-devcd-catch|devcd-catch).*--listen
  1017864: 0 head head -1
  1017888: 0 gh gh api repos/tenstorrent/tt-metal/contents/.github/CODE_OF_CONDUCT.md
  1018048: 0 ping ping -c 1 -W 2 192.168.8.146
  1018128: 0 python3 [python3]
  1018156: 0 bash bash /home/mesh-home/.local/bin/mesh-looper --test
  1018257: 0 bash bash /home/mesh-home/.local/bin/mesh-cstate --test
  1018348: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1018486: 0 bash bash /home/mesh-home/.local/bin/mesh-chat-review --test
  1018488: 0 grep grep -q traces.log
  1018497: 0 bash bash /home/mesh-home/.local/bin/mesh-chat-review --test
  1018499: 0 bash bash /home/mesh-home/.local/bin/mesh-hw-fault-watch --test
  1018536: 0 bash bash /home/mesh-home/.local/bin/mesh-hw-fault-watch
  1018625: 0 bash bash /home/mesh-home/.local/bin/mesh-chat-review --test
  1018661: 0 timeout timeout 12 /home/mesh-home/.local/bin/mesh-memory-recall --test
  1018809: 0 python3 python3 /home/mesh-home/.local/bin/mesh-memory-recall --test
  1019055: 0 ssh ssh -o ConnectTimeout=6 -o StrictHostKeyChecking=accept-new -o BatchMode=yes root@100.105.241.84 true
  1019079: 0 sleep sleep 1
  1019098: 0 bash bash /home/mesh-home/.local/bin/mesh-kernel-taint --test
  1019107: 0 bash bash /home/mesh-home/.local/bin/mesh-kernel-taint
  1019236: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1019434: 0 bash bash /home/mesh-home/.local/bin/mesh-mem-guard --test
  1019446: 0 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  1019462: 0 python3 python3 /home/mesh-home/lte-workstation/scripts/mesh_task_log.py append /tmp/tmp.NTTk7NXyOO/td.mesh-dispatch/tmpzztq7jed/mesh mesh-home/mesh-task@mesh-home v1 r=2 | /ask=s:20260907-demo | /chain=s:demo | /created=s:2026-09-14T03:24:31Z | /current=i:0 | /dispatch=s:sent | /status=s:open | /steps/0/description=s:inspect source missing-prerequisite recovery: before rejecting, inspect repo, ledger, and live mesh; reuse an exact active prerequisite task or create/link one, then do mesh-owned work and evidence-based decisions/registrations without waiting. Keep parent queued/typed-blocked until gate passes. If external data unavailable, substitute honestly or record exact event/retry condition. Reject only invalid, duplicate, out-of-scope, or unsafe work with evidence. | /steps/0/dispatch_until=s:2026-09-14T03:54:32Z | /steps/0/dispatched_at=s:2026-09-14T03:24:32Z | /steps/0/id=s:demo/inspect | /steps/0/owner=s:alpha | /steps/0/priority=i:0 | /steps/0/queued_at=s:2026-09-14T03:24:32Z | /steps/0/slug=s:inspect | /steps/0/status=s:open | /steps/1/description=s:verify result missing-prerequisite recovery: before rejecting, inspect repo, ledger, and live mesh; reuse an exact active prerequisite task or create/link one, then do mesh-owned work and evidence-based decisions/registrations without waiting. Keep parent queued/typed-blocked until gate passes. If external data unavailable, substitute honestly or record exact event/retry condition. Reject only invalid, duplicate, out-of-scope, or unsafe work with evidence. | /steps/1/id=s:demo/verify | /steps/1/owner=s:beta | /steps/1/priority=i:0 | /steps/1/slug=s:verify | /steps/1/status=s:open | /steps/2/description=s:close chain missing-prerequisite recovery: before rejecting, inspect repo, ledger, and live mesh; reuse an exact active prerequisite task or create/link one, then do mesh-owned work and evidence-based decisions/registrations without waiting. Keep parent queued/typed-blocked until gate passes. If external data unavailable, substitute honestly or record exact event/retry condition. Reject only invalid, duplicate, out-of-scope, or unsafe work with evidence. | /steps/2/id=s:demo/close | /steps/2/owner=s:gamma | /steps/2/priority=i:0 | /steps/2/slug=s:close | /steps/2/status=s:open | /version=i:2
  1019469: 0 bash bash /home/mesh-home/.local/bin/mesh-promises
  1019473: 0 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  1019474: 0 sed sed s/^$/(none)/
  1019487: 0 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  1019512: 0 bash bash /home/mesh-home/.local/bin/mesh-edge-gate-audit
  1019530: 0 timeout timeout 12 /home/mesh-home/.local/bin/mesh-metronome --test
  1019590: 0 bash bash /home/mesh-home/.local/bin/mesh-metronome --test
  1019609: 0 timeout timeout 20 /home/mesh-home/.local/bin/mesh-exit-node-lan-heal --test
  1019621: 0 bash bash /home/mesh-home/.local/bin/mesh-exit-node-lan-heal --test
  1019644: 0 hledger hledger -f /tmp/tmp.NTTk7NXyOO/td.mesh-ledger/mesh-ledger.TNvKhdox/tmp.F3V4K437S8/dp.journal check
  1019705: 0 bash bash /home/mesh-home/.local/bin/mesh-lan-jitter --edge
  1019718: 0 bash bash /home/mesh-home/.local/bin/mesh-device-churn
  1019784: 0 sleep sleep 5
  1019860: 0 bash bash /home/mesh-home/.local/bin/mesh-light --test
  1019891: 0 python3 python3 /home/mesh-home/.local/bin/mesh-job-answers --covered hh:136175487
  1020017: 0 bash bash /home/mesh-home/.local/bin/mesh-light --test
  1020028: 0 python3 python3 - /tmp/tmp.NTTk7NXyOO/td.mesh-activity-tempo/tmp.Y0ozqozKhP/tmp.XTb5e9pXSv/flat.jpg
  1020063: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1020206: 0 bash bash /home/mesh-home/.local/bin/mesh-ambient-clock --json
  1020217: 0 python3 python3 -c import json,sys; print(json.dumps(sys.stdin.read(), ensure_ascii=False)[1:-1], end="")
  1020305: 0 bash bash /home/mesh-home/.local/bin/mesh-link-flap --test
  1020329: 0 timeout timeout -k 2 8 flock -w 8 /tmp/.mesh-mic.lock arecord -d 1 -D plughw:1,0 -f S16_LE -r 16000 /tmp/.card-mic.985920.wav
  1020366: 0 flock flock -w 8 /tmp/.mesh-mic.lock arecord -d 1 -D plughw:1,0 -f S16_LE -r 16000 /tmp/.card-mic.985920.wav
  1020382: 0 timeout timeout 12 /home/mesh-home/.local/bin/mesh-mic-crossvalidate --test
  1020393: 0 bash bash /home/mesh-home/.local/bin/mesh-link-flap --json
  1020409: 0 bash bash /home/mesh-home/.local/bin/mesh-mic-crossvalidate --test
  1020425: 0 arecord arecord -d 1 -D plughw:1,0 -f S16_LE -r 16000 /tmp/.card-mic.985920.wav
  1020493: 0 ffmpeg ffmpeg -hide_banner -f lavfi -i sine=frequency=440:duration=0.5 -ac 1 -ar 44100 /tmp/tmp.NTTk7NXyOO/td.mesh-mic-crossvalidate/.mesh-cv-test.wav -y
  1020537: 0 bash bash /home/mesh-home/.local/bin/mesh-exit-node-lan-heal --test
  1020538: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1020547: 0 bash bash /home/mesh-home/.local/bin/mesh-exit-node-lan-heal
  1020578: 0 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-cron-catchup
  1020582: 0 bash bash /home/mesh-home/.local/bin/mesh-home-state --test
  1020594: 0 bash bash /home/mesh-home/.local/bin/mesh-heavy-run 2000 -- touch /tmp/tmp.NTTk7NXyOO/td.mesh-heavy-run/tmp.Bch95seCmD/queued-ran
  1020598: 0 bash bash /home/mesh-home/.local/bin/mesh-home-state --json
  1020625: 0 bash bash /home/mesh-home/.local/bin/mesh-clear-audit --test
  1020702: 0 bash bash /home/mesh-home/.local/bin/mesh-device-churn
  1020745: 0 bash bash /home/mesh-home/.local/bin/mesh-promises
  1020755: 0 ping ping -c1 -W1 198.51.100.9
  1020760: 0 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-job-mail --lanes --json
  1020763: 0 bash bash /home/mesh-home/.local/bin/mesh-imac-wifi
  1020772: 0 sleep sleep 1
  1020775: 0 bash bash /home/mesh-home/.local/bin/mesh-media-scene --edge
  1020782: 0 bash bash /home/mesh-home/.local/bin/mesh-closure --null
  1020791: 0 bash bash /home/mesh-home/.local/bin/mesh-imac-wifi
  1020837: 0 bash bash /home/mesh-home/.local/bin/mesh-edge-gate-audit
  1020838: 0 timeout timeout 8 ssh -o BatchMode=yes -o ConnectTimeout=5 ilya@192.168.8.214 true
  1020845: 0 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-job-chatwatch
  1020860: 0 ssh ssh -o BatchMode=yes -o ConnectTimeout=5 ilya@192.168.8.214 true
  1020921: 0 bash bash /home/mesh-home/.local/bin/mesh-mca --test
  1020928: 0 bash bash /home/mesh-home/.local/bin/mesh-mca
  1020939: 0 bash bash /home/mesh-home/.local/bin/mesh-budget --test
  1020951: 0 bash bash /home/mesh-home/.local/bin/mesh-budget --test
  1020953: 0 sed sed -n 3p
  1020962: 0 bash bash /home/mesh-home/.local/bin/mesh-budget --dash
  1020989: 0 bash bash /home/mesh-home/lte-workstation/scripts/mesh-knowledge-publish
  1020991: 0 bash bash /home/mesh-home/.local/bin/mesh-correlate --test
  1021003: 0 timeout timeout 12 /home/mesh-home/.local/bin/mesh-mind-compact --test
  1021010: 0 bash bash /home/mesh-home/.local/bin/mesh-correlate --dry
  1021013: 0 bash bash /home/mesh-home/.local/bin/mesh-mind-compact --test
  1021027: 0 bash bash /home/mesh-home/.local/bin/mesh-budget --dash
  1021050: 0 bash bash /home/mesh-home/.local/bin/mesh-membership-crdt --test
  1021068: 4123168608 python3 python3 /tmp/tmp.NTTk7NXyOO/td.mesh-membership-crdt/mesh-crdt-9W6MWC.py selftest 2
  1021082: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-lan-newdevice --test
  1021102: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-promises
  1021105: 4123168608 tr tr   \n
  1021116: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-bruno --test
  1021119: 4123168608 grep grep -vx
  1021122: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-promises
  1021123: 4123168608 sort sort -u
  1021125: 4123168608 tr tr \n
  1021133: 4123168608 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-docstore --file /tmp/tmp.NTTk7NXyOO/td.mesh-docstore/docstore-test-bw33tsr1/t.db ingest
  1021135: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-mca
  1021147: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1021150: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-chat-review --test
  1021169: 4123168608 python3 python3 - /tmp/tmp.NTTk7NXyOO/td.mesh-home-state/tmp.U5t3t4noYg/.mesh/sensors.log /tmp/tmp.NTTk7NXyOO/td.mesh-home-state/tmp.U5t3t4noYg/.mesh/transcript.log --json    INITIAL EMPTY|dwell_s=3600|changes_24h=9
  1021172: 4123168608 sleep sleep 5
  1021180: 4123168608 python3 python3 -c  import json,sys,os,re,time from datetime import datetime,timezone ledger=sys.argv[1]; frm=int(sys.argv[2]); to=int(sys.argv[3]) batch=int(os.environ["MESH_BATCH"]); thresh=float(os.environ["MESH_THRESH"]) minn=int(os.environ.get("MESH_MINN","8")) loss_fresh=int(os.environ.get("MESH_LOSS_FRESH","172800"))   # loss ledger older than this (s) → stale (0=off) tokens=[t for t in os.environ["MESH_ANOM"].split() if t] loss=os.environ["MESH_LOSS"]; reason=os.environ["MESH_REASON"]; iso=os.environ["MESH_ISO"] def _isosecs(t):     return datetime.strptime(t,"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp() def loss_read(s):     # Read of the loss meter, keyed on the MACHINE fields from mesh-clear-loss --report     # (COST_ALL/N_ALL/LAST_TS), NOT the "first number in the flattened table" (that grabs a SAMPLE COUNT).     #   ok     — measured, |cost| < thresh, enough samples, FRESH    → the ONLY state that permits CLEAN     #   high   — measured, |cost| >= thresh                          → FLAG (real excess loss)     #   lown   — measured but N_ALL < minn                           → FLAG (not authoritative yet)     #   stale  — measured but LAST_TS older than loss_fresh          → FLAG (frozen ledger — dead canary cron;     #              the twin of absent: an AGING snapshot must not read as live authoritative CLEAN forever.     #              Fail-safe: LAST_TS missing/unparseable while a budget is set → stale, not a silent pass)     #   absent — no COST_ALL field (meter never ran / no ledger)     → FLAG (UNMEASURED, never a hollow pass)     s=s or ""     m=re.search(r"COST_ALL=([-+]?\d*\.?\d+)", s)     if not m: return ("absent",None,0)     try: cost=float(m.group(1))     except Exception: return ("absent",None,0)     nm=re.search(r"N_ALL=(\d+)", s); nn=int(nm.group(1)) if nm else 0     if nn<minn: return ("lown",cost,nn)     if loss_fresh>0:         tm=re.search(r"LAST_TS=(\S+)", s)         try:             if (not tm) or (_isosecs(iso)-_isosecs(tm.group(1)))>loss_fresh: return ("stale",cost,nn)         except Exception: return ("stale",cost,nn)     return (("high" if abs(cost)>=thresh else "ok"),cost,nn) rows=[] for l in open(ledger,encoding="utf-8"):     l=l.strip()     if not l: continue     try: rows.append(json.loads(l))     except Exception: pass span=rows[frm:to] n=len(span) if n==0:     line="clear-audit [%s] (%s, 0 batch·0 clears): loss=<%s> coverage=n/a anomalies=0 detail=- → CLEAN" % (iso,reason,loss)     print(line); sys.exit(0) cov=sum(1 for r in span if r.get("handoff_present") and r.get("handoff_fresh")) anom=0; detail=[] for r in span:     blob=" ".join(str(r.get(k,"")) for k in ("reason","source","win")).lower()     if not r.get("handoff_present"): anom+=1; detail.append("no-handoff"); continue     if not r.get("handoff_fresh"): anom+=1; detail.append("stale-handoff"); continue     for t in tokens:         if t in blob: anom+=1; detail.append(t); break covp=round(cov*100/n) lstate,lcost,lnn=loss_read(loss) lossgood=(lstate=="ok")                        # CLEAN requires a MEASURED, tolerable, adequately-sampled cost loss_ok_json = True if lstate=="ok" else (False if lstate=="high" else None)  # None = unmeasured/low-n, not a pass if lstate!="ok": detail.append("loss:"+lstate) # surface WHY the loss axis blocked CLEAN (absent/lown/high) verdict="CLEAN" if (anom==0 and covp==100 and lossgood) else "FLAG" batches=max(1,(n+batch-1)//batch) detail_s=",".join(sorted(set(detail))) or "-" line="clear-audit [%s] (%s, %d batch·%d clears): loss=<%s> coverage=%d%% anomalies=%d detail=%s → %s" % (     iso,reason,batches,n,loss,covp,anom,detail_s,verdict) # structured rollup row (the dash reads the one-liner via .clear-audit-last; this is the durable history). try:     with open(os.environ["MESH_ROLLUP"],"a") as f:         f.write(json.dumps({"ts":int(time.time()),"iso":iso,"reason":reason,"batches":batches,                             "clears":n,"coverage_pct":covp,"anomalies":anom,"detail":detail_s,                             "loss":loss,"loss_ok":loss_ok_json,"loss_state":lstate,                             "loss_cost":lcost,"loss_n":lnn,"verdict":verdict},ensure_ascii=False)+"\n") except Exception: pass print(line)  /tmp/tmp.NTTk7NXyOO/td.mesh-clear-audit/tmp.RF9Ay2hIjc/m/clear-log.jsonl 0 10
  1021184: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-bruno --json
  1021188: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-chat-review --test
  1021189: 4123168608 grep grep -cE \[idle\]|\[room-moved\]
  1021190: 4123168608 sort sort -u
  1021196: 4123168608 tr tr \n
  1021228: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-chat [fyi] kernel-taint: kernel fault RATE on mesh-home — warn_count +5 (now 12), oops_count +0 (now 0) since the last sample. The taint LATCH cannot show this: its W bit was already set, so a storm reads OK there forever. Deltas are boot-scoped; check 'journalctl -k -b | grep -A25 "cut here"' for the splat and its subsystem.
  1021245: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-dash --test-fast
  1021254: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-dash --once sound
  1021255: 4123168608 grep grep -E ^  drop
  1021266: 4123168608 sleep sleep 8
  1021283: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-media-scene --edge
  1021289: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-correlate --dry
  1021296: 4123168608 rg rg -m 40 --no-messages -o .{0,80}"file_path":"[^"]*/memory/[^"]*\.md"\} /home/mesh-home/.claude/projects/-home-mesh-home
  1021309: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-closure --null
  1021311: 4123168608 python3 python3 -
  1021323: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-media-scene --edge
  1021335: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-gpu-display --json
  1021349: 4123168608 python3 python3 - /tmp/tmp.NTTk7NXyOO/td.mesh-local-mind/tmp.QbijHPZIbG/jit/worker-d380c35895b7925d96c66d8e33020da385a3887405dec53747fa36222fffee3e.py /tmp/tmp.NTTk7NXyOO/td.mesh-local-mind/tmp.QbijHPZIbG/jit/worker-d380c35895b7925d96c66d8e33020da385a3887405dec53747fa36222fffee3e.pyc.1014717
  1021358: 4123168608 timeout timeout 12 /home/mesh-home/.local/bin/mesh-mind-control --test
  1021370: 4123168608 python /home/mesh-home/grainneukeln/.venv/bin/python -c import sys, os, math, wave import numpy as np  SR    = int(os.environ.get("METRO_SR", "44100")) BEATS = int(os.environ.get("METRO_BEATS", "32")) SIG   = int(os.environ.get("METRO_SIG", "4")) GAIN  = float(os.environ.get("METRO_GAIN", "0.6")) MDIR  = os.environ.get("METRO_DIR")  def click(freq, dur=0.04):     """One percussive click: a short sine burst with a fast exponential decay (a tick, not a tone)."""     n = int(SR*dur)     t = np.arange(n)/SR     env = np.exp(-t/0.008)                 # ~8ms decay → sharp transient     return np.sin(2*np.pi*freq*t)*env  def synth_clicks(bpm, beats=None):     beats = beats if beats else BEATS     spb = 60.0/bpm                          # seconds per beat     n = int(SR*spb*beats)     buf = np.zeros(n + SR//10, dtype=np.float64)     hi, lo = click(1600), click(1000)       # accented downbeat (1600Hz) vs normal beat (1000Hz)     for b in range(beats):         start = int(round(b*spb*SR))         c = hi if (b % SIG == 0) else lo         buf[start:start+len(c)] += c*(1.0 if (b % SIG == 0) else 0.7)     buf /= np.max(np.abs(buf)) + 1e-9     return (buf*GAIN*32767).astype(np.int16)  def write_wav(path, samples, sr=None):     sr = sr or SR     os.makedirs(os.path.dirname(path), exist_ok=True)     with wave.open(path, "wb") as w:         w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)         w.writeframes(samples.tobytes())  def detect_onsets(samples, sr, hop=0.010, refractory=0.18):     """Energy-onset detection: frame RMS, adaptive threshold, rising-edge + refractory. Returns onset     times (s). Robust to a noise floor; refractory caps the max tempo (~330 BPM) and kills double-triggers."""     x = samples.astype(np.float64)     if x.size == 0: return []     h = max(1, int(sr*hop))     nfr = x.size // h     if nfr < 2: return []     energy = np.array([np.sqrt(np.mean(x[i*h:(i+1)*h]**2)) for i in range(nfr)])     floor = np.percentile(energy, 20)     peak  = energy.max()     if peak <= floor*1.5: return []         # essentially silence / no transients     thr = floor + 0.20*(peak - floor)     onsets = []     last = -1e9     for i in range(1, nfr):         t = i*h/sr         if energy[i] >= thr and energy[i-1] < thr and (t - last) >= refractory:             onsets.append(t); last = t     return onsets  def fold_bpm(bpm):     """Fold a detected tempo into a musical 40..240 range (handles octave errors gracefully)."""     if bpm <= 0: return bpm     while bpm < 40:  bpm *= 2     while bpm > 240: bpm /= 2     return bpm  def bpm_from_onsets(onsets):     if len(onsets) < 2: return None     iois = np.diff(np.array(onsets))     iois = iois[iois > 0.05]                # drop spurious sub-50ms gaps     if iois.size == 0: return None     return fold_bpm(60.0/float(np.median(iois)))  def cmd_gen(bpm, beats):     samples = synth_clicks(bpm, beats)     path = os.path.join(MDIR, "click_%dbpm.wav" % int(round(bpm)))     write_wav(path, samples)     print("%.1f\t%d\t%s" % (bpm, beats or BEATS, path))   # bpm<TAB>beats<TAB>path     return 0  def cmd_tap(wavpath):     with wave.open(wavpath, "rb") as w:         sr = w.getframerate()         x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)         if w.getnchannels() > 1: x = x[::w.getnchannels()]     onsets = detect_onsets(x, sr)     bpm = bpm_from_onsets(onsets)     if bpm is None:         print("TAP\t0\tnone (need >=2 clear taps; got %d onset(s))" % len(onsets)); return 2     print("TAP\t%d\t%.1f" % (len(onsets), bpm))           # TAP<TAB>n_onsets<TAB>bpm     return 0  def cmd_test():     fails = 0     # 1) click WAV is valid + non-silent     s = synth_clicks(120, 8)     if s.dtype != np.int16 or int(np.max(np.abs(s))) == 0:         print("smoke-test: FAIL (click buffer invalid/silent)"); return 1     # 2) CLOSED LOOP: recover the synthesized tempo through the detector, for several tempos     for target in (60, 92, 120, 160):         clicks = synth_clicks(target, 12)         onsets = detect_onsets(clicks, SR)         got = bpm_from_onsets(onsets)         if got is None:             print("smoke-test: FAIL (%dbpm: no tempo recovered)" % target); fails += 1; continue         err = abs(got-target)         if err > 2:             print("smoke-test: FAIL (%dbpm → detected %.1f, %d onsets, off by %.1f)" % (target, got, len(onsets), err)); fails += 1     # 3) WAV round-trip     import tempfile     tmp = tempfile.mkdtemp(); p = os.path.join(tmp, "c.wav"); write_wav(p, s)     with wave.open(p, "rb") as w:         ok = (w.getnchannels()==1 and w.getsampwidth()==2 and w.getframerate()==SR)     os.remove(p); os.rmdir(tmp)     if not ok: print("smoke-test: FAIL (WAV round-trip)"); fails += 1     if fails: print("smoke-test: FAIL (%d)" % fails); return 1     print("smoke-test: ok (click valid + tempo recovered within 2bpm @ 60/92/120/160, valid WAV)")     return 0  mode = sys.argv[1] if   mode == "gen":  sys.exit(cmd_gen(float(sys.argv[2]), int(sys.argv[3]))) elif mode == "tap":  sys.exit(cmd_tap(sys.argv[2])) elif mode == "test": sys.exit(cmd_test()) test
  1021409: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-mind-control --test
  1021417: 4123168608 bash bash /home/mesh-home/lte-workstation/scripts/mesh-knowledge-publish
  1021434: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-gpu-display --json
  1021436: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-algedonic --test
  1021449: 4123168608 nvidia-smi nvidia-smi --query-gpu=uuid,pci.bus_id,display_attached,display_active --format=csv,noheader,nounits
  1021464: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-algedonic --agency-cost
  1021469: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-mdns-census
  1021475: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-homeostasis --test
  1021487: 4123168608 python3 python3 -
  1021489: 4123168608 dirname [dirname] <defunct>
  1021494: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-load-audit --json
  1021515: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-load-audit --json
  1021517: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-lan-newdevice --test
  1021525: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-budget --gate frames --why bruno-watch
  1021534: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-kill-events --test
  1021539: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-cooscillate --test
  1021543: 4123168608 python3 python3 -
  1021544: 4123168608 wc wc -l
  1021548: 4123168608 awk [awk] <defunct>
  1021549: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-kill-events
  1021551: 4123168608 awk awk BEGIN{print 20+0}
  1021554: 4123168608 bash [bash] <defunct>
  1021564: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-budget --dash
  1021575: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1021577: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-chat [verify] can someone check whether the artifact exists?
  1021581: 4123168608 mktemp [mktemp] <defunct>
  1021582: 4123168608 stat [stat]
  1021585: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-land --apply mesh-land: add focused test artifact
  1021586: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-hw-health
  1021587: 4123168608 grep grep -cF -- flock -n 200 /home/mesh-home/.local/bin/mesh-channel-keepalive
  1021588: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-exit-node-lan-heal
  1021590: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-closure --null
  1021591: 4123168608 python3 python3 -c import sys; sys.stdout.write(sys.stdin.read()[:40])
  1021592: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-edge-gate-audit
  1021593: 4123168608 awk [awk] <defunct>
doctor pid=908001 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  908001: 30 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  975033: 13 timeout timeout 20 /home/mesh-home/.local/bin/mesh-activity-tempo --test
  975053: 13 bash bash /home/mesh-home/.local/bin/mesh-activity-tempo --test
  975164: 12 bash bash /home/mesh-home/.local/bin/mesh-activity-tempo --test
  1005626: 4 bash bash /home/mesh-home/.local/bin/mesh-light --test
  1019860: 0 bash bash /home/mesh-home/.local/bin/mesh-light --test
  1020017: 0 bash bash /home/mesh-home/.local/bin/mesh-light --test
  1020028: 0 python3 python3 - /tmp/tmp.NTTk7NXyOO/td.mesh-activity-tempo/tmp.Y0ozqozKhP/tmp.XTb5e9pXSv/flat.jpg
doctor pid=908447 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  908447: 30 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  975433: 13 timeout timeout 20 /home/mesh-home/.local/bin/mesh-algedonic --test
  975454: 13 bash bash /home/mesh-home/.local/bin/mesh-algedonic --test
  1021436: 0 bash bash /home/mesh-home/.local/bin/mesh-algedonic --test
  1021464: 0 bash bash /home/mesh-home/.local/bin/mesh-algedonic --agency-cost
  1022116: 0 bash bash /home/mesh-home/.local/bin/mesh-algedonic --agency-cost
  1022155: 0 bash bash /home/mesh-home/.local/bin/mesh-algedonic --agency-cost
  1022176: 0 python3 python3 - /tmp/tmp.NTTk7NXyOO/td.mesh-algedonic/tmp.3cGBQDrjx5/algedonic.log /tmp/tmp.NTTk7NXyOO/td.mesh-algedonic/tmp.3cGBQDrjx5/chat.log 1800 6 200 999
doctor pid=908548 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  908548: 30 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  975486: 13 timeout timeout 20 /home/mesh-home/.local/bin/mesh-ambient-clock --test
  975498: 13 bash bash /home/mesh-home/.local/bin/mesh-ambient-clock --test
  975722: 13 bash bash /home/mesh-home/.local/bin/mesh-ambient-clock --test
  1022736: 0 bash bash /home/mesh-home/.local/bin/mesh-ambient-clock --test
  1022759: 0 bash bash /home/mesh-home/.local/bin/mesh-ambient-clock --json
  1023117: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-ambient-clock --json
  1023133: 4123168608 python3 [python3] <defunct>
doctor pid=909261 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  909261: 30 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  975885: 13 timeout timeout 20 /home/mesh-home/.local/bin/mesh-approach --test
  975911: 13 bash bash /home/mesh-home/.local/bin/mesh-approach --test
  975993: 13 bash bash /home/mesh-home/.local/bin/mesh-approach --test
  976851: 12 bash bash /home/mesh-home/.local/bin/mesh-approach --test
  976853: 12 bash bash /home/mesh-home/.local/bin/mesh-approach --test
  976856: 12 timeout timeout 20 mesh-wifi-motion
  976858: 12 bash bash /home/mesh-home/.local/bin/mesh-wifi-motion
  979004: 12 timeout timeout 45 mesh-wifiscan --log
  979011: 12 bash bash /home/mesh-home/.local/bin/mesh-wifiscan --log
  1012839: 2 sleep sleep 45
doctor pid=911151 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  911151: 30 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  976965: 13 timeout timeout 20 /home/mesh-home/.local/bin/mesh-audio-route --test
  976976: 12 bash bash /home/mesh-home/.local/bin/mesh-audio-route --test
  980421: 11 bash bash /home/mesh-home/.local/bin/mesh-audio-route --test
  1022896: 0 bash bash /home/mesh-home/.local/bin/mesh-audio-route --test
  1022933: 0 timeout timeout 4 ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@192.168.8.146 echo ok
  1022975: 0 ssh ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@192.168.8.146 echo ok
doctor pid=912063 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  912063: 30 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  977530: 13 timeout timeout 20 /home/mesh-home/.local/bin/mesh-autowire --test
  977563: 13 bash bash /home/mesh-home/.local/bin/mesh-autowire --test
doctor pid=912183 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  912183: 30 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  977885: 13 timeout timeout 20 /home/mesh-home/.local/bin/mesh-awaydigest --test
  977922: 13 python3 python3 /home/mesh-home/.local/bin/mesh-awaydigest --test
doctor pid=914728 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  914728: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  979576: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-ble-recut-arm --test
  979670: 12 bash bash /home/mesh-home/.local/bin/mesh-ble-recut-arm --test
  1015883: 2 bash bash /home/mesh-home/.local/bin/mesh-ble-recut-arm --test
  1015892: 2 bash bash /home/mesh-home/.local/bin/mesh-ble-recut-arm --test
doctor pid=916328 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  916328: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  980541: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-body-backup --test
  980558: 12 bash bash /home/mesh-home/.local/bin/mesh-body-backup --test
  1016713: 2 bash bash /home/mesh-home/.local/bin/mesh-body-backup --test
  1016747: 2 bash bash /home/mesh-home/.local/bin/mesh-body-backup --where
  1025055: 0 bash bash /home/mesh-home/.local/bin/mesh-body-backup --where
  1025080: 0 bash bash /home/mesh-home/.local/bin/mesh-body-backup --where
  1025089: 0 ping ping -c1 -W1 192.0.2.7
doctor pid=918922 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  918922: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  982019: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-bruno --test
  982046: 12 bash bash /home/mesh-home/.local/bin/mesh-bruno --test
  1026281: 0 bash bash /home/mesh-home/.local/bin/mesh-bruno --test
  1026315: 0 bash bash /home/mesh-home/.local/bin/mesh-bruno --json
doctor pid=919072 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  919072: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  982256: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-bruno-watch --test
  982282: 12 bash bash /home/mesh-home/.local/bin/mesh-bruno-watch --test
  995457: 9 bash bash /home/mesh-home/.local/bin/mesh-bruno-watch --test
  1024952: 0 bash bash /home/mesh-home/.local/bin/mesh-cam-lock --dev /dev/video0 --why bruno-watch -- sudo -n fswebcam -q -S 25 -d /dev/video0 -r 1280x720 --no-banner /tmp/tmp.NTTk7NXyOO/td.mesh-bruno-watch/tmp.yRinpIkIik/w.jpg
  1025312: 0 bash bash /home/mesh-home/.local/bin/mesh-budget --gate frames --why bruno-watch
doctor pid=919602 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  919602: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  982602: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-bt-lock-verdict --test
  982614: 12 bash bash /home/mesh-home/.local/bin/mesh-bt-lock-verdict --test
  985001: 11 bash bash /home/mesh-home/.local/bin/mesh-bt-lock-verdict --test
  985027: 11 bash bash /home/mesh-home/.local/bin/mesh-bt-lock-verdict --test
  985028: 11 grep grep -cx 11
  985048: 11 journalctl journalctl --since @1787137200 -o short-iso _TRANSPORT=kernel
  985051: 11 grep grep Opcode 0x0401 failed
  985052: 11 awk awk {split($1,a,"T"); print substr(a[2],4,2)}
doctor pid=919858 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  919858: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  982721: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-budget --test
  982771: 12 bash bash /home/mesh-home/.local/bin/mesh-budget --test
  1029099: 0 bash bash /home/mesh-home/.local/bin/mesh-budget --sample
doctor pid=922697 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  922697: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  984942: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-card --test
  985090: 12 bash bash /home/mesh-home/.local/bin/mesh-card --test
  987477: 11 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  999563: 8 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  999583: 8 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  999584: 8 sed sed s/^$/(none)/
  999596: 8 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  1000846: 7 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  1000871: 7 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  1000911: 7 timeout timeout -k 2 8 mesh-imac-notify --probe
  1000939: 7 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --probe
  1001016: 7 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --probe
  1001490: 7 timeout timeout 25 ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=accept-new ilya@192.168.8.214 sh -s
  1001527: 7 ssh ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=accept-new ilya@192.168.8.214 sh -s
doctor pid=922914 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  922914: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  985405: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-card-watchdog --test
  985425: 12 bash bash /home/mesh-home/.local/bin/mesh-card-watchdog --test
  985578: 12 bash bash /home/mesh-home/.local/bin/mesh-card-watchdog --test
  985902: 12 bash bash /home/mesh-home/.local/bin/mesh-card-watchdog --test
  985920: 12 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  1019446: 2 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  1019473: 2 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  1019474: 2 sed sed s/^$/(none)/
  1019487: 2 bash bash /home/mesh-home/.local/bin/mesh-card --refresh
  1024289: 1 timeout timeout -k 2 8 mesh-camera --test
  1024329: 1 bash bash /home/mesh-home/lte-workstation/scripts/integrations/mesh-camera --test
  1024595: 1 bash bash /home/mesh-home/lte-workstation/scripts/integrations/mesh-camera --test
  1024642: 1 python3 python3 -c import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())
doctor pid=923695 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  923695: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  985878: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-cell-signal --test
  985909: 12 bash bash /home/mesh-home/.local/bin/mesh-cell-signal --test
  1006276: 6 bash bash /home/mesh-home/.local/bin/mesh-cell-signal --test
  1025619: 1 bash bash /home/mesh-home/.local/bin/mesh-cell-signal --test
  1025624: 1 timeout timeout 4 ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@100.103.99.16 echo ok
  1025653: 1 ssh ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@100.103.99.16 echo ok
doctor pid=924422 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  924422: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  987306: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-channel-keepalive --test
  987315: 12 bash bash /home/mesh-home/.local/bin/mesh-channel-keepalive --test
  1025484: 1 bash bash /home/mesh-home/.local/bin/mesh-channel-keepalive --test
  1029443: 0 bash bash /home/mesh-home/.local/bin/mesh-channel-keepalive --test
  1029464: 0 ps ps -o comm= -p 1023183
doctor pid=926600 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  926600: 28 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  989134: 11 timeout timeout 20 /home/mesh-home/.local/bin/mesh-chat --test
  989167: 11 bash bash /home/mesh-home/.local/bin/mesh-chat --test
  1030042: 0 bash bash /home/mesh-home/.local/bin/mesh-chat [verify] can someone check the ds mic organ?
  1031946: 0 bash bash /home/mesh-home/.local/bin/mesh-chat [verify] can someone check the ds mic organ?
  1031999: 0 bash bash /home/mesh-home/.local/bin/mesh-chat [verify] can someone check the ds mic organ?
  1032037: 0 bash bash /home/mesh-home/.local/bin/mesh-promises --address [verify] can someone check the ds mic organ?
doctor pid=928299 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  928299: 28 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  991299: 11 timeout timeout 20 /home/mesh-home/.local/bin/mesh-chat-review --test
  991315: 11 bash bash /home/mesh-home/.local/bin/mesh-chat-review --test
  1031478: 0 bash bash /home/mesh-home/.local/bin/mesh-chat-review --test
  1031479: 0 grep grep -q CODE-CHECK
  1031505: 0 bash bash /home/mesh-home/.local/bin/mesh-chat-review --test
  1031522: 0 bash bash /home/mesh-home/.local/bin/mesh-chat-review --test
  1032736: 0 bash bash /home/mesh-home/.local/bin/mesh-chat-review --test
  1032740: 0 bash bash /home/mesh-home/.local/bin/mesh-chat-review --test
  1032741: 0 grep grep -cE \[mind-(paused|limited|blocked|unblocked)\]
doctor pid=930963 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  930963: 28 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1023946: 2 sleep sleep 8
doctor pid=931737 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  931737: 28 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  994465: 11 timeout timeout 20 /home/mesh-home/.local/bin/mesh-clear-audit --test
  994499: 11 bash bash /home/mesh-home/.local/bin/mesh-clear-audit --test
  1034285: 0 bash bash /home/mesh-home/.local/bin/mesh-clear-audit --test
  1034310: 0 python3 python3 -c import json,sys n=0 for l in open(sys.argv[1],encoding="utf-8"):     l=l.strip()     if not l: continue     try: json.loads(l); n+=1     except Exception: pass print(n) /tmp/tmp.NTTk7NXyOO/td.mesh-clear-audit/tmp.RF9Ay2hIjc/m/clear-log.jsonl
doctor pid=933663 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  933663: 27 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  996008: 10 timeout timeout 20 /home/mesh-home/.local/bin/mesh-closure --test
  996024: 10 bash bash /home/mesh-home/.local/bin/mesh-closure --test
  1034369: 0 bash bash /home/mesh-home/.local/bin/mesh-closure --null
  1034660: 0 bash bash /home/mesh-home/.local/bin/mesh-closure --null
doctor pid=936756 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  936756: 27 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  998675: 10 timeout timeout 20 /home/mesh-home/.local/bin/mesh-conversation --test
  998686: 10 bash bash /home/mesh-home/.local/bin/mesh-conversation --test
  1031897: 1 bash bash /home/mesh-home/.local/bin/mesh-conversation --test
doctor pid=937324 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  937324: 27 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  999710: 9 timeout timeout 20 /home/mesh-home/.local/bin/mesh-convexity --test
  999767: 9 bash bash /home/mesh-home/.local/bin/mesh-convexity --test
  1001842: 9 bash bash /home/mesh-home/.local/bin/mesh-convexity --test
  1001867: 9 bash bash /home/mesh-home/.local/bin/mesh-convexity --test
  1001926: 9 python3 python3 -
doctor pid=937922 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  937922: 27 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1000300: 10 timeout timeout 20 /home/mesh-home/.local/bin/mesh-cooscillate --test
  1000338: 9 bash bash /home/mesh-home/.local/bin/mesh-cooscillate --test
  1037120: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-cooscillate --test
  1037133: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-cooscillate --dry
doctor pid=938134 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  938134: 27 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1000570: 10 timeout timeout 20 /home/mesh-home/.local/bin/mesh-correlate --test
  1000608: 10 bash bash /home/mesh-home/.local/bin/mesh-correlate --test
  1035216: 0 bash bash /home/mesh-home/.local/bin/mesh-correlate --test
  1035225: 0 bash bash /home/mesh-home/.local/bin/mesh-correlate --dry
  1037675: 4123168608 rm rm -f /tmp/tmp.NTTk7NXyOO/td.mesh-correlate/tmp.ZqEml3aIO4
doctor pid=941696 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  941696: 26 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1004218: 9 timeout timeout 20 /home/mesh-home/.local/bin/mesh-criticality --test
  1004220: 9 bash bash /home/mesh-home/.local/bin/mesh-criticality --test
  1004566: 9 bash bash /home/mesh-home/.local/bin/mesh-criticality --test
  1004613: 9 python3 python3 -
doctor pid=942095 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  942095: 26 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1004627: 9 timeout timeout 20 /home/mesh-home/.local/bin/mesh-cron-catchup --test
  1004676: 9 python3 python3 /home/mesh-home/.local/bin/mesh-cron-catchup --test
doctor pid=942502 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  942502: 26 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1005105: 9 timeout timeout 20 /home/mesh-home/.local/bin/mesh-cstate --test
  1005157: 9 bash bash /home/mesh-home/.local/bin/mesh-cstate --test
  1028741: 2 bash bash /home/mesh-home/.local/bin/mesh-cstate --test
  1028773: 2 bash bash /home/mesh-home/.local/bin/mesh-cstate --json
  1037147: 0 bash bash /home/mesh-home/.local/bin/mesh-cstate --json
  1039248: 4123168608 bash [bash] <defunct>
doctor pid=943114 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  943114: 26 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1005428: 9 timeout timeout 20 /home/mesh-home/.local/bin/mesh-dash --test-fast
  1005519: 9 bash bash /home/mesh-home/.local/bin/mesh-dash --test-fast
  1005823: 9 bash bash /home/mesh-home/.local/bin/mesh-dash --test-fast
  1021245: 4 bash bash /home/mesh-home/.local/bin/mesh-dash --test-fast
  1021254: 4 bash bash /home/mesh-home/.local/bin/mesh-dash --once sound
  1021255: 4 grep grep -E ^  drop
  1025117: 3 bash bash /home/mesh-home/.local/bin/mesh-dash --once sound
  1039666: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-dash --once sound
  1039670: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-records --organs
doctor pid=945108 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  945108: 25 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1007250: 8 timeout timeout 20 /home/mesh-home/.local/bin/mesh-devcd-catch --test-fast
  1007311: 8 bash bash /home/mesh-home/.local/bin/mesh-devcd-catch --test-fast
  1038782: 0 bash bash /home/mesh-home/.local/bin/mesh-devcd-catch --sweep
  1040330: 4123168608 sudo /usr/bin/sudo -n cat /tmp/tmp.NTTk7NXyOO/td.mesh-devcd-catch/tmp.VMExJ5OMFV/class2/devcd8/data
doctor pid=945385 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  945385: 26 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1007433: 8 timeout timeout 20 /home/mesh-home/.local/bin/mesh-device-churn --test
  1007478: 8 bash bash /home/mesh-home/.local/bin/mesh-device-churn --test
  1038045: 0 bash bash /home/mesh-home/.local/bin/mesh-device-churn
  1038927: 0 bash bash /home/mesh-home/.local/bin/mesh-device-churn
doctor pid=946547 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  946547: 25 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1008732: 8 timeout timeout 20 /home/mesh-home/.local/bin/mesh-digest --test
  1008766: 8 bash bash /home/mesh-home/.local/bin/mesh-digest --test
  1009172: 8 bash bash /home/mesh-home/.local/bin/mesh-digest --test
  1009180: 8 bash bash /home/mesh-home/.local/bin/mesh-digest
  1023834: 4 bash bash /home/mesh-home/.local/bin/mesh-reliability --window 24
  1023837: 4 grep grep -a .
  1023982: 4 python3 python3 - /home/mesh-home/.mesh/chat.log 1789269874 1789356274 summary
doctor pid=948376 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  948376: 25 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1010301: 8 timeout timeout 20 /home/mesh-home/.local/bin/mesh-dispatch --test
  1010329: 8 bash bash /home/mesh-home/.local/bin/mesh-dispatch --test
  1010789: 8 python3 python3 /home/mesh-home/.local/bin/mesh-task --test
  1035504: 1 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-task create experiment-contract /tmp/tmp.NTTk7NXyOO/td.mesh-dispatch/tmpzztq7jed/experiment-plan.tsv
  1039172: 0 python3 python3 /home/mesh-home/lte-workstation/scripts/mesh_task_log.py append /tmp/tmp.NTTk7NXyOO/td.mesh-dispatch/tmpzztq7jed/mesh mesh-home/mesh-task@mesh-home v1 r=2 | /ask=n:null | /chain=s:experiment-contract | /created=s:2026-09-14T03:24:37Z | /current=i:0 | /dispatch=s:sent | /status=s:open | /steps/0/description=s:Run experiments and compare parameter arms missing-prerequisite recovery: before rejecting, inspect repo, ledger, and live mesh; reuse an exact active prerequisite task or create/link one, then do mesh-owned work and evidence-based decisions/registrations without waiting. Keep parent queued/typed-blocked until gate passes. If external data unavailable, substitute honestly or record exact event/retry condition. Reject only invalid, duplicate, out-of-scope, or unsafe work with evidence. machine-owned parameter selection: choose all not-yet-frozen parameters from repository/runtime evidence; record the chosen seed, ranges, and arm ordering, model revision, corpus/dataset manifests (including CSV/JSON/TSV inputs), dataset split and sample budget, cross-validation folds/repeats where applicable (or record not applicable when the frozen design has no CV field), training hyperparameters, metrics and decision thresholds, stopping rule, and resource and wall-time caps with rationale before execution; preserve any frozen registration unchanged; verify the result; do not wait for the operator to pick or freeze them. resource ownership: treat temporary GPU/CPU/memory/headroom scarcity as queued retry state; choose an available node/slot or retry cadence from live mesh evidence, record the resource decision and evidence in the artifact, and do not wait for the operator to reschedule it. For a GPU-bound job on mesh-home, use mesh-heavy-run with MESH_HEAVY_GPU_PREEMPT=1 and the task's measured minimum-free-VRAM threshold; its bounded mesh-gpu-lease may pause only mesh-managed GPU services, then restores their prior active state on completion or expiry. If the declared headroom still cannot be reached, services are restored and the job stays queued. | /steps/0/dispatch_until=s:2026-09-14T03:54:38Z | /steps/0/dispatched_at=s:2026-09-14T03:24:38Z | /steps/0/id=s:experiment-contract/experiment-review | /steps/0/owner=s:alpha | /steps/0/priority=i:0 | /steps/0/queued_at=s:2026-09-14T03:24:38Z | /steps/0/slug=s:experiment-review | /steps/0/status=s:open | /version=i:2
  1041952: 0 python3 /usr/bin/python3 /home/mesh-home/lte-workstation/scripts/mesh-log-scrub
doctor pid=949052 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  949052: 25 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1011049: 8 timeout timeout 20 /home/mesh-home/.local/bin/mesh-dms --test
  1011085: 8 bash bash /home/mesh-home/.local/bin/mesh-dms --test
doctor pid=949775 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  949775: 25 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1012067: 8 timeout timeout 20 /home/mesh-home/.local/bin/mesh-docstore --test
  1012135: 8 python3 python3 /home/mesh-home/.local/bin/mesh-docstore --test
  1043151: 4123168608 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-docstore --file /tmp/tmp.NTTk7NXyOO/td.mesh-docstore/docstore-test-bw33tsr1/rot.db put --key rotten --value the original bytes
doctor pid=950281 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  950281: 25 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1012086: 8 timeout timeout 20 /home/mesh-home/.local/bin/mesh-doctor --test
  1012129: 8 bash bash /home/mesh-home/.local/bin/mesh-doctor --test
  1037349: 1 bash bash /home/mesh-home/.local/bin/mesh-doctor --test
  1037376: 1 bash bash /home/mesh-home/.local/bin/mesh-supervise --status
  1042406: 0 bash bash /home/mesh-home/.local/bin/mesh-supervise --status
  1042428: 0 bash bash /home/mesh-home/.local/bin/mesh-supervise --status
  1042438: 0 pgrep pgrep -u 1000 -f -- mesh-selfcare --loop
doctor pid=952479 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  952479: 25 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1014302: 8 timeout timeout 20 /home/mesh-home/.local/bin/mesh-edge-gate-audit --test
  1014349: 8 bash bash /home/mesh-home/.local/bin/mesh-edge-gate-audit --test
  1017347: 7 bash bash /home/mesh-home/.local/bin/mesh-edge-gate-audit --test
  1017354: 7 bash bash /home/mesh-home/.local/bin/mesh-edge-gate-audit
  1042269: 0 bash bash /home/mesh-home/.local/bin/mesh-edge-gate-audit
  1044488: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-edge-gate-audit
  1044585: 4123168608 timeout timeout 90 /tmp/tmp.NTTk7NXyOO/td.mesh-edge-gate-audit/tmp.N0bBTzYZhY/bin/mesh-fix-needsprior --edge
doctor pid=953694 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  953694: 25 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1015103: 8 timeout timeout 20 /home/mesh-home/.local/bin/mesh-egress-health --test
  1015127: 8 bash bash /home/mesh-home/.local/bin/mesh-egress-health --test
  1043469: 0 bash bash /home/mesh-home/.local/bin/mesh-egress-health
  1043899: 0 bash bash /home/mesh-home/.local/bin/mesh-egress-health
  1044054: 0 bash bash /home/mesh-home/.local/bin/mesh-egress-health
  1044109: 0 python3 python3 -c import sys,json;print(json.load(sys.stdin).get("country_iso",""))
doctor pid=958551 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  958551: 24 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1019609: 6 timeout timeout 20 /home/mesh-home/.local/bin/mesh-exit-node-lan-heal --test
  1019621: 6 bash bash /home/mesh-home/.local/bin/mesh-exit-node-lan-heal --test
  1042591: 0 bash bash /home/mesh-home/.local/bin/mesh-exit-node-lan-heal --test
  1042606: 0 bash bash /home/mesh-home/.local/bin/mesh-exit-node-lan-heal
doctor pid=961127 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  961127: 23 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1022585: 6 timeout timeout 20 /home/mesh-home/.local/bin/mesh-fitness --test
  1022604: 6 bash bash /home/mesh-home/.local/bin/mesh-fitness --test
  1045099: 0 bash bash /home/mesh-home/.local/bin/mesh-fitness --test
  1045149: 0 bash bash /home/mesh-home/.local/bin/mesh-fitness --test
doctor pid=962788 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  962788: 23 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1024082: 5 timeout timeout 20 /home/mesh-home/.local/bin/mesh-forage --test
  1024120: 5 bash bash /home/mesh-home/.local/bin/mesh-forage --test
  1024273: 5 bash bash /home/mesh-home/.local/bin/mesh-forage --test
  1024681: 5 bash bash /home/mesh-home/.local/bin/mesh-forage --json
  1025596: 5 bash bash /home/mesh-home/.local/bin/mesh-forage --json
  1025633: 5 bash bash /home/mesh-home/.local/bin/mesh-forage --json
  1025688: 5 bash bash /home/mesh-home/.local/bin/mesh-promises --json
  1028844: 4 python3 python3 - json /home/mesh-home/.mesh/chat.log 2026-09-14T03:24:34Z 24 6 1
doctor pid=963655 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  963655: 22 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1024868: 5 timeout timeout 20 /home/mesh-home/.local/bin/mesh-fsnotify --test
  1024914: 5 bash bash /home/mesh-home/.local/bin/mesh-fsnotify --test
  1040438: 1 bash bash /home/mesh-home/.local/bin/mesh-fsnotify --window 5 --debounce 2 /tmp/tmp.NTTk7NXyOO/td.mesh-fsnotify/tmp.7Fvxmfmdn1/watched -- bash -c echo x >> '/tmp/tmp.NTTk7NXyOO/td.mesh-fsnotify/tmp.7Fvxmfmdn1/ran'
  1044182: 0 sleep sleep 2
doctor pid=964028 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  964028: 23 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1025248: 5 timeout timeout 20 /home/mesh-home/.local/bin/mesh-fswriter --test
  1025318: 5 python3 python3 /home/mesh-home/.local/bin/mesh-fswriter --test
  1042099: 1 sudo sudo -n --preserve-env=MESH_FSWRITER_TEST_STALL /usr/bin/python3 /home/mesh-home/.local/bin/mesh-fswriter --_armed --_log /tmp/tmp.NTTk7NXyOO/td.mesh-fswriter/fswriter-test-56h10jvi/log --window 3.0 /tmp/tmp.NTTk7NXyOO/td.mesh-fswriter/fswriter-test-56h10jvi/watched
  1043922: 0 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-fswriter --_armed --_log /tmp/tmp.NTTk7NXyOO/td.mesh-fswriter/fswriter-test-56h10jvi/log --window 3.0 /tmp/tmp.NTTk7NXyOO/td.mesh-fswriter/fswriter-test-56h10jvi/watched
  1045013: 0 bash [bash] <defunct>
doctor pid=965887 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  965887: 22 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1027179: 5 timeout timeout 20 /home/mesh-home/.local/bin/mesh-generate --test
  1027221: 5 bash bash /home/mesh-home/.local/bin/mesh-generate --test
  1027716: 5 bash bash /home/mesh-home/lte-workstation/tests/test-mesh-chat-generate-utf8-boundaries.sh
  1047052: 0 python3 python3 - /tmp/tmp.NTTk7NXyOO/td.mesh-generate/tmp.szUVZbMKBq/chat-home/.mesh/chat.log
doctor pid=971756 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  971756: 21 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1032658: 4 timeout timeout 20 /home/mesh-home/.local/bin/mesh-gmail-note3 --test
  1032697: 4 python3 python3 /home/mesh-home/.local/bin/mesh-gmail-note3 --test
  1037209: 2 adb adb exec-out su -c 'cat /data/data/com.google.android.gm/databases/bigTopDataDB.1023405767'
doctor pid=973768 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  973768: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1035121: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-guardian --test
  1035175: 3 bash bash /home/mesh-home/.local/bin/mesh-guardian --test
  1035471: 3 timeout timeout 30 bash /home/mesh-home/.local/bin/mesh-guardian
  1035496: 3 bash bash /home/mesh-home/.local/bin/mesh-guardian
  1035762: 3 bash bash /home/mesh-home/.local/bin/mesh-guardian
  1035788: 3 bash bash /home/mesh-home/.local/bin/mesh-guardian
  1035789: 3 grep grep -q ok
  1035803: 3 timeout timeout 14 ssh -n -o BatchMode=yes -o ConnectTimeout=6 nonexistent-host-127-0-99-253.local echo ok
  1035816: 3 ssh ssh -n -o BatchMode=yes -o ConnectTimeout=6 nonexistent-host-127-0-99-253.local echo ok
doctor pid=973921 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  973921: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1035531: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-guitar-watch --test
  1035558: 3 bash bash /home/mesh-home/.local/bin/mesh-guitar-watch --test
  1035874: 3 bash bash /home/mesh-home/.local/bin/mesh-guitar-watch --test
  1041180: 2 bash bash /home/mesh-home/.local/bin/mesh-guitar-watch --test
  1041190: 2 bash bash /home/mesh-home/.local/bin/mesh-guitar-watch --test
  1041232: 2 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-guitar-watch/tmp.oq3TCQfC3r/tmp.xmC4LcP3jc/tone.wav
  1041582: 2 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-guitar-watch/tmp.oq3TCQfC3r/tmp.xmC4LcP3jc/tone.wav
  1041604: 2 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-guitar-watch/tmp.oq3TCQfC3r/tmp.xmC4LcP3jc/tone.wav
  1041605: 2 grep grep ^MEASURE
  1041632: 2 python /home/mesh-home/grainneukeln/.venv/bin/python - /tmp/tmp.NTTk7NXyOO/td.mesh-guitar-watch/tmp.oq3TCQfC3r/tmp.xmC4LcP3jc/tone.wav 0,12,3 0.006 measure
doctor pid=974193 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  974193: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1035905: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-handoff --test
  1035977: 3 bash bash /home/mesh-home/.local/bin/mesh-handoff --test
  1050875: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-handoff --test
doctor pid=976228 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  976228: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1038593: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-heartbeat --test
  1038631: 3 bash bash /home/mesh-home/.local/bin/mesh-heartbeat --test
  1039306: 3 bash bash /home/mesh-home/.local/bin/mesh-heartbeat --test
  1039322: 3 timeout timeout 8 /home/mesh-home/.local/bin/mesh-health
  1039323: 3 grep grep -E PASS|FAIL|OFFLINE|SKIP
  1039324: 3 sed sed s/^/  /
  1039388: 3 bash bash /home/mesh-home/.local/bin/mesh-health
  1044350: 1 bash bash /home/mesh-home/.local/bin/mesh-health
  1045156: 1 bash bash /home/mesh-home/.local/bin/mesh-health
  1045175: 1 ping ping -c 1 -W 2 192.168.8.1
doctor pid=977017 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  977017: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1026018: 6 sleep sleep 8
doctor pid=977271 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  977271: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1039873: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-hh-drive --test
  1040010: 3 bash bash /home/mesh-home/.local/bin/mesh-hh-drive --test
  1045962: 1 sleep sleep 2
doctor pid=977808 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  977808: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1040459: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-hire-scan --test
  1040538: 3 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --test
  1049216: 0 gh gh auth status
doctor pid=978071 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  978071: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1040646: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-hire-submit --test
  1040675: 3 bash bash /home/mesh-home/.local/bin/mesh-hire-submit --test
  1041688: 3 bash bash /home/mesh-home/.local/bin/mesh-hire-submit --test
  1041697: 3 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --repo trovu/trovu
  1051188: 0 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --repo trovu/trovu
  1051210: 0 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --repo trovu/trovu
  1051214: 0 gh gh api repos/trovu/trovu/contents/.github/CONTRIBUTING.md
doctor pid=978346 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  978346: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1051443: 0 timeout timeout 25 /home/mesh-home/.local/bin/mesh-historical-ask-ledger --test
  1051460: 0 python3 python3 /home/mesh-home/.local/bin/mesh-historical-ask-ledger --test
doctor pid=979572 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  979572: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1042253: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-homeostasis --test
  1042290: 3 bash bash /home/mesh-home/.local/bin/mesh-homeostasis --test
  1055100: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-homeostasis --test
  1055113: 4123168608 python3 python3 - descend /tmp/tmp.NTTk7NXyOO/td.mesh-homeostasis/tmp.fzR0GCPPGy/somem.tsv
doctor pid=979986 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  979986: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1042755: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-home-state --test
  1042792: 3 bash bash /home/mesh-home/.local/bin/mesh-home-state --test
  1051046: 1 bash bash /home/mesh-home/.local/bin/mesh-home-state --json
  1052543: 0 python3 python3 - /home/mesh-home/.mesh/sensors.log /home/mesh-home/.mesh/transcript.log --json DATA-STALE|dwell_s=170930|changes_24h=0|fixture=CYCLING DIM|source=webcam|scene=localized|spread_luma=223|frame_age_s=2 OFFLINE INITIAL UNCERTAIN|dwell_s=1200|changes_24h=36|dwell_cov=100  UNREACHABLE
doctor pid=981059 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  981059: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1043905: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-hw-fault-watch --test
  1043926: 3 bash bash /home/mesh-home/.local/bin/mesh-hw-fault-watch --test
  1054640: 0 bash bash /home/mesh-home/.local/bin/mesh-hw-fault-watch --test
  1054654: 0 bash bash /home/mesh-home/.local/bin/mesh-hw-fault-watch
  1057178: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-hw-fault-watch
doctor pid=981298 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  981298: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1044073: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-hw-health --test
  1044108: 3 bash bash /home/mesh-home/.local/bin/mesh-hw-health --test
  1049748: 1 bash bash /home/mesh-home/.local/bin/mesh-hw-health
  1055235: 0 bash bash /home/mesh-home/.local/bin/mesh-hw-health
doctor pid=982041 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  982041: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1045057: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-ideate --test
  1045107: 3 bash bash /home/mesh-home/.local/bin/mesh-ideate --test
  1048810: 2 bash bash /home/mesh-home/.local/bin/mesh-ideate --test
  1049341: 2 bash bash /home/mesh-home/.local/bin/mesh-ideate --test
  1059142: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-ideate --test
doctor pid=983105 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  983105: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1046454: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-imac-cam-watch --test
  1046500: 3 bash bash /home/mesh-home/.local/bin/mesh-imac-cam-watch --test
  1058696: 0 python3 python3 - /tmp/tmp.NTTk7NXyOO/td.mesh-imac-cam-watch/tmp.jwaPcy55Pw
doctor pid=984152 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  984152: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1047515: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-imac-notify --test
  1047560: 3 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --test
  1060844: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --test
  1061024: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --test
  1061025: 4123168608 sed sed -n s/^GATE=//p
  1061026: 4123168608 head head -1
  1061056: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --test
doctor pid=984830 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  984830: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1048259: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-imac-say --test
  1048286: 3 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --test
  1060750: 0 bash bash /home/mesh-home/.local/bin/mesh-imac-notify --test
  1060884: 0 sh sh -c set -u MSG_B64='eA=='; TITLE_B64='dA=='; WANT_SAY=0; FORCE=0; PROBE=1; VOL_FLOOR=20; VOICE_B64=''; CONFIRM_S=15 d64() { printf '%s' "$1" | base64 -D 2>/dev/null || printf '%s' "$1" | base64 --decode 2>/dev/null; }  # --- THE GATE: screen state, never ssh reachability ------------------------------------------- G="$(python -c ' import Quartz d = Quartz.CGSessionCopyCurrentDictionary() or {} print("%s %s" % (d.get("CGSSessionScreenIsLocked", 0), d.get("kCGSSessionOnConsoleKey", 0))) ' 2>/dev/null)" LOCKED="$(printf '%s' "$G" | awk '{print $1}')" CONSOLE="$(printf '%s' "$G" | awk '{print $2}')" PWR="$(ioreg -n IODisplayWrangler -r -d 1 2>/dev/null | sed -n 's/.*"CurrentPowerState"=\([0-9]*\).*/\1/p' | head -1)" VOL="$(osascript -e 'output volume of (get volume settings)' 2>/dev/null)" case "$VOL" in ''|*[!0-9]*) VOL=-1 ;; esac  # An UNREADABLE gate is a CLOSED gate. A python that did not run, an ioreg that said nothing — # each renders here as blindness, and blindness must never open a door onto the operator's desk. GATE=open [ -z "$LOCKED" ] || [ -z "$CONSOLE" ] && GATE=unreadable-session [ -z "$PWR" ] && GATE=unreadable-display [ "$GATE" = open ] && [ "$LOCKED" = True ] && GATE=screen-locked [ "$GATE" = open ] && [ "$CONSOLE" != True ] && GATE=off-console [ "$GATE" = open ] && [ "$PWR" -lt 4 ] 2>/dev/null && GATE=display-asleep  echo "GATE=$GATE"; echo "LOCKED=$LOCKED"; echo "CONSOLE=$CONSOLE"; echo "PWR=$PWR"; echo "VOL=$VOL" [ "$PROBE" = 1 ] && exit 0  if [ "$GATE" != open ] && [ "$FORCE" != 1 ]; then echo "FIRED=0"; exit 0; fi  MSG="$(d64 "$MSG_B64")"; TITLE="$(d64 "$TITLE_B64")"  # --- watermark BEFORE the shot: the store row we later demand must be one this call caused ------ DB="$(getconf DARWIN_USER_DIR)com.apple.notificationcenter/db2/db" WM="$(sqlite3 "$DB" 'select coalesce(max(delivered_date),0) from record;' 2>/dev/null)" [ -n "$WM" ] || WM=0 echo "WM=$WM"  # --- fire. OSA rc is captured APART from the ssh rc — a live ssh to a machine that refused the #     AppleScript is the false OK this tool exists to refuse. ------------------------------------ OSA_ERR="$(osascript -e 'on run argv display notification (item 1 of argv) with title (item 2 of argv) end run' "$MSG" "$TITLE" 2>&1)"; OSA_RC=$? echo "FIRED=1"; echo "OSA_RC=$OSA_RC"; echo "OSA_ERR=$OSA_ERR"  # --- the audible leg: opt-in, floor-bound, and NO --force override -------------------------- SAY=off if [ "$WANT_SAY" = 1 ]; then   if [ "$GATE" != open ]; then SAY="skipped:gate-$GATE"   elif [ "$VOL" -lt "$VOL_FLOOR" ] 2>/dev/null; then SAY="skipped:vol-$VOL-below-floor-$VOL_FLOOR"   else     VOICE="$(d64 "$VOICE_B64")"     if [ -n "$VOICE" ]; then say -v "$VOICE" -- "$MSG" 2>/dev/null; else say -- "$MSG" 2>/dev/null; fi     SAY_RC=$?     [ "$SAY_RC" = 0 ] && SAY=fired || SAY="refused:rc$SAY_RC"   fi fi echo "SAY=$SAY"  # --- the health check: the Mac's OWN store, joined to the poster's bundle id, past the watermark. #     Polled, because the store write lags the AppleScript return. ------------------------------- PRESENTED=na; REC=- i=0 while [ $i -lt $CONFIRM_S ]; do   R="$(sqlite3 "$DB" "select r.rec_id||'|'||r.presented from record r join app a on a.app_id=r.app_id where a.identifier='com.apple.scripteditor2' and r.delivered_date > $WM order by r.rec_id desc limit 1;" 2>/dev/null)"   if [ -n "$R" ]; then     REC="$(printf '%s' "$R" | cut -d'|' -f1)"     PRESENTED="$(printf '%s' "$R" | cut -d'|' -f2)"     break   fi   i=$((i+1)); sleep 1 done echo "PRESENTED=$PRESENTED"; echo "REC=$REC"
  1060885: 0 sed sed -n s/^GATE=//p
  1060888: 0 head head -1
  1061782: 4123168608 sh sh -c set -u MSG_B64='eA=='; TITLE_B64='dA=='; WANT_SAY=0; FORCE=0; PROBE=1; VOL_FLOOR=20; VOICE_B64=''; CONFIRM_S=15 d64() { printf '%s' "$1" | base64 -D 2>/dev/null || printf '%s' "$1" | base64 --decode 2>/dev/null; }  # --- THE GATE: screen state, never ssh reachability ------------------------------------------- G="$(python -c ' import Quartz d = Quartz.CGSessionCopyCurrentDictionary() or {} print("%s %s" % (d.get("CGSSessionScreenIsLocked", 0), d.get("kCGSSessionOnConsoleKey", 0))) ' 2>/dev/null)" LOCKED="$(printf '%s' "$G" | awk '{print $1}')" CONSOLE="$(printf '%s' "$G" | awk '{print $2}')" PWR="$(ioreg -n IODisplayWrangler -r -d 1 2>/dev/null | sed -n 's/.*"CurrentPowerState"=\([0-9]*\).*/\1/p' | head -1)" VOL="$(osascript -e 'output volume of (get volume settings)' 2>/dev/null)" case "$VOL" in ''|*[!0-9]*) VOL=-1 ;; esac  # An UNREADABLE gate is a CLOSED gate. A python that did not run, an ioreg that said nothing — # each renders here as blindness, and blindness must never open a door onto the operator's desk. GATE=open [ -z "$LOCKED" ] || [ -z "$CONSOLE" ] && GATE=unreadable-session [ -z "$PWR" ] && GATE=unreadable-display [ "$GATE" = open ] && [ "$LOCKED" = True ] && GATE=screen-locked [ "$GATE" = open ] && [ "$CONSOLE" != True ] && GATE=off-console [ "$GATE" = open ] && [ "$PWR" -lt 4 ] 2>/dev/null && GATE=display-asleep  echo "GATE=$GATE"; echo "LOCKED=$LOCKED"; echo "CONSOLE=$CONSOLE"; echo "PWR=$PWR"; echo "VOL=$VOL" [ "$PROBE" = 1 ] && exit 0  if [ "$GATE" != open ] && [ "$FORCE" != 1 ]; then echo "FIRED=0"; exit 0; fi  MSG="$(d64 "$MSG_B64")"; TITLE="$(d64 "$TITLE_B64")"  # --- watermark BEFORE the shot: the store row we later demand must be one this call caused ------ DB="$(getconf DARWIN_USER_DIR)com.apple.notificationcenter/db2/db" WM="$(sqlite3 "$DB" 'select coalesce(max(delivered_date),0) from record;' 2>/dev/null)" [ -n "$WM" ] || WM=0 echo "WM=$WM"  # --- fire. OSA rc is captured APART from the ssh rc — a live ssh to a machine that refused the #     AppleScript is the false OK this tool exists to refuse. ------------------------------------ OSA_ERR="$(osascript -e 'on run argv display notification (item 1 of argv) with title (item 2 of argv) end run' "$MSG" "$TITLE" 2>&1)"; OSA_RC=$? echo "FIRED=1"; echo "OSA_RC=$OSA_RC"; echo "OSA_ERR=$OSA_ERR"  # --- the audible leg: opt-in, floor-bound, and NO --force override -------------------------- SAY=off if [ "$WANT_SAY" = 1 ]; then   if [ "$GATE" != open ]; then SAY="skipped:gate-$GATE"   elif [ "$VOL" -lt "$VOL_FLOOR" ] 2>/dev/null; then SAY="skipped:vol-$VOL-below-floor-$VOL_FLOOR"   else     VOICE="$(d64 "$VOICE_B64")"     if [ -n "$VOICE" ]; then say -v "$VOICE" -- "$MSG" 2>/dev/null; else say -- "$MSG" 2>/dev/null; fi     SAY_RC=$?     [ "$SAY_RC" = 0 ] && SAY=fired || SAY="refused:rc$SAY_RC"   fi fi echo "SAY=$SAY"  # --- the health check: the Mac's OWN store, joined to the poster's bundle id, past the watermark. #     Polled, because the store write lags the AppleScript return. ------------------------------- PRESENTED=na; REC=- i=0 while [ $i -lt $CONFIRM_S ]; do   R="$(sqlite3 "$DB" "select r.rec_id||'|'||r.presented from record r join app a on a.app_id=r.app_id where a.identifier='com.apple.scripteditor2' and r.delivered_date > $WM order by r.rec_id desc limit 1;" 2>/dev/null)"   if [ -n "$R" ]; then     REC="$(printf '%s' "$R" | cut -d'|' -f1)"     PRESENTED="$(printf '%s' "$R" | cut -d'|' -f2)"     break   fi   i=$((i+1)); sleep 1 done echo "PRESENTED=$PRESENTED"; echo "REC=$REC"
  1061828: 4123168608 head [head] <defunct>
doctor pid=985556 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  985556: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1048772: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-imac-wifi --test
  1048834: 3 bash bash /home/mesh-home/.local/bin/mesh-imac-wifi --test
  1051067: 2 timeout timeout 5 ssh -o BatchMode=yes -o ConnectTimeout=3 ilya@192.168.8.214 echo ok
  1051105: 2 ssh ssh -o BatchMode=yes -o ConnectTimeout=3 ilya@192.168.8.214 echo ok
doctor pid=987046 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  987046: 20 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1050304: 3 timeout timeout 20 /home/mesh-home/.local/bin/mesh-interruptibility --test
  1050314: 3 bash bash /home/mesh-home/.local/bin/mesh-interruptibility --test
  1062485: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-interruptibility --edge
  1062676: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-interruptibility --edge
  1062721: 4123168608 bash [bash]
doctor pid=990627 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  990627: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1053681: 2 timeout timeout 20 /home/mesh-home/.local/bin/mesh-job-apply --test
  1053712: 2 python3 python3 /home/mesh-home/.local/bin/mesh-job-apply --test
  1060531: 0 python3 python3 /home/mesh-home/.local/bin/mesh-job-answers --match
doctor pid=991489 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  991489: gone
doctor pid=992264 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  992264: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1055072: 2 timeout timeout 20 /home/mesh-home/.local/bin/mesh-job-calls --test
  1055111: 2 bash bash /home/mesh-home/.local/bin/mesh-job-calls --test
  1055325: 2 bash bash /home/mesh-home/.local/bin/mesh-job-calls --test
  1055383: 2 bash bash /home/mesh-home/.local/bin/mesh-job-calls --test
  1055387: 2 timeout timeout 10 mesh-phone-ip
  1055428: 2 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1056183: 2 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1056229: 2 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1056249: 2 bash bash /home/mesh-home/.local/bin/mesh-peer-addr Redmi
  1062096: 0 ping ping -c 1 -W 2 192.168.8.203
doctor pid=992606 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  992606: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1056113: 2 timeout timeout 20 /home/mesh-home/.local/bin/mesh-job-chatwatch --test
  1056268: 2 python3 python3 /home/mesh-home/.local/bin/mesh-job-chatwatch --test
  1058727: 1 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-job-chatwatch
doctor pid=994370 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  994370: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1058530: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-job-mail --test
  1058597: 1 python3 python3 /home/mesh-home/.local/bin/mesh-job-mail --test
  1064887: 0 python3 python3 /home/mesh-home/.local/bin/mesh-gmail-note3 --json --list 0 --since 3
doctor pid=995068 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  995068: gone
doctor pid=995242 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  995242: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1059809: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-job-reply --test
  1059868: 1 python3 python3 /home/mesh-home/.local/bin/mesh-job-reply --test
  1065690: 0 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-job-reply
doctor pid=995501 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  995501: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1059738: 2 timeout timeout 20 /home/mesh-home/.local/bin/mesh-job-scan --test
  1059778: 2 python3 python3 /home/mesh-home/.local/bin/mesh-job-scan --test
  1066282: 0 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-job-scan --resolve-check
doctor pid=996139 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  996139: gone
doctor pid=997211 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  997211: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1061526: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-job-track --test
  1061549: 1 python3 python3 /home/mesh-home/.local/bin/mesh-job-track --test
  1067525: 0 bash bash /home/mesh-home/.local/bin/mesh-hh-drive --goto https://hh.ru/applicant/negotiations
  1068049: 4123168608 sleep sleep 8
doctor pid=997529 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  997529: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1061384: 2 timeout timeout 20 /home/mesh-home/.local/bin/mesh-journal-watch --test
  1061462: 2 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --test
  1068695: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --test
  1068704: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --test
  1068708: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-journal-watch
doctor pid=998672 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  998672: gone
doctor pid=999388 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  999388: gone
doctor pid=999913 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  999913: gone
doctor pid=1000664 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1000664: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1064425: 2 timeout timeout 20 /home/mesh-home/.local/bin/mesh-labor --test
  1064501: 1 bash bash /home/mesh-home/.local/bin/mesh-labor --test
  1069511: 0 bash bash /home/mesh-home/.local/bin/mesh-labor --feed
  1070790: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-labor --feed
  1070799: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-labor --feed
  1070801: 4123168608 awk awk {c[$2" "$3" "$4]++} END{for(k in c) print c[k], k}
  1070952: 4123168608 awk [awk]
doctor pid=1001589 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1001589: gone
doctor pid=1001934 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1001934: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1065454: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-land --test
  1065512: 1 bash bash /home/mesh-home/.local/bin/mesh-land --test
  1066625: 1 bash bash /home/mesh-home/.local/bin/mesh-land --apply mesh-land: add focused test artifact
  1066944: 1 bash bash /home/mesh-home/.local/bin/mesh-land --apply mesh-land: add focused test artifact
  1066973: 1 bash bash /home/mesh-home/.local/bin/mesh-land --apply mesh-land: add focused test artifact
  1066990: 1 bash [bash] <defunct>
  1066992: 1 awk awk -F \t { print $1 }
doctor pid=1003507 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1003507: gone
doctor pid=1003970 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1003970: 18 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1066985: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-lan-newdevice --test
  1067035: 1 bash bash /home/mesh-home/.local/bin/mesh-lan-newdevice --test
  1067134: 1 bash bash /home/mesh-home/.local/bin/mesh-lan-newdevice --test
  1067154: 1 bash bash /home/mesh-home/.local/bin/mesh-peer-addr router
  1072148: 0 ping ping -c 1 -W 2 192.168.8.1
doctor pid=1004502 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1004502: 18 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1067575: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-lan-presence --test
  1067602: 1 bash bash /home/mesh-home/.local/bin/mesh-lan-presence --test
  1067636: 1 bash bash /home/mesh-home/.local/bin/mesh-lan-presence --test
  1067647: 1 bash bash /home/mesh-home/.local/bin/mesh-peer-addr router
  1071736: 0 ping ping -c 1 -W 2 192.168.8.1
doctor pid=1004983 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1004983: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1068037: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-leadlag --test
  1068064: 1 bash bash /home/mesh-home/.local/bin/mesh-leadlag --test
  1068644: 1 bash bash /home/mesh-home/.local/bin/mesh-leadlag --test
  1068646: 1 python3 python3 -
doctor pid=1005470 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1005470: gone
doctor pid=1006080 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1006080: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1070070: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-ledger --test
  1070096: 1 bash bash /home/mesh-home/.local/bin/mesh-ledger --test
doctor pid=1007139 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1007139: gone
doctor pid=1008920 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1008920: gone
doctor pid=1009749 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1009749: 18 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1072799: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-load-attrib --test
  1072869: 1 bash bash /home/mesh-home/.local/bin/mesh-load-attrib --test
  1074314: 0 bash bash /home/mesh-home/.local/bin/mesh-load-attrib --test
  1074517: 0 bash bash /home/mesh-home/.local/bin/mesh-load-attrib --test
  1074545: 0 bash bash /home/mesh-home/.local/bin/mesh-stress --json
  1078337: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-stress --json
doctor pid=1010069 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1010069: 18 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1073047: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-load-audit --test
  1073078: 1 bash bash /home/mesh-home/.local/bin/mesh-load-audit --test
  1076327: 0 bash bash /home/mesh-home/.local/bin/mesh-load-audit --test
  1076344: 0 bash bash /home/mesh-home/.local/bin/mesh-load-audit --json
  1076345: 0 sed sed -n s/.*"node_conn":\([01]\).*/\1/p
  1077686: 0 cat cat /proc/1000664/stat /proc/1001934/stat /proc/100195/stat /proc/1003970/stat /proc/1004502/stat /proc/1004983/stat /proc/1005105/stat /proc/1005157/stat /proc/1005428/stat /proc/1005519/stat /proc/1005823/stat /proc/1006080/stat /proc/1006235/stat /proc/1006592/stat /proc/1007250/stat /proc/1007311/stat /proc/1007433/stat /proc/1007478/stat /proc/1008732/stat /proc/1008766/stat /proc/1009172/stat /proc/1009180/stat /proc/1009749/stat /proc/100/stat /proc/1010069/stat /proc/1010301/stat /proc/1010329/stat /proc/1010704/stat /proc/1010789/stat /proc/1011049/stat /proc/1011085/stat /proc/1012067/stat /proc/1012086/stat /proc/1012129/stat /proc/1012135/stat /proc/1012230/stat /proc/1012839/stat /proc/1013358/stat /proc/1014302/stat /proc/1014349/stat /proc/1014700/stat /proc/1014828/stat /proc/1015103/stat /proc/1015127/stat /proc/1015373/stat /proc/1016017/stat /proc/1016284/stat /proc/1017255/stat /proc/1019609/stat /proc/1019621/stat /proc/101/stat /proc/1020538/stat /proc/1021003/stat /proc/1021013/stat /proc/1021147/stat /proc/1021245/stat /proc/1021254/stat /proc/1021255/stat /proc/1021752/stat /proc/1021766/stat /proc/1021798/stat /proc/1022585/stat /proc/1022604/stat /proc/1023004/stat /proc/1024082/stat /proc/1024120/stat /proc/1024273/stat /proc/1024529/stat /proc/1024681/stat /proc/1024868/stat /proc/1024914/stat /proc/1024/stat /proc/1025117/stat /proc/1025248/stat /proc/1025318/stat /proc/1025596/stat /proc/1025633/stat /proc/1025688/stat /proc/1025848/stat /proc/1026825/stat /proc/1026858/stat /proc/1027179/stat /proc/1027221/stat /proc/1028038/stat /proc/1028119/stat /proc/1028369/stat /proc/1028422/stat /proc/1028844/stat /proc/1029311/stat /proc/1029391/stat /proc/102/stat /proc/1030140/stat /proc/1030715/stat /proc/1031218/stat /proc/1032658/stat /proc/1032697/stat /proc/1033224/stat /proc/1033272/stat /proc/1033374/stat /proc/1033685/stat /proc/1034881/stat /proc/1035121/stat /proc/1035175/stat /proc/1035237/stat /proc/1035253/stat /proc/1035281/stat /proc/1035445/stat /proc/1035531/stat /proc/1035558/stat /proc/1035704/stat /proc/1035756/stat /proc/1035874/stat /proc/1035905/stat /proc/1035977/stat /proc/1036012/stat /proc/1036315/stat /proc/1036741/stat /proc/1038593/stat /proc/1038631/stat /proc/1038/stat /proc/1039873/stat /proc/1040010/stat /proc/1040459/stat /proc/1040538/stat /proc/1040646/stat /proc/1040675/stat /proc/1041180/stat /proc/1041190/stat /proc/1041232/stat /proc/1041582/stat /proc/1041604/stat /proc/1041605/stat /proc/1041632/stat /proc/1041688/stat /proc/1041697/stat /proc/1042253/stat /proc/1042290/stat /proc/1042665/stat /proc/1042755/stat /proc/1042792/stat /proc/1042919/stat /proc/1042964/stat /proc/1043198/stat /proc/1043204/stat /proc/1043502/stat /proc/1043788/stat /proc/1043826/stat /proc/1043905/stat /proc/1043926/stat /proc/1044073/stat /proc/1044108/stat /proc/1044484/stat /proc/1044503/stat /proc/1045057/stat /proc/1045107/stat /proc/1046454/stat /proc/1046500/stat /proc/1046906/stat /proc/1046946/stat /proc/1047365/stat /proc/1047515/stat /proc/1047560/stat /proc/1047846/stat /proc/1047865/stat /proc/1047927/stat /proc/1048230/stat /proc/1048259/stat /proc/1048282/stat /proc/1048286/stat /proc/1048558/stat /proc/1048772/stat /proc/1048810/stat /proc/1048834/stat /proc/1049051/stat /proc/1049068/stat /proc/1049075/stat /proc/1049117/stat /proc/1049296/stat /proc/1049341/stat /proc/1049748/stat /proc/104/stat /proc/1050050/stat /proc/1050052/stat /proc/1050065/stat /proc/1050304/stat /proc/1050314/stat /proc/1050581/stat /proc/1050596/stat /proc/1050615/stat /proc/1050617/stat /proc/1050618/stat /proc/1050802/stat /proc/1050820/stat /proc/1050821/stat /proc/1050835/stat /proc/1050949/stat /proc/1050973/stat /proc/1051030/stat /proc/1051098/stat /proc/1051306/stat /proc/1051529/stat /proc/1051531/stat /proc/1051774/stat /proc/1051800/stat /proc/1051860/stat /proc/1051873/stat /proc/1051978/stat /proc/1051994/stat /proc/1052316/stat /proc/1052347/stat /proc/1052348/stat /proc/1052362/stat /proc/1052502/stat /proc/1053450/stat /proc/1053500/stat /proc/1053586/stat /proc/1053681/stat /proc/1053712/stat /proc/1054103/stat /proc/1054157/stat /proc/1054248/stat /proc/1054249/stat /proc/1055072/stat /proc/1055111/stat /proc/1055235/stat /proc/1055325/stat /proc/1055383/stat /proc/1055387/stat /proc/1055428/stat /proc/1056113/stat /proc/1056240/stat /proc/1056268/stat /proc/1056294/stat /proc/1056348/stat /proc/1056421/stat /proc/1056533/stat /proc/1056949/stat /proc/1056951/stat /proc/1056971/stat /proc/1056976/stat /proc/1057054/stat /proc/1057081/stat /proc/1057149/stat /proc/1057403/stat /proc/1057785/stat /proc/1057917/stat /proc/1058233/stat /proc/1058257/stat /proc/1058301/stat /proc/1058530/stat /proc/1058597/stat /proc/1058684/stat /proc/1058700/stat /proc/1058727/stat /proc/1058/stat /proc/1059399/stat /proc/1059439/stat /proc/1059738/stat /proc/1059758/stat /proc/1059778/stat /proc/1059809/stat /proc/1059825/stat /proc/1059868/stat /proc/1059905/stat /proc/1059925/stat /proc/105/stat /proc/1060436/stat /proc/1060469/stat /proc/1060485/stat /proc/1060487/stat /proc/1060523/stat /proc/1060527/stat /proc/1060557/stat /proc/1060698/stat /proc/1060705/stat /proc/1060707/stat /proc/1060708/stat /proc/1060720/stat /proc/1060735/stat /proc/1060811/stat /proc/1060814/stat /proc/1060820/stat /proc/1060828/stat /proc/1060886/stat /proc/1060/stat /proc/1061303/stat /proc/1061384/stat /proc/1061449/stat /proc/1061462/stat /proc/1061526/stat /proc/1061549/stat /proc/1061835/stat /proc/1061894/stat /proc/1061905/stat /proc/1061963/stat /proc/1061972/stat /proc/1062122/stat /proc/1062422/stat /proc/1062544/stat /proc/1062614/stat /proc/1062655/stat /proc/1062948/stat /proc/1063147/stat /proc/1063183/stat /proc/1063258/stat /proc/1063282/stat /proc/1063302/stat /proc/1063822/stat /proc/1063924/stat /proc/1064243/stat /proc/1064293/stat /proc/1064359/stat /proc/1064425/stat /proc/1064501/stat /proc/1064887/stat /proc/1065010/stat /proc/1065020/stat /proc/1065166/stat /proc/1065454/stat /proc/1065512/stat /proc/1065515/stat /proc/1065557/stat /proc/1065697/stat /proc/1065719/stat /proc/1065785/stat /proc/1065855/stat /proc/1066137/stat /proc/1066166/stat /proc/1066342/stat /proc/1066344/stat /proc/1066369/stat /proc/1066442/stat /proc/1066625/stat /proc/1066742/stat /proc/1066985/stat /proc/1067035/stat /proc/1067092/stat /proc/1067113/stat /proc/1067134/stat /proc/1067154/stat /proc/1067404/stat /proc/1067512/stat /proc/1067525/stat /proc/1067575/stat /proc/1067593/stat /proc/1067602/stat /proc/1067628/stat /proc/1067636/stat /proc/1067647/stat /proc/1067742/stat /proc/1067747/stat /proc/1067783/stat /proc/1067870/stat /proc/1067886/stat /proc/1067889/stat /proc/1067919/stat /proc/1067947/stat /proc/1067976/stat /proc/1067/stat /proc/1068037/stat /proc/1068044/stat /proc/1068049/stat /proc/1068064/stat /proc/1068155/stat /proc/1068156/stat /proc/1068210/stat /proc/1068241/stat /proc/1068317/stat /proc/1068327/stat /proc/1068344/stat /proc/1068474/stat /proc/1068505/stat /proc/1068510/stat /proc/1068569/stat /proc/1068596/stat /proc/1068598/stat /proc/1068603/stat /proc/1068613/stat /proc/1068644/stat /proc/1068646/stat /proc/1068759/stat /proc/1068813/stat /proc/1068871/stat /proc/1068897/stat /proc/1068898/stat /proc/1068914/stat /proc/1068939/stat /proc/1068941/stat /proc/1069074/stat /proc/1069402/stat /proc/1069511/stat /proc/1069581/stat /proc/1069729/stat /proc/106/stat /proc/1070033/stat /proc/1070070/stat /proc/1070096/stat /proc/1070120/stat /proc/1070218/stat /proc/1070272/stat /proc/1070423/stat /proc/1070443/stat /proc/1070475/stat /proc/1070527/stat /proc/1070567/stat /proc/1070593/stat /proc/1070773/stat /proc/1070871/stat /proc/1070885/stat /proc/1071047/stat /proc/1071312/stat /proc/1071454/stat /proc/1071551/stat /proc/1071608/stat /proc/1071727/stat /proc/1071736/stat /proc/1071920/stat /proc/1071944/stat /proc/1071958/stat /proc/1071960/stat /proc/1072148/stat /proc/1072225/stat /proc/1072458/stat /proc/1072466/stat /proc/1072474/stat /proc/1072488/stat /proc/1072493/stat /proc/1072763/stat /proc/1072797/stat /proc/1072799/stat /proc/1072864/stat /proc/1072869/stat /proc/1072878/stat /proc/1072896/stat /proc/1072953/stat /proc/1073002/stat /proc/1073010/stat /proc/1073012/stat /proc/1073024/stat /proc/1073047/stat /proc/1073078/stat /proc/1073163/stat /proc/1073175/stat /proc/1073276/stat /proc/1073303/stat /proc/1073326/stat /proc/1073399/stat /proc/1073462/stat /proc/1073476/stat /proc/1073489/stat /proc/1073491/stat /proc/1073493/stat /proc/1073501/stat /proc/1073503/stat /proc/1073511/stat /proc/1073558/stat /proc/1073646/stat /proc/1073665/stat /proc/1073683/stat /proc/1073704/stat /proc/1073720/stat /proc/1073759/stat /proc/1073770/stat /proc/1073784/stat /proc/1073874/stat /proc/1073877/stat /proc/1073880/stat /proc/1073895/stat /proc/1073947/stat /proc/1073949/stat /proc/1073973/stat /proc/1074035/stat /proc/1074047/stat /proc/1074067/stat /proc/1074073/stat /proc/1074112/stat /proc/1074119/stat /proc/1074136/stat /proc/1074200/stat /proc/1074314/stat /proc/1074321/stat /proc/1074327/stat /proc/1074334/stat /proc/1074340/stat /proc/1074350/stat /proc/1074352/stat /proc/1074421/stat /proc/1074487/stat /proc/1074489/stat /proc/1074517/stat /proc/1074545/stat /proc/1074553/stat /proc/1074764/stat /proc/1074769/stat /proc/1074781/stat /proc/1074824/stat /proc/1074830/stat /proc/1075182/stat /proc/1075245/stat /proc/1075302/stat /proc/1075356/stat /proc/1075366/stat /proc/1075387/stat /proc/1075399/stat /proc/1075406/stat /proc/1075410/stat /proc/1075461/stat /proc/1075594/stat /proc/1075627/stat /proc/1075663/stat /proc/1075672/stat /proc/1075697/stat /proc/1075739/stat /proc/1075883/stat /proc/1075933/stat /proc/1075955/stat /proc/1075966/stat /proc/1075967/stat /proc/1076019/stat /proc/1076045/stat /proc/1076110/stat /proc/1076135/stat /proc/1076153/stat /proc/1076154/stat /proc/1076177/stat /proc/1076178/stat /proc/1076179/stat /proc/1076245/stat /proc/1076260/stat /proc/1076269/stat /proc/1076270/stat /proc/1076327/stat /proc/1076342/stat /proc/1076344/stat /proc/1076345/stat /proc/1076359/stat /proc/1076384/stat /proc/1076386/stat /proc/1076395/stat /proc/1076406/stat /proc/1076408/stat /proc/1076416/stat /proc/1076423/stat /proc/1076459/stat /proc/1076467/stat /proc/1076573/stat /proc/1076593/stat /proc/1076629/stat /proc/1076641/stat /proc/1076662/stat /proc/1076692/stat /proc/1076702/stat /proc/1076707/stat /proc/1076735/stat /proc/1076755/stat /proc/1076762/stat /proc/1076773/stat /proc/1076785/stat /proc/1076787/stat /proc/1076789/stat /proc/1076800/stat /proc/1076810/stat /proc/1076815/stat /proc/1076825/stat /proc/1076830/stat /proc/1076832/stat /proc/1076845/stat /proc/1076857/stat /proc/1076881/stat /proc/1076882/stat /proc/1076905/stat /proc/1076908/stat /proc/1076918/stat /proc/1076923/stat /proc/1076925/stat /proc/1076927/stat /proc/1076929/stat /proc/1076964/stat /proc/1076965/stat /proc/1076971/stat /proc/1076979/stat /proc/1076984/stat /proc/1076987/stat /proc/1076989/stat /proc/1076994/stat /proc/1077000/stat /proc/1077014/stat /proc/1077017/stat /proc/1077081/stat /proc/1077089/stat /proc/1077112/stat /proc/1077165/stat /proc/1077166/stat /proc/1077204/stat /proc/1077217/stat /proc/1077232/stat /proc/1077234/stat /proc/1077242/stat /proc/1077244/stat /proc/1077271/stat /proc/1077272/stat /proc/1077281/stat /proc/1077284/stat /proc/1077288/stat /proc/1077305/stat /proc/1077313/stat /proc/1077316/stat /proc/1077327/stat /proc/1077384/stat /proc/1077388/stat /proc/1077389/stat /proc/1077403/stat /proc/1077405/stat /proc/1077416/stat /proc/1077417/stat /proc/1077420/stat /proc/1077421/stat /proc/1077424/stat /proc/1077428/stat /proc/1077433/stat /proc/1077440/stat /proc/1077450/stat /proc/1077459/stat /proc/1077461/stat /proc/1077477/stat /proc/1077481/stat /proc/1077486/stat /proc/1077491/stat /proc/1077493/stat /proc/1077494/stat /proc/1077499/stat /proc/1077500/stat /proc/1077502/stat /proc/1077505/stat /proc/1077508/stat /proc/1077513/stat /proc/1077517/stat /proc/1077518/stat /proc/1077520/stat /proc/1077522/stat /proc/1077525/stat /proc/1077526/stat /proc/1077529/stat /proc/1077533/stat /proc/1077535/stat /proc/1077537/stat /proc/1077540/stat /proc/1077541/stat /proc/1077546/stat /proc/1077549/stat /proc/1077550/stat /proc/1077561/stat /proc/1077568/stat /proc/1077570/stat /proc/1077571/stat /proc/1077573/stat /proc/1077575/stat /proc/1077576/stat /proc/1077578/stat /proc/1077579/stat /proc/1077581/stat /proc/1077583/stat /proc/1077586/stat /proc/1077587/stat /proc/1077596/stat /proc/1077602/stat /proc/1077608/stat /proc/1077615/stat /proc/1077617/stat /proc/1077618/stat /proc/1077619/stat /proc/1077625/stat /proc/1077635/stat /proc/1077636/stat /proc/1077637/stat /proc/1077643/stat /proc/1077644/stat /proc/1077647/stat /proc/1077651/stat /proc/1077652/stat /proc/1077660/stat /proc/1077661/stat /proc/1077663/stat /proc/1077664/stat /proc/1077665/stat /proc/1077667/stat /proc/1077668/stat /proc/1077672/stat /proc/1077673/stat /proc/1077675/stat /proc/1077677/stat /proc/1077678/stat /proc/1077679/stat /proc/1077680/stat /proc/1077686/stat /proc/1077689/stat /proc/1077691/stat /proc/1077695/stat /proc/1077697/stat /proc/1077699/stat /proc/1077701/stat /proc/1077704/stat /proc/1077705/stat /proc/1077706/stat /proc/1077707/stat /proc/1077708/stat /proc/1077709/stat /proc/1077712/stat /proc/1077714/stat /proc/1077715/stat /proc/1077716/stat /proc/1077717/stat /proc/1077718/stat /proc/1077719/stat /proc/1077720/stat /proc/1077721/stat /proc/1077722/stat /proc/1077723/stat /proc/1077724/stat /proc/1077725/stat /proc/1077726/stat /proc/1077728/stat /proc/1077729/stat /proc/1077731/stat /proc/1077733/stat /proc/1077734/stat /proc/1077739/stat /proc/1077742/stat /proc/1077749/stat /proc/1077754/stat /proc/1077755/stat /proc/1077758/stat /proc/1077759/stat /proc/1077760/stat /proc/1077761/stat /proc/1077763/stat /proc/1077764/stat /proc/1077765/stat /proc/1077766/stat /proc/1077768/stat /proc/1077769/stat /proc/1077771/stat /proc/1077774/stat /proc/1077776/stat /proc/1077778/stat /proc/1077780/stat /proc/1077781/stat /proc/1077783/stat /proc/1077785/stat /proc/1077786/stat /proc/1077787/stat /proc/1077788/stat /proc/1077789/stat /proc/1077790/stat /proc/1077/stat /proc/107/stat /proc/108/stat /proc/1091175/stat /proc/1095/stat /proc/10/stat /proc/1109/stat /proc/110/stat /proc/1114/stat /proc/111/stat /proc/112/stat /proc/1131695/stat /proc/1132237/stat /proc/1134093/stat /proc/113/stat /proc/1146022/stat /proc/114/stat /proc/1152858/stat /proc/116/stat /proc/117/stat /proc/1181875/stat /proc/118/stat /proc/119/stat /proc/120/stat /proc/1214/stat /proc/121/stat /proc/1224538/stat /proc/122/stat /proc/123/stat /proc/125/stat /proc/127/stat /proc/128/stat /proc/129/stat /proc/12/stat /proc/130/stat /proc/1313/stat /proc/1315/stat /proc/1317/stat /proc/1318/stat /proc/1319/stat /proc/131/stat /proc/1325/stat /proc/1328079/stat /proc/1328865/stat /proc/132/stat /proc/133/stat /proc/134/stat /proc/1355/stat /proc/135/stat /proc/1361278/stat /proc/137/stat /proc/138/stat /proc/1397/stat /proc/1398/stat /proc/139/stat /proc/13/stat /proc/140/stat /proc/1412/stat /proc/141/stat /proc/142/stat /proc/1486/stat /proc/14/stat /proc/1542254/stat /proc/1548467/stat /proc/1561467/stat /proc/156/stat /proc/157/stat /proc/158/stat /proc/15/stat /proc/1607508/stat /proc/160/stat /proc/166/stat /proc/1674168/stat /proc/1674602/stat /proc/1675857/stat /proc/1675900/stat /proc/1675903/stat /proc/1675974/stat /proc/1675992/stat /proc/1678191/stat /proc/1688380/stat /proc/16/stat /proc/1718199/stat /proc/173301/stat /proc/173/stat /proc/1758067/stat /proc/1797392/stat /proc/17/stat /proc/184/stat /proc/185/stat /proc/1878/stat /proc/188618/stat /proc/189236/stat /proc/189417/stat /proc/18/stat /proc/1900/stat /proc/1902/stat /proc/1903/stat /proc/1904/stat /proc/1905/stat /proc/1925338/stat /proc/192866/stat /proc/19330/stat /proc/1940/stat /proc/1941/stat /proc/1953208/stat /proc/19/stat /proc/1/stat /proc/2019433/stat /proc/2038135/stat /proc/2049766/stat /proc/20/stat /proc/2114008/stat /proc/211/stat /proc/21240/stat /proc/213112/stat /proc/214/stat /proc/215112/stat /proc/218/stat /proc/21/stat /proc/220744/stat /proc/222267/stat /proc/2236965/stat /proc/226/stat /proc/2275811/stat /proc/227/stat /proc/229/stat /proc/22/stat /proc/232/stat /proc/2343989/stat /proc/2378515/stat /proc/238/stat /proc/23/stat /proc/240/stat /proc/242/stat /proc/243/stat /proc/244/stat /proc/245/stat /proc/2486018/stat /proc/249397/stat /proc/24/stat /proc/2519290/stat /proc/260682/stat /proc/260871/stat /proc/262117/stat /proc/2621732/stat /proc/2621746/stat /proc/262393/stat /proc/2625300/stat /proc/2628578/stat /proc/263/stat /proc/266605/stat /proc/26/stat /proc/2793787/stat /proc/27/stat /proc/2807535/stat /proc/28/stat /proc/2905207/stat /proc/2923641/stat /proc/294/stat /proc/295/stat /proc/2969201/stat /proc/296/stat /proc/297/stat /proc/298/stat /proc/299792/stat /proc/299/stat /proc/29/stat /proc/2/stat /proc/3000654/stat /proc/3002827/stat /proc/300/stat /proc/301/stat /proc/302/stat /proc/303/stat /proc/304/stat /proc/305/stat /proc/3067272/stat /proc/3067791/stat /proc/3068534/stat /proc/306/stat /proc/307/stat /proc/3085169/stat /proc/308/stat /proc/3094741/stat /proc/3098174/stat /proc/309/stat /proc/30/stat /proc/312356/stat /proc/317664/stat /proc/318780/stat /proc/3191483/stat /proc/3209369/stat /proc/32/stat /proc/331353/stat /proc/3319863/stat /proc/332/stat /proc/3384315/stat /proc/33/stat /proc/340537/stat /proc/340589/stat /proc/341413/stat /proc/3415918/stat /proc/343365/stat /proc/343690/stat /proc/3438702/stat /proc/344297/stat /proc/344603/stat /proc/344688/stat /proc/344811/stat /proc/345705/stat /proc/346406/stat /proc/346409/stat /proc/346410/stat /proc/346416/stat /proc/346665/stat /proc/346666/stat /proc/346754/stat /proc/346756/stat /proc/34/stat /proc/3504319/stat /proc/352321/stat /proc/3549520/stat /proc/35/stat /proc/363/stat /proc/3658073/stat /proc/366248/stat /proc/367058/stat /proc/367187/stat /proc/36/stat /proc/3728464/stat /proc/3729179/stat /proc/3736724/stat /proc/375057/stat /proc/3768388/stat /proc/3768714/stat /proc/377154/stat /proc/377156/stat /proc/3779261/stat /proc/3796465/stat /proc/3828628/stat /proc/385105/stat /proc/385530/stat /proc/385702/stat /proc/3894834/stat /proc/38/stat /proc/3900358/stat /proc/3905731/stat /proc/3929239/stat /proc/3929241/stat /proc/3929247/stat /proc/3929260/stat /proc/3987711/stat /proc/39/stat /proc/3/stat /proc/4044263/stat /proc/40/stat /proc/412310/stat /proc/412522/stat /proc/4190599/stat /proc/4190602/stat /proc/41/stat /proc/421766/stat /proc/421853/stat /proc/421916/stat /proc/426122/stat /proc/426174/stat /proc/426176/stat /proc/429/stat /proc/42/stat /proc/431/stat /proc/44/stat /proc/45/stat /proc/46/stat /proc/47/stat /proc/48/stat /proc/492/stat /proc/497/stat /proc/4/stat /proc/506988/stat /proc/507068/stat /proc/507120/stat /proc/507197/stat /proc/507250/stat /proc/507325/stat /proc/507339/stat /proc/507375/stat /proc/507395/stat /proc/507466/stat /proc/507516/stat /proc/507586/stat /proc/507657/stat /proc/507718/stat /proc/507833/stat /proc/507913/stat /proc/508003/stat /proc/508031/stat /proc/50/stat /proc/511403/stat /proc/511413/stat /proc/512509/stat /proc/512562/stat /proc/512636/stat /proc/512766/stat /proc/512891/stat /proc/513089/stat /proc/513281/stat /proc/513678/stat /proc/514030/stat /proc/514431/stat /proc/514726/stat /proc/514854/stat /proc/515142/stat /proc/515268/stat /proc/515476/stat /proc/515676/stat /proc/516004/stat /proc/516308/stat /proc/516332/stat /proc/516528/stat /proc/516903/stat /proc/517291/stat /proc/518417/stat /proc/518439/stat /proc/518941/stat /proc/519399/stat /proc/519476/stat /proc/519650/stat /proc/51/stat /proc/520644/stat /proc/520867/stat /proc/521261/stat /proc/524250/stat /proc/524884/stat /proc/526993/stat /proc/528195/stat /proc/528331/stat /proc/529071/stat /proc/52/stat /proc/530/stat /proc/531/stat /proc/538/stat /proc/53/stat /proc/54/stat /proc/566/stat /proc/569720/stat /proc/56/stat /proc/57/stat /proc/580/stat /proc/58/stat /proc/59/stat /proc/5/stat /proc/60/stat /proc/620496/stat /proc/620562/stat /proc/620737/stat /proc/62/stat /proc/63/stat /proc/64/stat /proc/65/stat /proc/66218/stat /proc/66/stat /proc/6824/stat /proc/6825/stat /proc/6853/stat /proc/6854/stat /proc/689674/stat /proc/689/stat /proc/68/stat /proc/690/stat /proc/697047/stat /proc/69/stat /proc/6/stat /proc/70747/stat /proc/707606/stat /proc/70/stat /proc/710968/stat /proc/71/stat /proc/722/stat /proc/72/stat /proc/743/stat /proc/744/stat /proc/745/stat /proc/746/stat /proc/747/stat /proc/748/stat /proc/749615/stat /proc/749618/stat /proc/74/stat /proc/753338/stat /proc/753389/stat /proc/753451/stat /proc/753455/stat /proc/753649/stat /proc/753706/stat /proc/75/stat /proc/76/stat /proc/77/stat /proc/780205/stat /proc/78/stat /proc/7/stat /proc/80/stat /proc/81/stat /proc/827965/stat /proc/82/stat /proc/83/stat /proc/845/stat /proc/846/stat /proc/848/stat /proc/849/stat /proc/84/stat /proc/850/stat /proc/853/stat /proc/863278/stat /proc/86/stat /proc/87443/stat /proc/87/stat /proc/880667/stat /proc/883038/stat /proc/889011/stat /proc/88/stat /proc/89636/stat /proc/897497/stat /proc/89777/stat /proc/89827/stat /proc/89/stat /proc/900036/stat /proc/901256/stat /proc/901259/stat /proc/901290/stat /proc/901298/stat /proc/901299/stat /proc/901304/stat /proc/901323/stat /proc/901367/stat /proc/901369/stat /proc/901395/stat /proc/901444/stat /proc/901453/stat /proc/901457/stat /proc/901476/stat /proc/901545/stat /proc/904630/stat /proc/906547/stat /proc/907719/stat /proc/908001/stat /proc/908447/stat /proc/908548/stat /proc/909261/stat /proc/90/stat /proc/910/stat /proc/911/stat /proc/912063/stat /proc/912183/stat /proc/912366/stat /proc/912402/stat /proc/912701/stat /proc/912/stat /proc/914728/stat /proc/917335/stat /proc/918440/stat /proc/918922/stat /proc/919072/stat /proc/919602/stat /proc/919858/stat /proc/921902/stat /proc/922697/stat /proc/922914/stat /proc/923695/stat /proc/923/stat /proc/924422/stat /proc/924/stat /proc/926600/stat /proc/928299/stat /proc/92/stat /proc/930963/stat /proc/931737/stat /proc/933663/stat /proc/935170/stat /proc/936/stat /proc/937317/stat /proc/937324/stat /proc/937922/stat /proc/937/stat /proc/938134/stat /proc/93/stat /proc/941213/stat /proc/941696/stat /proc/942095/stat /proc/942502/stat /proc/943114/stat /proc/943/stat /proc/945108/stat /proc/945173/stat /proc/945385/stat /proc/946547/stat /proc/946/stat /proc/948376/stat /proc/949052/stat /proc/949375/stat /proc/949775/stat /proc/94/stat /proc/950281/stat /proc/950/stat /proc/951/stat /proc/952479/stat /proc/952/stat /proc/953694/stat /proc/95501/stat /proc/955/stat /proc/958551/stat /proc/959515/stat /proc/95/stat /proc/960883/stat /proc/961127/stat /proc/962788/stat /proc/963655/stat /proc/964028/stat /proc/964/stat /proc/965289/stat /proc/965887/stat /proc/967706/stat /proc/967712/stat /proc/967716/stat /proc/967729/stat /proc/96/stat /proc/971749/stat /proc/971756/stat /proc/973171/stat /proc/973281/stat /proc/973290/stat /proc/973768/stat /proc/973921/stat /proc/974193/stat /proc/975244/stat /proc/976228/stat /proc/977017/stat /proc/977271/stat /proc/977766/stat /proc/977808/stat /proc/978071/stat /proc/978/stat /proc/979004/stat /proc/979011/stat /proc/979572/stat /proc/979981/stat /proc/979986/stat /proc/980011/stat /proc/980012/stat /proc/980037/stat /proc/980198/stat /proc/980207/stat /proc/980208/stat /proc/980215/stat /proc/980935/stat /proc/981059/stat /proc/981298/stat /proc/982006/stat /proc/982041/stat /proc/982049/stat /proc/983105/stat /proc/984152/stat /proc/984830/stat /proc/985556/stat /proc/985848/stat /proc/987046/stat /proc/98/stat /proc/990627/stat /proc/992264/stat /proc/992606/stat /proc/994370/stat /proc/995242/stat /proc/995501/stat /proc/996315/stat /proc/996317/stat /proc/996319/stat /proc/996320/stat /proc/996329/stat /proc/996529/stat /proc/996547/stat /proc/996548/stat /proc/996563/stat /proc/997211/stat /proc/997529/stat /proc/99/stat
  1077689: 0 awk awk { pid=$1; sub(/^[0-9]+ \(/,"",$0); n=index($0,")"); comm=substr($0,1,n-1); rest=substr($0,n+2); split(rest,a," "); print pid"\t"comm"\t"(a[12]+a[13])"\t"a[20]"\t"a[18]"\t"a[2] }
doctor pid=1010704 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1010704: 18 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1073720: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-load-gate --test
  1073759: 1 bash bash /home/mesh-home/.local/bin/mesh-load-gate --test
  1079102: 0 bash bash /home/mesh-home/.local/bin/mesh-load-gate e2e-plain 92.34
  1079489: 0 bash bash /home/mesh-home/.local/bin/mesh-load-gate e2e-plain 92.34
  1079510: 0 bash bash /home/mesh-home/.local/bin/mesh-load-gate e2e-plain 92.34
  1079543: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-load-gate e2e-plain 92.34
  1079566: 4123168608 bash bash /home/mesh-home/lte-workstation/scripts/uxn/mesh-sexpr-gate --const load-gate k
doctor pid=1011130 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1011130: gone
doctor pid=1012230 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1012230: 18 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1075182: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-lock-holder --test
  1075245: 1 bash bash /home/mesh-home/.local/bin/mesh-lock-holder --test
doctor pid=1013465 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1013465: gone
doctor pid=1013960 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1013960: gone
doctor pid=1014700 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1014700: 18 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1079955: 0 timeout timeout 20 /home/mesh-home/.local/bin/mesh-mains-hum --test
  1079992: 0 python3 python3 /home/mesh-home/.local/bin/mesh-mains-hum --test
  1081397: 0 python /home/mesh-home/grainneukeln/.venv/bin/python -c import numpy
doctor pid=1015373 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1015373: 18 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1078460: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-mca --test
  1078502: 1 bash bash /home/mesh-home/.local/bin/mesh-mca --test
  1084352: 0 bash bash /home/mesh-home/.local/bin/mesh-mca --test
  1084394: 0 bash bash /home/mesh-home/.local/bin/mesh-mca
  1084858: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-mca
doctor pid=1016017 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1016017: 18 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1079280: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-mdns-census --test
  1079359: 1 bash bash /home/mesh-home/.local/bin/mesh-mdns-census --test
  1084805: 0 bash bash /home/mesh-home/.local/bin/mesh-mdns-census
  1085090: 0 bash bash /home/mesh-home/.local/bin/mesh-mdns-census
  1085099: 0 bash bash /home/mesh-home/.local/bin/mesh-mdns-census
  1085293: 0 bash bash /home/mesh-home/.local/bin/mesh-mdns-census
  1085317: 0 bash bash /home/mesh-home/.local/bin/mesh-mdns-census
  1085440: 0 python3 python3 -
doctor pid=1016284 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1016284: 18 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1080041: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-media-scene --test
  1080102: 1 bash bash /home/mesh-home/.local/bin/mesh-media-scene --test
  1084175: 0 bash bash /home/mesh-home/.local/bin/mesh-media-scene --edge
doctor pid=1016818 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1016818: gone
doctor pid=1017255 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1017255: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1080444: 2 timeout timeout 20 /home/mesh-home/.local/bin/mesh-mem-guard --test
  1080456: 2 bash bash /home/mesh-home/.local/bin/mesh-mem-guard --test
  1081506: 1 bash bash /home/mesh-home/.local/bin/mesh-mem-guard --test
  1081526: 1 bash bash /home/mesh-home/.local/bin/mesh-promises
  1085638: 0 python3 python3 - report /tmp/tmp.NTTk7NXyOO/td.mesh-mem-guard/tmp.gHtOoRlq0y/board 2026-09-14T03:24:50Z 24 6 1
doctor pid=1018348 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1018348: gone
doctor pid=1018856 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1018856: gone
doctor pid=1019236 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1019236: gone
doctor pid=1020063 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1020063: gone
doctor.log mtime=2026-09-14T03:24:03.120417+00:00 size=5564929
doctor.log tail:
2026-09-14T03:23:01Z  [33mWARN[0m mic DEFAULT device broken/busy (use -D plughw:N,M)
2026-09-14T03:23:01Z  [33mWARN[0m untimed peer-SSH — hangs on a dead peer:mesh-load-audit
2026-09-14T03:23:01Z  [33mWARN[0m 6 bypass(es) of 1 declared sole-path funnel(s) — the rule is recited but the arrangement is broken: librosa-analysis<- mesh-song-verify:94 librosa-analysis<- mesh-song-verify:95 librosa-analysis<- mesh-song-verify:102 librosa-analysis<- mesh-song-verify:109 librosa-analysis<- mesh-song-verify:111 librosa-analysis<- mesh-song-verify:114 
2026-09-14T03:23:01Z  [33mWARN[0m 5 site(s) render absence as a negative reading (absent path and bad reading → the SAME verdict word): A mesh-body-backup:452 SZ=0 -> :472 [-lt 20000000] FAIL A mesh-clear-health:41 reactor_age=1789356235 -> :42 [-gt 900] FAIL T mesh-random-track-grind:584 timeout -> :584 FAILED (rc=124 is a state, not a verdict) A mesh-revive:217 n=0 -> :364 [-lt 3] OFFLINE T mesh-say:432 timeout -> :445 FAILED (rc=124 is a state, not a verdict)

### 30-second sample 2026-09-14T03:25:25+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 143 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  958551: 69 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  961127: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  962788: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  963655: 67 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  964028: 67 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  965887: 67 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  971756: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  973768: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  973921: 64 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  974193: 64 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  976228: 64 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  977271: 63 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  977808: 63 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  978071: 63 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  979572: 63 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  979986: 63 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  981059: 62 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  981298: 62 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  982041: 62 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  985556: 61 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  987046: 61 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  990627: 60 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  992264: 59 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  992606: 59 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  994370: 59 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  995501: 58 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  997211: 58 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  997529: 58 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1000664: 57 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1001934: 57 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1003970: 56 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1004502: 56 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1004983: 56 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1006080: 55 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1009749: 54 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1010069: 54 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1010704: 54 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1012230: 54 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1014700: 53 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1015373: 53 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1016284: 53 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1017255: 52 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1020538: 51 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1021147: 51 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1024529: 50 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1025848: 50 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1026858: 50 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1028038: 49 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1029311: 49 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1034881: 48 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1035281: 47 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1042665: 45 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1043502: 45 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1047365: 44 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1051978: 43 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1057785: 42 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1058257: 41 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1061303: 41 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1063924: 40 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1065515: 39 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1066742: 39 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1067512: 39 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1067889: 39 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1068505: 38 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1069729: 38 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1070593: 38 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1072797: 37 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1073973: 37 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1081163: 35 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1081707: 35 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1082796: 35 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085252: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085283: 29 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085337: 33 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085385: 30 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085411: 25 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085469: 32 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085508: 32 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085563: 32 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085567: 24 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085642: 24 timeout timeout 25 /home/mesh-home/.local/bin/mesh-exit-node-lan-heal --test
  1085654: 26 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085664: 26 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085711: 28 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085743: 27 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085791: 24 bash bash /home/mesh-home/.local/bin/mesh-exit-node-lan-heal --test
  1085798: 27 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085811: 27 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085925: 32 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085936: 26 timeout timeout 12 /home/mesh-home/.local/bin/mesh-restore --test
  1086009: 34 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1086024: 23 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1086084: 25 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1086140: 30 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1086160: 23 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1086204: 27 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1086220: 23 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1086231: 26 bash bash /home/mesh-home/.local/bin/mesh-restore --test
  1086234: 30 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1086253: 22 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1086263: 24 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1086266: 26 timeout timeout 20 /home/mesh-home/.local/bin/mesh-mlme-tap --test
  1086397: 26 bash bash /home/mesh-home/.local/bin/mesh-mlme-tap --test
  1086464: 23 timeout timeout 25 /home/mesh-home/.local/bin/mesh-fitness --test
  1086733: 26 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1086766: 23 bash bash /home/mesh-home/.local/bin/mesh-fitness --test
  1087614: 22 timeout timeout 25 /home/mesh-home/.local/bin/mesh-forage --test
  1087712: 22 bash bash /home/mesh-home/.local/bin/mesh-forage --test
  1087855: 22 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1088100: 22 bash bash /home/mesh-home/.local/bin/mesh-forage --test
  1088139: 22 timeout timeout 25 /home/mesh-home/.local/bin/mesh-fsnotify --test
  1088311: 22 bash bash /home/mesh-home/.local/bin/mesh-fsnotify --test
  1088711: 22 timeout timeout 25 /home/mesh-home/.local/bin/mesh-fswriter --test
  1088763: 22 python3 python3 /home/mesh-home/.local/bin/mesh-fswriter --test
  1089279: 22 bash bash /home/mesh-home/.local/bin/mesh-forage --json
  1091052: 22 timeout timeout 25 /home/mesh-home/.local/bin/mesh-generate --test
  1091111: 22 bash bash /home/mesh-home/.local/bin/mesh-generate --test
  1091153: 22 bash bash /home/mesh-home/.local/bin/mesh-forage --json
  1091196: 22 bash bash /home/mesh-home/.local/bin/mesh-forage --json
  1091268: 21 bash bash /home/mesh-home/.local/bin/mesh-promises --json
  1092162: 21 timeout timeout 20 /home/mesh-home/.local/bin/mesh-mind-compact --test
  1092242: 21 bash bash /home/mesh-home/.local/bin/mesh-mind-compact --test
  1093623: 21 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1094189: 21 bash bash /home/mesh-home/.local/bin/mesh-mind-compact --test
  1094621: 21 timeout timeout 12 /home/mesh-home/.local/bin/mesh-route-events --test
  1094716: 21 bash bash /home/mesh-home/.local/bin/mesh-route-events --test
  1097200: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-gmail-note3 --test
  1097234: 20 python3 python3 /home/mesh-home/.local/bin/mesh-gmail-note3 --test
  1097564: 20 python3 python3 - json /home/mesh-home/.mesh/chat.log 2026-09-14T03:25:03Z 24 6 1
  1099369: 19 timeout timeout 25 /home/mesh-home/.local/bin/mesh-guardian --test
  1099439: 19 bash bash /home/mesh-home/.local/bin/mesh-guardian --test
  1099441: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1100051: 19 timeout timeout 25 /home/mesh-home/.local/bin/mesh-guitar-watch --test
  1100087: 19 bash bash /home/mesh-home/.local/bin/mesh-guitar-watch --test
  1100180: 19 timeout timeout 25 /home/mesh-home/.local/bin/mesh-handoff --test
  1100235: 19 bash bash /home/mesh-home/.local/bin/mesh-handoff --test
  1100559: 19 bash bash /home/mesh-home/.local/bin/mesh-guitar-watch --test
  1102174: 19 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1102266: 19 timeout timeout 25 /home/mesh-home/.local/bin/mesh-heartbeat --test
  1102332: 18 bash bash /home/mesh-home/.local/bin/mesh-heartbeat --test
  1103764: 18 timeout timeout 25 /home/mesh-home/.local/bin/mesh-hh-drive --test
  1103792: 18 bash bash /home/mesh-home/.local/bin/mesh-hh-drive --test
  1104232: 18 timeout timeout 25 /home/mesh-home/.local/bin/mesh-hire-scan --test
  1104328: 18 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --test
  1104503: 18 timeout timeout 25 /home/mesh-home/.local/bin/mesh-hire-submit --test
  1104558: 18 bash bash /home/mesh-home/.local/bin/mesh-hire-submit --test
  1105467: 18 timeout timeout 20 /home/mesh-home/.local/bin/mesh-pidfile.sh --test
  1105493: 18 bash bash /home/mesh-home/.local/bin/mesh-pidfile.sh --test
  1105781: 18 bash bash /home/mesh-home/.local/bin/mesh-hire-submit --test
  1105829: 18 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --repo trovu/trovu
  1106167: 18 timeout timeout 20 /home/mesh-home/.local/bin/mesh-pkg-watch --test
  1106248: 17 bash bash /home/mesh-home/.local/bin/mesh-pkg-watch --test
  1106291: 17 timeout timeout 25 /home/mesh-home/.local/bin/mesh-homeostasis --test
  1106348: 17 bash bash /home/mesh-home/.local/bin/mesh-homeostasis --test
  1106480: 17 bash bash /home/mesh-home/.local/bin/mesh-pkg-watch --test
  1106811: 17 timeout timeout 25 /home/mesh-home/.local/bin/mesh-home-state --test
  1106886: 17 bash bash /home/mesh-home/.local/bin/mesh-home-state --test
  1106976: 17 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1107145: 17 timeout timeout 20 /home/mesh-home/.local/bin/mesh-plan-idle --test
  1107224: 17 bash bash /home/mesh-home/.local/bin/mesh-plan-idle --test
  1107376: 17 bash bash /home/mesh-home/.local/bin/mesh-plan-idle --test
  1107422: 17 bash bash /home/mesh-home/.local/bin/mesh-plan-idle --test
  1108042: 17 timeout timeout 25 /home/mesh-home/.local/bin/mesh-hw-fault-watch --test
  1108080: 17 bash bash /home/mesh-home/.local/bin/mesh-hw-fault-watch --test
  1108298: 17 timeout timeout 25 /home/mesh-home/.local/bin/mesh-hw-health --test
  1108312: 17 bash bash /home/mesh-home/.local/bin/mesh-hw-health --test
  1109172: 17 timeout timeout 25 /home/mesh-home/.local/bin/mesh-ideate --test
  1109287: 17 bash bash /home/mesh-home/.local/bin/mesh-ideate --test
  1109611: 17 timeout timeout 20 /home/mesh-home/.local/bin/mesh-precision --test
  1109679: 17 bash bash /home/mesh-home/.local/bin/mesh-precision --test
  1109708: 17 bash bash /home/mesh-home/.local/bin/mesh-plan-idle --test
  1109737: 17 grep grep -oE \[(done|taking|dispatch|evaporated)\][^]]*[a-z][a-z0-9-]*/[a-z0-9-]+ /home/mesh-home/.mesh/chat.log
  1109738: 17 grep grep -oE [a-z][a-z0-9-]*/[a-z0-9-]+
  1109812: 17 sort sort -u
  1110238: 6 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-records/tmp.hHQ0S2RlYo/src/probe.wav
  1110242: 6 bash bash /home/mesh-home/.local/bin/mesh-roll-call
  1110246: 13 timeout timeout 25 /home/mesh-home/.local/bin/mesh-journal-watch --test
  1110250: 13 bash bash /home/mesh-home/.local/bin/mesh-quota --test
  1110252: 6 awk awk -F\t -v m=minds $3==m {printf "x%s — %s\n", $1, $4; exit}
  1110254: 8 bash bash /home/mesh-home/.local/bin/mesh-spend --tokens --json
  1110258: 5 timeout timeout 25 /home/mesh-home/.local/bin/mesh-misha-eye-contact --test
  1110259: 14 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110262: 7 bash bash /home/mesh-home/.local/bin/mesh-mem-guard --test
  1110264: 0 bash bash /home/mesh-home/.local/bin/mesh-queue-tend
  1110269: 5 bash bash /home/mesh-home/.local/bin/mesh-stop-check
  1110271: 7 python /home/mesh-home/grainneukeln/.venv/bin/python - /tmp/tmp.NTTk7NXyOO/td.mesh-soundscape/tmp.4PRKj0TRDE.wav 3,12,0 0.006 scan
  1110272: 8 timeout timeout 40 bash /home/mesh-home/.local/bin/mesh-heartbeat --rejoin
  1110278: 0 bash bash /home/mesh-home/.local/bin/mesh-tell --test
  1110291: 7 grep grep ^WINNER
  1110295: 0 bash bash /home/mesh-home/.local/bin/mesh-interruptibility --test
  1110300: 0 bash bash /home/mesh-home/.local/bin/mesh-room-reflex --test
  1110303: 12 bash bash /home/mesh-home/.local/bin/mesh-labor --test
  1110310: 0 bash bash /home/mesh-home/.local/bin/mesh-job-calls --test
  1110316: 0 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --repo trovu/trovu
  1110326: 5 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110328: 13 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --test
  1110330: 14 bash bash /home/mesh-home/.local/bin/mesh-ideate --test
  1110331: 6 bash bash /home/mesh-home/.local/bin/mesh-roll-call --test
  1110332: 8 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110333: 2 timeout timeout 25 /home/mesh-home/.local/bin/mesh-music-session --test
  1110341: 10 sleep sleep 60
  1110342: 6 timeout timeout 20 /home/mesh-home/.local/bin/mesh-room-address --test
  1110343: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-quota-react --test
  1110348: 0 bash bash /home/mesh-home/.local/bin/mesh-embed --cos ZOMBIE: wire mesh-zzz to mesh-www aggregator (field: fusion) [taking] ACTIVE-CLAIM kelvin telemetry probe — on it
  1110349: 9 bash bash /home/mesh-home/.local/bin/mesh-selfcare --test
  1110351: 9 timeout timeout 25 /home/mesh-home/.local/bin/mesh-load-gate --test
  1110353: 16 timeout timeout 12 /home/mesh-home/.local/bin/mesh-sense-reception --test
  1110357: 8 bash bash /home/mesh-home/.local/bin/mesh-ss-connections --test
  1110359: 11 bash bash /home/mesh-home/.local/bin/mesh-social-context --test
  1110360: 11 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110361: 12 bash bash /home/mesh-home/.local/bin/mesh-quota-react --test
  1110362: 8 bash bash /home/mesh-home/.local/bin/mesh-lock-holder --test
  1110363: 6 bash bash /home/mesh-home/.local/bin/mesh-stranger-watch --test
  1110364: 12 bash bash /home/mesh-home/.local/bin/mesh-quota-react --test
  1110370: 3 sh sh /home/mesh-home/.local/bin/mesh-steward-deadman --check
  1110377: 1 ffmpeg ffmpeg -hide_banner -loglevel error -y -f lavfi -i sine=frequency=440:duration=0.2 -ar 22050 -ac 1 /tmp/tmp.NTTk7NXyOO/td.mesh-say/mtts-play-MzF7zi.wav
  1110378: 10 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110382: 0 bash bash /home/mesh-home/.local/bin/mesh-job-calls --test
  1110383: 0 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --repo trovu/trovu
  1110384: 7 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110389: 15 timeout timeout 25 /home/mesh-home/.local/bin/mesh-interruptibility --test
  1110390: 8 timeout timeout 12 /home/mesh-home/.local/bin/mesh-ss-test --test
  1110400: 10 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110402: 1 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --test
  1110404: 9 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110406: 1 sleep sleep 8
  1110409: 3 bash bash /home/mesh-home/.local/bin/mesh-synergy --test
  1110413: 15 timeout timeout 20 /home/mesh-home/.local/bin/mesh-prior-art --test
  1110417: 12 timeout timeout 25 /home/mesh-home/.local/bin/mesh-job-track --test
  1110419: 1 timeout timeout 25 /home/mesh-home/.local/bin/mesh-overhear --test
  1110427: 7 bash bash /home/mesh-home/.local/bin/mesh-load-audit --test
  1110429: 9 bash bash /home/mesh-home/.local/bin/mesh-load-gate --test
  1110431: 5 timeout timeout 20 mesh-promises --json
  1110435: 1 bash bash /home/mesh-home/.local/bin/mesh-tts --test
  1110436: 3 timeout timeout 12 /home/mesh-home/.local/bin/mesh-sync-tools --test
  1110437: 0 gh gh api repos/trovu/trovu/contents/.github/pull_request_template.md
  1110439: 16 bash bash /home/mesh-home/.local/bin/mesh-sense-reception --test
  1110441: 10 python3 python3 /home/mesh-home/.local/bin/mesh-gmail-note3 --json --list 0 --since 3
  1110447: 4 bash bash /home/mesh-home/.local/bin/mesh-misha-wake --test
  1110449: 4 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110450: 13 timeout timeout 20 /home/mesh-home/.local/bin/mesh-queue-tend --test
  1110458: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-room-gigaam --test
  1110460: 11 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110462: 7 bash bash /home/mesh-home/.local/bin/mesh-labor --feed
  1110465: 7 bash bash /home/mesh-home/.local/bin/mesh-load-audit --json
  1110468: 7 sed sed -n s/.*"node_conn":\([01]\).*/\1/p
  1110475: 4 sleep sleep 60
  1110477: 6 timeout timeout 20 /home/mesh-home/.local/bin/mesh-room-music --test
  1110482: 8 bash bash /home/mesh-home/.local/bin/mesh-heartbeat --rejoin
  1110484: 0 timeout timeout 10 mesh-phone-ip
  1110486: 13 timeout timeout 25 /home/mesh-home/.local/bin/mesh-job-mail --test
  1110487: 1 bash bash /home/mesh-home/.local/bin/mesh-revive --check
  1110488: 0 bash bash /home/mesh-home/.local/bin/mesh-labor --json
  1110489: 2 bash bash /home/mesh-home/.local/bin/mesh-music-session --test
  1110490: 1 python3 python3 - journal /tmp/tmp.NTTk7NXyOO/td.mesh-promises/tmp.7BZxpZRpDr/tmp.MI1adxcabo/board 2026-07-24T12:00:00Z 24 6 1 /tmp/tmp.NTTk7NXyOO/td.mesh-promises/tmp.7BZxpZRpDr/tmp.MI1adxcabo/j.journal
  1110494: 6 bash bash /home/mesh-home/.local/bin/mesh-room-address --test
  1110495: 0 flock flock -w 1 9
  1110497: 8 bash bash /home/mesh-home/.local/bin/mesh-load-attrib --test
  1110499: 5 bash bash /home/mesh-home/.local/bin/mesh-misha-eye-contact --test
  1110500: 15 bash bash /home/mesh-home/.local/bin/mesh-prior-art --test
  1110502: 0 bash bash /home/mesh-home/.local/bin/mesh-mlme-tap --daemon
  1110506: 10 bash bash /home/mesh-home/.local/bin/mesh-socket-state --test
  1110511: 0 bash bash /home/mesh-home/.local/bin/mesh-relay-attest record groq llama-3.1-8b who are you I am an assistant
  1110515: 1 bash bash /home/mesh-home/.local/bin/mesh-psi --test
  1110519: 12 python3 python3 /home/mesh-home/.local/bin/mesh-job-track --test
  1110522: 2 bash bash /home/mesh-home/.local/bin/mesh-sense-reception
  1110524: 2 bash bash /home/mesh-home/.local/bin/mesh-synergy --test
  1110526: 13 bash bash /home/mesh-home/.local/bin/mesh-queue-tend --test
  1110529: 8 bash bash /home/mesh-home/.local/bin/mesh-load-attrib --test
  1110538: 1 bash bash /home/mesh-home/.local/bin/mesh-psi
  1110540: 1 python /home/mesh-home/.venv-ai/bin/python -
  1110543: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110545: 13 python3 python3 /home/mesh-home/.local/bin/mesh-job-mail --test
  1110546: 6 bash bash /home/mesh-home/.local/bin/mesh-roll-call
  1110549: 6 bash bash /home/mesh-home/.local/bin/mesh-room-music --test
  1110550: 0 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1110553: 7 bash bash /home/mesh-home/.local/bin/mesh-ledger --price-window 5
  1110554: 15 bash bash /home/mesh-home/.local/bin/mesh-interruptibility --test
  1110556: 0 bash bash /home/mesh-home/.local/bin/mesh-mind-state --test
  1110561: 14 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110563: 1 mesh-room-gigaa /home/mesh-home/.venv-ai/bin/python /home/mesh-home/.local/bin/mesh-room-gigaam --test
  1110567: 9 bash bash /home/mesh-home/.local/bin/mesh-report --test
  1110569: 3 timeout timeout 12 /home/mesh-home/.local/bin/mesh-sweep-rollcall-proposes --test
  1110572: 2 timeout timeout 12 /home/mesh-home/.local/bin/mesh-tailscaled-heal --test
  1110577: 5 bash bash /home/mesh-home/.local/bin/mesh-mind-control --test
  1110578: 7 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --test
  1110588: 15 bash bash /home/mesh-home/.local/bin/mesh-guitar-watch --test
  1110590: 0 bash bash /home/mesh-home/.local/bin/mesh-body-motion
  1110592: 9 timeout timeout 25 /home/mesh-home/.local/bin/mesh-load-audit --test
  1110594: 1 sleep sleep 5
  1110597: 7 bash bash /home/mesh-home/.local/bin/mesh-spend --tokens --json
  1110598: 7 bash bash /home/mesh-home/.local/bin/mesh-ledger --price-window 5
  1110601: 10 timeout timeout 12 /home/mesh-home/.local/bin/mesh-song-verify --test
  1110607: 2 timeout timeout 25 /home/mesh-home/.local/bin/mesh-music-fanout --test
  1110609: 1 bash bash /home/mesh-home/.local/bin/mesh-tts --test
  1110612: 15 timeout timeout 20 /home/mesh-home/.local/bin/mesh-promises --test
  1110615: 0 timeout timeout 12 /home/mesh-home/.local/bin/mesh-tcp-metrics --test
  1110616: 10 timeout timeout 20 /home/mesh-home/.local/bin/mesh-relay --test
  1110617: 1 bash bash /home/mesh-home/.local/bin/mesh-overhear --test
  1110618: 16 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110624: 0 bash bash /home/mesh-home/.local/bin/mesh-stress --json
  1110625: 4 sleep sleep 8
  1110628: 2 python3 python3 -c  import sys, os, itertools, statistics, collections, datetime, random TAPE=sys.argv[1]; TOP=int(sys.argv[2]); NULLS=int(sys.argv[3]) LEVELS=int(sys.argv[4]) if len(sys.argv)>4 else 0 MISSING={"NOLOG","STALE","UNKNOWN","","-","n/a","na","?"}   # honest-fusion: not a value, never a level FOLDS=5; MINN=int(os.environ.get("SYNERGY_MINN","200")) recs=[]; names=None try: fh=open(TAPE) except OSError as e: print("tape unreadable: %s"%e); sys.exit(2) for line in fh:     line=line.rstrip("\n")     if not line or line.startswith("#"): continue     f=line.split("\t")     if names is None: names=f; continue     if len(f)!=len(names): continue     try: t=datetime.datetime.strptime(f[0],"%Y-%m-%dT%H:%M:%SZ")     except ValueError: continue     recs.append((t,f)) if names is None or len(recs)<MINN:     print("tape carries %d usable rows (< %d) — UNKNOWN, not a null result"%(len(recs),MINN)); sys.exit(2) recs.sort(key=lambda r:r[0]) SENSES=names[1:]; NS=len(SENSES); N=len(recs) # LEVELS>0 quantile-bins any column whose readings are all numbers. A quantity has to be discretised # before a cell-counting model can hold it, and THE NUMBER OF LEVELS IS THE EXPERIMENT: this census # came back null on a tape of verdicts already coarsened to 2-10 categories upstream, so re-asking the # same question at several resolutions is how you tell a quiet sensorium from a tape that threw the # signal away. Edges come from the columns OWN marginal distribution and carry no information about # any target, so binning cannot leak the answer into the fold. codes=[]; alpha=[]; present=[]; kinds=[] for j in range(NS):     raw=[(f[j+1] if j+1<len(f) else "") for t,f in recs]     vals=[v for v in raw if v not in MISSING]     numeric=bool(vals) and LEVELS>0     if numeric:         try: nv=[float(v) for v in vals]         except ValueError: numeric=False     if numeric:         sv=sorted(nv)         edges=[sv[int(q*(len(sv)-1))] for q in [i/LEVELS for i in range(1,LEVELS)]]         edges=sorted(set(edges))         def lvl(x,e=edges):             k=0             for b in e:                 if x>b: k+=1                 else: break             return k         c=[]         for v in raw:             c.append(-1 if v in MISSING else lvl(float(v)))         codes.append(c); alpha.append(len(set(x for x in c if x>=0))); kinds.append("q%d"%LEVELS)     else:         m={}; c=[]         for v in raw: c.append(-1 if v in MISSING else m.setdefault(v,len(m)))         codes.append(c); alpha.append(len(m)); kinds.append("tok")     present.append(sum(1 for x in c if x>=0)) gaps=[(recs[i+1][0]-recs[i][0]).total_seconds() for i in range(N-1)] cad=statistics.median(gaps) if gaps else 0 MAXGAP=2.5*cad if cad>0 else 0 # ADJACENCY: a successor exists only if the next row is really the next TICK. A hole in the tape on a # node that power-cycles is an OUTAGE, not a slow sample; pairing across it invents a transition. succ=[(i+1) if (i+1<N and MAXGAP>0 and 0<(recs[i+1][0]-recs[i][0]).total_seconds()<=MAXGAP) else -1       for i in range(N)] adj=sum(1 for s in succ if s>=0) print("tape        : %s"%TAPE) print("coverage    : rows=%d  span=%sZ..%sZ  cadence_median=%.0fs  adjacent_successors=%d/%d (%.1f%%)"       %(N,recs[0][0].isoformat(),recs[-1][0].isoformat(),cad,adj,N,100.0*adj/N)) print("axes        : "+"  ".join("%s[%s](k=%d,%.0f%%)"%(s,kd,a,100.0*p/N) for s,kd,a,p in zip(SENSES,kinds,alpha,present)))  def census(shift):     res=[]     for T in range(NS):         cT=codes[T]         for A,B in itertools.combinations([j for j in range(NS) if j!=T],2):             cA=codes[A]             cB=codes[B] if shift==0 else codes[B][shift:]+codes[B][:shift]             idx=[i for i in range(N) if succ[i]>=0 and cT[i]>=0 and cA[i]>=0 and cB[i]>=0 and cT[succ[i]]>=0]             n=len(idx)             if n<MINN: continue             y=[cT[succ[i]] for i in idx]             kp=[(cT[i],) for i in idx]; ka=[(cT[i],cA[i]) for i in idx]             kb=[(cT[i],cB[i]) for i in idx]; kj=[(cT[i],cA[i],cB[i]) for i in idx]             hits={"persist":0,"+A":0,"+B":0,"+AB":0}             fold=n//FOLDS             for f in range(FOLDS):                 lo=f*fold; hi=(f+1)*fold if f<FOLDS-1 else n                 tr=list(range(0,lo))+list(range(hi,n))                 tab={}                 for nm,k in (("persist",kp),("+A",ka),("+B",kb),("+AB",kj)):                     d=collections.defaultdict(collections.Counter)                     for p in tr: d[k[p]][y[p]]+=1                     tab[nm]={kk:cc.most_common(1)[0][0] for kk,cc in d.items()}                 gc=collections.Counter(y[p] for p in tr).most_common(1)[0][0]                 for p in range(lo,hi):                     # BACKOFF: an unseen cell falls back to its parent model, never to a guess — so the                     # joint model is never punished for sparsity it can route around, and never rewarded                     # for cells it has not actually seen.                     pr=tab["persist"].get(kp[p],gc)                     if pr==y[p]: hits["persist"]+=1                     for nm,k in (("+A",ka),("+B",kb)):                         v=tab[nm].get(k[p]); v=pr if v is None else v                         if v==y[p]: hits[nm]+=1                     v=tab["+AB"].get(kj[p])                     if v is None: v=tab["+A"].get(ka[p],pr)                     if v==y[p]: hits["+AB"]+=1             acc={k:v/n for k,v in hits.items()}             base=max(acc["persist"],acc["+A"],acc["+B"])             # the single-axis control is scored on the B LEG ALONE, because B is the only column the null             # shifts. Scoring it on max(+A,+B) would leave the real A->target relation inside the null             # itself, and the control line would then be inflated by the very signal it is meant to             # measure — it read +0.1141 that way, high enough to swallow every real single-axis gain.             res.append((acc["+AB"]-base,T,A,B,n,acc,acc["+B"]-acc["persist"]))     res.sort(reverse=True)     return res  real=census(0) if not real:     print("no triple reaches the %d-sample floor on common support — UNKNOWN, not a null result"%MINN); sys.exit(2) random.seed(20260830) shifts=sorted(random.sample(range(N//8,N-N//8),min(NULLS,max(1,N//4)))) nulls=[census(s) for s in shifts] gains=[g for g,_,_,_,_,_,_ in real] nullgains=sorted([g for c in nulls for g,_,_,_,_,_,_ in c],reverse=True) # THE SECOND QUESTION, and it is the one that says what a null joint result MEANS. If no single axis # beats persistence either, the tape carries no learnable structure at all and "no synergy" is a # statement about stickiness, not about fusion. If single axes DO beat it while pairs add nothing, # then correlation genuinely buys nothing here and the finding is about fusion. sgains=[sg for _,_,_,_,_,_,sg in real] snull=[sg for c in nulls for _,_,_,_,_,_,sg in c] srepmax=[max(sg for _,_,_,_,_,_,sg in c) if c else float("-inf") for c in nulls] sthr=max(srepmax) def q(sorted_desc,p):     if not sorted_desc: return float("nan")     i=int(p*(len(sorted_desc)-1)); return sorted_desc[i] # THE FINDING LINE — family-wise, re-derived each run from THIS corpus own null, never pinned. The # census asks the same question of HUNDREDS of triples, so a per-triple 99th percentile is guaranteed to # hand back ~1% of them as findings even when nothing is there — it did exactly that on the tool own # arm-7 fixture (252 triples, one spurious EARNED). The line that survives a census is the null MAXIMUM # PER REPLICATE: the largest gain a whole pass over relation-free data can produce. Clearing it means # clearing the best thing chance built out of this many triples, not the best thing chance built out of # one. Conservative by construction, and that is the correct direction for an instrument whose null # result is itself the publishable answer. repmax=[max(g for g,_,_,_,_,_,_ in c) if c else float("-inf") for c in nulls] thr=max(repmax) thr_rule="largest joint gain any of %d relation-free passes produced over %d triples each — family-wise, not per-triple"%(len(nulls),len(real)) print("triples     : %d real / %d null (circular shifts of B at rows %s; marginals AND autocorrelation preserved)"       %(len(real),len(nullgains),",".join(map(str,shifts)))) print("finding line: joint gain > %+.4f  (%s)"%(thr,thr_rule)) hdr="%-16s%-16s%-16s%7s%9s%8s%8s%8s%9s"%("target","A","B","n","persist","+A","+B","+AB","joint") print("") for th in (0.0,0.005,0.01,0.02,0.05):     nr=sum(1 for g in gains if g>th); nn=sum(1 for g in nullgains if g>th)/max(1,len(nulls))     print("  joint gain > %+.3f : real %4d   null %6.1f (mean of %d replicates)"%(th,nr,nn,len(nulls))) found=[r for r in real if r[0]>thr] sfound=[r for r in real if r[6]>sthr] print("") print("single-axis control (does ONE axis beat persistence? if not, a null joint result is about the") print("tape being sticky, not about fusion):") print("  best single gain: %+.4f   line: %+.4f   clearing it: %d of %d triples"%(max(sgains) if sgains else float("nan"),sthr,len(sfound),len(real))) print("") print("VERDICT     : %s"%("EARNED — %d triple(s) clear the null line"%len(found) if found else       "INDISTINGUISHABLE FROM NULL — no pair on this tape carries joint information; a fused sense built on these axes would report its own noise")) print("") print("top %d by joint gain (a pair must beat persistence AND each single axis):"%TOP) print(hdr) for g,T,A,B,n,a,sg in real[:TOP]:     mark=" *" if g>thr else ""     print("%-16s%-16s%-16s%7d%9.4f%8.4f%8.4f%8.4f%+9.4f%s"%(SENSES[T],SENSES[A],SENSES[B],n,           a["persist"],a["+A"],a["+B"],a["+AB"],g,mark)) sys.exit(0 if found else 1)  /tmp/tmp.NTTk7NXyOO/td.mesh-synergy/tmp.KSntOlL8O9/planted.tsv 5 3
  1110631: 3 bash bash /home/mesh-home/.local/bin/mesh-sync-tools --test
  1110634: 6 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110639: 1 bash bash /home/mesh-home/.local/bin/mesh-tts --test-play
  1110641: 7 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --scope
  1110642: 15 bash bash /home/mesh-home/.local/bin/mesh-guitar-watch --test
  1110644: 15 timeout timeout 20 /home/mesh-home/.local/bin/mesh-promises.bak-20260912-witness --test
  1110654: 2 sleep sleep 3
  1110655: 15 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-guitar-watch/tmp.TKjWoEnDBY/tmp.S7SkKiV87Y/tone.wav
  1110656: 0 timeout timeout 18 ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=6 -o StrictHostKeyChecking=accept-new u0_a380@192.168.8.203 timeout 12 termux-sensor -s bma420,ORIENTATION,STEP_COUNTER,LINEARACCEL,GYROSCOPE,tmd2755_l,tmd2755_p -n 2
  1110665: 6 timeout timeout 25 /home/mesh-home/.local/bin/mesh-mains-hum --test
  1110667: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-storage-health --test
  1110668: 3 timeout timeout 12 /home/mesh-home/.local/bin/mesh-swap-rate --test
  1110673: 8 bash bash /home/mesh-home/.local/bin/mesh-ss-test --test
  1110676: 0 bash bash /home/mesh-home/.local/bin/mesh-mind-state --test
  1110678: 5 bash bash /home/mesh-home/.local/bin/mesh-promises --json
  1110681: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110686: 0 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1110691: 15 bash bash /home/mesh-home/.local/bin/mesh-promises --test
  1110697: 3 bash bash /home/mesh-home/.local/bin/mesh-generate --run-with-test-files
  1110700: 6 timeout timeout 20 /home/mesh-home/.local/bin/mesh-room-context --test
  1110708: 5 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110710: 3 bash bash /home/mesh-home/.local/bin/mesh-fsnotify --window 4 --debounce 0 /tmp/tmp.NTTk7NXyOO/td.mesh-promises-watch/tmp.IovDIfp5Bd/watched -- true
  1110712: 0 bash bash /home/mesh-home/.local/bin/mesh-peer-addr Redmi
  1110713: 1 bash bash /home/mesh-home/.local/bin/mesh-roll-call-retire-arm --test
  1110718: 15 bash bash /home/mesh-home/.local/bin/mesh-promises.bak-20260912-witness --test
  1110719: 3 sh sh /home/mesh-home/.local/bin/mesh-steward-deadman --check
  1110721: 3 bash bash /home/mesh-home/.local/bin/mesh-peer-addr router
  1110728: 2 bash bash /home/mesh-home/.local/bin/mesh-room-activity
  1110731: 1 bash bash /home/mesh-home/.local/bin/mesh-study-bridge
  1110732: 9 bash bash /home/mesh-home/.local/bin/mesh-load-audit --test
  1110734: 3 bash bash /home/mesh-home/.local/bin/mesh-sweep-rollcall-proposes --test
  1110735: 2 bash bash /home/mesh-home/.local/bin/mesh-tailscaled-heal --test
  1110746: 11 bash bash /home/mesh-home/.local/bin/mesh-social-context
  1110748: 5 timeout timeout 12 /home/mesh-home/.local/bin/mesh-study-bridge --test
  1110754: 0 timeout timeout 25 /home/mesh-home/.local/bin/mesh-node-care --test
  1110757: 10 bash bash /home/mesh-home/.local/bin/mesh-song-verify --test
  1110760: 3 bash bash /home/mesh-home/.local/bin/mesh-pace --eff-gap 180
  1110762: 15 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110766: 11 timeout timeout 25 /home/mesh-home/.local/bin/mesh-lan-presence --test
  1110770: 2 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110772: 6 python /home/mesh-home/grainneukeln/.venv/bin/python /home/mesh-home/.local/bin/mesh-mains-hum --test
  1110775: 6 bash bash /home/mesh-home/.local/bin/mesh-room-address --test
  1110781: 1 bash bash /home/mesh-home/.local/bin/mesh-roll-call-retire-arm
  1110785: 0 bash bash /home/mesh-home/.local/bin/mesh-tcp-metrics --test
  1110786: 7 timeout timeout 20 /home/mesh-home/.local/bin/mesh-roll-call-retire-arm --test
  1110791: 8 bash bash /home/mesh-home/.local/bin/mesh-stress --json
  1110792: 13 timeout timeout 25 /home/mesh-home/.local/bin/mesh-job-scan --test
  1110793: 3 bash bash /home/mesh-home/.local/bin/mesh-swap-rate --test
  1110794: 3 head head -1
  1110796: 9 timeout timeout 12 /home/mesh-home/.local/bin/mesh-speech-classify --test
  1110807: 2 bash bash /home/mesh-home/.local/bin/mesh-music-fanout --test
  1110810: 9 timeout timeout 20 /home/mesh-home/.local/bin/mesh-resource-guard --test
  1110821: 16 timeout timeout 25 /home/mesh-home/.local/bin/mesh-imac-wifi --test
  1110822: 11 bash bash /home/mesh-home/.local/bin/mesh-social-context --test
  1110823: 3 bash bash /home/mesh-home/.local/bin/mesh-generate --run-with-test-files
  1110827: 0 bash bash /home/mesh-home/.local/bin/mesh-room-context --test
  1110831: 1 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1110832: 0 bash bash /home/mesh-home/.local/bin/mesh-overhear --test
  1110835: 0 bash bash /home/mesh-home/.local/bin/mesh-music-session --test
  1110836: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110838: 9 timeout timeout 12 /home/mesh-home/.local/bin/mesh-spend --test
  1110840: 1 bash bash /home/mesh-home/.local/bin/mesh-reflexes --test
  1110841: 11 timeout timeout 12 mesh-body-motion
  1110842: 0 python3 [python3]
  1110844: 0 python3 python3 -c  import os,re _bindir=os.environ.get("MESH_REFLEXES_BINDIR") or os.path.join(os.environ["HOME"],".local","bin") # Match a tool by the BASENAME of a whole shell token, never by a substring of the path. On THIS node # $HOME is /home/mesh-home, so a path-substring regex reads "mesh-home" out of every single reflex line # and offers it to the header lookup — harmless only for as long as no file named `mesh-home` lands in # the bindir, and it silently ate the first mutation test (a mutant that broke the multi-token scan went # red on the WRONG assertion because "mesh-home" was token #1). Tokenize, basename, then match anchored. _TOOLRE=re.compile(r"^mesh-[a-z0-9][a-z0-9-]*$") _SPLITRE=re.compile(r"[\s;&|()]+") _CADRE=re.compile(r"^#\s*reflex-cadence:\s*(\S+)") _hdrcache={} def header_cadence(tool):     if tool in _hdrcache: return _hdrcache[tool]     v=None     try:         with open(os.path.join(_bindir,tool),errors="replace") as f:             for i,l in enumerate(f):                 if i>200: break                 m=_CADRE.match(l.strip())                 if m: v=m.group(1); break     except Exception:         v=None            # unreadable/absent tool -> NO veto (absence is not a declaration)     _hdrcache[tool]=v; return v def declined_by(g):     """g = a reflex SIGNATURE. -> the tool name declaring reflex-cadence: off, else None.     EVERY mesh-* token is checked, not just the first: the real line is     `mesh-load-gate bruno-watch 11 && ... mesh-bruno-watch --once`, where the veto is on the SECOND."""     if not g: return None     toks=[os.path.basename(x) for x in _SPLITRE.split(g) if x]     for t in dict.fromkeys(x for x in toks if _TOOLRE.match(x)):         c=header_cadence(t)         if c is not None and c.lower()=="off": return t     return None  import sys,re,os from collections import Counter home=os.environ["HOME"] desired_path,live_path,out_path=sys.argv[1],sys.argv[2],sys.argv[3] def sig(line):     s=line.strip()     if not s or s.startswith("#"): return None     s=s.replace("$HOME",home).replace("${HOME}",home)     if s.startswith("@"):         p=s.split(None,1); s=p[1] if len(p)>1 else s     elif re.match(r"^[A-Za-z_][A-Za-z0-9_]*=",s):         pass     else:         p=s.split(None,5); s=p[5] if len(p)>5 else s     s=re.sub(r"\s+#.*$","",s)     s=re.sub(r"\s*(>>?\s*\S+|2>&1|2>\s*\S+)\s*"," ",s)     s=re.sub(r"\s+"," ",s).strip()     return s want={}; dorder=[] for l in open(desired_path).read().splitlines():     if not l.strip() or l.strip().startswith("#"): continue     g=sig(l)     if g is None: continue     if g not in want: dorder.append(g)     want[g]=l # PAUSED scan: a comment line "# PAUSED <slug> ..." opens a pause context over the FOLLOWING # commented-out cron lines (broken by the first blank/non-comment line). Their sigs are DELIBERATELY # paused: never re-added by the self-heal below — else --apply resurrects a paused reflex every # cycle (the phaedra mesh-dispatch case, 2026-07-21). KEEP IN SYNC with sigs --paused. paused=set(); in_pause=False for line in open(live_path).read().splitlines():     st=line.strip()     if re.match(r"^#\s*PAUSED\b",st): in_pause=True; continue     if not st or not st.startswith("#"): in_pause=False; continue     if in_pause:         g=sig(st.lstrip("#").strip())         if g: paused.add(g) # COMMENTED-TWIN scan (WITHHELD). A human who comments a reflex OUT of the live crontab has # withdrawn it — whatever words they wrote in front of it. The PAUSED marker above is ONE spelling # of that; it is not the only one anybody uses, and requiring it made every other spelling a no-op. # MEASURED on this node 2026-08-19: the operator quiesced three GPU reflexes on 2026-07-24 as #   "# GPU-QUIESCE 2026-07-24 operator: */5 * * * * $HOME/.local/bin/mesh-bruno >> ..." # and --apply, running every 5 minutes, read that as ABSENT and re-added all three within the hour. # They have been running for 26 days beside their own commented-out monument (bruno.log was written # 60 s before this was measured). So: a desired reflex whose signature ALSO appears in a # commented-out cron line is WITHHELD — never silently re-added. mesh-autowire already reads a # commented line as protective ("already wired? present in the desired set OR the live crontab" — # its grep matches comments); this makes mesh-reflexes agree with it instead of undoing it. # The schedule need not sit at the start of the comment: the marker text can precede it, so the # cron line is searched for ANYWHERE after the "#" rather than assumed to be the first token. CRONISH=re.compile(r"((?:[-0-9*/,]+\s+){4}[-0-9*/,]+\s+\S.*)$") ATISH=re.compile(r"(@[a-z]+\s+\S.*)$") def commented_sig(line):     st=line.strip()     if not st.startswith("#"): return None     body=st.lstrip("#").strip()     m=CRONISH.search(body) or ATISH.search(body)     if not m: return None     return sig(m.group(1)) commented=set() for line in open(live_path).read().splitlines():     g=commented_sig(line)     if g: commented.add(g) # HEADER VETO. declined_by() comes from DECLINE_PY_CORE, prepended to this source at every call site. import datetime TODAY=datetime.date.today().isoformat() # live, exact-deduped, order-preserving live=[]; seen=set(); deduped=[] for line in open(live_path).read().splitlines():     st=line.strip()     if st=="" or st.startswith("#"):         live.append(("c",line)); continue     if line in seen:         deduped.append(line); continue            # exact-duplicate line -> drop (routine)     seen.add(line); live.append(("x",line)) cnt=Counter(sig(l) for k,l in live if k=="x") out=[]; placed=set(); replaced=[]; collapsed=[] declined_live=[] for k,line in live:     if k=="c":         out.append(line); continue     g=sig(line)     _dt=declined_by(g)     if _dt:         # The tool itself says `off`. Comment the ACTIVE line out in place under a named tombstone —         # the one deactivation --apply performs. NOT a drop: the text survives verbatim behind the         # marker, and commented_sig() reads it back as a withdrawal on the next run.         # NB no apostrophes anywhere in this python source: RECONCILE_PY is a SINGLE-quoted bash         # string, so one quote here terminates it and the whole heredoc lands as a filename.         out.append("# DECLINED-BY-HEADER %s mesh-reflexes: %s declares reflex-cadence: off — %s"%(TODAY,_dt,line.strip()))         declined_live.append((_dt,line)); continue     if g in want and cnt[g]>1:         # TWIN of a desired reflex (the cron-dup case: a reconcile that minted a comment/text twin).         # Collapse to ONE canonical desired line at the FIRST occurrence; drop the later twin(s). This         # is the "REPLACE a reconciled entry rather than append a duplicate" the task asks for.         if g in placed:             collapsed.append(line); continue         placed.add(g); canon=want[g]         if line.strip()!=canon.strip():             out.append(canon); replaced.append(g)         else:             out.append(line)     else:         # SINGLETON (or non-desired) live line -> preserve verbatim. Deliberately do NOT re-pace a         # single live reflex to match the desired schedule: a live-only slow-down not yet written back         # to reflexes.cron (e.g. an operator pacing change) must NOT be silently reverted. Schedule         # reconcile is the operator/steward decision; --apply only de-dups + self-heals missing.         out.append(line)         if g in want: placed.add(g) added=[]; pausedskip=[]; withheld=[]; declined_want=[] for g in dorder:     _dt=declined_by(g)     if _dt:                                        # the tool VETOES itself -> never wire, whatever desired says         declined_want.append((_dt,want[g])); continue     if g not in placed and cnt.get(g,0)==0:        # desired reflex entirely absent from live -> self-heal         if g in paused:                            # ... unless deliberately PAUSED in the live crontab             pausedskip.append(want[g]); continue         if g in commented:                         # ... or commented out under ANY wording (WITHHELD)             withheld.append(want[g]); continue         out.append(want[g]); placed.add(g); added.append(want[g]) deduped=deduped+collapsed open(out_path,"w").write(("\n".join(out)+"\n") if out else "") def nm(ls):     return " ".join(sorted({m for l in ls for m in re.findall(r"mesh-[a-z0-9][a-z0-9-]*",l)})) print("ADDED=%d"%len(added)) print("REPLACED=%d"%len(replaced)) print("DEDUPED=%d"%len(deduped)) print("PAUSED=%d"%len(pausedskip)) print("WITHHELD=%d"%len(withheld)) print("DECLINED=%d"%len(declined_want)) print("DECLINEDOFF=%d"%len(declined_live)) print("DECLINEDNAMES=%s"%" ".join(sorted({t for t,_ in declined_want+declined_live}))) print("DECLINEDSIGS=%s"%"|".join(sorted({sig(l) or l.strip() for _,l in declined_want+declined_live}))) print("CHANGED=%d"%(1 if (added or replaced or deduped or declined_live) else 0)) print("ADDNAMES=%s"%nm(added)) print("ADDSIGS=%s"%"|".join(sorted(sig(l) for l in added))) print("PAUSEDNAMES=%s"%nm(pausedskip)) print("WITHHELDNAMES=%s"%nm(withheld)) print("WITHHELDSIGS=%s"%"|".join(sorted(sig(l) for l in withheld)))  /tmp/tmp.NTTk7NXyOO/td.mesh-reflexes/tmp.FBIIBp4A3Q/desired /home/mesh-home/.mesh/.reflexes.lock.live /home/mesh-home/.mesh/.reflexes.lock.new
  1110855: 5 bash bash /home/mesh-home/.local/bin/mesh-study-bridge --test
  1110858: 6 bash bash /home/mesh-home/.local/bin/mesh-room-context --test
  1110859: 16 bash bash /home/mesh-home/.local/bin/mesh-imac-wifi --test
  1110860: 0 ssh ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=6 -o StrictHostKeyChecking=accept-new u0_a380@192.168.8.203 timeout 12 termux-sensor -s bma420,ORIENTATION,STEP_COUNTER,LINEARACCEL,GYROSCOPE,tmd2755_l,tmd2755_p -n 2
  1110862: 11 timeout timeout 120 /home/mesh-home/.local/bin/mesh-social-context
  1110863: 11 tail tail -1
  1110864: 0 timeout timeout 4 mesh-proc-churn --json
  1110867: 11 bash bash /home/mesh-home/.local/bin/mesh-body-motion
  1110871: 1 timeout timeout 90 /home/mesh-home/.local/bin/mesh-ss-test
  1110872: 11 bash bash /home/mesh-home/.local/bin/mesh-lan-presence --test
  1110874: 3 tr tr -cd 0-9
  1110875: 0 ssh ssh -o ConnectTimeout=6 -o StrictHostKeyChecking=accept-new -o BatchMode=yes root@192.168.8.1 true
  1110878: 10 timeout timeout 25 /home/mesh-home/.local/bin/mesh-leadlag --test
  1110879: 8 bash bash /home/mesh-home/.local/bin/mesh-heartbeat --rejoin
  1110881: 1 bash bash /home/mesh-home/.local/bin/mesh-ss-test
  1110883: 3 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110888: 1 ping ping -c 1 -W 2 192.168.8.1
  1110892: 14 bash bash /home/mesh-home/.local/bin/mesh-promises.bak-20260912-witness --test
  1110899: 15 timeout timeout 20 /home/mesh-home/.local/bin/mesh-promises-watch --test
  1110900: 11 timeout timeout 25 /home/mesh-home/.local/bin/mesh-lan-newdevice --test
  1110907: 0 bash bash /home/mesh-home/.local/bin/mesh-selfcare --test
  1110911: 10 bash bash /home/mesh-home/.local/bin/mesh-relay --test
  1110913: 1 timeout timeout 4 ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@100.103.99.16 echo ok
  1110922: 14 bash bash /home/mesh-home/.local/bin/mesh-hw-health
  1110923: 11 timeout timeout 12 /home/mesh-home/.local/bin/mesh-social-context --test
  1110926: 13 python3 python3 /home/mesh-home/.local/bin/mesh-job-scan --test
  1110932: 1 bash bash /home/mesh-home/.local/bin/mesh-reflexes --apply
  1110939: 10 bash bash /home/mesh-home/.local/bin/mesh-leadlag --test
  1110945: 15 bash bash /home/mesh-home/.local/bin/mesh-promises-watch --test
  1110948: 0 bash bash /home/mesh-home/.local/bin/mesh-misha-eye-contact --test
  1110950: 11 bash bash /home/mesh-home/.local/bin/mesh-social-context
  1110952: 14 bash bash /home/mesh-home/.local/bin/mesh-ideate --test
  1110955: 7 timeout timeout 25 /home/mesh-home/.local/bin/mesh-media-scene --test
  1110957: 9 bash bash /home/mesh-home/.local/bin/mesh-speech-classify --test
  1110958: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-room-address --test
  1110963: 10 timeout timeout 20 /home/mesh-home/.local/bin/mesh-reflex-health --test
  1110976: 6 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-records/tmp.hHQ0S2RlYo/src/probe.wav
  1110977: 9 bash bash /home/mesh-home/.local/bin/mesh-hh-drive --goto https://hh.ru/applicant/negotiations
  1110978: 0 python3 python3 - /tmp/tmp.NTTk7NXyOO/td.mesh-misha-eye-contact/tmp.F3tmEZvKn5/no-such-frame.jpg /home/mesh-home/.mesh/groq.env
  1110982: 14 timeout timeout 25 /home/mesh-home/.local/bin/mesh-job-apply --test
  1110984: 14 bash bash /home/mesh-home/.local/bin/mesh-promises --test
  1110985: 10 bash bash /home/mesh-home/.local/bin/mesh-reflex-health --test
  1110988: 7 bash bash /home/mesh-home/.local/bin/mesh-roll-call-retire-arm --test
  1110989: 7 timeout timeout 20 /home/mesh-home/.local/bin/mesh-roll-call --test
  1110990: 0 bash bash /home/mesh-home/.local/bin/mesh-ss-test
  1110994: 1 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110996: 0 bash bash /home/mesh-home/.local/bin/mesh-node-care --test
  1111000: 3 bash bash /home/mesh-home/.local/bin/mesh-sense-reception --test
  1111004: 9 timeout timeout 25 /home/mesh-home/.local/bin/mesh-ledger --test
  1111011: 9 bash bash /home/mesh-home/.local/bin/mesh-spend --test
  1111014: 0 timeout timeout 25 /home/mesh-home/.local/bin/mesh-node-health --test
  1111016: 11 bash bash /home/mesh-home/.local/bin/mesh-hw-health
  1111018: 14 timeout timeout 25 /home/mesh-home/.local/bin/mesh-job-calls --test
  1111019: 13 timeout timeout 20 /home/mesh-home/.local/bin/mesh-quota --test
  1111020: 9 bash bash /home/mesh-home/.local/bin/mesh-resource-guard --test
  1111021: 1 bash bash /home/mesh-home/.local/bin/mesh-cam-lock --dev /dev/video0 --why misha-wake-sg -- sg video -c fswebcam --no-banner -d '/dev/video0' -r '640x480' -S 8 '/tmp/tmp.NTTk7NXyOO/td.mesh-misha-wake/tmp.cpJNs31S0g/.mesh/.misha-wake-frame.new.jpg'
  1111022: 0 bash bash /home/mesh-home/.local/bin/mesh-tcp-metrics --test
  1111023: 2 bash bash /home/mesh-home/.local/bin/mesh-room-activity
  1111025: 1 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-task create demo /tmp/tmp.NTTk7NXyOO/td.mesh-task/tmp5q417zt3/plan.tsv ask:20260907-demo
  1111030: 0 bash bash /home/mesh-home/.local/bin/mesh-room-context --json
  1111031: 10 bash bash /home/mesh-home/.local/bin/mesh-reflex-health --test
  1111032: 5 bash bash /home/mesh-home/.local/bin/mesh-stop-check --test
  1111037: 7 bash bash /home/mesh-home/.local/bin/mesh-media-scene --test
  1111038: 12 timeout timeout 20 /home/mesh-home/.local/bin/mesh-random-track-grind --test
  1111039: 16 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111042: 11 bash bash /home/mesh-home/.local/bin/mesh-social-context --test
  1111044: 0 timeout timeout 15 ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 phaedra cat /var/lib/shadowsocks-libev/config.json
  1111048: 1 sleep sleep 8
  1111049: 0 timeout timeout 12 /home/mesh-home/.local/bin/mesh-tcp-attrib --test
  1111052: 10 bash bash /home/mesh-home/.local/bin/mesh-labor --feed
  1111053: 8 bash bash /home/mesh-home/.local/bin/mesh-heartbeat --rejoin
  1111056: 6 timeout timeout 12 /home/mesh-home/.local/bin/mesh-steward-deadman --test
  1111060: 11 bash bash /home/mesh-home/.local/bin/mesh-lan-newdevice --test
  1111061: 12 timeout timeout 25 /home/mesh-home/.local/bin/mesh-labor --test
  1111063: 6 sh sh /home/mesh-home/.local/bin/mesh-steward-deadman --test
  1111064: 1 sleep sleep 4
  1111067: 2 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1111068: 5 bash bash /home/mesh-home/.local/bin/mesh-imac-wifi
  1111072: 8 journalctl journalctl -b -1 -p err --no-pager
  1111073: 14 python3 python3 /home/mesh-home/.local/bin/mesh-job-apply --test
  1111075: 8 tail tail -30
  1111083: 3 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111084: 12 bash bash /home/mesh-home/.local/bin/mesh-random-track-grind --test
  1111087: 14 bash bash /home/mesh-home/.local/bin/mesh-job-calls --test
  1111089: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-route-events --daemon
  1111090: 3 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-fswriter --_armed --_log /tmp/tmp.NTTk7NXyOO/td.mesh-fswriter/fswriter-test-whv04xzk/log --window 6.0 /tmp/tmp.NTTk7NXyOO/td.mesh-fswriter/fswriter-test-whv04xzk/watched
  1111093: 5 bash bash /home/mesh-home/.local/bin/mesh-stop-check
  1111096: 7 bash bash /home/mesh-home/.local/bin/mesh-roll-call --test
  1111100: 1 ssh ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@100.103.99.16 echo ok
  1111101: 7 sleep sleep 8
  1111104: 6 timeout timeout 12 /home/mesh-home/.local/bin/mesh-stop-check --test
  1111108: 2 tail tail -1
  1111111: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-tcp-metrics --raw
  1111112: 3 bash bash /home/mesh-home/.local/bin/mesh-sense-reception
  1111117: 1 bash bash /home/mesh-home/.local/bin/mesh-swap-rate --test
  1111118: 6 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-records/tmp.hHQ0S2RlYo/src/probe.wav
  1111119: 10 timeout timeout 20 /home/mesh-home/.local/bin/mesh-reflexes --test
  1111120: 8 timeout timeout 20 /home/mesh-home/.local/bin/mesh-revive --test
  1111123: 6 grep grep ^MEASURE
  1111129: 1 sleep sleep 8
  1111135: 0 python3 python3 /home/mesh-home/.local/bin/mesh-proc-churn --json
  1111137: 6 sleep sleep 8
  1111138: 8 bash bash /home/mesh-home/.local/bin/mesh-ss-test --test
  1111140: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111142: 1 bash bash /home/mesh-home/.local/bin/mesh-swap-rate --json
  1111143: 10 bash bash /home/mesh-home/.local/bin/mesh-reflexes --test
  1111153: 0 ssh ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 phaedra cat /var/lib/shadowsocks-libev/config.json
  1111157: 2 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111161: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-mca
  1111162: 2 sleep sleep 8
  1111168: 7 timeout timeout 25 /home/mesh-home/.local/bin/mesh-mca --test
  1111173: 9 bash bash /home/mesh-home/.local/bin/mesh-ledger --test
  1111183: 1 timeout timeout 12 /home/mesh-home/.local/bin/mesh-task --test
  1111190: 8 bash bash /home/mesh-home/.local/bin/mesh-resource-guard --test
  1111192: 0 bash bash /home/mesh-home/.local/bin/mesh-tcp-metrics --raw
  1111193: 0 awk awk $2 != "-"
  1111194: 7 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --scope
  1111195: 14 timeout timeout 25 /home/mesh-home/.local/bin/mesh-job-chatwatch --test
  1111196: 8 bash bash /home/mesh-home/.local/bin/mesh-revive --test
  1111199: 0 wc wc -l
  1111201: 8 python3 python3 - /home/mesh-home/.mesh/spend.log /home/mesh-home/.mesh/tick.log 5 --tokens /tmp/tmp.NTTk7NXyOO/td.mesh-spend/tmp.yjvbjv5G8u/tmp/tmp.tPGmE54XL5 /home/mesh-home/.claude/projects 1
  1111203: 6 timeout timeout 12 /home/mesh-home/.local/bin/mesh-stranger-watch --test
  1111204: 6 python /home/mesh-home/grainneukeln/.venv/bin/python - /tmp/tmp.NTTk7NXyOO/td.mesh-records/tmp.hHQ0S2RlYo/src/probe.wav 0,12,3 0.006 measure
  1111205: 7 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --scope
  1111207: 7 awk awk -F\t -v idcap=4 -v sfloor=0.90 -v minsig=8 -v fminsig=4        # FAMILY SKELETON — the message with every VARIABLE token dropped: a family is the set of signatures       # that are the same sentence differing only where the message carries a value. Two properties earn it:       #   - it is computed from the RAW message, NEVER the normalized one. After normalize() a digit-derived       #     N is indistinguishable from a literal N (`Network`, `HNC`), so keying on the normalized text       #     would drop real words and merge unrelated messages. The raw still has actual digits.       #   - it drops variable tokens rather than taking a leading PREFIX. A prefix rule was tried first and       #     measured FALSE against the live journal here (2026-08-28): every rtw_8822bu 1-3:1.0 line begins       #     with a digit-bearing word, so seven genuinely DIFFERENT driver faults (leave idle state failed,       #     h2c queue mismatch, failed to configure mac, ...) all landed in one catch-all bucket and were       #     reported as a storm. They are seven real faults, correctly given seven signatures. Under the       #     skeleton they have seven distinct skeletons and no family fires.       function famkey(ident, raw,   i, w, nw, out) {         nw = split(raw, w, /[ \t]+/); out = ""         for (i=1; i<=nw; i++) {           if (w[i] ~ /[0-9]/) continue                 # carries a value -> not part of the skeleton           out = (out=="" ? w[i] : out " " w[i])         }         if (out == "") out = "<all-variable>"         return ident "|||" out       }       {         sig=$1; raw=$2; total++         n[sig]++         k=sig SUBSEP raw; c[k]++         if (c[k]==1) d[sig]++          # distinct raw messages absorbed by this signature         if (c[k]==2) r[sig]++          # ... of which RECUR (a stable, re-visited value, not a fresh counter)         if (!(sig in fam)) fam[sig] = famkey(substr(sig, 1, index(sig,"|||")-1), raw)       }       END{         if (total==0) { print "NO-DATA"; exit }         sigs=0; single=0; degen=0; idfold=0         for (s in n) {           sigs++           if (n[s]==1) single++           f=fam[s]; fs[f]++; if (n[s]==1) fsingle[f]++           body=substr(s, index(s,"|||")+3)           # DEGENERATE: a signature body with no alphabetic character discriminates NOTHING — every fault           # that lands in it after the first is silent forever.           if (body !~ /[A-Za-z]/) {             degen++             printf "  DEGENERATE     n=%-5d raws=%-3d  [%s]  <- no alphabetic content: absorbs anything\n", n[s], d[s], s | "sort"             continue           }           # IDENTITY-FOLD: >=2 distinct raws, a SMALL set (<=idcap), and >=2 of them RECUR. A small           # re-visited value set is an enumerable identity (device/port/instance index), not an unbounded           # counter — so normalize() folded away WHICH thing faulted, and only the first ever alerted.           if (d[s]>=2 && d[s]<=idcap && r[s]>=2) {             idfold++             printf "  IDENTITY-FOLD  n=%-5d raws=%-3d  [%s]  <- %d distinct raws, %d recurring: an enumerable identity was folded\n", n[s], d[s], s, d[s], r[s] | "sort"           }         }         # FAMILY-STORM — the per-family twin of the global singleton rate (2026-08-28, same task). ONE         # global rate over the whole alphabet is a MAJORITY VOTE: the UUID family above was storming five         # signatures wide beside ~26 healthy repeating ones, and 5/31 = 0.16 can never reach SFLOOR 0.90,         # so the guard shipped for exactly this pole could not see the pole in its own normalizer. A rate         # computed over signatures SHARING A STEM lets one storming family trip it while the rest is         # healthy. It is an ADDED arm, not a replacement: an alphabet that is globally all-singleton has         # every family at size 1, below fminsig, so a pure per-family rule would go BLIND to the shape         # case (12) asserts. Report-only, like everything in --scope — it names a stem whose residue never         # converges and leaves it to a human to say whether that residue is identity or noise, which is         # the one question the normalizer structurally cannot answer about itself.         storm=0; fams=0         for (f in fs) {           fams++           # the all-variable bucket is a CATCH-ALL, not a family — it holds messages that share no fixed           # text at all, so a high singleton rate in it says nothing about any one stem. Excluded loudly           # rather than silently: it is counted in families= and never in family-storm=.           if (f ~ /\|\|\|<all-variable>$/) continue           if (fs[f] >= fminsig && (fsingle[f]+0)/fs[f] >= sfloor) {             storm++             printf "  FAMILY-STORM   sigs=%-5d singletons=%-3d  [%s]  <- this stem mints a fresh signature nearly every time: normalize() leaves a per-event residue here\n", fs[f], fsingle[f]+0, f | "sort"           }         }         close("sort")         rho = 1 - (sigs/total)         srate = single/sigs         printf "records=%d  signatures=%d  compression=%.3f  singleton-rate=%.2f  degenerate=%d  identity-fold=%d  families=%d  family-storm=%d\n", total, sigs, rho, srate, degen, idfold, fams, storm         gpart = (sigs>=minsig && srate>=sfloor)         fpart = (storm>0)         if (degen>0 || idfold>0) { verdict="OVER-COMPRESSED"; rc=3 }         else if (gpart || fpart) { verdict="OVER-PARTICULARIZED"; rc=4 }         else { verdict="BALANCED"; rc=0 }         # WHICH arm fired is part of the verdict — the two have different remedies (a global storm means         # the normalizer is too fine everywhere; a family storm means one stem carries an unfolded residue).         why = ""         if (gpart) why = sprintf("global singleton-rate %.2f >= %s over %d signatures", srate, sfloor, sigs)         if (fpart) why = why (gpart ? "; " : "") sprintf("%d storming famil%s (>=%d sigs each, singleton-rate >= %s)", storm, (storm==1?"y":"ies"), fminsig, sfloor)         # both poles can hold at once; the silent pole wins the verdict (a blind sense outranks a loud one)         also=""         if (rc==4) also=" (" why ")"         if (rc==3 && (gpart || fpart)) also=" (+ over-particularized: " why ")"         print "scope: " verdict also         exit rc       }
  1111218: 14 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-guitar-watch/tmp.TKjWoEnDBY/tmp.S7SkKiV87Y/tone.wav
  1111224: 7 bash bash /home/mesh-home/.local/bin/mesh-mca --test
  1111225: 0 bash bash /home/mesh-home/.local/bin/mesh-node-health --test
  1111228: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-tcp-metrics --raw
  1111229: 0 sleep sleep 1.5
  1111230: 0 bash bash /home/mesh-home/.local/bin/mesh-tcp-attrib --test
  1111231: 5 timeout timeout 25 /home/mesh-home/.local/bin/mesh-mind-state --test
  1111238: 7 journalctl journalctl -b 0 -p err -o json
  1111240: 14 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-guitar-watch/tmp.TKjWoEnDBY/tmp.S7SkKiV87Y/tone.wav
  1111241: 7 jq jq -r ((.SYSLOG_IDENTIFIER // ._COMM // "kernel")|tostring) + "|||" + ((.MESSAGE // "")|tostring)
  1111242: 14 grep grep ^MEASURE
  1111245: 0 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-job-apply --reasons
  1111253: 14 python3 python3 /home/mesh-home/.local/bin/mesh-job-chatwatch --test
  1111255: 6 bash bash /home/mesh-home/.local/bin/mesh-stop-check --test
  1111258: 0 bash bash /home/mesh-home/.local/bin/mesh-imac-wifi
  1111259: 11 sudo [sudo] <defunct>
  1111262: 0 bash bash /home/mesh-home/.local/bin/mesh-room-music --test
  1111265: 8 bash bash /home/mesh-home/.local/bin/mesh-records
  1111268: 8 bash bash /home/mesh-home/.local/bin/mesh-speech-classify --test
  1111270: 9 bash bash /home/mesh-home/.local/bin/mesh-report --test
  1111277: 14 python /home/mesh-home/grainneukeln/.venv/bin/python - /tmp/tmp.NTTk7NXyOO/td.mesh-guitar-watch/tmp.TKjWoEnDBY/tmp.S7SkKiV87Y/tone.wav 0,12,3 0.006 measure
  1111280: 0 timeout timeout 3 bash -c exec 3<>/dev/tcp/192.168.8.214/22
  1111283: 10 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111288: 4 timeout timeout 12 /home/mesh-home/.local/bin/mesh-supervise --test
  1111291: 0 bash bash /home/mesh-home/.local/bin/mesh-precision --test
  1111294: 10 bash bash /home/mesh-home/.local/bin/mesh-leadlag --test
  1111307: 5 bash bash /home/mesh-home/.local/bin/mesh-relay --test
  1111316: 14 timeout timeout 20 /home/mesh-home/.local/bin/mesh-psi --test
  1111318: 9 bash bash /home/mesh-home/.local/bin/mesh-sound-reflex --test
  1111322: 4123168608 timeout timeout 12 /home/mesh-home/.local/bin/mesh-temp-display --test
  1111325: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-quota --test
  1111330: 0 bash bash /home/mesh-home/.local/bin/mesh-labor --json
  1111334: 11 timeout timeout 12 /home/mesh-home/.local/bin/mesh-socket-state --test
  1111339: 1 python3 python3 /home/mesh-home/.local/bin/mesh-task --test
  1111342: 4 bash bash /home/mesh-home/.local/bin/mesh-ss-connections --test
  1111346: 15 bash bash /home/mesh-home/.local/bin/mesh-pkg-watch --test
  1111347: 0 bash bash /home/mesh-home/.local/bin/mesh-precision --json --closure /tmp/tmp.NTTk7NXyOO/td.mesh-precision/tmp.UyHiuZs5Go/short_y --env /tmp/tmp.NTTk7NXyOO/td.mesh-precision/tmp.UyHiuZs5Go/noise_e
  1111348: 6 timeout timeout 25 /home/mesh-home/.local/bin/mesh-mind-control --test
  1111354: 15 apt-check /usr/bin/python3 /usr/lib/update-notifier/apt-check
  1111372: 4 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-job-chatwatch
  1111380: 1 bash bash /home/mesh-home/.local/bin/mesh-budget --gate frames --why misha-wake-sg
  1111383: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-ss-connections
  1111385: 15 bash bash /home/mesh-home/.local/bin/mesh-fsnotify --test
  1111390: 3 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111391: 8 bash bash /home/mesh-home/.local/bin/mesh-soundscape --test
  1111396: 9 timeout timeout 25 /home/mesh-home/.local/bin/mesh-load-attrib --test
  1111400: 8 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111401: 0 awk awk -v s=2026-09-14T02:25:24Z -v now=2026-09-14T03:25:24Z      $2=="grant" && $3=="axis=frames" && $1>=s { c=split($0,f," "); for(i=1;i<=c;i++) if(f[i]~/^cost=/){split(f[i],g,"=");n+=g[2]+0} }     NR==1 { first=$1 }     END{ note = (first>s) ? "LOWER BOUND (mesh-cam-lock openers only); ledger starts " first : "LOWER BOUND: counts only captures routed through mesh-cam-lock"          printf "%d %s %s\n", n+0, "full", note } /home/mesh-home/.mesh/budget-ledger.log
  1111404: 14 bash bash /home/mesh-home/.local/bin/mesh-psi --test
  1111406: 4 bash bash /home/mesh-home/.local/bin/mesh-roll-call
  1111412: 10 python3 python3 -
  1111413: 8 timeout timeout 12 /home/mesh-home/.local/bin/mesh-ss-connections --test
  1111414: 10 timeout timeout 12 /home/mesh-home/.local/bin/mesh-sound-reflex --test
  1111417: 11 bash bash /home/mesh-home/.local/bin/mesh-socket-state --test
  1111422: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-quota-react --_confirm-dialog-poll 0
  1111423: 7 bash bash /home/mesh-home/.local/bin/mesh-soundscape --test
  1111426: 3 sleep sleep 8
  1111427: 0 bash bash /home/mesh-home/.local/bin/mesh-labor --json
  1111428: 4 bash bash /home/mesh-home/.local/bin/mesh-ss-connections
  1111429: 0 bash bash /home/mesh-home/.local/bin/mesh-lock-holder --test
  1111430: 6 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111431: 0 grep grep -q attributed=
  1111436: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-stress --test
  1111437: 6 bash bash /home/mesh-home/.local/bin/mesh-mind-control --test
  1111444: 7 python3 python3 /tmp/tmp.NTTk7NXyOO/td.mesh-labor/mesh-ledger.IHT1ewyy/tmp.Ozed9NAobV 2026-09-14 2026-09-13T22:25:17Z 2026-09-14T03:25:17Z /tmp/tmp.NTTk7NXyOO/td.mesh-labor/mesh-ledger.IHT1ewyy/tmp.H4SRttsJY5
  1111445: 0 bash bash /home/mesh-home/.local/bin/mesh-tcp-attrib --test
  1111449: 4 awk awk -F\t          # RETIRE-AWARE ROUND CUTOFF (board task rollcall-escalation-counter-ignores-retire, 2026-08-19):         # the count is of rounds a proposal recurred in, so it must be a count of rounds SINCE THE LAST         # DECISION — otherwise a retire cannot lower it and the closed item re-escalates every round         # until LEDGER_DAYS ages it out. Live: job RETIRED hh-выход-мимо-VPN 2026-08-17T20:02:40Z and the         # next FIVE rounds each carried a verbatim "recurred x3 — unchanged (hh-выход-мимо-VPN)" demand         # for a decision already taken. The pre-existing retire credit (the excl harvest in the RETIRE         # branch above) could not reach it TWICE OVER: it matches only the literal wording "declined",         # and even harvested, propose_sig destroys the non-ASCII subject (hh dropped as <=2 chars, VPN         # kept) so both keys collapse to a token or two and sig_actioned s >=2-shared floor can never         # fire. Neither defect is fixable by widening a string match; the ARITHMETIC is what is wrong.         # So: cutoff = the epoch of the most-recent DECISION-ANNOUNCING null (retire_marker) posted by         # the sig s most-recent proposer — the same mind the escalation clause addresses (recur_for_mind),         # so the credit lands where the demand is sent — and only rounds AFTER it are counted. No subject         # matching is involved, which is exactly why it survives a subject propose_sig cannot key.         # Conservative in the documented direction: that mind s retire also resets its OTHER live chronic         # sigs (they simply re-accumulate), and a bare empty round ("PROPOSE none", no marker) resets         # nothing at all.         $1=="__RETIRE__" { if($3+0 > nullep[$4]+0) nullep[$4]=$3+0; next }         { key=$1 SUBSEP $2           if(!(key in epk) || $3+0 > epk[key]+0) epk[key]=$3+0           if(!(key in repk)) { repk[key]=$5; mindk[key]=$4 }           if(!($1 in maxrnd) || $2+0 > maxrnd[$1]+0){ maxrnd[$1]=$2+0; who[$1]=$4 }           sigs[$1]=1 }         END { for(k in sigs){                 cut = (who[k] in nullep) ? nullep[who[k]]+0 : 0                 n=0; mx=-1; mn=-1; mep=0; w=""; rp=""; rp0=""                 for(key in epk){                   split(key, a, SUBSEP); if(a[1]!=k) continue                   if(cut>0 && epk[key]+0 <= cut) continue                   r=a[2]+0; n++                   if(mx<0 || r>mx){ mx=r; w=mindk[key]; rp=repk[key] }                   if(mn<0 || r<mn){ mn=r; rp0=repk[key] }                   if(epk[key]+0 > mep) mep=epk[key]+0 }                 if(n>0) printf "%d\t%s\t%s\t%s\t%s\t%d\n", n, k, w, rp, rp0, mep } }
  1111450: 0 bash bash /home/mesh-home/.local/bin/mesh-lock-holder --test
  1111451: 5 bash bash /home/mesh-home/.local/bin/mesh-mind-state --test
  1111452: 7 bash bash /home/mesh-home/.local/bin/mesh-roll-call --test
  1111453: 8 bash bash /home/mesh-home/.local/bin/mesh-hh-drive --goto https://hh.ru/search/vacancy?text=team%20lead%20Go&page=0&order_by=publication_time&search_field=name&search_field=description&items_on_page=50
  1111456: 4 sort sort -rn
  1111459: 4 bash bash /home/mesh-home/.local/bin/mesh-roll-call
  1111462: 10 bash bash /home/mesh-home/.local/bin/mesh-sound-reflex --test
  1111467: 0 bash bash /home/mesh-home/.local/bin/mesh-embed --cos ZOMBIE: wire mesh-zzz to mesh-www aggregator (field: fusion) [taking] ACTIVE-CLAIM kelvin telemetry probe — on it
  1111470: 0 bash bash /home/mesh-home/.local/bin/mesh-land --apply mesh-land: add focused test artifact
  1111471: 0 bash bash -c exec 3<>/dev/tcp/192.168.8.214/22
  1111472: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-quota --test
  1111475: 4123168608 python3 python3 -c  import os, sys, time, glob  WARM = float(os.environ.get("MESH_TEMP_WARM", "60")) HOT  = float(os.environ.get("MESH_TEMP_HOT",  "80")) CRIT = float(os.environ.get("MESH_TEMP_CRIT", "88")) INTERVAL = float(os.environ.get("MESH_TEMP_INTERVAL", "2"))  RESET="\033[0m"; BOLD="\033[1m" GREEN="\033[32m"; YELLOW="\033[33m"; RED="\033[31m"; REDBG="\033[41m\033[97m"; DIM="\033[2m"; CYAN="\033[36m"  # ── pure decision: temperature -> band (exercised by --test) ───────────── def level(c):     if c >= CRIT: return "CRITICAL"     if c >= HOT:  return "HOT"     if c >= WARM: return "WARM"     return "OK"  def colour(lvl):     return {"OK":GREEN, "WARM":YELLOW, "HOT":RED, "CRITICAL":REDBG}.get(lvl, "")  # ── 5-row big digits (glanceable across a room) ────────────────────────── FONT = {  "0":["█████","█   █","█   █","█   █","█████"],  "1":["  ██ "," ███ ","  ██ ","  ██ "," ████"],  "2":["█████","    █","█████","█    ","█████"],  "3":["█████","    █","█████","    █","█████"],  "4":["█   █","█   █","█████","    █","    █"],  "5":["█████","█    ","█████","    █","█████"],  "6":["█████","█    ","█████","█   █","█████"],  "7":["█████","    █","   █ ","  █  ","  █  "],  "8":["█████","█   █","█████","█   █","█████"],  "9":["█████","█   █","█████","    █","█████"],  ".":["     ","     ","     ","  ██ ","  ██ "],  "C":["█████","█    ","█    ","█    ","█████"],  "°":["██ ","█ █","██ ","   ","   "],  " ":["   ","   ","   ","   ","   "], } def big(s):     rows=["","","","",""]     for ch in s:         g=FONT.get(ch, FONT[" "])         for i in range(5): rows[i]+=g[i]+" "     return rows  def read_zones():     zs=[]     for tf in sorted(glob.glob("/sys/class/thermal/thermal_zone*/temp")):         d=os.path.dirname(tf)         try:             t=int(open(tf).read().strip())/1000.0             typ=open(os.path.join(d,"type")).read().strip()         except Exception:             continue         zs.append((typ, t))     # AMD boxes expose NO thermal_zone for the CPU (only cooling_device*) — the package temp lives     # in hwmon k10temp (Tctl/Tdie). Pull labelled hwmon temps so an AMD node is not "NO ZONES".     for h in sorted(glob.glob("/sys/class/hwmon/hwmon*")):         try:             name=open(os.path.join(h,"name")).read().strip()         except Exception:             continue         if name not in ("k10temp","nvme"): continue         for inf in sorted(glob.glob(os.path.join(h,"temp*_input"))):             try:                 t=int(open(inf).read().strip())/1000.0                 lab=open(inf[:-6]+"_label").read().strip()             except Exception:                 continue             zs.append(("%s %s"%(name,lab), t))     return zs  def pkg(zs):     # the package temp drives the freeze; fall back to the hottest zone if absent     for typ,t in zs:         if typ=="x86_pkg_temp": return typ,t     for want in ("k10temp Tdie","k10temp Tctl"):   # AMD package temp         for typ,t in zs:             if typ==want: return typ,t     return max(zs, key=lambda z: z[1]) if zs else ("none", 0.0)  def gauge(c, width=40):     filled=max(0, min(width, int(round(c/100.0*width))))     lvl=level(c); col=colour(lvl)     return col + "█"*filled + RESET + DIM + "·"*(width-filled) + RESET  # per-zone spread across the session: a zone whose reading NEVER moves while the package swings # tens of degrees is a dead ACPI stub (ds acpitz sat at 27.8°C through a 50→90°C CPU night, # 2026-07-06 — operator read it as "the board never overheats", it measures nothing). Flag it # honestly instead of deleting: acpitz IS live on other boards (IdeaPad), so detect, never assume. _span={}   # typ -> [min, max]  def frame(zs, host):     if not zs:         return REDBG+BOLD+"  NO THERMAL ZONES READABLE — cannot show temperature  "+RESET     ptyp,pc = pkg(zs)     lvl=level(pc); col=colour(lvl)     ts=time.strftime("%H:%M:%SZ", time.gmtime())     out=[]     out.append(BOLD+CYAN+"  "+host.upper()+" THERMALS"+RESET+DIM+"   "+ts+"   refresh %gs"%INTERVAL+RESET)     out.append("")     for r in big("%.0f°C" % pc):         out.append("   "+col+BOLD+r+RESET)     out.append("")     out.append("   %s  %s  %s(freeze-risk ≥%g°C)%s" % (gauge(pc), col+BOLD+lvl+RESET, DIM, CRIT, RESET))     out.append("")     out.append("   "+DIM+"package: %s = %.1f°C"%(ptyp,pc)+RESET)     out.append("   "+DIM+"all zones:"+RESET)     for typ,t in zs:         c2=colour(level(t))         flag = "  <<< " + level(t) if t>=HOT else ""         s=_span.setdefault(typ,[t,t]); s[0]=min(s[0],t); s[1]=max(s[1],t)         pspan=_span.get(ptyp,[pc,pc])         stub = "  (не двигается — заглушка, не верь)" if (typ!=ptyp and s[1]-s[0]<0.5 and pspan[1]-pspan[0]>=10.0) else ""         out.append("     %-18s %s%5.1f°C%s%s%s" % (typ, c2, t, RESET, c2+BOLD+flag+RESET, DIM+stub+RESET))     out.append("")     if lvl=="CRITICAL":         out.append("   "+REDBG+BOLD+"  *** FREEZE RISK — COOL THE NODE NOW ***  "+RESET)     return "\n".join(out)  # ── modes ──────────────────────────────────────────────────────────────── if len(sys.argv) > 1 and sys.argv[1]=="--test":     f=0     def eq(a,b,m):         global f         if a!=b: print("FAIL %s: got %r want %r"%(m,a,b)); f=1     eq(level(20),"OK","20->OK"); eq(level(59.9),"OK","59.9->OK")     eq(level(60),"WARM","60->WARM"); eq(level(79.9),"WARM","79.9->WARM")     eq(level(80),"HOT","80->HOT"); eq(level(87.9),"HOT","87.9->HOT")     eq(level(88),"CRITICAL","88->CRITICAL"); eq(level(95),"CRITICAL","95->CRITICAL")     rows=big("58°C")     eq(len(rows),5,"big->5 rows")     if not all(rows): print("FAIL: big rows non-empty"); f=1     # pkg() prefers x86_pkg_temp over a hotter other zone     p=pkg([("acpitz",27.0),("x86_pkg_temp",58.0),("SEN1",82.0)])     eq(p[0],"x86_pkg_temp","pkg prefers package")     # pkg() falls back to hottest when no package zone     p2=pkg([("acpitz",27.0),("SEN1",82.0)])     eq(p2[1],82.0,"pkg fallback=hottest")     # frame renders without a tty and contains the temp (plain-digit line) + the right band word     fr=frame([("acpitz",27.0),("x86_pkg_temp",65.0)], "test-node")     if "65" not in fr or "WARM" not in fr: print("FAIL: frame missing temp/band"); f=1     fr2=frame([], "test-node")     if "NO THERMAL ZONES" not in fr2: print("FAIL: empty-zones must say so, not a false 0C"); f=1     print("smoke-test: ok (level bands + big-digit + pkg-pick + honest-empty)" if f==0 else "smoke-test: FAILED"); sys.exit(f)  # --line: one compact uncoloured line (for a tmux status bar / quick glance / piping) if len(sys.argv) > 1 and sys.argv[1]=="--line":     zs=read_zones()     if not zs: print("temp: UNREADABLE"); sys.exit(0)     ptyp,pc=pkg(zs); print("CPU %.0f°C %s" % (pc, level(pc))); sys.exit(0)  ONCE = (len(sys.argv) > 1 and sys.argv[1]=="--once") host = os.environ.get("MESH_TEMP_HOST") or os.uname().nodename  def paint():     zs=read_zones()     body=frame(zs, host)     # build then clear+paint atomically (a slow read leaves the last good frame, never a blank screen)     sys.stdout.write("\033[H\033[2J" + body + "\n")     sys.stdout.flush()  if ONCE:     paint(); sys.exit(0)  # full-screen loop: hide cursor, restore on exit sys.stdout.write("\033[?25l") try:     while True:         paint()         time.sleep(INTERVAL) except KeyboardInterrupt:     pass finally:     sys.stdout.write("\033[?25h\n"); sys.stdout.flush()  --test
  1111476: 7 timeout timeout 25 /home/mesh-home/.local/bin/mesh-mem-guard --test
  1111478: 3 timeout timeout 12 /home/mesh-home/.local/bin/mesh-swap-drain --test
  1111485: 6 bash bash /home/mesh-home/.local/bin/mesh-records
  1111489: 1 timeout timeout 20 /home/mesh-home/.local/bin/mesh-say --test
  1111496: 2 bash bash /home/mesh-home/.local/bin/mesh-sense-reception
  1111497: 5 timeout timeout 20 /home/mesh-home/.local/bin/mesh-room-reflex --test
  1111498: 0 bash bash /home/mesh-home/.local/bin/mesh-restore --test
  1111501: 6 timeout timeout 12 /home/mesh-home/.local/bin/mesh-storage-health --test
  1111503: 10 timeout timeout 12 /home/mesh-home/.local/bin/mesh-soundscape --test
  1111505: 0 bash bash /home/mesh-home/.local/bin/mesh-load-audit --json
  1111508: 2 adb adb exec-out su -c 'cat /data/data/com.google.android.gm/databases/bigTopDataDB.1023405767'
  1111511: 7 python3 python3 - /tmp/tmp.NTTk7NXyOO/td.mesh-labor/tmp.lcMkr7WhnP/task-feed/spend.log /home/mesh-home/.mesh/tick.log 5 --tokens /tmp/tmp.NTTk7NXyOO/td.mesh-labor/tmp.VsZYPXqc4G /home/mesh-home/.claude/projects 1
  1111512: 2 main /home/mesh-home/.mesh/whispercpp/main -m /home/mesh-home/.mesh/whispercpp/models/ggml-tiny.bin -l ru -nt -f /home/mesh-home/.mesh/model-fixtures/stt-ru-operator-0812/input.wav
  1111513: 0 ping ping -c1 -W2 -n 100.74.0.1
  1111521: 0 bash bash /home/mesh-home/.local/bin/mesh-mca
  1111524: 6 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111526: 4123168608 timeout timeout 4 mesh-irq-rate --json
  1111529: 0 bash bash /home/mesh-home/.local/bin/mesh-mem-guard --test
  1111530: 9 bash bash /home/mesh-home/.local/bin/mesh-load-attrib --test
  1111531: 4 bash bash /home/mesh-home/.local/bin/mesh-supervise --test
  1111532: 5 bash bash /home/mesh-home/.local/bin/mesh-room-reflex --test
  1111533: 1 bash bash /home/mesh-home/.local/bin/mesh-route-events --test
  1111535: 0 bash bash /home/mesh-home/.local/bin/mesh-embed --cos ZOMBIE: wire mesh-zzz to mesh-www aggregator (field: fusion) [taking] ACTIVE-CLAIM kelvin telemetry probe — on it
  1111537: 3 bash bash /home/mesh-home/.local/bin/mesh-queue-tend --test
  1111539: 3 bash bash /home/mesh-home/.local/bin/mesh-selfcare --test
  1111540: 4 sleep sleep 8
  1111547: 0 pgrep pgrep -P 1111639
  1111550: 0 timeout timeout 20 /home/mesh-home/.local/bin/mesh-selfcare --test
  1111551: 1 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --test
  1111553: 2 timeout timeout 60 mesh-room-activity
  1111555: 3 bash bash /home/mesh-home/.local/bin/mesh-misha-wake --test
  1111557: 8 timeout timeout 20 /home/mesh-home/.local/bin/mesh-rhythm --test
  1111558: 0 bash bash /home/mesh-home/.local/bin/mesh-ledger --price-window 5
  1111560: 3 bash bash /home/mesh-home/.local/bin/mesh-swap-drain --test
  1111567: 6 timeout timeout 90 mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-records/tmp.hHQ0S2RlYo/src/probe.wav
  1111568: 9 timeout timeout 20 /home/mesh-home/.local/bin/mesh-report --test
  1111569: 6 head head -1
  1111576: 3 bash bash /home/mesh-home/.local/bin/mesh-selfcare --test
  1111580: 0 bash bash /home/mesh-home/.local/bin/mesh-homeostasis --test
  1111583: 6 bash bash /home/mesh-home/.local/bin/mesh-storage-health --test
  1111588: 0 python3 python3 -
  1111591: 10 bash bash /home/mesh-home/.local/bin/mesh-soundscape --test
  1111593: 1 bash bash /home/mesh-home/.local/bin/mesh-relay --test
  1111600: 1 gh gh api repos/tenstorrent/tt-metal/contents/CODE_OF_CONDUCT.md
  1111601: 4 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111607: 7 bash bash /home/mesh-home/.local/bin/mesh-labor --feed
  1111612: 5 sleep sleep 20
  1111613: 2 sleep sleep 5
  1111614: 4 sleep sleep 5
  1111617: 8 bash bash /home/mesh-home/.local/bin/mesh-rhythm --test
  1111621: 3 bash [bash] <defunct>
  1111623: 2 sleep sleep 5
  1111624: 1 timeout timeout -k 5 45 sudo -n unshare -n env MESH_ROUTE_EVENTS_LOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.9xCZGTSO7Z/e.log MESH_ROUTE_EVENTS_COVF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.9xCZGTSO7Z/e.cov MESH_ROUTE_EVENTS_LOCK=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.9xCZGTSO7Z/e.lock MESH_ROUTE_EVENTS_STARTF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.9xCZGTSO7Z/e.started MESH_ROUTE_EVENTS_PIDF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.9xCZGTSO7Z/e.pid MESH_ROUTE_EVENTS_DLOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.9xCZGTSO7Z/e.dlog MESH_ROUTE_EVENTS_COV_S=2 MESH_ROUTE_EVENTS_MON_ARGS=route bash -c        ip link set lo up       setpriv --reuid=1000 --regid=1000 --clear-groups bash "/home/mesh-home/.local/bin/mesh-route-events" --daemon >>"/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.9xCZGTSO7Z/e.dlog" 2>&1       echo "rc=$?"
  1111626: 11 timeout timeout 20 /home/mesh-home/.local/bin/mesh-records --test
  1111629: 0 bash bash /home/mesh-home/.local/bin/mesh-pace --eff-gap 180
  1111630: 4123168608 python3 python3 /home/mesh-home/.local/bin/mesh-irq-rate --json
  1111632: 4 timeout timeout 25 /home/mesh-home/.local/bin/mesh-misha-wake --test
  1111634: 3 bash bash /home/mesh-home/.local/bin/mesh-link-heal --layer
  1111636: 0 timeout timeout 12 /home/mesh-home/.local/bin/mesh-tcp-retrans --test
  1111653: 3 bash bash /home/mesh-home/.local/bin/mesh-queue-tend
  1111657: 2 bash bash /home/mesh-home/.local/bin/mesh-music-fanout --test
  1111664: 3 head head -n1
  1111671: 0 arecord arecord -q -f S16_LE -r 8000 -c 1 -d 6 /tmp/tmp.NTTk7NXyOO/td.mesh-mains-hum/tmppyx9bp0c/hum.wav
  1111686: 1 ip ip -ts monitor label route
  1111689: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-quota --test
  1111692: 1 bash bash /home/mesh-home/.local/bin/mesh-say --test
  1111696: 13 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111718: 10 timeout timeout 20 /home/mesh-home/.local/bin/mesh-relay-attest --test
  1111720: 0 bash [bash] <defunct>
  1111724: 5 timeout timeout 12 /home/mesh-home/.local/bin/mesh-stress --test
  1111726: 10 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111727: 0 sleep sleep 2
  1111733: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-socket-state --exposure
  1111743: 2 timeout timeout 12 /home/mesh-home/.local/bin/mesh-system-vitality --test
  1111754: 8 bash bash /home/mesh-home/.local/bin/mesh-records --test
  1111757: 0 bash bash /home/mesh-home/.local/bin/mesh-selfcare --test
  1111760: 8 bash bash /home/mesh-home/.local/bin/mesh-heartbeat --test
  1111762: 10 bash bash /home/mesh-home/.local/bin/mesh-relay-attest --test
  1111764: 0 python /home/mesh-home/grainneukeln/.venv/bin/python /tmp/tmp.NTTk7NXyOO/td.mesh-overhear/tmp.StiALqXwWM/overhear-0NcAQt.py gate_kind ambient
  1111765: 0 bash bash /home/mesh-home/.local/bin/mesh-tcp-retrans --test
  1111766: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-tell --test
  1111775: 6 bash bash /home/mesh-home/.local/bin/mesh-roll-call
  1111780: 11 bash bash /home/mesh-home/.local/bin/mesh-records --test
  1111785: 0 bash bash /home/mesh-home/.local/bin/mesh-pace --eff-gap 180
  1111787: 8 timeout timeout 25 /home/mesh-home/.local/bin/mesh-lock-holder --test
  1111792: 1 sudo sudo -n unshare -n env MESH_ROUTE_EVENTS_LOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.9xCZGTSO7Z/e.log MESH_ROUTE_EVENTS_COVF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.9xCZGTSO7Z/e.cov MESH_ROUTE_EVENTS_LOCK=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.9xCZGTSO7Z/e.lock MESH_ROUTE_EVENTS_STARTF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.9xCZGTSO7Z/e.started MESH_ROUTE_EVENTS_PIDF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.9xCZGTSO7Z/e.pid MESH_ROUTE_EVENTS_DLOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.9xCZGTSO7Z/e.dlog MESH_ROUTE_EVENTS_COV_S=2 MESH_ROUTE_EVENTS_MON_ARGS=route bash -c        ip link set lo up       setpriv --reuid=1000 --regid=1000 --clear-groups bash "/home/mesh-home/.local/bin/mesh-route-events" --daemon >>"/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.9xCZGTSO7Z/e.dlog" 2>&1       echo "rc=$?"
  1111794: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-pace --status
  1111799: 4123168608 awk awk $1=="dispatch"{print $4" "$5; exit}
  1111804: 0 bash bash /home/mesh-home/.local/bin/mesh-stranger-watch
  1111807: 3 python3 python3 - json /home/mesh-home/.mesh/chat.log 2026-09-14T03:25:20Z 24 6 1
  1111810: 8 bash bash /home/mesh-home/.local/bin/mesh-records
  1111825: 0 sleep sleep 4
  1111826: 0 bash bash /home/mesh-home/.local/bin/mesh-tcp-attrib --window 1
  1111834: 0 bash bash /home/mesh-home/.local/bin/mesh-rhythm --test
  1111840: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-lan-newdevice --test
  1111844: 0 python3 python3 -
  1111847: 5 bash bash /home/mesh-home/.local/bin/mesh-guardian --test
  1111851: 6 bash bash /home/mesh-home/.local/bin/mesh-roll-call
  1111854: 5 bash bash /home/mesh-home/.local/bin/mesh-stress --test
  1111858: 0 bash bash /home/mesh-home/.local/bin/mesh-pace --eff-gap 180
  1111873: 0 python3 python3 -
  1111877: 1 bash bash /home/mesh-home/.local/bin/mesh-overhear --test
  1111878: 2 timeout timeout 20 /home/mesh-home/.local/bin/mesh-rq-wait --test
  1111884: 0 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111889: 2 bash bash /home/mesh-home/.local/bin/mesh-system-vitality --test
  1111891: 3 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111895: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-prior-art zzqqx-nothing zzqqy-either
  1111898: 3 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-model-bench --test
  1111900: 5 bash bash /home/mesh-home/.local/bin/mesh-stop-check
  1111904: 4 sudo sudo -n --preserve-env=MESH_FSWRITER_TEST_STALL /usr/bin/python3 /home/mesh-home/.local/bin/mesh-fswriter --_armed --_log /tmp/tmp.NTTk7NXyOO/td.mesh-fswriter/fswriter-test-whv04xzk/log --window 6.0 /tmp/tmp.NTTk7NXyOO/td.mesh-fswriter/fswriter-test-whv04xzk/watched
  1111914: 0 bash bash /home/mesh-home/.local/bin/mesh-mind-control --scan-orphans
  1111929: 3 bash bash /home/mesh-home/.local/bin/mesh-sync-tools --test
  1111930: 4 timeout timeout 25 /home/mesh-home/.local/bin/mesh-model-bench --test
  1111937: 3 sleep sleep 8
  1111940: 0 bash bash /home/mesh-home/.local/bin/mesh-reflexes --apply
  1111947: 5 timeout timeout 20 /home/mesh-home/.local/bin/mesh-room-sense-loss --test
  1111949: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-psi
  1111952: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-land --apply mesh-land: add focused test artifact
  1111958: 11 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111963: 2 python3 python3 /home/mesh-home/.local/bin/mesh-rq-wait --test
  1111965: 3 sleep sleep 5
  1111966: 1 python3 python3 - journal /tmp/tmp.NTTk7NXyOO/td.mesh-promises.bak-20260912-witness/tmp.hHjl9H6hUR/tmp.SUpqqljIhZ/board 2026-07-24T12:00:00Z 24 6 1 /tmp/tmp.NTTk7NXyOO/td.mesh-promises.bak-20260912-witness/tmp.hHjl9H6hUR/tmp.SUpqqljIhZ/j.journal
  1111979: 3 python3 python3 /home/mesh-home/lte-workstation/scripts/mesh-manifest --check
  1111983: 11 timeout timeout 25 /home/mesh-home/.local/bin/mesh-land --test
  1111991: 5 timeout [timeout] <defunct>
  1111999: 3 inotifywait inotifywait -qq -t 4 -e close_write,modify,create,move /tmp/tmp.NTTk7NXyOO/td.mesh-promises-watch/tmp.IovDIfp5Bd/watched
  1112005: 5 bash bash /home/mesh-home/.local/bin/mesh-room-sense-loss --test
  1112006: 11 bash bash /home/mesh-home/.local/bin/mesh-imac-wifi
  1112009: 4 python3 python3 /home/mesh-home/.local/bin/mesh-model-bench --test
  1112030: 1 sleep sleep 8
  1112032: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-psi-attrib --who cpu
  1112035: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-mind-control --test
  1112040: 11 bash bash /home/mesh-home/.local/bin/mesh-land --test
  1112062: 1 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1112073: 0 bash bash /home/mesh-home/.local/bin/mesh-selfcare --test
  1112084: 0 sleep sleep 8
  1112091: 1 bash bash -c        ip link set lo up       setpriv --reuid=1000 --regid=1000 --clear-groups bash "/home/mesh-home/.local/bin/mesh-route-events" --daemon >>"/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.9xCZGTSO7Z/e.dlog" 2>&1       echo "rc=$?"
  1112106: 0 timeout timeout 20 mesh-labor --json
  1112112: 0 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1112121: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-room-address --test
  1112137: 4123168608 bash [bash]
  1112140: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-ledger --price-window 5
  1112142: 0 timeout timeout 10 /home/mesh-home/.local/bin/mesh-supervise
  1112148: 1 sleep sleep 8
  1112155: 0 bash bash /home/mesh-home/.local/bin/mesh-conn --oneline
  1112156: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-mind-control --scan-orphans
  1112157: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-land --apply mesh-land: add focused test artifact
  1112158: 3 bash bash /home/mesh-home/.local/bin/mesh-fitness --test
  1112165: 0 bash bash /home/mesh-home/.local/bin/mesh-conn --oneline
  1112175: 0 timeout timeout 8 curl -s -o /dev/null -w %{http_code} --max-time 8 https://1.1.1.1
  1112190: 1 bash bash /home/mesh-home/.local/bin/mesh-route-events --daemon
  1112199: 3 bash bash /home/mesh-home/.local/bin/mesh-fitness --test
  1112204: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-hw-fault-watch --test
  1112207: 4123168608 timeout timeout 8 ollama run qwen2.5:3b --think=false --format json Ты — фильтр пробуждения для голосового ассистента по имени Миша (звательные формы: Миша, Миш, Мишань). В комнате идёт живой разговор; микрофон также ловит галлюцинации распознавания речи на тишине. Ниже последние реплики из комнаты по порядку. Реши ТОЛЬКО про ПОСЛЕДНЮЮ реплику, используя предыдущие как контекст. ГЛАВНОЕ ПРАВИЛО: если в ПОСЛЕДНЕЙ реплике есть звательное обращение к Мише (Миша/Миш/Мишань — часто выделено запятой: "Миш,", "Ну вот, Миш," "Миша,") — это ВСЕГДА {"wake":true}, даже если дальше идёт жалоба, ремарка или незаконченная мысль. При любом сомнении отвечай {"wake":true} — пропущенное обращение хуже лишнего. Ответь {"wake":false} ТОЛЬКО когда обращения к Мише в последней реплике нет: люди говорят между собой; о Мише в ТРЕТЬЕМ лице без обращения к нему ("спроси у Миши", "Миша вчера чинил", "как думаешь, Миша прав"); слова, лишь ПОХОЖИЕ на имя (мишка, мишура, Мишель); бессмысленный обрывок STT на тишине. Примеры: Разговор: ПОСЛЕДНЯЯ: "Миша, ты нас слышишь?" -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Ну вот, Миш, плохо слушать, всё прерывается" -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Миш, кстати, а ты видишь..." -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Время" -> {"wake":false} Разговор: "Смотри какие мишки на витрине" ПОСЛЕДНЯЯ: "Да, милые, купим?" -> {"wake":false} Разговор: ПОСЛЕДНЯЯ: "Как думаешь, Миша был прав вчера?" -> {"wake":false} Разговор: ПОСЛЕДНЯЯ: "Повесь мишуру повыше" -> {"wake":false} Разговор:  ПОСЛЕДНЯЯ: "КОНЕЦ"
  1112208: 0 curl curl -s -o /dev/null -w %{http_code} --max-time 8 https://1.1.1.1
  1112210: 0 grep grep -H ^lock: /proc/1000664/fdinfo/0 /proc/1000664/fdinfo/1 /proc/1000664/fdinfo/2 /proc/1001934/fdinfo/0 /proc/1001934/fdinfo/1 /proc/1001934/fdinfo/2 /proc/100195/fdinfo/0 /proc/100195/fdinfo/1 /proc/100195/fdinfo/2 /proc/100195/fdinfo/255 /proc/1003970/fdinfo/0 /proc/1003970/fdinfo/1 /proc/1003970/fdinfo/2 /proc/1004502/fdinfo/0 /proc/1004502/fdinfo/1 /proc/1004502/fdinfo/2 /proc/1004983/fdinfo/0 /proc/1004983/fdinfo/1 /proc/1004983/fdinfo/2 /proc/1006080/fdinfo/0 /proc/1006080/fdinfo/1 /proc/1006080/fdinfo/2 /proc/1009749/fdinfo/0 /proc/1009749/fdinfo/1 /proc/1009749/fdinfo/2 /proc/1010069/fdinfo/0 /proc/1010069/fdinfo/1 /proc/1010069/fdinfo/2 /proc/1010704/fdinfo/0 /proc/1010704/fdinfo/1 /proc/1010704/fdinfo/2 /proc/1012230/fdinfo/0 /proc/1012230/fdinfo/1 /proc/1012230/fdinfo/2 /proc/1013358/fdinfo/0 /proc/1013358/fdinfo/1 /proc/1013358/fdinfo/2 /proc/1014700/fdinfo/0 /proc/1014700/fdinfo/1 /proc/1014700/fdinfo/2 /proc/1015373/fdinfo/0 /proc/1015373/fdinfo/1 /proc/1015373/fdinfo/2 /proc/1016284/fdinfo/0 /proc/1016284/fdinfo/1 /proc/1016284/fdinfo/2 /proc/1017255/fdinfo/0 /proc/1017255/fdinfo/1 /proc/1017255/fdinfo/2 /proc/1020538/fdinfo/0 /proc/1020538/fdinfo/1 /proc/1020538/fdinfo/2 /proc/1021147/fdinfo/0 /proc/1021147/fdinfo/1 /proc/1021147/fdinfo/2 /proc/1021766/fdinfo/0 /proc/1021766/fdinfo/1 /proc/1021766/fdinfo/2 /proc/1021798/fdinfo/0 /proc/1021798/fdinfo/1 /proc/1021798/fdinfo/2 /proc/1021798/fdinfo/3 /proc/1021798/fdinfo/4 /proc/1024529/fdinfo/0 /proc/1024529/fdinfo/1 /proc/1024529/fdinfo/2 /proc/1025848/fdinfo/0 /proc/1025848/fdinfo/1 /proc/1025848/fdinfo/2 /proc/1026858/fdinfo/0 /proc/1026858/fdinfo/1 /proc/1026858/fdinfo/2 /proc/1028038/fdinfo/0 /proc/1028038/fdinfo/1 /proc/1028038/fdinfo/2 /proc/1029311/fdinfo/0 /proc/1029311/fdinfo/1 /proc/1029311/fdinfo/2 /proc/1033685/fdinfo/0 /proc/1033685/fdinfo/1 /proc/1033685/fdinfo/2 /proc/1034881/fdinfo/0 /proc/1034881/fdinfo/1 /proc/1034881/fdinfo/2 /proc/1035281/fdinfo/0 /proc/1035281/fdinfo/1 /proc/1035281/fdinfo/2 /proc/1036315/fdinfo/0 /proc/1036315/fdinfo/1 /proc/1036315/fdinfo/2 /proc/1042665/fdinfo/0 /proc/1042665/fdinfo/1 /proc/1042665/fdinfo/2 /proc/1043502/fdinfo/0 /proc/1043502/fdinfo/1 /proc/1043502/fdinfo/2 /proc/1044484/fdinfo/0 /proc/1044484/fdinfo/1 /proc/1044484/fdinfo/2 /proc/1044503/fdinfo/0 /proc/1044503/fdinfo/1 /proc/1044503/fdinfo/2 /proc/1044503/fdinfo/255 /proc/1046906/fdinfo/0 /proc/1046906/fdinfo/1 /proc/1046906/fdinfo/2 /proc/1046946/fdinfo/0 /proc/1046946/fdinfo/1 /proc/1046946/fdinfo/2 /proc/1046946/fdinfo/255 /proc/1046946/fdinfo/3 /proc/1047365/fdinfo/0 /proc/1047365/fdinfo/1 /proc/1047365/fdinfo/2 /proc/1050949/fdinfo/0 /proc/1050949/fdinfo/1 /proc/1050949/fdinfo/2 /proc/1050949/fdinfo/3 /proc/1050973/fdinfo/0 /proc/1050973/fdinfo/1 /proc/1050973/fdinfo/2 /proc/1051030/fdinfo/0 /proc/1051030/fdinfo/1 /proc/1051030/fdinfo/2 /proc/1051030/fdinfo/255 /proc/1051529/fdinfo/0 /proc/1051529/fdinfo/1 /proc/1051529/fdinfo/2 /proc/1051529/fdinfo/255 /proc/1051531/fdinfo/0 /proc/1051531/fdinfo/1 /proc/1051531/fdinfo/2 /proc/1051774/fdinfo/0 /proc/1051774/fdinfo/1 /proc/1051774/fdinfo/2 /proc/1051800/fdinfo/0 /proc/1051800/fdinfo/1 /proc/1051800/fdinfo/2 /proc/1051800/fdinfo/3 /proc/1051978/fdinfo/0 /proc/1051978/fdinfo/1 /proc/1051978/fdinfo/2 /proc/1057785/fdinfo/0 /proc/1057785/fdinfo/1 /proc/1057785/fdinfo/2 /proc/1058257/fdinfo/0 /proc/1058257/fdinfo/1 /proc/1058257/fdinfo/2 /proc/1061303/fdinfo/0 /proc/1061303/fdinfo/1 /proc/1061303/fdinfo/2 /proc/1063924/fdinfo/0 /proc/1063924/fdinfo/1 /proc/1063924/fdinfo/2 /proc/1065515/fdinfo/0 /proc/1065515/fdinfo/1 /proc/1065515/fdinfo/2 /proc/1066742/fdinfo/0 /proc/1066742/fdinfo/1 /proc/1066742/fdinfo/2 /proc/1067512/fdinfo/0 /proc/1067512/fdinfo/1 /proc/1067512/fdinfo/2 /proc/1067889/fdinfo/0 /proc/1067889/fdinfo/1 /proc/1067889/fdinfo/2 /proc/1068505/fdinfo/0 /proc/1068505/fdinfo/1 /proc/1068505/fdinfo/2 /proc/1069729/fdinfo/0 /proc/1069729/fdinfo/1 /proc/1069729/fdinfo/2 /proc/1070593/fdinfo/0 /proc/1070593/fdinfo/1 /proc/1070593/fdinfo/2 /proc/1072763/fdinfo/0 /proc/1072763/fdinfo/1 /proc/1072763/fdinfo/2 /proc/1072763/fdinfo/255 /proc/1072797/fdinfo/0 /proc/1072797/fdinfo/1 /proc/1072797/fdinfo/2 /proc/1073973/fdinfo/0 /proc/1073973/fdinfo/1 /proc/1073973/fdinfo/2 /proc/1078032/fdinfo/0 /proc/1078032/fdinfo/1 /proc/1078032/fdinfo/2 /proc/1081163/fdinfo/0 /proc/1081163/fdinfo/1 /proc/1081163/fdinfo/2 /proc/1081707/fdinfo/0 /proc/1081707/fdinfo/1 /proc/1081707/fdinfo/2 /proc/1082796/fdinfo/0 /proc/1082796/fdinfo/1 /proc/1082796/fdinfo/2 /proc/1085035/fdinfo/0 /proc/1085035/fdinfo/1 /proc/1085035/fdinfo/2 /proc/1085062/fdinfo/0 /proc/1085062/fdinfo/1 /proc/1085062/fdinfo/2 /proc/1085062/fdinfo/255 /proc/1085252/fdinfo/0 /proc/1085252/fdinfo/1 /proc/1085252/fdinfo/2 /proc/1085253/fdinfo/0 /proc/1085253/fdinfo/1 /proc/1085253/fdinfo/2 /proc/1085253/fdinfo/255 /proc/1085253/fdinfo/3 /proc/1085283/fdinfo/0 /proc/1085283/fdinfo/1 /proc/1085283/fdinfo/2 /proc/1085287/fdinfo/0 /proc/1085287/fdinfo/1 /proc/1085287/fdinfo/2 /proc/1085287/fdinfo/255 /proc/1085287/fdinfo/3 /proc/1085327/fdinfo/0 /proc/1085327/fdinfo/1 /proc/1085327/fdinfo/10 /proc/1085327/fdinfo/11 /proc/1085327/fdinfo/2 /proc/1085337/fdinfo/0 /proc/1085337/fdinfo/1 /proc/1085337/fdinfo/2 /proc/1085361/fdinfo/0 /proc/1085361/fdinfo/1 /proc/1085361/fdinfo/2 /proc/1085383/fdinfo/0 /proc/1085383/fdinfo/1 /proc/1085383/fdinfo/2 /proc/1085383/fdinfo/255 /proc/1085383/fdinfo/3 /proc/1085385/fdinfo/0 /proc/1085385/fdinfo/1 /proc/1085385/fdinfo/2 /proc/1085386/fdinfo/0 /proc/1085386/fdinfo/1 /proc/1085386/fdinfo/2 /proc/1085411/fdinfo/0 /proc/1085411/fdinfo/1 /proc/1085411/fdinfo/2 /proc/1085438/fdinfo/0 /proc/1085438/fdinfo/1 /proc/1085438/fdinfo/2 /proc/1085438/fdinfo/9 /proc/1085447/fdinfo/0 /proc/1085447/fdinfo/1 /proc/1085447/fdinfo/2 /proc/1085469/fdinfo/0 /proc/1085469/fdinfo/1 /proc/1085469/fdinfo/2 /proc/1085491/fdinfo/0 /proc/1085491/fdinfo/1 /proc/1085491/fdinfo/2 /proc/1085491/fdinfo/255 /proc/1085491/fdinfo/9 /proc/1085508/fdinfo/0 /proc/1085508/fdinfo/1 /proc/1085508/fdinfo/2 /proc/1085528/fdinfo/0 /proc/1085528/fdinfo/1 /proc/1085528/fdinfo/2 /proc/1085528/fdinfo/255 /proc/1085563/fdinfo/0 /proc/1085563/fdinfo/1 /proc/1085563/fdinfo/2 /proc/1085567/fdinfo/0 /proc/1085567/fdinfo/1 /proc/1085567/fdinfo/2 /proc/1085612/fdinfo/0 /proc/1085612/fdinfo/1 /proc/1085612/fdinfo/2 /proc/1085612/fdinfo/9 /proc/1085615/fdinfo/0 /proc/1085615/fdinfo/1 /proc/1085615/fdinfo/2 /proc/1085616/fdinfo/0 /proc/1085616/fdinfo/1 /proc/1085616/fdinfo/2 /proc/1085642/fdinfo/0 /proc/1085642/fdinfo/1 /proc/1085642/fdinfo/2 /proc/1085643/fdinfo/0 /proc/1085643/fdinfo/1 /proc/1085643/fdinfo/10 /proc/1085643/fdinfo/11 /proc/1085643/fdinfo/2 /proc/1085654/fdinfo/0 /proc/1085654/fdinfo/1 /proc/1085654/fdinfo/2 /proc/1085664/fdinfo/0 /proc/1085664/fdinfo/1 /proc/1085664/fdinfo/2 /proc/1085711/fdinfo/0 /proc/1085711/fdinfo/1 /proc/1085711/fdinfo/2 /proc/1085743/fdinfo/0 /proc/1085743/fdinfo/1 /proc/1085743/fdinfo/2 /proc/1085765/fdinfo/0 /proc/1085765/fdinfo/1 /proc/1085765/fdinfo/2 /proc/1085765/fdinfo/255 /proc/1085765/fdinfo/3 /proc/1085765/fdinfo/9 /proc/1085776/fdinfo/0 /proc/1085776/fdinfo/1 /proc/1085776/fdinfo/10 /proc/1085776/fdinfo/11 /proc/1085776/fdinfo/2 /proc/1085791/fdinfo/0 /proc/1085791/fdinfo/1 /proc/1085791/fdinfo/2 /proc/1085791/fdinfo/255 /proc/1085791/fdinfo/3 /proc/1085798/fdinfo/0 /proc/1085798/fdinfo/1 /proc/1085798/fdinfo/2 /proc/1085811/fdinfo/0 /proc/1085811/fdinfo/1 /proc/1085811/fdinfo/2 /proc/1085825/fdinfo/0 /proc/1085825/fdinfo/1 /proc/1085825/fdinfo/2 /proc/1085925/fdinfo/0 /proc/1085925/fdinfo/1 /proc/1085925/fdinfo/2 /proc/1085933/fdinfo/0 /proc/1085933/fdinfo/1 /proc/1085933/fdinfo/2 /proc/1085933/fdinfo/255 /proc/1085933/fdinfo/3 /proc/1085936/fdinfo/0 /proc/1085936/fdinfo/1 /proc/1085936/fdinfo/2 /proc/1085949/fdinfo/0 /proc/1085949/fdinfo/1 /proc/1085949/fdinfo/10 /proc/1085949/fdinfo/11 /proc/1085949/fdinfo/2 /proc/1086009/fdinfo/0 /proc/1086009/fdinfo/1 /proc/1086009/fdinfo/2 /proc/1086020/fdinfo/0 /proc/1086020/fdinfo/1 /proc/1086020/fdinfo/2 /proc/1086020/fdinfo/255 /proc/1086020/fdinfo/9 /proc/1086023/fdinfo/0 /proc/1086023/fdinfo/1 /proc/1086023/fdinfo/2 /proc/1086024/fdinfo/0 /proc/1086024/fdinfo/1 /proc/1086024/fdinfo/2 /proc/1086084/fdinfo/0 /proc/1086084/fdinfo/1 /proc/1086084/fdinfo/2 /proc/1086088/fdinfo/0 /proc/1086088/fdinfo/1 /proc/1086088/fdinfo/2 /proc/1086089/fdinfo/0 /proc/1086089/fdinfo/1 /proc/1086089/fdinfo/2 /proc/1086140/fdinfo/0 /proc/1086140/fdinfo/1 /proc/1086140/fdinfo/2 /proc/1086160/fdinfo/0 /proc/1086160/fdinfo/1 /proc/1086160/fdinfo/2 /proc/1086161/fdinfo/0 /proc/1086161/fdinfo/1 /proc/1086161/fdinfo/2 /proc/1086161/fdinfo/3 /proc/1086203/fdinfo/0 /proc/1086203/fdinfo/1 /proc/1086203/fdinfo/2 /proc/1086203/fdinfo/9 /proc/1086204/fdinfo/0 /proc/1086204/fdinfo/1 /proc/1086204/fdinfo/2 /proc/1086220/fdinfo/0 /proc/1086220/fdinfo/1 /proc/1086220/fdinfo/2 /proc/1086231/fdinfo/0 /proc/1086231/fdinfo/1 /proc/1086231/fdinfo/10 /proc/1086231/fdinfo/2 /proc/1086231/fdinfo/255 /proc/1086231/fdinfo/3 /proc/1086234/fdinfo/0 /proc/1086234/fdinfo/1 /proc/1086234/fdinfo/2 /proc/1086253/fdinfo/0 /proc/1086253/fdinfo/1 /proc/1086253/fdinfo/2 /proc/1086262/fdinfo/0 /proc/1086262/fdinfo/1 /proc/1086262/fdinfo/2 /proc/1086262/fdinfo/3 /proc/1086262/fdinfo/9 /proc/1086263/fdinfo/0 /proc/1086263/fdinfo/1 /proc/1086263/fdinfo/2 /proc/1086266/fdinfo/0 /proc/1086266/fdinfo/1 /proc/1086266/fdinfo/2 /proc/1086355/fdinfo/0 /proc/1086355/fdinfo/1 /proc/1086355/fdinfo/10 /proc/1086355/fdinfo/11 /proc/1086355/fdinfo/2 /proc/1086397/fdinfo/0 /proc/1086397/fdinfo/1 /proc/1086397/fdinfo/2 /proc/1086397/fdinfo/255 /proc/1086397/fdinfo/3 /proc/1086438/fdinfo/0 /proc/1086438/fdinfo/1 /proc/1086438/fdinfo/2 /proc/1086438/fdinfo/255 /proc/1086464/fdinfo/0 /proc/1086464/fdinfo/1 /proc/1086464/fdinfo/2 /proc/1086489/fdinfo/0 /proc/1086489/fdinfo/1 /proc/1086489/fdinfo/10 /proc/1086489/fdinfo/11 /proc/1086489/fdinfo/2 /proc/1086501/fdinfo/0 /proc/1086501/fdinfo/1 /proc/1086501/fdinfo/2 /proc/1086501/fdinfo/9 /proc/1086502/fdinfo/0 /proc/1086502/fdinfo/1 /proc/1086502/fdinfo/10 /proc/1086502/fdinfo/11 /proc/1086502/fdinfo/2 /proc/1086508/fdinfo/0 /proc/1086508/fdinfo/1 /proc/1086508/fdinfo/2 /proc/1086508/fdinfo/3 /proc/1086516/fdinfo/0 /proc/1086516/fdinfo/1 /proc/1086516/fdinfo/10 /proc/1086516/fdinfo/11 /proc/1086516/fdinfo/2 /proc/1086531/fdinfo/0 /proc/1086531/fdinfo/1 /proc/1086531/fdinfo/10 /proc/1086531/fdinfo/11 /proc/1086531/fdinfo/2 /proc/1086574/fdinfo/0 /proc/1086574/fdinfo/1 /proc/1086574/fdinfo/2 /proc/1086574/fdinfo/9 /proc/1086576/fdinfo/0 /proc/1086576/fdinfo/1 /proc/1086576/fdinfo/2 /proc/1086576/fdinfo/9 /proc/1086580/fdinfo/0 /proc/1086580/fdinfo/1 /proc/1086580/fdinfo/2 /proc/1086580/fdinfo/3 /proc/1086580/fdinfo/4 /proc/1086580/fdinfo/5 /proc/1086580/fdinfo/7 /proc/1086652/fdinfo/0 /proc/1086652/fdinfo/1 /proc/1086652/fdinfo/10 /proc/1086652/fdinfo/11 /proc/1086652/fdinfo/2 /proc/1086665/fdinfo/0 /proc/1086665/fdinfo/1 /proc/1086665/fdinfo/10 /proc/1086665/fdinfo/11 /proc/1086665/fdinfo/2 /proc/1086722/fdinfo/0 /proc/1086722/fdinfo/1 /proc/1086722/fdinfo/2 /proc/1086722/fdinfo/255 /proc/1086722/fdinfo/3 /proc/1086722/fdinfo/9 /proc/1086733/fdinfo/0 /proc/1086733/fdinfo/1 /proc/1086733/fdinfo/2 /proc/1086749/fdinfo/0 /proc/1086749/fdinfo/1 /proc/1086749/fdinfo/2 /proc/1086749/fdinfo/255 /proc/1086749/fdinfo/3 /proc/1086757/fdinfo/0 /proc/1086757/fdinfo/1 /proc/1086757/fdinfo/10 /proc/1086757/fdinfo/11 /proc/1086757/fdinfo/2 /proc/1086766/fdinfo/0 /proc/1086766/fdinfo/1 /proc/1086766/fdinfo/2 /proc/1086766/fdinfo/255 /proc/1086766/fdinfo/3 /proc/1086804/fdinfo/0 /proc/1086804/fdinfo/1 /proc/1086804/fdinfo/10 /proc/1086804/fdinfo/2 /proc/1086804/fdinfo/255 /proc/1086804/fdinfo/3 /proc/1086849/fdinfo/0 /proc/1086849/fdinfo/1 /proc/1086849/fdinfo/2 /proc/1086849/fdinfo/255 /proc/1086849/fdinfo/3 /proc/1086856/fdinfo/0 /proc/1086856/fdinfo/1 /proc/1086856/fdinfo/2 /proc/1086856/fdinfo/255 /proc/1086856/fdinfo/3 /proc/1087614/fdinfo/0 /proc/1087614/fdinfo/1 /proc/1087614/fdinfo/2 /proc/1087712/fdinfo/0 /proc/1087712/fdinfo/1 /proc/1087712/fdinfo/2 /proc/1087712/fdinfo/255 /proc/1087855/fdinfo/0 /proc/1087855/fdinfo/1 /proc/1087855/fdinfo/2 /proc/1088100/fdinfo/0 /proc/1088100/fdinfo/1 /proc/1088100/fdinfo/2 /proc/1088100/fdinfo/255 /proc/1088100/fdinfo/3 /proc/1088139/fdinfo/0 /proc/1088139/fdinfo/1 /proc/1088139/fdinfo/2 /proc/1088311/fdinfo/0 /proc/1088311/fdinfo/1 /proc/1088311/fdinfo/10 /proc/1088311/fdinfo/2 /proc/1088311/fdinfo/255 /proc/1088711/fdinfo/0 /proc/1088711/fdinfo/1 /proc/1088711/fdinfo/2 /proc/1088763/fdinfo/0 /proc/1088763/fdinfo/1 /proc/1088763/fdinfo/2 /proc/1088763/fdinfo/3 /proc/1088763/fdinfo/5 /proc/1089279/fdinfo/0 /proc/1089279/fdinfo/1 /proc/1089279/fdinfo/2 /proc/1089279/fdinfo/255 /proc/1089279/fdinfo/3 /proc/1090007/fdinfo/0 /proc/1090007/fdinfo/1 /proc/1090007/fdinfo/2 /proc/1091052/fdinfo/0 /proc/1091052/fdinfo/1 /proc/1091052/fdinfo/2 /proc/1091111/fdinfo/0 /proc/1091111/fdinfo/1 /proc/1091111/fdinfo/2 /proc/1091111/fdinfo/255 /proc/1091153/fdinfo/0 /proc/1091153/fdinfo/1 /proc/1091153/fdinfo/2 /proc/1091153/fdinfo/3 /proc/1091196/fdinfo/0 /proc/1091196/fdinfo/1 /proc/1091196/fdinfo/2 /proc/1091268/fdinfo/0 /proc/1091268/fdinfo/1 /proc/1091268/fdinfo/2 /proc/1091268/fdinfo/255 /proc/1092162/fdinfo/0 /proc/1092162/fdinfo/1 /proc/1092162/fdinfo/2 /proc/1092242/fdinfo/0 /proc/1092242/fdinfo/1 /proc/1092242/fdinfo/2 /proc/1092242/fdinfo/255 /proc/1093623/fdinfo/0 /proc/1093623/fdinfo/1 /proc/1093623/fdinfo/2 /proc/1094189/fdinfo/0 /proc/1094189/fdinfo/1 /proc/1094189/fdinfo/2 /proc/1094189/fdinfo/255 /proc/1094189/fdinfo/3 /proc/1094621/fdinfo/0 /proc/1094621/fdinfo/1 /proc/1094621/fdinfo/2 /proc/1094716/fdinfo/0 /proc/1094716/fdinfo/1 /proc/1094716/fdinfo/2 /proc/1094716/fdinfo/255 /proc/1094716/fdinfo/3 /proc/1096522/fdinfo/0 /proc/1096522/fdinfo/1 /proc/1096522/fdinfo/10 /proc/1096522/fdinfo/2 /proc/1096522/fdinfo/3 /proc/1096651/fdinfo/0 /proc/1096651/fdinfo/1 /proc/1096651/fdinfo/2 /proc/1097200/fdinfo/0 /proc/1097200/fdinfo/1 /proc/1097200/fdinfo/2 /proc/1097234/fdinfo/0 /proc/1097234/fdinfo/1 /proc/1097234/fdinfo/2 /proc/1097234/fdinfo/3 /proc/1097234/fdinfo/5 /proc/1097404/fdinfo/0 /proc/1097404/fdinfo/1 /proc/1097404/fdinfo/2 /proc/1097470/fdinfo/0 /proc/1097470/fdinfo/1 /proc/1097470/fdinfo/2 /proc/1097470/fdinfo/255 /proc/1097470/fdinfo/3 /proc/1097564/fdinfo/0 /proc/1097564/fdinfo/1 /proc/1097564/fdinfo/2 /proc/1097564/fdinfo/3 /proc/1098096/fdinfo/0 /proc/1098096/fdinfo/1 /proc/1098096/fdinfo/2 /proc/1098180/fdinfo/0 /proc/1098180/fdinfo/1 /proc/1098180/fdinfo/2 /proc/1098180/fdinfo/255 /proc/1098180/fdinfo/3 /proc/1098214/fdinfo/0 /proc/1098214/fdinfo/1 /proc/1098214/fdinfo/2 /proc/1098214/fdinfo/3 /proc/1099369/fdinfo/0 /proc/1099369/fdinfo/1 /proc/1099369/fdinfo/2 /proc/1099439/fdinfo/0 /proc/1099439/fdinfo/1 /proc/1099439/fdinfo/2 /proc/1099439/fdinfo/255 /proc/1099439/fdinfo/3 /proc/1099441/fdinfo/0 /proc/1099441/fdinfo/1 /proc/1099441/fdinfo/2 /proc/1100051/fdinfo/0 /proc/1100051/fdinfo/1 /proc/1100051/fdinfo/2 /proc/1100087/fdinfo/0 /proc/1100087/fdinfo/1 /proc/1100087/fdinfo/2 /proc/1100087/fdinfo/255 /proc/1100180/fdinfo/0 /proc/1100180/fdinfo/1 /proc/1100180/fdinfo/2 /proc/1100235/fdinfo/0 /proc/1100235/fdinfo/1 /proc/1100235/fdinfo/10 /proc/1100235/fdinfo/11 /proc/1100235/fdinfo/2 /proc/1100235/fdinfo/255 /proc/1100559/fdinfo/0 /proc/1100559/fdinfo/1 /proc/1100559/fdinfo/2 /proc/1100559/fdinfo/255 /proc/1100559/fdinfo/3 /proc/1101738/fdinfo/0 /proc/1101738/fdinfo/1 /proc/1101738/fdinfo/2 /proc/1102155/fdinfo/0 /proc/1102155/fdinfo/1 /proc/1102155/fdinfo/2 /proc/1102174/fdinfo/0 /proc/1102174/fdinfo/1 /proc/1102174/fdinfo/2 /proc/1102247/fdinfo/0 /proc/1102247/fdinfo/1 /proc/1102247/fdinfo/2 /proc/1102247/fdinfo/255 /proc/1102247/fdinfo/3 /proc/1102266/fdinfo/0 /proc/1102266/fdinfo/1 /proc/1102266/fdinfo/2 /proc/1102332/fdinfo/0 /proc/1102332/fdinfo/1 /proc/1102332/fdinfo/2 /proc/1102332/fdinfo/255 /proc/1102332/fdinfo/3 /proc/1103494/fdinfo/0 /proc/1103494/fdinfo/1 /proc/1103494/fdinfo/2 /proc/1103494/fdinfo/255 /proc/1103494/fdinfo/3 /proc/1103494/fdinfo/9 /proc/1103764/fdinfo/0 /proc/1103764/fdinfo/1 /proc/1103764/fdinfo/2 /proc/1103792/fdinfo/0 /proc/1103792/fdinfo/1 /proc/1103792/fdinfo/2 /proc/1103792/fdinfo/255 /proc/1104116/fdinfo/0 /proc/1104116/fdinfo/1 /proc/1104116/fdinfo/2 /proc/1104232/fdinfo/0 /proc/1104232/fdinfo/1 /proc/1104232/fdinfo/2 /proc/1104328/fdinfo/0 /proc/1104328/fdinfo/1 /proc/1104328/fdinfo/10 /proc/1104328/fdinfo/11 /proc/1104328/fdinfo/2 /proc/1104328/fdinfo/255 /proc/1104328/fdinfo/3 /proc/1104503/fdinfo/0 /proc/1104503/fdinfo/1 /proc/1104503/fdinfo/2 /proc/1104558/fdinfo/0 /proc/1104558/fdinfo/1 /proc/1104558/fdinfo/2 /proc/1104558/fdinfo/255 /proc/1104558/fdinfo/3 /proc/1105467/fdinfo/0 /proc/1105467/fdinfo/1 /proc/1105467/fdinfo/2 /proc/1105493/fdinfo/0 /proc/1105493/fdinfo/1 /proc/1105493/fdinfo/2 /proc/1105493/fdinfo/255 /proc/1105781/fdinfo/0 /proc/1105781/fdinfo/1 /proc/1105781/fdinfo/2 /proc/1105829/fdinfo/0 /proc/1105829/fdinfo/1 /proc/1105829/fdinfo/2 /proc/1105829/fdinfo/255 /proc/1105829/fdinfo/3 /proc/1106167/fdinfo/0 /proc/1106167/fdinfo/1 /proc/1106167/fdinfo/2 /proc/1106248/fdinfo/0 /proc/1106248/fdinfo/1 /proc/1106248/fdinfo/2 /proc/1106248/fdinfo/255 /proc/1106291/fdinfo/0 /proc/1106291/fdinfo/1 /proc/1106291/fdinfo/2 /proc/1106348/fdinfo/0 /proc/1106348/fdinfo/1 /proc/1106348/fdinfo/2 /proc/1106348/fdinfo/255 /proc/1106348/fdinfo/3 /proc/1106480/fdinfo/0 /proc/1106480/fdinfo/1 /proc/1106480/fdinfo/2 /proc/1106480/fdinfo/255 /proc/1106480/fdinfo/3 /proc/1106811/fdinfo/0 /proc/1106811/fdinfo/1 /proc/1106811/fdinfo/2 /proc/1106886/fdinfo/0 /proc/1106886/fdinfo/1 /proc/1106886/fdinfo/2 /proc/1106886/fdinfo/255 /proc/1106886/fdinfo/3 /proc/1106976/fdinfo/0 /proc/1106976/fdinfo/1 /proc/1106976/fdinfo/2 /proc/1107145/fdinfo/0 /proc/1107145/fdinfo/1 /proc/1107145/fdinfo/2 /proc/1107224/fdinfo/0 /proc/1107224/fdinfo/1 /proc/1107224/fdinfo/2 /proc/1107224/fdinfo/255 /proc/1107224/fdinfo/3 /proc/1107376/fdinfo/0 /proc/1107376/fdinfo/1 /proc/1107376/fdinfo/2 /proc/1107376/fdinfo/3 /proc/1107422/fdinfo/0 /proc/1107422/fdinfo/1 /proc/1107422/fdinfo/2 /proc/1107422/fdinfo/3 /proc/1108042/fdinfo/0 /proc/1108042/fdinfo/1 /proc/1108042/fdinfo/2 /proc/1108080/fdinfo/0 /proc/1108080/fdinfo/1 /proc/1108080/fdinfo/2 /proc/1108080/fdinfo/255 /proc/1108080/fdinfo/3 /proc/1108298/fdinfo/0 /proc/1108298/fdinfo/1 /proc/1108298/fdinfo/2 /proc/1108312/fdinfo/0 /proc/1108312/fdinfo/1 /proc/1108312/fdinfo/2 /proc/1108312/fdinfo/255 /proc/1109172/fdinfo/0 /proc/1109172/fdinfo/1 /proc/1109172/fdinfo/2 /proc/1109287/fdinfo/0 /proc/1109287/fdinfo/1 /proc/1109287/fdinfo/2 /proc/1109287/fdinfo/255 /proc/1109611/fdinfo/0 /proc/1109611/fdinfo/1 /proc/1109611/fdinfo/2 /proc/1109679/fdinfo/0 /proc/1109679/fdinfo/1 /proc/1109679/fdinfo/2 /proc/1109679/fdinfo/255 /proc/1109679/fdinfo/3 /proc/1109708/fdinfo/0 /proc/1109708/fdinfo/1 /proc/1109708/fdinfo/2 /proc/1109737/fdinfo/0 /proc/1109737/fdinfo/1 /proc/1109737/fdinfo/2 /proc/1109737/fdinfo/3 /proc/1109738/fdinfo/0 /proc/1109738/fdinfo/1 /proc/1109738/fdinfo/2 /proc/1109812/fdinfo/0 /proc/1109812/fdinfo/1 /proc/1109812/fdinfo/2 /proc/1110237/fdinfo/0 /proc/1110237/fdinfo/1 /proc/1110237/fdinfo/2 /proc/1110237/fdinfo/3 /proc/1110238/fdinfo/0 /proc/1110238/fdinfo/1 /proc/1110238/fdinfo/2 /proc/1110238/fdinfo/255 /proc/1110238/fdinfo/3 /proc/1110238/fdinfo/9 /proc/1110242/fdinfo/0 /proc/1110242/fdinfo/1 /proc/1110242/fdinfo/2 /proc/1110246/fdinfo/0 /proc/1110246/fdinfo/1 /proc/1110246/fdinfo/2 /proc/1110250/fdinfo/0 /proc/1110250/fdinfo/1 /proc/1110250/fdinfo/2 /proc/1110250/fdinfo/255 /proc/1110250/fdinfo/3 /proc/1110252/fdinfo/0 /proc/1110252/fdinfo/1 /proc/1110252/fdinfo/2 /proc/1110254/fdinfo/0 /proc/1110254/fdinfo/1 /proc/1110254/fdinfo/2 /proc/1110254/fdinfo/255 /proc/1110257/fdinfo/0 /proc/1110257/fdinfo/1 /proc/1110257/fdinfo/2 /proc/1110257/fdinfo/3 /proc/1110258/fdinfo/0 /proc/1110258/fdinfo/1 /proc/1110258/fdinfo/2 /proc/1110259/fdinfo/0 /proc/1110259/fdinfo/1 /proc/1110259/fdinfo/2 /proc/1110262/fdinfo/0 /proc/1110262/fdinfo/1 /proc/1110262/fdinfo/2 /proc/1110262/fdinfo/255 /proc/1110262/fdinfo/3 /proc/1110263/fdinfo/0 /proc/1110263/fdinfo/1 /proc/1110263/fdinfo/2 /proc/1110263/fdinfo/255 /proc/1110263/fdinfo/3 /proc/1110266/fdinfo/0 /proc/1110266/fdinfo/1 /proc/1110266/fdinfo/2 /proc/1110266/fdinfo/3 /proc/1110268/fdinfo/0 /proc/1110268/fdinfo/1 /proc/1110268/fdinfo/10 /proc/1110268/fdinfo/2 /proc/1110268/fdinfo/3 /proc/1110268/fdinfo/63 /proc/1110269/fdinfo/0 /proc/1110269/fdinfo/1 /proc/1110269/fdinfo/10 /proc/1110269/fdinfo/2 /proc/1110271/fdinfo/0 /proc/1110271/fdinfo/1 /proc/1110271/fdinfo/2 /proc/1110272/fdinfo/0 /proc/1110272/fdinfo/1 /proc/1110272/fdinfo/2 /proc/1110282/fdinfo/0 /proc/1110282/fdinfo/1 /proc/1110282/fdinfo/2 /proc/1110288/fdinfo/0 /proc/1110288/fdinfo/1 /proc/1110288/fdinfo/2 /proc/1110289/fdinfo/0 /proc/1110289/fdinfo/1 /proc/1110289/fdinfo/2 /proc/1110291/fdinfo/0 /proc/1110291/fdinfo/1 /proc/1110291/fdinfo/2 /proc/1110292/fdinfo/0 /proc/1110292/fdinfo/1 /proc/1110292/fdinfo/2 /proc/1110297/fdinfo/0 /proc/1110297/fdinfo/1 /proc/1110297/fdinfo/2 /proc/1110302/fdinfo/0 /proc/1110302/fdinfo/1 /proc/1110302/fdinfo/10 /proc/1110302/fdinfo/2 /proc/1110302/fdinfo/3 /proc/1110303/fdinfo/0 /proc/1110303/fdinfo/1 /proc/1110303/fdinfo/2 /proc/1110303/fdinfo/255 /proc/1110312/fdinfo/0 /proc/1110312/fdinfo/1 /proc/1110312/fdinfo/2 /proc/1110312/fdinfo/3 /proc/1110313/fdinfo/0 /proc/1110313/fdinfo/1 /proc/1110313/fdinfo/2 /proc/1110313/fdinfo/4 /proc/1110314/fdinfo/0 /proc/1110314/fdinfo/1 /proc/1110314/fdinfo/2 /proc/1110326/fdinfo/0 /proc/1110326/fdinfo/1 /proc/1110326/fdinfo/2 /proc/1110327/fdinfo/0 /proc/1110327/fdinfo/1 /proc/1110327/fdinfo/10 /proc/1110327/fdinfo/11 /proc/1110327/fdinfo/12 /proc/1110327/fdinfo/2 /proc/1110327/fdinfo/255 /proc/1110327/fdinfo/3 /proc/1110328/fdinfo/0 /proc/1110328/fdinfo/1 /proc/1110328/fdinfo/2 /proc/1110328/fdinfo/255 /proc/1110328/fdinfo/3 /proc/1110330/fdinfo/0 /proc/1110330/fdinfo/1 /proc/1110330/fdinfo/10 /proc/1110330/fdinfo/2 /proc/1110330/fdinfo/3 /proc/1110331/fdinfo/0 /proc/1110331/fdinfo/1 /proc/1110331/fdinfo/2 /proc/1110332/fdinfo/0 /proc/1110332/fdinfo/1 /proc/1110332/fdinfo/2 /proc/1110333/fdinfo/0 /proc/1110333/fdinfo/1 /proc/1110333/fdinfo/2 /proc/1110340/fdinfo/0 /proc/1110340/fdinfo/1 /proc/1110340/fdinfo/2 /proc/1110340/fdinfo/3 /proc/1110340/fdinfo/9 /proc/1110341/fdinfo/0 /proc/1110341/fdinfo/1 /proc/1110341/fdinfo/2 /proc/1110342/fdinfo/0 /proc/1110342/fdinfo/1 /proc/1110342/fdinfo/2 /proc/1110343/fdinfo/0 /proc/1110343/fdinfo/1 /proc/1110343/fdinfo/2 /proc/1110349/fdinfo/0 /proc/1110349/fdinfo/1 /proc/1110349/fdinfo/2 /proc/1110349/fdinfo/255 /proc/1110349/fdinfo/3 /proc/1110351/fdinfo/0 /proc/1110351/fdinfo/1 /proc/1110351/fdinfo/2 /proc/1110353/fdinfo/0 /proc/1110353/fdinfo/1 /proc/1110353/fdinfo/2 /proc/1110357/fdinfo/0 /proc/1110357/fdinfo/1 /proc/1110357/fdinfo/2 /proc/1110357/fdinfo/255 /proc/1110357/fdinfo/3 /proc/1110359/fdinfo/0 /proc/1110359/fdinfo/1 /proc/1110359/fdinfo/2 /proc/1110359/fdinfo/255 /proc/1110360/fdinfo/0 /proc/1110360/fdinfo/1 /proc/1110360/fdinfo/2 /proc/1110361/fdinfo/0 /proc/1110361/fdinfo/1 /proc/1110361/fdinfo/2 /proc/1110361/fdinfo/255 /proc/1110361/fdinfo/3 /proc/1110361/fdinfo/4 /proc/1110362/fdinfo/0 /proc/1110362/fdinfo/1 /proc/1110362/fdinfo/2 /proc/1110362/fdinfo/255 /proc/1110363/fdinfo/0 /proc/1110363/fdinfo/1 /proc/1110363/fdinfo/10 /proc/1110363/fdinfo/11 /proc/1110363/fdinfo/2 /proc/1110363/fdinfo/255 /proc/1110364/fdinfo/0 /proc/1110364/fdinfo/1 /proc/1110364/fdinfo/2 /proc/1110364/fdinfo/255 /proc/1110365/fdinfo/0 /proc/1110365/fdinfo/1 /proc/1110365/fdinfo/2 /proc/1110367/fdinfo/0 /proc/1110367/fdinfo/1 /proc/1110367/fdinfo/2 /proc/1110370/fdinfo/0 /proc/1110370/fdinfo/1 /proc/1110370/fdinfo/10 /proc/1110370/fdinfo/2 /proc/1110370/fdinfo/3 /proc/1110373/fdinfo/0 /proc/1110373/fdinfo/1 /proc/1110373/fdinfo/2 /proc/1110377/fdinfo/0 /proc/1110377/fdinfo/1 /proc/1110377/fdinfo/2 /proc/1110378/fdinfo/0 /proc/1110378/fdinfo/1 /proc/1110378/fdinfo/2 /proc/1110380/fdinfo/0 /proc/1110380/fdinfo/1 /proc/1110380/fdinfo/2 /proc/1110380/fdinfo/3 /proc/1110381/fdinfo/0 /proc/1110381/fdinfo/1 /proc/1110381/fdinfo/2 /proc/1110382/fdinfo/0 /proc/1110382/fdinfo/1 /proc/1110382/fdinfo/2 /proc/1110383/fdinfo/0 /proc/1110383/fdinfo/1 /proc/1110383/fdinfo/2 /proc/1110384/fdinfo/0 /proc/1110384/fdinfo/1 /proc/1110384/fdinfo/2 /proc/1110389/fdinfo/0 /proc/1110389/fdinfo/1 /proc/1110389/fdinfo/2 /proc/1110390/fdinfo/0 /proc/1110390/fdinfo/1 /proc/1110390/fdinfo/2 /proc/1110393/fdinfo/0 /proc/1110393/fdinfo/1 /proc/1110393/fdinfo/2 /proc/1110400/fdinfo/0 /proc/1110400/fdinfo/1 /proc/1110400/fdinfo/2 /proc/1110402/fdinfo/0 /proc/1110402/fdinfo/1 /proc/1110402/fdinfo/10 /proc/1110402/fdinfo/11 /proc/1110402/fdinfo/2 /proc/1110402/fdinfo/3 /proc/1110404/fdinfo/0 /proc/1110404/fdinfo/1 /proc/1110404/fdinfo/2 /proc/1110406/fdinfo/0 /proc/1110406/fdinfo/1 /proc/1110406/fdinfo/2 /proc/1110409/fdinfo/0 /proc/1110409/fdinfo/1 /proc/1110409/fdinfo/2 /proc/1110409/fdinfo/255 /proc/1110409/fdinfo/3 /proc/1110413/fdinfo/0 /proc/1110413/fdinfo/1 /proc/1110413/fdinfo/2 /proc/1110417/fdinfo/0 /proc/1110417/fdinfo/1 /proc/1110417/fdinfo/2 /proc/1110419/fdinfo/0 /proc/1110419/fdinfo/1 /proc/1110419/fdinfo/2 /proc/1110422/fdinfo/0 /proc/1110422/fdinfo/1 /proc/1110422/fdinfo/10 /proc/1110422/fdinfo/2 /proc/1110422/fdinfo/63 /proc/1110425/fdinfo/0 /proc/1110425/fdinfo/1 /proc/1110425/fdinfo/2 /proc/1110427/fdinfo/0 /proc/1110427/fdinfo/1 /proc/1110427/fdinfo/2 /proc/1110428/fdinfo/0 /proc/1110428/fdinfo/1 /proc/1110428/fdinfo/2 /proc/1110428/fdinfo/3 /proc/1110429/fdinfo/0 /proc/1110429/fdinfo/1 /proc/1110429/fdinfo/2 /proc/1110429/fdinfo/255 /proc/1110429/fdinfo/3 /proc/1110431/fdinfo/0 /proc/1110431/fdinfo/1 /proc/1110431/fdinfo/2 /proc/1110435/fdinfo/0 /proc/1110435/fdinfo/1 /proc/1110435/fdinfo/2 /proc/1110435/fdinfo/255 /proc/1110435/fdinfo/3 /proc/1110436/fdinfo/0 /proc/1110436/fdinfo/1 /proc/1110436/fdinfo/2 /proc/1110438/fdinfo/0 /proc/1110438/fdinfo/1 /proc/1110438/fdinfo/10 /proc/1110438/fdinfo/2 /proc/1110438/fdinfo/255 /proc/1110438/fdinfo/3 /proc/1110438/fdinfo/9 /proc/1110439/fdinfo/0 /proc/1110439/fdinfo/1 /proc/1110439/fdinfo/2 /proc/1110439/fdinfo/255 /proc/1110439/fdinfo/3 /proc/1110440/fdinfo/0 /proc/1110440/fdinfo/1 /proc/1110440/fdinfo/2 /proc/1110441/fdinfo/0 /proc/1110441/fdinfo/1 /proc/1110441/fdinfo/2 /proc/1110447/fdinfo/0 /proc/1110447/fdinfo/1 /proc/1110447/fdinfo/2 /proc/1110447/fdinfo/255 /proc/1110448/fdinfo/0 /proc/1110448/fdinfo/1 /proc/1110448/fdinfo/2 /proc/1110449/fdinfo/0 /proc/1110449/fdinfo/1 /proc/1110449/fdinfo/2 /proc/1110450/fdinfo/0 /proc/1110450/fdinfo/1 /proc/1110450/fdinfo/2 /proc/1110457/fdinfo/0 /proc/1110457/fdinfo/1 /proc/1110457/fdinfo/2 /proc/1110458/fdinfo/0 /proc/1110458/fdinfo/1 /proc/1110458/fdinfo/2 /proc/1110459/fdinfo/0 /proc/1110459/fdinfo/1 /proc/1110459/fdinfo/2 /proc/1110459/fdinfo/255 /proc/1110460/fdinfo/0 /proc/1110460/fdinfo/1 /proc/1110460/fdinfo/2 /proc/1110462/fdinfo/0 /proc/1110462/fdinfo/1 /proc/1110462/fdinfo/10 /proc/1110462/fdinfo/11 /proc/1110462/fdinfo/2 /proc/1110462/fdinfo/9 /proc/1110463/fdinfo/0 /proc/1110463/fdinfo/1 /proc/1110463/fdinfo/2 /proc/1110465/fdinfo/0 /proc/1110465/fdinfo/1 /proc/1110465/fdinfo/2 /proc/1110465/fdinfo/255 /proc/1110465/fdinfo/3 /proc/1110468/fdinfo/0 /proc/1110468/fdinfo/1 /proc/1110468/fdinfo/2 /proc/1110475/fdinfo/0 /proc/1110475/fdinfo/1 /proc/1110475/fdinfo/2 /proc/1110477/fdinfo/0 /proc/1110477/fdinfo/1 /proc/1110477/fdinfo/2 /proc/1110479/fdinfo/0 /proc/1110479/fdinfo/1 /proc/1110479/fdinfo/2 /proc/1110479/fdinfo/3 /proc/1110479/fdinfo/9 /proc/1110481/fdinfo/0 /proc/1110481/fdinfo/1 /proc/1110481/fdinfo/2 /proc/1110481/fdinfo/3 /proc/1110482/fdinfo/0 /proc/1110482/fdinfo/1 /proc/1110482/fdinfo/2 /proc/1110482/fdinfo/255 /proc/1110482/fdinfo/3 /proc/1110486/fdinfo/0 /proc/1110486/fdinfo/1 /proc/1110486/fdinfo/2 /proc/1110487/fdinfo/0 /proc/1110487/fdinfo/1 /proc/1110487/fdinfo/2 /proc/1110487/fdinfo/255 /proc/1110487/fdinfo/3 /proc/1110489/fdinfo/0 /proc/1110489/fdinfo/1 /proc/1110489/fdinfo/2 /proc/1110489/fdinfo/255 /proc/1110490/fdinfo/0 /proc/1110490/fdinfo/1 /proc/1110490/fdinfo/2 /proc/1110494/fdinfo/0 /proc/1110494/fdinfo/1 /proc/1110494/fdinfo/2 /proc/1110494/fdinfo/255 /proc/1110495/fdinfo/0 /proc/1110495/fdinfo/1 /proc/1110495/fdinfo/2 /proc/1110497/fdinfo/0 /proc/1110497/fdinfo/1 /proc/1110497/fdinfo/2 /proc/1110497/fdinfo/3 /proc/1110499/fdinfo/0 /proc/1110499/fdinfo/1 /proc/1110499/fdinfo/2 /proc/1110499/fdinfo/255 /proc/1110499/fdinfo/3 /proc/1110500/fdinfo/0 /proc/1110500/fdinfo/1 /proc/1110500/fdinfo/2 /proc/1110500/fdinfo/255 /proc/1110500/fdinfo/3 /proc/1110506/fdinfo/0 /proc/1110506/fdinfo/1 /proc/1110506/fdinfo/2 /proc/1110506/fdinfo/3 /proc/1110513/fdinfo/0 /proc/1110513/fdinfo/1 /proc/1110513/fdinfo/2 /proc/1110513/fdinfo/3 /proc/1110515/fdinfo/0 /proc/1110515/fdinfo/1 /proc/1110515/fdinfo/2 /proc/1110518/fdinfo/0 /proc/1110518/fdinfo/1 /proc/1110518/fdinfo/2 /proc/1110519/fdinfo/0 /proc/1110519/fdinfo/1 /proc/1110519/fdinfo/2 /proc/1110519/fdinfo/3 /proc/1110519/fdinfo/5 /proc/1110522/fdinfo/0 /proc/1110522/fdinfo/1 /proc/1110522/fdinfo/10 /proc/1110522/fdinfo/2 /proc/1110522/fdinfo/3 /proc/1110522/fdinfo/63 /proc/1110523/fdinfo/0 /proc/1110523/fdinfo/1 /proc/1110523/fdinfo/2 /proc/1110524/fdinfo/0 /proc/1110524/fdinfo/1 /proc/1110524/fdinfo/2 /proc/1110526/fdinfo/0 /proc/1110526/fdinfo/1 /proc/1110526/fdinfo/2 /proc/1110526/fdinfo/255 /proc/1110526/fdinfo/3 /proc/1110529/fdinfo/0 /proc/1110529/fdinfo/1 /proc/1110529/fdinfo/2 /proc/1110534/fdinfo/0 /proc/1110534/fdinfo/1 /proc/1110534/fdinfo/10 /proc/1110534/fdinfo/2 /proc/1110534/fdinfo/63 /proc/1110536/fdinfo/0 /proc/1110536/fdinfo/1 /proc/1110536/fdinfo/2 /proc/1110536/fdinfo/3 /proc/1110536/fdinfo/4 /proc/1110536/fdinfo/5 /proc/1110536/fdinfo/6 /proc/1110536/fdinfo/8 /proc/1110538/fdinfo/0 /proc/1110538/fdinfo/1 /proc/1110538/fdinfo/2 /proc/1110538/fdinfo/255 /proc/1110538/fdinfo/3 /proc/1110539/fdinfo/0 /proc/1110539/fdinfo/1 /proc/1110539/fdinfo/2 /proc/1110539/fdinfo/3 /proc/1110540/fdinfo/0 /proc/1110540/fdinfo/1 /proc/1110540/fdinfo/2 /proc/1110544/fdinfo/0 /proc/1110544/fdinfo/1 /proc/1110544/fdinfo/2 /proc/1110545/fdinfo/0 /proc/1110545/fdinfo/1 /proc/1110545/fdinfo/2 /proc/1110545/fdinfo/3 /proc/1110545/fdinfo/5 /proc/1110546/fdinfo/0 /proc/1110546/fdinfo/1 /proc/1110546/fdinfo/2 /proc/1110546/fdinfo/255 /proc/1110546/fdinfo/3 /proc/1110547/fdinfo/0 /proc/1110547/fdinfo/1 /proc/1110547/fdinfo/2 /proc/1110549/fdinfo/0 /proc/1110549/fdinfo/1 /proc/1110549/fdinfo/2 /proc/1110549/fdinfo/255 /proc/1110549/fdinfo/3 /proc/1110553/fdinfo/0 /proc/1110553/fdinfo/1 /proc/1110553/fdinfo/2 /proc/1110553/fdinfo/255 /proc/1110553/fdinfo/9 /proc/1110554/fdinfo/0 /proc/1110554/fdinfo/1 /proc/1110554/fdinfo/2 /proc/1110554/fdinfo/255 /proc/1110554/fdinfo/3 /proc/1110558/fdinfo/0 /proc/1110558/fdinfo/1 /proc/1110558/fdinfo/2 /proc/1110559/fdinfo/0 /proc/1110559/fdinfo/1 /proc/1110559/fdinfo/2 /proc/1110560/fdinfo/0 /proc/1110560/fdinfo/1 /proc/1110560/fdinfo/2 /proc/1110561/fdinfo/0 /proc/1110561/fdinfo/1 /proc/1110561/fdinfo/2 /proc/1110563/fdinfo/0 /proc/1110563/fdinfo/1 /proc/1110563/fdinfo/2 /proc/1110564/fdinfo/0 /proc/1110564/fdinfo/1 /proc/1110564/fdinfo/2 /proc/1110567/fdinfo/0 /proc/1110567/fdinfo/1 /proc/1110567/fdinfo/2 /proc/1110567/fdinfo/255 /proc/1110568/fdinfo/0 /proc/1110568/fdinfo/1 /proc/1110568/fdinfo/2 /proc/1110568/fdinfo/3 /proc/1110568/fdinfo/4 /proc/1110569/fdinfo/0 /proc/1110569/fdinfo/1 /proc/1110569/fdinfo/2 /proc/1110572/fdinfo/0 /proc/1110572/fdinfo/1 /proc/1110572/fdinfo/2 /proc/1110574/fdinfo/0 /proc/1110574/fdinfo/1 /proc/1110574/fdinfo/2 /proc/1110576/fdinfo/0 /proc/1110576/fdinfo/1 /proc/1110576/fdinfo/2 /proc/1110576/fdinfo/255 /proc/1110577/fdinfo/0 /proc/1110577/fdinfo/1 /proc/1110577/fdinfo/2 /proc/1110577/fdinfo/255 /proc/1110577/fdinfo/3 /proc/1110578/fdinfo/0 /proc/1110578/fdinfo/1 /proc/1110578/fdinfo/2 /proc/1110580/fdinfo/0 /proc/1110580/fdinfo/1 /proc/1110580/fdinfo/2 /proc/1110585/fdinfo/0 /proc/1110585/fdinfo/1 /proc/1110585/fdinfo/2 /proc/1110585/fdinfo/3 /proc/1110587/fdinfo/0 /proc/1110587/fdinfo/1 /proc/1110587/fdinfo/2 /proc/1110588/fdinfo/0 /proc/1110588/fdinfo/1 /proc/1110588/fdinfo/2 /proc/1110588/fdinfo/3 /proc/1110590/fdinfo/0 /proc/1110590/fdinfo/1 /proc/1110590/fdinfo/2 /proc/1110592/fdinfo/0 /proc/1110592/fdinfo/1 /proc/1110592/fdinfo/2 /proc/1110594/fdinfo/0 /proc/1110594/fdinfo/1 /proc/1110594/fdinfo/2 /proc/1110597/fdinfo/0 /proc/1110597/fdinfo/1 /proc/1110597/fdinfo/2 /proc/1110597/fdinfo/255 /proc/1110597/fdinfo/9 /proc/1110598/fdinfo/0 /proc/1110598/fdinfo/1 /proc/1110598/fdinfo/2 /proc/1110598/fdinfo/9 /proc/1110599/fdinfo/0 /proc/1110599/fdinfo/1 /proc/1110599/fdinfo/2 /proc/1110600/fdinfo/0 /proc/1110600/fdinfo/1 /proc/1110600/fdinfo/2 /proc/1110601/fdinfo/0 /proc/1110601/fdinfo/1 /proc/1110601/fdinfo/2 /proc/1110602/fdinfo/0 /proc/1110602/fdinfo/1 /proc/1110602/fdinfo/2 /proc/1110603/fdinfo/0 /proc/1110603/fdinfo/1 /proc/1110603/fdinfo/2 /proc/1110604/fdinfo/0 /proc/1110604/fdinfo/1 /proc/1110604/fdinfo/2 /proc/1110604/fdinfo/3 /proc/1110607/fdinfo/0 /proc/1110607/fdinfo/1 /proc/1110607/fdinfo/2 /proc/1110609/fdinfo/0 /proc/1110609/fdinfo/1 /proc/1110609/fdinfo/2 /proc/1110610/fdinfo/0 /proc/1110610/fdinfo/1 /proc/1110610/fdinfo/2 /proc/1110612/fdinfo/0 /proc/1110612/fdinfo/1 /proc/1110612/fdinfo/2 /proc/1110613/fdinfo/0 /proc/1110613/fdinfo/1 /proc/1110613/fdinfo/2 /proc/1110613/fdinfo/9 /proc/1110616/fdinfo/0 /proc/1110616/fdinfo/1 /proc/1110616/fdinfo/2 /proc/1110617/fdinfo/0 /proc/1110617/fdinfo/1 /proc/1110617/fdinfo/2 /proc/1110617/fdinfo/255 /proc/1110618/fdinfo/0 /proc/1110618/fdinfo/1 /proc/1110618/fdinfo/2 /proc/1110622/fdinfo/0 /proc/1110622/fdinfo/1 /proc/1110622/fdinfo/10 /proc/1110622/fdinfo/2 /proc/1110625/fdinfo/0 /proc/1110625/fdinfo/1 /proc/1110625/fdinfo/2 /proc/1110628/fdinfo/0 /proc/1110628/fdinfo/1 /proc/1110628/fdinfo/2 /proc/1110628/fdinfo/3 /proc/1110630/fdinfo/0 /proc/1110630/fdinfo/1 /proc/1110630/fdinfo/2 /proc/1110630/fdinfo/255 /proc/1110630/fdinfo/3 /proc/1110631/fdinfo/0 /proc/1110631/fdinfo/1 /proc/1110631/fdinfo/2 /proc/1110631/fdinfo/255 /proc/1110631/fdinfo/3 /proc/1110634/fdinfo/0 /proc/1110634/fdinfo/1 /proc/1110634/fdinfo/2 /proc/1110637/fdinfo/0 /proc/1110637/fdinfo/1 /proc/1110637/fdinfo/2 /proc/1110637/fdinfo/3 /proc/1110639/fdinfo/0 /proc/1110639/fdinfo/1 /proc/1110639/fdinfo/2 /proc/1110639/fdinfo/255 /proc/1110641/fdinfo/0 /proc/1110641/fdinfo/1 /proc/1110641/fdinfo/2 /proc/1110641/fdinfo/255 /proc/1110642/fdinfo/0 /proc/1110642/fdinfo/1 /proc/1110642/fdinfo/2 /proc/1110643/fdinfo/0 /proc/1110643/fdinfo/1 /proc/1110643/fdinfo/2 /proc/1110643/fdinfo/7 /proc/1110643/fdinfo/9 /proc/1110644/fdinfo/0 /proc/1110644/fdinfo/1 /proc/1110644/fdinfo/2 /proc/1110652/fdinfo/0 /proc/1110652/fdinfo/1 /proc/1110652/fdinfo/2 /proc/1110654/fdinfo/0 /proc/1110654/fdinfo/1 /proc/1110654/fdinfo/2 /proc/1110654/fdinfo/9 /proc/1110655/fdinfo/0 /proc/1110655/fdinfo/1 /proc/1110655/fdinfo/2 /proc/1110655/fdinfo/255 /proc/1110655/fdinfo/3 /proc/1110656/fdinfo/0 /proc/1110656/fdinfo/1 /proc/1110656/fdinfo/2 /proc/1110661/fdinfo/0 /proc/1110661/fdinfo/1 /proc/1110661/fdinfo/10 /proc/1110661/fdinfo/2 /proc/1110663/fdinfo/0 /proc/1110663/fdinfo/1 /proc/1110663/fdinfo/2 /proc/1110664/fdinfo/0 /proc/1110664/fdinfo/1 /proc/1110664/fdinfo/10 /proc/1110664/fdinfo/2 /proc/1110664/fdinfo/63 /proc/1110665/fdinfo/0 /proc/1110665/fdinfo/1 /proc/1110665/fdinfo/2 /proc/1110666/fdinfo/0 /proc/1110666/fdinfo/1 /proc/1110666/fdinfo/2 /proc/1110667/fdinfo/0 /proc/1110667/fdinfo/1 /proc/1110667/fdinfo/2 /proc/1110667/fdinfo/255 /proc/1110667/fdinfo/3 /proc/1110668/fdinfo/0 /proc/1110668/fdinfo/1 /proc/1110668/fdinfo/2 /proc/1110673/fdinfo/0 /proc/1110673/fdinfo/1 /proc/1110673/fdinfo/2 /proc/1110673/fdinfo/255 /proc/1110674/fdinfo/0 /proc/1110674/fdinfo/1 /proc/1110674/fdinfo/2 /proc/1110674/fdinfo/3 /proc/1110678/fdinfo/0 /proc/1110678/fdinfo/1 /proc/1110678/fdinfo/2 /proc/1110678/fdinfo/255 /proc/1110680/fdinfo/0 /proc/1110680/fdinfo/1 /proc/1110680/fdinfo/2 /proc/1110691/fdinfo/0 /proc/1110691/fdinfo/1 /proc/1110691/fdinfo/2 /proc/1110691/fdinfo/255 /proc/1110695/fdinfo/0 /proc/1110695/fdinfo/1 /proc/1110695/fdinfo/2 /proc/1110695/fdinfo/3 /proc/1110696/fdinfo/0 /proc/1110696/fdinfo/1 /proc/1110696/fdinfo/2 /proc/1110696/fdinfo/255 /proc/1110696/fdinfo/3 /proc/1110697/fdinfo/0 /proc/1110697/fdinfo/1 /proc/1110697/fdinfo/2 /proc/1110697/fdinfo/9 /proc/1110700/fdinfo/0 /proc/1110700/fdinfo/1 /proc/1110700/fdinfo/2 /proc/1110706/fdinfo/0 /proc/1110706/fdinfo/1 /proc/1110706/fdinfo/2 /proc/1110708/fdinfo/0 /proc/1110708/fdinfo/1 /proc/1110708/fdinfo/2 /proc/1110710/fdinfo/0 /proc/1110710/fdinfo/1 /proc/1110710/fdinfo/2 /proc/1110710/fdinfo/255 /proc/1110710/fdinfo/9 /proc/1110713/fdinfo/0 /proc/1110713/fdinfo/1 /proc/1110713/fdinfo/2 /proc/1110717/fdinfo/0 /proc/1110717/fdinfo/1 /proc/1110717/fdinfo/2 /proc/1110718/fdinfo/0 /proc/1110718/fdinfo/1 /proc/1110718/fdinfo/2 /proc/1110718/fdinfo/255 /proc/1110719/fdinfo/0 /proc/1110719/fdinfo/1 /proc/1110719/fdinfo/10 /proc/1110719/fdinfo/2 /proc/1110721/fdinfo/0 /proc/1110721/fdinfo/1 /proc/1110721/fdinfo/2 /proc/1110721/fdinfo/255 /proc/1110723/fdinfo/0 /proc/1110723/fdinfo/1 /proc/1110723/fdinfo/2 /proc/1110725/fdinfo/0 /proc/1110725/fdinfo/1 /proc/1110725/fdinfo/2 /proc/1110728/fdinfo/0 /proc/1110728/fdinfo/1 /proc/1110728/fdinfo/2 /proc/1110728/fdinfo/255 /proc/1110728/fdinfo/3 /proc/1110728/fdinfo/63 /proc/1110729/fdinfo/0 /proc/1110729/fdinfo/1 /proc/1110729/fdinfo/2 /proc/1110731/fdinfo/0 /proc/1110731/fdinfo/1 /proc/1110731/fdinfo/2 /proc/1110731/fdinfo/255 /proc/1110731/fdinfo/3 /proc/1110732/fdinfo/0 /proc/1110732/fdinfo/1 /proc/1110732/fdinfo/2 /proc/1110732/fdinfo/255 /proc/1110732/fdinfo/3 /proc/1110733/fdinfo/0 /proc/1110733/fdinfo/1 /proc/1110733/fdinfo/2 /proc/1110734/fdinfo/0 /proc/1110734/fdinfo/1 /proc/1110734/fdinfo/2 /proc/1110734/fdinfo/255 /proc/1110734/fdinfo/3 /proc/1110735/fdinfo/0 /proc/1110735/fdinfo/1 /proc/1110735/fdinfo/2 /proc/1110735/fdinfo/255 /proc/1110735/fdinfo/3 /proc/1110744/fdinfo/0 /proc/1110744/fdinfo/1 /proc/1110744/fdinfo/2 /proc/1110745/fdinfo/0 /proc/1110745/fdinfo/1 /proc/1110745/fdinfo/2 /proc/1110746/fdinfo/0 /proc/1110746/fdinfo/1 /proc/1110746/fdinfo/2 /proc/1110748/fdinfo/0 /proc/1110748/fdinfo/1 /proc/1110748/fdinfo/2 /proc/1110752/fdinfo/0 /proc/1110752/fdinfo/1 /proc/1110752/fdinfo/2 /proc/1110757/fdinfo/0 /proc/1110757/fdinfo/1 /proc/1110757/fdinfo/2 /proc/1110757/fdinfo/255 /proc/1110758/fdinfo/0 /proc/1110758/fdinfo/1 /proc/1110758/fdinfo/2 /proc/1110760/fdinfo/0 /proc/1110760/fdinfo/1 /proc/1110760/fdinfo/2 /proc/1110760/fdinfo/255 /proc/1110760/fdinfo/3 /proc/1110760/fdinfo/9 /proc/1110762/fdinfo/0 /proc/1110762/fdinfo/1 /proc/1110762/fdinfo/2 /proc/1110764/fdinfo/0 /proc/1110764/fdinfo/1 /proc/1110764/fdinfo/2 /proc/1110764/fdinfo/3 /proc/1110766/fdinfo/0 /proc/1110766/fdinfo/1 /proc/1110766/fdinfo/2 /proc/1110770/fdinfo/0 /proc/1110770/fdinfo/1 /proc/1110770/fdinfo/2 /proc/1110772/fdinfo/0 /proc/1110772/fdinfo/1 /proc/1110772/fdinfo/2 /proc/1110774/fdinfo/0 /proc/1110774/fdinfo/1 /proc/1110774/fdinfo/2 /proc/1110775/fdinfo/0 /proc/1110775/fdinfo/1 /proc/1110775/fdinfo/2 /proc/1110775/fdinfo/255 /proc/1110777/fdinfo/0 /proc/1110777/fdinfo/1 /proc/1110777/fdinfo/2 /proc/1110779/fdinfo/0 /proc/1110779/fdinfo/1 /proc/1110779/fdinfo/2 /proc/1110779/fdinfo/3 /proc/1110780/fdinfo/0 /proc/1110780/fdinfo/1 /proc/1110780/fdinfo/2 /proc/1110781/fdinfo/0 /proc/1110781/fdinfo/1 /proc/1110781/fdinfo/2 /proc/1110781/fdinfo/255 /proc/1110786/fdinfo/0 /proc/1110786/fdinfo/1 /proc/1110786/fdinfo/2 /proc/1110791/fdinfo/0 /proc/1110791/fdinfo/1 /proc/1110791/fdinfo/2 /proc/1110791/fdinfo/255 /proc/1110791/fdinfo/3 /proc/1110792/fdinfo/0 /proc/1110792/fdinfo/1 /proc/1110792/fdinfo/2 /proc/1110793/fdinfo/0 /proc/1110793/fdinfo/1 /proc/1110793/fdinfo/2 /proc/1110793/fdinfo/255 /proc/1110793/fdinfo/3 /proc/1110794/fdinfo/0 /proc/1110794/fdinfo/1 /proc/1110794/fdinfo/2 /proc/1110794/fdinfo/9 /proc/1110795/fdinfo/0 /proc/1110795/fdinfo/1 /proc/1110795/fdinfo/10 /proc/1110795/fdinfo/11 /proc/1110795/fdinfo/12 /proc/1110795/fdinfo/2 /proc/1110796/fdinfo/0 /proc/1110796/fdinfo/1 /proc/1110796/fdinfo/2 /proc/1110798/fdinfo/0 /proc/1110798/fdinfo/1 /proc/1110798/fdinfo/2 /proc/1110802/fdinfo/0 /proc/1110802/fdinfo/1 /proc/1110802/fdinfo/2 /proc/1110802/fdinfo/255 /proc/1110802/fdinfo/3 /proc/1110804/fdinfo/0 /proc/1110804/fdinfo/1 /proc/1110804/fdinfo/2 /proc/1110804/fdinfo/255 /proc/1110804/fdinfo/3 /proc/1110807/fdinfo/0 /proc/1110807/fdinfo/1 /proc/1110807/fdinfo/2 /proc/1110807/fdinfo/255 /proc/1110808/fdinfo/0 /proc/1110808/fdinfo/1 /proc/1110808/fdinfo/2 /proc/1110809/fdinfo/0 /proc/1110809/fdinfo/1 /proc/1110809/fdinfo/2 /proc/1110810/fdinfo/0 /proc/1110810/fdinfo/1 /proc/1110810/fdinfo/2 /proc/1110812/fdinfo/0 /proc/1110812/fdinfo/1 /proc/1110812/fdinfo/2 /proc/1110812/fdinfo/3 /proc/1110818/fdinfo/0 /proc/1110818/fdinfo/1 /proc/1110818/fdinfo/2 /proc/1110818/fdinfo/3 /proc/1110820/fdinfo/0 /proc/1110820/fdinfo/1 /proc/1110820/fdinfo/2 /proc/1110820/fdinfo/3 /proc/1110821/fdinfo/0 /proc/1110821/fdinfo/1 /proc/1110821/fdinfo/2 /proc/1110822/fdinfo/0 /proc/1110822/fdinfo/1 /proc/1110822/fdinfo/2 /proc/1110823/fdinfo/0 /proc/1110823/fdinfo/1 /proc/1110823/fdinfo/2 /proc/1110823/fdinfo/255 /proc/1110823/fdinfo/3 /proc/1110823/fdinfo/9 /proc/1110824/fdinfo/0 /proc/1110824/fdinfo/1 /proc/1110824/fdinfo/2 /proc/1110829/fdinfo/0 /proc/1110829/fdinfo/1 /proc/1110829/fdinfo/2 /proc/1110829/fdinfo/255 /proc/1110829/fdinfo/3 /proc/1110831/fdinfo/0 /proc/1110831/fdinfo/1 /proc/1110831/fdinfo/10 /proc/1110831/fdinfo/11 /proc/1110831/fdinfo/12 /proc/1110831/fdinfo/2 /proc/1110831/fdinfo/62 /proc/1110831/fdinfo/63 /proc/1110832/fdinfo/0 /proc/1110832/fdinfo/1 /proc/1110832/fdinfo/2 /proc/1110838/fdinfo/0 /proc/1110838/fdinfo/1 /proc/1110838/fdinfo/2 /proc/1110840/fdinfo/0 /proc/1110840/fdinfo/1 /proc/1110840/fdinfo/2 /proc/1110841/fdinfo/0 /proc/1110841/fdinfo/1 /proc/1110841/fdinfo/2 /proc/1110843/fdinfo/0 /proc/1110843/fdinfo/1 /proc/1110843/fdinfo/2 /proc/1110845/fdinfo/0 /proc/1110845/fdinfo/1 /proc/1110845/fdinfo/2 /proc/1110847/fdinfo/0 /proc/1110847/fdinfo/1 /proc/1110847/fdinfo/2 /proc/1110853/fdinfo/0 /proc/1110853/fdinfo/1 /proc/1110853/fdinfo/10 /proc/1110853/fdinfo/2 /proc/1110853/fdinfo/255 /proc/1110853/fdinfo/63 /proc/1110855/fdinfo/0 /proc/1110855/fdinfo/1 /proc/1110855/fdinfo/2 /proc/1110855/fdinfo/255 /proc/1110858/fdinfo/0 /proc/1110858/fdinfo/1 /proc/1110858/fdinfo/2 /proc/1110858/fdinfo/255 /proc/1110858/fdinfo/3 /proc/1110859/fdinfo/0 /proc/1110859/fdinfo/1 /proc/1110859/fdinfo/2 /proc/1110859/fdinfo/255 /proc/1110860/fdinfo/0 /proc/1110860/fdinfo/1 /proc/1110860/fdinfo/2 /proc/1110860/fdinfo/3 /proc/1110862/fdinfo/0 /proc/1110862/fdinfo/1 /proc/1110862/fdinfo/2 /proc/1110863/fdinfo/0 /proc/1110863/fdinfo/1 /proc/1110863/fdinfo/2 /proc/1110867/fdinfo/0 /proc/1110867/fdinfo/1 /proc/1110867/fdinfo/2 /proc/1110867/fdinfo/255 /proc/1110867/fdinfo/3 /proc/1110871/fdinfo/0 /proc/1110871/fdinfo/1 /proc/1110871/fdinfo/2 /proc/1110872/fdinfo/0 /proc/1110872/fdinfo/1 /proc/1110872/fdinfo/2 /proc/1110872/fdinfo/255 /proc/1110874/fdinfo/0 /proc/1110874/fdinfo/1 /proc/1110874/fdinfo/2 /proc/1110874/fdinfo/9 /proc/1110875/fdinfo/0 /proc/1110875/fdinfo/1 /proc/1110875/fdinfo/2 /proc/1110878/fdinfo/0 /proc/1110878/fdinfo/1 /proc/1110878/fdinfo/2 /proc/1110879/fdinfo/0 /proc/1110879/fdinfo/1 /proc/1110879/fdinfo/10 /proc/1110879/fdinfo/2 /proc/1110879/fdinfo/3 /proc/1110881/fdinfo/0 /proc/1110881/fdinfo/1 /proc/1110881/fdinfo/2 /proc/1110881/fdinfo/255 /proc/1110881/fdinfo/3 /proc/1110881/fdinfo/9 /proc/1110883/fdinfo/0 /proc/1110883/fdinfo/1 /proc/1110883/fdinfo/2 /proc/1110887/fdinfo/0 /proc/1110887/fdinfo/1 /proc/1110887/fdinfo/2 /proc/1110889/fdinfo/0 /proc/1110889/fdinfo/1 /proc/1110889/fdinfo/10 /proc/1110889/fdinfo/11 /proc/1110889/fdinfo/2 /proc/1110889/fdinfo/3 /proc/1110890/fdinfo/0 /proc/1110890/fdinfo/1 /proc/1110890/fdinfo/2 /proc/1110890/fdinfo/3 /proc/1110891/fdinfo/0 /proc/1110891/fdinfo/1 /proc/1110891/fdinfo/2 /proc/1110891/fdinfo/3 /proc/1110892/fdinfo/0 /proc/1110892/fdinfo/1 /proc/1110892/fdinfo/10 /proc/1110892/fdinfo/2 /proc/1110892/fdinfo/255 /proc/1110894/fdinfo/0 /proc/1110894/fdinfo/1 /proc/1110894/fdinfo/2 /proc/1110894/fdinfo/255 /proc/1110894/fdinfo/3 /proc/1110896/fdinfo/0 /proc/1110896/fdinfo/1 /proc/1110896/fdinfo/2 /proc/1110898/fdinfo/0 /proc/1110898/fdinfo/1 /proc/1110898/fdinfo/2 /proc/1110899/fdinfo/0 /proc/1110899/fdinfo/1 /proc/1110899/fdinfo/2 /proc/1110900/fdinfo/0 /proc/1110900/fdinfo/1 /proc/1110900/fdinfo/2 /proc/1110905/fdinfo/0 /proc/1110905/fdinfo/1 /proc/1110905/fdinfo/2 /proc/1110907/fdinfo/0 /proc/1110907/fdinfo/1 /proc/1110907/fdinfo/2 /proc/1110911/fdinfo/0 /proc/1110911/fdinfo/1 /proc/1110911/fdinfo/2 /proc/1110911/fdinfo/255 /proc/1110912/fdinfo/0 /proc/1110912/fdinfo/1 /proc/1110912/fdinfo/2 /proc/1110912/fdinfo/255 /proc/1110913/fdinfo/0 /proc/1110913/fdinfo/1 /proc/1110913/fdinfo/2 /proc/1110913/fdinfo/62 /proc/1110913/fdinfo/63 /proc/1110922/fdinfo/0 /proc/1110922/fdinfo/1 /proc/1110922/fdinfo/2 /proc/1110922/fdinfo/255 /proc/1110922/fdinfo/3 /proc/1110923/fdinfo/0 /proc/1110923/fdinfo/1 /proc/1110923/fdinfo/2 /proc/1110926/fdinfo/0 /proc/1110926/fdinfo/1 /proc/1110926/fdinfo/2 /proc/1110926/fdinfo/3 /proc/1110926/fdinfo/5 /proc/1110931/fdinfo/0 /proc/1110931/fdinfo/1 /proc/1110931/fdinfo/2 /proc/1110932/fdinfo/0 /proc/1110932/fdinfo/1 /proc/1110932/fdinfo/2 /proc/1110932/fdinfo/255 /proc/1110932/fdinfo/9 /proc/1110939/fdinfo/0 /proc/1110939/fdinfo/1 /proc/1110939/fdinfo/2 /proc/1110939/fdinfo/255 /proc/1110939/fdinfo/3 /proc/1110941/fdinfo/0 /proc/1110941/fdinfo/1 /proc/1110941/fdinfo/2 /proc/1110942/fdinfo/0 /proc/1110942/fdinfo/1 /proc/1110942/fdinfo/2 /proc/1110942/fdinfo/255 /proc/1110945/fdinfo/0 /proc/1110945/fdinfo/1 /proc/1110945/fdinfo/2 /proc/1110945/fdinfo/255 /proc/1110947/fdinfo/0 /proc/1110947/fdinfo/1 /proc/1110947/fdinfo/2 /proc/1110947/fdinfo/255 /proc/1110947/fdinfo/3 /proc/1110949/fdinfo/0 /proc/1110949/fdinfo/1 /proc/1110949/fdinfo/2 /proc/1110950/fdinfo/0 /proc/1110950/fdinfo/1 /proc/1110950/fdinfo/2 /proc/1110950/fdinfo/255 /proc/1110950/fdinfo/3 /proc/1110952/fdinfo/0 /proc/1110952/fdinfo/1 /proc/1110952/fdinfo/2 /proc/1110952/fdinfo/3 /proc/1110955/fdinfo/0 /proc/1110955/fdinfo/1 /proc/1110955/fdinfo/2 /proc/1110957/fdinfo/0 /proc/1110957/fdinfo/1 /proc/1110957/fdinfo/2 /proc/1110957/fdinfo/255 /proc/1110957/fdinfo/3 /proc/1110958/fdinfo/0 /proc/1110958/fdinfo/1 /proc/1110958/fdinfo/2 /proc/1110963/fdinfo/0 /proc/1110963/fdinfo/1 /proc/1110963/fdinfo/2 /proc/1110976/fdinfo/0 /proc/1110976/fdinfo/1 /proc/1110976/fdinfo/2 /proc/1110976/fdinfo/9 /proc/1110977/fdinfo/0 /proc/1110977/fdinfo/1 /proc/1110977/fdinfo/2 /proc/1110977/fdinfo/255 /proc/1110979/fdinfo/0 /proc/1110979/fdinfo/1 /proc/1110979/fdinfo/2 /proc/1110982/fdinfo/0 /proc/1110982/fdinfo/1 /proc/1110982/fdinfo/2 /proc/1110984/fdinfo/0 /proc/1110984/fdinfo/1 /proc/1110984/fdinfo/10 /proc/1110984/fdinfo/2 /proc/1110984/fdinfo/255 /proc/1110985/fdinfo/0 /proc/1110985/fdinfo/1 /proc/1110985/fdinfo/2 /proc/1110985/fdinfo/3 /proc/1110988/fdinfo/0 /proc/1110988/fdinfo/1 /proc/1110988/fdinfo/2 /proc/1110988/fdinfo/255 /proc/1110988/fdinfo/3 /proc/1110989/fdinfo/0 /proc/1110989/fdinfo/1 /proc/1110989/fdinfo/2 /proc/1110990/fdinfo/0 /proc/1110990/fdinfo/1 /proc/1110990/fdinfo/2 /proc/1110990/fdinfo/9 /proc/1110994/fdinfo/0 /proc/1110994/fdinfo/1 /proc/1110994/fdinfo/2 /proc/1111000/fdinfo/0 /proc/1111000/fdinfo/1 /proc/1111000/fdinfo/2 /proc/1111003/fdinfo/0 /proc/1111003/fdinfo/1 /proc/1111003/fdinfo/2 /proc/1111003/fdinfo/255 /proc/1111003/fdinfo/3 /proc/1111004/fdinfo/0 /proc/1111004/fdinfo/1 /proc/1111004/fdinfo/2 /proc/1111007/fdinfo/0 /proc/1111007/fdinfo/1 /proc/1111007/fdinfo/2 /proc/1111011/fdinfo/0 /proc/1111011/fdinfo/1 /proc/1111011/fdinfo/2 /proc/1111011/fdinfo/255 /proc/1111012/fdinfo/0 /proc/1111012/fdinfo/1 /proc/1111012/fdinfo/2 /proc/1111016/fdinfo/0 /proc/1111016/fdinfo/1 /proc/1111016/fdinfo/10 /proc/1111016/fdinfo/2 /proc/1111016/fdinfo/3 /proc/1111016/fdinfo/4 /proc/1111018/fdinfo/0 /proc/1111018/fdinfo/1 /proc/1111018/fdinfo/2 /proc/1111019/fdinfo/0 /proc/1111019/fdinfo/1 /proc/1111019/fdinfo/2 /proc/1111020/fdinfo/0 /proc/1111020/fdinfo/1 /proc/1111020/fdinfo/2 /proc/1111020/fdinfo/255 /proc/1111021/fdinfo/0 /proc/1111021/fdinfo/1 /proc/1111021/fdinfo/2 /proc/1111021/fdinfo/255 /proc/1111023/fdinfo/0 /proc/1111023/fdinfo/1 /proc/1111023/fdinfo/2 /proc/1111023/fdinfo/63 /proc/1111025/fdinfo/0 /proc/1111025/fdinfo/1 /proc/1111025/fdinfo/2 /proc/1111025/fdinfo/3 /proc/1111028/fdinfo/0 /proc/1111028/fdinfo/1 /proc/1111028/fdinfo/2 /proc/1111028/fdinfo/3 /proc/1111031/fdinfo/0 /proc/1111031/fdinfo/1 /proc/1111031/fdinfo/2 /proc/1111031/fdinfo/255 /proc/1111031/fdinfo/3 /proc/1111032/fdinfo/0 /proc/1111032/fdinfo/1 /proc/1111032/fdinfo/2 /proc/1111033/fdinfo/0 /proc/1111033/fdinfo/1 /proc/1111033/fdinfo/10 /proc/1111033/fdinfo/2 /proc/1111033/fdinfo/63 /proc/1111036/fdinfo/0 /proc/1111036/fdinfo/1 /proc/1111036/fdinfo/2 /proc/1111037/fdinfo/0 /proc/1111037/fdinfo/1 /proc/1111037/fdinfo/10 /proc/1111037/fdinfo/11 /proc/1111037/fdinfo/2 /proc/1111037/fdinfo/255 /proc/1111038/fdinfo/0 /proc/1111038/fdinfo/1 /proc/1111038/fdinfo/2 /proc/1111039/fdinfo/0 /proc/1111039/fdinfo/1 /proc/1111039/fdinfo/2 /proc/1111042/fdinfo/0 /proc/1111042/fdinfo/1 /proc/1111042/fdinfo/2 /proc/1111042/fdinfo/255 /proc/1111042/fdinfo/3 /proc/1111044/fdinfo/0 /proc/1111044/fdinfo/1 /proc/1111044/fdinfo/2 /proc/1111044/fdinfo/9 /proc/1111047/fdinfo/0 /proc/1111047/fdinfo/1 /proc/1111047/fdinfo/2 /proc/1111047/fdinfo/3 /proc/1111048/fdinfo/0 /proc/1111048/fdinfo/1 /proc/1111048/fdinfo/2 /proc/1111049/fdinfo/0 /proc/1111049/fdinfo/1 /proc/1111049/fdinfo/2 /proc/1111052/fdinfo/0 /proc/1111052/fdinfo/1 /proc/1111052/fdinfo/10 /proc/1111052/fdinfo/11 /proc/1111052/fdinfo/2 /proc/1111052/fdinfo/255 /proc/1111052/fdinfo/3 /proc/1111052/fdinfo/9 /proc/1111053/fdinfo/0 /proc/1111053/fdinfo/1 /proc/1111053/fdinfo/10 /proc/1111053/fdinfo/2 /proc/1111056/fdinfo/0 /proc/1111056/fdinfo/1 /proc/1111056/fdinfo/2 /proc/1111060/fdinfo/0 /proc/1111060/fdinfo/1 /proc/1111060/fdinfo/2 /proc/1111060/fdinfo/255 /proc/1111060/fdinfo/3 /proc/1111061/fdinfo/0 /proc/1111061/fdinfo/1 /proc/1111061/fdinfo/2 /proc/1111063/fdinfo/0 /proc/1111063/fdinfo/1 /proc/1111063/fdinfo/10 /proc/1111063/fdinfo/2 /proc/1111063/fdinfo/3 /proc/1111064/fdinfo/0 /proc/1111064/fdinfo/1 /proc/1111064/fdinfo/2 /proc/1111067/fdinfo/0 /proc/1111067/fdinfo/1 /proc/1111067/fdinfo/10 /proc/1111067/fdinfo/11 /proc/1111067/fdinfo/12 /proc/1111067/fdinfo/2 /proc/1111067/fdinfo/255 /proc/1111067/fdinfo/3 /proc/1111067/fdinfo/62 /proc/1111067/fdinfo/63 /proc/1111068/fdinfo/0 /proc/1111068/fdinfo/1 /proc/1111068/fdinfo/2 /proc/1111068/fdinfo/3 /proc/1111072/fdinfo/0 /proc/1111072/fdinfo/1 /proc/1111072/fdinfo/10 /proc/1111072/fdinfo/11 /proc/1111072/fdinfo/12 /proc/1111072/fdinfo/13 /proc/1111072/fdinfo/14 /proc/1111072/fdinfo/15 /proc/1111072/fdinfo/16 /proc/1111072/fdinfo/17 /proc/1111072/fdinfo/18 /proc/1111072/fdinfo/19 /proc/1111072/fdinfo/2 /proc/1111072/fdinfo/20 /proc/1111072/fdinfo/21 /proc/1111072/fdinfo/22 /proc/1111072/fdinfo/23 /proc/1111072/fdinfo/24 /proc/1111072/fdinfo/25 /proc/1111072/fdinfo/26 /proc/1111072/fdinfo/27 /proc/1111072/fdinfo/28 /proc/1111072/fdinfo/29 /proc/1111072/fdinfo/30 /proc/1111072/fdinfo/31 /proc/1111072/fdinfo/32 /proc/1111072/fdinfo/33 /proc/1111072/fdinfo/34 /proc/1111072/fdinfo/35 /proc/1111072/fdinfo/36 /proc/1111072/fdinfo/37 /proc/1111072/fdinfo/38 /proc/1111072/fdinfo/39 /proc/1111072/fdinfo/40 /proc/1111072/fdinfo/41 /proc/1111072/fdinfo/42 /proc/1111072/fdinfo/43 /proc/1111072/fdinfo/44 /proc/1111072/fdinfo/45 /proc/1111072/fdinfo/46 /proc/1111072/fdinfo/47 /proc/1111072/fdinfo/48 /proc/1111072/fdinfo/49 /proc/1111072/fdinfo/5 /proc/1111072/fdinfo/50 /proc/1111072/fdinfo/51 /proc/1111072/fdinfo/52 /proc/1111072/fdinfo/53 /proc/1111072/fdinfo/54 /proc/1111072/fdinfo/55 /proc/1111072/fdinfo/56 /proc/1111072/fdinfo/57 /proc/1111072/fdinfo/58 /proc/1111072/fdinfo/59 /proc/1111072/fdinfo/6 /proc/1111072/fdinfo/60 /proc/1111072/fdinfo/61 /proc/1111072/fdinfo/62 /proc/1111072/fdinfo/63 /proc/1111072/fdinfo/64 /proc/1111072/fdinfo/65 /proc/1111072/fdinfo/66 /proc/1111072/fdinfo/67 /proc/1111072/fdinfo/68 /proc/1111072/fdinfo/69 /proc/1111072/fdinfo/7 /proc/1111072/fdinfo/70 /proc/1111072/fdinfo/71 /proc/1111072/fdinfo/72 /proc/1111072/fdinfo/73 /proc/1111072/fdinfo/74 /proc/1111072/fdinfo/75 /proc/1111072/fdinfo/76 /proc/1111072/fdinfo/77 /proc/1111072/fdinfo/78 /proc/1111072/fdinfo/79 /proc/1111072/fdinfo/8 /proc/1111072/fdinfo/80 /proc/1111072/fdinfo/81 /proc/1111072/fdinfo/82 /proc/1111072/fdinfo/83 /proc/1111072/fdinfo/84 /proc/1111072/fdinfo/85 /proc/1111072/fdinfo/86 /proc/1111072/fdinfo/87 /proc/1111072/fdinfo/88 /proc/1111072/fdinfo/89 /proc/1111072/fdinfo/9 /proc/1111072/fdinfo/90 /proc/1111072/fdinfo/91 /proc/1111072/fdinfo/92 /proc/1111072/fdinfo/93 /proc/1111072/fdinfo/94 /proc/1111072/fdinfo/95 /proc/1111072/fdinfo/96 /proc/1111072/fdinfo/97 /proc/1111072/fdinfo/98 /proc/1111072/fdinfo/99 /proc/1111073/fdinfo/0 /proc/1111073/fdinfo/1 /proc/1111073/fdinfo/2 /proc/1111073/fdinfo/3 /proc/1111073/fdinfo/5 /proc/1111075/fdinfo/0 /proc/1111075/fdinfo/1 /proc/1111075/fdinfo/2 /proc/1111077/fdinfo/0 /proc/1111077/fdinfo/1 /proc/1111077/fdinfo/2 /proc/1111078/fdinfo/0 /proc/1111078/fdinfo/1 /proc/1111078/fdinfo/10 /proc/1111078/fdinfo/11 /proc/1111078/fdinfo/2 /proc/1111078/fdinfo/3 /proc/1111078/fdinfo/63 /proc/1111081/fdinfo/0 /proc/1111081/fdinfo/1 /proc/1111081/fdinfo/2 /proc/1111082/fdinfo/0 /proc/1111082/fdinfo/1 /proc/1111082/fdinfo/10 /proc/1111082/fdinfo/2 /proc/1111083/fdinfo/0 /proc/1111083/fdinfo/1 /proc/1111083/fdinfo/2 /proc/1111084/fdinfo/0 /proc/1111084/fdinfo/1 /proc/1111084/fdinfo/2 /proc/1111084/fdinfo/255 /proc/1111084/fdinfo/3 /proc/1111086/fdinfo/0 /proc/1111086/fdinfo/1 /proc/1111086/fdinfo/2 /proc/1111087/fdinfo/0 /proc/1111087/fdinfo/1 /proc/1111087/fdinfo/2 /proc/1111087/fdinfo/255 /proc/1111088/fdinfo/0 /proc/1111088/fdinfo/1 /proc/1111088/fdinfo/2 /proc/1111088/fdinfo/3 /proc/1111088/fdinfo/4 /proc/1111088/fdinfo/5 /proc/1111088/fdinfo/6 /proc/1111093/fdinfo/0 /proc/1111093/fdinfo/1 /proc/1111093/fdinfo/2 /proc/1111093/fdinfo/255 /proc/1111093/fdinfo/3 /proc/1111096/fdinfo/0 /proc/1111096/fdinfo/1 /proc/1111096/fdinfo/2 /proc/1111096/fdinfo/255 /proc/1111097/fdinfo/0 /proc/1111097/fdinfo/1 /proc/1111097/fdinfo/2 /proc/1111100/fdinfo/0 /proc/1111100/fdinfo/1 /proc/1111100/fdinfo/2 /proc/1111100/fdinfo/3 /proc/1111101/fdinfo/0 /proc/1111101/fdinfo/1 /proc/1111101/fdinfo/2 /proc/1111103/fdinfo/0 /proc/1111103/fdinfo/1 /proc/1111103/fdinfo/2 /proc/1111104/fdinfo/0 /proc/1111104/fdinfo/1 /proc/1111104/fdinfo/2 /proc/1111108/fdinfo/0 /proc/1111108/fdinfo/1 /proc/1111108/fdinfo/2 /proc/1111108/fdinfo/63 /proc/1111109/fdinfo/0 /proc/1111109/fdinfo/1 /proc/1111109/fdinfo/10 /proc/1111109/fdinfo/11 /proc/1111109/fdinfo/12 /proc/1111109/fdinfo/13 /proc/1111109/fdinfo/14 /proc/1111109/fdinfo/15 /proc/1111109/fdinfo/16 /proc/1111109/fdinfo/17 /proc/1111109/fdinfo/18 /proc/1111109/fdinfo/19 /proc/1111109/fdinfo/2 /proc/1111109/fdinfo/20 /proc/1111109/fdinfo/21 /proc/1111109/fdinfo/22 /proc/1111109/fdinfo/23 /proc/1111109/fdinfo/24 /proc/1111109/fdinfo/25 /proc/1111109/fdinfo/26 /proc/1111109/fdinfo/27 /proc/1111109/fdinfo/28 /proc/1111109/fdinfo/29 /proc/1111109/fdinfo/3 /proc/1111109/fdinfo/30 /proc/1111109/fdinfo/31 /proc/1111109/fdinfo/32 /proc/1111109/fdinfo/33 /proc/1111109/fdinfo/34 /proc/1111109/fdinfo/35 /proc/1111109/fdinfo/36 /proc/1111109/fdinfo/37 /proc/1111109/fdinfo/4 /proc/1111109/fdinfo/5 /proc/1111109/fdinfo/6 /proc/1111109/fdinfo/7 /proc/1111109/fdinfo/8 /proc/1111109/fdinfo/9 /proc/1111110/fdinfo/0 /proc/1111110/fdinfo/1 /proc/1111110/fdinfo/2 /proc/1111110/fdinfo/255 /proc/1111110/fdinfo/3 /proc/1111112/fdinfo/0 /proc/1111112/fdinfo/1 /proc/1111112/fdinfo/10 /proc/1111112/fdinfo/2 /proc/1111112/fdinfo/255 /proc/1111112/fdinfo/3 /proc/1111112/fdinfo/63 /proc/1111117/fdinfo/0 /proc/1111117/fdinfo/1 /proc/1111117/fdinfo/2 /proc/1111118/fdinfo/0 /proc/1111118/fdinfo/1 /proc/1111118/fdinfo/2 /proc/1111118/fdinfo/9 /proc/1111119/fdinfo/0 /proc/1111119/fdinfo/1 /proc/1111119/fdinfo/2 /proc/1111120/fdinfo/0 /proc/1111120/fdinfo/1 /proc/1111120/fdinfo/2 /proc/1111123/fdinfo/0 /proc/1111123/fdinfo/1 /proc/1111123/fdinfo/2 /proc/1111123/fdinfo/9 /proc/1111124/fdinfo/0 /proc/1111124/fdinfo/1 /proc/1111124/fdinfo/2 /proc/1111129/fdinfo/0 /proc/1111129/fdinfo/1 /proc/1111129/fdinfo/2 /proc/1111130/fdinfo/0 /proc/1111130/fdinfo/1 /proc/1111130/fdinfo/2 /proc/1111137/fdinfo/0 /proc/1111137/fdinfo/1 /proc/1111137/fdinfo/2 /proc/1111138/fdinfo/0 /proc/1111138/fdinfo/1 /proc/1111138/fdinfo/2 /proc/1111138/fdinfo/255 /proc/1111142/fdinfo/0 /proc/1111142/fdinfo/1 /proc/1111142/fdinfo/2 /proc/1111142/fdinfo/255 /proc/1111143/fdinfo/0 /proc/1111143/fdinfo/1 /proc/1111143/fdinfo/2 /proc/1111143/fdinfo/255 /proc/1111143/fdinfo/3 /proc/1111153/fdinfo/0 /proc/1111153/fdinfo/1 /proc/1111153/fdinfo/2 /proc/1111153/fdinfo/3 /proc/1111157/fdinfo/0 /proc/1111157/fdinfo/1 /proc/1111157/fdinfo/2 /proc/1111161/fdinfo/0 /proc/1111161/fdinfo/1 /proc/1111161/fdinfo/2 /proc/1111162/fdinfo/0 /proc/1111162/fdinfo/1 /proc/1111162/fdinfo/2 /proc/1111168/fdinfo/0 /proc/1111168/fdinfo/1 /proc/1111168/fdinfo/2 /proc/1111169/fdinfo/0 /proc/1111169/fdinfo/1 /proc/1111169/fdinfo/2 /proc/1111173/fdinfo/0 /proc/1111173/fdinfo/1 /proc/1111173/fdinfo/2 /proc/1111173/fdinfo/255 /proc/1111173/fdinfo/3 /proc/1111183/fdinfo/0 /proc/1111183/fdinfo/1 /proc/1111183/fdinfo/2 /proc/1111190/fdinfo/0 /proc/1111190/fdinfo/1 /proc/1111190/fdinfo/2 /proc/1111190/fdinfo/255 /proc/1111190/fdinfo/3 /proc/1111192/fdinfo/0 /proc/1111192/fdinfo/1 /proc/1111192/fdinfo/2 /proc/1111192/fdinfo/255 /proc/1111192/fdinfo/3 /proc/1111194/fdinfo/0 /proc/1111194/fdinfo/1 /proc/1111194/fdinfo/2 /proc/1111195/fdinfo/0 /proc/1111195/fdinfo/1 /proc/1111195/fdinfo/2 /proc/1111196/fdinfo/0 /proc/1111196/fdinfo/1 /proc/1111196/fdinfo/2 /proc/1111196/fdinfo/255 /proc/1111201/fdinfo/0 /proc/1111201/fdinfo/1 /proc/1111201/fdinfo/2 /proc/1111201/fdinfo/3 /proc/1111202/fdinfo/0 /proc/1111202/fdinfo/1 /proc/1111202/fdinfo/2 /proc/1111203/fdinfo/0 /proc/1111203/fdinfo/1 /proc/1111203/fdinfo/2 /proc/1111204/fdinfo/0 /proc/1111204/fdinfo/1 /proc/1111204/fdinfo/2 /proc/1111204/fdinfo/9 /proc/1111205/fdinfo/0 /proc/1111205/fdinfo/1 /proc/1111205/fdinfo/2 /proc/1111205/fdinfo/3 /proc/1111207/fdinfo/0 /proc/1111207/fdinfo/1 /proc/1111207/fdinfo/2 /proc/1111210/fdinfo/0 /proc/1111210/fdinfo/1 /proc/1111210/fdinfo/10 /proc/1111210/fdinfo/11 /proc/1111210/fdinfo/12 /proc/1111210/fdinfo/2 /proc/1111210/fdinfo/255 /proc/1111210/fdinfo/3 /proc/1111210/fdinfo/63 /proc/1111212/fdinfo/0 /proc/1111212/fdinfo/1 /proc/1111212/fdinfo/2 /proc/1111212/fdinfo/9 /proc/1111213/fdinfo/0 /proc/1111213/fdinfo/1 /proc/1111213/fdinfo/2 /proc/1111216/fdinfo/0 /proc/1111216/fdinfo/1 /proc/1111216/fdinfo/2 /proc/1111218/fdinfo/0 /proc/1111218/fdinfo/1 /proc/1111218/fdinfo/2 /proc/1111220/fdinfo/0 /proc/1111220/fdinfo/1 /proc/1111220/fdinfo/2 /proc/1111224/fdinfo/0 /proc/1111224/fdinfo/1 /proc/1111224/fdinfo/2 /proc/1111224/fdinfo/255 /proc/1111224/fdinfo/3 /proc/1111226/fdinfo/0 /proc/1111226/fdinfo/1 /proc/1111226/fdinfo/2 /proc/1111228/fdinfo/0 /proc/1111228/fdinfo/1 /proc/1111228/fdinfo/2 /proc/1111228/fdinfo/3 /proc/1111229/fdinfo/0 /proc/1111229/fdinfo/1 /proc/1111229/fdinfo/10 /proc/1111229/fdinfo/2 /proc/1111230/fdinfo/0 /proc/1111230/fdinfo/1 /proc/1111230/fdinfo/2 /proc/1111230/fdinfo/255 /proc/1111231/fdinfo/0 /proc/1111231/fdinfo/1 /proc/1111231/fdinfo/2 /proc/1111236/fdinfo/0 /proc/1111236/fdinfo/1 /proc/1111236/fdinfo/2 /proc/1111236/fdinfo/3 /proc/1111238/fdinfo/0 /proc/1111238/fdinfo/1 /proc/1111238/fdinfo/10 /proc/1111238/fdinfo/11 /proc/1111238/fdinfo/12 /proc/1111238/fdinfo/13 /proc/1111238/fdinfo/14 /proc/1111238/fdinfo/15 /proc/1111238/fdinfo/16 /proc/1111238/fdinfo/17 /proc/1111238/fdinfo/18 /proc/1111238/fdinfo/19 /proc/1111238/fdinfo/2 /proc/1111238/fdinfo/20 /proc/1111238/fdinfo/21 /proc/1111238/fdinfo/22 /proc/1111238/fdinfo/23 /proc/1111238/fdinfo/24 /proc/1111238/fdinfo/25 /proc/1111238/fdinfo/26 /proc/1111238/fdinfo/27 /proc/1111238/fdinfo/28 /proc/1111238/fdinfo/29 /proc/1111238/fdinfo/30 /proc/1111238/fdinfo/31 /proc/1111238/fdinfo/32 /proc/1111238/fdinfo/33 /proc/1111238/fdinfo/34 /proc/1111238/fdinfo/35 /proc/1111238/fdinfo/36 /proc/1111238/fdinfo/37 /proc/1111238/fdinfo/38 /proc/1111238/fdinfo/39 /proc/1111238/fdinfo/40 /proc/1111238/fdinfo/41 /proc/1111238/fdinfo/42 /proc/1111238/fdinfo/43 /proc/1111238/fdinfo/44 /proc/1111238/fdinfo/45 /proc/1111238/fdinfo/46 /proc/1111238/fdinfo/47 /proc/1111238/fdinfo/48 /proc/1111238/fdinfo/49 /proc/1111238/fdinfo/5 /proc/1111238/fdinfo/50 /proc/1111238/fdinfo/51 /proc/1111238/fdinfo/52 /proc/1111238/fdinfo/53 /proc/1111238/fdinfo/54 /proc/1111238/fdinfo/55 /proc/1111238/fdinfo/56 /proc/1111238/fdinfo/57 /proc/1111238/fdinfo/58 /proc/1111238/fdinfo/59 /proc/1111238/fdinfo/6 /proc/1111238/fdinfo/60 /proc/1111238/fdinfo/61 /proc/1111238/fdinfo/62 /proc/1111238/fdinfo/63 /proc/1111238/fdinfo/64 /proc/1111238/fdinfo/65 /proc/1111238/fdinfo/66 /proc/1111238/fdinfo/67 /proc/1111238/fdinfo/68 /proc/1111238/fdinfo/69 /proc/1111238/fdinfo/7 /proc/1111238/fdinfo/70 /proc/1111238/fdinfo/71 /proc/1111238/fdinfo/72 /proc/1111238/fdinfo/73 /proc/1111238/fdinfo/74 /proc/1111238/fdinfo/75 /proc/1111238/fdinfo/76 /proc/1111238/fdinfo/77 /proc/1111238/fdinfo/78 /proc/1111238/fdinfo/79 /proc/1111238/fdinfo/8 /proc/1111238/fdinfo/80 /proc/1111238/fdinfo/81 /proc/1111238/fdinfo/82 /proc/1111238/fdinfo/83 /proc/1111238/fdinfo/84 /proc/1111238/fdinfo/85 /proc/1111238/fdinfo/86 /proc/1111238/fdinfo/87 /proc/1111238/fdinfo/88 /proc/1111238/fdinfo/89 /proc/1111238/fdinfo/9 /proc/1111238/fdinfo/90 /proc/1111238/fdinfo/91 /proc/1111238/fdinfo/92 /proc/1111238/fdinfo/93 /proc/1111238/fdinfo/94 /proc/1111238/fdinfo/95 /proc/1111238/fdinfo/96 /proc/1111238/fdinfo/97 /proc/1111238/fdinfo/98 /proc/1111238/fdinfo/99 /proc/1111240/fdinfo/0 /proc/1111240/fdinfo/1 /proc/1111240/fdinfo/2 /proc/1111241/fdinfo/0 /proc/1111241/fdinfo/1 /proc/1111241/fdinfo/2 /proc/1111242/fdinfo/0 /proc/1111242/fdinfo/1 /proc/1111242/fdinfo/2 /proc/1111243/fdinfo/0 /proc/1111243/fdinfo/1 /proc/1111243/fdinfo/2 /proc/1111243/fdinfo/4 /proc/1111245/fdinfo/0 /proc/1111245/fdinfo/1 /proc/1111245/fdinfo/2 /proc/1111247/fdinfo/0 /proc/1111247/fdinfo/1 /proc/1111247/fdinfo/2 /proc/1111249/fdinfo/0 /proc/1111249/fdinfo/1 /proc/1111249/fdinfo/2 /proc/1111249/fdinfo/255 /proc/1111252/fdinfo/0 /proc/1111252/fdinfo/1 /proc/1111252/fdinfo/2 /proc/1111253/fdinfo/0 /proc/1111253/fdinfo/1 /proc/1111253/fdinfo/2 /proc/1111253/fdinfo/3 /proc/1111253/fdinfo/5 /proc/1111254/fdinfo/0 /proc/1111254/fdinfo/1 /proc/1111254/fdinfo/2 /proc/1111255/fdinfo/0 /proc/1111255/fdinfo/1 /proc/1111255/fdinfo/2 /proc/1111255/fdinfo/255 /proc/1111255/fdinfo/3 /proc/1111260/fdinfo/0 /proc/1111260/fdinfo/1 /proc/1111260/fdinfo/10 /proc/1111260/fdinfo/11 /proc/1111260/fdinfo/12 /proc/1111260/fdinfo/2 /proc/1111260/fdinfo/255 /proc/1111260/fdinfo/63 /proc/1111263/fdinfo/0 /proc/1111263/fdinfo/1 /proc/1111263/fdinfo/2 /proc/1111265/fdinfo/0 /proc/1111265/fdinfo/1 /proc/1111265/fdinfo/10 /proc/1111265/fdinfo/2 /proc/1111265/fdinfo/3 /proc/1111265/fdinfo/9 /proc/1111266/fdinfo/0 /proc/1111266/fdinfo/1 /proc/1111266/fdinfo/2 /proc/1111268/fdinfo/0 /proc/1111268/fdinfo/1 /proc/1111268/fdinfo/2 /proc/1111270/fdinfo/0 /proc/1111270/fdinfo/1 /proc/1111270/fdinfo/2 /proc/1111270/fdinfo/255 /proc/1111275/fdinfo/0 /proc/1111275/fdinfo/1 /proc/1111275/fdinfo/2 /proc/1111277/fdinfo/0 /proc/1111277/fdinfo/1 /proc/1111277/fdinfo/2 /proc/1111280/fdinfo/0 /proc/1111280/fdinfo/1 /proc/1111280/fdinfo/2 /proc/1111280/fdinfo/3 /proc/1111281/fdinfo/0 /proc/1111281/fdinfo/1 /proc/1111281/fdinfo/2 /proc/1111283/fdinfo/0 /proc/1111283/fdinfo/1 /proc/1111283/fdinfo/2 /proc/1111287/fdinfo/0 /proc/1111287/fdinfo/1 /proc/1111287/fdinfo/2 /proc/1111287/fdinfo/3 /proc/1111288/fdinfo/0 /proc/1111288/fdinfo/1 /proc/1111288/fdinfo/2 /proc/1111290/fdinfo/0 /proc/1111290/fdinfo/1 /proc/1111290/fdinfo/2 /proc/1111290/fdinfo/3 /proc/1111292/fdinfo/0 /proc/1111292/fdinfo/1 /proc/1111292/fdinfo/2 /proc/1111292/fdinfo/3 /proc/1111294/fdinfo/0 /proc/1111294/fdinfo/1 /proc/1111294/fdinfo/2 /proc/1111296/fdinfo/0 /proc/1111296/fdinfo/1 /proc/1111296/fdinfo/2 /proc/1111307/fdinfo/0 /proc/1111307/fdinfo/1 /proc/1111307/fdinfo/2 /proc/1111307/fdinfo/3 /proc/1111316/fdinfo/0 /proc/1111316/fdinfo/1 /proc/1111316/fdinfo/2 /proc/1111317/fdinfo/0 /proc/1111317/fdinfo/1 /proc/1111317/fdinfo/2 /proc/1111317/fdinfo/255 /proc/1111317/fdinfo/3 /proc/1111318/fdinfo/0 /proc/1111318/fdinfo/1 /proc/1111318/fdinfo/2 /proc/1111318/fdinfo/255 /proc/1111318/fdinfo/3 /proc/1111318/fdinfo/9 /proc/1111322/fdinfo/0 /proc/1111322/fdinfo/1 /proc/1111322/fdinfo/2 /proc/1111334/fdinfo/0 /proc/1111334/fdinfo/1 /proc/1111334/fdinfo/2 /proc/1111336/fdinfo/0 /proc/1111336/fdinfo/1 /proc/1111336/fdinfo/2 /proc/1111336/fdinfo/255 /proc/1111336/fdinfo/3 /proc/1111336/fdinfo/9 /proc/1111338/fdinfo/0 /proc/1111338/fdinfo/1 /proc/1111338/fdinfo/2 /proc/1111339/fdinfo/0 /proc/1111339/fdinfo/1 /proc/1111339/fdinfo/2 /proc/1111339/fdinfo/3 /proc/1111339/fdinfo/5 /proc/1111342/fdinfo/0 /proc/1111342/fdinfo/1 /proc/1111342/fdinfo/2 /proc/1111344/fdinfo/0 /proc/1111344/fdinfo/1 /proc/1111344/fdinfo/2 /proc/1111345/fdinfo/0 /proc/1111345/fdinfo/1 /proc/1111345/fdinfo/2 /proc/1111346/fdinfo/0 /proc/1111346/fdinfo/1 /proc/1111346/fdinfo/2 /proc/1111348/fdinfo/0 /proc/1111348/fdinfo/1 /proc/1111348/fdinfo/2 /proc/1111350/fdinfo/0 /proc/1111350/fdinfo/1 /proc/1111350/fdinfo/2 /proc/1111351/fdinfo/0 /proc/1111351/fdinfo/1 /proc/1111351/fdinfo/2 /proc/1111351/fdinfo/3 /proc/1111352/fdinfo/0 /proc/1111352/fdinfo/1 /proc/1111352/fdinfo/2 /proc/1111353/fdinfo/0 /proc/1111353/fdinfo/1 /proc/1111353/fdinfo/2 /proc/1111354/fdinfo/0 /proc/1111354/fdinfo/1 /proc/1111354/fdinfo/2 /proc/1111367/fdinfo/0 /proc/1111367/fdinfo/1 /proc/1111367/fdinfo/2 /proc/1111371/fdinfo/0 /proc/1111371/fdinfo/1 /proc/1111371/fdinfo/2 /proc/1111372/fdinfo/0 /proc/1111372/fdinfo/1 /proc/1111372/fdinfo/2 /proc/1111372/fdinfo/3 /proc/1111374/fdinfo/0 /proc/1111374/fdinfo/1 /proc/1111374/fdinfo/2 /proc/1111374/fdinfo/63 /proc/1111375/fdinfo/0 /proc/1111375/fdinfo/1 /proc/1111375/fdinfo/2 /proc/1111375/fdinfo/255 /proc/1111375/fdinfo/3 /proc/1111376/fdinfo/0 /proc/1111376/fdinfo/1 /proc/1111376/fdinfo/2 /proc/1111378/fdinfo/0 /proc/1111378/fdinfo/1 /proc/1111378/fdinfo/2 /proc/1111380/fdinfo/0 /proc/1111380/fdinfo/1 /proc/1111380/fdinfo/2 /proc/1111380/fdinfo/255 /proc/1111380/fdinfo/3 /proc/1111383/fdinfo/0 /proc/1111383/fdinfo/1 /proc/1111383/fdinfo/2 /proc/1111383/fdinfo/255 /proc/1111383/fdinfo/3 /proc/1111385/fdinfo/0 /proc/1111385/fdinfo/1 /proc/1111385/fdinfo/2 /proc/1111385/fdinfo/255 /proc/1111386/fdinfo/0 /proc/1111386/fdinfo/1 /proc/1111386/fdinfo/2 /proc/1111386/fdinfo/255 /proc/1111386/fdinfo/3 /proc/1111389/fdinfo/0 /proc/1111389/fdinfo/1 /proc/1111389/fdinfo/2 /proc/1111390/fdinfo/0 /proc/1111390/fdinfo/1 /proc/1111390/fdinfo/2 /proc/1111391/fdinfo/0 /proc/1111391/fdinfo/1 /proc/1111391/fdinfo/2 /proc/1111396/fdinfo/0 /proc/1111396/fdinfo/1 /proc/1111396/fdinfo/2 /proc/1111397/fdinfo/0 /proc/1111397/fdinfo/1 /proc/1111397/fdinfo/2 /proc/1111397/fdinfo/255 /proc/1111398/fdinfo/0 /proc/1111398/fdinfo/1 /proc/1111398/fdinfo/2 /proc/1111398/fdinfo/3 /proc/1111400/fdinfo/0 /proc/1111400/fdinfo/1 /proc/1111400/fdinfo/2 /proc/1111401/fdinfo/0 /proc/1111401/fdinfo/1 /proc/1111401/fdinfo/2 /proc/1111401/fdinfo/3 /proc/1111403/fdinfo/0 /proc/1111403/fdinfo/1 /proc/1111403/fdinfo/2 /proc/1111404/fdinfo/0 /proc/1111404/fdinfo/1 /proc/1111404/fdinfo/2 /proc/1111404/fdinfo/255 /proc/1111404/fdinfo/3 /proc/1111405/fdinfo/0 /proc/1111405/fdinfo/1 /proc/1111405/fdinfo/2 /proc/1111405/fdinfo/255 /proc/1111405/fdinfo/3 /proc/1111406/fdinfo/0 /proc/1111406/fdinfo/1 /proc/1111406/fdinfo/2 /proc/1111406/fdinfo/3 /proc/1111406/fdinfo/4 /proc/1111407/fdinfo/0 /proc/1111407/fdinfo/1 /proc/1111407/fdinfo/2 /proc/1111408/fdinfo/0 /proc/1111408/fdinfo/1 /proc/1111408/fdinfo/2 /proc/1111412/fdinfo/0 /proc/1111412/fdinfo/1 /proc/1111412/fdinfo/2 /proc/1111413/fdinfo/0 /proc/1111413/fdinfo/1 /proc/1111413/fdinfo/2 /proc/1111414/fdinfo/0 /proc/1111414/fdinfo/1 /proc/1111414/fdinfo/2 /proc/1111415/fdinfo/0 /proc/1111415/fdinfo/1 /proc/1111415/fdinfo/2 /proc/1111417/fdinfo/0 /proc/1111417/fdinfo/1 /proc/1111417/fdinfo/2 /proc/1111417/fdinfo/255 /proc/1111418/fdinfo/0 /proc/1111418/fdinfo/1 /proc/1111418/fdinfo/2 /proc/1111418/fdinfo/3 /proc/1111420/fdinfo/0 /proc/1111420/fdinfo/1 /proc/1111420/fdinfo/2 /proc/1111420/fdinfo/3 /proc/1111420/fdinfo/4 /proc/1111423/fdinfo/0 /proc/1111423/fdinfo/1 /proc/1111423/fdinfo/2 /proc/1111426/fdinfo/0 /proc/1111426/fdinfo/1 /proc/1111426/fdinfo/2 /proc/1111428/fdinfo/0 /proc/1111428/fdinfo/1 /proc/1111428/fdinfo/10 /proc/1111428/fdinfo/2 /proc/1111428/fdinfo/255 /proc/1111428/fdinfo/3 /proc/1111429/fdinfo/0 /proc/1111429/fdinfo/1 /proc/1111429/fdinfo/2 /proc/1111429/fdinfo/3 /proc/1111430/fdinfo/0 /proc/1111430/fdinfo/1 /proc/1111430/fdinfo/2 /proc/1111431/fdinfo/0 /proc/1111431/fdinfo/1 /proc/1111431/fdinfo/2 /proc/1111436/fdinfo/0 /proc/1111436/fdinfo/1 /proc/1111436/fdinfo/2 /proc/1111437/fdinfo/0 /proc/1111437/fdinfo/1 /proc/1111437/fdinfo/2 /proc/1111437/fdinfo/255 /proc/1111444/fdinfo/0 /proc/1111444/fdinfo/1 /proc/1111444/fdinfo/2 /proc/1111444/fdinfo/9 /proc/1111445/fdinfo/0 /proc/1111445/fdinfo/1 /proc/1111445/fdinfo/2 /proc/1111447/fdinfo/0 /proc/1111447/fdinfo/1 /proc/1111447/fdinfo/2 /proc/1111447/fdinfo/3 /proc/1111449/fdinfo/0 /proc/1111449/fdinfo/1 /proc/1111449/fdinfo/2 /proc/1111450/fdinfo/0 /proc/1111450/fdinfo/1 /proc/1111450/fdinfo/2 /proc/1111450/fdinfo/3 /proc/1111451/fdinfo/0 /proc/1111451/fdinfo/1 /proc/1111451/fdinfo/2 /proc/1111451/fdinfo/255 /proc/1111451/fdinfo/3 /proc/1111452/fdinfo/0 /proc/1111452/fdinfo/1 /proc/1111452/fdinfo/2 /proc/1111452/fdinfo/255 /proc/1111452/fdinfo/3 /proc/1111453/fdinfo/0 /proc/1111453/fdinfo/1 /proc/1111453/fdinfo/2 /proc/1111453/fdinfo/255 /proc/1111456/fdinfo/0 /proc/1111456/fdinfo/1 /proc/1111456/fdinfo/2 /proc/1111457/fdinfo/0 /proc/1111457/fdinfo/1 /proc/1111457/fdinfo/2 /proc/1111458/fdinfo/0 /proc/1111458/fdinfo/1 /proc/1111458/fdinfo/2 /proc/1111459/fdinfo/0 /proc/1111459/fdinfo/1 /proc/1111459/fdinfo/2 /proc/1111462/fdinfo/0 /proc/1111462/fdinfo/1 /proc/1111462/fdinfo/2 /proc/1111462/fdinfo/255 /proc/1111467/fdinfo/0 /proc/1111467/fdinfo/1 /proc/1111467/fdinfo/2 /proc/1111467/fdinfo/3 /proc/1111476/fdinfo/0 /proc/1111476/fdinfo/1 /proc/1111476/fdinfo/2 /proc/1111477/fdinfo/0 /proc/1111477/fdinfo/1 /proc/1111477/fdinfo/2 /proc/1111477/fdinfo/3 /proc/1111478/fdinfo/0 /proc/1111478/fdinfo/1 /proc/1111478/fdinfo/2 /proc/1111484/fdinfo/0 /proc/1111484/fdinfo/1 /proc/1111484/fdinfo/10 /proc/1111484/fdinfo/2 /proc/1111485/fdinfo/0 /proc/1111485/fdinfo/1 /proc/1111485/fdinfo/10 /proc/1111485/fdinfo/2 /proc/1111485/fdinfo/9 /proc/1111486/fdinfo/0 /proc/1111486/fdinfo/1 /proc/1111486/fdinfo/10 /proc/1111486/fdinfo/2 /proc/1111486/fdinfo/3 /proc/1111489/fdinfo/0 /proc/1111489/fdinfo/1 /proc/1111489/fdinfo/2 /proc/1111491/fdinfo/0 /proc/1111491/fdinfo/1 /proc/1111491/fdinfo/2 /proc/1111491/fdinfo/255 /proc/1111491/fdinfo/3 /proc/1111491/fdinfo/63 /proc/1111496/fdinfo/0 /proc/1111496/fdinfo/1 /proc/1111496/fdinfo/10 /proc/1111496/fdinfo/11 /proc/1111496/fdinfo/2 /proc/1111496/fdinfo/63 /proc/1111497/fdinfo/0 /proc/1111497/fdinfo/1 /proc/1111497/fdinfo/2 /proc/1111501/fdinfo/0 /proc/1111501/fdinfo/1 /proc/1111501/fdinfo/2 /proc/1111503/fdinfo/0 /proc/1111503/fdinfo/1 /proc/1111503/fdinfo/2 /proc/1111508/fdinfo/0 /proc/1111508/fdinfo/1 /proc/1111508/fdinfo/2 /proc/1111508/fdinfo/3 /proc/1111511/fdinfo/0 /proc/1111511/fdinfo/1 /proc/1111511/fdinfo/2 /proc/1111511/fdinfo/3 /proc/1111511/fdinfo/9 /proc/1111512/fdinfo/0 /proc/1111512/fdinfo/1 /proc/1111512/fdinfo/2 /proc/1111512/fdinfo/3 /proc/1111522/fdinfo/0 /proc/1111522/fdinfo/1 /proc/1111522/fdinfo/2 /proc/1111522/fdinfo/255 /proc/1111522/fdinfo/3 /proc/1111524/fdinfo/0 /proc/1111524/fdinfo/1 /proc/1111524/fdinfo/2 /proc/1111526/fdinfo/0 /proc/1111526/fdinfo/1 /proc/1111526/fdinfo/2 /proc/1111526/fdinfo/255 /proc/1111526/fdinfo/3 /proc/1111528/fdinfo/0 /proc/1111528/fdinfo/1 /proc/1111528/fdinfo/2 /proc/1111528/fdinfo/3 /proc/1111530/fdinfo/0 /proc/1111530/fdinfo/1 /proc/1111530/fdinfo/2 /proc/1111530/fdinfo/255 /proc/1111530/fdinfo/3 /proc/1111531/fdinfo/0 /proc/1111531/fdinfo/1 /proc/1111531/fdinfo/2 /proc/1111531/fdinfo/255 /proc/1111531/fdinfo/3 /proc/1111532/fdinfo/0 /proc/1111532/fdinfo/1 /proc/1111532/fdinfo/2 /proc/1111532/fdinfo/255 /proc/1111532/fdinfo/3 /proc/1111533/fdinfo/0 /proc/1111533/fdinfo/1 /proc/1111533/fdinfo/2 /proc/1111534/fdinfo/0 /proc/1111534/fdinfo/1 /proc/1111534/fdinfo/2 /proc/1111534/fdinfo/255 /proc/1111537/fdinfo/0 /proc/1111537/fdinfo/1 /proc/1111537/fdinfo/2 /proc/1111539/fdinfo/0 /proc/1111539/fdinfo/1 /proc/1111539/fdinfo/2 /proc/1111539/fdinfo/3 /proc/1111540/fdinfo/0 /proc/1111540/fdinfo/1 /proc/1111540/fdinfo/2 /proc/1111551/fdinfo/0 /proc/1111551/fdinfo/1 /proc/1111551/fdinfo/10 /proc/1111551/fdinfo/11 /proc/1111551/fdinfo/2 /proc/1111552/fdinfo/0 /proc/1111552/fdinfo/1 /proc/1111552/fdinfo/2 /proc/1111553/fdinfo/0 /proc/1111553/fdinfo/1 /proc/1111553/fdinfo/2 /proc/1111553/fdinfo/63 /proc/1111554/fdinfo/0 /proc/1111554/fdinfo/1 /proc/1111554/fdinfo/2 /proc/1111554/fdinfo/255 /proc/1111554/fdinfo/3 /proc/1111555/fdinfo/0 /proc/1111555/fdinfo/1 /proc/1111555/fdinfo/10 /proc/1111555/fdinfo/11 /proc/1111555/fdinfo/2 /proc/1111557/fdinfo/0 /proc/1111557/fdinfo/1 /proc/1111557/fdinfo/2 /proc/1111560/fdinfo/0 /proc/1111560/fdinfo/1 /proc/1111560/fdinfo/10 /proc/1111560/fdinfo/2 /proc/1111560/fdinfo/255 /proc/1111564/fdinfo/0 /proc/1111564/fdinfo/1 /proc/1111564/fdinfo/2 /proc/1111565/fdinfo/0 /proc/1111565/fdinfo/1 /proc/1111565/fdinfo/2 /proc/1111565/fdinfo/255 /proc/1111565/fdinfo/3 /proc/1111567/fdinfo/0 /proc/1111567/fdinfo/1 /proc/1111567/fdinfo/2 /proc/1111567/fdinfo/9 /proc/1111568/fdinfo/0 /proc/1111568/fdinfo/1 /proc/1111568/fdinfo/2 /proc/1111569/fdinfo/0 /proc/1111569/fdinfo/1 /proc/1111569/fdinfo/2 /proc/1111569/fdinfo/9 /proc/1111570/fdinfo/0 /proc/1111570/fdinfo/1 /proc/1111570/fdinfo/2 /proc/1111572/fdinfo/0 /proc/1111572/fdinfo/1 /proc/1111572/fdinfo/2 /proc/1111576/fdinfo/0 /proc/1111576/fdinfo/1 /proc/1111576/fdinfo/2 /proc/1111583/fdinfo/0 /proc/1111583/fdinfo/1 /proc/1111583/fdinfo/2 /proc/1111583/fdinfo/255 /proc/1111583/fdinfo/3 /proc/1111591/fdinfo/0 /proc/1111591/fdinfo/1 /proc/1111591/fdinfo/2 /proc/1111591/fdinfo/255 /proc/1111591/fdinfo/3 /proc/1111593/fdinfo/0 /proc/1111593/fdinfo/1 /proc/1111593/fdinfo/2 /proc/1111594/fdinfo/0 /proc/1111594/fdinfo/1 /proc/1111594/fdinfo/10 /proc/1111594/fdinfo/11 /proc/1111594/fdinfo/12 /proc/1111594/fdinfo/2 /proc/1111594/fdinfo/62 /proc/1111594/fdinfo/63 /proc/1111600/fdinfo/0 /proc/1111600/fdinfo/1 /proc/1111600/fdinfo/2 /proc/1111600/fdinfo/4 /proc/1111600/fdinfo/5 /proc/1111600/fdinfo/6 /proc/1111601/fdinfo/0 /proc/1111601/fdinfo/1 /proc/1111601/fdinfo/2 /proc/1111602/fdinfo/0 /proc/1111602/fdinfo/1 /proc/1111602/fdinfo/2 /proc/1111602/fdinfo/9 /proc/1111607/fdinfo/0 /proc/1111607/fdinfo/1 /proc/1111607/fdinfo/10 /proc/1111607/fdinfo/11 /proc/1111607/fdinfo/2 /proc/1111607/fdinfo/3 /proc/1111607/fdinfo/9 /proc/1111609/fdinfo/0 /proc/1111609/fdinfo/1 /proc/1111609/fdinfo/2 /proc/1111612/fdinfo/0 /proc/1111612/fdinfo/1 /proc/1111612/fdinfo/2 /proc/1111613/fdinfo/0 /proc/1111613/fdinfo/1 /proc/1111613/fdinfo/2 /proc/1111614/fdinfo/0 /proc/1111614/fdinfo/1 /proc/1111614/fdinfo/2 /proc/1111617/fdinfo/0 /proc/1111617/fdinfo/1 /proc/1111617/fdinfo/2 /proc/1111617/fdinfo/255 /proc/1111617/fdinfo/3 /proc/1111623/fdinfo/0 /proc/1111623/fdinfo/1 /proc/1111623/fdinfo/2 /proc/1111624/fdinfo/0 /proc/1111624/fdinfo/1 /proc/1111624/fdinfo/2 /proc/1111626/fdinfo/0 /proc/1111626/fdinfo/1 /proc/1111626/fdinfo/2 /proc/1111632/fdinfo/0 /proc/1111632/fdinfo/1 /proc/1111632/fdinfo/2 /proc/1111634/fdinfo/0 /proc/1111634/fdinfo/1 /proc/1111634/fdinfo/2 /proc/1111634/fdinfo/255 /proc/1111639/fdinfo/0 /proc/1111639/fdinfo/1 /proc/1111639/fdinfo/2 /proc/1111639/fdinfo/3 /proc/1111639/fdinfo/4 /proc/1111639/fdinfo/5 /proc/1111639/fdinfo/6 /proc/1111640/fdinfo/0 /proc/1111640/fdinfo/1 /proc/1111640/fdinfo/2 /proc/1111652/fdinfo/0 /proc/1111652/fdinfo/1 /proc/1111652/fdinfo/2 /proc/1111652/fdinfo/62 /proc/1111652/fdinfo/63 /proc/1111653/fdinfo/0 /proc/1111653/fdinfo/1 /proc/1111653/fdinfo/2 /proc/1111653/fdinfo/255 /proc/1111653/fdinfo/3 /proc/1111653/fdinfo/9 /proc/1111657/fdinfo/0 /proc/1111657/fdinfo/1 /proc/1111657/fdinfo/2 /proc/1111657/fdinfo/255 /proc/1111664/fdinfo/0 /proc/1111664/fdinfo/1 /proc/1111664/fdinfo/2 /proc/1111666/fdinfo/0 /proc/1111666/fdinfo/1 /proc/1111666/fdinfo/2 /proc/1111666/fdinfo/255 /proc/1111666/fdinfo/3 /proc/1111670/fdinfo/0 /proc/1111670/fdinfo/1 /proc/1111670/fdinfo/2 /proc/1111670/fdinfo/63 /proc/1111672/fdinfo/0 /proc/1111672/fdinfo/1 /proc/1111672/fdinfo/10 /proc/1111672/fdinfo/11 /proc/1111672/fdinfo/12 /proc/1111672/fdinfo/2 /proc/1111672/fdinfo/63 /proc/1111679/fdinfo/0 /proc/1111679/fdinfo/1 /proc/1111679/fdinfo/2 /proc/1111679/fdinfo/63 /proc/1111683/fdinfo/0 /proc/1111683/fdinfo/1 /proc/1111683/fdinfo/2 /proc/1111686/fdinfo/0 /proc/1111686/fdinfo/1 /proc/1111686/fdinfo/2 /proc/1111686/fdinfo/3 /proc/1111686/fdinfo/4 /proc/1111686/fdinfo/7 /proc/1111686/fdinfo/9 /proc/1111692/fdinfo/0 /proc/1111692/fdinfo/1 /proc/1111692/fdinfo/2 /proc/1111692/fdinfo/255 /proc/1111696/fdinfo/0 /proc/1111696/fdinfo/1 /proc/1111696/fdinfo/2 /proc/1111705/fdinfo/0 /proc/1111705/fdinfo/1 /proc/1111705/fdinfo/2 /proc/1111705/fdinfo/3 /proc/1111710/fdinfo/0 /proc/1111710/fdinfo/1 /proc/1111710/fdinfo/2 /proc/1111710/fdinfo/255 /proc/1111711/fdinfo/0 /proc/1111711/fdinfo/1 /proc/1111711/fdinfo/10 /proc/1111711/fdinfo/11 /proc/1111711/fdinfo/12 /proc/1111711/fdinfo/2 /proc/1111711/fdinfo/255 /proc/1111711/fdinfo/3 /proc/1111711/fdinfo/62 /proc/1111711/fdinfo/63 /proc/1111714/fdinfo/0 /proc/1111714/fdinfo/1 /proc/1111714/fdinfo/2 /proc/1111714/fdinfo/63 /proc/1111718/fdinfo/0 /proc/1111718/fdinfo/1 /proc/1111718/fdinfo/2 /proc/1111724/fdinfo/0 /proc/1111724/fdinfo/1 /proc/1111724/fdinfo/2 /proc/1111726/fdinfo/0 /proc/1111726/fdinfo/1 /proc/1111726/fdinfo/2 /proc/1111728/fdinfo/0 /proc/1111728/fdinfo/1 /proc/1111728/fdinfo/2 /proc/1111728/fdinfo/3 /proc/1111741/fdinfo/0 /proc/1111741/fdinfo/1 /proc/1111741/fdinfo/10 /proc/1111741/fdinfo/2 /proc/1111741/fdinfo/255 /proc/1111743/fdinfo/0 /proc/1111743/fdinfo/1 /proc/1111743/fdinfo/2 /proc/1111754/fdinfo/0 /proc/1111754/fdinfo/1 /proc/1111754/fdinfo/2 /proc/1111760/fdinfo/0 /proc/1111760/fdinfo/1 /proc/1111760/fdinfo/2 /proc/1111761/fdinfo/0 /proc/1111761/fdinfo/1 /proc/1111761/fdinfo/2 /proc/1111761/fdinfo/3 /proc/1111762/fdinfo/0 /proc/1111762/fdinfo/1 /proc/1111762/fdinfo/2 /proc/1111762/fdinfo/255 /proc/1111772/fdinfo/0 /proc/1111772/fdinfo/1 /proc/1111772/fdinfo/2 /proc/1111772/fdinfo/63 /proc/1111775/fdinfo/0 /proc/1111775/fdinfo/1 /proc/1111775/fdinfo/2 /proc/1111775/fdinfo/3 /proc/1111780/fdinfo/0 /proc/1111780/fdinfo/1 /proc/1111780/fdinfo/2 /proc/1111780/fdinfo/255 /proc/1111780/fdinfo/3 /proc/1111781/fdinfo/0 /proc/1111781/fdinfo/1 /proc/1111781/fdinfo/2 /proc/1111787/fdinfo/0 /proc/1111787/fdinfo/1 /proc/1111787/fdinfo/2 /proc/1111793/fdinfo/0 /proc/1111793/fdinfo/1 /proc/1111793/fdinfo/2 /proc/1111794/fdinfo/0 /proc/1111794/fdinfo/1 /proc/1111794/fdinfo/10 /proc/1111794/fdinfo/11 /proc/1111794/fdinfo/2 /proc/1111794/fdinfo/63 /proc/1111806/fdinfo/0 /proc/1111806/fdinfo/1 /proc/1111806/fdinfo/2 /proc/1111806/fdinfo/9 /proc/1111807/fdinfo/0 /proc/1111807/fdinfo/1 /proc/1111807/fdinfo/2 /proc/1111807/fdinfo/3 /proc/1111809/fdinfo/0 /proc/1111809/fdinfo/1 /proc/1111809/fdinfo/2 /proc/1111809/fdinfo/3 /proc/1111810/fdinfo/0 /proc/1111810/fdinfo/1 /proc/1111810/fdinfo/10 /proc/1111810/fdinfo/2 /proc/1111810/fdinfo/255 /proc/1111810/fdinfo/3 /proc/1111810/fdinfo/9 /proc/1111846/fdinfo/0 /proc/1111846/fdinfo/1 /proc/1111846/fdinfo/2 /proc/1111846/fdinfo/3 /proc/1111847/fdinfo/0 /proc/1111847/fdinfo/1 /proc/1111847/fdinfo/2 /proc/1111848/fdinfo/0 /proc/1111848/fdinfo/1 /proc/1111848/fdinfo/2 /proc/1111851/fdinfo/0 /proc/1111851/fdinfo/1 /proc/1111851/fdinfo/2 /proc/1111853/fdinfo/0 /proc/1111853/fdinfo/1 /proc/1111853/fdinfo/10 /proc/1111853/fdinfo/11 /proc/1111853/fdinfo/12 /proc/1111853/fdinfo/13 /proc/1111853/fdinfo/14 /proc/1111853/fdinfo/15 /proc/1111853/fdinfo/16 /proc/1111853/fdinfo/17 /proc/1111853/fdinfo/18 /proc/1111853/fdinfo/19 /proc/1111853/fdinfo/2 /proc/1111853/fdinfo/20 /proc/1111853/fdinfo/21 /proc/1111853/fdinfo/23 /proc/1111853/fdinfo/3 /proc/1111853/fdinfo/4 /proc/1111853/fdinfo/5 /proc/1111853/fdinfo/6 /proc/1111853/fdinfo/7 /proc/1111853/fdinfo/8 /proc/1111853/fdinfo/9 /proc/1111854/fdinfo/0 /proc/1111854/fdinfo/1 /proc/1111854/fdinfo/2 /proc/1111854/fdinfo/255 /proc/1111854/fdinfo/3 /proc/1111855/fdinfo/0 /proc/1111855/fdinfo/1 /proc/1111855/fdinfo/10 /proc/1111855/fdinfo/11 /proc/1111855/fdinfo/2 /proc/1111860/fdinfo/0 /proc/1111860/fdinfo/1 /proc/1111860/fdinfo/2 /proc/1111860/fdinfo/255 /proc/1111877/fdinfo/0 /proc/1111877/fdinfo/1 /proc/1111877/fdinfo/2 /proc/1111877/fdinfo/255 /proc/1111877/fdinfo/3 /proc/1111878/fdinfo/0 /proc/1111878/fdinfo/1 /proc/1111878/fdinfo/2 /proc/1111881/fdinfo/0 /proc/1111881/fdinfo/1 /proc/1111881/fdinfo/2 /proc/1111881/fdinfo/63 /proc/1111888/fdinfo/0 /proc/1111888/fdinfo/1 /proc/1111888/fdinfo/2 /proc/1111888/fdinfo/9 /proc/1111889/fdinfo/0 /proc/1111889/fdinfo/1 /proc/1111889/fdinfo/2 /proc/1111889/fdinfo/255 /proc/1111889/fdinfo/3 /proc/1111891/fdinfo/0 /proc/1111891/fdinfo/1 /proc/1111891/fdinfo/2 /proc/1111893/fdinfo/0 /proc/1111893/fdinfo/1 /proc/1111893/fdinfo/2 /proc/1111893/fdinfo/3 /proc/1111898/fdinfo/0 /proc/1111898/fdinfo/1 /proc/1111898/fdinfo/2 /proc/1111898/fdinfo/3 /proc/1111898/fdinfo/5 /proc/1111899/fdinfo/0 /proc/1111899/fdinfo/1 /proc/1111899/fdinfo/2 /proc/1111900/fdinfo/0 /proc/1111900/fdinfo/1 /proc/1111900/fdinfo/10 /proc/1111900/fdinfo/2 /proc/1111900/fdinfo/3 /proc/1111901/fdinfo/0 /proc/1111901/fdinfo/1 /proc/1111901/fdinfo/2 /proc/1111906/fdinfo/0 /proc/1111906/fdinfo/1 /proc/1111906/fdinfo/2 /proc/1111906/fdinfo/3 /proc/1111911/fdinfo/0 /proc/1111911/fdinfo/1 /proc/1111911/fdinfo/2 /proc/1111911/fdinfo/3 /proc/1111911/fdinfo/4 /proc/1111911/fdinfo/5 /proc/1111914/fdinfo/0 /proc/1111914/fdinfo/1 /proc/1111914/fdinfo/2 /proc/1111916/fdinfo/0 /proc/1111916/fdinfo/1 /proc/1111916/fdinfo/2 /proc/1111916/fdinfo/255 /proc/1111916/fdinfo/3 /proc/1111918/fdinfo/0 /proc/1111918/fdinfo/1 /proc/1111918/fdinfo/2 /proc/1111918/fdinfo/3 /proc/1111929/fdinfo/0 /proc/1111929/fdinfo/1 /proc/1111929/fdinfo/2 /proc/1111930/fdinfo/0 /proc/1111930/fdinfo/1 /proc/1111930/fdinfo/2 /proc/1111937/fdinfo/0 /proc/1111937/fdinfo/1 /proc/1111937/fdinfo/2 /proc/1111939/fdinfo/0 /proc/1111939/fdinfo/1 /proc/1111939/fdinfo/2 /proc/1111947/fdinfo/0 /proc/1111947/fdinfo/1 /proc/1111947/fdinfo/2 /proc/1111949/fdinfo/0 /proc/1111949/fdinfo/1 /proc/1111949/fdinfo/2 /proc/1111951/fdinfo/0 /proc/1111951/fdinfo/1 /proc/1111951/fdinfo/2 /proc/1111958/fdinfo/0 /proc/1111958/fdinfo/1 /proc/1111958/fdinfo/2 /proc/1111960/fdinfo/0 /proc/1111960/fdinfo/1 /proc/1111960/fdinfo/2 /proc/1111960/fdinfo/3 /proc/1111960/fdinfo/9 /proc/1111962/fdinfo/0 /proc/1111962/fdinfo/1 /proc/1111962/fdinfo/2 /proc/1111962/fdinfo/9 /proc/1111963/fdinfo/0 /proc/1111963/fdinfo/1 /proc/1111963/fdinfo/2 /proc/1111965/fdinfo/0 /proc/1111965/fdinfo/1 /proc/1111965/fdinfo/2 /proc/1111966/fdinfo/0 /proc/1111966/fdinfo/1 /proc/1111966/fdinfo/2 /proc/1111971/fdinfo/0 /proc/1111971/fdinfo/1 /proc/1111971/fdinfo/2 /proc/1111979/fdinfo/0 /proc/1111979/fdinfo/1 /proc/1111979/fdinfo/2 /proc/1111983/fdinfo/0 /proc/1111983/fdinfo/1 /proc/1111983/fdinfo/2 /proc/1111991/fdinfo/0 /proc/1111991/fdinfo/1 /proc/1111991/fdinfo/2 /proc/1111995/fdinfo/0 /proc/1111995/fdinfo/1 /proc/1111995/fdinfo/2 /proc/1111998/fdinfo/0 /proc/1111998/fdinfo/1 /proc/1111998/fdinfo/2 /proc/1111998/fdinfo/255 /proc/1111998/fdinfo/3 /proc/1111999/fdinfo/0 /proc/1111999/fdinfo/1 /proc/1111999/fdinfo/2 /proc/1111999/fdinfo/3 /proc/1111999/fdinfo/9 /proc/1112002/fdinfo/0 /proc/1112002/fdinfo/1 /proc/1112002/fdinfo/2 /proc/1112002/fdinfo/255 /proc/1112002/fdinfo/3 /proc/1112005/fdinfo/0 /proc/1112005/fdinfo/1 /proc/1112005/fdinfo/2 /proc/1112005/fdinfo/255 /proc/1112005/fdinfo/3 /proc/1112006/fdinfo/0 /proc/1112006/fdinfo/1 /proc/1112006/fdinfo/2 /proc/1112006/fdinfo/255 /proc/1112006/fdinfo/3 /proc/1112009/fdinfo/0 /proc/1112009/fdinfo/1 /proc/1112009/fdinfo/2 /proc/1112030/fdinfo/0 /proc/1112030/fdinfo/1 /proc/1112030/fdinfo/2 /proc/1112040/fdinfo/0 /proc/1112040/fdinfo/1 /proc/1112040/fdinfo/10 /proc/1112040/fdinfo/11 /proc/1112040/fdinfo/2 /proc/1112040/fdinfo/255 /proc/1112045/fdinfo/0 /proc/1112045/fdinfo/1 /proc/1112045/fdinfo/2 /proc/1112045/fdinfo/255 /proc/1112062/fdinfo/0 /proc/1112062/fdinfo/1 /proc/1112062/fdinfo/2 /proc/1112083/fdinfo/0 /proc/1112083/fdinfo/1 /proc/1112083/fdinfo/2 /proc/1112126/fdinfo/0 /proc/1112126/fdinfo/1 /proc/1112126/fdinfo/2 /proc/1112135/fdinfo/0 /proc/1112135/fdinfo/1 /proc/1112135/fdinfo/10 /proc/1112135/fdinfo/2 /proc/1112135/fdinfo/255 /proc/1112135/fdinfo/63 /proc/1112137/fdinfo/0 /proc/1112137/fdinfo/1 /proc/1112137/fdinfo/2 /proc/1112137/fdinfo/9 /proc/1112147/fdinfo/0 /proc/1112147/fdinfo/1 /proc/1112147/fdinfo/2 /proc/1112147/fdinfo/3 /proc/1112148/fdinfo/0 /proc/1112148/fdinfo/1 /proc/1112148/fdinfo/2 /proc/1112158/fdinfo/0 /proc/1112158/fdinfo/1 /proc/1112158/fdinfo/10 /proc/1112158/fdinfo/2 /proc/1112159/fdinfo/0 /proc/1112159/fdinfo/1 /proc/1112159/fdinfo/2 /proc/1112190/fdinfo/0 /proc/1112190/fdinfo/1 /proc/1112190/fdinfo/2 /proc/1112190/fdinfo/255 /proc/1112190/fdinfo/7 /proc/1112190/fdinfo/9 /proc/1112199/fdinfo/0 /proc/1112199/fdinfo/1 /proc/1112199/fdinfo/10 /proc/1112199/fdinfo/2 /proc/1112203/fdinfo/0 /proc/1112203/fdinfo/1 /proc/1112203/fdinfo/2 /proc/1112203/fdinfo/3 /proc/1112237/fdinfo/0 /proc/1112237/fdinfo/1 /proc/1112237/fdinfo/2 /proc/1112237/fdinfo/3 /proc/1112246/fdinfo/0 /proc/1112246/fdinfo/1 /proc/1112246/fdinfo/2 /proc/1112246/fdinfo/3 /proc/1112246/fdinfo/9 /proc/1112257/fdinfo/0 /proc/1112257/fdinfo/1 /proc/1112257/fdinfo/2 /proc/1112260/fdinfo/0 /proc/1112260/fdinfo/1 /proc/1112260/fdinfo/2 /proc/1112269/fdinfo/0 /proc/1112269/fdinfo/1 /proc/1112269/fdinfo/2 /proc/1112269/fdinfo/3 /proc/1112277/fdinfo/0 /proc/1112277/fdinfo/1 /proc/1112277/fdinfo/2 /proc/1112291/fdinfo/0 /proc/1112291/fdinfo/1 /proc/1112291/fdinfo/2 /proc/1112291/fdinfo/3 /proc/1112291/fdinfo/9 /proc/1112356/fdinfo/0 /proc/1112356/fdinfo/1 /proc/1112356/fdinfo/2 /proc/1132237/fdinfo/0 /proc/1132237/fdinfo/1 /proc/1132237/fdinfo/2 /proc/1132237/fdinfo/3 /proc/1132237/fdinfo/4 /proc/1132237/fdinfo/5 /proc/1132237/fdinfo/6 /proc/1132237/fdinfo/7 /proc/1132237/fdinfo/8 /proc/1224538/fdinfo/0 /proc/1224538/fdinfo/1 /proc/1224538/fdinfo/2 /proc/1224538/fdinfo/255 /proc/1313/fdinfo/0 /proc/1313/fdinfo/1 /proc/1313/fdinfo/2 /proc/1313/fdinfo/255 /proc/1313/fdinfo/9 /proc/1315/fdinfo/0 /proc/1315/fdinfo/1 /proc/1315/fdinfo/2 /proc/1315/fdinfo/3 /proc/1315/fdinfo/4 /proc/1315/fdinfo/5 /proc/1315/fdinfo/6 /proc/1315/fdinfo/8 /proc/1315/fdinfo/9 /proc/1317/fdinfo/0 /proc/1317/fdinfo/1 /proc/1317/fdinfo/10 /proc/1317/fdinfo/11 /proc/1317/fdinfo/12 /proc/1317/fdinfo/13 /proc/1317/fdinfo/14 /proc/1317/fdinfo/15 /proc/1317/fdinfo/16 /proc/1317/fdinfo/17 /proc/1317/fdinfo/18 /proc/1317/fdinfo/19 /proc/1317/fdinfo/2 /proc/1317/fdinfo/20 /proc/1317/fdinfo/21 /proc/1317/fdinfo/22 /proc/1317/fdinfo/23 /proc/1317/fdinfo/24 /proc/1317/fdinfo/25 /proc/1317/fdinfo/26 /proc/1317/fdinfo/27 /proc/1317/fdinfo/28 /proc/1317/fdinfo/29 /proc/1317/fdinfo/3 /proc/1317/fdinfo/30 /proc/1317/fdinfo/31 /proc/1317/fdinfo/32 /proc/1317/fdinfo/33 /proc/1317/fdinfo/34 /proc/1317/fdinfo/35 /proc/1317/fdinfo/36 /proc/1317/fdinfo/37 /proc/1317/fdinfo/38 /proc/1317/fdinfo/39 /proc/1317/fdinfo/4 /proc/1317/fdinfo/40 /proc/1317/fdinfo/41 /proc/1317/fdinfo/42 /proc/1317/fdinfo/43 /proc/1317/fdinfo/44 /proc/1317/fdinfo/45 /proc/1317/fdinfo/46 /proc/1317/fdinfo/47 /proc/1317/fdinfo/48 /proc/1317/fdinfo/49 /proc/1317/fdinfo/5 /proc/1317/fdinfo/50 /proc/1317/fdinfo/51 /proc/1317/fdinfo/52 /proc/1317/fdinfo/53 /proc/1317/fdinfo/54 /proc/1317/fdinfo/55 /proc/1317/fdinfo/56 /proc/1317/fdinfo/57 /proc/1317/fdinfo/58 /proc/1317/fdinfo/59 /proc/1317/fdinfo/6 /proc/1317/fdinfo/60 /proc/1317/fdinfo/7 /proc/1317/fdinfo/8 /proc/1317/fdinfo/9 /proc/1318/fdinfo/0 /proc/1318/fdinfo/1 /proc/1318/fdinfo/10 /proc/1318/fdinfo/11 /proc/1318/fdinfo/12 /proc/1318/fdinfo/13 /proc/1318/fdinfo/14 /proc/1318/fdinfo/15 /proc/1318/fdinfo/16 /proc/1318/fdinfo/2 /proc/1318/fdinfo/3 /proc/1318/fdinfo/4 /proc/1318/fdinfo/5 /proc/1318/fdinfo/6 /proc/1318/fdinfo/7 /proc/1318/fdinfo/8 /proc/1318/fdinfo/9 /proc/1319/fdinfo/0 /proc/1319/fdinfo/1 /proc/1319/fdinfo/10 /proc/1319/fdinfo/11 /proc/1319/fdinfo/12 /proc/1319/fdinfo/13 /proc/1319/fdinfo/14 /proc/1319/fdinfo/15 /proc/1319/fdinfo/16 /proc/1319/fdinfo/17 /proc/1319/fdinfo/18 /proc/1319/fdinfo/19 /proc/1319/fdinfo/2 /proc/1319/fdinfo/20 /proc/1319/fdinfo/21 /proc/1319/fdinfo/22 /proc/1319/fdinfo/23 /proc/1319/fdinfo/24 /proc/1319/fdinfo/25 /proc/1319/fdinfo/26 /proc/1319/fdinfo/27 /proc/1319/fdinfo/28 /proc/1319/fdinfo/29 /proc/1319/fdinfo/3 /proc/1319/fdinfo/30 /proc/1319/fdinfo/31 /proc/1319/fdinfo/33 /proc/1319/fdinfo/4 /proc/1319/fdinfo/5 /proc/1319/fdinfo/6 /proc/1319/fdinfo/7 /proc/1319/fdinfo/8 /proc/1319/fdinfo/9 /proc/1325/fdinfo/0 /proc/1325/fdinfo/1 /proc/1325/fdinfo/10 /proc/1325/fdinfo/11 /proc/1325/fdinfo/12 /proc/1325/fdinfo/13 /proc/1325/fdinfo/14 /proc/1325/fdinfo/15 /proc/1325/fdinfo/16 /proc/1325/fdinfo/17 /proc/1325/fdinfo/18 /proc/1325/fdinfo/19 /proc/1325/fdinfo/2 /proc/1325/fdinfo/20 /proc/1325/fdinfo/21 /proc/1325/fdinfo/22 /proc/1325/fdinfo/3 /proc/1325/fdinfo/4 /proc/1325/fdinfo/5 /proc/1325/fdinfo/6 /proc/1325/fdinfo/7 /proc/1325/fdinfo/8 /proc/1325/fdinfo/9 /proc/1328079/fdinfo/0 /proc/1328079/fdinfo/1 /proc/1328079/fdinfo/2 /proc/1328079/fdinfo/3 /proc/1328079/fdinfo/4 /proc/1328079/fdinfo/5 /proc/1328079/fdinfo/6 /proc/1328865/fdinfo/0 /proc/1328865/fdinfo/1 /proc/1328865/fdinfo/2 /proc/1328865/fdinfo/255 /proc/1355/fdinfo/0 /proc/1355/fdinfo/1 /proc/1355/fdinfo/10 /proc/1355/fdinfo/11 /proc/1355/fdinfo/12 /proc/1355/fdinfo/13 /proc/1355/fdinfo/14 /proc/1355/fdinfo/2 /proc/1355/fdinfo/3 /proc/1355/fdinfo/4 /proc/1355/fdinfo/5 /proc/1355/fdinfo/6 /proc/1355/fdinfo/7 /proc/1355/fdinfo/8 /proc/1355/fdinfo/9 /proc/1361278/fdinfo/0 /proc/1361278/fdinfo/1 /proc/1361278/fdinfo/10 /proc/1361278/fdinfo/2 /proc/1361278/fdinfo/255 /proc/1398/fdinfo/0 /proc/1398/fdinfo/1 /proc/1398/fdinfo/2 /proc/1398/fdinfo/255 /proc/1412/fdinfo/0 /proc/1412/fdinfo/1 /proc/1412/fdinfo/2 /proc/1412/fdinfo/3 /proc/1412/fdinfo/5 /proc/1548467/fdinfo/0 /proc/1548467/fdinfo/1 /proc/1548467/fdinfo/10 /proc/1548467/fdinfo/11 /proc/1548467/fdinfo/12 /proc/1548467/fdinfo/13 /proc/1548467/fdinfo/14 /proc/1548467/fdinfo/15 /proc/1548467/fdinfo/16 /proc/1548467/fdinfo/17 /proc/1548467/fdinfo/2 /proc/1548467/fdinfo/3 /proc/1548467/fdinfo/4 /proc/1548467/fdinfo/5 /proc/1548467/fdinfo/6 /proc/1548467/fdinfo/7 /proc/1548467/fdinfo/8 /proc/1548467/fdinfo/9 /proc/1561467/fdinfo/0 /proc/1561467/fdinfo/1 /proc/1561467/fdinfo/2 /proc/1561467/fdinfo/3 /proc/1561467/fdinfo/4 /proc/1561467/fdinfo/5 /proc/1561467/fdinfo/6 /proc/1561467/fdinfo/7 /proc/1561467/fdinfo/8 /proc/1674168/fdinfo/0 /proc/1674168/fdinfo/1 /proc/1674168/fdinfo/2 /proc/1674168/fdinfo/3 /proc/1674168/fdinfo/4 /proc/1674168/fdinfo/5 /proc/1674168/fdinfo/6 /proc/1674168/fdinfo/7 /proc/1674168/fdinfo/8 /proc/1674602/fdinfo/0 /proc/1674602/fdinfo/1 /proc/1674602/fdinfo/10 /proc/1674602/fdinfo/11 /proc/1674602/fdinfo/12 /proc/1674602/fdinfo/13 /proc/1674602/fdinfo/14 /proc/1674602/fdinfo/15 /proc/1674602/fdinfo/16 /proc/1674602/fdinfo/17 /proc/1674602/fdinfo/18 /proc/1674602/fdinfo/19 /proc/1674602/fdinfo/2 /proc/1674602/fdinfo/20 /proc/1674602/fdinfo/21 /proc/1674602/fdinfo/23 /proc/1674602/fdinfo/25 /proc/1674602/fdinfo/27 /proc/1674602/fdinfo/3 /proc/1674602/fdinfo/4 /proc/1674602/fdinfo/5 /proc/1674602/fdinfo/6 /proc/1674602/fdinfo/7 /proc/1674602/fdinfo/8 /proc/1674602/fdinfo/9 /proc/1675857/fdinfo/0 /proc/1675857/fdinfo/1 /proc/1675857/fdinfo/10 /proc/1675857/fdinfo/11 /proc/1675857/fdinfo/12 /proc/1675857/fdinfo/13 /proc/1675857/fdinfo/14 /proc/1675857/fdinfo/15 /proc/1675857/fdinfo/16 /proc/1675857/fdinfo/17 /proc/1675857/fdinfo/18 /proc/1675857/fdinfo/19 /proc/1675857/fdinfo/2 /proc/1675857/fdinfo/20 /proc/1675857/fdinfo/21 /proc/1675857/fdinfo/22 /proc/1675857/fdinfo/23 /proc/1675857/fdinfo/24 /proc/1675857/fdinfo/25 /proc/1675857/fdinfo/26 /proc/1675857/fdinfo/27 /proc/1675857/fdinfo/28 /proc/1675857/fdinfo/29 /proc/1675857/fdinfo/3 /proc/1675857/fdinfo/30 /proc/1675857/fdinfo/31 /proc/1675857/fdinfo/32 /proc/1675857/fdinfo/33 /proc/1675857/fdinfo/34 /proc/1675857/fdinfo/35 /proc/1675857/fdinfo/36 /proc/1675857/fdinfo/37 /proc/1675857/fdinfo/38 /proc/1675857/fdinfo/39 /proc/1675857/fdinfo/4 /proc/1675857/fdinfo/40 /proc/1675857/fdinfo/41 /proc/1675857/fdinfo/42 /proc/1675857/fdinfo/43 /proc/1675857/fdinfo/44 /proc/1675857/fdinfo/45 /proc/1675857/fdinfo/46 /proc/1675857/fdinfo/47 /proc/1675857/fdinfo/48 /proc/1675857/fdinfo/49 /proc/1675857/fdinfo/5 /proc/1675857/fdinfo/50 /proc/1675857/fdinfo/51 /proc/1675857/fdinfo/52 /proc/1675857/fdinfo/53 /proc/1675857/fdinfo/54 /proc/1675857/fdinfo/55 /proc/1675857/fdinfo/56 /proc/1675857/fdinfo/57 /proc/1675857/fdinfo/58 /proc/1675857/fdinfo/59 /proc/1675857/fdinfo/6 /proc/1675857/fdinfo/60 /proc/1675857/fdinfo/61 /proc/1675857/fdinfo/62 /proc/1675857/fdinfo/63 /proc/1675857/fdinfo/64 /proc/1675857/fdinfo/65 /proc/1675857/fdinfo/67 /proc/1675857/fdinfo/69 /proc/1675857/fdinfo/7 /proc/1675857/fdinfo/70 /proc/1675857/fdinfo/75 /proc/1675857/fdinfo/8 /proc/1675857/fdinfo/9 /proc/1675900/fdinfo/0 /proc/1675900/fdinfo/1 /proc/1675900/fdinfo/10 /proc/1675900/fdinfo/2 /proc/1675900/fdinfo/3 /proc/1675900/fdinfo/4 /proc/1675900/fdinfo/5 /proc/1675900/fdinfo/6 /proc/1675900/fdinfo/7 /proc/1675900/fdinfo/8 /proc/1675900/fdinfo/9 /proc/1675903/fdinfo/0 /proc/1675903/fdinfo/1 /proc/1675903/fdinfo/10 /proc/1675903/fdinfo/2 /proc/1675903/fdinfo/3 /proc/1675903/fdinfo/4 /proc/1675903/fdinfo/5 /proc/1675903/fdinfo/6 /proc/1675903/fdinfo/7 /proc/1675903/fdinfo/8 /proc/1675903/fdinfo/9 /proc/1675974/fdinfo/0 /proc/1675974/fdinfo/1 /proc/1675974/fdinfo/10 /proc/1675974/fdinfo/11 /proc/1675974/fdinfo/12 /proc/1675974/fdinfo/13 /proc/1675974/fdinfo/14 /proc/1675974/fdinfo/15 /proc/1675974/fdinfo/16 /proc/1675974/fdinfo/17 /proc/1675974/fdinfo/18 /proc/1675974/fdinfo/19 /proc/1675974/fdinfo/2 /proc/1675974/fdinfo/20 /proc/1675974/fdinfo/21 /proc/1675974/fdinfo/22 /proc/1675974/fdinfo/23 /proc/1675974/fdinfo/24 /proc/1675974/fdinfo/25 /proc/1675974/fdinfo/26 /proc/1675974/fdinfo/27 /proc/1675974/fdinfo/29 /proc/1675974/fdinfo/3 /proc/1675974/fdinfo/32 /proc/1675974/fdinfo/4 /proc/1675974/fdinfo/5 /proc/1675974/fdinfo/6 /proc/1675974/fdinfo/7 /proc/1675974/fdinfo/8 /proc/1675974/fdinfo/9 /proc/1675992/fdinfo/0 /proc/1675992/fdinfo/1 /proc/1675992/fdinfo/10 /proc/1675992/fdinfo/103 /proc/1675992/fdinfo/11 /proc/1675992/fdinfo/12 /proc/1675992/fdinfo/13 /proc/1675992/fdinfo/14 /proc/1675992/fdinfo/15 /proc/1675992/fdinfo/16 /proc/1675992/fdinfo/17 /proc/1675992/fdinfo/18 /proc/1675992/fdinfo/19 /proc/1675992/fdinfo/2 /proc/1675992/fdinfo/20 /proc/1675992/fdinfo/21 /proc/1675992/fdinfo/22 /proc/1675992/fdinfo/23 /proc/1675992/fdinfo/24 /proc/1675992/fdinfo/25 /proc/1675992/fdinfo/27 /proc/1675992/fdinfo/28 /proc/1675992/fdinfo/29 /proc/1675992/fdinfo/3 /proc/1675992/fdinfo/30 /proc/1675992/fdinfo/31 /proc/1675992/fdinfo/35 /proc/1675992/fdinfo/36 /proc/1675992/fdinfo/37 /proc/1675992/fdinfo/38 /proc/1675992/fdinfo/39 /proc/1675992/fdinfo/4 /proc/1675992/fdinfo/40 /proc/1675992/fdinfo/41 /proc/1675992/fdinfo/44 /proc/1675992/fdinfo/45 /proc/1675992/fdinfo/48 /proc/1675992/fdinfo/49 /proc/1675992/fdinfo/5 /proc/1675992/fdinfo/50 /proc/1675992/fdinfo/51 /proc/1675992/fdinfo/6 /proc/1675992/fdinfo/7 /proc/1675992/fdinfo/8 /proc/1675992/fdinfo/9 /proc/1678191/fdinfo/0 /proc/1678191/fdinfo/1 /proc/1678191/fdinfo/10 /proc/1678191/fdinfo/100 /proc/1678191/fdinfo/101 /proc/1678191/fdinfo/102 /proc/1678191/fdinfo/103 /proc/1678191/fdinfo/104 /proc/1678191/fdinfo/105 /proc/1678191/fdinfo/106 /proc/1678191/fdinfo/107 /proc/1678191/fdinfo/108 /proc/1678191/fdinfo/109 /proc/1678191/fdinfo/11 /proc/1678191/fdinfo/110 /proc/1678191/fdinfo/111 /proc/1678191/fdinfo/112 /proc/1678191/fdinfo/113 /proc/1678191/fdinfo/114 /proc/1678191/fdinfo/115 /proc/1678191/fdinfo/118 /proc/1678191/fdinfo/12 /proc/1678191/fdinfo/122 /proc/1678191/fdinfo/123 /proc/1678191/fdinfo/124 /proc/1678191/fdinfo/125 /proc/1678191/fdinfo/126 /proc/1678191/fdinfo/127 /proc/1678191/fdinfo/128 /proc/1678191/fdinfo/129 /proc/1678191/fdinfo/13 /proc/1678191/fdinfo/130 /proc/1678191/fdinfo/132 /proc/1678191/fdinfo/14 /proc/1678191/fdinfo/15 /proc/1678191/fdinfo/16 /proc/1678191/fdinfo/17 /proc/1678191/fdinfo/18 /proc/1678191/fdinfo/19 /proc/1678191/fdinfo/2 /proc/1678191/fdinfo/20 /proc/1678191/fdinfo/21 /proc/1678191/fdinfo/22 /proc/1678191/fdinfo/23 /proc/1678191/fdinfo/24 /proc/1678191/fdinfo/25 /proc/1678191/fdinfo/26 /proc/1678191/fdinfo/27 /proc/1678191/fdinfo/28 /proc/1678191/fdinfo/29 /proc/1678191/fdinfo/3 /proc/1678191/fdinfo/30 /proc/1678191/fdinfo/31 /proc/1678191/fdinfo/32 /proc/1678191/fdinfo/33 /proc/1678191/fdinfo/34 /proc/1678191/fdinfo/35 /proc/1678191/fdinfo/36 /proc/1678191/fdinfo/37 /proc/1678191/fdinfo/38 /proc/1678191/fdinfo/39 /proc/1678191/fdinfo/4 /proc/1678191/fdinfo/40 /proc/1678191/fdinfo/41 /proc/1678191/fdinfo/42 /proc/1678191/fdinfo/43 /proc/1678191/fdinfo/44 /proc/1678191/fdinfo/45 /proc/1678191/fdinfo/46 /proc/1678191/fdinfo/47 /proc/1678191/fdinfo/48 /proc/1678191/fdinfo/49 /proc/1678191/fdinfo/5 /proc/1678191/fdinfo/50 /proc/1678191/fdinfo/51 /proc/1678191/fdinfo/52 /proc/1678191/fdinfo/53 /proc/1678191/fdinfo/54 /proc/1678191/fdinfo/55 /proc/1678191/fdinfo/56 /proc/1678191/fdinfo/57 /proc/1678191/fdinfo/58 /proc/1678191/fdinfo/59 /proc/1678191/fdinfo/6 /proc/1678191/fdinfo/60 /proc/1678191/fdinfo/61 /proc/1678191/fdinfo/62 /proc/1678191/fdinfo/63 /proc/1678191/fdinfo/64 /proc/1678191/fdinfo/65 /proc/1678191/fdinfo/66 /proc/1678191/fdinfo/67 /proc/1678191/fdinfo/68 /proc/1678191/fdinfo/69 /proc/1678191/fdinfo/7 /proc/1678191/fdinfo/70 /proc/1678191/fdinfo/71 /proc/1678191/fdinfo/72 /proc/1678191/fdinfo/73 /proc/1678191/fdinfo/74 /proc/1678191/fdinfo/75 /proc/1678191/fdinfo/76 /proc/1678191/fdinfo/77 /proc/1678191/fdinfo/78 /proc/1678191/fdinfo/79 /proc/1678191/fdinfo/8 /proc/1678191/fdinfo/80 /proc/1678191/fdinfo/81 /proc/1678191/fdinfo/82 /proc/1678191/fdinfo/83 /proc/1678191/fdinfo/84 /proc/1678191/fdinfo/85 /proc/1678191/fdinfo/86 /proc/1678191/fdinfo/87 /proc/1678191/fdinfo/88 /proc/1678191/fdinfo/89 /proc/1678191/fdinfo/9 /proc/1678191/fdinfo/90 /proc/1678191/fdinfo/91 /proc/1678191/fdinfo/92 /proc/1678191/fdinfo/93 /proc/1678191/fdinfo/94 /proc/1678191/fdinfo/95 /proc/1678191/fdinfo/96 /proc/1678191/fdinfo/97 /proc/1678191/fdinfo/98 /proc/1678191/fdinfo/99 /proc/1688380/fdinfo/0 /proc/1688380/fdinfo/1 /proc/1688380/fdinfo/10 /proc/1688380/fdinfo/103 /proc/1688380/fdinfo/11 /proc/1688380/fdinfo/12 /proc/1688380/fdinfo/13 /proc/1688380/fdinfo/14 /proc/1688380/fdinfo/2 /proc/1688380/fdinfo/3 /proc/1688380/fdinfo/4 /proc/1688380/fdinfo/5 /proc/1688380/fdinfo/6 /proc/1688380/fdinfo/7 /proc/1688380/fdinfo/8 /proc/1688380/fdinfo/9 /proc/1718199/fdinfo/0 /proc/1718199/fdinfo/1 /proc/1718199/fdinfo/10 /proc/1718199/fdinfo/2 /proc/1718199/fdinfo/255 /proc/173301/fdinfo/0 /proc/173301/fdinfo/1 /proc/173301/fdinfo/10 /proc/173301/fdinfo/2 /proc/173301/fdinfo/255 /proc/173301/fdinfo/8 /proc/1758067/fdinfo/0 /proc/1758067/fdinfo/1 /proc/1758067/fdinfo/2 /proc/1758067/fdinfo/255 /proc/189236/fdinfo/0 /proc/189236/fdinfo/1 /proc/189236/fdinfo/2 /proc/189236/fdinfo/255 /proc/189417/fdinfo/0 /proc/189417/fdinfo/1 /proc/189417/fdinfo/2 /proc/189417/fdinfo/255 /proc/1900/fdinfo/0 /proc/1900/fdinfo/1 /proc/1900/fdinfo/2 /proc/1900/fdinfo/3 /proc/1900/fdinfo/4 /proc/1902/fdinfo/0 /proc/1902/fdinfo/1 /proc/1902/fdinfo/10 /proc/1902/fdinfo/11 /proc/1902/fdinfo/12 /proc/1902/fdinfo/13 /proc/1902/fdinfo/14 /proc/1902/fdinfo/15 /proc/1902/fdinfo/16 /proc/1902/fdinfo/17 /proc/1902/fdinfo/18 /proc/1902/fdinfo/2 /proc/1902/fdinfo/3 /proc/1902/fdinfo/4 /proc/1902/fdinfo/5 /proc/1902/fdinfo/6 /proc/1902/fdinfo/7 /proc/1902/fdinfo/8 /proc/1902/fdinfo/9 /proc/1903/fdinfo/0 /proc/1903/fdinfo/1 /proc/1903/fdinfo/2 /proc/1903/fdinfo/255 /proc/1904/fdinfo/0 /proc/1904/fdinfo/1 /proc/1904/fdinfo/2 /proc/1904/fdinfo/3 /proc/1904/fdinfo/4 /proc/1904/fdinfo/5 /proc/1904/fdinfo/6 /proc/1905/fdinfo/0 /proc/1905/fdinfo/1 /proc/1905/fdinfo/10 /proc/1905/fdinfo/2 /proc/1905/fdinfo/255 /proc/1905/fdinfo/8 /proc/1905/fdinfo/9 /proc/192866/fdinfo/0 /proc/192866/fdinfo/1 /proc/192866/fdinfo/2 /proc/192866/fdinfo/3 /proc/192866/fdinfo/4 /proc/192866/fdinfo/5 /proc/1940/fdinfo/0 /proc/1940/fdinfo/1 /proc/1940/fdinfo/2 /proc/1940/fdinfo/3 /proc/1940/fdinfo/4 /proc/1940/fdinfo/9 /proc/1941/fdinfo/0 /proc/1941/fdinfo/1 /proc/1941/fdinfo/2 /proc/1953208/fdinfo/0 /proc/1953208/fdinfo/1 /proc/1953208/fdinfo/10 /proc/1953208/fdinfo/2 /proc/1953208/fdinfo/255 /proc/2038135/fdinfo/0 /proc/2038135/fdinfo/1 /proc/2038135/fdinfo/10 /proc/2038135/fdinfo/11 /proc/2038135/fdinfo/12 /proc/2038135/fdinfo/13 /proc/2038135/fdinfo/14 /proc/2038135/fdinfo/15 /proc/2038135/fdinfo/16 /proc/2038135/fdinfo/17 /proc/2038135/fdinfo/2 /proc/2038135/fdinfo/3 /proc/2038135/fdinfo/4 /proc/2038135/fdinfo/5 /proc/2038135/fdinfo/6 /proc/2038135/fdinfo/7 /proc/2038135/fdinfo/8 /proc/2038135/fdinfo/9 /proc/2049766/fdinfo/0 /proc/2049766/fdinfo/1 /proc/2049766/fdinfo/10 /proc/2049766/fdinfo/11 /proc/2049766/fdinfo/12 /proc/2049766/fdinfo/13 /proc/2049766/fdinfo/14 /proc/2049766/fdinfo/15 /proc/2049766/fdinfo/16 /proc/2049766/fdinfo/17 /proc/2049766/fdinfo/2 /proc/2049766/fdinfo/3 /proc/2049766/fdinfo/4 /proc/2049766/fdinfo/5 /proc/2049766/fdinfo/6 /proc/2049766/fdinfo/7 /proc/2049766/fdinfo/8 /proc/2049766/fdinfo/9 /proc/213112/fdinfo/0 /proc/213112/fdinfo/1 /proc/213112/fdinfo/2 /proc/213112/fdinfo/255 /proc/215112/fdinfo/0 /proc/215112/fdinfo/1 /proc/215112/fdinfo/10 /proc/215112/fdinfo/2 /proc/215112/fdinfo/255 /proc/2343989/fdinfo/0 /proc/2343989/fdinfo/1 /proc/2343989/fdinfo/10 /proc/2343989/fdinfo/2 /proc/2343989/fdinfo/255 /proc/2519290/fdinfo/0 /proc/2519290/fdinfo/1 /proc/2519290/fdinfo/2 /proc/2519290/fdinfo/3 /proc/2519290/fdinfo/4 /proc/2519290/fdinfo/5 /proc/2519290/fdinfo/6 /proc/2519290/fdinfo/7 /proc/2519290/fdinfo/8 /proc/260682/fdinfo/0 /proc/260682/fdinfo/1 /proc/260682/fdinfo/2 /proc/260682/fdinfo/255 /proc/260682/fdinfo/3 /proc/260871/fdinfo/0 /proc/260871/fdinfo/1 /proc/260871/fdinfo/10 /proc/260871/fdinfo/11 /proc/260871/fdinfo/12 /proc/260871/fdinfo/13 /proc/260871/fdinfo/14 /proc/260871/fdinfo/15 /proc/260871/fdinfo/16 /proc/260871/fdinfo/17 /proc/260871/fdinfo/2 /proc/260871/fdinfo/3 /proc/260871/fdinfo/4 /proc/260871/fdinfo/5 /proc/260871/fdinfo/6 /proc/260871/fdinfo/7 /proc/260871/fdinfo/8 /proc/260871/fdinfo/9 /proc/262117/fdinfo/0 /proc/262117/fdinfo/1 /proc/262117/fdinfo/2 /proc/262117/fdinfo/255 /proc/262117/fdinfo/3 /proc/2621732/fdinfo/0 /proc/2621732/fdinfo/1 /proc/2621732/fdinfo/10 /proc/2621732/fdinfo/11 /proc/2621732/fdinfo/12 /proc/2621732/fdinfo/13 /proc/2621732/fdinfo/14 /proc/2621732/fdinfo/15 /proc/2621732/fdinfo/16 /proc/2621732/fdinfo/17 /proc/2621732/fdinfo/2 /proc/2621732/fdinfo/27 /proc/2621732/fdinfo/3 /proc/2621732/fdinfo/4 /proc/2621732/fdinfo/5 /proc/2621732/fdinfo/6 /proc/2621732/fdinfo/7 /proc/2621732/fdinfo/8 /proc/2621732/fdinfo/9 /proc/262393/fdinfo/0 /proc/262393/fdinfo/1 /proc/262393/fdinfo/2 /proc/262393/fdinfo/255 /proc/266605/fdinfo/0 /proc/266605/fdinfo/1 /proc/266605/fdinfo/2 /proc/266605/fdinfo/255 /proc/266605/fdinfo/3 /proc/2793787/fdinfo/0 /proc/2793787/fdinfo/1 /proc/2793787/fdinfo/2 /proc/2793787/fdinfo/3 /proc/2793787/fdinfo/4 /proc/2793787/fdinfo/5 /proc/2793787/fdinfo/6 /proc/2793787/fdinfo/7 /proc/2793787/fdinfo/8 /proc/2807535/fdinfo/0 /proc/2807535/fdinfo/1 /proc/2807535/fdinfo/2 /proc/2807535/fdinfo/3 /proc/2807535/fdinfo/4 /proc/2807535/fdinfo/5 /proc/2807535/fdinfo/6 /proc/2807535/fdinfo/7 /proc/2807535/fdinfo/8 /proc/2923641/fdinfo/0 /proc/2923641/fdinfo/1 /proc/2923641/fdinfo/10 /proc/2923641/fdinfo/2 /proc/2923641/fdinfo/255 /proc/2969201/fdinfo/0 /proc/2969201/fdinfo/1 /proc/2969201/fdinfo/10 /proc/2969201/fdinfo/2 /proc/2969201/fdinfo/255 /proc/299792/fdinfo/0 /proc/299792/fdinfo/1 /proc/299792/fdinfo/2 /proc/299792/fdinfo/255 /proc/3000654/fdinfo/0 /proc/3000654/fdinfo/1 /proc/3000654/fdinfo/2 /proc/3000654/fdinfo/255 /proc/3000654/fdinfo/9 /proc/3002827/fdinfo/0 /proc/3002827/fdinfo/1 /proc/3002827/fdinfo/2 /proc/3002827/fdinfo/3 /proc/3002827/fdinfo/9 /proc/3085169/fdinfo/0 /proc/3085169/fdinfo/1 /proc/3085169/fdinfo/2 /proc/3085169/fdinfo/3 /proc/3085169/fdinfo/4 /proc/3085169/fdinfo/5 /proc/3085169/fdinfo/6 /proc/3085169/fdinfo/7 /proc/3085169/fdinfo/8 /proc/3094741/fdinfo/0 /proc/3094741/fdinfo/1 /proc/3094741/fdinfo/2 /proc/3094741/fdinfo/3 /proc/3094741/fdinfo/4 /proc/3094741/fdinfo/5 /proc/3094741/fdinfo/6 /proc/3094741/fdinfo/7 /proc/3094741/fdinfo/8 /proc/317664/fdinfo/0 /proc/317664/fdinfo/1 /proc/317664/fdinfo/2 /proc/318780/fdinfo/0 /proc/318780/fdinfo/1 /proc/318780/fdinfo/2 /proc/318780/fdinfo/255 /proc/3191483/fdinfo/0 /proc/3191483/fdinfo/1 /proc/3191483/fdinfo/10 /proc/3191483/fdinfo/11 /proc/3191483/fdinfo/12 /proc/3191483/fdinfo/13 /proc/3191483/fdinfo/14 /proc/3191483/fdinfo/15 /proc/3191483/fdinfo/16 /proc/3191483/fdinfo/17 /proc/3191483/fdinfo/2 /proc/3191483/fdinfo/3 /proc/3191483/fdinfo/4 /proc/3191483/fdinfo/5 /proc/3191483/fdinfo/6 /proc/3191483/fdinfo/7 /proc/3191483/fdinfo/8 /proc/3191483/fdinfo/9 /proc/3209369/fdinfo/0 /proc/3209369/fdinfo/1 /proc/3209369/fdinfo/10 /proc/3209369/fdinfo/2 /proc/3209369/fdinfo/255 /proc/343365/fdinfo/0 /proc/343365/fdinfo/1 /proc/343365/fdinfo/2 /proc/343365/fdinfo/255 /proc/343365/fdinfo/9 /proc/343690/fdinfo/0 /proc/343690/fdinfo/1 /proc/343690/fdinfo/2 /proc/343690/fdinfo/255 /proc/343690/fdinfo/7 /proc/343690/fdinfo/9 /proc/344297/fdinfo/0 /proc/344297/fdinfo/1 /proc/344297/fdinfo/2 /proc/344297/fdinfo/3 /proc/344297/fdinfo/5 /proc/344603/fdinfo/0 /proc/344603/fdinfo/1 /proc/344603/fdinfo/2 /proc/344603/fdinfo/255 /proc/344603/fdinfo/9 /proc/344688/fdinfo/0 /proc/344688/fdinfo/1 /proc/344688/fdinfo/2 /proc/344688/fdinfo/3 /proc/344688/fdinfo/4 /proc/344688/fdinfo/5 /proc/344688/fdinfo/6 /proc/344688/fdinfo/8 /proc/344811/fdinfo/0 /proc/344811/fdinfo/1 /proc/344811/fdinfo/2 /proc/344811/fdinfo/3 /proc/344811/fdinfo/4 /proc/344811/fdinfo/7 /proc/344811/fdinfo/9 /proc/345705/fdinfo/0 /proc/345705/fdinfo/1 /proc/345705/fdinfo/2 /proc/345705/fdinfo/3 /proc/345705/fdinfo/9 /proc/346406/fdinfo/0 /proc/346406/fdinfo/1 /proc/346406/fdinfo/2 /proc/346406/fdinfo/9 /proc/346409/fdinfo/0 /proc/346409/fdinfo/1 /proc/346409/fdinfo/2 /proc/346409/fdinfo/9 /proc/346410/fdinfo/0 /proc/346410/fdinfo/1 /proc/346410/fdinfo/2 /proc/346410/fdinfo/3 /proc/346410/fdinfo/4 /proc/346410/fdinfo/5 /proc/346410/fdinfo/9 /proc/346416/fdinfo/0 /proc/346416/fdinfo/1 /proc/346416/fdinfo/2 /proc/346416/fdinfo/9 /proc/346665/fdinfo/0 /proc/346665/fdinfo/1 /proc/346665/fdinfo/2 /proc/346665/fdinfo/7 /proc/346665/fdinfo/9 /proc/346666/fdinfo/0 /proc/346666/fdinfo/1 /proc/346666/fdinfo/2 /proc/346666/fdinfo/7 /proc/346666/fdinfo/9 /proc/346754/fdinfo/0 /proc/346754/fdinfo/1 /proc/346754/fdinfo/2 /proc/346754/fdinfo/7 /proc/346754/fdinfo/9 /proc/346756/fdinfo/0 /proc/346756/fdinfo/1 /proc/346756/fdinfo/2 /proc/346756/fdinfo/7 /proc/346756/fdinfo/9 /proc/3504319/fdinfo/0 /proc/3504319/fdinfo/1 /proc/3504319/fdinfo/10 /proc/3504319/fdinfo/11 /proc/3504319/fdinfo/2 /proc/3504319/fdinfo/255 /proc/3504319/fdinfo/3 /proc/352321/fdinfo/0 /proc/352321/fdinfo/1 /proc/352321/fdinfo/10 /proc/352321/fdinfo/2 /proc/352321/fdinfo/255 /proc/3549520/fdinfo/0 /proc/3549520/fdinfo/1 /proc/3549520/fdinfo/2 /proc/3549520/fdinfo/3 /proc/3549520/fdinfo/4 /proc/3549520/fdinfo/5 /proc/3549520/fdinfo/6 /proc/3549520/fdinfo/7 /proc/3549520/fdinfo/8 /proc/3658073/fdinfo/0 /proc/3658073/fdinfo/1 /proc/3658073/fdinfo/10 /proc/3658073/fdinfo/2 /proc/3658073/fdinfo/255 /proc/3729179/fdinfo/0 /proc/3729179/fdinfo/1 /proc/3729179/fdinfo/10 /proc/3729179/fdinfo/11 /proc/3729179/fdinfo/12 /proc/3729179/fdinfo/13 /proc/3729179/fdinfo/15 /proc/3729179/fdinfo/16 /proc/3729179/fdinfo/17 /proc/3729179/fdinfo/19 /proc/3729179/fdinfo/2 /proc/3729179/fdinfo/20 /proc/3729179/fdinfo/21 /proc/3729179/fdinfo/23 /proc/3729179/fdinfo/27 /proc/3729179/fdinfo/28 /proc/3729179/fdinfo/3 /proc/3729179/fdinfo/30 /proc/3729179/fdinfo/31 /proc/3729179/fdinfo/33 /proc/3729179/fdinfo/34 /proc/3729179/fdinfo/35 /proc/3729179/fdinfo/36 /proc/3729179/fdinfo/37 /proc/3729179/fdinfo/39 /proc/3729179/fdinfo/4 /proc/3729179/fdinfo/41 /proc/3729179/fdinfo/42 /proc/3729179/fdinfo/43 /proc/3729179/fdinfo/44 /proc/3729179/fdinfo/45 /proc/3729179/fdinfo/46 /proc/3729179/fdinfo/47 /proc/3729179/fdinfo/48 /proc/3729179/fdinfo/5 /proc/3729179/fdinfo/54 /proc/3729179/fdinfo/56 /proc/3729179/fdinfo/7 /proc/3729179/fdinfo/8 /proc/3729179/fdinfo/9 /proc/375057/fdinfo/0 /proc/375057/fdinfo/1 /proc/375057/fdinfo/10 /proc/375057/fdinfo/2 /proc/375057/fdinfo/255 /proc/3828628/fdinfo/0 /proc/3828628/fdinfo/1 /proc/3828628/fdinfo/2 /proc/3894834/fdinfo/0 /proc/3894834/fdinfo/1 /proc/3894834/fdinfo/10 /proc/3894834/fdinfo/11 /proc/3894834/fdinfo/12 /proc/3894834/fdinfo/13 /proc/3894834/fdinfo/14 /proc/3894834/fdinfo/15 /proc/3894834/fdinfo/16 /proc/3894834/fdinfo/17 /proc/3894834/fdinfo/2 /proc/3894834/fdinfo/3 /proc/3894834/fdinfo/4 /proc/3894834/fdinfo/5 /proc/3894834/fdinfo/6 /proc/3894834/fdinfo/60 /proc/3894834/fdinfo/7 /proc/3894834/fdinfo/8 /proc/3894834/fdinfo/9 /proc/3900358/fdinfo/0 /proc/3900358/fdinfo/1 /proc/3900358/fdinfo/10 /proc/3900358/fdinfo/11 /proc/3900358/fdinfo/12 /proc/3900358/fdinfo/13 /proc/3900358/fdinfo/14 /proc/3900358/fdinfo/15 /proc/3900358/fdinfo/16 /proc/3900358/fdinfo/17 /proc/3900358/fdinfo/2 /proc/3900358/fdinfo/3 /proc/3900358/fdinfo/4 /proc/3900358/fdinfo/5 /proc/3900358/fdinfo/51 /proc/3900358/fdinfo/6 /proc/3900358/fdinfo/7 /proc/3900358/fdinfo/8 /proc/3900358/fdinfo/9 /proc/3905731/fdinfo/0 /proc/3905731/fdinfo/1 /proc/3905731/fdinfo/10 /proc/3905731/fdinfo/11 /proc/3905731/fdinfo/12 /proc/3905731/fdinfo/13 /proc/3905731/fdinfo/14 /proc/3905731/fdinfo/15 /proc/3905731/fdinfo/16 /proc/3905731/fdinfo/17 /proc/3905731/fdinfo/2 /proc/3905731/fdinfo/20 /proc/3905731/fdinfo/3 /proc/3905731/fdinfo/4 /proc/3905731/fdinfo/5 /proc/3905731/fdinfo/6 /proc/3905731/fdinfo/7 /proc/3905731/fdinfo/8 /proc/3905731/fdinfo/9 /proc/3929241/fdinfo/0 /proc/3929241/fdinfo/1 /proc/3929241/fdinfo/2 /proc/3929241/fdinfo/3 /proc/3929241/fdinfo/9 /proc/412310/fdinfo/0 /proc/412310/fdinfo/1 /proc/412310/fdinfo/2 /proc/412310/fdinfo/255 /proc/412522/fdinfo/0 /proc/412522/fdinfo/1 /proc/412522/fdinfo/2 /proc/412522/fdinfo/255 /proc/412522/fdinfo/3 /proc/421766/fdinfo/0 /proc/421766/fdinfo/1 /proc/421766/fdinfo/10 /proc/421766/fdinfo/100 /proc/421766/fdinfo/101 /proc/421766/fdinfo/102 /proc/421766/fdinfo/103 /proc/421766/fdinfo/104 /proc/421766/fdinfo/105 /proc/421766/fdinfo/106 /proc/421766/fdinfo/107 /proc/421766/fdinfo/108 /proc/421766/fdinfo/109 /proc/421766/fdinfo/11 /proc/421766/fdinfo/110 /proc/421766/fdinfo/111 /proc/421766/fdinfo/112 /proc/421766/fdinfo/113 /proc/421766/fdinfo/114 /proc/421766/fdinfo/115 /proc/421766/fdinfo/116 /proc/421766/fdinfo/117 /proc/421766/fdinfo/118 /proc/421766/fdinfo/119 /proc/421766/fdinfo/12 /proc/421766/fdinfo/120 /proc/421766/fdinfo/121 /proc/421766/fdinfo/122 /proc/421766/fdinfo/123 /proc/421766/fdinfo/124 /proc/421766/fdinfo/125 /proc/421766/fdinfo/126 /proc/421766/fdinfo/127 /proc/421766/fdinfo/128 /proc/421766/fdinfo/129 /proc/421766/fdinfo/13 /proc/421766/fdinfo/130 /proc/421766/fdinfo/131 /proc/421766/fdinfo/132 /proc/421766/fdinfo/133 /proc/421766/fdinfo/134 /proc/421766/fdinfo/135 /proc/421766/fdinfo/136 /proc/421766/fdinfo/137 /proc/421766/fdinfo/138 /proc/421766/fdinfo/139 /proc/421766/fdinfo/14 /proc/421766/fdinfo/140 /proc/421766/fdinfo/141 /proc/421766/fdinfo/142 /proc/421766/fdinfo/143 /proc/421766/fdinfo/144 /proc/421766/fdinfo/145 /proc/421766/fdinfo/146 /proc/421766/fdinfo/147 /proc/421766/fdinfo/148 /proc/421766/fdinfo/149 /proc/421766/fdinfo/15 /proc/421766/fdinfo/150 /proc/421766/fdinfo/151 /proc/421766/fdinfo/152 /proc/421766/fdinfo/153 /proc/421766/fdinfo/154 /proc/421766/fdinfo/155 /proc/421766/fdinfo/156 /proc/421766/fdinfo/157 /proc/421766/fdinfo/158 /proc/421766/fdinfo/159 /proc/421766/fdinfo/16 /proc/421766/fdinfo/160 /proc/421766/fdinfo/161 /proc/421766/fdinfo/162 /proc/421766/fdinfo/163 /proc/421766/fdinfo/164 /proc/421766/fdinfo/165 /proc/421766/fdinfo/17 /proc/421766/fdinfo/171 /proc/421766/fdinfo/18 /proc/421766/fdinfo/19 /proc/421766/fdinfo/2 /proc/421766/fdinfo/20 /proc/421766/fdinfo/21 /proc/421766/fdinfo/22 /proc/421766/fdinfo/23 /proc/421766/fdinfo/24 /proc/421766/fdinfo/25 /proc/421766/fdinfo/26 /proc/421766/fdinfo/27 /proc/421766/fdinfo/28 /proc/421766/fdinfo/29 /proc/421766/fdinfo/3 /proc/421766/fdinfo/30 /proc/421766/fdinfo/31 /proc/421766/fdinfo/32 /proc/421766/fdinfo/33 /proc/421766/fdinfo/34 /proc/421766/fdinfo/35 /proc/421766/fdinfo/36 /proc/421766/fdinfo/37 /proc/421766/fdinfo/38 /proc/421766/fdinfo/39 /proc/421766/fdinfo/4 /proc/421766/fdinfo/40 /proc/421766/fdinfo/41 /proc/421766/fdinfo/42 /proc/421766/fdinfo/43 /proc/421766/fdinfo/44 /proc/421766/fdinfo/45 /proc/421766/fdinfo/46 /proc/421766/fdinfo/47 /proc/421766/fdinfo/48 /proc/421766/fdinfo/49 /proc/421766/fdinfo/5 /proc/421766/fdinfo/50 /proc/421766/fdinfo/51 /proc/421766/fdinfo/52 /proc/421766/fdinfo/53 /proc/421766/fdinfo/54 /proc/421766/fdinfo/55 /proc/421766/fdinfo/56 /proc/421766/fdinfo/57 /proc/421766/fdinfo/58 /proc/421766/fdinfo/59 /proc/421766/fdinfo/6 /proc/421766/fdinfo/60 /proc/421766/fdinfo/61 /proc/421766/fdinfo/62 /proc/421766/fdinfo/63 /proc/421766/fdinfo/64 /proc/421766/fdinfo/65 /proc/421766/fdinfo/66 /proc/421766/fdinfo/67 /proc/421766/fdinfo/68 /proc/421766/fdinfo/69 /proc/421766/fdinfo/7 /proc/421766/fdinfo/70 /proc/421766/fdinfo/71 /proc/421766/fdinfo/72 /proc/421766/fdinfo/73 /proc/421766/fdinfo/74 /proc/421766/fdinfo/75 /proc/421766/fdinfo/76 /proc/421766/fdinfo/77 /proc/421766/fdinfo/78 /proc/421766/fdinfo/79 /proc/421766/fdinfo/8 /proc/421766/fdinfo/80 /proc/421766/fdinfo/81 /proc/421766/fdinfo/82 /proc/421766/fdinfo/83 /proc/421766/fdinfo/84 /proc/421766/fdinfo/85 /proc/421766/fdinfo/86 /proc/421766/fdinfo/87 /proc/421766/fdinfo/88 /proc/421766/fdinfo/89 /proc/421766/fdinfo/9 /proc/421766/fdinfo/90 /proc/421766/fdinfo/91 /proc/421766/fdinfo/92 /proc/421766/fdinfo/93 /proc/421766/fdinfo/94 /proc/421766/fdinfo/95 /proc/421766/fdinfo/96 /proc/421766/fdinfo/97 /proc/421766/fdinfo/98 /proc/421766/fdinfo/99 /proc/421853/fdinfo/0 /proc/421853/fdinfo/1 /proc/421853/fdinfo/10 /proc/421853/fdinfo/11 /proc/421853/fdinfo/12 /proc/421853/fdinfo/13 /proc/421853/fdinfo/14 /proc/421853/fdinfo/15 /proc/421853/fdinfo/16 /proc/421853/fdinfo/17 /proc/421853/fdinfo/18 /proc/421853/fdinfo/19 /proc/421853/fdinfo/2 /proc/421853/fdinfo/20 /proc/421853/fdinfo/21 /proc/421853/fdinfo/22 /proc/421853/fdinfo/23 /proc/421853/fdinfo/24 /proc/421853/fdinfo/25 /proc/421853/fdinfo/26 /proc/421853/fdinfo/27 /proc/421853/fdinfo/28 /proc/421853/fdinfo/29 /proc/421853/fdinfo/3 /proc/421853/fdinfo/30 /proc/421853/fdinfo/31 /proc/421853/fdinfo/32 /proc/421853/fdinfo/33 /proc/421853/fdinfo/34 /proc/421853/fdinfo/35 /proc/421853/fdinfo/36 /proc/421853/fdinfo/4 /proc/421853/fdinfo/5 /proc/421853/fdinfo/6 /proc/421853/fdinfo/7 /proc/421853/fdinfo/8 /proc/421853/fdinfo/9 /proc/421916/fdinfo/0 /proc/421916/fdinfo/1 /proc/421916/fdinfo/10 /proc/421916/fdinfo/11 /proc/421916/fdinfo/12 /proc/421916/fdinfo/13 /proc/421916/fdinfo/14 /proc/421916/fdinfo/15 /proc/421916/fdinfo/16 /proc/421916/fdinfo/17 /proc/421916/fdinfo/18 /proc/421916/fdinfo/19 /proc/421916/fdinfo/2 /proc/421916/fdinfo/20 /proc/421916/fdinfo/21 /proc/421916/fdinfo/22 /proc/421916/fdinfo/23 /proc/421916/fdinfo/24 /proc/421916/fdinfo/25 /proc/421916/fdinfo/26 /proc/421916/fdinfo/27 /proc/421916/fdinfo/28 /proc/421916/fdinfo/29 /proc/421916/fdinfo/3 /proc/421916/fdinfo/30 /proc/421916/fdinfo/31 /proc/421916/fdinfo/32 /proc/421916/fdinfo/33 /proc/421916/fdinfo/34 /proc/421916/fdinfo/35 /proc/421916/fdinfo/36 /proc/421916/fdinfo/37 /proc/421916/fdinfo/38 /proc/421916/fdinfo/39 /proc/421916/fdinfo/4 /proc/421916/fdinfo/41 /proc/421916/fdinfo/5 /proc/421916/fdinfo/6 /proc/421916/fdinfo/7 /proc/421916/fdinfo/8 /proc/421916/fdinfo/9 /proc/506988/fdinfo/0 /proc/506988/fdinfo/1 /proc/506988/fdinfo/2 /proc/506988/fdinfo/255 /proc/507068/fdinfo/0 /proc/507068/fdinfo/1 /proc/507068/fdinfo/2 /proc/507068/fdinfo/255 /proc/507120/fdinfo/0 /proc/507120/fdinfo/1 /proc/507120/fdinfo/2 /proc/507120/fdinfo/255 /proc/507197/fdinfo/0 /proc/507197/fdinfo/1 /proc/507197/fdinfo/2 /proc/507197/fdinfo/255 /proc/507197/fdinfo/3 /proc/507250/fdinfo/0 /proc/507250/fdinfo/1 /proc/507250/fdinfo/2 /proc/507250/fdinfo/255 /proc/507325/fdinfo/0 /proc/507325/fdinfo/1 /proc/507325/fdinfo/2 /proc/507325/fdinfo/255 /proc/507325/fdinfo/3 /proc/507375/fdinfo/0 /proc/507375/fdinfo/1 /proc/507375/fdinfo/2 /proc/507375/fdinfo/255 /proc/507466/fdinfo/0 /proc/507466/fdinfo/1 /proc/507466/fdinfo/2 /proc/507466/fdinfo/255 /proc/507516/fdinfo/0 /proc/507516/fdinfo/1 /proc/507516/fdinfo/2 /proc/507516/fdinfo/255 /proc/507586/fdinfo/0 /proc/507586/fdinfo/1 /proc/507586/fdinfo/2 /proc/507586/fdinfo/255 /proc/507657/fdinfo/0 /proc/507657/fdinfo/1 /proc/507657/fdinfo/2 /proc/507657/fdinfo/255 /proc/507718/fdinfo/0 /proc/507718/fdinfo/1 /proc/507718/fdinfo/2 /proc/507718/fdinfo/255 /proc/507833/fdinfo/0 /proc/507833/fdinfo/1 /proc/507833/fdinfo/2 /proc/507833/fdinfo/255 /proc/507913/fdinfo/0 /proc/507913/fdinfo/1 /proc/507913/fdinfo/2 /proc/507913/fdinfo/255 /proc/508031/fdinfo/0 /proc/508031/fdinfo/1 /proc/508031/fdinfo/2 /proc/508031/fdinfo/255 /proc/511403/fdinfo/0 /proc/511403/fdinfo/1 /proc/511403/fdinfo/10 /proc/511403/fdinfo/11 /proc/511403/fdinfo/12 /proc/511403/fdinfo/13 /proc/511403/fdinfo/14 /proc/511403/fdinfo/15 /proc/511403/fdinfo/16 /proc/511403/fdinfo/17 /proc/511403/fdinfo/18 /proc/511403/fdinfo/19 /proc/511403/fdinfo/2 /proc/511403/fdinfo/20 /proc/511403/fdinfo/21 /proc/511403/fdinfo/22 /proc/511403/fdinfo/23 /proc/511403/fdinfo/24 /proc/511403/fdinfo/25 /proc/511403/fdinfo/26 /proc/511403/fdinfo/27 /proc/511403/fdinfo/28 /proc/511403/fdinfo/29 /proc/511403/fdinfo/3 /proc/511403/fdinfo/30 /proc/511403/fdinfo/31 /proc/511403/fdinfo/32 /proc/511403/fdinfo/33 /proc/511403/fdinfo/34 /proc/511403/fdinfo/35 /proc/511403/fdinfo/36 /proc/511403/fdinfo/4 /proc/511403/fdinfo/5 /proc/511403/fdinfo/6 /proc/511403/fdinfo/7 /proc/511403/fdinfo/8 /proc/511403/fdinfo/9 /proc/511413/fdinfo/0 /proc/511413/fdinfo/1 /proc/511413/fdinfo/2 /proc/511413/fdinfo/255 /proc/512509/fdinfo/0 /proc/512509/fdinfo/1 /proc/512509/fdinfo/2 /proc/512562/fdinfo/0 /proc/512562/fdinfo/1 /proc/512562/fdinfo/2 /proc/512636/fdinfo/0 /proc/512636/fdinfo/1 /proc/512636/fdinfo/2 /proc/512766/fdinfo/0 /proc/512766/fdinfo/1 /proc/512766/fdinfo/2 /proc/512891/fdinfo/0 /proc/512891/fdinfo/1 /proc/512891/fdinfo/2 /proc/513089/fdinfo/0 /proc/513089/fdinfo/1 /proc/513089/fdinfo/2 /proc/513281/fdinfo/0 /proc/513281/fdinfo/1 /proc/513281/fdinfo/2 /proc/513678/fdinfo/0 /proc/513678/fdinfo/1 /proc/513678/fdinfo/2 /proc/514030/fdinfo/0 /proc/514030/fdinfo/1 /proc/514030/fdinfo/2 /proc/514431/fdinfo/0 /proc/514431/fdinfo/1 /proc/514431/fdinfo/2 /proc/514726/fdinfo/0 /proc/514726/fdinfo/1 /proc/514726/fdinfo/10 /proc/514726/fdinfo/11 /proc/514726/fdinfo/12 /proc/514726/fdinfo/13 /proc/514726/fdinfo/14 /proc/514726/fdinfo/15 /proc/514726/fdinfo/16 /proc/514726/fdinfo/17 /proc/514726/fdinfo/18 /proc/514726/fdinfo/19 /proc/514726/fdinfo/2 /proc/514726/fdinfo/20 /proc/514726/fdinfo/21 /proc/514726/fdinfo/22 /proc/514726/fdinfo/23 /proc/514726/fdinfo/24 /proc/514726/fdinfo/25 /proc/514726/fdinfo/26 /proc/514726/fdinfo/28 /proc/514726/fdinfo/29 /proc/514726/fdinfo/3 /proc/514726/fdinfo/30 /proc/514726/fdinfo/31 /proc/514726/fdinfo/32 /proc/514726/fdinfo/33 /proc/514726/fdinfo/34 /proc/514726/fdinfo/35 /proc/514726/fdinfo/36 /proc/514726/fdinfo/37 /proc/514726/fdinfo/38 /proc/514726/fdinfo/39 /proc/514726/fdinfo/4 /proc/514726/fdinfo/40 /proc/514726/fdinfo/41 /proc/514726/fdinfo/42 /proc/514726/fdinfo/43 /proc/514726/fdinfo/44 /proc/514726/fdinfo/45 /proc/514726/fdinfo/46 /proc/514726/fdinfo/5 /proc/514726/fdinfo/50 /proc/514726/fdinfo/52 /proc/514726/fdinfo/56 /proc/514726/fdinfo/58 /proc/514726/fdinfo/59 /proc/514726/fdinfo/6 /proc/514726/fdinfo/61 /proc/514726/fdinfo/63 /proc/514726/fdinfo/65 /proc/514726/fdinfo/66 /proc/514726/fdinfo/68 /proc/514726/fdinfo/7 /proc/514726/fdinfo/71 /proc/514726/fdinfo/72 /proc/514726/fdinfo/73 /proc/514726/fdinfo/74 /proc/514726/fdinfo/77 /proc/514726/fdinfo/78 /proc/514726/fdinfo/8 /proc/514726/fdinfo/82 /proc/514726/fdinfo/9 /proc/514854/fdinfo/0 /proc/514854/fdinfo/1 /proc/514854/fdinfo/2 /proc/515142/fdinfo/0 /proc/515142/fdinfo/1 /proc/515142/fdinfo/10 /proc/515142/fdinfo/11 /proc/515142/fdinfo/12 /proc/515142/fdinfo/13 /proc/515142/fdinfo/14 /proc/515142/fdinfo/15 /proc/515142/fdinfo/16 /proc/515142/fdinfo/17 /proc/515142/fdinfo/18 /proc/515142/fdinfo/19 /proc/515142/fdinfo/2 /proc/515142/fdinfo/21 /proc/515142/fdinfo/22 /proc/515142/fdinfo/23 /proc/515142/fdinfo/24 /proc/515142/fdinfo/25 /proc/515142/fdinfo/26 /proc/515142/fdinfo/27 /proc/515142/fdinfo/29 /proc/515142/fdinfo/3 /proc/515142/fdinfo/32 /proc/515142/fdinfo/33 /proc/515142/fdinfo/34 /proc/515142/fdinfo/38 /proc/515142/fdinfo/39 /proc/515142/fdinfo/4 /proc/515142/fdinfo/40 /proc/515142/fdinfo/41 /proc/515142/fdinfo/42 /proc/515142/fdinfo/43 /proc/515142/fdinfo/44 /proc/515142/fdinfo/47 /proc/515142/fdinfo/48 /proc/515142/fdinfo/5 /proc/515142/fdinfo/50 /proc/515142/fdinfo/51 /proc/515142/fdinfo/53 /proc/515142/fdinfo/55 /proc/515142/fdinfo/56 /proc/515142/fdinfo/58 /proc/515142/fdinfo/59 /proc/515142/fdinfo/6 /proc/515142/fdinfo/60 /proc/515142/fdinfo/62 /proc/515142/fdinfo/63 /proc/515142/fdinfo/65 /proc/515142/fdinfo/66 /proc/515142/fdinfo/69 /proc/515142/fdinfo/7 /proc/515142/fdinfo/8 /proc/515142/fdinfo/9 /proc/515268/fdinfo/0 /proc/515268/fdinfo/1 /proc/515268/fdinfo/2 /proc/515476/fdinfo/0 /proc/515476/fdinfo/1 /proc/515476/fdinfo/10 /proc/515476/fdinfo/11 /proc/515476/fdinfo/12 /proc/515476/fdinfo/13 /proc/515476/fdinfo/14 /proc/515476/fdinfo/15 /proc/515476/fdinfo/16 /proc/515476/fdinfo/17 /proc/515476/fdinfo/18 /proc/515476/fdinfo/19 /proc/515476/fdinfo/2 /proc/515476/fdinfo/20 /proc/515476/fdinfo/21 /proc/515476/fdinfo/22 /proc/515476/fdinfo/23 /proc/515476/fdinfo/24 /proc/515476/fdinfo/26 /proc/515476/fdinfo/29 /proc/515476/fdinfo/3 /proc/515476/fdinfo/30 /proc/515476/fdinfo/31 /proc/515476/fdinfo/32 /proc/515476/fdinfo/33 /proc/515476/fdinfo/34 /proc/515476/fdinfo/35 /proc/515476/fdinfo/36 /proc/515476/fdinfo/37 /proc/515476/fdinfo/38 /proc/515476/fdinfo/39 /proc/515476/fdinfo/4 /proc/515476/fdinfo/40 /proc/515476/fdinfo/41 /proc/515476/fdinfo/42 /proc/515476/fdinfo/43 /proc/515476/fdinfo/44 /proc/515476/fdinfo/45 /proc/515476/fdinfo/46 /proc/515476/fdinfo/47 /proc/515476/fdinfo/49 /proc/515476/fdinfo/5 /proc/515476/fdinfo/50 /proc/515476/fdinfo/51 /proc/515476/fdinfo/52 /proc/515476/fdinfo/53 /proc/515476/fdinfo/54 /proc/515476/fdinfo/55 /proc/515476/fdinfo/56 /proc/515476/fdinfo/57 /proc/515476/fdinfo/58 /proc/515476/fdinfo/59 /proc/515476/fdinfo/6 /proc/515476/fdinfo/62 /proc/515476/fdinfo/63 /proc/515476/fdinfo/64 /proc/515476/fdinfo/66 /proc/515476/fdinfo/67 /proc/515476/fdinfo/69 /proc/515476/fdinfo/7 /proc/515476/fdinfo/70 /proc/515476/fdinfo/73 /proc/515476/fdinfo/8 /proc/515476/fdinfo/9 /proc/515676/fdinfo/0 /proc/515676/fdinfo/1 /proc/515676/fdinfo/2 /proc/516004/fdinfo/0 /proc/516004/fdinfo/1 /proc/516004/fdinfo/2 /proc/516308/fdinfo/0 /proc/516308/fdinfo/1 /proc/516308/fdinfo/10 /proc/516308/fdinfo/11 /proc/516308/fdinfo/12 /proc/516308/fdinfo/13 /proc/516308/fdinfo/14 /proc/516308/fdinfo/15 /proc/516308/fdinfo/16 /proc/516308/fdinfo/17 /proc/516308/fdinfo/18 /proc/516308/fdinfo/19 /proc/516308/fdinfo/2 /proc/516308/fdinfo/20 /proc/516308/fdinfo/21 /proc/516308/fdinfo/22 /proc/516308/fdinfo/23 /proc/516308/fdinfo/24 /proc/516308/fdinfo/25 /proc/516308/fdinfo/26 /proc/516308/fdinfo/27 /proc/516308/fdinfo/28 /proc/516308/fdinfo/29 /proc/516308/fdinfo/3 /proc/516308/fdinfo/30 /proc/516308/fdinfo/31 /proc/516308/fdinfo/32 /proc/516308/fdinfo/33 /proc/516308/fdinfo/34 /proc/516308/fdinfo/35 /proc/516308/fdinfo/36 /proc/516308/fdinfo/37 /proc/516308/fdinfo/38 /proc/516308/fdinfo/39 /proc/516308/fdinfo/4 /proc/516308/fdinfo/40 /proc/516308/fdinfo/41 /proc/516308/fdinfo/42 /proc/516308/fdinfo/44 /proc/516308/fdinfo/45 /proc/516308/fdinfo/46 /proc/516308/fdinfo/47 /proc/516308/fdinfo/48 /proc/516308/fdinfo/49 /proc/516308/fdinfo/5 /proc/516308/fdinfo/52 /proc/516308/fdinfo/56 /proc/516308/fdinfo/58 /proc/516308/fdinfo/6 /proc/516308/fdinfo/60 /proc/516308/fdinfo/61 /proc/516308/fdinfo/62 /proc/516308/fdinfo/63 /proc/516308/fdinfo/66 /proc/516308/fdinfo/67 /proc/516308/fdinfo/69 /proc/516308/fdinfo/7 /proc/516308/fdinfo/71 /proc/516308/fdinfo/72 /proc/516308/fdinfo/8 /proc/516308/fdinfo/9 /proc/516332/fdinfo/0 /proc/516332/fdinfo/1 /proc/516332/fdinfo/10 /proc/516332/fdinfo/11 /proc/516332/fdinfo/12 /proc/516332/fdinfo/13 /proc/516332/fdinfo/14 /proc/516332/fdinfo/15 /proc/516332/fdinfo/16 /proc/516332/fdinfo/17 /proc/516332/fdinfo/18 /proc/516332/fdinfo/19 /proc/516332/fdinfo/2 /proc/516332/fdinfo/21 /proc/516332/fdinfo/22 /proc/516332/fdinfo/23 /proc/516332/fdinfo/24 /proc/516332/fdinfo/25 /proc/516332/fdinfo/26 /proc/516332/fdinfo/27 /proc/516332/fdinfo/28 /proc/516332/fdinfo/29 /proc/516332/fdinfo/3 /proc/516332/fdinfo/30 /proc/516332/fdinfo/31 /proc/516332/fdinfo/32 /proc/516332/fdinfo/33 /proc/516332/fdinfo/34 /proc/516332/fdinfo/35 /proc/516332/fdinfo/36 /proc/516332/fdinfo/37 /proc/516332/fdinfo/38 /proc/516332/fdinfo/39 /proc/516332/fdinfo/4 /proc/516332/fdinfo/40 /proc/516332/fdinfo/41 /proc/516332/fdinfo/42 /proc/516332/fdinfo/43 /proc/516332/fdinfo/44 /proc/516332/fdinfo/45 /proc/516332/fdinfo/47 /proc/516332/fdinfo/49 /proc/516332/fdinfo/5 /proc/516332/fdinfo/50 /proc/516332/fdinfo/51 /proc/516332/fdinfo/52 /proc/516332/fdinfo/54 /proc/516332/fdinfo/55 /proc/516332/fdinfo/56 /proc/516332/fdinfo/57 /proc/516332/fdinfo/59 /proc/516332/fdinfo/6 /proc/516332/fdinfo/60 /proc/516332/fdinfo/61 /proc/516332/fdinfo/64 /proc/516332/fdinfo/67 /proc/516332/fdinfo/69 /proc/516332/fdinfo/7 /proc/516332/fdinfo/8 /proc/516332/fdinfo/9 /proc/516528/fdinfo/0 /proc/516528/fdinfo/1 /proc/516528/fdinfo/2 /proc/516903/fdinfo/0 /proc/516903/fdinfo/1 /proc/516903/fdinfo/10 /proc/516903/fdinfo/11 /proc/516903/fdinfo/12 /proc/516903/fdinfo/13 /proc/516903/fdinfo/14 /proc/516903/fdinfo/15 /proc/516903/fdinfo/16 /proc/516903/fdinfo/17 /proc/516903/fdinfo/18 /proc/516903/fdinfo/19 /proc/516903/fdinfo/2 /proc/516903/fdinfo/20 /proc/516903/fdinfo/21 /proc/516903/fdinfo/22 /proc/516903/fdinfo/23 /proc/516903/fdinfo/24 /proc/516903/fdinfo/26 /proc/516903/fdinfo/27 /proc/516903/fdinfo/28 /proc/516903/fdinfo/29 /proc/516903/fdinfo/3 /proc/516903/fdinfo/30 /proc/516903/fdinfo/31 /proc/516903/fdinfo/32 /proc/516903/fdinfo/33 /proc/516903/fdinfo/34 /proc/516903/fdinfo/35 /proc/516903/fdinfo/36 /proc/516903/fdinfo/37 /proc/516903/fdinfo/38 /proc/516903/fdinfo/39 /proc/516903/fdinfo/4 /proc/516903/fdinfo/40 /proc/516903/fdinfo/41 /proc/516903/fdinfo/42 /proc/516903/fdinfo/43 /proc/516903/fdinfo/44 /proc/516903/fdinfo/45 /proc/516903/fdinfo/46 /proc/516903/fdinfo/47 /proc/516903/fdinfo/48 /proc/516903/fdinfo/49 /proc/516903/fdinfo/5 /proc/516903/fdinfo/50 /proc/516903/fdinfo/52 /proc/516903/fdinfo/53 /proc/516903/fdinfo/55 /proc/516903/fdinfo/56 /proc/516903/fdinfo/57 /proc/516903/fdinfo/6 /proc/516903/fdinfo/60 /proc/516903/fdinfo/62 /proc/516903/fdinfo/63 /proc/516903/fdinfo/64 /proc/516903/fdinfo/7 /proc/516903/fdinfo/8 /proc/516903/fdinfo/81 /proc/516903/fdinfo/9 /proc/517291/fdinfo/0 /proc/517291/fdinfo/1 /proc/517291/fdinfo/10 /proc/517291/fdinfo/11 /proc/517291/fdinfo/12 /proc/517291/fdinfo/13 /proc/517291/fdinfo/14 /proc/517291/fdinfo/15 /proc/517291/fdinfo/16 /proc/517291/fdinfo/17 /proc/517291/fdinfo/18 /proc/517291/fdinfo/19 /proc/517291/fdinfo/2 /proc/517291/fdinfo/20 /proc/517291/fdinfo/21 /proc/517291/fdinfo/22 /proc/517291/fdinfo/3 /proc/517291/fdinfo/30 /proc/517291/fdinfo/31 /proc/517291/fdinfo/32 /proc/517291/fdinfo/33 /proc/517291/fdinfo/34 /proc/517291/fdinfo/35 /proc/517291/fdinfo/36 /proc/517291/fdinfo/37 /proc/517291/fdinfo/38 /proc/517291/fdinfo/39 /proc/517291/fdinfo/4 /proc/517291/fdinfo/5 /proc/517291/fdinfo/50 /proc/517291/fdinfo/54 /proc/517291/fdinfo/55 /proc/517291/fdinfo/58 /proc/517291/fdinfo/6 /proc/517291/fdinfo/60 /proc/517291/fdinfo/7 /proc/517291/fdinfo/8 /proc/517291/fdinfo/9 /proc/518417/fdinfo/0 /proc/518417/fdinfo/1 /proc/518417/fdinfo/10 /proc/518417/fdinfo/11 /proc/518417/fdinfo/12 /proc/518417/fdinfo/13 /proc/518417/fdinfo/14 /proc/518417/fdinfo/15 /proc/518417/fdinfo/16 /proc/518417/fdinfo/17 /proc/518417/fdinfo/18 /proc/518417/fdinfo/19 /proc/518417/fdinfo/2 /proc/518417/fdinfo/20 /proc/518417/fdinfo/21 /proc/518417/fdinfo/22 /proc/518417/fdinfo/23 /proc/518417/fdinfo/24 /proc/518417/fdinfo/25 /proc/518417/fdinfo/26 /proc/518417/fdinfo/27 /proc/518417/fdinfo/28 /proc/518417/fdinfo/29 /proc/518417/fdinfo/3 /proc/518417/fdinfo/30 /proc/518417
  1112212: 0 bash bash /home/mesh-home/.local/bin/mesh-supervise
  1112216: 0 bash bash /home/mesh-home/.local/bin/mesh-home-state --test
  1112218: 4123168608 tr tr -d \n
  1112227: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-land --apply mesh-land: add focused test artifact
  1112228: 4123168608 awk awk -F \t { print $1 }
  1112233: 0 timeout timeout 12 /home/mesh-home/.local/bin/mesh-tell --test
  1112241: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-room-reflex --test
  1112246: 3 bash bash /home/mesh-home/.local/bin/mesh-generate --run-with-test-files
  1112257: 3 timeout timeout 12 /home/mesh-home/.local/bin/mesh-synergy --test
  1112261: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-hw-fault-watch
  1112264: 0 sleep sleep 8
  1112277: 4123168608 ollama ollama run qwen2.5:3b --think=false --format json Ты — фильтр пробуждения для голосового ассистента по имени Миша (звательные формы: Миша, Миш, Мишань). В комнате идёт живой разговор; микрофон также ловит галлюцинации распознавания речи на тишине. Ниже последние реплики из комнаты по порядку. Реши ТОЛЬКО про ПОСЛЕДНЮЮ реплику, используя предыдущие как контекст. ГЛАВНОЕ ПРАВИЛО: если в ПОСЛЕДНЕЙ реплике есть звательное обращение к Мише (Миша/Миш/Мишань — часто выделено запятой: "Миш,", "Ну вот, Миш," "Миша,") — это ВСЕГДА {"wake":true}, даже если дальше идёт жалоба, ремарка или незаконченная мысль. При любом сомнении отвечай {"wake":true} — пропущенное обращение хуже лишнего. Ответь {"wake":false} ТОЛЬКО когда обращения к Мише в последней реплике нет: люди говорят между собой; о Мише в ТРЕТЬЕМ лице без обращения к нему ("спроси у Миши", "Миша вчера чинил", "как думаешь, Миша прав"); слова, лишь ПОХОЖИЕ на имя (мишка, мишура, Мишель); бессмысленный обрывок STT на тишине. Примеры: Разговор: ПОСЛЕДНЯЯ: "Миша, ты нас слышишь?" -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Ну вот, Миш, плохо слушать, всё прерывается" -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Миш, кстати, а ты видишь..." -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Время" -> {"wake":false} Разговор: "Смотри какие мишки на витрине" ПОСЛЕДНЯЯ: "Да, милые, купим?" -> {"wake":false} Разговор: ПОСЛЕДНЯЯ: "Как думаешь, Миша был прав вчера?" -> {"wake":false} Разговор: ПОСЛЕДНЯЯ: "Повесь мишуру повыше" -> {"wake":false} Разговор:  ПОСЛЕДНЯЯ: "КОНЕЦ"
  1112286: 0 python3 python3 -c import sys,json; print(json.load(sys.stdin).get("state",""))
  1112296: 0 ffmpeg ffmpeg -v error -y -i /tmp/tmp.NTTk7NXyOO/td.mesh-music-fanout/tmp.nWubsUX14p/tmp.x4JQQOPr36/work/.cap-stub.raw.wav -af loudnorm=I=-16:TP=-1 -ac 1 -ar 22050 /tmp/tmp.NTTk7NXyOO/td.mesh-music-fanout/tmp.nWubsUX14p/tmp.x4JQQOPr36/work/records-stub/.pending.wav
  1112307: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-revive --check
doctor pid=952479 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  952479: gone
doctor pid=953694 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  953694: gone
doctor pid=958551 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  958551: 70 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
doctor pid=961127 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  961127: 69 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1086464: 24 timeout timeout 25 /home/mesh-home/.local/bin/mesh-fitness --test
  1086766: 24 bash bash /home/mesh-home/.local/bin/mesh-fitness --test
  1110773: 0 timeout timeout 1 /tmp/tmp.NTTk7NXyOO/td.mesh-fitness/tmp.aF8EIGj1jX/scripts/mesh-truehang --test
  1110815: 0 bash bash /home/mesh-home/.local/bin/mesh-fitness --test
  1110876: 0 bash bash /tmp/tmp.NTTk7NXyOO/td.mesh-fitness/tmp.aF8EIGj1jX/scripts/mesh-truehang --test
doctor pid=962788 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  962788: 69 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1087614: 24 timeout timeout 25 /home/mesh-home/.local/bin/mesh-forage --test
  1087712: 24 bash bash /home/mesh-home/.local/bin/mesh-forage --test
  1088100: 24 bash bash /home/mesh-home/.local/bin/mesh-forage --test
  1089279: 24 bash bash /home/mesh-home/.local/bin/mesh-forage --json
  1091153: 23 bash bash /home/mesh-home/.local/bin/mesh-forage --json
  1091196: 23 bash bash /home/mesh-home/.local/bin/mesh-forage --json
  1091268: 23 bash bash /home/mesh-home/.local/bin/mesh-promises --json
  1097564: 22 python3 python3 - json /home/mesh-home/.mesh/chat.log 2026-09-14T03:25:03Z 24 6 1
doctor pid=963655 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  963655: 70 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1088139: 24 timeout timeout 25 /home/mesh-home/.local/bin/mesh-fsnotify --test
  1088311: 24 bash bash /home/mesh-home/.local/bin/mesh-fsnotify --test
doctor pid=964028 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  964028: 70 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
doctor pid=965887 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  965887: 70 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1091052: 24 timeout timeout 25 /home/mesh-home/.local/bin/mesh-generate --test
  1091111: 24 bash bash /home/mesh-home/.local/bin/mesh-generate --test
  1114934: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-generate --run-with-test-files
  1115204: 4123168608 bash [bash] <defunct>
doctor pid=971756 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  971756: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1097200: 23 timeout timeout 25 /home/mesh-home/.local/bin/mesh-gmail-note3 --test
  1097234: 23 python3 python3 /home/mesh-home/.local/bin/mesh-gmail-note3 --test
  1111508: 5 adb adb exec-out su -c 'cat /data/data/com.google.android.gm/databases/bigTopDataDB.1023405767'
doctor pid=973768 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  973768: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1099369: 23 timeout timeout 25 /home/mesh-home/.local/bin/mesh-guardian --test
  1099439: 23 bash bash /home/mesh-home/.local/bin/mesh-guardian --test
  1110457: 2 bash bash /home/mesh-home/.local/bin/mesh-guardian
  1110528: 2 bash bash /home/mesh-home/.local/bin/mesh-guardian
  1110530: 2 grep grep -q ok
  1110671: 2 timeout timeout 14 ssh -n -o BatchMode=yes -o ConnectTimeout=6 nonexistent-host-127-0-99-253.local echo ok
  1110764: 2 ssh ssh -n -o BatchMode=yes -o ConnectTimeout=6 nonexistent-host-127-0-99-253.local echo ok
  1111750: 2 bash bash /home/mesh-home/.local/bin/mesh-guardian --test
  1111767: 2 grep grep -q telegram organ keeper ACTIVE
  1111944: 2 timeout timeout 30 bash /home/mesh-home/.local/bin/mesh-guardian
  1112038: 2 bash bash /home/mesh-home/.local/bin/mesh-guardian
doctor pid=973921 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  973921: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1100051: 23 timeout timeout 25 /home/mesh-home/.local/bin/mesh-guitar-watch --test
  1100087: 23 bash bash /home/mesh-home/.local/bin/mesh-guitar-watch --test
  1100559: 23 bash bash /home/mesh-home/.local/bin/mesh-guitar-watch --test
  1110588: 18 bash bash /home/mesh-home/.local/bin/mesh-guitar-watch --test
  1110642: 18 bash bash /home/mesh-home/.local/bin/mesh-guitar-watch --test
  1110655: 18 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-guitar-watch/tmp.TKjWoEnDBY/tmp.S7SkKiV87Y/tone.wav
  1111218: 18 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-guitar-watch/tmp.TKjWoEnDBY/tmp.S7SkKiV87Y/tone.wav
  1111240: 18 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-guitar-watch/tmp.TKjWoEnDBY/tmp.S7SkKiV87Y/tone.wav
  1111242: 18 grep grep ^MEASURE
  1111277: 18 python /home/mesh-home/grainneukeln/.venv/bin/python - /tmp/tmp.NTTk7NXyOO/td.mesh-guitar-watch/tmp.TKjWoEnDBY/tmp.S7SkKiV87Y/tone.wav 0,12,3 0.006 measure
doctor pid=974193 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  974193: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1100180: 23 timeout timeout 25 /home/mesh-home/.local/bin/mesh-handoff --test
  1100235: 23 bash bash /home/mesh-home/.local/bin/mesh-handoff --test
doctor pid=976228 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  976228: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1102266: 23 timeout timeout 25 /home/mesh-home/.local/bin/mesh-heartbeat --test
  1102332: 23 bash bash /home/mesh-home/.local/bin/mesh-heartbeat --test
  1110272: 12 timeout timeout 40 bash /home/mesh-home/.local/bin/mesh-heartbeat --rejoin
  1110482: 12 bash bash /home/mesh-home/.local/bin/mesh-heartbeat --rejoin
  1110879: 12 bash bash /home/mesh-home/.local/bin/mesh-heartbeat --rejoin
  1111760: 12 bash bash /home/mesh-home/.local/bin/mesh-heartbeat --test
  1118285: 0 bash bash /home/mesh-home/.local/bin/mesh-heartbeat --rejoin
  1118301: 0 journalctl journalctl -k -b 0 -p warning --no-pager
  1118308: 0 tail tail -40
doctor pid=977271 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  977271: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1103764: 22 timeout timeout 25 /home/mesh-home/.local/bin/mesh-hh-drive --test
  1103792: 22 bash bash /home/mesh-home/.local/bin/mesh-hh-drive --test
  1119183: 0 sleep sleep 2
doctor pid=977808 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  977808: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1104232: 23 timeout timeout 25 /home/mesh-home/.local/bin/mesh-hire-scan --test
  1104328: 23 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --test
  1121540: 0 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --test
  1121625: 0 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --test
  1121642: 0 gh gh api repos/tenstorrent/tt-metal/contents/.github/pull_request_template.md
doctor pid=978071 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  978071: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1104503: 23 timeout timeout 25 /home/mesh-home/.local/bin/mesh-hire-submit --test
  1104558: 23 bash bash /home/mesh-home/.local/bin/mesh-hire-submit --test
  1105781: 23 bash bash /home/mesh-home/.local/bin/mesh-hire-submit --test
  1105829: 23 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --repo trovu/trovu
  1117438: 1 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --repo trovu/trovu
  1117443: 1 bash bash /home/mesh-home/.local/bin/mesh-hire-scan --repo trovu/trovu
  1117449: 1 gh gh api repos/trovu/trovu/contents/AGENTS.md
doctor pid=979572 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  979572: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1106291: 23 timeout timeout 25 /home/mesh-home/.local/bin/mesh-homeostasis --test
  1106348: 23 bash bash /home/mesh-home/.local/bin/mesh-homeostasis --test
doctor pid=979986 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  979986: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1106811: 23 timeout timeout 25 /home/mesh-home/.local/bin/mesh-home-state --test
  1106886: 23 bash bash /home/mesh-home/.local/bin/mesh-home-state --test
  1128453: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-home-state --test
  1128538: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-home-state --json
doctor pid=981059 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  981059: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1108042: 23 timeout timeout 25 /home/mesh-home/.local/bin/mesh-hw-fault-watch --test
  1108080: 23 bash bash /home/mesh-home/.local/bin/mesh-hw-fault-watch --test
  1127383: 0 bash bash /home/mesh-home/.local/bin/mesh-hw-fault-watch --test
  1127450: 0 bash bash /home/mesh-home/.local/bin/mesh-hw-fault-watch --legs
doctor pid=981298 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  981298: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1108298: 23 timeout timeout 25 /home/mesh-home/.local/bin/mesh-hw-health --test
  1108312: 23 bash bash /home/mesh-home/.local/bin/mesh-hw-health --test
  1110922: 20 bash bash /home/mesh-home/.local/bin/mesh-hw-health
  1111016: 17 bash bash /home/mesh-home/.local/bin/mesh-hw-health
doctor pid=982041 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  982041: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1109172: 23 timeout timeout 25 /home/mesh-home/.local/bin/mesh-ideate --test
  1109287: 23 bash bash /home/mesh-home/.local/bin/mesh-ideate --test
  1110330: 21 bash bash /home/mesh-home/.local/bin/mesh-ideate --test
  1110952: 21 bash bash /home/mesh-home/.local/bin/mesh-ideate --test
doctor pid=985556 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  985556: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110821: 23 timeout timeout 25 /home/mesh-home/.local/bin/mesh-imac-wifi --test
  1110859: 23 bash bash /home/mesh-home/.local/bin/mesh-imac-wifi --test
  1114681: 4 bash bash /home/mesh-home/.local/bin/mesh-imac-wifi --test
  1114699: 4 bash bash /home/mesh-home/.local/bin/mesh-imac-wifi --test
  1114712: 4 timeout timeout 8 ssh -o BatchMode=yes -o ConnectTimeout=5 ilya@192.168.8.214 true
  1114806: 4 ssh ssh -o BatchMode=yes -o ConnectTimeout=5 ilya@192.168.8.214 true
doctor pid=987046 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  987046: 68 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110295: 7 bash bash /home/mesh-home/.local/bin/mesh-interruptibility --test
  1110389: 22 timeout timeout 25 /home/mesh-home/.local/bin/mesh-interruptibility --test
  1110554: 22 bash bash /home/mesh-home/.local/bin/mesh-interruptibility --test
doctor pid=990627 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  990627: 67 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110982: 21 timeout timeout 25 /home/mesh-home/.local/bin/mesh-job-apply --test
  1111073: 21 python3 python3 /home/mesh-home/.local/bin/mesh-job-apply --test
  1111245: 8 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-job-apply --reasons
  1134077: 0 python3 python3 /home/mesh-home/.local/bin/mesh-job-answers --covered hh:135161211
doctor pid=992264 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  992264: 67 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110310: 8 bash bash /home/mesh-home/.local/bin/mesh-job-calls --test
  1110382: 8 bash bash /home/mesh-home/.local/bin/mesh-job-calls --test
  1110484: 8 timeout timeout 10 mesh-phone-ip
  1110686: 8 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1111018: 22 timeout timeout 25 /home/mesh-home/.local/bin/mesh-job-calls --test
  1111087: 22 bash bash /home/mesh-home/.local/bin/mesh-job-calls --test
  1126401: 2 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1126493: 2 timeout timeout 4 ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@100.103.99.16 echo ok
  1126645: 2 ssh ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@100.103.99.16 echo ok
doctor pid=992606 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  992606: 67 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111195: 21 timeout timeout 25 /home/mesh-home/.local/bin/mesh-job-chatwatch --test
  1111253: 21 python3 python3 /home/mesh-home/.local/bin/mesh-job-chatwatch --test
  1118294: 4 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-job-chatwatch
doctor pid=994370 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  994370: 67 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110486: 21 timeout timeout 25 /home/mesh-home/.local/bin/mesh-job-mail --test
  1110545: 21 python3 python3 /home/mesh-home/.local/bin/mesh-job-mail --test
  1127277: 2 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-job-mail --lanes --json
  1132761: 1 python3 python3 /home/mesh-home/.local/bin/mesh-cron-catchup --boot-windows
  1135859: 0 journalctl journalctl --list-boots -o json
doctor pid=995501 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  995501: 67 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110792: 21 timeout timeout 25 /home/mesh-home/.local/bin/mesh-job-scan --test
  1110926: 21 python3 python3 /home/mesh-home/.local/bin/mesh-job-scan --test
doctor pid=997211 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  997211: 66 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110417: 21 timeout timeout 25 /home/mesh-home/.local/bin/mesh-job-track --test
  1110519: 21 python3 python3 /home/mesh-home/.local/bin/mesh-job-track --test
doctor pid=997529 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  997529: 67 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110246: 21 timeout timeout 25 /home/mesh-home/.local/bin/mesh-journal-watch --test
  1110328: 21 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --test
  1110578: 16 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --test
  1110641: 16 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --scope
  1111194: 15 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --scope
  1111205: 15 bash bash /home/mesh-home/.local/bin/mesh-journal-watch --scope
  1111207: 15 awk awk -F\t -v idcap=4 -v sfloor=0.90 -v minsig=8 -v fminsig=4        # FAMILY SKELETON — the message with every VARIABLE token dropped: a family is the set of signatures       # that are the same sentence differing only where the message carries a value. Two properties earn it:       #   - it is computed from the RAW message, NEVER the normalized one. After normalize() a digit-derived       #     N is indistinguishable from a literal N (`Network`, `HNC`), so keying on the normalized text       #     would drop real words and merge unrelated messages. The raw still has actual digits.       #   - it drops variable tokens rather than taking a leading PREFIX. A prefix rule was tried first and       #     measured FALSE against the live journal here (2026-08-28): every rtw_8822bu 1-3:1.0 line begins       #     with a digit-bearing word, so seven genuinely DIFFERENT driver faults (leave idle state failed,       #     h2c queue mismatch, failed to configure mac, ...) all landed in one catch-all bucket and were       #     reported as a storm. They are seven real faults, correctly given seven signatures. Under the       #     skeleton they have seven distinct skeletons and no family fires.       function famkey(ident, raw,   i, w, nw, out) {         nw = split(raw, w, /[ \t]+/); out = ""         for (i=1; i<=nw; i++) {           if (w[i] ~ /[0-9]/) continue                 # carries a value -> not part of the skeleton           out = (out=="" ? w[i] : out " " w[i])         }         if (out == "") out = "<all-variable>"         return ident "|||" out       }       {         sig=$1; raw=$2; total++         n[sig]++         k=sig SUBSEP raw; c[k]++         if (c[k]==1) d[sig]++          # distinct raw messages absorbed by this signature         if (c[k]==2) r[sig]++          # ... of which RECUR (a stable, re-visited value, not a fresh counter)         if (!(sig in fam)) fam[sig] = famkey(substr(sig, 1, index(sig,"|||")-1), raw)       }       END{         if (total==0) { print "NO-DATA"; exit }         sigs=0; single=0; degen=0; idfold=0         for (s in n) {           sigs++           if (n[s]==1) single++           f=fam[s]; fs[f]++; if (n[s]==1) fsingle[f]++           body=substr(s, index(s,"|||")+3)           # DEGENERATE: a signature body with no alphabetic character discriminates NOTHING — every fault           # that lands in it after the first is silent forever.           if (body !~ /[A-Za-z]/) {             degen++             printf "  DEGENERATE     n=%-5d raws=%-3d  [%s]  <- no alphabetic content: absorbs anything\n", n[s], d[s], s | "sort"             continue           }           # IDENTITY-FOLD: >=2 distinct raws, a SMALL set (<=idcap), and >=2 of them RECUR. A small           # re-visited value set is an enumerable identity (device/port/instance index), not an unbounded           # counter — so normalize() folded away WHICH thing faulted, and only the first ever alerted.           if (d[s]>=2 && d[s]<=idcap && r[s]>=2) {             idfold++             printf "  IDENTITY-FOLD  n=%-5d raws=%-3d  [%s]  <- %d distinct raws, %d recurring: an enumerable identity was folded\n", n[s], d[s], s, d[s], r[s] | "sort"           }         }         # FAMILY-STORM — the per-family twin of the global singleton rate (2026-08-28, same task). ONE         # global rate over the whole alphabet is a MAJORITY VOTE: the UUID family above was storming five         # signatures wide beside ~26 healthy repeating ones, and 5/31 = 0.16 can never reach SFLOOR 0.90,         # so the guard shipped for exactly this pole could not see the pole in its own normalizer. A rate         # computed over signatures SHARING A STEM lets one storming family trip it while the rest is         # healthy. It is an ADDED arm, not a replacement: an alphabet that is globally all-singleton has         # every family at size 1, below fminsig, so a pure per-family rule would go BLIND to the shape         # case (12) asserts. Report-only, like everything in --scope — it names a stem whose residue never         # converges and leaves it to a human to say whether that residue is identity or noise, which is         # the one question the normalizer structurally cannot answer about itself.         storm=0; fams=0         for (f in fs) {           fams++           # the all-variable bucket is a CATCH-ALL, not a family — it holds messages that share no fixed           # text at all, so a high singleton rate in it says nothing about any one stem. Excluded loudly           # rather than silently: it is counted in families= and never in family-storm=.           if (f ~ /\|\|\|<all-variable>$/) continue           if (fs[f] >= fminsig && (fsingle[f]+0)/fs[f] >= sfloor) {             storm++             printf "  FAMILY-STORM   sigs=%-5d singletons=%-3d  [%s]  <- this stem mints a fresh signature nearly every time: normalize() leaves a per-event residue here\n", fs[f], fsingle[f]+0, f | "sort"           }         }         close("sort")         rho = 1 - (sigs/total)         srate = single/sigs         printf "records=%d  signatures=%d  compression=%.3f  singleton-rate=%.2f  degenerate=%d  identity-fold=%d  families=%d  family-storm=%d\n", total, sigs, rho, srate, degen, idfold, fams, storm         gpart = (sigs>=minsig && srate>=sfloor)         fpart = (storm>0)         if (degen>0 || idfold>0) { verdict="OVER-COMPRESSED"; rc=3 }         else if (gpart || fpart) { verdict="OVER-PARTICULARIZED"; rc=4 }         else { verdict="BALANCED"; rc=0 }         # WHICH arm fired is part of the verdict — the two have different remedies (a global storm means         # the normalizer is too fine everywhere; a family storm means one stem carries an unfolded residue).         why = ""         if (gpart) why = sprintf("global singleton-rate %.2f >= %s over %d signatures", srate, sfloor, sigs)         if (fpart) why = why (gpart ? "; " : "") sprintf("%d storming famil%s (>=%d sigs each, singleton-rate >= %s)", storm, (storm==1?"y":"ies"), fminsig, sfloor)         # both poles can hold at once; the silent pole wins the verdict (a blind sense outranks a loud one)         also=""         if (rc==4) also=" (" why ")"         if (rc==3 && (gpart || fpart)) also=" (+ over-particularized: " why ")"         print "scope: " verdict also         exit rc       }
  1111238: 15 journalctl journalctl -b 0 -p err -o json
  1111241: 15 jq jq -r ((.SYSLOG_IDENTIFIER // ._COMM // "kernel")|tostring) + "|||" + ((.MESSAGE // "")|tostring)
doctor pid=1000664 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1000664: 66 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110303: 21 bash bash /home/mesh-home/.local/bin/mesh-labor --test
  1110462: 16 bash bash /home/mesh-home/.local/bin/mesh-labor --feed
  1110553: 16 bash bash /home/mesh-home/.local/bin/mesh-ledger --price-window 5
  1110597: 16 bash bash /home/mesh-home/.local/bin/mesh-spend --tokens --json
  1110598: 16 bash bash /home/mesh-home/.local/bin/mesh-ledger --price-window 5
  1111052: 19 bash bash /home/mesh-home/.local/bin/mesh-labor --feed
  1111061: 21 timeout timeout 25 /home/mesh-home/.local/bin/mesh-labor --test
  1111444: 16 python3 python3 /tmp/tmp.NTTk7NXyOO/td.mesh-labor/mesh-ledger.IHT1ewyy/tmp.Ozed9NAobV 2026-09-14 2026-09-13T22:25:17Z 2026-09-14T03:25:17Z /tmp/tmp.NTTk7NXyOO/td.mesh-labor/mesh-ledger.IHT1ewyy/tmp.H4SRttsJY5
  1111511: 16 python3 python3 - /tmp/tmp.NTTk7NXyOO/td.mesh-labor/tmp.lcMkr7WhnP/task-feed/spend.log /home/mesh-home/.mesh/tick.log 5 --tokens /tmp/tmp.NTTk7NXyOO/td.mesh-labor/tmp.VsZYPXqc4G /home/mesh-home/.claude/projects 1
  1111607: 16 bash bash /home/mesh-home/.local/bin/mesh-labor --feed
doctor pid=1001934 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1001934: 66 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111983: 21 timeout timeout 25 /home/mesh-home/.local/bin/mesh-land --test
  1112040: 21 bash bash /home/mesh-home/.local/bin/mesh-land --test
  1139168: 0 bash bash /home/mesh-home/.local/bin/mesh-land --apply mesh-land: add focused test artifact
  1139978: 0 bash bash /home/mesh-home/.local/bin/mesh-land --apply mesh-land: add focused test artifact
  1140021: 0 bash bash /home/mesh-home/.local/bin/mesh-land --apply mesh-land: add focused test artifact
  1140103: 0 bash bash /home/mesh-home/.local/bin/mesh-land --apply mesh-land: add focused test artifact
  1140104: 0 awk awk -F \t { print $1 }
  1140248: 0 python3 python3 /home/mesh-home/lte-workstation/scripts/mesh-manifest --check
doctor pid=1003970 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1003970: 66 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110900: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-lan-newdevice --test
  1111060: 20 bash bash /home/mesh-home/.local/bin/mesh-lan-newdevice --test
  1132214: 2 bash bash /home/mesh-home/.local/bin/mesh-lan-newdevice --allow aa:bb:cc:dd:ee:03
  1132428: 2 bash bash /home/mesh-home/.local/bin/mesh-lan-newdevice --allow aa:bb:cc:dd:ee:03
  1132453: 2 bash bash /home/mesh-home/.local/bin/mesh-peer-addr router
  1138611: 1 ping ping -c 1 -W 2 192.168.8.1
doctor pid=1004502 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1004502: 66 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110766: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-lan-presence --test
  1110872: 20 bash bash /home/mesh-home/.local/bin/mesh-lan-presence --test
  1128749: 3 ssh ssh -o ConnectTimeout=6 -o StrictHostKeyChecking=accept-new -o BatchMode=yes root@192.168.8.1 true
doctor pid=1004983 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1004983: 66 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110878: 21 timeout timeout 25 /home/mesh-home/.local/bin/mesh-leadlag --test
  1110939: 21 bash bash /home/mesh-home/.local/bin/mesh-leadlag --test
  1123133: 5 bash bash /home/mesh-home/.local/bin/mesh-leadlag --test
  1123172: 5 python3 python3 -
doctor pid=1006080 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1006080: 66 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111004: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-ledger --test
  1111173: 19 bash bash /home/mesh-home/.local/bin/mesh-ledger --test
  1143377: 0 bash bash /home/mesh-home/.local/bin/mesh-ledger --check
  1146680: 4123168608 python3 python3 - /tmp/tmp.NTTk7NXyOO/td.mesh-ledger/mesh-ledger.asQBcgL6/tmp.C27NXOH7Ia/alghome2/.mesh/ledger/2026.journal
doctor pid=1009749 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1009749: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110497: 19 bash bash /home/mesh-home/.local/bin/mesh-load-attrib --test
  1110529: 19 bash bash /home/mesh-home/.local/bin/mesh-load-attrib --test
  1110791: 19 bash bash /home/mesh-home/.local/bin/mesh-stress --json
  1111396: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-load-attrib --test
  1111530: 20 bash bash /home/mesh-home/.local/bin/mesh-load-attrib --test
doctor pid=1010069 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1010069: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110592: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-load-audit --test
  1110732: 20 bash bash /home/mesh-home/.local/bin/mesh-load-audit --test
doctor pid=1010704 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1010704: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110351: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-load-gate --test
  1110429: 20 bash bash /home/mesh-home/.local/bin/mesh-load-gate --test
doctor pid=1012230 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1012230: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110362: 20 bash bash /home/mesh-home/.local/bin/mesh-lock-holder --test
  1111429: 12 bash bash /home/mesh-home/.local/bin/mesh-lock-holder --test
  1111431: 12 grep grep -q attributed=
  1111787: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-lock-holder --test
  1148668: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-lock-holder --test
doctor pid=1014700 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1014700: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110665: 18 timeout timeout 25 /home/mesh-home/.local/bin/mesh-mains-hum --test
  1110772: 18 python /home/mesh-home/grainneukeln/.venv/bin/python /home/mesh-home/.local/bin/mesh-mains-hum --test
  1111671: 12 arecord arecord -q -f S16_LE -r 8000 -c 1 -d 6 /tmp/tmp.NTTk7NXyOO/td.mesh-mains-hum/tmppyx9bp0c/hum.wav
doctor pid=1015373 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1015373: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111168: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-mca --test
  1111224: 20 bash bash /home/mesh-home/.local/bin/mesh-mca --test
  1143164: 2 bash bash /home/mesh-home/.local/bin/mesh-mca --test
  1149050: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-mca --test
  1149061: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-mca --test
doctor pid=1016284 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1016284: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110955: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-media-scene --test
  1111037: 20 bash bash /home/mesh-home/.local/bin/mesh-media-scene --test
  1148398: 0 bash bash /home/mesh-home/.local/bin/mesh-media-scene --edge
  1148400: 0 bash bash /home/mesh-home/.local/bin/mesh-media-scene --edge
  1148537: 0 bash bash /home/mesh-home/.local/bin/mesh-media-scene --edge
  1148686: 0 bash bash /home/mesh-home/.local/bin/mesh-gpu-display --json
  1148920: 0 bash bash /home/mesh-home/.local/bin/mesh-gpu-display --json
  1148978: 0 nvidia-smi nvidia-smi --query-gpu=uuid,pci.bus_id,display_attached,display_active --format=csv,noheader,nounits
doctor pid=1017255 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1017255: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110262: 20 bash bash /home/mesh-home/.local/bin/mesh-mem-guard --test
  1111476: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-mem-guard --test
  1111529: 13 bash bash /home/mesh-home/.local/bin/mesh-mem-guard --test
  1148414: 4123168608 bash [bash]
doctor pid=1020538 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1020538: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1092162: 35 timeout timeout 20 /home/mesh-home/.local/bin/mesh-mind-compact --test
  1092242: 35 bash bash /home/mesh-home/.local/bin/mesh-mind-compact --test
  1094189: 35 bash bash /home/mesh-home/.local/bin/mesh-mind-compact --test
doctor pid=1021147 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1021147: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110577: 20 bash bash /home/mesh-home/.local/bin/mesh-mind-control --test
  1111348: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-mind-control --test
  1111437: 20 bash bash /home/mesh-home/.local/bin/mesh-mind-control --test
doctor pid=1024529 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1024529: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111231: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-mind-state --test
  1111451: 20 bash bash /home/mesh-home/.local/bin/mesh-mind-state --test
doctor pid=1025848 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1025848: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110258: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-misha-eye-contact --test
  1110499: 20 bash bash /home/mesh-home/.local/bin/mesh-misha-eye-contact --test
  1118865: 11 bash bash /home/mesh-home/.local/bin/mesh-misha-eye-contact --test
  1118894: 11 python3 python3 - /tmp/tmp.NTTk7NXyOO/td.mesh-misha-eye-contact/tmp.F3tmEZvKn5/blank.jpg /home/mesh-home/.mesh/groq.env
  1121895: 10 curl curl -s -m 90 http://localhost:11434/api/generate -H Content-Type: application/json -d @/tmp/misha-eye-req-1118894.json
doctor pid=1026858 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1026858: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110447: 20 bash bash /home/mesh-home/.local/bin/mesh-misha-wake --test
  1111632: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-misha-wake --test
  1148452: 0 awk awk -v s=2026-09-14T02:25:40Z -v now=2026-09-14T03:25:40Z      $2=="grant" && $3=="axis=frames" && $1>=s { c=split($0,f," "); for(i=1;i<=c;i++) if(f[i]~/^cost=/){split(f[i],g,"=");n+=g[2]+0} }     NR==1 { first=$1 }     END{ note = (first>s) ? "LOWER BOUND (mesh-cam-lock openers only); ledger starts " first : "LOWER BOUND: counts only captures routed through mesh-cam-lock"          printf "%d %s %s\n", n+0, "full", note } /home/mesh-home/.mesh/budget-ledger.log
  1148518: 0 bash bash /home/mesh-home/.local/bin/mesh-misha-wake --test
  1148700: 0 bash bash /home/mesh-home/.local/bin/mesh-misha-wake --test
  1148793: 0 bash bash /home/mesh-home/.local/bin/mesh-cam-lock --dev /dev/video0 --why misha-wake -- sh -c fswebcam --no-banner -d '/dev/video0' -r '640x480' -S 8 '/tmp/tmp.NTTk7NXyOO/td.mesh-misha-wake/tmp.cpJNs31S0g/.mesh/.misha-wake-frame.new.jpg'
  1148941: 0 bash bash /home/mesh-home/.local/bin/mesh-budget --gate frames --why misha-wake
doctor pid=1028038 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1028038: 66 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1140440: 7 timeout timeout 25 /home/mesh-home/.local/bin/mesh-mlme-tap --test
  1140479: 7 bash bash /home/mesh-home/.local/bin/mesh-mlme-tap --test
  1149135: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-mlme-tap --test
  1149220: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-mlme-tap --test
  1149270: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-mlme-tap --test
  1149272: 4123168608 tr tr \n
  1149287: 4123168608 python3 python3 -c  import re,sys H=sys.argv[1] CMDS=("AUTHENTICATE","ASSOCIATE","DEAUTHENTICATE","DISASSOCIATE","CONNECT","ROAM","DISCONNECT",       "FRAME","FRAME_TX_STATUS","NEW_STATION","DEL_STATION") ATTRS=("IFINDEX","IFNAME","MAC","FRAME","REASON_CODE","TIMED_OUT","DISCONNECTED_BY_AP","ACK") PINNED_C={"AUTHENTICATE":37,"ASSOCIATE":38,"DEAUTHENTICATE":39,"DISASSOCIATE":40,"CONNECT":46,           "ROAM":47,"DISCONNECT":48,"FRAME":59,"FRAME_TX_STATUS":60,"NEW_STATION":19,"DEL_STATION":20} PINNED_A={"IFINDEX":3,"IFNAME":4,"MAC":6,"FRAME":51,"REASON_CODE":54,"TIMED_OUT":65,           "DISCONNECTED_BY_AP":71,"ACK":92} def parse(src, enum, prefix):     m=re.search(r"^enum %s \{(.*?)^\};"%enum, src, re.S|re.M)     if not m: return {}     body=re.sub(r"/\*.*?\*/","",m.group(1),flags=re.S)     out={}; nxt=0     for line in body.split("\n"):         line=line.strip()         mm=re.match(r"^(%s[A-Z0-9_]*)\s*(=\s*([^,]+))?,?$"%prefix, line)         if not mm: continue         name=mm.group(1); val=mm.group(3)         if val is not None:             v=val.strip()             if re.fullmatch(r"\d+", v): nxt=int(v)             elif v in out: nxt=out[v]           # an ALIAS: takes the target value, does not advance             else: continue                      # unresolvable: skip WITHOUT advancing the counter         out[name]=nxt; nxt+=1     return out c=a={} src="" try: src=open(H).read() except Exception: pass if src:     c=parse(src,"nl80211_commands","NL80211_CMD_")     a=parse(src,"nl80211_attrs","NL80211_ATTR_") ok = all(("NL80211_CMD_"+k) in c for k in CMDS) and all(("NL80211_ATTR_"+k) in a for k in ATTRS) if ok:     src_name="header:"+H     C={k:c["NL80211_CMD_"+k] for k in CMDS}; A={k:a["NL80211_ATTR_"+k] for k in ATTRS} else:     src_name="pinned"; C=PINNED_C; A=PINNED_A print(" ".join("cmd:%s=%d"%(k,C[k]) for k in CMDS)) print(" ".join("attr:%s=%d"%(k,A[k]) for k in ATTRS)) print("src=%s"%src_name)  /usr/include/linux/nl80211.h
doctor pid=1029311 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1029311: 66 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111512: 18 main /home/mesh-home/.mesh/whispercpp/main -m /home/mesh-home/.mesh/whispercpp/models/ggml-tiny.bin -l ru -nt -f /home/mesh-home/.mesh/model-fixtures/stt-ru-operator-0812/input.wav
  1111898: 19 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-model-bench --test
  1111930: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-model-bench --test
  1112009: 20 python3 python3 /home/mesh-home/.local/bin/mesh-model-bench --test
doctor pid=1034881 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1034881: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110607: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-music-fanout --test
  1110807: 20 bash bash /home/mesh-home/.local/bin/mesh-music-fanout --test
  1111657: 20 bash bash /home/mesh-home/.local/bin/mesh-music-fanout --test
  1113096: 15 bash bash /home/mesh-home/.local/bin/mesh-music-fanout --test
  1113158: 15 bash bash /home/mesh-home/.local/bin/mesh-music-fanout --test
  1113229: 15 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-music-fanout/tmp.nWubsUX14p/tmp.x4JQQOPr36/work/records-stub/20260914-032527-stub-522b51f6.wav
  1113231: 15 grep grep ^MEASURE
  1113233: 15 head head -1
  1113522: 15 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-music-fanout/tmp.nWubsUX14p/tmp.x4JQQOPr36/work/records-stub/20260914-032527-stub-522b51f6.wav
  1113571: 15 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-music-fanout/tmp.nWubsUX14p/tmp.x4JQQOPr36/work/records-stub/20260914-032527-stub-522b51f6.wav
  1113601: 15 grep grep ^MEASURE
  1113682: 15 python /home/mesh-home/grainneukeln/.venv/bin/python - /tmp/tmp.NTTk7NXyOO/td.mesh-music-fanout/tmp.nWubsUX14p/tmp.x4JQQOPr36/work/records-stub/20260914-032527-stub-522b51f6.wav 0,12,3 0.006 measure
doctor pid=1035281 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1035281: 66 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110333: 20 timeout timeout 25 /home/mesh-home/.local/bin/mesh-music-session --test
  1110489: 20 bash bash /home/mesh-home/.local/bin/mesh-music-session --test
doctor pid=1042665 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1042665: 64 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110754: 19 timeout timeout 25 /home/mesh-home/.local/bin/mesh-node-care --test
  1110996: 19 bash bash /home/mesh-home/.local/bin/mesh-node-care --test
  1149233: 4 journalctl journalctl -b -1 -p err --no-pager
  1149234: 4 tail tail -40
  1149560: 4 bash bash /home/mesh-home/.local/bin/mesh-node-care --test
  1149582: 4 sh sh -s
doctor pid=1043502 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1043502: gone
doctor pid=1047365 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1047365: 64 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110739: 18 timeout timeout 25 /home/mesh-home/.local/bin/mesh-note3-light-raw --test
  1111188: 18 bash bash /home/mesh-home/.local/bin/mesh-note3-light-raw --test
  1148400: 0 bash bash /home/mesh-home/.local/bin/mesh-note3-light-raw --edge
  1148783: 4123168608 python3 python3 -c  ts, up, maxa = int('799995000000000'), float('800000'), float('600') if ts == 0:     print('NEVER -'); raise SystemExit age = up - ts / 1e9 print(('STALE' if age > maxa else 'LIVE'), '%.1f' % age)
doctor pid=1051978 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1051978: 63 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111132: 17 timeout timeout 25 /home/mesh-home/.local/bin/mesh-note3-ui --test
  1111328: 17 bash bash /home/mesh-home/.local/bin/mesh-note3-ui --test
  1149408: 4 timeout timeout 30 adb -s 4d00553d61ab90b7 exec-out screencap -p
  1149541: 4 adb adb -s 4d00553d61ab90b7 exec-out screencap -p
doctor pid=1057785 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1057785: 62 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1116897: 16 timeout timeout 25 /home/mesh-home/.local/bin/mesh-object-id --test
  1116972: 16 bash bash /home/mesh-home/.local/bin/mesh-object-id --test
doctor pid=1058257 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1058257: 62 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1117435: 16 timeout timeout 25 /home/mesh-home/.local/bin/mesh-observer-effect --test
  1117490: 16 bash bash /home/mesh-home/.local/bin/mesh-observer-effect --test
  1119367: 16 bash bash /home/mesh-home/.local/bin/mesh-observer-effect --test
  1119402: 16 bash bash /home/mesh-home/.local/bin/mesh-observer-effect --tool mesh-oe-red
  1119710: 16 flock flock -n -o -E 3 /tmp/tmp.NTTk7NXyOO/td.mesh-observer-effect/tmp.9S8cWBL590/.mesh/.observer-effect.lock bash /home/mesh-home/.local/bin/mesh-observer-effect --tool mesh-oe-red
  1119841: 16 bash bash /home/mesh-home/.local/bin/mesh-observer-effect --tool mesh-oe-red
  1120248: 16 bash bash /home/mesh-home/.local/bin/mesh-observer-effect --tool mesh-oe-red
  1120291: 16 bash bash /home/mesh-home/.local/bin/mesh-observer-effect --tool mesh-oe-red
  1120294: 16 wc wc -l
  1120308: 16 bash bash /home/mesh-home/.local/bin/mesh-observer-effect --tool mesh-oe-red
  1120309: 16 sort sort -u
doctor pid=1061303 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1061303: 61 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1121434: 16 timeout timeout 25 /home/mesh-home/.local/bin/mesh-operator-context --test
  1121494: 16 bash bash /home/mesh-home/.local/bin/mesh-operator-context --test
  1149122: 0 bash bash /home/mesh-home/.local/bin/mesh-operator-context --test
  1149166: 0 bash bash /home/mesh-home/.local/bin/mesh-operator-context --test
  1149167: 0 cut cut -f1,2
  1149250: 0 python3 python3 -c  import sys, re  lease = int(sys.argv[1]) raw   = {k: sys.argv[2 + 2*i]     for i, k in enumerate(("body","grip","ambient","light","prox"))} ages  = {k: sys.argv[2 + 2*i + 1] for i, k in enumerate(("body","grip","ambient","light","prox"))}  # A producer says "I cannot see" in words, not by writing nothing. Anything here is BLINDNESS, # never a reading — see fault (1). Compared upper-case and after the field split. # DEAF is the mesh-ambient-level unreachable sentinel (added there 2026-08-20, a full DAY before it # was added here — this set is a hand-maintained allowlist and a NEW producer word walks straight # past it; membership is not completeness). Live on mesh-home 2026-08-20..21: the room # ear held the only mic for 31h, ambient published DEAF, and this classifier scored it "ok" — a # blind organ sentinel fused as a reading, which is fault (1) at the top of this file recurring # under a word that did not exist when fault (1) was fixed. BLIND = {"", "UNREACHABLE", "MISSING", "OFFLINE", "UNKNOWN", "UNCERTAIN",          "DEAF", "N/A", "NA", "ERROR", "NONE", "-", "?"}  def field(key, text):     # Split on the delimiter the PRODUCER uses, never a guess — see fault (4).     text = (text or "").strip().split("\n")[0].strip()     if key == "body":         # mesh-body-motion: <steps>|<tag>|<hyst>|<pending>|<dwell>|<changes>; unreachable is         # the literal "|OFFLINE||||". The tag is field 2 and may carry [] in older records.         parts = text.split("|")         v = parts[1] if len(parts) > 1 else parts[0]         v = v.strip().strip("[]")         v = re.sub(r"^BODY-", "", v.upper())         return v     if key == "light":         # mesh-light writes EITHER "DIM" or "LIT|dwell_s=..|changes_24h=..". Whitespace is not         # the delimiter on the second shape.         return text.split("|")[0].split()[0].upper() if text.split("|")[0].split() else ""     if key in ("grip", "prox"):         # mesh-grip: "HELD 5 17593"; mesh-proximity: "<zone> <mac> <name>".         return text.split()[0].split("|")[0].upper() if text.split() else ""     # ambient: field 1 is the label. It is bare on the happy path (SILENCE/QUIET/MODERATE/LOUD) but     # the unreachable line carries its cause as `DEAF|reason=<held|floor|...>`, so the pipe IS the     # producer delimiter here now — splitting on whitespace alone would hand BLIND the string     # "DEAF|REASON=HELD", which matches nothing and scores the dead mic as a live reading again.     return text.split("|")[0].split()[0].upper() if text.split("|")[0].split() else ""  def status(key):     v = field(key, raw[key])     try:         age = int(ages[key])     except (ValueError, TypeError):         age = -1     if v in BLIND:         return v or "MISSING", "blind"     if age < 0:         return v, "blind"       # no file at all     if age > lease:         return v, "stale"       # last value on disk is not a claim about now     return v, "ok"  vals, why = {}, {} for k in ("body", "grip", "ambient", "light", "prox"):     vals[k], why[k] = status(k)  # prox is REPORTED, never gating — see fault (3). It names the nearest BLE device, which on this # node is furniture; an input no branch consults must not be allowed to decide the verdict. GATING = ("body", "grip", "ambient", "light") bad = [f"{k}:{why[k]}" for k in GATING if why[k] != "ok"]  def out(tag, st):     # NB no single quotes anywhere in this program: the whole thing lives inside a     # single-quoted bash string, so one apostrophe ends it and the rest leaks out as shell     # words. It did exactly that here once (why[.prox.] -> NameError: name prox is not     # defined), which is a syntax error in a language the reader was not thinking about.     pv = vals["prox"]     if why["prox"] != "ok":         pv = pv + "(" + why["prox"] + ")"     print("\t".join([tag, st, vals["body"], vals["grip"], vals["ambient"], vals["light"], pv]))     sys.exit(0)  if bad:     out("[unreachable:" + ",".join(bad) + "]", "UNCERTAIN")  body, grip, ambient, light = vals["body"], vals["grip"], vals["ambient"], vals["light"] walking = body in ("WALKING", "CARRIED") handled = body == "HANDLED" held    = grip == "HELD" loud    = ambient in ("LOUD", "MODERATE") bright  = light in ("LIT", "BRIGHT")  if walking:                                   out("[operator-mobile]", "ACTIVE_MOBILE") elif handled and loud:                        out("[operator-active]", "ACTIVE_MOBILE") elif held and not walking and loud and not bright: out("[operator-at-computer]", "AT_COMPUTER") elif held and not walking and bright:         out("[operator-at-computer]", "AT_COMPUTER") elif held and not walking:                    out("[operator-passive]", "PASSIVE") elif not held and not walking and not loud and not bright: out("[operator-resting]", "RESTING") else:                                         out("[operator-uncertain]", "UNCERTAIN")  900 42264|STILL|1||219834|0 0 HELD 5 1 0 SILENCE 0 OFFLINE 2026-08-17T19:24:14Z 0 NEAR a b 0
doctor pid=1063924 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1063924: 61 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1125075: 15 timeout timeout 25 /home/mesh-home/.local/bin/mesh-operator-hands --test
  1125221: 15 bash bash /home/mesh-home/.local/bin/mesh-operator-hands --test
  1125277: 15 python3 python3 - test /home/mesh-home/.mesh/chat.log 14 /home/mesh-home/lte-workstation/docs/fixtures/operator-hands-labels.tsv
doctor pid=1065515 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1065515: 60 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1126337: 15 timeout timeout 25 /home/mesh-home/.local/bin/mesh-organ-keepalive --test
  1126411: 15 bash bash /home/mesh-home/.local/bin/mesh-organ-keepalive --test
  1130993: 14 bash bash /home/mesh-home/.local/bin/mesh-organ-keepalive --test
  1131047: 14 bash bash /home/mesh-home/.local/bin/mesh-organ-keepalive --test
  1131080: 14 bash bash /home/mesh-home/.local/bin/mesh-organ-keepalive --test
  1131126: 14 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1148797: 2 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1148811: 2 timeout timeout 4 ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@192.168.8.146 echo ok
  1148898: 2 ssh ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@192.168.8.146 echo ok
doctor pid=1066742 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1066742: gone
doctor pid=1067512 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1067512: 61 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1128905: 15 timeout timeout 25 /home/mesh-home/.local/bin/mesh-pace --test
  1128997: 15 bash bash /home/mesh-home/.local/bin/mesh-pace --test
  1148914: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-pace --test
doctor pid=1067889 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1067889: 61 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1129343: 15 timeout timeout 25 /home/mesh-home/.local/bin/mesh-package-power --test
  1129477: 15 bash bash /home/mesh-home/.local/bin/mesh-package-power --test
doctor pid=1068505 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1068505: 61 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1130323: 16 timeout timeout 25 /home/mesh-home/.local/bin/mesh-pane-consume --test
  1130419: 16 bash bash /home/mesh-home/.local/bin/mesh-pane-consume --test
  1144395: 12 bash bash /home/mesh-home/.local/bin/mesh-pane-consume --test
  1144445: 12 python3 python3 /home/mesh-home/.local/bin/mesh-task queue --dispatch --owner fakech
doctor pid=1069729 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1069729: 61 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1131663: 16 timeout timeout 25 /home/mesh-home/.local/bin/mesh-path-watch --test
  1131795: 16 bash bash /home/mesh-home/.local/bin/mesh-path-watch --test
  1148657: 0 bash bash /home/mesh-home/.local/bin/mesh-path-watch
  1149186: 0 bash bash /home/mesh-home/.local/bin/mesh-path-watch
  1149354: 0 bash bash /home/mesh-home/.local/bin/mesh-path-watch
  1149404: 0 python3 python3 -c  import json, sys try:     d = json.load(sys.stdin) except Exception:     sys.exit(1) peers = d.get("Peer") or {} rows = [] for p in peers.values():     if "tag:lte-node" not in (p.get("Tags") or []):         continue     # space-safe: "Redmi 10" would corrupt the whitespace-split tape/state fields     host = (p.get("HostName") or "?").strip().replace(" ", "_")     if not p.get("Online"):         mode = "offline"     elif (p.get("CurAddr") or "").strip():         mode = "direct"     else:         mode = "relay"     rows.append(f"{host} {mode}") if not rows:     sys.exit(1) print("\n".join(sorted(rows)))
doctor pid=1070593 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1070593: 61 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1132552: 16 timeout timeout 25 /home/mesh-home/.local/bin/mesh-pcie-health --test
  1132658: 16 bash bash /home/mesh-home/.local/bin/mesh-pcie-health --test
  1148348: 0 bash bash /home/mesh-home/.local/bin/mesh-pcie-health
  1148369: 0 bash bash /home/mesh-home/.local/bin/mesh-pcie-health
  1148495: 0 bash bash /home/mesh-home/.local/bin/mesh-pcie-health
  1149445: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-pcie-health
  1149514: 0 bash bash /home/mesh-home/.local/bin/mesh-pcie-health --test
doctor pid=1072797 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1072797: 60 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1135389: 15 timeout timeout 25 /home/mesh-home/.local/bin/mesh-perimeter --test
  1135482: 15 bash bash /home/mesh-home/.local/bin/mesh-perimeter --test
  1148455: 10 bash bash /home/mesh-home/.local/bin/mesh-lan-newdevice --status
  1149200: 6 bash bash /home/mesh-home/.local/bin/mesh-lan-newdevice --status
  1149317: 6 timeout timeout 12 ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=accept-new root@100.105.241.84 cat /tmp/dhcp.leases 2>/dev/null
  1149375: 6 ssh ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=accept-new root@100.105.241.84 cat /tmp/dhcp.leases 2>/dev/null
  1149431: 10 bash bash /home/mesh-home/.local/bin/mesh-perimeter --test
  1149450: 10 timeout timeout 60 mesh-lan-newdevice --status
doctor pid=1073973 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1073973: 61 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1136383: 15 timeout timeout 25 /home/mesh-home/.local/bin/mesh-phone-ap --test
  1136453: 15 bash bash /home/mesh-home/.local/bin/mesh-phone-ap --test
  1148407: 3 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1148430: 3 bash bash /home/mesh-home/.local/bin/mesh-peer-addr Redmi
  1149087: 3 bash bash /home/mesh-home/.local/bin/mesh-phone-ap --test
  1149203: 3 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1149598: 3 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
doctor pid=1078032 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1078032: gone
doctor pid=1081163 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1081163: 59 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1144571: 14 timeout timeout 25 /home/mesh-home/.local/bin/mesh-pidfile.sh --test
  1144620: 14 bash bash /home/mesh-home/.local/bin/mesh-pidfile.sh --test
  1148538: 0 sudo [sudo] <defunct>
doctor pid=1081707 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1081707: 59 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1145682: 14 timeout timeout 25 /home/mesh-home/.local/bin/mesh-pkg-watch --test
  1145827: 14 bash bash /home/mesh-home/.local/bin/mesh-pkg-watch --test
  1146085: 14 bash bash /home/mesh-home/.local/bin/mesh-pkg-watch --test
  1148352: 12 bash bash /home/mesh-home/.local/bin/mesh-pkg-watch --test
  1148382: 12 apt-check /usr/bin/python3 /usr/lib/update-notifier/apt-check
doctor pid=1082796 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1082796: 59 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1146569: 14 timeout timeout 25 /home/mesh-home/.local/bin/mesh-plan-idle --test
  1146672: 14 bash bash /home/mesh-home/.local/bin/mesh-plan-idle --test
  1146764: 14 bash bash /home/mesh-home/.local/bin/mesh-plan-idle --test
  1146787: 14 bash bash /home/mesh-home/.local/bin/mesh-plan-idle --test
  1148113: 13 bash bash /home/mesh-home/.local/bin/mesh-plan-idle --test
  1148120: 13 grep grep -oE \[(done|taking|dispatch|evaporated)\][^]]*[a-z][a-z0-9-]*/[a-z0-9-]+ /home/mesh-home/.mesh/chat.log
  1148122: 13 grep grep -oE [a-z][a-z0-9-]*/[a-z0-9-]+
  1148131: 13 sort sort -u
doctor pid=1085252 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085252: gone
doctor pid=1085283 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085283: 54 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148368: 5 bash bash /home/mesh-home/.local/bin/mesh-records --test
  1148391: 5 bash bash /home/mesh-home/.local/bin/mesh-records
  1148409: 4 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-records/tmp.nFwQUVjjiu/src/probe.wav
  1148473: 5 bash bash /home/mesh-home/.local/bin/mesh-records
  1148599: 4 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-records/tmp.nFwQUVjjiu/src/probe.wav
  1148613: 4 grep grep ^MEASURE
  1148620: 4 bash bash /home/mesh-home/.local/bin/mesh-records
  1148696: 4 python /home/mesh-home/grainneukeln/.venv/bin/python - /tmp/tmp.NTTk7NXyOO/td.mesh-records/tmp.nFwQUVjjiu/src/probe.wav 0,12,3 0.006 measure
  1148839: 4 timeout timeout 90 mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-records/tmp.nFwQUVjjiu/src/probe.wav
  1148840: 4 head head -1
  1149095: 4 bash bash /home/mesh-home/.local/bin/mesh-soundscape --measure /tmp/tmp.NTTk7NXyOO/td.mesh-records/tmp.nFwQUVjjiu/src/probe.wav
  1149525: 9 timeout timeout 25 /home/mesh-home/.local/bin/mesh-records --test
  1149565: 9 bash bash /home/mesh-home/.local/bin/mesh-records --test
doctor pid=1085337 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085337: 58 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148453: 0 bash bash /home/mesh-home/.local/bin/mesh-prior-art zzqqx-nothing zzqqy-either
  1149377: 13 timeout timeout 25 /home/mesh-home/.local/bin/mesh-prior-art --test
  1149427: 13 bash bash /home/mesh-home/.local/bin/mesh-prior-art --test
  1149552: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-prior-art zzqqx-nothing zzqqy-either
doctor pid=1085385 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085385: 56 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148346: 0 bash bash /home/mesh-home/.local/bin/mesh-embed --cos ZOMBIE: wire mesh-zzz to mesh-www aggregator (field: fusion) [taking] ACTIVE-CLAIM kelvin telemetry probe — on it
  1148387: 0 bash bash /home/mesh-home/.local/bin/mesh-embed --cos ZOMBIE: wire mesh-zzz to mesh-www aggregator (field: fusion) [taking] ACTIVE-CLAIM kelvin telemetry probe — on it
  1148465: 0 bash bash /home/mesh-home/.local/bin/mesh-embed --cos ZOMBIE: wire mesh-zzz to mesh-www aggregator (field: fusion) [taking] ACTIVE-CLAIM kelvin telemetry probe — on it
  1148521: 10 timeout timeout 25 /home/mesh-home/.local/bin/mesh-queue-tend --test
  1148580: 0 python3 python3 -c import json,sys; print(json.dumps({"model": sys.argv[1], "input": sys.stdin.read()})) all-minilm:latest
  1148587: 10 bash bash /home/mesh-home/.local/bin/mesh-queue-tend --test
  1148606: 0 bash bash /home/mesh-home/.local/bin/mesh-queue-tend
  1148653: 0 bash bash /home/mesh-home/.local/bin/mesh-embed --cos ZOMBIE: wire mesh-zzz to mesh-www aggregator (field: fusion) [taking] ACTIVE-CLAIM kelvin telemetry probe — on it
  1149271: 3 bash bash /home/mesh-home/.local/bin/mesh-queue-tend --test
  1149306: 3 bash bash /home/mesh-home/.local/bin/mesh-queue-tend
doctor pid=1085411 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085411: 51 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148344: 6 bash bash /home/mesh-home/.local/bin/mesh-rhythm --test
  1148377: 0 bash bash /home/mesh-home/.local/bin/mesh-rhythm --test
  1148415: 0 python3 python3 -
  1149304: 6 timeout timeout 25 /home/mesh-home/.local/bin/mesh-rhythm --test
doctor pid=1085469 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085469: 58 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148638: 12 timeout timeout 25 /home/mesh-home/.local/bin/mesh-psi --test
  1148827: 0 bash bash /home/mesh-home/.local/bin/mesh-psi --test
  1148879: 0 bash bash /home/mesh-home/.local/bin/mesh-psi
  1148919: 12 bash bash /home/mesh-home/.local/bin/mesh-psi --test
doctor pid=1085508 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085508: 59 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148420: 13 bash bash /home/mesh-home/.local/bin/mesh-fsnotify --test
  1148550: 1 inotifywait inotifywait -qq -t 3 -e close_write,modify,create,move /tmp/tmp.NTTk7NXyOO/td.mesh-promises-watch/tmp.mc02raw6HP/watched
  1148906: 1 bash bash /home/mesh-home/.local/bin/mesh-fsnotify --window 4 --debounce 0 /tmp/tmp.NTTk7NXyOO/td.mesh-promises-watch/tmp.mc02raw6HP/watched -- true
  1149089: 13 timeout timeout 25 /home/mesh-home/.local/bin/mesh-promises-watch --test
  1149157: 13 bash bash /home/mesh-home/.local/bin/mesh-promises-watch --test
doctor pid=1085563 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085563: 59 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148774: 13 bash bash /home/mesh-home/.local/bin/mesh-promises --test
  1149122: 0 python3 python3 - journal /tmp/tmp.NTTk7NXyOO/td.mesh-promises/tmp.WkZP43TS3B/tmp.zirkgGfECS/board 2026-07-24T12:00:00Z 24 6 1 /tmp/tmp.NTTk7NXyOO/td.mesh-promises/tmp.WkZP43TS3B/tmp.zirkgGfECS/j.journal
  1149151: 14 timeout timeout 25 /home/mesh-home/.local/bin/mesh-promises --test
  1149204: 14 bash bash /home/mesh-home/.local/bin/mesh-promises --test
doctor pid=1085567 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085567: 51 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148435: 5 bash bash /home/mesh-home/.local/bin/mesh-room-address --test
  1148581: 4 bash bash /home/mesh-home/.local/bin/mesh-room-address --test
  1148749: 4 timeout timeout 8 ollama run qwen2.5:3b --think=false --format json Ты — фильтр пробуждения для голосового ассистента по имени Миша (звательные формы: Миша, Миш, Мишань). В комнате идёт живой разговор; микрофон также ловит галлюцинации распознавания речи на тишине. Ниже последние реплики из комнаты по порядку. Реши ТОЛЬКО про ПОСЛЕДНЮЮ реплику, используя предыдущие как контекст. ГЛАВНОЕ ПРАВИЛО: если в ПОСЛЕДНЕЙ реплике есть звательное обращение к Мише (Миша/Миш/Мишань — часто выделено запятой: "Миш,", "Ну вот, Миш," "Миша,") — это ВСЕГДА {"wake":true}, даже если дальше идёт жалоба, ремарка или незаконченная мысль. При любом сомнении отвечай {"wake":true} — пропущенное обращение хуже лишнего. Ответь {"wake":false} ТОЛЬКО когда обращения к Мише в последней реплике нет: люди говорят между собой; о Мише в ТРЕТЬЕМ лице без обращения к нему ("спроси у Миши", "Миша вчера чинил", "как думаешь, Миша прав"); слова, лишь ПОХОЖИЕ на имя (мишка, мишура, Мишель); бессмысленный обрывок STT на тишине. Примеры: Разговор: ПОСЛЕДНЯЯ: "Миша, ты нас слышишь?" -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Ну вот, Миш, плохо слушать, всё прерывается" -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Миш, кстати, а ты видишь..." -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Время" -> {"wake":false} Разговор: "Смотри какие мишки на витрине" ПОСЛЕДНЯЯ: "Да, милые, купим?" -> {"wake":false} Разговор: ПОСЛЕДНЯЯ: "Как думаешь, Миша был прав вчера?" -> {"wake":false} Разговор: ПОСЛЕДНЯЯ: "Повесь мишуру повыше" -> {"wake":false} Разговор:  ПОСЛЕДНЯЯ: "Миша, ты нас слышишь сейчас или нет? По-моему, нет."
  1148750: 4 tr tr -d \n
  1148859: 4 ollama ollama run qwen2.5:3b --think=false --format json Ты — фильтр пробуждения для голосового ассистента по имени Миша (звательные формы: Миша, Миш, Мишань). В комнате идёт живой разговор; микрофон также ловит галлюцинации распознавания речи на тишине. Ниже последние реплики из комнаты по порядку. Реши ТОЛЬКО про ПОСЛЕДНЮЮ реплику, используя предыдущие как контекст. ГЛАВНОЕ ПРАВИЛО: если в ПОСЛЕДНЕЙ реплике есть звательное обращение к Мише (Миша/Миш/Мишань — часто выделено запятой: "Миш,", "Ну вот, Миш," "Миша,") — это ВСЕГДА {"wake":true}, даже если дальше идёт жалоба, ремарка или незаконченная мысль. При любом сомнении отвечай {"wake":true} — пропущенное обращение хуже лишнего. Ответь {"wake":false} ТОЛЬКО когда обращения к Мише в последней реплике нет: люди говорят между собой; о Мише в ТРЕТЬЕМ лице без обращения к нему ("спроси у Миши", "Миша вчера чинил", "как думаешь, Миша прав"); слова, лишь ПОХОЖИЕ на имя (мишка, мишура, Мишель); бессмысленный обрывок STT на тишине. Примеры: Разговор: ПОСЛЕДНЯЯ: "Миша, ты нас слышишь?" -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Ну вот, Миш, плохо слушать, всё прерывается" -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Миш, кстати, а ты видишь..." -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Время" -> {"wake":false} Разговор: "Смотри какие мишки на витрине" ПОСЛЕДНЯЯ: "Да, милые, купим?" -> {"wake":false} Разговор: ПОСЛЕДНЯЯ: "Как думаешь, Миша был прав вчера?" -> {"wake":false} Разговор: ПОСЛЕДНЯЯ: "Повесь мишуру повыше" -> {"wake":false} Разговор:  ПОСЛЕДНЯЯ: "Миша, ты нас слышишь сейчас или нет? По-моему, нет."
  1149009: 5 timeout timeout 25 /home/mesh-home/.local/bin/mesh-room-address --test
  1149177: 5 bash bash /home/mesh-home/.local/bin/mesh-room-address --test
  1149635: 4 bash bash /home/mesh-home/.local/bin/mesh-room-address --test
doctor pid=1085654 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085654: 53 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085936: 53 timeout timeout 12 /home/mesh-home/.local/bin/mesh-restore --test
  1086231: 53 bash bash /home/mesh-home/.local/bin/mesh-restore --test
  1148817: 15 bash bash /home/mesh-home/.local/bin/mesh-restore --test
  1148931: 15 bash bash /home/mesh-home/.local/bin/mesh-restore --test
doctor pid=1085664 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085664: 54 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148532: 8 timeout timeout 25 /home/mesh-home/.local/bin/mesh-resource-guard --test
  1148578: 7 bash bash /home/mesh-home/.local/bin/mesh-resource-guard --test
  1148683: 8 bash bash /home/mesh-home/.local/bin/mesh-resource-guard --test
  1149417: 4123168608 awk [awk]
doctor pid=1085711 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085711: 55 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148639: 10 timeout timeout 25 /home/mesh-home/.local/bin/mesh-reflexes --test
  1148692: 10 bash bash /home/mesh-home/.local/bin/mesh-reflexes --test
  1149621: 1 bash bash /home/mesh-home/.local/bin/mesh-reflexes --test
  1149634: 1 bash bash /home/mesh-home/.local/bin/mesh-reflexes --apply
doctor pid=1085743 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085743: gone
doctor pid=1085798 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085798: gone
doctor pid=1085811 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085811: 56 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148497: 10 timeout timeout 25 /home/mesh-home/.local/bin/mesh-reflex-health --test
  1148520: 10 bash bash /home/mesh-home/.local/bin/mesh-reflex-health --test
  1148857: 10 bash bash /home/mesh-home/.local/bin/mesh-reflex-health --test
doctor pid=1085925 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085925: 61 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148873: 0 bash bash /home/mesh-home/.local/bin/mesh-promises.bak-20260912-witness --test
  1148938: 0 bash bash /home/mesh-home/.local/bin/mesh-promises.bak-20260912-witness --test
  1148941: 0 grep grep -oE (^| )open=[0-9]+
  1148944: 0 cut cut -d= -f2
  1148967: 15 bash bash /home/mesh-home/.local/bin/mesh-promises.bak-20260912-witness --test
  1149175: 16 timeout timeout 25 /home/mesh-home/.local/bin/mesh-promises.bak-20260912-witness --test
  1149253: 16 bash bash /home/mesh-home/.local/bin/mesh-promises.bak-20260912-witness --test
doctor pid=1086009 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1086009: 63 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148601: 1 bash bash /home/mesh-home/.local/bin/mesh-precision --test
  1148701: 1 bash bash /home/mesh-home/.local/bin/mesh-precision --json --closure /tmp/tmp.NTTk7NXyOO/td.mesh-precision/tmp.JXSUaoiSlD/zi_y --env /tmp/tmp.NTTk7NXyOO/td.mesh-precision/tmp.JXSUaoiSlD/zi_e
  1148903: 18 timeout timeout 25 /home/mesh-home/.local/bin/mesh-precision --test
  1148963: 18 bash bash /home/mesh-home/.local/bin/mesh-precision --test
  1149061: 1 python3 python3 -
doctor pid=1086024 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1086024: gone
doctor pid=1086084 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1086084: 54 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148380: 6 bash bash /home/mesh-home/.local/bin/mesh-roll-call
  1148571: 7 bash bash /home/mesh-home/.local/bin/mesh-roll-call
  1148600: 7 bash bash /home/mesh-home/.local/bin/mesh-roll-call
  1148612: 7 bash bash /home/mesh-home/.local/bin/mesh-roll-call
  1148614: 7 awk awk -F\t -v m=minds $3==m {printf "x%s — %s\n", $1, $4; exit}
  1148759: 9 bash bash /home/mesh-home/.local/bin/mesh-roll-call --test
  1148798: 9 timeout timeout 25 /home/mesh-home/.local/bin/mesh-roll-call --test
  1148925: 9 bash bash /home/mesh-home/.local/bin/mesh-roll-call --test
  1149287: 7 bash bash /home/mesh-home/.local/bin/mesh-roll-call --test
  1149502: 7 bash bash /home/mesh-home/.local/bin/mesh-roll-call
  1149798: 6 bash bash /home/mesh-home/.local/bin/mesh-roll-call
  1149800: 6 awk awk -F\t          # RETIRE-AWARE ROUND CUTOFF (board task rollcall-escalation-counter-ignores-retire, 2026-08-19):         # the count is of rounds a proposal recurred in, so it must be a count of rounds SINCE THE LAST         # DECISION — otherwise a retire cannot lower it and the closed item re-escalates every round         # until LEDGER_DAYS ages it out. Live: job RETIRED hh-выход-мимо-VPN 2026-08-17T20:02:40Z and the         # next FIVE rounds each carried a verbatim "recurred x3 — unchanged (hh-выход-мимо-VPN)" demand         # for a decision already taken. The pre-existing retire credit (the excl harvest in the RETIRE         # branch above) could not reach it TWICE OVER: it matches only the literal wording "declined",         # and even harvested, propose_sig destroys the non-ASCII subject (hh dropped as <=2 chars, VPN         # kept) so both keys collapse to a token or two and sig_actioned s >=2-shared floor can never         # fire. Neither defect is fixable by widening a string match; the ARITHMETIC is what is wrong.         # So: cutoff = the epoch of the most-recent DECISION-ANNOUNCING null (retire_marker) posted by         # the sig s most-recent proposer — the same mind the escalation clause addresses (recur_for_mind),         # so the credit lands where the demand is sent — and only rounds AFTER it are counted. No subject         # matching is involved, which is exactly why it survives a subject propose_sig cannot key.         # Conservative in the documented direction: that mind s retire also resets its OTHER live chronic         # sigs (they simply re-accumulate), and a bare empty round ("PROPOSE none", no marker) resets         # nothing at all.         $1=="__RETIRE__" { if($3+0 > nullep[$4]+0) nullep[$4]=$3+0; next }         { key=$1 SUBSEP $2           if(!(key in epk) || $3+0 > epk[key]+0) epk[key]=$3+0           if(!(key in repk)) { repk[key]=$5; mindk[key]=$4 }           if(!($1 in maxrnd) || $2+0 > maxrnd[$1]+0){ maxrnd[$1]=$2+0; who[$1]=$4 }           sigs[$1]=1 }         END { for(k in sigs){                 cut = (who[k] in nullep) ? nullep[who[k]]+0 : 0                 n=0; mx=-1; mn=-1; mep=0; w=""; rp=""; rp0=""                 for(key in epk){                   split(key, a, SUBSEP); if(a[1]!=k) continue                   if(cut>0 && epk[key]+0 <= cut) continue                   r=a[2]+0; n++                   if(mx<0 || r>mx){ mx=r; w=mindk[key]; rp=repk[key] }                   if(mn<0 || r<mn){ mn=r; rp0=repk[key] }                   if(epk[key]+0 > mep) mep=epk[key]+0 }                 if(n>0) printf "%d\t%s\t%s\t%s\t%s\t%d\n", n, k, w, rp, rp0, mep } }
  1149804: 6 sort sort -rn
doctor pid=1086140 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1086140: 60 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148366: 15 timeout timeout 25 /home/mesh-home/.local/bin/mesh-quota --test
  1148469: 15 bash bash /home/mesh-home/.local/bin/mesh-quota --test
  1148480: 3 bash bash /home/mesh-home/.local/bin/mesh-quota --test
  1148586: 3 bash bash /home/mesh-home/.local/bin/mesh-quota --test
  1148747: 3 bash bash /home/mesh-home/.local/bin/mesh-quota --test
  1148769: 0 bash bash /home/mesh-home/.local/bin/mesh-pace --status
  1148791: 3 bash bash /home/mesh-home/.local/bin/mesh-pace --status
  1148813: 3 awk awk $1=="dispatch"{print $4" "$5; exit}
  1148815: 0 bash bash /home/mesh-home/.local/bin/mesh-pace --status
  1148878: 0 timeout timeout 20 mesh-labor --json
  1148959: 0 bash bash /home/mesh-home/.local/bin/mesh-labor --json
doctor pid=1086160 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1086160: 53 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148376: 8 timeout timeout 25 /home/mesh-home/.local/bin/mesh-room-music --test
  1148413: 8 bash bash /home/mesh-home/.local/bin/mesh-room-music --test
  1148927: 0 bash bash /home/mesh-home/.local/bin/mesh-room-music --test
  1149015: 0 bash bash /home/mesh-home/.local/bin/mesh-room-music --test
  1149018: 0 grep grep -oE (^| )s [0-9.]+
  1149023: 0 grep grep -oE [0-9.]+$
doctor pid=1086204 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1086204: 57 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148867: 0 bash bash /home/mesh-home/.local/bin/mesh-selfcare --loop 1
  1148876: 0 bash bash /home/mesh-home/.local/bin/mesh-selfcare --loop 1
  1148881: 0 bash bash /home/mesh-home/.local/bin/mesh-selfcare --loop 1
  1148933: 0 bash bash /home/mesh-home/.local/bin/mesh-link-heal --layer
  1148961: 0 head head -n1
  1149043: 1 bash bash /home/mesh-home/.local/bin/mesh-selfcare --loop 1
  1149080: 11 timeout timeout 25 /home/mesh-home/.local/bin/mesh-report --test
  1149293: 11 bash bash /home/mesh-home/.local/bin/mesh-report --test
  1149456: 11 bash bash /home/mesh-home/.local/bin/mesh-report --test
  1149520: 11 bash bash /home/mesh-home/.local/bin/mesh-selfcare --test
doctor pid=1086220 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1086220: 54 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1149283: 4 sleep sleep 8
doctor pid=1086234 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1086234: 60 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148431: 15 bash bash /home/mesh-home/.local/bin/mesh-quota-react --test
  1148765: 1 bash bash /home/mesh-home/.local/bin/mesh-quota-react --edge
  1148980: 15 timeout timeout 25 /home/mesh-home/.local/bin/mesh-quota-react --test
  1148996: 1 bash bash /home/mesh-home/.local/bin/mesh-quota-react --edge
  1149041: 1 bash bash /home/mesh-home/.local/bin/mesh-quota-react --test
  1149065: 15 bash bash /home/mesh-home/.local/bin/mesh-quota-react --test
  1149074: 1 pstree pstree -p 1148708
  1149076: 1 bash bash /home/mesh-home/.local/bin/mesh-quota-react --edge
  1149077: 1 grep grep -oE claude|opencode|codex|agy|gemini
  1149081: 1 head head -1
doctor pid=1086253 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1086253: 54 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148381: 3 bash bash /home/mesh-home/.local/bin/mesh-room-reflex --test
  1148543: 2 bash bash /home/mesh-home/.local/bin/mesh-room-address --window
  1148558: 2 bash bash /home/mesh-home/.local/bin/mesh-room-address --window
  1148592: 2 timeout timeout 8 ollama run qwen2.5:3b --think=false --format json Ты — фильтр пробуждения для голосового ассистента по имени Миша (звательные формы: Миша, Миш, Мишань). В комнате идёт живой разговор; микрофон также ловит галлюцинации распознавания речи на тишине. Ниже последние реплики из комнаты по порядку. Реши ТОЛЬКО про ПОСЛЕДНЮЮ реплику, используя предыдущие как контекст. ГЛАВНОЕ ПРАВИЛО: если в ПОСЛЕДНЕЙ реплике есть звательное обращение к Мише (Миша/Миш/Мишань — часто выделено запятой: "Миш,", "Ну вот, Миш," "Миша,") — это ВСЕГДА {"wake":true}, даже если дальше идёт жалоба, ремарка или незаконченная мысль. При любом сомнении отвечай {"wake":true} — пропущенное обращение хуже лишнего. Ответь {"wake":false} ТОЛЬКО когда обращения к Мише в последней реплике нет: люди говорят между собой; о Мише в ТРЕТЬЕМ лице без обращения к нему ("спроси у Миши", "Миша вчера чинил", "как думаешь, Миша прав"); слова, лишь ПОХОЖИЕ на имя (мишка, мишура, Мишель); бессмысленный обрывок STT на тишине. Примеры: Разговор: ПОСЛЕДНЯЯ: "Миша, ты нас слышишь?" -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Ну вот, Миш, плохо слушать, всё прерывается" -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Миш, кстати, а ты видишь..." -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Время" -> {"wake":false} Разговор: "Смотри какие мишки на витрине" ПОСЛЕДНЯЯ: "Да, милые, купим?" -> {"wake":false} Разговор: ПОСЛЕДНЯЯ: "Как думаешь, Миша был прав вчера?" -> {"wake":false} Разговор: ПОСЛЕДНЯЯ: "Повесь мишуру повыше" -> {"wake":false} Разговор: [11:00:00] предыдущая ПОСЛЕДНЯЯ: "[11:00:30] Миша, глянь"
  1148611: 2 tr tr -d \n
  1148673: 2 ollama ollama run qwen2.5:3b --think=false --format json Ты — фильтр пробуждения для голосового ассистента по имени Миша (звательные формы: Миша, Миш, Мишань). В комнате идёт живой разговор; микрофон также ловит галлюцинации распознавания речи на тишине. Ниже последние реплики из комнаты по порядку. Реши ТОЛЬКО про ПОСЛЕДНЮЮ реплику, используя предыдущие как контекст. ГЛАВНОЕ ПРАВИЛО: если в ПОСЛЕДНЕЙ реплике есть звательное обращение к Мише (Миша/Миш/Мишань — часто выделено запятой: "Миш,", "Ну вот, Миш," "Миша,") — это ВСЕГДА {"wake":true}, даже если дальше идёт жалоба, ремарка или незаконченная мысль. При любом сомнении отвечай {"wake":true} — пропущенное обращение хуже лишнего. Ответь {"wake":false} ТОЛЬКО когда обращения к Мише в последней реплике нет: люди говорят между собой; о Мише в ТРЕТЬЕМ лице без обращения к нему ("спроси у Миши", "Миша вчера чинил", "как думаешь, Миша прав"); слова, лишь ПОХОЖИЕ на имя (мишка, мишура, Мишель); бессмысленный обрывок STT на тишине. Примеры: Разговор: ПОСЛЕДНЯЯ: "Миша, ты нас слышишь?" -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Ну вот, Миш, плохо слушать, всё прерывается" -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Миш, кстати, а ты видишь..." -> {"wake":true} Разговор: ПОСЛЕДНЯЯ: "Время" -> {"wake":false} Разговор: "Смотри какие мишки на витрине" ПОСЛЕДНЯЯ: "Да, милые, купим?" -> {"wake":false} Разговор: ПОСЛЕДНЯЯ: "Как думаешь, Миша был прав вчера?" -> {"wake":false} Разговор: ПОСЛЕДНЯЯ: "Повесь мишуру повыше" -> {"wake":false} Разговор: [11:00:00] предыдущая ПОСЛЕДНЯЯ: "[11:00:30] Миша, глянь"
  1149222: 8 timeout timeout 25 /home/mesh-home/.local/bin/mesh-room-reflex --test
  1149266: 8 bash bash /home/mesh-home/.local/bin/mesh-room-reflex --test
doctor pid=1086263 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1086263: 56 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1149062: 0 bash bash /home/mesh-home/.local/bin/mesh-roll-call-retire-arm --test
  1149072: 0 bash bash /home/mesh-home/.local/bin/mesh-roll-call-retire-arm
  1149390: 10 timeout timeout 25 /home/mesh-home/.local/bin/mesh-roll-call-retire-arm --test
  1149503: 10 bash bash /home/mesh-home/.local/bin/mesh-roll-call-retire-arm --test
doctor pid=1086733 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1086733: 57 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148412: 12 timeout timeout 25 /home/mesh-home/.local/bin/mesh-revive --test
  1148572: 12 bash bash /home/mesh-home/.local/bin/mesh-revive --test
  1148640: 5 bash bash /home/mesh-home/.local/bin/mesh-revive --check
  1149000: 0 bash bash /home/mesh-home/.local/bin/mesh-sms ⚠️ mesh-revive ESCALATED: mesh-home still starving after heal — LOCAL LINK WEDGED — the fault is this node's own uplink, NOT the upstream; mesh-link-heal owns this layer (the exit-node/tailscale rungs below aim elsewhere). Manual intervention needed.
  1149106: 0 bash bash /home/mesh-home/.local/bin/mesh-sms ⚠️ mesh-revive ESCALATED: mesh-home still starving after heal — LOCAL LINK WEDGED — the fault is this node's own uplink, NOT the upstream; mesh-link-heal owns this layer (the exit-node/tailscale rungs below aim elsewhere). Manual intervention needed.
  1149291: 0 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
doctor pid=1087855 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1087855: gone
doctor pid=1093623 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1093623: 53 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148346: 0 sleep sleep 1
  1148396: 2 bash bash /home/mesh-home/.local/bin/mesh-route-events --daemon
  1148401: 2 bash bash /home/mesh-home/.local/bin/mesh-route-events --daemon
  1148421: 2 sleep sleep 5
  1148562: 2 gawk gawk BEGIN{ FS="\n" } {   line=$0   ts="-"   if (match(line, /^\[[0-9][^]]*\][ ]?/)) {     ts=substr(line, RSTART+1, RLENGTH-2); sub(/\]$/,"",ts); sub(/[ ]+$/,"",ts)     line=substr(line, RSTART+RLENGTH)   }   fam="?"   if (match(line, /^\[[A-Z0-9]+\]/)) { fam=substr(line, RSTART+1, RLENGTH-2); line=substr(line, RSTART+RLENGTH) }   op="add"   if (line ~ /^Deleted[ ]/) { op="del"; sub(/^Deleted[ ]+/,"",line) }   else if (line ~ /^Replaced[ ]/) { op="repl"; sub(/^Replaced[ ]+/,"",line) }   if (line == "") next   # infer the family only when the label is absent, and SAY that it was inferred   if (fam == "?") { if (line ~ /^[0-9]+:/ || line ~ /[ \t]lookup[ \t]/) fam="?~RULE"; else fam="?~ROUTE" }   tbl="-"   if (fam ~ /RULE/) { if (match(line, /lookup[ \t]+[^ \t]+/)) { tbl=substr(line,RSTART,RLENGTH); sub(/^lookup[ \t]+/,"",tbl) } }   else { if (match(line, /[ \t]table[ \t]+[^ \t]+/)) { tbl=substr(line,RSTART,RLENGTH); sub(/^[ \t]*table[ \t]+/,"",tbl) } else tbl="main" }   kind="-"   if (fam ~ /RULE/) kind="rule"   else if (line ~ /^throw[ \t]/) kind="throw"   else if (line ~ /^blackhole[ \t]/) kind="blackhole"   else if (line ~ /^unreachable[ \t]/) kind="unreachable"   else if (line ~ /^prohibit[ \t]/) kind="prohibit"   else if (line ~ /^default([ \t]|$)/) kind="default"   else kind="unicast"   dst="-"   if (fam !~ /RULE/) { n=split(line, w, /[ \t]+/); for (i=1;i<=n;i++) { if (w[i] ~ /^(throw|blackhole|unreachable|prohibit|local|broadcast|multicast|unicast)$/) continue; dst=w[i]; break } }   txt=line; gsub(/\t/," ",txt); gsub(/[ ]+$/,"",txt)   printf "%d %s fam=%s op=%s table=%s kind=%s dst=%s ts=%s :: %s\n", \     systime(), strftime("%Y-%m-%dT%H:%M:%SZ", systime(), 1), fam, op, tbl, kind, dst, ts, txt   fflush() }
  1148563: 3 bash bash -c        set -uo pipefail       ip link set lo up       setpriv --reuid=1000 --regid=1000 --clear-groups bash "/home/mesh-home/.local/bin/mesh-route-events" --daemon >>"/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.dlog" 2>&1 &       DP=$!       for i in $(seq 1 40); do grep -q SUBSCRIBED "/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.cov" 2>/dev/null && break; sleep 0.25; done       ip route add throw 192.168.8.0/24 table 52       ip route add blackhole 198.51.100.0/24 table 52       ip rule add from 10.9.9.9 lookup 52 pref 5270       ip rule add from 10.9.9.10 lookup 99 pref 5271       sleep 1       # FOUR throw-deletes, THREE of which must survive as wipes. Each exists because a mutation of       # the classifier was GREEN without it — a two-event fixture proved only that a classifier was       # present, never that any of its three terms was doing work.       # W1 — rule STANDING, no rule-delete anywhere yet: the reconverge shape, a real WIPE.       ip route del throw 192.168.8.0/24 table 52       sleep 1       # W2 — a rule-delete lands microseconds before, but it is for a DIFFERENT TABLE (99). Another       # table being dismantled says nothing about ours, so this is still a WIPE. Without this, a       # classifier that ignored the table matched any rule-delete and stayed green.       ip route add throw 192.168.8.0/24 table 52       ip rule del from 10.9.9.10 lookup 99 pref 5271       ip route del throw 192.168.8.0/24 table 52       sleep 1       # T1 — the TEARDOWN: the OWN rule of THIS table, deleted immediately before. The halt shape       # produced the live false positive (wipes=4 for a window in which nothing was swallowed).       ip route add throw 192.168.8.0/24 table 52       ip rule del from 10.9.9.9 lookup 52 pref 5270       ip route del throw 192.168.8.0/24 table 52       sleep 4       # W3 — the table-52 rule-delete is now well OUTSIDE the window, so it no longer excuses       # anything: a WIPE again. Without this, a classifier that dropped the time test entirely (any       # earlier rule-delete excuses every later throw) stayed green.       ip route add throw 192.168.8.0/24 table 52       ip route del throw 192.168.8.0/24 table 52       sleep 1       kill -TERM -- -$(sed -n "s/.*) //p" /proc/$DP/stat 2>/dev/null | awk "{print \$3}") 2>/dev/null       sleep 0.5       exit 0
  1148596: 2 bash bash /home/mesh-home/.local/bin/mesh-route-events --daemon
  1148852: 8 timeout timeout 20 /home/mesh-home/.local/bin/mesh-route-events --test
  1148924: 3 bash bash /home/mesh-home/.local/bin/mesh-route-events --test
  1148930: 3 bash bash /home/mesh-home/.local/bin/mesh-route-events --daemon
  1148942: 8 bash bash /home/mesh-home/.local/bin/mesh-route-events --test
  1148949: 1 sleep sleep 2
  1148952: 3 timeout timeout -k 5 60 sudo -n unshare -n env MESH_ROUTE_EVENTS_LOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.log MESH_ROUTE_EVENTS_COVF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.cov MESH_ROUTE_EVENTS_LOCK=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.lock MESH_ROUTE_EVENTS_STARTF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.started MESH_ROUTE_EVENTS_PIDF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.pid MESH_ROUTE_EVENTS_DLOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.dlog MESH_ROUTE_EVENTS_COV_S=2 bash -c        set -uo pipefail       ip link set lo up       setpriv --reuid=1000 --regid=1000 --clear-groups bash "/home/mesh-home/.local/bin/mesh-route-events" --daemon >>"/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.dlog" 2>&1 &       DP=$!       for i in $(seq 1 40); do grep -q SUBSCRIBED "/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.cov" 2>/dev/null && break; sleep 0.25; done       ip route add throw 192.168.8.0/24 table 52       ip route add blackhole 198.51.100.0/24 table 52       ip rule add from 10.9.9.9 lookup 52 pref 5270       ip rule add from 10.9.9.10 lookup 99 pref 5271       sleep 1       # FOUR throw-deletes, THREE of which must survive as wipes. Each exists because a mutation of       # the classifier was GREEN without it — a two-event fixture proved only that a classifier was       # present, never that any of its three terms was doing work.       # W1 — rule STANDING, no rule-delete anywhere yet: the reconverge shape, a real WIPE.       ip route del throw 192.168.8.0/24 table 52       sleep 1       # W2 — a rule-delete lands microseconds before, but it is for a DIFFERENT TABLE (99). Another       # table being dismantled says nothing about ours, so this is still a WIPE. Without this, a       # classifier that ignored the table matched any rule-delete and stayed green.       ip route add throw 192.168.8.0/24 table 52       ip rule del from 10.9.9.10 lookup 99 pref 5271       ip route del throw 192.168.8.0/24 table 52       sleep 1       # T1 — the TEARDOWN: the OWN rule of THIS table, deleted immediately before. The halt shape       # produced the live false positive (wipes=4 for a window in which nothing was swallowed).       ip route add throw 192.168.8.0/24 table 52       ip rule del from 10.9.9.9 lookup 52 pref 5270       ip route del throw 192.168.8.0/24 table 52       sleep 4       # W3 — the table-52 rule-delete is now well OUTSIDE the window, so it no longer excuses       # anything: a WIPE again. Without this, a classifier that dropped the time test entirely (any       # earlier rule-delete excuses every later throw) stayed green.       ip route add throw 192.168.8.0/24 table 52       ip route del throw 192.168.8.0/24 table 52       sleep 1       kill -TERM -- -$(sed -n "s/.*) //p" /proc/$DP/stat 2>/dev/null | awk "{print \$3}") 2>/dev/null       sleep 0.5       exit 0
  1148990: 3 sudo sudo -n unshare -n env MESH_ROUTE_EVENTS_LOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.log MESH_ROUTE_EVENTS_COVF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.cov MESH_ROUTE_EVENTS_LOCK=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.lock MESH_ROUTE_EVENTS_STARTF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.started MESH_ROUTE_EVENTS_PIDF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.pid MESH_ROUTE_EVENTS_DLOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.dlog MESH_ROUTE_EVENTS_COV_S=2 bash -c        set -uo pipefail       ip link set lo up       setpriv --reuid=1000 --regid=1000 --clear-groups bash "/home/mesh-home/.local/bin/mesh-route-events" --daemon >>"/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.dlog" 2>&1 &       DP=$!       for i in $(seq 1 40); do grep -q SUBSCRIBED "/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.iuOaNAtB1X/e.cov" 2>/dev/null && break; sleep 0.25; done       ip route add throw 192.168.8.0/24 table 52       ip route add blackhole 198.51.100.0/24 table 52       ip rule add from 10.9.9.9 lookup 52 pref 5270       ip rule add from 10.9.9.10 lookup 99 pref 5271       sleep 1       # FOUR throw-deletes, THREE of which must survive as wipes. Each exists because a mutation of       # the classifier was GREEN without it — a two-event fixture proved only that a classifier was       # present, never that any of its three terms was doing work.       # W1 — rule STANDING, no rule-delete anywhere yet: the reconverge shape, a real WIPE.       ip route del throw 192.168.8.0/24 table 52       sleep 1       # W2 — a rule-delete lands microseconds before, but it is for a DIFFERENT TABLE (99). Another       # table being dismantled says nothing about ours, so this is still a WIPE. Without this, a       # classifier that ignored the table matched any rule-delete and stayed green.       ip route add throw 192.168.8.0/24 table 52       ip rule del from 10.9.9.10 lookup 99 pref 5271       ip route del throw 192.168.8.0/24 table 52       sleep 1       # T1 — the TEARDOWN: the OWN rule of THIS table, deleted immediately before. The halt shape       # produced the live false positive (wipes=4 for a window in which nothing was swallowed).       ip route add throw 192.168.8.0/24 table 52       ip rule del from 10.9.9.9 lookup 52 pref 5270       ip route del throw 192.168.8.0/24 table 52       sleep 4       # W3 — the table-52 rule-delete is now well OUTSIDE the window, so it no longer excuses       # anything: a WIPE again. Without this, a classifier that dropped the time test entirely (any       # earlier rule-delete excuses every later throw) stayed green.       ip route add throw 192.168.8.0/24 table 52       ip route del throw 192.168.8.0/24 table 52       sleep 1       kill -TERM -- -$(sed -n "s/.*) //p" /proc/$DP/stat 2>/dev/null | awk "{print \$3}") 2>/dev/null       sleep 0.5       exit 0
  1149241: 2 ip ip -ts monitor label route rule
doctor pid=1099441 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1099441: 52 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148577: 6 timeout timeout 25 /home/mesh-home/.local/bin/mesh-rq-wait --test
  1148630: 6 python3 python3 /home/mesh-home/.local/bin/mesh-rq-wait --test
  1149298: 3 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-rq-wait --json
doctor pid=1102174 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1102174: 51 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148681: 1 piper /home/mesh-home/.mesh/piper/piper/piper -m /home/mesh-home/.mesh/piper/voices/ru_RU-irina-medium.onnx -f /tmp/tmp.NTTk7NXyOO/td.mesh-say/mtts-test-EOoUGN.wav
  1149111: 6 bash bash /home/mesh-home/.local/bin/mesh-tts --test
  1149689: 6 timeout timeout 25 /home/mesh-home/.local/bin/mesh-say --test
  1149762: 6 bash bash /home/mesh-home/.local/bin/mesh-say --test
doctor pid=1106976 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1106976: 50 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148361: 3 timeout timeout 25 /home/mesh-home/.local/bin/mesh-selfcare --test
  1148429: 1 bash bash /home/mesh-home/.local/bin/mesh-revive --check
  1148478: 3 bash bash /home/mesh-home/.local/bin/mesh-selfcare --test
  1149140: 3 bash bash /home/mesh-home/.local/bin/mesh-selfcare --test
  1149251: 1 bash bash /home/mesh-home/.local/bin/mesh-selfcare --test
doctor pid=1110259 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110259: 47 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148406: 1 timeout timeout 25 /home/mesh-home/.local/bin/mesh-sim-state --test
  1148819: 1 bash bash /home/mesh-home/.local/bin/mesh-sim-state --test
  1148838: 0 bash bash /home/mesh-home/.local/bin/mesh-sim-state --test
  1148872: 0 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1149021: 0 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1149061: 0 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1149121: 0 bash bash /home/mesh-home/.local/bin/mesh-peer-addr Redmi
doctor pid=1110326 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110326: gone
doctor pid=1110332 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110332: 42 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148768: 5 sleep sleep 8
doctor pid=1110360 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110360: 45 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
doctor pid=1110378 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110378: 44 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148585: 7 sleep sleep 8
doctor pid=1110384 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110384: gone
doctor pid=1110400 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110400: 45 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148590: 7 sleep sleep 8
doctor pid=1110404 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110404: 44 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148886: 7 sleep sleep 8
doctor pid=1110449 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110449: gone
doctor pid=1110460 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110460: 46 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148411: 1 timeout timeout 25 /home/mesh-home/.local/bin/mesh-socket-state --test
  1148424: 1 bash bash /home/mesh-home/.local/bin/mesh-socket-state --test
  1148745: 1 bash bash /home/mesh-home/.local/bin/mesh-socket-state --test
  1149191: 1 bash bash /home/mesh-home/.local/bin/mesh-socket-state --exposure
  1150539: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-socket-state --exposure
  1150543: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-socket-state --exposure
doctor pid=1110543 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110543: 36 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1149267: 15 timeout timeout 20 /home/mesh-home/.local/bin/mesh-tcp-metrics --test
  1149314: 15 bash bash /home/mesh-home/.local/bin/mesh-tcp-metrics --test
  1151244: 4123168608 bash /bin/bash /home/mesh-home/.local/bin/mesh-tcp-metrics --edge
  1151820: 4123168608 bash /bin/bash /home/mesh-home/.local/bin/mesh-tcp-metrics --edge
  1151841: 4123168608 sort sort -n
doctor pid=1110561 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110561: 50 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148425: 5 timeout timeout 25 /home/mesh-home/.local/bin/mesh-session-watchdog --test
  1148684: 4 bash bash /home/mesh-home/.local/bin/mesh-session-watchdog --test
  1152893: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-session-watchdog --test
  1152913: 4123168608 bash bash /home/mesh-home/.local/bin/mesh-session-watchdog --test
doctor pid=1110618 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110618: 52 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148827: 7 timeout timeout 25 /home/mesh-home/.local/bin/mesh-sense-map --test
  1148853: 7 python3 python3 /home/mesh-home/.local/bin/mesh-sense-map --test
doctor pid=1110634 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110634: 43 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148568: 5 sleep sleep 8
doctor pid=1110652 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110652: gone
doctor pid=1110708 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110708: 43 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148953: 5 sleep sleep 8
doctor pid=1110762 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110762: gone
doctor pid=1110770 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110770: gone
doctor pid=1110883 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110883: 41 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
doctor pid=1110994 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110994: 39 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1153234: 2 sleep sleep 8
doctor pid=1111039 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111039: 54 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1149060: 5 timeout timeout 20 /home/mesh-home/.local/bin/mesh-sense-reception --test
  1149149: 5 bash bash /home/mesh-home/.local/bin/mesh-sense-reception --test
  1151269: 2 bash bash /home/mesh-home/.local/bin/mesh-sense-reception --test
  1151325: 2 bash bash /home/mesh-home/.local/bin/mesh-sense-reception
  1153211: 2 bash bash /home/mesh-home/.local/bin/mesh-sense-reception
  1154022: 2 bash bash /home/mesh-home/.local/bin/mesh-sense-reception
  1154051: 2 timeout timeout 60 mesh-room-activity
  1154117: 2 bash bash /home/mesh-home/.local/bin/mesh-room-activity
  1154211: 2 bash bash /home/mesh-home/.local/bin/mesh-room-activity
  1154234: 2 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1154235: 2 tail tail -1
  1156038: 1 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1156041: 1 timeout timeout 4 ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@100.103.99.16 echo ok
  1156174: 1 ssh ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@100.103.99.16 echo ok
doctor pid=1111083 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111083: 42 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148940: 18 timeout timeout 20 /home/mesh-home/.local/bin/mesh-sync-tools --test
  1149079: 18 bash bash /home/mesh-home/.local/bin/mesh-sync-tools --test
  1162911: 0 bash bash /tmp/tmp.NTTk7NXyOO/td.mesh-sync-tools/mesh-sync-tools-test.fj6D9hvN/repo/scripts/mesh-sync-tools
  1163832: 4123168608 bash bash /tmp/tmp.NTTk7NXyOO/td.mesh-sync-tools/mesh-sync-tools-test.fj6D9hvN/repo/scripts/mesh-sync-tools
  1163851: 4123168608 bash bash /tmp/tmp.NTTk7NXyOO/td.mesh-sync-tools/mesh-sync-tools-test.fj6D9hvN/repo/scripts/mesh-sync-tools
  1163853: 4123168608 awk awk -F \t $4 == "tool" && $5 == "install" { print $1 }
  1163932: 4123168608 python3 python3 /tmp/tmp.NTTk7NXyOO/td.mesh-sync-tools/mesh-sync-tools-test.fj6D9hvN/repo/scripts/mesh-manifest --check
doctor pid=1111157 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111157: 41 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148874: 4 sleep sleep 8
doctor pid=1111161 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111161: gone
doctor pid=1111283 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111283: gone
doctor pid=1111390 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111390: 43 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148393: 6 sleep sleep 8
doctor pid=1111400 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111400: 48 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1156872: 3 timeout timeout 25 /home/mesh-home/.local/bin/mesh-ss-test --test
  1156918: 3 bash bash /home/mesh-home/.local/bin/mesh-ss-test --test
  1157113: 3 bash bash /home/mesh-home/.local/bin/mesh-ss-test --test
  1165733: 1 timeout timeout 10 ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -o BatchMode=yes 192.0.2.1 true
  1165804: 1 ssh ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -o BatchMode=yes 192.0.2.1 true
doctor pid=1111430 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111430: gone
doctor pid=1111524 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111524: gone
doctor pid=1111601 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111601: 46 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1165600: 2 sleep sleep 8
doctor pid=1111696 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111696: 55 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148716: 9 bash bash /home/mesh-home/.local/bin/mesh-perimeter --test
  1149626: 9 timeout timeout 25 /home/mesh-home/.local/bin/mesh-situation --test
  1149663: 9 bash bash /home/mesh-home/.local/bin/mesh-situation --test
  1152512: 5 bash bash /home/mesh-home/.local/bin/mesh-perimeter --test
  1152531: 5 timeout timeout 60 mesh-lan-newdevice --status
  1152605: 5 bash bash /home/mesh-home/.local/bin/mesh-lan-newdevice --status
  1166228: 2 bash bash /home/mesh-home/.local/bin/mesh-lan-newdevice --status
  1166247: 2 timeout timeout 12 ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=accept-new root@100.105.241.84 cat /tmp/dhcp.leases 2>/dev/null
  1166270: 2 ssh ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=accept-new root@100.105.241.84 cat /tmp/dhcp.leases 2>/dev/null
doctor pid=1111726 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111726: 52 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1149837: 7 timeout timeout 25 /home/mesh-home/.local/bin/mesh-soundscape --test
  1149902: 7 bash bash /home/mesh-home/.local/bin/mesh-soundscape --test
  1156268: 5 bash bash /home/mesh-home/.local/bin/mesh-soundscape --test
  1156273: 5 bash bash /home/mesh-home/.local/bin/mesh-soundscape --test
  1156275: 5 grep grep ^WINNER
  1156328: 5 python /home/mesh-home/grainneukeln/.venv/bin/python - /tmp/tmp.NTTk7NXyOO/td.mesh-soundscape/tmp.c8YDXAOMYf.wav 3,12,0 0.006 scan
doctor pid=1111884 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111884: gone
doctor pid=1111891 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111891: gone
doctor pid=1111958 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111958: gone
doctor pid=1112062 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1112062: 45 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1151598: 7 sleep sleep 8
doctor.log mtime=2026-09-14T03:24:03.120417+00:00 size=5564929
doctor.log tail:
2026-09-14T03:23:01Z  [33mWARN[0m mic DEFAULT device broken/busy (use -D plughw:N,M)
2026-09-14T03:23:01Z  [33mWARN[0m untimed peer-SSH — hangs on a dead peer:mesh-load-audit
2026-09-14T03:23:01Z  [33mWARN[0m 6 bypass(es) of 1 declared sole-path funnel(s) — the rule is recited but the arrangement is broken: librosa-analysis<- mesh-song-verify:94 librosa-analysis<- mesh-song-verify:95 librosa-analysis<- mesh-song-verify:102 librosa-analysis<- mesh-song-verify:109 librosa-analysis<- mesh-song-verify:111 librosa-analysis<- mesh-song-verify:114 
2026-09-14T03:23:01Z  [33mWARN[0m 5 site(s) render absence as a negative reading (absent path and bad reading → the SAME verdict word): A mesh-body-backup:452 SZ=0 -> :472 [-lt 20000000] FAIL A mesh-clear-health:41 reactor_age=1789356235 -> :42 [-gt 900] FAIL T mesh-random-track-grind:584 timeout -> :584 FAILED (rc=124 is a state, not a verdict) A mesh-revive:217 n=0 -> :364 [-lt 3] OFFLINE T mesh-say:432 timeout -> :445 FAILED (rc=124 is a state, not a verdict)

### 30-second sample 2026-09-14T03:26:39+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 217 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085654: 100 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085936: 100 timeout timeout 12 /home/mesh-home/.local/bin/mesh-restore --test
  1086231: 100 bash bash /home/mesh-home/.local/bin/mesh-restore --test
  1093623: 95 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110681: 74 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111039: 90 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1111083: 77 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1137059: 65 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1138105: 65 timeout timeout 12 /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1138204: 65 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1147113: 63 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1147833: 63 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148390: 62 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148625: 62 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148652: 50 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148809: 56 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148869: 59 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148958: 62 timeout timeout 12 /home/mesh-home/.local/bin/mesh-udev-stream --test
  1148969: 55 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1149006: 62 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
  1149030: 55 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1149099: 57 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1149292: 53 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1149535: 53 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1149602: 58 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1193326: 25 timeout timeout 25 /home/mesh-home/.local/bin/mesh-sync-tools --test
  1193354: 25 bash bash /home/mesh-home/.local/bin/mesh-sync-tools --test
  1196440: 24 timeout timeout 20 /home/mesh-home/.local/bin/mesh-voice-tx --test
  1196457: 24 bash bash /home/mesh-home/.local/bin/mesh-voice-tx --test
  1208936: 18 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1209248: 18 timeout timeout 25 /home/mesh-home/.local/bin/mesh-tv --test
  1209263: 18 bash bash /home/mesh-home/.local/bin/mesh-tv --test
  1209294: 18 python3 python3 /home/mesh-home/.local/bin/mesh-tv-dlna --test
  1209613: 17 timeout timeout 25 /home/mesh-home/.local/bin/mesh-tv-dlna --test
  1209649: 17 python3 python3 /home/mesh-home/.local/bin/mesh-tv-dlna --test
  1210945: 17 timeout timeout 25 /home/mesh-home/.local/bin/mesh-unit-churn --test
  1210955: 17 bash bash /home/mesh-home/.local/bin/mesh-unit-churn --test
  1211607: 16 timeout timeout 25 /home/mesh-home/.local/bin/mesh-tell --test
  1211626: 16 bash bash /home/mesh-home/.local/bin/mesh-tell --test
  1211722: 16 bash bash /home/mesh-home/.local/bin/mesh-tell --test
  1216936: 13 timeout timeout 25 /home/mesh-home/.local/bin/mesh-vitality --test
  1216956: 13 bash bash /home/mesh-home/.local/bin/mesh-vitality --test
  1217101: 13 bash bash /home/mesh-home/.local/bin/mesh-vitality --test
  1218129: 12 timeout timeout 25 /home/mesh-home/.local/bin/mesh-route-events --test
  1218152: 12 bash bash /home/mesh-home/.local/bin/mesh-route-events --test
  1220115: 11 timeout timeout 25 /home/mesh-home/.local/bin/mesh-voice-clone-daemon --test
  1220151: 11 mesh-voice-clon /home/mesh-home/.venv-ai/bin/python /home/mesh-home/.local/bin/mesh-voice-clone-daemon --test
  1220285: 11 python /home/mesh-home/.venv-ai/bin/python /home/mesh-home/.local/bin/mesh-voice-clone-daemon --test
  1221758: 10 timeout timeout 25 /home/mesh-home/.local/bin/mesh-vote --test
  1221770: 10 bash bash /home/mesh-home/.local/bin/mesh-vote --test
  1222124: 10 timeout timeout 25 /home/mesh-home/.local/bin/mesh-vpn-health --test
  1222136: 10 bash bash /home/mesh-home/.local/bin/mesh-vpn-health --test
  1222545: 10 bash bash /home/mesh-home/.local/bin/mesh-vpn-health --test
  1225492: 7 timeout timeout 25 /home/mesh-home/.local/bin/mesh-wchan --test
  1225511: 7 python3 python3 /home/mesh-home/.local/bin/mesh-wchan --test
  1225553: 7 timeout timeout 25 /home/mesh-home/.local/bin/mesh-whisper-run --test
  1225557: 7 bash bash /home/mesh-home/.local/bin/mesh-whisper-run --test
  1225584: 7 bash bash /home/mesh-home/.local/bin/mesh-whisper-run --test
  1231353: 4 bash bash /home/mesh-home/.local/bin/mesh-voice-tx --test
  1231675: 4 sleep sleep 8
  1231934: 4 bash bash /home/mesh-home/.local/bin/mesh-voice-tx --test
  1231935: 4 main /home/mesh-home/.mesh/whispercpp/main -m /home/mesh-home/.mesh/whispercpp/models/ggml-base.bin -f /tmp/tmp.NTTk7NXyOO/td.mesh-voice-tx/mvtx-lb-fMrAmw-16k.wav -l auto -nt -t 2
  1231938: 4 tr tr -d \r\n
  1231943: 4 timeout timeout 25 /home/mesh-home/.local/bin/mesh-witness --test
  1231951: 4 python3 python3 /home/mesh-home/.local/bin/mesh-witness --test
  1234680: 2 timeout timeout 25 /home/mesh-home/.local/bin/mesh-voice-print --test
  1234688: 2 python3 /home/mesh-home/.venv-ai/bin/python3 /home/mesh-home/.local/bin/mesh-voice-print --test
  1234931: 2 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
  1234933: 2 timeout timeout 3 udevadm monitor --udev
  1234939: 2 udevadm udevadm monitor --udev
  1235302: 2 bash bash /home/mesh-home/.local/bin/mesh-whisper-run --test
  1235310: 2 timeout timeout 240 /home/mesh-home/.local/bin/mesh-whisper-run -m /home/mesh-home/.mesh/whispercpp/models/ggml-base.bin -f /home/mesh-home/.mesh/whispercpp/sample-jfk.wav -nt -l auto
  1235312: 2 main /home/mesh-home/.mesh/whispercpp/main -m /home/mesh-home/.mesh/whispercpp/models/ggml-base.bin -f /home/mesh-home/.mesh/whispercpp/sample-jfk.wav -nt -l auto
  1235772: 2 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-wchan --json --log
  1235809: 1 bash bash /home/mesh-home/.local/bin/mesh-vpn-health --test
  1235845: 1 timeout timeout 90 bash /home/mesh-home/.local/bin/mesh-vpn-health --edge
  1235858: 1 bash bash /home/mesh-home/.local/bin/mesh-vpn-health --edge
  1235911: 1 sleep sleep 2
  1236243: 1 bash bash /home/mesh-home/.local/bin/mesh-vitality --test
  1236250: 1 bash bash /home/mesh-home/.local/bin/mesh-vitality --test
  1236258: 1 bash bash /home/mesh-home/.local/bin/mesh-vitality --test
  1236259: 1 awk awk -F \t $4 == "tool" && $5 == "install" { print $1 }
  1236273: 1 bash bash /home/mesh-home/.local/bin/mesh-mind-state --stats
  1238445: 0 bash bash /home/mesh-home/.local/bin/mesh-route-events --test
  1238453: 0 timeout timeout -k 5 45 sudo -n unshare -n env MESH_ROUTE_EVENTS_LOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.log MESH_ROUTE_EVENTS_COVF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.cov MESH_ROUTE_EVENTS_LOCK=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.lock MESH_ROUTE_EVENTS_STARTF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.started MESH_ROUTE_EVENTS_PIDF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.pid MESH_ROUTE_EVENTS_DLOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.dlog MESH_ROUTE_EVENTS_COV_S=2 MESH_ROUTE_EVENTS_MON_ARGS=route bash -c        ip link set lo up       setpriv --reuid=1000 --regid=1000 --clear-groups bash "/home/mesh-home/.local/bin/mesh-route-events" --daemon >>"/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.dlog" 2>&1       echo "rc=$?"
  1238471: 0 sudo sudo -n unshare -n env MESH_ROUTE_EVENTS_LOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.log MESH_ROUTE_EVENTS_COVF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.cov MESH_ROUTE_EVENTS_LOCK=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.lock MESH_ROUTE_EVENTS_STARTF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.started MESH_ROUTE_EVENTS_PIDF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.pid MESH_ROUTE_EVENTS_DLOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.dlog MESH_ROUTE_EVENTS_COV_S=2 MESH_ROUTE_EVENTS_MON_ARGS=route bash -c        ip link set lo up       setpriv --reuid=1000 --regid=1000 --clear-groups bash "/home/mesh-home/.local/bin/mesh-route-events" --daemon >>"/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.dlog" 2>&1       echo "rc=$?"
  1238645: 0 bash bash -c        ip link set lo up       setpriv --reuid=1000 --regid=1000 --clear-groups bash "/home/mesh-home/.local/bin/mesh-route-events" --daemon >>"/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.dlog" 2>&1       echo "rc=$?"
  1238680: 0 bash bash /home/mesh-home/.local/bin/mesh-route-events --daemon
  1239059: 0 ip ip -ts monitor label route
  1240055: 0 bash bash /tmp/tmp.NTTk7NXyOO/td.mesh-restore/tmp.E93sINoKuR/broken2 --test
  1240401: 0 python3 python3 /home/mesh-home/lte-workstation/scripts/mesh-manifest --list
  1240462: 0 bash bash /home/mesh-home/.local/bin/mesh-unit-churn --test
  1240465: 0 bash bash /home/mesh-home/.local/bin/mesh-unit-churn
  1240638: 0 bash bash /home/mesh-home/.local/bin/mesh-mind-state --stats
  1240643: 0 bash bash /home/mesh-home/.local/bin/mesh-mind-state --stats
  1240648: 0 bash bash -c pidx=$(tmux list-panes -t "$(hostname):senses" -F '#{pane_top} #{pane_index}' 2>/dev/null | sort -n | tail -1 | awk '{print $2}'); [ -n "$pidx" ] || exit 0; tty=$(tmux display-message -p -t "$(hostname):senses.$pidx" '#{pane_tty}' 2>/dev/null); [ -n "$tty" ] && ps -t "$tty" -o comm= 2>/dev/null
doctor pid=1085654 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085654: 100 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085936: 100 timeout timeout 12 /home/mesh-home/.local/bin/mesh-restore --test
  1086231: 100 bash bash /home/mesh-home/.local/bin/mesh-restore --test
  1240055: 0 bash bash /tmp/tmp.NTTk7NXyOO/td.mesh-restore/tmp.E93sINoKuR/broken2 --test
doctor pid=1093623 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1093623: 95 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1218129: 13 timeout timeout 25 /home/mesh-home/.local/bin/mesh-route-events --test
  1218152: 13 bash bash /home/mesh-home/.local/bin/mesh-route-events --test
  1238445: 1 bash bash /home/mesh-home/.local/bin/mesh-route-events --test
  1238453: 1 timeout timeout -k 5 45 sudo -n unshare -n env MESH_ROUTE_EVENTS_LOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.log MESH_ROUTE_EVENTS_COVF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.cov MESH_ROUTE_EVENTS_LOCK=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.lock MESH_ROUTE_EVENTS_STARTF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.started MESH_ROUTE_EVENTS_PIDF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.pid MESH_ROUTE_EVENTS_DLOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.dlog MESH_ROUTE_EVENTS_COV_S=2 MESH_ROUTE_EVENTS_MON_ARGS=route bash -c        ip link set lo up       setpriv --reuid=1000 --regid=1000 --clear-groups bash "/home/mesh-home/.local/bin/mesh-route-events" --daemon >>"/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.dlog" 2>&1       echo "rc=$?"
  1238471: 0 sudo sudo -n unshare -n env MESH_ROUTE_EVENTS_LOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.log MESH_ROUTE_EVENTS_COVF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.cov MESH_ROUTE_EVENTS_LOCK=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.lock MESH_ROUTE_EVENTS_STARTF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.started MESH_ROUTE_EVENTS_PIDF=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.pid MESH_ROUTE_EVENTS_DLOG=/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.dlog MESH_ROUTE_EVENTS_COV_S=2 MESH_ROUTE_EVENTS_MON_ARGS=route bash -c        ip link set lo up       setpriv --reuid=1000 --regid=1000 --clear-groups bash "/home/mesh-home/.local/bin/mesh-route-events" --daemon >>"/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.dlog" 2>&1       echo "rc=$?"
  1238645: 0 bash bash -c        ip link set lo up       setpriv --reuid=1000 --regid=1000 --clear-groups bash "/home/mesh-home/.local/bin/mesh-route-events" --daemon >>"/tmp/tmp.NTTk7NXyOO/td.mesh-route-events/tmp.xLIg8K82js/e.dlog" 2>&1       echo "rc=$?"
  1238680: 0 bash bash /home/mesh-home/.local/bin/mesh-route-events --daemon
  1239059: 0 ip ip -ts monitor label route
  1241291: 0 sleep sleep 0.2
doctor pid=1110681 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110681: 74 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1211607: 17 timeout timeout 25 /home/mesh-home/.local/bin/mesh-tell --test
  1211626: 17 bash bash /home/mesh-home/.local/bin/mesh-tell --test
  1211722: 17 bash bash /home/mesh-home/.local/bin/mesh-tell --test
doctor pid=1111039 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111039: 90 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1231675: 4 sleep sleep 8
doctor pid=1111083 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1111083: 78 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1193326: 26 timeout timeout 25 /home/mesh-home/.local/bin/mesh-sync-tools --test
  1193354: 26 bash bash /home/mesh-home/.local/bin/mesh-sync-tools --test
  1242231: 0 bash bash /tmp/tmp.NTTk7NXyOO/td.mesh-sync-tools/tmp.fctRxeS4WY/repo/scripts/mesh-sync-tools --apply
doctor pid=1137059 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1137059: 66 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1138105: 66 timeout timeout 12 /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1138204: 66 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1208936: 18 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
doctor pid=1147113 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1147113: 64 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1209248: 18 timeout timeout 25 /home/mesh-home/.local/bin/mesh-tv --test
  1209263: 18 bash bash /home/mesh-home/.local/bin/mesh-tv --test
  1209294: 18 python3 python3 /home/mesh-home/.local/bin/mesh-tv-dlna --test
doctor pid=1147833 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1147833: 64 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1209613: 18 timeout timeout 25 /home/mesh-home/.local/bin/mesh-tv-dlna --test
  1209649: 18 python3 python3 /home/mesh-home/.local/bin/mesh-tv-dlna --test
doctor pid=1148390 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1148390: 63 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1210945: 18 timeout timeout 25 /home/mesh-home/.local/bin/mesh-unit-churn --test
  1210955: 18 bash bash /home/mesh-home/.local/bin/mesh-unit-churn --test
  1242695: 0 bash bash /home/mesh-home/.local/bin/mesh-unit-churn --test
  1242696: 0 bash bash /home/mesh-home/.local/bin/mesh-unit-churn
doctor pid=1148625 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1148625: 63 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148958: 63 timeout timeout 12 /home/mesh-home/.local/bin/mesh-udev-stream --test
  1149006: 63 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
  1242006: 0 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
  1242365: 0 sleep sleep 1
doctor pid=1148652 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1148652: 51 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1231943: 5 timeout timeout 25 /home/mesh-home/.local/bin/mesh-witness --test
  1231951: 5 python3 python3 /home/mesh-home/.local/bin/mesh-witness --test
  1236273: 2 bash bash /home/mesh-home/.local/bin/mesh-mind-state --stats
doctor pid=1148809 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1148809: 57 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1196440: 25 timeout timeout 20 /home/mesh-home/.local/bin/mesh-voice-tx --test
  1196457: 25 bash bash /home/mesh-home/.local/bin/mesh-voice-tx --test
  1231353: 5 bash bash /home/mesh-home/.local/bin/mesh-voice-tx --test
  1231934: 5 bash bash /home/mesh-home/.local/bin/mesh-voice-tx --test
  1231935: 5 main /home/mesh-home/.mesh/whispercpp/main -m /home/mesh-home/.mesh/whispercpp/models/ggml-base.bin -f /tmp/tmp.NTTk7NXyOO/td.mesh-voice-tx/mvtx-lb-fMrAmw-16k.wav -l auto -nt -t 2
  1231938: 5 tr tr -d \r\n
doctor pid=1148869 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1148869: 60 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1216936: 14 timeout timeout 25 /home/mesh-home/.local/bin/mesh-vitality --test
  1216956: 14 bash bash /home/mesh-home/.local/bin/mesh-vitality --test
  1217101: 14 bash bash /home/mesh-home/.local/bin/mesh-vitality --test
  1236243: 2 bash bash /home/mesh-home/.local/bin/mesh-vitality --test
  1243327: 0 timeout timeout 20 python3 - /home/mesh-home/lte-workstation /home/mesh-home/.mesh/reflexes.cron
  1243330: 0 python3 python3 - /home/mesh-home/lte-workstation /home/mesh-home/.mesh/reflexes.cron
doctor pid=1148969 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1148969: 56 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1222124: 11 timeout timeout 25 /home/mesh-home/.local/bin/mesh-vpn-health --test
  1222136: 11 bash bash /home/mesh-home/.local/bin/mesh-vpn-health --test
  1222545: 11 bash bash /home/mesh-home/.local/bin/mesh-vpn-health --test
  1241382: 1 bash bash /home/mesh-home/.local/bin/mesh-vpn-health --test
  1241480: 1 timeout timeout 90 bash /home/mesh-home/.local/bin/mesh-vpn-health --edge
  1241500: 1 bash bash /home/mesh-home/.local/bin/mesh-vpn-health --edge
  1241554: 1 sleep sleep 2
doctor pid=1149030 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1149030: 57 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1221758: 11 timeout timeout 25 /home/mesh-home/.local/bin/mesh-vote --test
  1221770: 11 bash bash /home/mesh-home/.local/bin/mesh-vote --test
  1244207: 0 bash bash /home/mesh-home/.local/bin/mesh-vote dtopic --algo multipaxos
  1244273: 0 python3 python3 - /tmp/tmp.NTTk7NXyOO/td.mesh-vote/tmp.zll3quGk11/.mesh/vote-state/dtopic.json 0 0.66 /tmp/tmp.NTTk7NXyOO/td.mesh-vote/tmp.AYKYcIJSRp multipaxos  0 0
doctor pid=1149099 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1149099: 58 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1234680: 4 timeout timeout 25 /home/mesh-home/.local/bin/mesh-voice-print --test
  1234688: 4 python3 /home/mesh-home/.venv-ai/bin/python3 /home/mesh-home/.local/bin/mesh-voice-print --test
doctor pid=1149292 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1149292: 55 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1225492: 9 timeout timeout 25 /home/mesh-home/.local/bin/mesh-wchan --test
  1225511: 9 python3 python3 /home/mesh-home/.local/bin/mesh-wchan --test
  1235772: 3 python3 /usr/bin/python3 /home/mesh-home/.local/bin/mesh-wchan --json --log
doctor pid=1149535 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1149535: 54 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1225553: 9 timeout timeout 25 /home/mesh-home/.local/bin/mesh-whisper-run --test
  1225557: 9 bash bash /home/mesh-home/.local/bin/mesh-whisper-run --test
  1225584: 9 bash bash /home/mesh-home/.local/bin/mesh-whisper-run --test
  1235302: 3 bash bash /home/mesh-home/.local/bin/mesh-whisper-run --test
  1235310: 3 timeout timeout 240 /home/mesh-home/.local/bin/mesh-whisper-run -m /home/mesh-home/.mesh/whispercpp/models/ggml-base.bin -f /home/mesh-home/.mesh/whispercpp/sample-jfk.wav -nt -l auto
  1235312: 3 main /home/mesh-home/.mesh/whispercpp/main -m /home/mesh-home/.mesh/whispercpp/models/ggml-base.bin -f /home/mesh-home/.mesh/whispercpp/sample-jfk.wav -nt -l auto
doctor pid=1149602 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1149602: 59 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1220115: 13 timeout timeout 25 /home/mesh-home/.local/bin/mesh-voice-clone-daemon --test
  1220151: 13 mesh-voice-clon /home/mesh-home/.venv-ai/bin/python /home/mesh-home/.local/bin/mesh-voice-clone-daemon --test
  1220285: 13 python /home/mesh-home/.venv-ai/bin/python /home/mesh-home/.local/bin/mesh-voice-clone-daemon --test
doctor.log mtime=2026-09-14T03:24:03.120417+00:00 size=5564929
doctor.log tail:
2026-09-14T03:23:01Z  [33mWARN[0m mic DEFAULT device broken/busy (use -D plughw:N,M)
2026-09-14T03:23:01Z  [33mWARN[0m untimed peer-SSH — hangs on a dead peer:mesh-load-audit
2026-09-14T03:23:01Z  [33mWARN[0m 6 bypass(es) of 1 declared sole-path funnel(s) — the rule is recited but the arrangement is broken: librosa-analysis<- mesh-song-verify:94 librosa-analysis<- mesh-song-verify:95 librosa-analysis<- mesh-song-verify:102 librosa-analysis<- mesh-song-verify:109 librosa-analysis<- mesh-song-verify:111 librosa-analysis<- mesh-song-verify:114 
2026-09-14T03:23:01Z  [33mWARN[0m 5 site(s) render absence as a negative reading (absent path and bad reading → the SAME verdict word): A mesh-body-backup:452 SZ=0 -> :472 [-lt 20000000] FAIL A mesh-clear-health:41 reactor_age=1789356235 -> :42 [-gt 900] FAIL T mesh-random-track-grind:584 timeout -> :584 FAILED (rc=124 is a state, not a verdict) A mesh-revive:217 n=0 -> :364 [-lt 3] OFFLINE T mesh-say:432 timeout -> :445 FAILED (rc=124 is a state, not a verdict)

### 30-second sample 2026-09-14T03:27:10+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 249 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085654: 132 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1110681: 106 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1137059: 97 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1138105: 97 timeout timeout 12 /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1138204: 97 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1148625: 94 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148809: 88 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148958: 94 timeout timeout 12 /home/mesh-home/.local/bin/mesh-udev-stream --test
  1149006: 94 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
  1208936: 50 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1211607: 48 timeout timeout 25 /home/mesh-home/.local/bin/mesh-tell --test
  1211626: 48 bash bash /home/mesh-home/.local/bin/mesh-tell --test
  1211722: 48 bash bash /home/mesh-home/.local/bin/mesh-tell --test
  1280801: 14 timeout timeout 20 /home/mesh-home/.local/bin/mesh-restore --test
  1280804: 14 bash bash /home/mesh-home/.local/bin/mesh-restore --test
  1287801: 9 bash bash /home/mesh-home/.local/bin/mesh-tell --test
  1287802: 9 bash bash /home/mesh-home/.local/bin/mesh-tell --fresh --node nobody@203.0.113.1 mtell-fresh-fixture-1211722 remote nudge
  1293369: 6 timeout timeout 25 /home/mesh-home/.local/bin/mesh-voice-tx --test
  1293381: 6 bash bash /home/mesh-home/.local/bin/mesh-voice-tx --test
  1296318: 4 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
  1298612: 3 bash bash /home/mesh-home/.local/bin/mesh-restore --test
  1298617: 3 bash bash /home/mesh-home/.local/bin/mesh-restore --test
  1298833: 3 bash bash /home/mesh-home/.local/bin/mesh-voice-tx --test
  1299251: 3 bash bash /home/mesh-home/.local/bin/mesh-voice-tx --test
  1299255: 3 main /home/mesh-home/.mesh/whispercpp/main -m /home/mesh-home/.mesh/whispercpp/models/ggml-base.bin -f /tmp/tmp.NTTk7NXyOO/td.mesh-voice-tx/mvtx-lb-Vdn0pg-16k.wav -l auto -nt -t 2
  1299258: 3 tr tr -d \r\n
  1304090: 1 ssh ssh -o BatchMode=yes -o ConnectTimeout=8 nobody@203.0.113.1 if command -v mesh-codex-lifecycle >/dev/null 2>&1; then mesh-codex-lifecycle --ready 'mtell-fresh-fixture-1211722'; fi
  1308157: 0 sleep sleep 0.2
doctor pid=1085654 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085654: 132 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1280801: 14 timeout timeout 20 /home/mesh-home/.local/bin/mesh-restore --test
  1280804: 14 bash bash /home/mesh-home/.local/bin/mesh-restore --test
  1298612: 3 bash bash /home/mesh-home/.local/bin/mesh-restore --test
  1298617: 3 bash bash /home/mesh-home/.local/bin/mesh-restore --test
doctor pid=1110681 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1110681: 106 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1211607: 48 timeout timeout 25 /home/mesh-home/.local/bin/mesh-tell --test
  1211626: 48 bash bash /home/mesh-home/.local/bin/mesh-tell --test
  1211722: 48 bash bash /home/mesh-home/.local/bin/mesh-tell --test
  1287801: 9 bash bash /home/mesh-home/.local/bin/mesh-tell --test
  1287802: 9 bash bash /home/mesh-home/.local/bin/mesh-tell --fresh --node nobody@203.0.113.1 mtell-fresh-fixture-1211722 remote nudge
  1304090: 1 ssh ssh -o BatchMode=yes -o ConnectTimeout=8 nobody@203.0.113.1 if command -v mesh-codex-lifecycle >/dev/null 2>&1; then mesh-codex-lifecycle --ready 'mtell-fresh-fixture-1211722'; fi
doctor pid=1137059 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1137059: 98 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1138105: 97 timeout timeout 12 /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1138204: 97 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1208936: 50 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
doctor pid=1148625 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1148625: 94 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148958: 94 timeout timeout 12 /home/mesh-home/.local/bin/mesh-udev-stream --test
  1149006: 94 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
  1309399: 0 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
  1309403: 0 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --status
  1309489: 0 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --status
doctor pid=1148809 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1148809: 88 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1293369: 7 timeout timeout 25 /home/mesh-home/.local/bin/mesh-voice-tx --test
  1293381: 7 bash bash /home/mesh-home/.local/bin/mesh-voice-tx --test
  1298833: 4 bash bash /home/mesh-home/.local/bin/mesh-voice-tx --test
  1299251: 4 bash bash /home/mesh-home/.local/bin/mesh-voice-tx --test
  1299255: 4 main /home/mesh-home/.mesh/whispercpp/main -m /home/mesh-home/.mesh/whispercpp/models/ggml-base.bin -f /tmp/tmp.NTTk7NXyOO/td.mesh-voice-tx/mvtx-lb-Vdn0pg-16k.wav -l auto -nt -t 2
  1299258: 4 tr tr -d \r\n
doctor.log mtime=2026-09-14T03:24:03.120417+00:00 size=5564929
doctor.log tail:
2026-09-14T03:23:01Z  [33mWARN[0m mic DEFAULT device broken/busy (use -D plughw:N,M)
2026-09-14T03:23:01Z  [33mWARN[0m untimed peer-SSH — hangs on a dead peer:mesh-load-audit
2026-09-14T03:23:01Z  [33mWARN[0m 6 bypass(es) of 1 declared sole-path funnel(s) — the rule is recited but the arrangement is broken: librosa-analysis<- mesh-song-verify:94 librosa-analysis<- mesh-song-verify:95 librosa-analysis<- mesh-song-verify:102 librosa-analysis<- mesh-song-verify:109 librosa-analysis<- mesh-song-verify:111 librosa-analysis<- mesh-song-verify:114 
2026-09-14T03:23:01Z  [33mWARN[0m 5 site(s) render absence as a negative reading (absent path and bad reading → the SAME verdict word): A mesh-body-backup:452 SZ=0 -> :472 [-lt 20000000] FAIL A mesh-clear-health:41 reactor_age=1789356235 -> :42 [-gt 900] FAIL T mesh-random-track-grind:584 timeout -> :584 FAILED (rc=124 is a state, not a verdict) A mesh-revive:217 n=0 -> :364 [-lt 3] OFFLINE T mesh-say:432 timeout -> :445 FAILED (rc=124 is a state, not a verdict)

### 30-second sample 2026-09-14T03:27:41+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 279 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1085654: 163 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1137059: 128 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148625: 125 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1337750: 15 timeout timeout 20 /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1337754: 15 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1350227: 10 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1370332: 3 timeout timeout 25 /home/mesh-home/.local/bin/mesh-restore --test
  1370336: 3 bash bash /home/mesh-home/.local/bin/mesh-restore --test
  1371182: 2 sleep sleep 5
  1375427: 0 sleep sleep 0.2
doctor pid=1085654 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1085654: 163 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1370332: 3 timeout timeout 25 /home/mesh-home/.local/bin/mesh-restore --test
  1370336: 3 bash bash /home/mesh-home/.local/bin/mesh-restore --test
  1375427: 0 sleep sleep 0.2
doctor pid=1137059 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1137059: 128 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1337750: 15 timeout timeout 20 /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1337754: 15 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1350227: 10 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
doctor pid=1148625 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1148625: 125 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1371182: 2 sleep sleep 5
doctor.log mtime=2026-09-14T03:24:03.120417+00:00 size=5564929
doctor.log tail:
2026-09-14T03:23:01Z  [33mWARN[0m mic DEFAULT device broken/busy (use -D plughw:N,M)
2026-09-14T03:23:01Z  [33mWARN[0m untimed peer-SSH — hangs on a dead peer:mesh-load-audit
2026-09-14T03:23:01Z  [33mWARN[0m 6 bypass(es) of 1 declared sole-path funnel(s) — the rule is recited but the arrangement is broken: librosa-analysis<- mesh-song-verify:94 librosa-analysis<- mesh-song-verify:95 librosa-analysis<- mesh-song-verify:102 librosa-analysis<- mesh-song-verify:109 librosa-analysis<- mesh-song-verify:111 librosa-analysis<- mesh-song-verify:114 
2026-09-14T03:23:01Z  [33mWARN[0m 5 site(s) render absence as a negative reading (absent path and bad reading → the SAME verdict word): A mesh-body-backup:452 SZ=0 -> :472 [-lt 20000000] FAIL A mesh-clear-health:41 reactor_age=1789356235 -> :42 [-gt 900] FAIL T mesh-random-track-grind:584 timeout -> :584 FAILED (rc=124 is a state, not a verdict) A mesh-revive:217 n=0 -> :364 [-lt 3] OFFLINE T mesh-say:432 timeout -> :445 FAILED (rc=124 is a state, not a verdict)

### 30-second sample 2026-09-14T03:28:12+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 310 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1137059: 158 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148625: 155 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1381729: 27 timeout timeout 20 /home/mesh-home/.local/bin/mesh-udev-stream --test
  1381732: 27 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
  1419245: 13 timeout timeout 25 /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1419247: 13 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1428683: 9 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1457504: 0 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
  1457568: 0 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
doctor pid=1137059 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1137059: 158 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1419245: 13 timeout timeout 25 /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1419247: 13 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
  1428683: 9 bash bash /home/mesh-home/.local/bin/mesh-tmp-guard --test
doctor pid=1148625 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1148625: 155 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1381729: 28 timeout timeout 20 /home/mesh-home/.local/bin/mesh-udev-stream --test
  1381732: 28 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
  1457504: 0 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
  1457568: 0 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
doctor.log mtime=2026-09-14T03:24:03.120417+00:00 size=5564929
doctor.log tail:
2026-09-14T03:23:01Z  [33mWARN[0m mic DEFAULT device broken/busy (use -D plughw:N,M)
2026-09-14T03:23:01Z  [33mWARN[0m untimed peer-SSH — hangs on a dead peer:mesh-load-audit
2026-09-14T03:23:01Z  [33mWARN[0m 6 bypass(es) of 1 declared sole-path funnel(s) — the rule is recited but the arrangement is broken: librosa-analysis<- mesh-song-verify:94 librosa-analysis<- mesh-song-verify:95 librosa-analysis<- mesh-song-verify:102 librosa-analysis<- mesh-song-verify:109 librosa-analysis<- mesh-song-verify:111 librosa-analysis<- mesh-song-verify:114 
2026-09-14T03:23:01Z  [33mWARN[0m 5 site(s) render absence as a negative reading (absent path and bad reading → the SAME verdict word): A mesh-body-backup:452 SZ=0 -> :472 [-lt 20000000] FAIL A mesh-clear-health:41 reactor_age=1789356235 -> :42 [-gt 900] FAIL T mesh-random-track-grind:584 timeout -> :584 FAILED (rc=124 is a state, not a verdict) A mesh-revive:217 n=0 -> :364 [-lt 3] OFFLINE T mesh-say:432 timeout -> :445 FAILED (rc=124 is a state, not a verdict)

### 30-second sample 2026-09-14T03:28:42+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 340 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148625: 185 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1505178: 10 timeout timeout 25 /home/mesh-home/.local/bin/mesh-udev-stream --test
  1505179: 10 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
  1528392: 0 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --check
  1528583: 0 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --check
doctor pid=1148625 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1148625: 185 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1505178: 10 timeout timeout 25 /home/mesh-home/.local/bin/mesh-udev-stream --test
  1505179: 10 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
  1528392: 0 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --check
  1528583: 0 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --check
doctor.log mtime=2026-09-14T03:24:03.120417+00:00 size=5564929
doctor.log tail:
2026-09-14T03:23:01Z  [33mWARN[0m mic DEFAULT device broken/busy (use -D plughw:N,M)
2026-09-14T03:23:01Z  [33mWARN[0m untimed peer-SSH — hangs on a dead peer:mesh-load-audit
2026-09-14T03:23:01Z  [33mWARN[0m 6 bypass(es) of 1 declared sole-path funnel(s) — the rule is recited but the arrangement is broken: librosa-analysis<- mesh-song-verify:94 librosa-analysis<- mesh-song-verify:95 librosa-analysis<- mesh-song-verify:102 librosa-analysis<- mesh-song-verify:109 librosa-analysis<- mesh-song-verify:111 librosa-analysis<- mesh-song-verify:114 
2026-09-14T03:23:01Z  [33mWARN[0m 5 site(s) render absence as a negative reading (absent path and bad reading → the SAME verdict word): A mesh-body-backup:452 SZ=0 -> :472 [-lt 20000000] FAIL A mesh-clear-health:41 reactor_age=1789356235 -> :42 [-gt 900] FAIL T mesh-random-track-grind:584 timeout -> :584 FAILED (rc=124 is a state, not a verdict) A mesh-revive:217 n=0 -> :364 [-lt 3] OFFLINE T mesh-say:432 timeout -> :445 FAILED (rc=124 is a state, not a verdict)

### 30-second sample 2026-09-14T03:29:12+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 370 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1148625: 215 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1505178: 40 timeout timeout 25 /home/mesh-home/.local/bin/mesh-udev-stream --test
  1505179: 40 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
doctor pid=1148625 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1148625: 216 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1505178: 40 timeout timeout 25 /home/mesh-home/.local/bin/mesh-udev-stream --test
  1505179: 40 bash bash /home/mesh-home/.local/bin/mesh-udev-stream --test
doctor.log mtime=2026-09-14T03:24:03.120417+00:00 size=5564929
doctor.log tail:
2026-09-14T03:23:01Z  [33mWARN[0m mic DEFAULT device broken/busy (use -D plughw:N,M)
2026-09-14T03:23:01Z  [33mWARN[0m untimed peer-SSH — hangs on a dead peer:mesh-load-audit
2026-09-14T03:23:01Z  [33mWARN[0m 6 bypass(es) of 1 declared sole-path funnel(s) — the rule is recited but the arrangement is broken: librosa-analysis<- mesh-song-verify:94 librosa-analysis<- mesh-song-verify:95 librosa-analysis<- mesh-song-verify:102 librosa-analysis<- mesh-song-verify:109 librosa-analysis<- mesh-song-verify:111 librosa-analysis<- mesh-song-verify:114 
2026-09-14T03:23:01Z  [33mWARN[0m 5 site(s) render absence as a negative reading (absent path and bad reading → the SAME verdict word): A mesh-body-backup:452 SZ=0 -> :472 [-lt 20000000] FAIL A mesh-clear-health:41 reactor_age=1789356235 -> :42 [-gt 900] FAIL T mesh-random-track-grind:584 timeout -> :584 FAILED (rc=124 is a state, not a verdict) A mesh-revive:217 n=0 -> :364 [-lt 3] OFFLINE T mesh-say:432 timeout -> :445 FAILED (rc=124 is a state, not a verdict)

### 30-second sample 2026-09-14T03:29:42+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 400 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1642242: 23 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1642283: 23 timeout timeout 60 /home/mesh-home/.local/bin/mesh-social-context --test
  1642285: 23 bash bash /home/mesh-home/.local/bin/mesh-social-context --test
  1642297: 23 bash bash /home/mesh-home/.local/bin/mesh-social-context --test
  1679196: 2 timeout timeout 120 /home/mesh-home/.local/bin/mesh-social-context
  1679200: 2 bash bash /home/mesh-home/.local/bin/mesh-social-context
  1679220: 2 bash bash /home/mesh-home/.local/bin/mesh-social-context
  1679222: 2 timeout timeout 12 mesh-body-motion
  1679224: 2 bash bash /home/mesh-home/.local/bin/mesh-body-motion
  1679229: 2 bash bash /home/mesh-home/.local/bin/mesh-body-motion
  1679230: 2 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1679288: 2 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1679290: 2 timeout timeout 4 ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@100.103.99.16 echo ok
  1679293: 2 ssh ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@100.103.99.16 echo ok
doctor pid=1642242 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1642242: 23 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1642283: 23 timeout timeout 60 /home/mesh-home/.local/bin/mesh-social-context --test
  1642285: 23 bash bash /home/mesh-home/.local/bin/mesh-social-context --test
  1642297: 23 bash bash /home/mesh-home/.local/bin/mesh-social-context --test
  1679196: 3 timeout timeout 120 /home/mesh-home/.local/bin/mesh-social-context
  1679200: 3 bash bash /home/mesh-home/.local/bin/mesh-social-context
  1679220: 3 bash bash /home/mesh-home/.local/bin/mesh-social-context
  1679222: 3 timeout timeout 12 mesh-body-motion
  1679224: 3 bash bash /home/mesh-home/.local/bin/mesh-body-motion
  1679229: 3 bash bash /home/mesh-home/.local/bin/mesh-body-motion
  1679230: 3 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1679288: 2 bash bash /home/mesh-home/.local/bin/mesh-phone-ip
  1679290: 2 timeout timeout 4 ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@100.103.99.16 echo ok
  1679293: 2 ssh ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=3 -o StrictHostKeyChecking=accept-new u0_a380@100.103.99.16 echo ok
doctor.log mtime=2026-09-14T03:24:03.120417+00:00 size=5564929
doctor.log tail:
2026-09-14T03:23:01Z  [33mWARN[0m mic DEFAULT device broken/busy (use -D plughw:N,M)
2026-09-14T03:23:01Z  [33mWARN[0m untimed peer-SSH — hangs on a dead peer:mesh-load-audit
2026-09-14T03:23:01Z  [33mWARN[0m 6 bypass(es) of 1 declared sole-path funnel(s) — the rule is recited but the arrangement is broken: librosa-analysis<- mesh-song-verify:94 librosa-analysis<- mesh-song-verify:95 librosa-analysis<- mesh-song-verify:102 librosa-analysis<- mesh-song-verify:109 librosa-analysis<- mesh-song-verify:111 librosa-analysis<- mesh-song-verify:114 
2026-09-14T03:23:01Z  [33mWARN[0m 5 site(s) render absence as a negative reading (absent path and bad reading → the SAME verdict word): A mesh-body-backup:452 SZ=0 -> :472 [-lt 20000000] FAIL A mesh-clear-health:41 reactor_age=1789356235 -> :42 [-gt 900] FAIL T mesh-random-track-grind:584 timeout -> :584 FAILED (rc=124 is a state, not a verdict) A mesh-revive:217 n=0 -> :364 [-lt 3] OFFLINE T mesh-say:432 timeout -> :445 FAILED (rc=124 is a state, not a verdict)

### 30-second sample 2026-09-14T03:30:12+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 430 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1642242: 53 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1642283: 53 timeout timeout 60 /home/mesh-home/.local/bin/mesh-social-context --test
  1642285: 53 bash bash /home/mesh-home/.local/bin/mesh-social-context --test
  1642297: 53 bash bash /home/mesh-home/.local/bin/mesh-social-context --test
  1702550: 12 timeout timeout 120 /home/mesh-home/.local/bin/mesh-social-context
  1702553: 12 bash bash /home/mesh-home/.local/bin/mesh-social-context
  1743939: 0 bash bash /home/mesh-home/.local/bin/mesh-social-context
  1743949: 0 timeout timeout 10 mesh-light
  1743957: 0 bash bash /home/mesh-home/.local/bin/mesh-light
  1744093: 0 bash bash /home/mesh-home/.local/bin/mesh-light
  1744097: 0 bash bash /home/mesh-home/.local/bin/mesh-light
  1744102: 0 timeout timeout 14 ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=6 u0_a380@192.168.8.203 termux-sensor -s tmd2755_l -d 500 -n 2 2>/dev/null
  1744107: 0 ssh ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=6 u0_a380@192.168.8.203 termux-sensor -s tmd2755_l -d 500 -n 2 2>/dev/null
doctor pid=1642242 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  1642242: 53 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
  1642283: 53 timeout timeout 60 /home/mesh-home/.local/bin/mesh-social-context --test
  1642285: 53 bash bash /home/mesh-home/.local/bin/mesh-social-context --test
  1642297: 53 bash bash /home/mesh-home/.local/bin/mesh-social-context --test
  1702550: 12 timeout timeout 120 /home/mesh-home/.local/bin/mesh-social-context
  1702553: 12 bash bash /home/mesh-home/.local/bin/mesh-social-context
  1743939: 0 bash bash /home/mesh-home/.local/bin/mesh-social-context
  1743949: 0 timeout timeout 10 mesh-light
  1743957: 0 bash bash /home/mesh-home/.local/bin/mesh-light
  1744093: 0 bash bash /home/mesh-home/.local/bin/mesh-light
  1744097: 0 bash bash /home/mesh-home/.local/bin/mesh-light
  1744102: 0 timeout timeout 14 ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=6 u0_a380@192.168.8.203 termux-sensor -s tmd2755_l -d 500 -n 2 2>/dev/null
  1744107: 0 ssh ssh -p 8022 -o BatchMode=yes -o ConnectTimeout=6 u0_a380@192.168.8.203 termux-sensor -s tmd2755_l -d 500 -n 2 2>/dev/null
doctor.log mtime=2026-09-14T03:24:03.120417+00:00 size=5564929
doctor.log tail:
2026-09-14T03:23:01Z  [33mWARN[0m mic DEFAULT device broken/busy (use -D plughw:N,M)
2026-09-14T03:23:01Z  [33mWARN[0m untimed peer-SSH — hangs on a dead peer:mesh-load-audit
2026-09-14T03:23:01Z  [33mWARN[0m 6 bypass(es) of 1 declared sole-path funnel(s) — the rule is recited but the arrangement is broken: librosa-analysis<- mesh-song-verify:94 librosa-analysis<- mesh-song-verify:95 librosa-analysis<- mesh-song-verify:102 librosa-analysis<- mesh-song-verify:109 librosa-analysis<- mesh-song-verify:111 librosa-analysis<- mesh-song-verify:114 
2026-09-14T03:23:01Z  [33mWARN[0m 5 site(s) render absence as a negative reading (absent path and bad reading → the SAME verdict word): A mesh-body-backup:452 SZ=0 -> :472 [-lt 20000000] FAIL A mesh-clear-health:41 reactor_age=1789356235 -> :42 [-gt 900] FAIL T mesh-random-track-grind:584 timeout -> :584 FAILED (rc=124 is a state, not a verdict) A mesh-revive:217 n=0 -> :364 [-lt 3] OFFLINE T mesh-say:432 timeout -> :445 FAILED (rc=124 is a state, not a verdict)

### 30-second sample 2026-09-14T03:30:42+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 461 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
doctor.log mtime=2026-09-14T03:30:41.688208+00:00 size=5573704
doctor.log tail:
2026-09-14T03:23:01Z  [33mWARN[0m --test UNASSESSED (budget spent before the runner reached them — NOT absent hardware, NOT a verdict on the tool): never assessed: mesh-ss-test | last assessed: mesh-song-verify(2d) mesh-sound-reflex(2d) mesh-soundscape(2d) mesh-spend(2d) mesh-ss-connections(2d) mesh-stop-check(2d) mesh-stranger-watch(2d) mesh-stress(2d) mesh-sync-tools(20d) mesh-synergy(2d) mesh-tailscaled-heal(2d) mesh-task(2d) mesh-tell(2d) mesh-test-forgery(2d) mesh-tg-update(2d) mesh-tiny-fleet(2d) mesh-tiny-fleet-snapshot(2d) mesh-tmp-guard(2d) mesh-transcribe-organ(2d) mesh-tv(2d) mesh-tv-dlna(2d) mesh-udev-stream(2d) mesh-usb(2d) mesh-vitality(2d) mesh-voice-clone-daemon(2d) mesh-vpn-health(15d) mesh-whisper-run(2d) mesh-wifi-quality(2d) mesh-witness(2d) mesh-activity-tempo(1d) mesh-algedonic(1d) mesh-ambient-clock(1d) mesh-approach(1d) mesh-autowire(1d) mesh-awaydigest(1d) mesh-ble-heal(1d) mesh-ble-recut-arm(1d) mesh-bruno(1d) mesh-bruno-watch(1d) mesh-bt-lock-verdict(1d) mesh-budget(1d) mesh-card(1d) mesh-card-watchdog(1d) mesh-channel-keepalive(1d) mesh-chat(1d) mesh-chat-review(1d) mesh-claude-deepseek(1d) mesh-clear-audit(1d) mesh-closure(1d) mesh-convexity(1d) mesh-cooscillate(1d) mesh-correlate(1d) mesh-criticality(1d) mesh-cron-catchup(1d) mesh-cstate(1d) mesh-dash(1d) mesh-devcd-catch(1d) mesh-device-churn(1d) mesh-digest(1d) mesh-dispatch(1d) mesh-dms(1d) mesh-docstore(1d) mesh-doctor(1d) mesh-edge-gate-audit(1d) mesh-egress-health(1d) mesh-exit-node-lan-heal(1d) mesh-fitness(1d) mesh-forage(1d) mesh-fsnotify(1d) mesh-fswriter(1d) mesh-generate(1d) mesh-gmail-note3(1d) mesh-guardian(1d) mesh-guitar-watch(1d) mesh-handoff(1d) mesh-heartbeat(1d) mesh-heavy-run(1d) mesh-hh-drive(1d) mesh-hire-scan(1d) mesh-hire-submit(1d) mesh-historical-ask-ledger(1d) mesh-home-state(1d) mesh-homeostasis(1d) mesh-hw-fault-watch(1d) mesh-hw-health(1d) mesh-ideate(1d) mesh-imac-wifi(1d) mesh-interruptibility(1d) mesh-job-apply(1d) mesh-job-calls(1d) mesh-job-chatwatch(1d) mesh-job-mail(1d) mesh-job-scan(5d) mesh-job-track(5d) mesh-journal-watch(1d) mesh-labor(1d) mesh-lan-newdevice(1d) mesh-lan6(1d) mesh-land(1d) mesh-leadlag(1d) mesh-ledger(1d) mesh-llama-vision(1d) mesh-load-attrib(1d) mesh-load-audit(1d) mesh-load-gate(1d) mesh-lock-holder(1d) mesh-mca(1d) mesh-media-scene(1d) mesh-mem-guard(1d) mesh-mind-compact(1d) mesh-mind-control(1d) mesh-mind-state(1d) mesh-misha-wake(1d) mesh-mlme-tap(3d) mesh-model-bench(1d) mesh-model-swap(1d) mesh-music-fanout(1d) mesh-music-session(1d) mesh-node-care(1d) mesh-note3-light-raw(1d) mesh-note3-ui(1d) mesh-observer-effect(1d) mesh-opencode-plugins(1d) mesh-operator-hands(1d) mesh-organ-keepalive(1d) mesh-overhear(1d) mesh-pace(15h) mesh-pane-consume(15h) mesh-path-watch(15h) mesh-pcie-health(15h) mesh-perimeter(14h) mesh-phone-ap(14h) mesh-pidfile.sh(14h) mesh-pkg-watch(14h) mesh-precision(14h) mesh-prior-art(14h) mesh-promises(13h) mesh-promises-watch(13h) mesh-promises.bak-20260912-witness(13h) mesh-psi(12h) mesh-queue-tend(12h) mesh-quota-react(12h) mesh-records(10h) mesh-reflex-health(9h) mesh-reflexes(9h) mesh-report(9h) mesh-resource-guard(9h) mesh-restore(3d) mesh-revive(7h) mesh-rhythm(3d) mesh-roll-call(6h) mesh-roll-call-retire-arm(6h) mesh-room-address(6h) mesh-room-gigaam(6h) mesh-room-music(6h) mesh-route-events(14d) mesh-rq-wait(6h) mesh-say(6h) mesh-selfcare(6h) mesh-sense-map(3h) mesh-sense-reception(4d) mesh-series-stats(1h) mesh-session-watchdog(1h) mesh-situation(1h)
2026-09-14T03:23:01Z  [33mWARN[0m --test FAIL(stale) — the age in each token is the age of the CONFIRM (where a serial confirm last REACHED this tool and found it red), NOT the age of a live fault: the rotation has not returned to it since, so a tool repaired AFTER that date renders here exactly like one still broken. These are NOT counted in the headline's FAIL, because that count is edge-triggered for the board and a carried-forward red must not re-alarm hourly. NOTHING in this list re-confirms anything: each token states only what THIS run's parallel probe returned for that tool, and a probe that TIMED-OUT or DID-NOT-REPORT is a state, never a verdict — so RE-RUN the --test before acting on, or deferring, any of these. A SUBJECT-MOVED token means the arm failing NOW is not the one the confirm measured, so the age is the NEW subject's and the confirmation's is stated beside it — do not read that red as old, and do not assume the task someone already took is about it: mesh-tiny-fleet(confirmed-2d-ago,this-run:probe-red-rc1) mesh-tiny-fleet-snapshot(confirmed-2d-ago,this-run:probe-red-rc128) mesh-tv(confirmed-2d-ago,this-run:probe-red-rc1) mesh-tv-dlna(confirmed-2d-ago,this-run:probe-red-rc1) mesh-usb(confirmed-2d-ago,this-run:probe-red-rc1) mesh-wifi-quality(confirmed-2d-ago,this-run:probe-red-rc1) mesh-ble-heal(confirmed-1d-ago,this-run:probe-red-rc1) mesh-claude-deepseek(confirmed-1d-ago,this-run:probe-red-rc1) mesh-fsnotify(confirmed-1d-ago,this-run:probe-TIMED-OUT-not-a-verdict) mesh-historical-ask-ledger(confirmed-1d-ago,this-run:probe-red-rc1) mesh-lan6(confirmed-1d-ago,this-run:probe-red-rc1) mesh-model-swap(confirmed-1d-ago,this-run:probe-red-rc1) mesh-opencode-plugins(confirmed-1d-ago,this-run:probe-red-rc1) mesh-report(confirmed-9h-ago,this-run:probe-TIMED-OUT-not-a-verdict) mesh-restore(confirmed-3d-ago,this-run:probe-red-rc1) mesh-selfcare(confirmed-6h-ago,this-run:probe-TIMED-OUT-not-a-verdict) mesh-sense-reception(new-subject-age-UNKNOWN-first-sighting,SUBJECT-MOVED,confirmed-4d-ago-against-a-different-one,this-run:probe-TIMED-OUT-not-a-verdict) mesh-series-stats(confirmed-1h-ago,this-run:probe-red-rc1)
2026-09-14T03:23:01Z  [33mWARN[0m --test TOO SLOW TO ASSESS (ran the full 60s serial-confirm window and did not finish — a timeout is not a verdict, so this is NOT a FAIL and NOT 'no hardware'; the suite wants a fast core: add '# test-fast: yes' + a --test-fast entry point and the doctor will drive that): mesh-social-context
2026-09-14T03:23:01Z  [33mWARN[0m printf+\n-empty-input fragile (empty var → spurious newline → wc-l miscounts by 1; guard with [ -n "$var" ]): mesh-board-id:208 mesh-channel-keepalive:1186 mesh-channel-keepalive:1368 mesh-convexity:1146 mesh-convexity:1149 mesh-cppc:275 mesh-dash:2135 mesh-dash:254 mesh-edge-gate-audit:325 mesh-edge-gate-audit:328 mesh-edge-gate-audit:332 mesh-lan-newdevice:797 mesh-load-audit:1143 mesh-load-audit:1570 mesh-nvme-internal-gradient:68 mesh-patterns.sh:787 mesh-patterns.sh:798 mesh-patterns.sh:809 mesh-patterns.sh:817 mesh-peer-addr:100 mesh-proximity:474 mesh-psi-attrib:317 mesh-random-track-grind:289 mesh-room-music:1001 mesh-room-music:1105 mesh-room-music:1106 mesh-room-sense:1028 mesh-sound-reflex:6266 mesh-sound-reflex:6279 mesh-tcp-attrib:269 mesh-wifi-motion:1140 test-chaos-drill:100

### 30-second sample 2026-09-14T03:31:13+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 491 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
doctor.log mtime=2026-09-14T03:30:41.688208+00:00 size=5573704
doctor.log tail:
2026-09-14T03:23:01Z  [33mWARN[0m --test UNASSESSED (budget spent before the runner reached them — NOT absent hardware, NOT a verdict on the tool): never assessed: mesh-ss-test | last assessed: mesh-song-verify(2d) mesh-sound-reflex(2d) mesh-soundscape(2d) mesh-spend(2d) mesh-ss-connections(2d) mesh-stop-check(2d) mesh-stranger-watch(2d) mesh-stress(2d) mesh-sync-tools(20d) mesh-synergy(2d) mesh-tailscaled-heal(2d) mesh-task(2d) mesh-tell(2d) mesh-test-forgery(2d) mesh-tg-update(2d) mesh-tiny-fleet(2d) mesh-tiny-fleet-snapshot(2d) mesh-tmp-guard(2d) mesh-transcribe-organ(2d) mesh-tv(2d) mesh-tv-dlna(2d) mesh-udev-stream(2d) mesh-usb(2d) mesh-vitality(2d) mesh-voice-clone-daemon(2d) mesh-vpn-health(15d) mesh-whisper-run(2d) mesh-wifi-quality(2d) mesh-witness(2d) mesh-activity-tempo(1d) mesh-algedonic(1d) mesh-ambient-clock(1d) mesh-approach(1d) mesh-autowire(1d) mesh-awaydigest(1d) mesh-ble-heal(1d) mesh-ble-recut-arm(1d) mesh-bruno(1d) mesh-bruno-watch(1d) mesh-bt-lock-verdict(1d) mesh-budget(1d) mesh-card(1d) mesh-card-watchdog(1d) mesh-channel-keepalive(1d) mesh-chat(1d) mesh-chat-review(1d) mesh-claude-deepseek(1d) mesh-clear-audit(1d) mesh-closure(1d) mesh-convexity(1d) mesh-cooscillate(1d) mesh-correlate(1d) mesh-criticality(1d) mesh-cron-catchup(1d) mesh-cstate(1d) mesh-dash(1d) mesh-devcd-catch(1d) mesh-device-churn(1d) mesh-digest(1d) mesh-dispatch(1d) mesh-dms(1d) mesh-docstore(1d) mesh-doctor(1d) mesh-edge-gate-audit(1d) mesh-egress-health(1d) mesh-exit-node-lan-heal(1d) mesh-fitness(1d) mesh-forage(1d) mesh-fsnotify(1d) mesh-fswriter(1d) mesh-generate(1d) mesh-gmail-note3(1d) mesh-guardian(1d) mesh-guitar-watch(1d) mesh-handoff(1d) mesh-heartbeat(1d) mesh-heavy-run(1d) mesh-hh-drive(1d) mesh-hire-scan(1d) mesh-hire-submit(1d) mesh-historical-ask-ledger(1d) mesh-home-state(1d) mesh-homeostasis(1d) mesh-hw-fault-watch(1d) mesh-hw-health(1d) mesh-ideate(1d) mesh-imac-wifi(1d) mesh-interruptibility(1d) mesh-job-apply(1d) mesh-job-calls(1d) mesh-job-chatwatch(1d) mesh-job-mail(1d) mesh-job-scan(5d) mesh-job-track(5d) mesh-journal-watch(1d) mesh-labor(1d) mesh-lan-newdevice(1d) mesh-lan6(1d) mesh-land(1d) mesh-leadlag(1d) mesh-ledger(1d) mesh-llama-vision(1d) mesh-load-attrib(1d) mesh-load-audit(1d) mesh-load-gate(1d) mesh-lock-holder(1d) mesh-mca(1d) mesh-media-scene(1d) mesh-mem-guard(1d) mesh-mind-compact(1d) mesh-mind-control(1d) mesh-mind-state(1d) mesh-misha-wake(1d) mesh-mlme-tap(3d) mesh-model-bench(1d) mesh-model-swap(1d) mesh-music-fanout(1d) mesh-music-session(1d) mesh-node-care(1d) mesh-note3-light-raw(1d) mesh-note3-ui(1d) mesh-observer-effect(1d) mesh-opencode-plugins(1d) mesh-operator-hands(1d) mesh-organ-keepalive(1d) mesh-overhear(1d) mesh-pace(15h) mesh-pane-consume(15h) mesh-path-watch(15h) mesh-pcie-health(15h) mesh-perimeter(14h) mesh-phone-ap(14h) mesh-pidfile.sh(14h) mesh-pkg-watch(14h) mesh-precision(14h) mesh-prior-art(14h) mesh-promises(13h) mesh-promises-watch(13h) mesh-promises.bak-20260912-witness(13h) mesh-psi(12h) mesh-queue-tend(12h) mesh-quota-react(12h) mesh-records(10h) mesh-reflex-health(9h) mesh-reflexes(9h) mesh-report(9h) mesh-resource-guard(9h) mesh-restore(3d) mesh-revive(7h) mesh-rhythm(3d) mesh-roll-call(6h) mesh-roll-call-retire-arm(6h) mesh-room-address(6h) mesh-room-gigaam(6h) mesh-room-music(6h) mesh-route-events(14d) mesh-rq-wait(6h) mesh-say(6h) mesh-selfcare(6h) mesh-sense-map(3h) mesh-sense-reception(4d) mesh-series-stats(1h) mesh-session-watchdog(1h) mesh-situation(1h)
2026-09-14T03:23:01Z  [33mWARN[0m --test FAIL(stale) — the age in each token is the age of the CONFIRM (where a serial confirm last REACHED this tool and found it red), NOT the age of a live fault: the rotation has not returned to it since, so a tool repaired AFTER that date renders here exactly like one still broken. These are NOT counted in the headline's FAIL, because that count is edge-triggered for the board and a carried-forward red must not re-alarm hourly. NOTHING in this list re-confirms anything: each token states only what THIS run's parallel probe returned for that tool, and a probe that TIMED-OUT or DID-NOT-REPORT is a state, never a verdict — so RE-RUN the --test before acting on, or deferring, any of these. A SUBJECT-MOVED token means the arm failing NOW is not the one the confirm measured, so the age is the NEW subject's and the confirmation's is stated beside it — do not read that red as old, and do not assume the task someone already took is about it: mesh-tiny-fleet(confirmed-2d-ago,this-run:probe-red-rc1) mesh-tiny-fleet-snapshot(confirmed-2d-ago,this-run:probe-red-rc128) mesh-tv(confirmed-2d-ago,this-run:probe-red-rc1) mesh-tv-dlna(confirmed-2d-ago,this-run:probe-red-rc1) mesh-usb(confirmed-2d-ago,this-run:probe-red-rc1) mesh-wifi-quality(confirmed-2d-ago,this-run:probe-red-rc1) mesh-ble-heal(confirmed-1d-ago,this-run:probe-red-rc1) mesh-claude-deepseek(confirmed-1d-ago,this-run:probe-red-rc1) mesh-fsnotify(confirmed-1d-ago,this-run:probe-TIMED-OUT-not-a-verdict) mesh-historical-ask-ledger(confirmed-1d-ago,this-run:probe-red-rc1) mesh-lan6(confirmed-1d-ago,this-run:probe-red-rc1) mesh-model-swap(confirmed-1d-ago,this-run:probe-red-rc1) mesh-opencode-plugins(confirmed-1d-ago,this-run:probe-red-rc1) mesh-report(confirmed-9h-ago,this-run:probe-TIMED-OUT-not-a-verdict) mesh-restore(confirmed-3d-ago,this-run:probe-red-rc1) mesh-selfcare(confirmed-6h-ago,this-run:probe-TIMED-OUT-not-a-verdict) mesh-sense-reception(new-subject-age-UNKNOWN-first-sighting,SUBJECT-MOVED,confirmed-4d-ago-against-a-different-one,this-run:probe-TIMED-OUT-not-a-verdict) mesh-series-stats(confirmed-1h-ago,this-run:probe-red-rc1)
2026-09-14T03:23:01Z  [33mWARN[0m --test TOO SLOW TO ASSESS (ran the full 60s serial-confirm window and did not finish — a timeout is not a verdict, so this is NOT a FAIL and NOT 'no hardware'; the suite wants a fast core: add '# test-fast: yes' + a --test-fast entry point and the doctor will drive that): mesh-social-context
2026-09-14T03:23:01Z  [33mWARN[0m printf+\n-empty-input fragile (empty var → spurious newline → wc-l miscounts by 1; guard with [ -n "$var" ]): mesh-board-id:208 mesh-channel-keepalive:1186 mesh-channel-keepalive:1368 mesh-convexity:1146 mesh-convexity:1149 mesh-cppc:275 mesh-dash:2135 mesh-dash:254 mesh-edge-gate-audit:325 mesh-edge-gate-audit:328 mesh-edge-gate-audit:332 mesh-lan-newdevice:797 mesh-load-audit:1143 mesh-load-audit:1570 mesh-nvme-internal-gradient:68 mesh-patterns.sh:787 mesh-patterns.sh:798 mesh-patterns.sh:809 mesh-patterns.sh:817 mesh-peer-addr:100 mesh-proximity:474 mesh-psi-attrib:317 mesh-random-track-grind:289 mesh-room-music:1001 mesh-room-music:1105 mesh-room-music:1106 mesh-room-sense:1028 mesh-sound-reflex:6266 mesh-sound-reflex:6279 mesh-tcp-attrib:269 mesh-wifi-motion:1140 test-chaos-drill:100

### 30-second sample 2026-09-14T03:31:43+00:00
lock-file: present
lock-holder:
(none reported)
doctor pid=753706 argv=bash /home/mesh-home/.local/bin/mesh-doctor --cron
process-tree:
  753706: 521 bash bash /home/mesh-home/.local/bin/mesh-doctor --cron
doctor.log mtime=2026-09-14T03:31:23.218081+00:00 size=5574454
doctor.log tail:
2026-09-14T03:23:01Z  [33mWARN[0m printf+\n-empty-input fragile (empty var → spurious newline → wc-l miscounts by 1; guard with [ -n "$var" ]): mesh-board-id:208 mesh-channel-keepalive:1186 mesh-channel-keepalive:1368 mesh-convexity:1146 mesh-convexity:1149 mesh-cppc:275 mesh-dash:2135 mesh-dash:254 mesh-edge-gate-audit:325 mesh-edge-gate-audit:328 mesh-edge-gate-audit:332 mesh-lan-newdevice:797 mesh-load-audit:1143 mesh-load-audit:1570 mesh-nvme-internal-gradient:68 mesh-patterns.sh:787 mesh-patterns.sh:798 mesh-patterns.sh:809 mesh-patterns.sh:817 mesh-peer-addr:100 mesh-proximity:474 mesh-psi-attrib:317 mesh-random-track-grind:289 mesh-room-music:1001 mesh-room-music:1105 mesh-room-music:1106 mesh-room-sense:1028 mesh-sound-reflex:6266 mesh-sound-reflex:6279 mesh-tcp-attrib:269 mesh-wifi-motion:1140 test-chaos-drill:100
2026-09-14T03:23:01Z  [33mWARN[0m orphans: 94 unwired+non-canon, confirmed 2+ checks (stable) — full list: cat ~/.mesh/.doctor-orphans-state
2026-09-14T03:23:01Z  [36mNOTE[0m unlaunched-but-exempt: 97 deployed tool(s) with NO launcher — self-declared on-demand, and cron/units/supervise/hooks/canon/corpus all empty for them (a census, not a fault; the fault is the exemption-claim leg)
2026-09-14T03:23:01Z  [33mWARN[0m orphan-ok exemptions claiming a caller that does not exist: mesh-lease mesh-sound-progress — nothing in crontab/units/supervise/hooks/the script corpus invokes them, confirmed 2+ checks. An exemption must cite what LAUNCHES the tool (a cron line, a caller, a unit, a hook), never a capability the tool merely accepts

### 30-second sample 2026-09-14T03:32:13+00:00
lock-file: present
lock-holder:
(none reported)
doctor-process: none
doctor.log mtime=2026-09-14T03:32:09.412951+00:00 size=5577696
doctor.log tail:
2026-09-14T03:23:01Z  [33mWARN[0m topology leak: mesh-vpn-health:100.64.0.9 (hardcoded IP — use env var / config instead)
2026-09-14T03:23:01Z  [33mWARN[0m topology leak: mesh-vpn-node-watch:100.94.116.17 (hardcoded IP — use env var / config instead)
2026-09-14T03:23:01Z  [33mWARN[0m topology leak: mesh-watchtower:100.94.116.17 (hardcoded IP — use env var / config instead)
2026-09-14T03:23:01Z  mesh-doctor: 2 FAIL, 34 WARN | serial-confirm 1/166 assessed, 18 FAIL(stale), 164 stale-verdict, 1 never-assessed

### completion 2026-09-14T03:32:13+00:00
lock-file: present
lock-holder:
(none reported)
doctor-process: none
doctor.log mtime=2026-09-14T03:32:09.412951+00:00 size=5577696
doctor.log tail:
2026-09-14T03:23:01Z  [33mWARN[0m topology leak: mesh-vpn-health:100.64.0.9 (hardcoded IP — use env var / config instead)
2026-09-14T03:23:01Z  [33mWARN[0m topology leak: mesh-vpn-node-watch:100.94.116.17 (hardcoded IP — use env var / config instead)
2026-09-14T03:23:01Z  [33mWARN[0m topology leak: mesh-watchtower:100.94.116.17 (hardcoded IP — use env var / config instead)
2026-09-14T03:23:01Z  mesh-doctor: 2 FAIL, 34 WARN | serial-confirm 1/166 assessed, 18 FAIL(stale), 164 stale-verdict, 1 never-assessed
