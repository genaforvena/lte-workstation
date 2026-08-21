# Getting the core onto a machine

The whole point of this being a skill rather than a repository is that planting must be one small
act. If planting starts with `git clone`, it is not planting a culture, it is deploying a system —
and the person you are planting for will, correctly, not do that.

## If you are already on the machine

You are Claude Code with this skill loaded. Write the file:

```sh
mkdir -p ~/.mishe/bin
cp "$CLAUDE_SKILL_DIR/core/mishe" ~/.mishe/bin/mishe 2>/dev/null \
  || cp ~/.claude/skills/mishe-mishe-to-tauftauf/core/mishe ~/.mishe/bin/mishe
chmod +x ~/.mishe/bin/mishe
~/.mishe/bin/mishe --test
```

If neither path resolves, you have the file contents in the skill you are reading — write it out
directly. It is one file and it is meant to be readable.

## If the machine has nothing yet

Someone with the mesh generates a seed and sends it — one file, over any channel that carries a
file or a paste:

```sh
mesh-mishe --seed            # writes ~/.mesh/mishe-seed.sh
```

The recipient runs `sh mishe-seed.sh`. It writes `~/.claude/skills/mishe-mishe-to-tauftauf/` and
`~/.mishe/bin/mishe`, runs the core's self-test, and stops. No network. No package manager. No
clone. Nothing outside their home directory. Nothing scheduled, and nothing installed.

`mishe view` (step 3 of `planting.md`) does not change that. Where tmux already exists it only
raises a session; where it does not, it **prints** the install command and one question for the
human, and returns non-zero. Printing a command is not running it, and `mishe --test` asserts the
difference directly: the package managers are shimmed to record every call, the degraded path is
driven, and the gate fails if the log is non-empty. It has been seen red against a mutant that
ran `apt-get`/`brew` from that branch.

It is deliberately **plain text, not base64**: someone who is about to run a script from a friend
should be able to read what it does, and an opaque blob teaches them a habit we do not want them
to have.

## Verify what arrived, not that it arrived

On the sending side, `mesh-mishe --test` plants the seed into a throwaway home directory and
asserts the planted core actually works — that files arrive byte-identical, that a claim written on
the new node is visible, that nothing got scheduled, and that nothing got installed (the
package managers are shimmed too, so a `brew install` anywhere in the plant is a recorded call). It does not assert that the file exists;
that assertion is worth nothing.

On the receiving side, the test that matters is not the seed's own output. It is step 5 of
`planting.md`: a real answer, about their real work, that they actually read.

## What is deliberately not here

- **No auto-update.** A planted node does not phone home and does not pull. If the culture changes,
  a person carries the change, the same way it arrived. A silent updater is a second writer nobody
  can see.
- **No registration.** Nothing anywhere records that this machine exists. There is no fleet.
- **No telemetry.** The board is theirs, local, and readable. Nothing leaves.
