# phone-collect-blind-to-the-working-path — the verdict named the phone, the measurement named three transports

**2026-08-21, senses@mesh-home.** `mesh-phone-collect` logged `[phone-unreachable] no ADB, LAN or WG
path` every 10 minutes for 37.3 days while the phone answered ssh over Tailscale in half a second.
The tailscale address was never a candidate. Fixed in the tool; the shape is filed here because the
tool was not wrong about what it measured — it was wrong about what it *said*.

## The measurement

| fact | value | how |
|---|---|---|
| log window | 2026-07-14T22:20:12Z → 2026-08-21T05:40:12Z | first/last line of `~/.mesh/phone-collect.log` |
| span | **37.3 days** | computed from those two stamps |
| lines | 3061 | `wc -l` |
| `[phone-unreachable]` | **3056 = 99.84%** | `awk` count |
| everything else | **5 lines, total** | one `[collect] +2984 rows via LAN` (2026-08-15T06:30:17Z) + four `no remote log yet (LAN)` (08-17, 08-18 ×3) |
| daily rate | 100% unreachable on 31 of 35 days with traffic; 97–99% on the other 4 | per-day `awk` |
| phone actually reachable | **5/5 ok**, `ssh -p 8022 u0_a380@100.103.99.16 'echo ok'`, 2026-08-21T05:36–05:37Z | measured by hand, independently of the operator's own 5/5 |

So: **one successful drain in the tool's entire life.**

## The cause, read in the source (not inferred from the log line)

The candidate list was three transports, hard-coded in the tool:

- **ADB** — `adb forward` → `127.0.0.1:8023` → phone:8022
- **LAN** — `192.168.8.203:8022`
- **WG**  — `10.66.66.10:8022` via `root@100.94.116.17`

There was **no tailscale path at all**. And the tool's own comment (old `:107-113`) already
diagnosed why LAN fails — the WG full tunnel routes the phone's TCP SYN-ACK out the tunnel, so
direct LAN-TCP to :8022 times out. The LAN failure was understood well enough to justify bolting on
**two workarounds**; the one path that works **without** a workaround was never added.

Worse, the mesh already had the answer. `phone_reach_candidates` in `mesh-patterns.sh` is the
canonical deduped phone-address ladder (`ts-slot` / `ts-live` / every `PHONE_LAN_IPS`), it resolves
the tailnet address correctly even in a bare cron environment (measured: `env -i` → `ts-slot
100.103.99.16`), and `phone_reachable_ip` — used by every other phone sense — goes through it.
`mesh-phone-collect` kept a private list beside it.

## The shape

**A probe that answers a different question in the same type.** `[phone-unreachable]` is *honest
about what was attempted* and *false about what it asserts*. "Unreachable" is a claim about the
PHONE; what was measured is "these three transports are down". Both render as one confident line,
and nothing in the line distinguishes them. Sibling of
`a-probe-that-answers-a-different-question-in-the-same-type` and
`a-collapsed-reason-makes-blind-and-quiet-identical`.

Note the second-order trap: **the diagnosis of one path's failure became the reason not to re-survey
the paths.** Once "LAN is broken because of the full tunnel" was written down, the list stopped being
a question. Two workarounds were added *within* the frame; the frame itself — "is this the set of
paths?" — was never re-asked.

## What was corrected in the task's own framing

Two claims in the incident report do not survive checking, and are recorded so the next hand does not
inherit them:

1. **`mesh-presence` / `mesh-operator-context` were NOT misled by this log.** Nothing machine-reads
   `phone-collect.log`: the only hit across `scripts/` and `~/.local/bin/` is a *prose comment* in
   `mesh-access-probe`. Those senses go through `phone_reachable_ip`, i.e. the ladder that already
   had the tailnet address. The blast radius is narrower than "everything that read this log".
2. **The real downstream cost is the other log, and it is silence, not a lie.**
   `~/.mesh/phone-track.log` — the roaming capture this tool exists to drain — has its newest row at
   **2026-07-25T07:01:19Z, 27 days stale**; the single 08-15 drain pulled 2984 rows that all end
   there. `mesh-phone-digest` (its only local consumer) degrades honestly: it prints `no rows in the
   last 24h — silent`. So the sense went **blind**, it did not go **false** — which is why nothing
   downstream screamed, and why 37 days passed.

Also stale and now corrected: `~/.mesh/nodes:7` carried `(LAN — the TS ip is dead, see PHONE_TS_IP
below)` while line 60 of the same file said `PHONE_TS_IP=100.103.99.16 — LIVE again 2026-08-20`. A
file that contradicts itself six lines apart sends the next reader to the dead half. **A workaround's
note outlives the outage it worked around** unless the note is dated *and* re-derived.

## A finding the fix produced immediately

The moment the refusal line started naming outcomes per candidate, a second, real, previously
invisible fault surfaced. Measured 2026-08-21:

```
05:36–05:37Z  ts 100.103.99.16 → ok, 5/5
05:38Z        ts 100.103.99.16 → Connection refused, 8/8
05:43Z (tool) ts:100.103.99.16=refused  adb:127.0.0.1:8023=closed  lan:192.168.8.203=refused  wg:10.66.66.10=timeout
05:45–05:47Z  ts → Connection refused, 10/10
```

`refused` (TCP RST) is not `timeout`. The host is **up and routable**; the phone's Termux **sshd is
down**. LAN answering RST at the same moment also shows the full-tunnel timeout story is not what is
happening *right now* — both paths agree the sshd died. These are two different incidents with two
different fixes (tap Termux vs chase the network), and the old single-string line could express
neither. The `adb` transport speaks its own dialect for the same fact: through the forward, a far-end
refusal surfaces as `Connection closed by 127.0.0.1 port 8023`, which is why it gets its own word
(`closed`) rather than falling through to an unclassified `fail-rc255`.

## The fix

Two changes, and the second matters more than the first.

1. **The tailnet path is a candidate, and it is first** — but not as a fourth constant. The `ts` and
   `lan` rungs now come from `phone_reach_candidates` (the shared ladder), so a phone address added
   to `~/.mesh/nodes` flows in by itself. A private constant here would rot exactly the way the old
   list did. `MESH_PHONE_TS_IP` remains as an explicit override.
2. **The refusal line enumerates every candidate by name with its own outcome word, rendered from the
   same array that was probed:**

   ```
   [phone-unreachable] no path answered — tried 4: ts:100.103.99.16=refused
     adb:127.0.0.1:8023=closed lan:192.168.8.203=refused wg:10.66.66.10=timeout
   ```

   This is the structural half. "Unreachable" now *means* "every path I know of, tried, named" — and
   the next transport that goes missing is missing **from the log line, in the log, visible by eye**,
   instead of being invisible in a list nobody re-reads. It is also why the fix cannot silently
   regress: the message is not writable by hand without failing its gate.

Deliberately NOT done: inverting the direction (having the phone call us). The asymmetry the operator
noticed is real — `mesh-phone-beacon2` PUSHES and its battery rows always arrive, and `mesh-light`'s
own comment records the loc-beacon push working "independent of sshd". But inverting here would be
building a second channel to route around a defect that is a **stale candidate list**, not a
direction problem. Fix the census first; if pull still starves after that, invert on evidence.

## The gates (all seen RED before green)

`--test` grew from 3 scenarios to 5. Mutants were run from an executable scratch copy by absolute
path, and each mutation was asserted to have LANDED (byte-length delta) before its output counted.

| mutant | restores | arm that goes red |
|---|---|---|
| **A** — drop the `ts` rungs from the candidate list | the exact pre-fix blindness | `reachable-only-over-ts declared unreachable (rc=2)`; also `ts transport not used`, `logged unreachable while a transport answered` |
| **B** — hand-write the old fixed refusal string | a message not derived from the list | all four `refusal line omits <tag>` + both classification arms |
| **C** — collapse the timeout branch of `_why` | a collapsed reason | `timeout not classified` |
| **D** — map `Connection closed by` to `timeout` | two mechanisms wearing one word | `adb-forward refusal not classified` |

Scenario 4 is the incident gate: adb down, LAN and WG time out, **only** the tailnet address answers
— the live 05:36Z state. Scenario 5 is the structural gate: an env-added transport
(`MESH_PHONE_TS_IP=10.9.9.9`) must appear in the refusal line **by itself**, which is what makes
"names every path" a property of the code rather than of the author's memory.

The test's mocks were tightened for the same reason the tool was wrong: the old mock ssh answered
`ok` to **every** host, so it structurally could not detect a missing transport. It now records the
host, and the ladder's two real inputs (`mesh-peer-addr`, `tailscale`) are stubbed rather than the
candidate list being injected — the assembly code under test is `phone_reach_candidates` itself.

## Live artifact

`mesh-phone-collect` run from a bare `env -i` cron-like environment, 2026-08-21T05:43:24Z:

```
[phone-unreachable] no path answered — tried 4: ts:100.103.99.16=refused
  adb:127.0.0.1:8023=fail-rc255 lan:192.168.8.203=refused wg:10.66.66.10=timeout
```

Four candidates, ts first, each with its own outcome. (`fail-rc255` in that run is what prompted the
`closed` classification, landed after it.) A collect *through* the tailnet path could not be captured
as a live artifact in this session: the phone's sshd went down at 05:38Z and stayed down through
05:47Z. That the transport works is proven by the 5/5 at 05:36–05:37Z; that it is now in the list is
proven by the line above. **Stating this rather than waiting for a green run is the point** — the
tool's whole defect was a verdict that sounded better than its evidence.

## Open, not mine

The phone's Termux sshd flaps (up 05:36, down 05:38 onward). Now visible as `refused` rather than
buried in `[phone-unreachable]`, but not fixed here — reviving it is a touch on the operator's daily
driver. Related: `mesh-access-probe`'s comment says mesh-home has **no ssh private key**; that is
itself stale (`~/.ssh/id_ed25519` exists and authenticated 5/5 today), so that tool's diagnosis of
this same silence should be re-derived before it is trusted.
