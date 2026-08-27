# Orphan census, 2026-08-27 — the invocation leg stops accepting a MENTION

`mesh-doctor`'s orphan check asks four questions of every script in `scripts/`: is it in the crontab,
in a systemd user unit, in `supervise.list`, in a Claude Code hook, named in CLAUDE.md's On-demand
canon, or **invoked by another script**. The last leg grepped the comment-stripped corpus for the
tool's name as a token and called any hit wiring.

## The refutation

`mesh-cam-watch`: **8 files matched, ZERO launch it.** Every one is a non-comment line, so stripping
comments could never have helped.

| file | line | what it actually is |
|---|---|---|
| `mesh-cam-light` | 173 | `case` pattern `*"owner=mesh-cam-watch"*)` |
| `mesh-cam-light` | 186 | a log string: "is mesh-cam-watch --daemon running?" |
| `mesh-cam-watch.service` | 2, 7 | an **uninstalled** unit in `scripts/` (`~/.config/systemd/user` has only `mesh-imac-cam-watch.service`) |
| `mesh-face-recognize` | 48 | prose in a header paragraph |
| `mesh-dash` | 3282 | an error string |
| `mesh-doctor` | 3970 | a `pass` message |
| `mesh-misha-wake` | 158 | a log string naming the frame's writer |
| `mesh-room-sense-loss` | 95, 172, 173, 215 | organ-name prose · `mesh-cam-watch.service` as an ARGUMENT · a remedy sentence |
| `mesh-motion-attrib` | 174 | an n/a explanation: "mesh-cam-watch does not run here" |

So the orphan check read it WIRED while `mesh-reflex-health` independently read it UNPRODUCED.
Reflex-health was right.

## The rule now applied

The corpus the leg reads is rendered to **one resolved basename per line** and matched with
`grep -Fx` — exact, never a token regex.

Kept as a launch: command position (including inside `$( )`, backticks, and the string a `bash -c` /
`ssh host` / `tmux new-window` executes); a `${VAR:-path}` assignment value; a bare one-token
argument. Dropped: `case` PATTERNS, and every file with no `#!` (a unit in `scripts/` is not
installed; a `.m`/`.swift`/journal is compiled or read).

The discrimination needs no heuristic. A log line, a description and a prompt are **one shell word
containing whitespace**, so their basename can never EQUAL a tool name.

`mesh-cam-watch.service` handed to `_probe_unit` is a handle for the UNIT; under exact matching it no
longer wires the SCRIPT.

## A second defect found in the same block

The crontab / systemd / supervise / hooks legs read their source through a PIPE into `grep -Eq` under
`set -o pipefail`. The reader exits at its first match, the writer takes SIGPIPE, pipefail promotes
141, and the leg silently reads "not wired". Measured against the live 291-line crontab under load:
**364/2000 = 18.2%** false negatives; a full orphan sweep returned **42/43/45/43** across four runs
with **eight flapping tools, every one cron-wired**. Herestring form: **41/41/41**, identical sets.
This is the real mechanism behind the "+new:mesh-powerbtn while mesh-powerbtn was cron-wired" flake
that was blamed on transient `crontab -l` reads. Fixed here too — the baseline is not reproducible
without it, so no A/B over this predicate meant anything until it was.

## The census

Both arms measured with the SIGPIPE fix applied, so the only variable is the invocation predicate.
Stable across repeated runs on both sides.

**41 orphans -> 71. +30 newly flagged, 0 lost.** (The 72/+31 this line carried while the census was
being written counted `mesh-pane-watch`, which the `# launches:` header below re-wires; the number
here is the one the live run prints — `orphans: 71 unwired+non-canon, confirmed 2+ checks — +new:30`,
2026-08-27T01:22Z first sighting, confirmed at the second check.)

Newly flagged, and what each was hiding behind:

- **case pattern / allowlist alternation** — `mesh-blessyou` `mesh-find` `mesh-see` `mesh-github-watch`
  `mesh-therm-ambient` `mesh-transcribe` `mesh-voice` `mesh-phone-convo` `mesh-phone-ear`
  `mesh-phone-sensors` `mesh-chaos-doctor` `mesh-chaos-verify`
- **a regex/`|`-joined string** — `mesh-eye` `mesh-mind-keepalive` `mesh-window-repair` `mesh-channels`
- **a space-separated wordlist in an assignment** (`CORE=`, `SUBSTRATE_TOOLS=`, `EMERGENCY_SET=`) —
  `mesh-reflect` `mesh-route` `mesh-harden-ssh` `mesh-revert-catch` `mesh-borrowed-brain` `mesh-review`
- **prose: a log line, a prompt, a description, an n/a message** — `mesh-cam-watch` `mesh-census`
  `mesh-fleet-feed` `mesh-lan-presence` `mesh-tuner-eye` `phone-setup`
- **a data-table row** — `mesh-operator-focus` (a `|`-delimited row in `mesh-reflex-health`, which
  CHECKS it rather than launching it)
- **an uninstalled unit file in `scripts/`** — `ngrok-notify.sh` (named only by `ngrok.service`, which
  is not in `~/.config/systemd/user`)

`mesh-pane-watch` was in this list until `mesh-liveness-loop` grew a `# launches:` header: its LOOPS
table (`"name|interval|command"` rows) is a real launcher that no syntactic reader can see, and
widening the reader to split on `|` would re-wire every entry in the first two groups above. A
launcher declares itself instead — on the LAUNCHER, so it is not a self-exemption.

## Known limit

A tool launched only from a data table, or handed to a generic dispatcher as a bare argument several
frames away, is invisible to this leg. That failure direction is a LOUD orphan WARN, never a silent
"wired", which is the correct way round.
