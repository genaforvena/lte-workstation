# Varvara has no audio input device — and what that costs a granular mixer

**Question (board task `INPUT`, 2026-08-21):** the operator wants a RECORD button in a uxn
build of grainneukeln. Does Varvara have an audio **input** device at all, or is the audio
device output-only?

**Answer: output-only. There is no audio input device anywhere in Varvara.** The RECORD
branch is dead as specified. What is *not* dead is playback, and there is a real
alternative — see "If he still wants the button" at the end.

Everything below is measured, not recalled. Sources: the spec page fetched
2026-08-21, and the reference C at upstream `43453d7` — the same commit `scripts/uxn/src/`
is vendored from, so this is our own emulator's ancestor, not a different project.

---

## 1. The device map has 16 pages and none of them is an input

From `wiki.xxiivv.com/site/varvara.html`, verbatim: "Each device has 16 bytes of
addressable memory in the device page, which are called ports."

| page | device | page | device |
|------|--------|------|--------|
| `00` | system | `80` | controller |
| `10` | console | `90` | mouse |
| `20` | screen | `a0` | file |
| `30` | **audio0** | `b0` | — |
| `40` | **audio1** | `c0` | datetime |
| `50` | **audio2** | `d0` | reserved |
| `60` | **audio3** | `e0` | — |
| `70` | — | `f0` | — |

`30`–`60` are **four playback voices**, not an in/out pair. There is no capture page, and
the two reserved pages are explicitly "implementation specific features that do not need to
be part of the specs" — i.e. anything you put there is not Varvara.

## 2. The audio device's readable surface is 3 bytes out of 16, and all 3 describe *your own* note

```
|30 @Audio0/vector $2 &position $2 &output $1 &pad $3 &adsr $2 &length $2 &addr $2 &volume $1 &pitch $1
```

- `position*` (`32`) — the playhead's offset into **the buffer you supplied**.
- `output` (`34`) — the envelope loudness (VU) of **the note you started**.
- `vector*` (`30`) — your own callback address, fired when a note ends.

Ports `35 36 37` are `--` in the spec: unused padding. Everything else is write-only
config. There is no read port, no length-of-captured-data, no buffer-full vector. Compare
the devices that *do* bring bytes in — `Console/read` (`12`), `File/read` (`ad`) — the
audio device has no member of that family.

**Measured, not read off the table.** `audio-in-probe.tal` writes the sentinel `a5` to all
16 ports and reads them back on a build with the real device linked:

```
ports 30..3f readback: a5 a5 01 0f 11 a5 a5 a5 a5 a5 a5 a5 a5 a5 a5 a5
                             ^^^^^ ^^
                             position*  output
```

Exactly three bytes are computed by the device. Thirteen echoed our own write. That
enumeration *is* the finding, and `test-audio-input` asserts precisely that shape.

## 3. `addr*` is read **by** the device and never written — proven three ways

The whole reference device is 125 lines (`src/devices/audio.c` @ `43453d7`) and contains
exactly **one** reference to uxn memory:

```c
c->addr = &uxn.ram[addr];                                    /* line 84 — a read handle */
s = (Sint8)(c->addr[c->i] + 0x80) * envelope(c, c->age++);   /* line 66 — dereferenced to READ */
*sample++ += s * c->volume[0] / 0x180;                       /* output goes to SDL's buffer */
```

There is no write into `uxn.ram` in the device at all. And the emulator opens the host
device for playback only — `src/uxnemu.c:250`:

```c
audio_id = SDL_OpenAudioDevice(NULL, 0, &as, NULL, 0);
/*                                   ^ iscapture = 0 */
```

That `0` is SDL's `iscapture` argument. There is no capture handle anywhere in the
emulator. `audio.h`'s entire public API — `audio_get_vu`, `audio_get_position`,
`audio_render`, `audio_start`, `audio_finished_handler` — has no capture entry point.

Third proof, runtime: `audio-in-probe.tal` arm 3 zeroes a 16-byte buffer, points `addr*` at
it, starts a note, and checksums the buffer afterwards. Unchanged, on a build where the
device demonstrably rendered nonzero samples from it.

## 4. Our own `bin/uxncli` has no audio device at all — in *or* out

`emu-sources` lists system, console, file, datetime, net. `emu_dei` has no `0x30`–`0x60`
case, so it falls through to `return uxn.dev[addr]`: **every audio port read returns the
ROM's own last write.** A naive "read the mic port" would get back a plausible non-zero
byte that is nothing but its own echo — the silent-fallback shape, exactly.

`uxn11`, the current reference emulator, is also audio-blind: its `dei_handlers[256]` table
has entries only at `04 05 15 16 28 2a 2c c0 c2..ca`, nothing in `30`–`6f`. The spec page
says so outright — "an emulator which includes everything but the audio device". Only the
SDL2 `uxnemu` implements audio, and only outbound.

So on this node, **even playback would have to be built first.**

## 5. Artifacts

| file | what it is |
|------|-----------|
| `audio-in-probe.tal` / `.rom` | the probe: sentinel readback, device identification, RAM-write test. 724 B |
| `audio-probe-emu.c` | throwaway audio-wired uxncli, links the real reference device so the PRESENT branch is not dead code |
| `src/devices/audio.{c,h}` | vendored at `43453d7`, **deliberately not in `EMU_SRC`** |
| `test-audio-input` | the gate, both arms |

Run: `./test-audio-input` → `ok (absent arm rc=2, present arm rc=0, addr* proven read-only)`.

```
$ ./bin/uxncli audio-in-probe.rom          # no audio device
device: ABSENT -- every port echoed our own write
arm3 (does the device write uxn RAM?): n/a on this build
verdict: NO AUDIO INPUT DEVICE IN VARVARA          rc=2   (honest n/a, not a pass)

$ ./uxncli-audio audio-in-probe.rom        # real reference device linked
device: PRESENT (34 is computed, not echo)
arm3: buffer UNCHANGED after a note -- addr* is read-only
harness: output-buffer NONZERO (device really rendered)   rc=0
```

**Seen red.** Three mutants, all caught: (1) make the device write `c->addr[c->i] = 0x42`
→ arm 3 and the C checksum both fail; (2) add `audio.c` to `EMU_SRC` → the invariant check
fires, because that would delete the ABSENT arm and leave the suite testing one thing
twice; (3) force `advance = 0` so nothing renders → the vacuity guard fires in both the ROM
and the harness.

That vacuity guard earned its place by first being **wrong**: it originally asserted
`position* != 0`, which called a perfectly live note dead — a 16-byte looping sample wraps
the playhead to exactly `i % 16 == 0` after 1024 frames. The predicate now reads `output`
(the VU), which is nonzero exactly while one of our notes is live.

---

## 6. The memory ceiling, honestly, against a granular mixer

Constants are from source, not memory: `PAGE_SIZE 0x10000` (`src/uxn.h`), `BANKS 0x10`
(`src/devices/system.h`), `POLYPHONY 4` and `SAMPLE_FREQUENCY 44100` (`audio.h`).

**The binding constraint is not memory — it is four voices.**

`POLYPHONY 4`. Varvara gives you exactly four simultaneous notes, compile-time fixed, one
per device page. Granular synthesis is defined by overlapping grains — grainneukeln's own
recipes run grain densities where dozens sound at once. On Varvara you get **four**. You
can retrigger fast (the audio vector fires when a note ends), so you can *sequence* many
grains; you cannot *overlap* more than four. Every other number below is roomier than this
one.

**Then: 64 KiB, and samples cannot live outside it.**

`Audio/addr*` is a bare 16-bit pointer with no bank field, and the device clamps to the end
of the address space:

```c
Uint16 addr = PEEK2(d + 0xc);
if(c->len > 0x10000 - addr) c->len = 0x10000 - addr;   /* hard clamp to bank 0 */
```

So *playable* sample data must sit in bank 0 alongside the program. Budget:

| | bytes |
|---|---|
| bank 0, total | 65 536 |
| usable (program starts at `0x0100`) | 65 280 |
| minus a ~4 KiB mixer ROM | ~61 184 |

Duration depends on pitch, because pitch *is* the resample ratio
(`rate = 44100 × advance / 0x10000`; pitch 60 is unity). Samples are **unsigned 8-bit
mono** — the spec is explicit — so one byte is one sample:

| pitch | playback rate | seconds in ~60 KiB |
|------:|--------------:|-------------------:|
| 60 | 44 100 Hz | **1.39** |
| 48 | 22 050 Hz | 2.79 |
| 36 | 11 025 Hz | 5.57 |
| 24 | 5 512 Hz | 11.15 |
| 12 | 2 756 Hz | 22.29 |

**The banks are cold storage, not more sample memory.** `BANKS 0x10` → 1 MiB total, of
which 64 KiB is addressable and **983 040 B is reachable only by block-copy** through
`System/expansion` (`fill`/`cpyl`/`cpyr`), and the spec notes "operations do not cross bank
boundaries". A grain corpus can live there, but every grain must be copied into bank 0
before any voice can play it. That is a workable design — a 1 MiB corpus, four voices, and
a copy per grain — but it is not a bigger playback window.

**Scale against what grainneukeln actually chews on today:** one 35-second ethnic clip is
6 174 078 B. That single clip is **94× the entire directly-addressable uxn memory** and
**5.9× the whole 1 MiB banked space**. The corpus directory is 698 MB — 665× the banked
total. A uxn granular mixer is not a port of grainneukeln; it is a different, much smaller
instrument that happens to share the technique.

---

## 7. If he still wants the button

The honest options, in order of how much they cost:

1. **Record outside uxn, play inside it.** The `file` device (`a0`/`b0`) reads arbitrary
   bytes off disk into RAM. Something else on the node captures (the mesh already has
   `mesh-overhear`, `mesh-room-gigaam`, the room ear), writes 8-bit mono into a file, and
   the ROM loads it via `File/read`. The RECORD button then triggers a capture *outside*
   the ROM. This needs no spec extension and works on `bin/uxncli` today — the file device
   is already in `EMU_SRC`.
2. **Record over the net device.** `d0` is ours (`src/devices/net.c`, already in the
   build). A ROM can pull sample bytes from a socket, which is the same shape as option 1
   without touching the filesystem.
3. **Write a capture device on one of the two reserved pages.** `d0`/`e0` exist for exactly
   this. But note what it costs: a ROM using it is **no longer portable Varvara** — it runs
   on our emulator and nothing else, and `emu-sources`' whole reason for existing is that
   the platforms must not disagree about what the emulator IS.

Options 1 and 2 keep the ROM portable. Option 3 does not. Nothing makes the *spec* grow an
input device.
