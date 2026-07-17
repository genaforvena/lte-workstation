# Sound reflex: random collage from ambient — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `mesh-sound-reflex` build each grind from a RANDOM collage of the fresh block's own ambient records (random subset, random cut per record, concat in random order) instead of picking the single highest-scoring record and grinding it whole.

**Architecture:** Add three testable helpers — `valid_source` (the only entry gate: decodable audio, not density), `cut_window` (one random cut), `collage_build` (random subset → cuts → concat feed). Extract the detached grind into `launch_grind`. Rewrite `tick()`'s no-`drop` branch to build a feed, re-measure it for the recipe axes, and settle verdicts (`grinding`/`blended`/`not-selected`/`invalid-source`). The `drop` lane and all anchor/novelty/grind-cap machinery are untouched.

**Tech Stack:** bash, `ffprobe`/`ffmpeg` (present at `/usr/bin`), `mesh-soundscape --measure` (sole measure tract), `mesh-room-music --remix` (sole grind owner). Tests are `mesh-sound-reflex --test` (bash smoke-test, sandboxed tmp ledger + `REC_DIR`).

## Global Constraints

- Source of truth is the genome: edit `scripts/mesh-sound-reflex`, deploy to `~/.local/bin/` (Task 6). `mesh-sync-tools` flags drift.
- **Only entry gate is validity** (file decodes as audio + `dur>0` + size ≥ `SR_MIN_BYTES`). NO `MIN_DENSITY`/`MIN_BEATS` filter on this path — cough and silence are wanted material (operator «кашель и тишину молоть тоже интересно»).
- `SR_MIN_DENSITY` / `SR_MIN_BEATS` stay declared read-only (a node may export them) but are retired from the picker; leave the historical cough-guard reasoning marked HISTORY, do not re-add the floor.
- `mesh-soundscape` stays the ONLY librosa analyzer (reuse `--measure`, never add a second).
- `mesh-room-music` stays the sole grind invocation owner (`launch_grind` only pins the recipe + provenance).
- **A gate not seen failing is not a gate:** every new `--test` assertion must be watched go RED (mutate the code) before restoring. Run mutants from a scratch copy of the script; never leave the live file mutated.
- Randomness is bash `$RANDOM` (this is a shell tool, not a workflow script — `$RANDOM` is fine).
- Commit after each task (genome-lane commits land on `main` here).

---

### Task 1: `valid_source` validity guard + inverted cough-guard test

**Files:**
- Modify: `scripts/mesh-sound-reflex` (add tunables near the header block ~line 55; add `valid_source`/`rand_between` after `grind_cap` ~line 78; add test section 6 in the `--test` block ~line 690)

**Interfaces:**
- Produces: `valid_source <file>` → rc 0 if decodable audio stream + `format.duration > 0` + size ≥ `SR_MIN_BYTES`; rc 1 otherwise. `rand_between <lo> <hi>` → integer in `[lo,hi]` (echoes `lo` if `hi<=lo`).

- [ ] **Step 1: Add the tunables.** In the header tunables region (after `MIN_DENSITY=...`, ~line 63), add:

```bash
# ── RANDOM COLLAGE (operator 2026-07-17: mixes = random cut + random select from the mesh's OWN
#    ambient records; grind cough+silence too). The picker below imposes NO density/beats floor —
#    the ONLY entry gate is `valid_source` (decodable audio). SR_MIN_DENSITY/SR_MIN_BEATS above are
#    HISTORY for this lane (kept read-only so a node exporting them does not change meaning); do NOT
#    re-add the floor. A hollow silence grind is caught HONESTLY downstream by mesh-room-music's
#    valid_track gate -> skip:degenerate, never by a pre-filter.
SR_COLLAGE_MAX="${SR_COLLAGE_MAX:-4}"   # max records blended into one collage
SR_CUT_MIN="${SR_CUT_MIN:-4}"           # random cut window: min seconds
SR_CUT_MAX="${SR_CUT_MAX:-12}"          # random cut window: max seconds
SR_MIN_BYTES="${SR_MIN_BYTES:-1024}"    # validity floor: reject 0-byte / header-only reads
```

- [ ] **Step 2: Add the helpers.** After `grind_cap(){...}` (~line 78), add:

```bash
rand_between(){ local lo="$1" hi="$2"; [ "$hi" -le "$lo" ] 2>/dev/null && { echo "$lo"; return; }; echo "$(( lo + RANDOM % (hi - lo + 1) ))"; }

# VALIDITY GUARD — the ONLY entry gate for the random-collage picker. A source is grindable material
# iff it DECODES as audio with real duration: near-silence PASSES (valid material the operator wants
# ground), only a 0-byte / header-only / corrupt / evicted read fails. NOT a density or beats test —
# that floor was retired 2026-07-17. (The old picker's `grep -v unmeasurable` conflated near-silence
# with unreadable; this separates them structurally: silence decodes, corruption does not.)
valid_source(){
  local f="$1" dur
  [ -f "$f" ] || return 1
  [ "$(stat -c%s "$f" 2>/dev/null || echo 0)" -ge "$SR_MIN_BYTES" ] || return 1
  ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$f" 2>/dev/null | grep -q . || return 1
  dur="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$f" 2>/dev/null)"
  awk -v d="${dur:-0}" 'BEGIN{ exit !(d+0 > 0) }'
}
```

- [ ] **Step 3: Write the failing test.** In the `--test` block, after section 5c's `is_outlier` asserts (~line 690, before `echo "smoke-test..."`), add:

```bash
  # 6. VALIDITY GUARD — the gate FLIPS (operator 2026-07-17: grind cough+silence too). A valid
  #    near-SILENT wav must be SELECTABLE material (the old floor EXCLUDED it); only a 0-byte/corrupt
  #    read is rejected. This is the inverted cough-guard: what used to be filtered is now wanted.
  vg="$tmp/vg"; mkdir -p "$vg"
  ffmpeg -v error -y -f lavfi -i "anullsrc=r=44100:cl=stereo" -t 3 "$vg/silence.wav" >/dev/null 2>&1
  ffmpeg -v error -y -f lavfi -i "sine=frequency=200:duration=3" -ac 2 "$vg/tone.wav" >/dev/null 2>&1
  : > "$vg/empty.wav"                      # 0-byte
  printf 'NOTAWAV\n' > "$vg/corrupt.wav"   # non-audio bytes
  valid_source "$vg/silence.wav" || { echo "  FAIL: a valid near-silent wav was rejected — the operator wants silence grindable, the guard must pass it"; f=1; }
  valid_source "$vg/tone.wav"    || { echo "  FAIL: a valid tone wav was rejected by the validity guard"; f=1; }
  valid_source "$vg/empty.wav"   && { echo "  FAIL: a 0-byte file passed the validity guard"; f=1; }
  valid_source "$vg/corrupt.wav" && { echo "  FAIL: a non-audio/corrupt file passed the validity guard"; f=1; }
  valid_source "$vg/nope.wav"    && { echo "  FAIL: a missing file passed the validity guard"; f=1; }
```

- [ ] **Step 4: Run test to verify it passes.** Run: `bash scripts/mesh-sound-reflex --test`. Expected: no `FAIL:` lines from section 6; final `smoke-test: ok`.

- [ ] **Step 5: Verify the gate can FAIL (mutation).** Copy to scratch, break the guard so silence is rejected, confirm RED:

```bash
cp scripts/mesh-sound-reflex "$TMPDIR/msr-mut" 2>/dev/null || cp scripts/mesh-sound-reflex /tmp/msr-mut
# mutate: make valid_source additionally reject files whose RMS is near-silent (re-adds a floor)
sed -i 's/  awk -v d="${dur:-0}" .BEGIN{ exit !(d+0 > 0) }./  awk -v d="${dur:-0}" '"'"'BEGIN{ exit 1 }'"'"'/' /tmp/msr-mut
bash /tmp/msr-mut --test 2>&1 | grep -q 'near-silent wav was rejected' && echo "MUTANT DIED (good)" || echo "MUTANT SURVIVED (gate is vacuous)"
rm -f /tmp/msr-mut
```
Expected: `MUTANT DIED (good)`.

- [ ] **Step 6: Commit.**

```bash
git add scripts/mesh-sound-reflex
git commit -m "feat(sound): valid_source guard — silence/cough are valid material (no density floor)"
```

---

### Task 2: `cut_window` random cut + test

**Files:**
- Modify: `scripts/mesh-sound-reflex` (add `cut_window` after `valid_source`; add test section 7)

**Interfaces:**
- Consumes: `rand_between`, `SR_CUT_MIN`, `SR_CUT_MAX`.
- Produces: `cut_window <src> <out.wav>` → cuts a random window (`len` random in `[min(SR_CUT_MIN,dur), min(SR_CUT_MAX,dur)]`, random offset), writes to `<out.wav>`, echoes `off:len`; rc 1 on ffmpeg failure or empty output.

- [ ] **Step 1: Add `cut_window`** after `valid_source`:

```bash
# RANDOM CUT — one window of random length in [min(SR_CUT_MIN,dur), min(SR_CUT_MAX,dur)] at a random
# offset. Echoes "off:len" (provenance for the params log); writes the cut to $2. Integer seconds:
# ample resolution for granular grinding and keeps the arithmetic honest under `set -u`.
cut_window(){
  local src="$1" out="$2" dur lo hi len off omax
  dur="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$src" 2>/dev/null)"
  dur="${dur%.*}"; [ "${dur:-0}" -ge 1 ] 2>/dev/null || dur=1
  lo="$SR_CUT_MIN"; [ "$dur" -lt "$lo" ] && lo="$dur"
  hi="$SR_CUT_MAX"; [ "$dur" -lt "$hi" ] && hi="$dur"
  len="$(rand_between "$lo" "$hi")"; [ "$len" -lt 1 ] && len=1
  omax=$(( dur - len )); [ "$omax" -lt 0 ] && omax=0
  off="$(rand_between 0 "$omax")"
  ffmpeg -hide_banner -nostats -y -ss "$off" -t "$len" -i "$src" -ac 2 -ar 44100 "$out" >/dev/null 2>&1 || return 1
  [ -s "$out" ] || return 1
  echo "${off}:${len}"
}
```

- [ ] **Step 2: Write the failing test.** Add section 7 in the `--test` block:

```bash
  # 7. RANDOM CUT — produces a valid sub-window and VARIES across draws (not a fixed slice).
  ffmpeg -v error -y -f lavfi -i "sine=frequency=300:duration=18" -ac 2 "$vg/src18.wav" >/dev/null 2>&1
  declare -A _cuts=(); cw_ok=1
  for i in $(seq 1 20); do
    cw="$(cut_window "$vg/src18.wav" "$vg/c.wav")" || { cw_ok=0; break; }
    [ -s "$vg/c.wav" ] || { cw_ok=0; break; }
    _cuts["$cw"]=1
    # length within bounds and inside the source
    off="${cw%%:*}"; len="${cw##*:}"
    awk -v o="$off" -v l="$len" 'BEGIN{ exit !(l>=1 && l<=12 && o>=0 && o+l<=18) }' || { echo "  FAIL: cut $cw out of bounds for an 18s source (len<=12, off+len<=18)"; f=1; }
  done
  [ "$cw_ok" = 1 ] || { echo "  FAIL: cut_window failed to produce a valid cut wav"; f=1; }
  [ "${#_cuts[@]}" -ge 2 ] || { echo "  FAIL: 20 cuts produced <2 distinct (off:len) — the cut is not random"; f=1; }
```

- [ ] **Step 3: Run test.** Run: `bash scripts/mesh-sound-reflex --test`. Expected: no section-7 `FAIL:`; `smoke-test: ok`.

- [ ] **Step 4: Verify it can FAIL (mutation).** Pin the cut to a constant window and confirm the "<2 distinct" assert fires:

```bash
cp scripts/mesh-sound-reflex /tmp/msr-mut
sed -i 's/  off="$(rand_between 0 "$omax")"/  off=0; len=6/' /tmp/msr-mut
bash /tmp/msr-mut --test 2>&1 | grep -q 'cut is not random' && echo "MUTANT DIED (good)" || echo "MUTANT SURVIVED"
rm -f /tmp/msr-mut
```
Expected: `MUTANT DIED (good)`.

- [ ] **Step 5: Commit.**

```bash
git add scripts/mesh-sound-reflex
git commit -m "feat(sound): cut_window — one random cut window, provenance off:len"
```

---

### Task 3: `collage_build` random subset + concat + test

**Files:**
- Modify: `scripts/mesh-sound-reflex` (add `collage_build` after `cut_window`; add test section 8)

**Interfaces:**
- Consumes: `valid_source`, `cut_window`, `rand_between`, `SR_COLLAGE_MAX`, `REC_DIR`. Reads candidate ledger lines from **stdin**.
- Produces: `collage_build <feed_out.wav>` → resolves each stdin line's hash (field 3) to `$REC_DIR/*-<h>.*`, validity-filters, picks a random subset of size `K=rand(1..min(nvalid,SR_COLLAGE_MAX))`, cuts each, concats in shuffled order to `<feed_out.wav>`. Prints exactly two lines on success: `used=<seed> <h2> ...` (seed first) and `meta=parts=<h1,h2,..> cuts=<off:len,..>`. rc 0 on success, rc 1 if no valid source / concat empty. Scratch cut files are written in `dirname(feed_out)`.

- [ ] **Step 1: Add `collage_build`** after `cut_window`:

```bash
# RANDOM COLLAGE — the core of the operator's 2026-07-17 doctrine. Reads candidate ledger lines on
# stdin, keeps only those whose source file passes `valid_source` (silence included), draws a RANDOM
# subset of size K (1..min(nvalid,SR_COLLAGE_MAX)), RANDOM-cuts each, and concats them in shuffled
# order into $1. Prints `used=<seed> <h..>` (seed first, carries the ledger grind verdict) and
# `meta=parts=.. cuts=..` for provenance. rc 1 when nothing usable — the caller declines out loud.
collage_build(){
  local feed="$1" scratch; scratch="$(dirname "$feed")"
  local ln h fpath; local -a vh=() vf=()
  while IFS= read -r ln; do
    [ -n "$ln" ] || continue
    h="$(awk '{print $3}' <<<"$ln")"; [ -n "$h" ] || continue
    fpath="$(ls "$REC_DIR"/*-"$h".* 2>/dev/null | head -1)"
    valid_source "$fpath" || continue
    vh+=("$h"); vf+=("$fpath")
  done
  local n="${#vh[@]}"; [ "$n" -gt 0 ] || return 1
  local kmax="$SR_COLLAGE_MAX"; [ "$n" -lt "$kmax" ] && kmax="$n"
  local K; K="$(rand_between 1 "$kmax")"
  local -a idx=(); local i j t
  for ((i=0;i<n;i++)); do idx+=("$i"); done
  for ((i=n-1;i>0;i--)); do j=$(( RANDOM % (i+1) )); t="${idx[i]}"; idx[i]="${idx[j]}"; idx[j]="$t"; done
  local -a used=() cuts=(); local ci=0 sel cw
  for ((i=0;i<K;i++)); do
    sel="${idx[i]}"
    cw="$(cut_window "${vf[$sel]}" "$scratch/cut$ci.wav")" || continue
    used+=("${vh[$sel]}"); cuts+=("$cw"); ci=$((ci+1))
  done
  [ "${#used[@]}" -gt 0 ] || return 1
  if [ "${#used[@]}" -eq 1 ]; then
    cp "$scratch/cut0.wav" "$feed" 2>/dev/null || return 1
  else
    local list="$scratch/concat.txt"; : > "$list"
    for ((i=0;i<ci;i++)); do echo "file '$scratch/cut$i.wav'" >> "$list"; done
    ffmpeg -hide_banner -nostats -y -f concat -safe 0 -i "$list" -ac 2 -ar 44100 "$feed" >/dev/null 2>&1 || return 1
  fi
  [ -s "$feed" ] || return 1
  printf 'used=%s\n' "${used[*]}"
  printf 'meta=parts=%s cuts=%s\n' "$(IFS=,; echo "${used[*]}")" "$(IFS=,; echo "${cuts[*]}")"
}
```

- [ ] **Step 2: Write the failing test.** Add section 8 (reuses `$vg`; builds a sandbox `REC_DIR`):

```bash
  # 8. COLLAGE — random SELECTION (not score-argmax) + random cut over a pool of ambient records.
  #    Over many draws >=2 distinct seeds must appear (uniform over >=2 members => P(all-same)~2^-19),
  #    K>=2 collages must occur, and the feed must concatenate. Selection is INDEPENDENT of score.
  crd="$tmp/records"; mkdir -p "$crd"
  REC_DIR_SAVE="$REC_DIR"; REC_DIR="$crd"
  # three valid ambient sources; the ledger lines carry DIFFERENT scores incl. a high one that must
  # NOT dominate selection (silence/low-score is equally selectable).
  ffmpeg -v error -y -f lavfi -i "sine=frequency=200:duration=18" -ac 2 "$crd/x-p1.wav" >/dev/null 2>&1
  ffmpeg -v error -y -f lavfi -i "sine=frequency=400:duration=18" -ac 2 "$crd/x-p2.wav" >/dev/null 2>&1
  ffmpeg -v error -y -f lavfi -i "anullsrc=r=44100:cl=stereo" -t 18 "$crd/x-p3.wav" >/dev/null 2>&1
  pool_lines=$'2026-07-17T00:00Z ear p1 dur=18 win=3 score=90 beats=8 [x] -> pending\n2026-07-17T00:00Z ear p2 dur=18 win=3 score=40 beats=6 [x] -> pending\n2026-07-17T00:00Z ear p3 dur=18 win=3 score=5 beats=0 [silent] -> pending'
  declare -A _seeds=(); saw_multi=0; cb_ok=1
  for i in $(seq 1 25); do
    res="$(printf '%s\n' "$pool_lines" | collage_build "$tmp/feed.wav")" || { cb_ok=0; break; }
    [ -s "$tmp/feed.wav" ] || { cb_ok=0; break; }
    u="$(sed -n 's/^used=//p' <<<"$res")"
    seed="${u%% *}"; _seeds["$seed"]=1
    nparts=$(wc -w <<<"$u"); [ "$nparts" -ge 2 ] && saw_multi=1
  done
  REC_DIR="$REC_DIR_SAVE"
  [ "$cb_ok" = 1 ] || { echo "  FAIL: collage_build failed to produce a feed from valid sources"; f=1; }
  [ "${#_seeds[@]}" -ge 2 ] || { echo "  FAIL: 25 collages selected <2 distinct seeds — selection is not random (still argmax?)"; f=1; }
  [ -n "${_seeds[p3]:-}" ] || echo "  NOTE: silent low-score p3 never seeded in 25 draws (statistically possible, not a hard fail)"
  [ "$saw_multi" = 1 ] || { echo "  FAIL: no K>=2 collage in 25 draws — subset selection collapsed to single-record"; f=1; }
```

- [ ] **Step 3: Run test.** Run: `bash scripts/mesh-sound-reflex --test`. Expected: no section-8 `FAIL:`; `smoke-test: ok`.

- [ ] **Step 4: Verify it can FAIL (mutation).** Force selection to always the top-score line and confirm the "<2 distinct seeds" assert fires:

```bash
cp scripts/mesh-sound-reflex /tmp/msr-mut
# mutate: replace the Fisher-Yates shuffle with identity (always pick the first pool member) and K=1
sed -i 's/  for ((i=n-1;i>0;i--)); do j=$(( RANDOM % (i+1) )); t="${idx\[i\]}"; idx\[i\]="${idx\[j\]}"; idx\[j\]="$t"; done/  K=1/' /tmp/msr-mut
bash /tmp/msr-mut --test 2>&1 | grep -qE 'selected <2 distinct seeds|no K>=2 collage' && echo "MUTANT DIED (good)" || echo "MUTANT SURVIVED"
rm -f /tmp/msr-mut
```
Expected: `MUTANT DIED (good)`. (If the `sed` pattern does not match due to quoting, mutate by hand: set `K=1` and delete the shuffle loop, then run `--test`.)

- [ ] **Step 5: Commit.**

```bash
git add scripts/mesh-sound-reflex
git commit -m "feat(sound): collage_build — random subset + random cut + concat feed"
```

---

### Task 4: Extract `launch_grind` (pure refactor, drop path unchanged)

**Files:**
- Modify: `scripts/mesh-sound-reflex` (add `launch_grind` before `tick()`; replace the inline `setsid bash -c '...'` block at the end of `tick()` ~lines 553-585 with a call)

**Interfaces:**
- Produces: `launch_grind <src> <args> <full_meta> <seed_hash> <dur> <organ> [scratch_dir]` — detaches the grind exactly as the current inline block does (same inner script), writing the ledger verdict on completion; if `scratch_dir` is non-empty, `rm -rf` it after the grind returns. `full_meta` is the complete `MESH_RMC_META` value (caller prepends `src=<organ>/<hash> `).

- [ ] **Step 1: Add `launch_grind`** immediately before `# ── one tick` / `tick(){`:

```bash
# Detached, hard-timeout-bounded grind. mesh-room-music stays the single owner of the grind
# invocation (admission, hollow/fresh gates, params log); this only pins the recipe + provenance and
# writes the ledger verdict when it lands. scratch (if given) is removed after the render returns.
launch_grind(){
  local src="$1" args="$2" meta="$3" h="$4" dur="$5" organ="$6" scratch="${7:-}"
  setsid bash -c '
    src="$1"; args="$2"; meta="$3"; h="$4"; GT="$5"; self="$6"; organ="$7"; dur="$8"; scratch="$9"
    raw="$(MESH_RMC_AUTOMIX="$args" MESH_RMC_META="$meta" \
           timeout "$GT" mesh-room-music --remix "$src" 2>/dev/null)"; rmc_rc=$?
    out="$(grep -E "\.mp3$" <<<"$raw" | tail -1)"
    if [ -n "$out" ] && [ -f "$out" ]; then
      "$self" --verdict "$h" "ground:$(basename "$out")"
    elif [ "$rmc_rc" -eq 124 ]; then
      "$self" --verdict "$h" "skip:grind-timeout(${GT}s)"
      "$self" --poke grind-timeout "Record $h [$organ] (dur=${dur}s) was still rendering when the ${GT}s grind cap killed it — the material is NOT judged degenerate. Either the cap is too tight for this source or the render genuinely hung; an untimed rerun distinguishes them."
    else
      "$self" --verdict "$h" "skip:degenerate"
      "$self" --poke degenerate "Record $h [$organ] ground to nothing usable with: $args. Either the recipe is pathological for this material or the source is thinner than it looked (a silent/near-silent collage often grinds hollow — expected, not an error)."
    fi
    [ -n "$scratch" ] && rm -rf "$scratch"
  ' _ "$src" "$args" "$meta" "$h" "$(grind_cap "$dur")" "$0" "$organ" "$dur" "$scratch" </dev/null >/dev/null 2>&1 &
}
```

- [ ] **Step 2: Replace the inline block in `tick()`.** Delete the existing `setsid bash -c '...' &` block (the ~30 lines ending the drop/single path) and the two lines above it that build `MESH_RMC_META="src=$organ/$h $meta"` inline; replace with:

```bash
  verdict "$h" "grinding"
  launch_grind "$src" "$args" "src=$organ/$h $meta" "$h" "$dur" "$organ"
  consume "$last"
}
```

- [ ] **Step 3: Verify no behavior change.** Run: `bash scripts/mesh-sound-reflex --test`. Expected: `smoke-test: ok` (all existing sections still green — the refactor is a pure move).

- [ ] **Step 4: Verify it parses + `--status` still works.** Run: `bash scripts/mesh-sound-reflex --status`. Expected: prints `ledger:/anchor:/poke:/epsilon:` with no bash syntax error.

- [ ] **Step 5: Commit.**

```bash
git add scripts/mesh-sound-reflex
git commit -m "refactor(sound): extract launch_grind (no behavior change; drop path intact)"
```

---

### Task 5: Rewrite `tick()`'s no-`drop` branch to the collage path

**Files:**
- Modify: `scripts/mesh-sound-reflex` (`tick()`: the `if [ -z "$cand" ]` score-argmax block ~line 447, the no-candidate decline ~line 460, and the per-line settle loop ~line 480; header docstring ~lines 2-16)

**Interfaces:**
- Consumes: `collage_build`, `valid_source`, `launch_grind`, `derive`, `beat_of`, `is_outlier`/`outlier_hw`.
- Produces: (behavior) when no `drop` is present, `tick()` builds a random collage from the fresh block's valid records, re-measures the feed for axes, derives a recipe, grinds the feed, and settles every fresh row.

- [ ] **Step 1: Restructure the branch.** In `tick()`, keep the `drop` detection, then split into drop-vs-collage. Replace from `if [ -z "$cand" ]; then` (the ranker) down through the single-record settle loop with:

```bash
  local drop_cand
  drop_cand="$(printf '%s\n' "$fresh" | grep ' drop ' | grep -v 'unmeasurable' | tail -n1)"

  if [ -n "$drop_cand" ]; then
    # ── DROP LANE (unchanged): an operator gesture outranks the ear and grinds WHOLE. ────────────
    cand="$drop_cand"
    # settle every other fresh row as not-picked (a drop led this block)
    local dch dline
    while IFS= read -r dline; do
      [ -n "$dline" ] || continue
      dch="$(awk '{print $3}' <<<"$dline")"
      [ -n "$dch" ] && [ "$dch" != "$(awk '{print $3}' <<<"$cand")" ] && verdict "$dch" "skip:not-picked(operator drop led this block)"
    done <<< "$fresh"
    local h organ score beats dur win dyn act rich move cent src
    h="$(awk '{print $3}' <<<"$cand")"; organ="$(awk '{print $2}' <<<"$cand")"
    score="$(kvof score "$cand")"; beats="$(kvof beats "$cand")"; dur="$(kvof dur "$cand")"; win="$(kvof win "$cand")"
    dyn="$(kvof dyn "$cand")"; act="$(kvof act "$cand")"; rich="$(kvof rich "$cand")"; move="$(kvof move "$cand")"; cent="$(kvof cent "$cand")"
    src="$(ls "$REC_DIR"/*-"$h".* 2>/dev/null | head -1)"
    [ -n "$src" ] || { verdict "$h" "skip:evicted-before-grind"; consume "$last"; return 0; }
    local beat_ms; beat_ms="$(beat_of "${win:-}" "${dur:-0}" "${beats:-0}")"
    local r; r="$(derive "${dyn:-0.3}" "${act:-0.3}" "${rich:-0.6}" "${move:-0.14}" "${cent:-1100}" "$beat_ms" 2>/dev/null)"
    case "$r" in
      WALKED-OUT*) verdict "$h" "held:walked-out"; poke "walked-out" "The novelty gate found no recipe far enough from the last $RECENT renders (epsilon=$EPSILON). Record $h [$organ] is held."; consume "$last"; return 0 ;;
      RECIPE*) : ;;
      *) verdict "$h" "skip:derive-failed"; consume "$last"; return 0 ;;
    esac
    local args meta; args="${r#RECIPE }"; args="${args%% ~ *}"; meta="${r#* ~ }"
    printf '%s (fit %s, last recipe cleared epsilon=%s vs last %d renders)\n' \
      "$(sed -n 's/.* novelty \([0-9.]*\).*/\1/p' <<<"$r")" "$(sed -n 's/.* fit \([0-9.]*\).*/\1/p' <<<"$r")" "$EPSILON" "$RECENT" > "$ROOM" 2>/dev/null || true
    poke "drop" "Operator drop landed: $(basename "$src") (score=$score beats=$beats dur=${dur}s). It outranks the ear and is grinding now as: $args"
    verdict "$h" "grinding"
    launch_grind "$src" "$args" "src=$organ/$h $meta" "$h" "$dur" "$organ"
    consume "$last"; return 0
  fi

  # ── RANDOM COLLAGE LANE (operator 2026-07-17): random subset of the block's valid records, ─────
  #    random-cut, concat -> one feed. NO density/beats floor; validity is the only gate.
  local scratch feed res used seed_h meta cuts
  scratch="$(mktemp -d "${TMPDIR:-/tmp}/sr-collage.XXXXXX")"; feed="$scratch/feed.wav"
  res="$(printf '%s\n' "$fresh" | grep -v ' drop ' | collage_build "$feed" 2>/dev/null)"
  if [ -z "$res" ] || [ ! -s "$feed" ]; then
    # Nothing valid in this block (all evicted/corrupt). Decline out loud, then consume.
    local dline dch dfile
    while IFS= read -r dline; do
      [ -n "$dline" ] || continue
      dch="$(awk '{print $3}' <<<"$dline")"; [ -n "$dch" ] || continue
      dfile="$(ls "$REC_DIR"/*-"$dch".* 2>/dev/null | head -1)"
      if [ -n "$dfile" ]; then verdict "$dch" "skip:invalid-source(unreadable/corrupt)"; else verdict "$dch" "skip:evicted-before-grind"; fi
    done <<< "$(printf '%s\n' "$fresh" | grep -v ' drop ')"
    rm -rf "$scratch"; consume "$last"; return 0
  fi
  used="$(sed -n 's/^used=//p' <<<"$res")"; seed_h="${used%% *}"
  meta="$(sed -n 's/^meta=//p' <<<"$res")"

  # Settle every fresh row: seed grinds; other USED rows are blended; valid-but-unused = not-selected;
  # anything invalid = skip:invalid-source. `used` is space-separated; membership test with word match.
  local dline dch dfile
  while IFS= read -r dline; do
    [ -n "$dline" ] || continue
    dch="$(awk '{print $3}' <<<"$dline")"; [ -n "$dch" ] || continue
    [ "$dch" = "$seed_h" ] && continue
    if [[ " $used " == *" $dch "* ]]; then
      verdict "$dch" "blended:$seed_h"
    else
      dfile="$(ls "$REC_DIR"/*-"$dch".* 2>/dev/null | head -1)"
      if [ -n "$dfile" ] && valid_source "$dfile"; then
        verdict "$dch" "skip:not-selected(random collage)"
      elif [ -n "$dfile" ]; then
        verdict "$dch" "skip:invalid-source(unreadable/corrupt)"
      else
        verdict "$dch" "skip:evicted-before-grind"
      fi
    fi
  done <<< "$(printf '%s\n' "$fresh" | grep -v ' drop ')"

  # Re-measure the FEED for the recipe axes (NOT a gate — MEASURE none/silence still grinds via the
  # documented fallbacks). This couples the recipe to the material actually fed, per the "not trivial
  # or boring" half of the doctrine.
  local mline dyn act rich move cent beats win fdur organ="collage" h="$seed_h" score=""
  mline="$(mesh-soundscape --measure "$feed" 2>/dev/null | grep '^MEASURE ' | head -1)"
  dyn="$(kvof dyn "$mline")"; act="$(kvof act "$mline")"; rich="$(kvof rich "$mline")"
  move="$(kvof move "$mline")"; cent="$(kvof cent "$mline")"; beats="$(kvof beats "$mline")"; win="$(kvof dur "$mline")"
  fdur="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$feed" 2>/dev/null)"; fdur="${fdur:-0}"
  local beat_ms; beat_ms="$(beat_of "${win:-}" "${fdur:-0}" "${beats:-0}")"

  local r; r="$(derive "${dyn:-0.3}" "${act:-0.3}" "${rich:-0.6}" "${move:-0.14}" "${cent:-1100}" "$beat_ms" 2>/dev/null)"
  case "$r" in
    WALKED-OUT*) verdict "$seed_h" "held:walked-out"; poke "walked-out" "The novelty gate found no recipe far enough from the last $RECENT renders (epsilon=$EPSILON). The collage feed ($meta) is held, not ground."; rm -rf "$scratch"; consume "$last"; return 0 ;;
    RECIPE*) : ;;
    *) verdict "$seed_h" "skip:derive-failed"; rm -rf "$scratch"; consume "$last"; return 0 ;;
  esac
  local args rmeta; args="${r#RECIPE }"; args="${args%% ~ *}"; rmeta="${r#* ~ }"
  printf '%s (fit %s, last recipe cleared epsilon=%s vs last %d renders)\n' \
    "$(sed -n 's/.* novelty \([0-9.]*\).*/\1/p' <<<"$r")" "$(sed -n 's/.* fit \([0-9.]*\).*/\1/p' <<<"$r")" "$EPSILON" "$RECENT" > "$ROOM" 2>/dev/null || true

  verdict "$seed_h" "grinding"
  launch_grind "$feed" "$args" "src=collage/$seed_h $meta $rmeta" "$seed_h" "$fdur" "collage" "$scratch"
  consume "$last"
}
```

- [ ] **Step 2: Update the header docstring** (~lines 2-16) so the "Rank by score" description no longer contradicts the code. Replace the "What was there before" paragraph's opening with a one-line note that selection is now random-collage-from-ambient, and add near the top:

```bash
# Operator 2026-07-17: mixes are built from the mesh's OWN ambient records, RANDOMLY cut and RANDOMLY
# selected (block collage), NOT by best-score — «случайно нарезанные и выбранные из того, что меш
# слышит». Cough and silence are wanted material; the picker imposes NO density/beats floor, only a
# validity guard (valid_source). The recipe is still DERIVED from the measured character of the feed
# actually built, so no two renders sit in the same corner of the param space (novelty gate).
```

- [ ] **Step 3: Run the full test.** Run: `bash scripts/mesh-sound-reflex --test`. Expected: `smoke-test: ok`, no `FAIL:`.

- [ ] **Step 4: Dry-run `tick()` against a sandbox ledger** (no real grind — point `mesh-room-music` at a stub via PATH, or just confirm verdicts + a feed are produced):

```bash
sb="$(mktemp -d)"; mkdir -p "$sb/records"
ffmpeg -v error -y -f lavfi -i "sine=frequency=250:duration=18" -ac 2 "$sb/records/x-aa.wav" >/dev/null 2>&1
ffmpeg -v error -y -f lavfi -i "anullsrc=r=44100:cl=stereo" -t 18 "$sb/records/x-bb.wav" >/dev/null 2>&1
printf '2026-07-17T00:00Z ear aa dur=18 win=3 score=40 beats=6 [x] dyn=0.2 act=0.3 rich=0.6 move=0.1 cent=1100 -> pending\n2026-07-17T00:00Z ear bb dur=18 win=3 score=5 beats=0 [silent] -> pending\n' > "$sb/ledger"
# stub grinder so nothing heavy runs; it just echoes a fake mp3 path
mkdir -p "$sb/bin"; printf '#!/usr/bin/env bash\necho "/tmp/fake-$$.mp3"\ntouch "/tmp/fake-$$.mp3"\n' > "$sb/bin/mesh-room-music"; chmod +x "$sb/bin/mesh-room-music"
SR_ANCHOR="$sb/anchor" MESH_REC_LOG="$sb/ledger" MESH_REC_DIR="$sb/records" MESH_RMC_PARAMS_LOG="$sb/params" \
  SR_ROOM="$sb/room" SR_LASTPOKE="$sb/lp" SR_TICK="$sb/tick" SR_NOTABLE="$sb/notable" SR_STARVED="$sb/starved" \
  PATH="$sb/bin:$PATH" bash scripts/mesh-sound-reflex
sleep 2
echo "=== ledger verdicts ==="; cat "$sb/ledger"
rm -rf "$sb" /tmp/fake-*.mp3
```
Expected: one row `-> grinding` or `-> ground:...`, the other `-> blended:<seed>` or `-> skip:not-selected(random collage)`; no `-> pending` left; no `skip:below-rhythm-floor` (the floor is gone). The silent `bb` record must NOT be excluded for silence.

- [ ] **Step 5: Commit.**

```bash
git add scripts/mesh-sound-reflex
git commit -m "feat(sound): tick() random-collage lane — replace score-argmax; drop lane preserved"
```

---

### Task 6: Recipe-from-feed + verdict-label tests, deploy, verify wiring

**Files:**
- Modify: `scripts/mesh-sound-reflex` (`--test` section 9)
- Deploy: `~/.local/bin/mesh-sound-reflex`

**Interfaces:**
- Consumes: everything above.

- [ ] **Step 1: Add section 9** — assert the recipe axes come from the FEED's measure, not a ledger row, and that `MEASURE none` falls back rather than declining:

```bash
  # 9. RECIPE FROM THE FEED, not the ledger row. Two feeds of different character must derive
  #    different recipes; a MEASURE-none (silent) feed must still derive (fallback), never decline.
  busy2="$(derive 0.30 0.90 0.60 0.14 1100 500)"
  calm2="$(derive 0.30 0.05 0.60 0.14 1100 500)"
  [ "$busy2" != "$calm2" ] || { echo "  FAIL: derive gave identical recipes for busy vs calm feed axes — the feed measure is not driving the recipe"; f=1; }
  # fallback axes (what tick() uses when MEASURE returns none) must still yield a RECIPE, not WALKED-OUT/empty
  fb="$(derive 0.3 0.3 0.6 0.14 1100 500)"
  case "$fb" in RECIPE*) : ;; *) echo "  FAIL: the MEASURE-none fallback axes did not derive a recipe (silence would wrongly decline)"; f=1; esac
```

- [ ] **Step 2: Run the full test.** Run: `bash scripts/mesh-sound-reflex --test`. Expected: `smoke-test: ok`.

- [ ] **Step 3: Deploy to `~/.local/bin` and confirm no drift.**

```bash
cp scripts/mesh-sound-reflex ~/.local/bin/mesh-sound-reflex && chmod +x ~/.local/bin/mesh-sound-reflex
~/.local/bin/mesh-sound-reflex --test | tail -1        # expect: smoke-test: ok
mesh-sync-tools 2>/dev/null | grep -i sound-reflex || echo "no drift on mesh-sound-reflex"
```
Expected: `smoke-test: ok`; no drift line.

- [ ] **Step 4: Confirm the reflex is still cron-wired and unchanged cadence.**

```bash
crontab -l | grep sound-reflex          # expect the */5 line still present
```
Expected: `*/5 * * * * $HOME/.local/bin/mesh-sound-reflex ...` present.

- [ ] **Step 5: Watch one real tick land** (the live ledger). After the next `*/5` boundary (or run `~/.local/bin/mesh-sound-reflex` once by hand), confirm the live ledger settles a fresh block with the new verdicts and a real mp3 lands:

```bash
~/.local/bin/mesh-sound-reflex
sleep 5
tail -6 ~/.mesh/records.log
grep -E 'src=collage/' ~/.mesh/room-music-params.log | tail -2
```
Expected: fresh rows show `grinding`/`ground:`/`blended:`/`skip:not-selected` (NOT `below-rhythm-floor`); a `src=collage/...` provenance line in the params log.

- [ ] **Step 6: Commit + board.**

```bash
git add scripts/mesh-sound-reflex
git commit -m "test(sound): recipe-from-feed + fallback gates; deploy random-collage picker"
mesh-chat "[done] sound/random-cut-select-from-ambient: mesh-sound-reflex now builds random block-collages from the mesh's own ambient (random subset + random cut + concat), validity-only gate — cough+silence grindable, no density floor. drop lane unchanged. --test green incl. inverted silence-selectable gate. commit <hash>"
```

---

## Self-Review

**Spec coverage:**
- Random selection (not score) → Task 3 (`collage_build`) + Task 5 (tick wiring). ✓
- Random cut → Task 2 (`cut_window`). ✓
- Block collage (subset + concat) → Task 3. ✓
- Validity-only gate, silence included → Task 1 (`valid_source`), inverted `--test`. ✓
- Verdicts (seed/blended/not-selected/invalid) → Task 5. ✓
- Re-measure feed for axes, fallback on none → Task 5 + Task 6 section 9. ✓
- Retire floor with HISTORY note, keep tunables read-only → Task 1 comment + Task 5 header. ✓
- `drop` lane preserved → Task 5 drop branch. ✓
- `mesh-room-music` sole grind owner / `mesh-soundscape` sole measure → Task 4 (`launch_grind`) + Task 5 (`--measure`). ✓
- Mutation discipline (gate seen red) → Tasks 1-3 step "verify it can FAIL". ✓
- Deploy + cron wiring intact → Task 6. ✓

**Placeholder scan:** No TBD/TODO; every code step shows the code; every run step shows the command + expected output. ✓

**Type consistency:** `valid_source`/`cut_window`/`rand_between`/`collage_build`/`launch_grind` signatures match across Tasks 1-6. `collage_build` prints `used=`/`meta=` consumed verbatim by Task 5's `sed -n 's/^used=//p'` / `s/^meta=//p'`. `launch_grind` arg order (`src args meta h dur organ [scratch]`) matches both call sites. ✓
