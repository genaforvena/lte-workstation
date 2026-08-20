---
title: The auth check I decided not to write, and the test that keeps it unwritten
tags: security, testing, architecture, devops
canonical_url:
---

> Every command and every exit code below is a live read from the machine in question,
> captured while writing. Nothing is reconstructed from memory.

I have a tool that mints unforgeable capability tokens. HMAC-SHA256, a one-way subset
ratchet on the rights, a depth limit so delegated authority can't propagate forever, an
auditable parent chain. It's a small honest implementation of the seL4/CapROS idea in
395 lines of bash and stdlib Python.

It has zero callers. That is not a gap in the roadmap. It is the finding.

## The integration that writes itself

Elsewhere in the same codebase there's a router that dispatches capability requests —
camera, SMS, text-to-speech — to whichever machine can service them. It gates callers with
a static allowlist: a header comment naming who may ask for what. A caller is in the list
or it isn't.

Put those two things in one repo and the next commit writes itself. You have a static
allowlist over here and an unforgeable token system over there. Obviously the router should
stop trusting a name and start verifying a token. Every reviewer would nod. I nearly did it
twice.

Instead I measured what the gate would exclude. Here is the whole measurement, run in one
ordinary shell, no privilege of any kind:

```
$ id -u
1000
$ stat -c '%a %U %s' ~/.mesh/cap-secret
600 mesh-home 32

$ export MESH_CALLER=genome
$ T=$(mesh-cap mint --rights=read,write,admin --for=camera-cap)
$ mesh-cap verify "$T" --action=admin --for=camera-cap; echo "rc=$?"
rc=0

$ mesh-cap inspect "$T"
grantor : genome
rights  : admin,read,write
depth   : 8
for     : camera-cap
parent  : ROOT
```

`rc=0` is ALLOW. I asserted I was `genome` by exporting a variable, and then I minted myself
an admin capability over the camera and it verified. Both halves worked, from the same
prompt, because they are the same privilege.

That's the argument, and it fits in one line: **the secret is mode 0600 and owned by uid
1000, and every caller the router serves runs as uid 1000.** The shell that can lie about
`MESH_CALLER` can also read the signing key. The token is unforgeable to everyone except
precisely the population that would be forging it.

So the gate excludes nobody it does not already admit. What it *does* add is a fail-closed
DENY path in front of live actuators — a camera, an SMS sender — whose rollback would have
to run through the router the gate now sits in front of. Availability cost, zero security
gain.

The general form is worth stating plainly, because I don't think it's the way most of us
reach for auth:

> **An authentication boundary that does not cross a privilege boundary is decoration.**

Cryptography does not create a boundary. It *enforces* one that the operating system, the
network, or the sandbox already drew. If both sides of your check run with the same
credentials, on the same host, as the same user, with read access to the same key material,
then you have not built a wall. You have built a very rigorous honour system, and you have
paid for it in availability.

I would guess this is the single most common shape of security theatre in internal systems:
service-to-service tokens between two containers that share a secrets mount, HMAC-signed
internal webhooks where the sender and receiver are the same deployment, an API key checked
by a process that could read the key file anyway. The check is real. The signature verifies.
It just isn't excluding anyone.

The question that dissolves it isn't "is this signed?" It's: **name the caller this stops.**
If you can't name one, or the one you name has to be something you already trust more than
the thing you're protecting, you're done — don't build it.

And name the condition that would flip the answer, because it usually exists and it's
usually specific. Mine is written into the source: a caller that does *not* share the
secret's uid. A sandboxed subagent. A separate service account. A token crossing a real
privilege boundary. The primitive stays in the tree, exercised and tested, waiting for a
consumer whose identity isn't self-asserted. Wire it *then*.

## The half I hadn't seen written down

Here's where it gets interesting, because deciding not to build something is the easy part.
Making the decision *survive* is the hard part.

I've watched this fail over and over. Someone thinks carefully, chooses not to add a thing,
writes a comment explaining why, and eighteen months later a new contributor — or the same
person, or a language model — reads the codebase, notices the obviously-missing integration,
and adds it. The comment was three files away. Nobody read it. The reasoning was correct,
recorded, and completely ineffective.

That's because of something I'd already learned the hard way in this codebase and hadn't
applied here: **a comment is not a channel to the reader.** Prose in a source file reaches
whoever happens to open that file at the moment they happen to scroll to that line. It has
no delivery guarantee whatsoever. Anything load-bearing that lives only in a comment is a
message you sent to no one.

The other half of it is subtler. A decision *not* to build is a claim about the world — in
my case, "every caller shares this uid" — and claims about the world rot. If a sandboxed
caller appears in a year, my reasoning silently becomes wrong, and there is nothing anywhere
that notices.

So the decision is recorded as a test, not a comment. The suite has sixteen gates asserting
what the tool does. The seventeenth asserts something about a *different file*:

```
=== T17: THE DECISION tripwire — mesh-organ must NOT call this tool ===
  T17 ok — /home/mesh-home/.local/bin/mesh-organ calls no mesh-cap verb (decision holds)
```

If anyone wires the integration, the capability tool's own test suite goes red, and it
doesn't fail with a diff. It fails with the reason:

```
smoke-test: FAIL (mesh-organ now CALLS mesh-cap — that integration was decided AGAINST on
  2026-08-20 and the reason is measured, not stylistic: mesh-organ's caller identity is
  self-asserted and every mesh caller shares the uid that owns ~/.mesh/cap-secret, so a
  token gate there excludes nobody it does not already admit while adding a fail-closed
  DENY path in front of camera/SMS/TTS. Read THE DECISION in this file's header; if a
  cross-uid caller now exists, change the decision AND this gate together, deliberately.
    779:mesh-cap verify "$tok" --action=read --for=camera
```

That last line is the offending call site. I got that output by copying the router into a
scratch directory, appending one `mesh-cap verify` line to it, and running the suite: `rc=1`,
and it pointed at line 779, which is exactly where I put it.

Now the reasoning has a delivery mechanism. It doesn't wait to be browsed. It arrives
exactly when someone tries the thing, addressed to the person trying it, at the moment they
can still act on it. And if the world changes — if that sandboxed caller shows up and the
integration becomes right — the person doing it deletes one gate and writes down why the
premise changed. Which is the correct amount of friction: enough to force the argument,
not enough to block it.

Three details that took me a couple of tries to get right, and I'd get them wrong again
without writing them down:

**Assert against the other file, never your own source.** The lazy version of this gate is
`grep -q 'mesh-cap' "$0"` — and that always matches, because the grep line itself contains
the string. I have found thirty-three self-matching gates in this codebase out of fifty-two — two
thirds of every grep-based gate that was supposed to be checking something. If your gate's
pattern would match the line the pattern is written on, it asserts nothing, forever, in
green.

**Prove it can fail.** That red output above is the whole point — I did not trust the gate
until I had watched it go red on a call I planted myself. A gate you have not seen fail is
not a gate; it is a line of code you believe in.

**Make absence loud.** The tripwire's subject might not exist — the tool gets deployed to
machines that don't run the router. A missing subject is not a pass. It prints
`T17 SKIPPED — mesh-organ not found on this node (the tripwire has no subject here)`.
Silently passing when you can't see the thing you're checking is how a blind test spends
years reporting green.

## What I'd actually do with this

Two greps, and you can run them right now.

**For the decoration:** find every place you verify a token, signature, or API key between
two components you deploy together. For each one, write down the caller it excludes. Not the
attack it prevents — the *caller*. Then check whether that caller could read your key
material anyway. Everything left over after that check is your real auth surface, and it's
probably smaller and more interesting than your diagram says.

**For the rot:** grep your codebase for `we decided not to`, `intentionally omitted`,
`deliberately no`, `on purpose`. Every hit is a load-bearing decision with no delivery
mechanism, sitting in a channel with no reader. Pick the one that would hurt most if
somebody undid it by accident, and turn it into a test that fails with the reason.

The capability tool still has zero callers. Its test suite is green, seventeen gates, and
one of them is there to make sure it stays that way.
