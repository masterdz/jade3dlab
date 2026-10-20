/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/AIinterp/Sources/Keywords/AIkeywords.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x004A4540 - 0x004A458B (Size: 75 bytes)
 * Assertion line 124: AI_gi_FunctionStackLevel == 0 | Message: The function [ReturnTrack] cannot be use inside a function
 * --------------------------------------------------------------------------- */
void sub_004A4540(void)
{
    /* Line 124 */ ERR_X_Error(AI_gi_FunctionStackLevel == 0, "The function [ReturnTrack] cannot be use inside a function", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   4a4540: a1 98 3b ac 00               	movl	11287448, %eax
     *   4a4545: 85 c0                        	testl	%eax, %eax
     *   4a4547: 74 30                        	je	0x4a4579 <.text+0xa3579>
     *   4a4549: 6a 01                        	pushl	$1
     *   4a454b: 6a 00                        	pushl	$0
     *   4a454d: 68 b8 0d 7b 00               	pushl	$8064440                # imm = 0x7B0DB8
     *   4a4552: 68 18 0c 7b 00               	pushl	$8064024                # imm = 0x7B0C18
     *   4a4557: 6a 7c                        	pushl	$124
     *   4a4559: 68 84 0d 7b 00               	pushl	$8064388                # imm = 0x7B0D84
     *   4a455e: 6a 00                        	pushl	$0
     *   4a4560: e8 6b bf f7 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4a4565: a1 64 3b ac 00               	movl	11287396, %eax
     *   4a456a: c7 00 00 00 00 00            	movl	$0, (%eax)
     *   4a4570: 83 c4 1c                     	addl	$28, %esp
     *   4a4573: b8 04 00 00 00               	movl	$4, %eax
     *   4a4578: c3                           	retl
     *   4a4579: 8b 0d 64 3b ac 00            	movl	11287396, %ecx
     *   4a457f: c7 01 00 00 00 00            	movl	$0, (%ecx)
     *   4a4585: b8 04 00 00 00               	movl	$4, %eax
     *   4a458a: c3                           	retl
     */
}
