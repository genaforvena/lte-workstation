---
title: A bare git pull wrote three-day-old code over the fix it had just fetched
tags: git, devops, automation, debugging
canonical_url:
---

Two lines of git config, both of them the sort of thing you set once and never look at again:

```
git config pull.rebase true
git config rebase.autoStash true
```

With those on, here is a `git pull` I ran on git 2.43.0 while writing this paragraph. Upstream
had a fix in it. My working tree had an unrelated line in it that was three days old.

```
$ git pull
From /tmp/.../origin
   d568744..670a133  main       -> origin/main
Updating d568744..670a133
Created autostash: 627da2a
Fast-forward
 tool.sh | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
Applied autostash.
$ echo $?
0
```

Nothing in that output is a warning. Now the file:

```
$ cat tool.sh
header v2 FIXED
body v1
footer ANCIENT

$ git show HEAD:tool.sh
header v2 FIXED
body v1
footer v1
```

The third line is not what the pull fetched. It is what my working tree was carrying from three
days ago, written back over the top of the fetch, silently, by the pull itself.

And then the part that ruined a day for me:

```
$ stat -c '%y' tool.sh
2026-08-30 02:04:12.307739896 +0000
$ date -u +'%Y-%m-%dT%H:%M:%SZ'
2026-08-30T02:04:12Z
```

**The content is three days old and the timestamp is now.** Not approximately now. The same
second. `git pull` manufactured a file whose age and whose origin point in opposite directions,
and it did it without being asked and without saying so.

I have written before that [mtime is not a
claim](https://dev.to/ilya_mozerov_867dbdd91feb/mtime-is-not-a-claim-36en). That post argued the
timestamp can lie. This one names a tool in everybody's `$PATH` that makes it lie, on purpose, as
a convenience feature.

## The reproducer

Paste this. It is self-contained and it takes about a second.

```bash
set -e
D=$(mktemp -d); cd "$D"
git init -q --bare origin.git
git init -q seed && cd seed
git config user.email t@t; git config user.name t
printf 'header v1\nbody v1\nfooter v1\n' > tool.sh
git add -A && git commit -qm v1
git push -q ../origin.git HEAD:refs/heads/main
cd ..

git clone -q -b main origin.git peer
git clone -q -b main origin.git node

# a colleague pushes a fix upstream
cd peer
git config user.email t@t; git config user.name t
printf 'header v2 FIXED\nbody v1\nfooter v1\n' > tool.sh
git commit -qam v2 && git push -q origin main

# your node: behind, with a stale dirty worktree, and the two config lines
cd ../node
git config user.email t@t; git config user.name t
git config pull.rebase true
git config rebase.autoStash true
printf 'header v1\nbody v1\nfooter ANCIENT\n' > tool.sh

git pull            # rc 0, no warning
cat tool.sh         # the fetched fix AND the ancient line
```

The mechanism is not subtle once you see it. `--autostash` stashes your dirty tree, moves HEAD to
upstream, and then **re-applies that tree on top of the files it just fetched**. A stash is a diff,
and a diff does not know how old it is. If your stale hunks and upstream's hunks touch different
regions of the file, the three-way merge succeeds, git prints `Applied autostash.`, and you are
left holding a file that is part fresh and part fossil with no marker anywhere saying which part
is which.

## The variant that is arguably worse

Change one thing in the reproducer — make the stale edit and the upstream fix touch the *same*
line — and you get this:

```
$ git pull --rebase --autostash
...
Applying autostash resulted in conflicts.
Your changes are safe in the stash.
$ echo $?
0
$ git status --porcelain
UU tool.sh
$ git diff --check | wc -l
3
```

Exit code zero, with conflict markers sitting in the working tree. `<<<<<<< Updated upstream` is
in the file. Git told you, on stdout, in a sentence, and then returned success anyway.

Every `git pull && make` in every deploy script on earth walks straight through that. So does
every CI step that checks `$?`. The one channel a script actually reads is the one channel that
says everything is fine.

## The evidence deletes itself

In the conflict case git says "Your changes are safe in the stash", and they are. In the *clean*
case — the silent one, the dangerous one — it drops the stash:

```
$ git stash list
$ git reflog stash
fatal: ambiguous argument 'stash': unknown revision or path not in the working tree
$ git fsck --no-reflogs
dangling commit 627da2a83474858795db626df235a5212fe6b6a8
dangling tree 3cc4ed3ec074be75d7721aa48579ae567e483d57
```

The only remaining record that a three-day-old tree was replayed over your pull is a dangling
commit that `git gc` will collect. `git stash list` is empty. There is no ref. If you go looking
a week later for how the old line got back in, there is nothing to find.

## Why every gate I had was green

This is the part that made me write the post rather than just fix the bug.

I run a small automation that commits work my agents produce. It has three criteria, and it is
honest enough to print them in its own commit message, every single time:

```
mesh-land: land 1 settled stream fix(es): mesh-job-apply

Stream-produced genome fixes that posted [done] but weren't committed (commits are
steward-centralised by design). Settled (stable mtime > 600s), parse-clean,
steward-reviewed. Landed + deployed by mesh-land.
```

Settled. Parse-clean. Reviewed. A replayed old tree satisfies all three, and it satisfies them
*by construction*, which is a different and much worse thing than satisfying them by luck.

**"Settled (stable mtime > 600s)" asks the clock.** We just measured what the clock says: the
pull stamped the file at the current second. Wait ten minutes and a three-day-old line has
"settled" exactly as hard as a change somebody finished thinking about ten minutes ago. The gate
is not weak here. It is answering a question about *provenance* by measuring *age*, and those
two quantities were pulled apart by the pull itself.

**"parse-clean" asks the form.** It always passes. A rollback is somebody's formerly-working
code. It parsed when it was written and it parses now. Running the test suite does not help
either, for the same reason — the reverted version was green on the day it shipped. Any check
that asks "is this well-formed?" is structurally incapable of noticing that well-formed code has
travelled backwards in time.

**And the log cannot tell you.** That commit subject is one template. It is byte-identical for a
real fix and for a revert wearing a fix's clothes, so the history is no help to a human reading
it afterwards either. What landed was a revert of a retry loop, committed under the words
"1 settled stream fix". It then conflicted with upstream permanently and jammed the very lane
that landed it. The board tape I can still read holds 38 `[strand]` posts over its three-day
window, and that tape is a sliding window, so 38 is a floor, not a count.

Age, form, wording. Three gates, three greens, one revert in production.

## What actually separates them

The question none of those gates asked is: **where did these bytes come from?**

There is a cheap answer. A candidate whose content is byte-identical to the blob that its own
path carried at some *ancestor of HEAD* is not an edit. It is the tree moving backwards.

```bash
H=$(git hash-object tool.sh)
for c in $(git rev-list HEAD -- tool.sh); do
  if [ "$(git rev-parse "$c:tool.sh" 2>/dev/null)" = "$H" ]; then
    echo "ROLLBACK: identical to the blob at $(git log -1 --format='%h %s' $c)"
  fi
done
```

Driven against a working tree holding a former version:

```
ROLLBACK: identical to the blob at 57f169f v0 no retry
```

and against a genuine new edit, on the same file, in the same repo, one command later:

```
matched an ancestor? 0
```

Both arms. A gate you have never watched fail is not a gate, so the negative arm matters as much
as the positive one — this thing has to stay quiet on ordinary work or it will be turned off
within a day.

Note `git rev-list HEAD -- tool.sh`: walk the revisions *of that path*, not of the repository.
On a real history the difference is between a few dozen commits and a few hundred thousand.

The other half is on the cause side, and it is blunter: **refuse to rebase at all while a stale
autostash is parked.** If the working tree is older than your settle window, the honest move is
to stop and name the files, not to merge them into whatever arrives.

And if you want none of this, the flag exists:

```
$ git pull --rebase --no-autostash
error: cannot pull with rebase: You have unstaged changes.
error: Please commit or stash them.
$ echo $?
128
```

Loud, non-zero, worktree untouched. That is what the failure was supposed to look like the whole
time.

## What this does not catch

The blob comparison is an exact-match floor and I want to be precise about where it stops. If
autostash replays your stale tree over an upstream change that touched *other* lines, the result
is a hybrid: part fossil, part fresh, byte-identical to nothing that ever existed. No ancestor
blob matches it. The check stays silent and the hybrid lands.

That is not a hole I have closed. It is the shape of the fix: exact reverts are caught, blends
are not, and I would rather say so than let the gate wear a completeness it does not have.

## The general form

I keep meeting this one and it never announces itself the same way twice:

- **Age is not origin.** Anything that decides readiness by asking how old a file is — settle
  gates, watch-and-build loops, deploy-on-quiet, incremental build systems — is asking the clock
  a question the clock cannot answer. It works right up until something writes old content with a
  new timestamp, and then it fails in the confident direction.
- **Form is not origin.** Parse-clean and test-green are green by construction on anything that
  ever worked. Against a rollback they contribute exactly nothing while looking like two
  independent confirmations.
- **A convenience that hides a conflict will eventually hide a regression.** `--autostash` exists
  to spare you a stash/pop dance. The dance was the part where you looked at what you were
  carrying.

If you have `rebase.autoStash = true` set globally, you have this. I cannot tell you how likely
you are to hit it; I can tell you that when you do, the exit code will be zero, the timestamp
will be fresh, your tests will pass, and the stash will already have been dropped.
