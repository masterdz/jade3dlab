/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/ENGine/Sources/Dare/dareinterface.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x0067B560 - 0x0067B5A6 (Size: 70 bytes)
 * Assertion line 1290: 0 | Message: The SoundParam not allocated.
 * --------------------------------------------------------------------------- */
void sub_0067B560(void)
{
    /* Line 1290 */ ERR_X_Error(0, "The SoundParam not allocated.", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   67b560: 8b 44 24 04                  	movl	4(%esp), %eax
     *   67b564: 8b 40 18                     	movl	24(%eax), %eax
     *   67b567: 85 c0                        	testl	%eax, %eax
     *   67b569: 74 3a                        	je	0x67b5a5 <_SND_fn_vDisplayError@8+0x5415>
     *   67b56b: 8b 40 24                     	movl	36(%eax), %eax
     *   67b56e: 85 c0                        	testl	%eax, %eax
     *   67b570: 74 08                        	je	0x67b57a <_SND_fn_vDisplayError@8+0x53ea>
     *   67b572: 8b 4c 24 08                  	movl	8(%esp), %ecx
     *   67b576: 89 48 14                     	movl	%ecx, 20(%eax)
     *   67b579: c3                           	retl
     *   67b57a: 6a 01                        	pushl	$1
     *   67b57c: 6a 00                        	pushl	$0
     *   67b57e: 68 88 87 7b 00               	pushl	$8095624                # imm = 0x7B8788
     *   67b583: e8 58 2a 0a 00               	calll	0x71dfe0 <_SND_fn_ulGetNumberOfSoundEventGroup@0>
     *   67b588: 83 c4 04                     	addl	$4, %esp
     *   67b58b: 50                           	pushl	%eax
     *   67b58c: 68 b8 f2 7a 00               	pushl	$8057528                # imm = 0x7AF2B8
     *   67b591: 68 0a 05 00 00               	pushl	$1290                   # imm = 0x50A
     *   67b596: 68 58 87 7b 00               	pushl	$8095576                # imm = 0x7B8758
     *   67b59b: 6a 00                        	pushl	$0
     *   67b59d: e8 2e 4f da ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   67b5a2: 83 c4 1c                     	addl	$28, %esp
     *   67b5a5: c3                           	retl
     */
}
