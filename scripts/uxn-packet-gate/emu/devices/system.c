#include <stdio.h>

#include "../uxn.h"
#include "system.h"

/*
Copyright (c) 2022-2025 Devine Lu Linvega, Andrew Alderwick

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE.
*/

char *boot_path;

static void
system_print(char *name, Stack *s)
{
	Uint8 i;
	fprintf(stderr, "%s ", name);
	for(i = s->ptr - 8; i != (Uint8)(s->ptr); i++)
		fprintf(stderr, "%02x%c", s->dat[i], i == 0xff ? '|' : ' ');
	fprintf(stderr, "<%02x\n", s->ptr);
}

static int
system_load(Uint8 *ram, char *rom_path)
{
	FILE *f = fopen(rom_path, "rb");
	if(f) {
		int i = 0, l = fread(ram, PAGE_SIZE - PAGE_PROGRAM, 1, f);
		while(l && ++i < BANKS)
			l = fread(ram + PAGE_SIZE * i - PAGE_PROGRAM, PAGE_SIZE, 1, f);
		fclose(f);
	}
	return !!f;
}

int
system_error(char *msg, const char *err)
{
	fprintf(stderr, "%s: %s\n", msg, err), fflush(stderr);
	return 0;
}

int
system_boot(Uint8 *ram, char *rom_path, int has_args)
{
	uxn.ram = ram;
	boot_path = rom_path;
	uxn.dev[0x17] = has_args;
	if(ram && system_load(uxn.ram + PAGE_PROGRAM, rom_path))
		return uxn_eval(PAGE_PROGRAM);
	return 0;
}

int
system_reboot(int soft)
{
	int i;
	for(i = 0x0; i < 0x100; i++) uxn.dev[i] = 0;
	for(i = soft ? 0x100 : 0; i < PAGE_SIZE; i++) uxn.ram[i] = 0;
	uxn.wst.ptr = uxn.rst.ptr = 0;
	return system_boot(uxn.ram, boot_path, 0);
}

static void
system_expansion(const Uint16 exp)
{
	Uint8 *aptr = uxn.ram + exp;
	unsigned short length = PEEK2(aptr + 1), limit;
	unsigned int bank = PEEK2(aptr + 3) * 0x10000;
	unsigned int addr = PEEK2(aptr + 5);
	if(uxn.ram[exp] == 0x0) {
		unsigned int dst_value = uxn.ram[exp + 7];
		unsigned short a = addr;
		if(bank < BANKS_CAP)
			for(limit = a + length; a != limit; a++)
				uxn.ram[bank + a] = dst_value;
	} else if(uxn.ram[exp] == 0x1) {
		unsigned int dst_bank = PEEK2(aptr + 7) * 0x10000;
		unsigned int dst_addr = PEEK2(aptr + 9);
		unsigned short a = addr, c = dst_addr;
		if(bank < BANKS_CAP && dst_bank < BANKS_CAP)
			for(limit = a + length; a != limit; c++, a++)
				uxn.ram[dst_bank + c] = uxn.ram[bank + a];
	} else if(uxn.ram[exp] == 0x2) {
		unsigned int dst_bank = PEEK2(aptr + 7) * 0x10000;
		unsigned int dst_addr = PEEK2(aptr + 9);
		unsigned short a = addr + length - 1, c = dst_addr + length - 1;
		if(bank < BANKS_CAP && dst_bank < BANKS_CAP)
			for(limit = addr - 1; a != limit; a--, c--)
				uxn.ram[dst_bank + c] = uxn.ram[bank + a];
	} else
		fprintf(stderr, "Unknown command: %s\n", &uxn.ram[exp]);
}

/* IO */

Uint8
system_dei(Uint8 addr)
{
	switch(addr) {
	case 0x4: return uxn.wst.ptr;
	case 0x5: return uxn.rst.ptr;
	default: return uxn.dev[addr];
	}
}

void
system_deo(Uint8 port)
{
	switch(port) {
	case 0x3: {
		system_expansion(PEEK2(uxn.dev + 2));
		break;
	}
	case 0x4:
		uxn.wst.ptr = uxn.dev[4];
		break;
	case 0x5:
		uxn.rst.ptr = uxn.dev[5];
		break;
	case 0xe:
		system_print("WST", &uxn.wst);
		system_print("RST", &uxn.rst);
		break;
	}
}
