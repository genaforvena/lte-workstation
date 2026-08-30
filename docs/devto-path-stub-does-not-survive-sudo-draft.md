---
title: Your fake binary on PATH does not survive sudo, and the test does the real thing instead of failing
tags: bash, testing, linux, devops
canonical_url:
---

The standard way to test a script that shells out to some dangerous command is to put a fake copy of
that command first on `PATH`, run the script, and assert on what the fake recorded. It is cheap, it
needs no container, and it works — right up until the code under test escalates.

Here is the whole thing, measured on the box I am writing this from:

```
$ cat "$stub/tailscale"
#!/bin/sh
echo "STUB REACHED: $*"
exit 7

$ PATH="$stub:$PATH" tailscale --version
STUB REACHED: --version

$ PATH="$stub:$PATH" sudo -n tailscale --version
1.102.2
  tailscale commit: 6cac918179d4d673bfebe2fc74f81183ddd73fea
```

Same shell. Same `PATH`. Same command. The second one reached the real binary.

## Why

`sudo` does not inherit your environment. Two lines in `/etc/sudoers` on this machine, both stock
Debian/Ubuntu defaults:

```
Defaults    env_reset
Defaults    secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
```

`env_reset` throws away the environment you handed it. `secure_path` then replaces `PATH` with that
fixed list — which contains no `/tmp`, no `~/.local/bin`, and nothing else a test harness could
write to without being root already. This is not a misconfiguration to fix; it is the entire point
of `secure_path`. It exists specifically so that a user who controls `PATH` cannot decide what runs
as root.

Which means: **the security property that makes `sudo` safe is exactly the property that silently
uninstalls your test double.**

## The part that makes it worse than a broken test

If this merely broke the test, it would be a nuisance. It does not break the test.

The function I was looking at tries unprivileged first, then falls back:

```bash
ts_set(){
  local out
  if out="$(timeout 15 tailscale set "$@" 2>&1)"; then printf '%s' "$out"; return 0; fi
  local unpriv="$out"
  if out="$(timeout 15 sudo -n tailscale set "$@" 2>&1)"; then printf 'via-sudo %s' "$out"; return 0; fi
  ...
}
```

That is a good shape — a machine that has been configured not to need root should not be pushed
through one. But now trace a test that stubs `tailscale` to deny, in order to exercise the refusal
path:

1. The stub is reached. It denies. Correct so far — this is the branch under test.
2. The fallback fires: `sudo -n tailscale set ...`
3. `secure_path` discards the stub directory.
4. The **real** `tailscale` runs.

And this box is:

```
mesh-home ALL=(ALL) NOPASSWD:ALL
```

so step 4 needs no password and no prompt. The command in question changes the machine's network
egress. The "smoke test" would have reconfigured the live route out of the host — the same route the
operator reaches the host over — and then reported green, because as far as the test could tell the
command succeeded.

The failure mode of a defeated test double is not a red test. **It is the real action, performed on
the real system, reported as a pass.** A red test tells you something. This tells you nothing, and
does the thing.

I want to be precise about how this generalises, because there is a weaker and much better-known
version of it: a subject that sets its own `PATH` will also lose your stub. That one is your code's
fault and you can fix it in your code. This one is not. You cannot make `sudo` honour your `PATH`
from the calling side — that is what it is for — so no amount of care inside the script under test
removes the hole. The boundary itself is the problem.

## The fix is to stub the thing that is still on your PATH

You cannot fake what runs *behind* `sudo`. You can fake `sudo`.

`sudo` is resolved from the caller's `PATH`, by the caller, before any privilege exists. So it is
stubbable by exactly the mechanism that failed for the binary behind it:

```bash
printf '#!/bin/sh\necho "sudo: a password is required" >&2\nexit 1\n' > "$stubdir/sudo"
chmod +x "$stubdir/sudo"
```

Now the escalation path is closed at the boundary rather than open past it, and — this is the useful
part — you have also made the "no sudo available" branch testable, which is a real branch that
otherwise only ever runs on someone else's machine.

Two things worth keeping around this:

**Run the subject under a private `HOME` too.** `env -i HOME="$fake" PATH="$stubdir:/usr/bin:/bin"`,
with the fake home's `bin` *being* the stub dir. Otherwise a subject that resolves tools relative to
`$HOME` walks straight out of your sandbox by a second door.

**If the library that holds the escalating call is missing, exit non-zero — do not fall back to a
raw call.** The temptation is `command -v mylib || do_it_directly`. That silently reintroduces the
unstubbed path in exactly the environment where something is already wrong.

## The second trap, from the same afternoon

Related, and it is the reason the first version of this test appeared to hang rather than to
misbehave.

The tool under test backgrounds a child — an auto-revert timer that undoes the change after N
seconds if nobody confirms. Capturing the tool's output with `$( )` does this:

```
$ time ./tool >/dev/null          # run it, do not capture
real 0m0.001s

$ out=$(./tool 2>&1)              # same tool, captured
real 0m6.003s
$ echo "$out"
done, returning immediately
auto-revert fired
```

Command substitution reads until **end of file on the pipe**, not until the command exits. The
backgrounded child inherited that same stdout, so the write end stays open for the child's entire
lifetime. The tool returned in one millisecond; the capture blocked for six seconds and then
handed back a line the tool never returned.

Two consequences, and the second one is the nasty one:

- Your timing measurement is now the child's lifetime, not the tool's. A test with a timeout around
  it is measuring the timeout.
- By the time the capture unblocks, the auto-revert child has already **run**. So the test then
  inspects state that has been torn down, and reports on a world that no longer exists.

The fix is to not let the child hold the pipe: redirect the background child's stdout somewhere else
at the point you launch it (`( ... ) >/dev/null 2>&1 &`), or capture to a file and read the file
rather than using `$( )`.

> A test that waits on the child it is testing is not measuring the tool.

## The frame underneath all of it

The bug that started this was small and boring: a `tailscale set ... 2>/dev/null` that threw away
its own refusal, so a permanently denied call was indistinguishable from a branch that simply did
not apply. That had already been found and fixed once — at **one** call site. Three identical raw
calls in a sibling script were untouched, and stayed broken.

So the fix was not a fourth careful copy of the call. It was one sourced function, both callers
using it, no third copy left to forget. When a defect is "we repaired this at one call site and it
survived at its sibling", writing the repair a second time by hand is the same defect, one round
later.
