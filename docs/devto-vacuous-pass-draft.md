---
title: n/a is not a verdict
tags: testing, linux, debugging, devops
canonical_url:
---

> Every number and every log line below is a live read from the machine in question, captured
> while writing. Nothing is reconstructed from memory; where the evidence was destroyed by a
> reboot mid-writing, I say so and name where I got it back from.

There are three things a check can tell you. It passed. It failed. Or it couldn't run —
the thing it measures isn't here. Most tools only have room for the first two, so the third
gets folded into whichever neighbour is closer. Fold it toward *pass* and a blind instrument
reports green. Fold it toward *fail* and real bugs drown in false accusations.

I did both, in the same codebase, an hour apart. Here's the green one first.

## The test passed because the hardware didn't exist

As I write this, the machine running every one of my agents is 73°C at the die and its
health check says this:

```
=== mesh-hw-health mesh-home 00:35Z ===
  thermal   n/a
  fan       n/a (not exposed via hwmon here)
  disk      nvme=42°C(throttle@74°C) ok
  battery   n/a
HW: OK
```

`HW: OK`. Exit code 0. Green.

The chip, at that same second:

```
$ cat /sys/class/hwmon/hwmon2/temp1_input
76750
```

76.75°C. The tool whose entire reason to exist is catching a dead cooler could not see the
CPU. It had never been able to see the CPU. And its test suite was green the whole time —
not green *despite* the bug. Green *because* of it.

That last part is the story. The bug is boring. The test is the interesting one.

## The boring bug

`mesh-hw-health` read temperatures like this:

```bash
for z in /sys/class/thermal/thermal_zone*/temp; do
  t=$(( $(cat "$z" 2>/dev/null || echo 0)/1000 ))
  [ "$t" -gt "$maxt" ] && maxt=$t
done
```

That's the Intel-shaped assumption. On this box — a Ryzen — `k10temp` is hwmon-only, and
`/sys/class/thermal` holds this:

```
cooling_device0  cooling_device1  cooling_device10 ... cooling_device15
```

Sixteen cooling devices and **zero** `thermal_zone*`. The glob matches nothing. The loop
body never runs. `maxt` stays `0`, falls to the else-branch, prints `n/a`, sets no warning,
and the report rolls up green.

Portability miss. One-line class of bug. You've written it; I've written it. Fine.

## The test that agreed

Here's the `--test` block that shipped alongside it, and I want you to read it as if it
were yours, because it very plausibly is:

```bash
zones=0
for z in /sys/class/thermal/thermal_zone*/temp; do
  [ -r "$z" ] || { echo "  FAIL: $z exists but is unreadable"; fail=1; continue; }
  v=$(cat "$z" 2>/dev/null || echo "")
  [ -z "$v" ] && { echo "  FAIL: $z is empty"; fail=1; continue; }
  v_int=$((v/1000)) || { echo "  FAIL: $z value '$v' is not numeric"; fail=1; continue; }
  [ "$v_int" -gt 0 ] || { echo "  FAIL: $z value $v_int is not positive"; fail=1; continue; }
  zones=$((zones+1))
done
[ "$zones" -eq 0 ] && echo "  n/a: no thermal zones — graceful off-node path"
```

Look at what that validates. Unreadable zone? Caught. Empty zone? Caught. Non-numeric?
Caught. Negative? Caught. Four real assertions, each one falsifiable, each one a genuine
bug someone actually hit. This is not a lazy test. Someone cared.

And on this machine it checks **nothing at all**, because the loop it hangs off of iterates
over an empty set. Every assertion inside a `for` loop with zero iterations is vacuously
true. The suite ran, executed no checks, and reported success.

Then there's line 109, which I can't stop looking at:

```bash
[ "$zones" -eq 0 ] && echo "  n/a: no thermal zones — graceful off-node path"
```

The code *noticed*. It saw zero sensors, said so out loud, gave the condition a friendly
name — "graceful off-node path" — and set no failure flag. Somebody anticipated this exact
state and classified it as fine. It's fine when you run the tool on a phone. It is not fine
when you run it on the workstation the phone reports to. The test had no way to tell those
apart, so it picked the generous reading and moved on.

That's what makes the vacuous pass so much worse than a missing test. A missing test is a
known gap. A vacuous test is a gap wearing a green checkmark. It doesn't just fail to catch
the bug — it actively certifies the bug, once per CI run, in a reassuring color.

## Proof it was blindness, not absence

The obvious objection: maybe the box just has no sensor. Maybe `n/a` is the truth.

It isn't, and I don't have to argue about it, because a *different* tool on the *same box*
read the *same chip* at the *same instant*:

```
$ mesh-therm-headroom
COMFORTABLE — pkg=69°C floor=41°C, 26°C to 95°C ceiling — ample headroom
$ cat /sys/class/hwmon/hwmon2/temp1_input
69625
```

69°C, matching `69625` to the degree. One tool reads the die; the other, one second later,
reports `n/a`. Same silicon, same kernel, same second. The sensor was always there. Only
one tool knew how to look, because it had been taught the hwmon path earlier and its
sibling never got the lesson.

This is the check that turns "I think it's broken" into "it's broken." If you can find a
second reader that sees what your blind tool can't, you're done arguing. Absence of
evidence became evidence of absence for exactly as long as nobody held up a second
instrument.

## The fix, and the part that generalizes

Two halves, because the glob was only half the fault.

**Read the chip.** Zones first, then hwmon: `k10temp` → `Tdie`/`Tctl`, else `Tccd*`, else
any non-disk hwmon sensor, with NVMe left as the ambient floor.

**Stop calling unknown "OK."** A missing read is an unmonitored cooler, not a healthy one.
Thermal-unknown now rolls up `WARN` — never `FAIL`, because a sensorless phone or VM is an
honest gap and I don't want to cry wolf on hardware that genuinely has nothing to report.
But it is no longer silent, and silence was the actual defect. The bad glob only blinded one
tool; the cheerful `n/a` is what let the blindness ride for months.

**And the gate that would have caught it** — the part worth stealing:

```bash
# REAL-READ GATE: the sensor loop above only validates zones that EXIST — on AMD there are
# none, so it passed vacuously while the tool was blind. Assert against the box instead:
# any temp sensor present => cpu_max_temp() MUST produce a plausible reading;
# nothing to read => honest skip, never a fake green.
```

The shape of it: **don't assert over the set you found. Assert over the set that exists.**

The old test asked *"is every zone I found valid?"* — a question with a smug answer when you
found none. The new one asks *"this box exposes temperature sensors somewhere; did my reader
produce a number between 10 and 149°C?"* If the box genuinely has no sensors, it skips and
says so. If the box has sensors and the reader came back empty, that's a failure — which is
precisely, exactly the state this tool sat in, green, for its entire life.

Live, both halves at once:

```
  ok: live CPU temp read 73°C · ambient floor 28°C (9 sensors)
$ cat /sys/class/hwmon/hwmon2/temp1_input
73375
```

73°C against 73375. And it's falsifiable in both directions — stub the reader and the report
flips to `HW: WARN` while `--test` fails. A test you can't break on purpose isn't a test
either; it's the same tautology wearing a different hat.

## I'd seen this exact movie

What convinces me this is a pattern and not an anecdote: it's the second time.

`mesh-mag` and `mesh-gyro` read the phone's magnetometer with `termux-sensor -n 1`. One
sample. That raced the driver's startup, so the read came back empty — every single cron
tick. The state file went five days stale. `--test` was green for all five, because it
exercised the offline classifier against canned values and never once demanded that live
hardware produce an axis. Reachable phone, cooperative driver, zero data. A *hollow* sense:
cron-green, artifact rotting.

Same disease. The suite tested the code's opinion of the hardware instead of the hardware.
Both fixes are the same move — make the test demand a real read, so the tool can't be
congratulated for producing nothing.

If you want one sentence to take to your own codebase: **a test that only exercises the
happy path's inputs will pass hardest on the machines where those inputs don't exist.**
Empty list, absent config key, feature-flagged-off branch, a mock that returns `[]`, a
`for` loop over a glob that matches nothing. `assert all(x.valid for x in things)` is a
poem when `things` is empty. Every language gives you this footgun for free and calls it
"vacuous truth" like it's a math curiosity instead of the reason your dashboard is lying.

## The same bug, pointed the other way

I would have shipped this piece with that as the ending. Then, one hour after the thermal
fix landed, I found its mirror image — and it's the half that actually explains the first.

A different tool, `mesh-autowire`, decides whether a check is healthy enough to put on a
schedule. It gated like this:

```bash
if ! timeout 30 "$tool" --test >/dev/null 2>&1; then
  echo "SKIP $name: --test FAILED (refuse to wire a broken reflex)"; continue
fi
```

Reasonable! Refuse to schedule a broken check. Except the exit code was never two-valued.
The convention here is three: `0` pass, `2` **honest n/a** — *the thing I measure is not on
this machine* — and anything else broken. A bare `!` can't see that distinction. It caught
`2` along with `1` and `127` and filed them all under the same headline: **FAILED (refuse to
wire a broken reflex)**.

So a perfectly sound tool got called broken for the crime of being honest. `mesh-wifi-temp`
exits `2` on this node because it reads Intel `iwlwifi` hwmon and this box has an
`rtl88XXau` — nothing to read, says so, correctly, in the exact way the contract asks for.
Every run, it got accused.

Same root as the thermal bug. Exactly inverted. One folded *unknown* into **OK** and shipped
a false green. The other folded *unknown* into **FAIL** and shipped a false red. Neither
tool could say the true thing, which was "I don't know, and here's why."

## What the false red was hiding

Here's why the red one is worse than it looks, and it's the number that changed my mind
about what this piece is about.

The autowire log covers about two hours:

```
$ grep -c 'test FAILED' ~/.mesh/autowire.log
258
$ grep 'test FAILED' ~/.mesh/autowire.log | grep -oE 'SKIP [a-z0-9-]+' | sort -u | wc -l
40
```

258 accusations against 40 distinct tools. Forty tools, all reported broken, all refusing to
be scheduled. That's not a bug list, that's wallpaper. Nobody reads a list of forty failures
where thirty-nine have been there since forever.

After the fix, the same gate re-runs and sorts them properly:

```
2026-07-15T00:31:43Z SKIP mesh-ss-test:      --test FAILED rc=1 (refuse to wire a broken reflex)
2026-07-15T00:31:47Z SKIP mesh-vpn-watchdog: --test FAILED rc=1 (refuse to wire a broken reflex)
2026-07-15T00:31:58Z SKIP mesh-wifiscan:     --test FAILED rc=1 (refuse to wire a broken reflex)
```

Three. Out of forty. The other thirty-seven now say `n/a rc=2 (organ absent on this node —
tool is sound, not wiring here)`, which is what they'd been trying to say the whole time.

**Three real bugs had been sitting in plain sight for as long as the log goes back**, wearing
the same label as thirty-seven non-bugs, invisible for exactly that reason. They didn't
surface because someone got clever. They surfaced because the crying wolf stopped. That's
alert fatigue with a denominator — not a vibe about dashboards, a measurement: signal was
7% of the alerts, and 7% is indistinguishable from noise to any human who has a job.

So the two bugs rhyme, and the rhyme is the lesson:

|  | folded into | produced | cost |
|---|---|---|---|
| `mesh-hw-health` | `n/a` → **OK** | false green | a blind watchdog, certified healthy |
| `mesh-autowire` | `n/a` → **FAIL** | false red | 3 real bugs hidden among 37 innocents |

Both tools had a third thing to say and no slot to say it in. Push the unknown toward green
and you get comfortable blindness. Push it toward red and you get a wall of noise that hides
the genuine failures. There is no safe direction to round off "I don't know," which is the
whole point: it isn't a degraded pass or a soft fail. It's a different kind of statement — a
fact about the *observer*, not the observed. `mesh-hw-health` at `thermal n/a` wasn't telling
me about my cooling. It was telling me about itself.

The fix in both cases is the same shape, and it's almost embarrassingly small — give the
third state a name and a slot:

```bash
gate_verdict(){ case "$1" in 0) printf 'PASS\n';; 2) printf 'NA\n';; *) printf 'FAIL\n';; esac; }
```

Three lines. Then `NA` gets its own branch, its own log line, its own honest sentence. And
`--test` asserts all three, including the one that bit: rc=2 must classify as `NA`, or the
suite fails.

## It isn't a testing bug

I had this filed as a test-harness problem right up until it happened twice more while I was
writing, in code that has no tests in it at all.

The first was an hour after the fix above. A sense that reads Bluetooth had been reporting
`LOCAL BLE scan on mesh-home failed` every cycle for days. The scan wasn't broken. The
capability was declared like this:

```bash
[ -d /sys/class/bluetooth ] && [ -n "$(ls /sys/class/bluetooth 2>/dev/null)" ] && o="$o ble"
```

`hci0` is in there. The kernel modules are loaded. The radio is real, and it works. What
wasn't installed was `bluez` — the userspace. So the node advertised an organ it had no way
to read, and every consumer that trusted the advertisement got a failure that read like a
hardware fault. Same shape as the thermal check, one step earlier: the question asked was
"is the driver loaded," the question that mattered was "can I read this thing," and the gap
between them is where the lie lives. `apt install bluez`; the scan now returns four devices,
and the capability is gated on a live read instead of on a directory being non-empty.

The second one cost me twenty-one minutes of total blackout on the machine running every one
of my agents, and it's the one I'd hang the whole essay on if I had to pick.

At 00:46:31 the WiFi dongle's firmware stopped acknowledging transmits:

```
2026-07-15T00:46:31 kernel: rtw_8822bu 1-2.3:1.2: failed to get tx report from firmware
```

Six of those in ten seconds. Zero packets moved after it. No carrier loss, no disconnect —
the association held, and so did this:

```
$ ip -br link show wlx<dongle>
wlx<dongle>  UP   <mac>  <BROADCAST,MULTICAST,UP,LOWER_UP>
```

`UP,LOWER_UP`. The link layer had exactly one thing to say and it said the true one: the
interface *is* up. It just doesn't have a word for "up and transmitting nothing," so every
check built on `ip link` — and that is most of them — greened straight through a dead node.
The thing that eventually noticed fired at 01:10:01, which is not a check. It's an obituary:
by then the adapter had fallen off the USB bus, re-enumerated onto a *different* bus path,
and reconnected itself. Nothing I wrote fixed it. The hardware re-seated and I took the
credit.

So: three tools, one kernel subsystem, four instances, and none of them share a line of
code. What they share is an instrument answering the question next to the one you asked.
Is the driver loaded — not, can I read it. Is the link up — not, are packets moving. Did
the loop find a failure — not, did the loop have anything to look at. Every one of those
pairs is *almost* the same question, and the gap between them is only visible on the day the
answers disagree. That's the day you're already down.

## The coda, which is not triumphant

Everything above is committed. It is also, at this moment, **not deployed**:

```
$ diff ~/.local/bin/mesh-hw-health scripts/mesh-hw-health >/dev/null && echo SAME || echo DRIFT
DRIFT
$ grep -c k10temp ~/.local/bin/mesh-hw-health
0
```

The source tree knows about `k10temp` in three places. The binary actually running on this
node knows about it in zero. Every reading I quoted at the top — `thermal n/a` at 76°C —
came from the *deployed* tool, which is still blind as I publish this, and will keep
cheerfully reporting `HW: OK` until someone pushes and syncs.

I'm leaving that in rather than tidying it up, because "we fixed it" is the part everybody
writes and "the fix is sitting in a commit while production runs the old one" is the part
everybody lives. The gap between a green test and a working system has room for a bad glob.
It also has room for a whole deploy.

## What to go look at

Two greps, and you can run them right now.

**For the false green:** find a test that loops over something it discovered — a glob, a
directory listing, a query result — and ask what it asserts when that thing is empty. If the
answer is "nothing, silently," you have a check that gets *more* confident the less it can
see.

**For the false red:** find a place where you check `if !cmd` or `if rc != 0`, and ask
whether the thing you're calling has more than two things to say. Then go look at your
alert list and count what fraction is real. If it's 7%, you don't have an alert list. You
have wallpaper, and there are three real bugs behind it.
