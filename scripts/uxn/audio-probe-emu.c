/*
audio-probe-emu.c — an AUDIO-WIRED uxncli, built ONLY by ./test-audio-input.

Why it exists: audio-in-probe.tal has two branches (device PRESENT / device ABSENT) and
bin/uxncli can only ever reach the ABSENT one, because EMU_SRC deliberately omits the audio
device. A branch nothing has been seen to take is not a branch — so this harness links the
REAL vendored reference device (src/devices/audio.c at upstream 43453d7, the same commit the
rest of src/ comes from) and drives the ROM down the PRESENT arm.

It is NOT an emulator anyone should ship: SDL owns the audio callback upstream, so here the
render is called synchronously right after a note starts, purely so the probe can ask the
question that matters — does rendering a note ever write back into uxn RAM?

The answer is asserted twice over: once in C (ram checksum across the render) and once by the
ROM itself (arm 3). Both must agree.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "uxn.h"
#include "devices/system.h"
#include "devices/console.h"
#include "devices/file.h"
#include "devices/datetime.h"
#include "devices/net.h"
#include "devices/audio.h"

Uxn uxn;
int console_vector;

static Sint16 render_buf[4096];
static int rendered_samples = 0;
static unsigned long ram_sum_before = 0, ram_sum_after = 0;

void
audio_finished_handler(int instance)
{
	(void)instance;
}

static unsigned long
ram_checksum(void)
{
	unsigned long s = 0;
	int i;
	for(i = 0; i < PAGE_SIZE; i++) s = s * 31 + uxn.ram[i];
	return s;
}

/* lifted verbatim from uxnemu.c's audio_dei, minus the SDL audio_id guard: here the
   device is unconditionally present, which is the whole point of this build. */
static Uint8
audio_dei(int instance, Uint8 *d, Uint8 port)
{
	switch(port) {
	case 0x4: return audio_get_vu(instance);
	case 0x2: POKE2(d + 0x2, audio_get_position(instance)); /* fall through */
	default: return d[port];
	}
}

static void
audio_deo(int instance, Uint8 *d, Uint8 port)
{
	if(port == 0xf) {
		audio_start(instance, d);
		/* SDL drives this from another thread upstream; drive it here so the ROM's
		   arm 3 is asked AFTER real samples have actually been produced. */
		ram_sum_before = ram_checksum();
		rendered_samples += audio_render(instance, render_buf, render_buf + 2048);
		ram_sum_after = ram_checksum();
	}
}

Uint8
emu_dei(Uint8 addr)
{
	switch(addr & 0xf0) {
	case 0x00: return system_dei(addr);
	case 0x30: return audio_dei(0, &uxn.dev[0x30], addr & 0x0f);
	case 0x40: return audio_dei(1, &uxn.dev[0x40], addr & 0x0f);
	case 0x50: return audio_dei(2, &uxn.dev[0x50], addr & 0x0f);
	case 0x60: return audio_dei(3, &uxn.dev[0x60], addr & 0x0f);
	case 0xc0: return datetime_dei(addr);
	case 0xd0: return net_dei(addr);
	}
	return uxn.dev[addr];
}

void
emu_deo(Uint8 addr, Uint8 value)
{
	uxn.dev[addr] = value;
	switch(addr & 0xf0) {
	case 0x00: system_deo(addr); break;
	case 0x10: console_deo(addr); break;
	case 0x30: audio_deo(0, &uxn.dev[0x30], addr & 0x0f); break;
	case 0x40: audio_deo(1, &uxn.dev[0x40], addr & 0x0f); break;
	case 0x50: audio_deo(2, &uxn.dev[0x50], addr & 0x0f); break;
	case 0x60: audio_deo(3, &uxn.dev[0x60], addr & 0x0f); break;
	case 0xa0: file_deo(addr); break;
	case 0xb0: file_deo(addr); break;
	case 0xd0: net_deo(addr); break;
	}
}

int
main(int argc, char **argv)
{
	int rc;
	if(argc < 2) return !fprintf(stdout, "usage: %s file.rom\n", argv[0]);
	if(!system_boot((Uint8 *)calloc(PAGE_SIZE * BANKS, sizeof(Uint8)), argv[1], 0))
		return !fprintf(stdout, "Could not load %s.\n", argv[1]);
	rc = uxn.dev[0x0f] & 0x7f;
	fprintf(stderr, "harness: rendered=%d samples ram-before=%lu ram-after=%lu %s\n",
		rendered_samples, ram_sum_before, ram_sum_after,
		ram_sum_before == ram_sum_after ? "RAM-UNCHANGED" : "RAM-CHANGED");
	{	/* "audio_render returned" is not "audio came out". Only a nonzero output
		   buffer proves the device really read our RAM and produced samples, and
		   without that proof arm 3's UNCHANGED is a fact about silence. */
		int i, nonzero = 0;
		for(i = 0; i < 4096; i++)
			if(render_buf[i]) { nonzero = 1; break; }
		fprintf(stderr, "harness: output-buffer %s\n", nonzero ? "NONZERO (device really rendered)" : "ALL-ZERO — arm 3 asked nothing");
		if(!nonzero) rc = rc ? rc : 1;
	}
	return rc;
}
