# Sound repo dirty inventory — 2026-09-14

Task: `sound-repo-dirty-inventory-20260914/inventory-untracked-grind-scripts`

## Finding

`~/grainneukeln` has four untracked executable shell scripts. `git status --short
--untracked-files=all` names only these four paths; `git ls-files` returns none of them. A repository
search finds no references to these filenames outside the files themselves. Their headers describe
personalized, finite batches and seeded recipes, which classifies them as operator/author batch
scripts rather than generated build output. Exact authorship cannot be established from Git because
they have no tracked history. The cited `mesh-grind-params.py` generator is not present in the
repository search results; the recipe arrays are embedded in the scripts.

| Path | Bytes; mtime UTC | SHA-256 | Visible purpose and dependencies |
|---|---:|---|---|
| `operator_ole_25.sh` | 1,456; 2026-09-09 10:13:59 | `6837cba3aac199d43387619b9fc0b77ff05bb17b70ffa1760e5471e67d3fabc5` | 25 `mesh-room-music --remix` renders from `downloads/operator-mWEvjzbTLR4/John Coltrane   Olé.mp3`, then validates and calls `mesh-room-music --deliver` per render. Requires `mesh-room-music`, `timeout`, `ffprobe`, and core shell utilities. Source exists (26,377,965 bytes); output directory exists with 2 files. |
| `sasha_dontbesad_grind.sh` | 5,161; 2026-09-03 02:12:56 | `cfa75e0f5769b303658a243b5277383164196836fa7f078aa809a156354dab67` | 25 seeded parameter sets and 95-second slices from `$HOME/.mesh/tg-inbox/1842929-_____-_Dont_be_sad__Master.wav`; grinds with local `main.py`/`.venv/bin/python`, validates via `mesh-song-verify`, and may trim through `mesh-sound-reflex`. Requires `ffmpeg`, `timeout`, and shell utilities. Source exists (142,704,746 bytes); output directory exists with 72 files. |
| `sasha_vnov_c_grind.sh` | 5,416; 2026-09-02 23:51:20 | `8a3754648023a909b2b289009a1314831b9f99bb2ff085f336f0228ae38771e0` | Second 25-recipe batch from `$HOME/.mesh/inbox/Саша - Вновь и вновь_Master.wav`; local `main.py`/`.venv/bin/python`, `ffmpeg`, `mesh-song-verify`, `mesh-sound-reflex`, and `timeout`. Source exists (108,511,506 bytes); output directory exists with 117 files. |
| `sasha_vnov_grind.sh` | 5,452; 2026-09-02 22:32:14 | `09b3e13b91466a69f337ea786c5490e901208687054ccac3d40bf8567c039dc3` | First 25-recipe batch from the same Vnov source, with local `main.py`/`.venv/bin/python`, `ffmpeg`, `mesh-song-verify`, `mesh-sound-reflex`, and `timeout`. Source exists; output directory exists with 79 files. |

## Verification and disposition

`bash -n` passed for all four scripts. The referenced sources, local grind entry points, mesh audio
tools, and output directories exist. No script was executed: three perform up to 25 expensive local
grinds, and the Olé script additionally delivers 25 messages; running them would create substantial
outputs and external side effects. No files in `~/grainneukeln` were edited by this inventory.

Disposition: preserve all four untracked scripts and their output directories. The evidence supports
that they are intentional one-off operator/author batch work, but does not establish whether they
should be versioned. Do not commit, delete, or rerun them without an explicit repo decision. The
grainneukeln worktree remains dirty by these same four paths.
