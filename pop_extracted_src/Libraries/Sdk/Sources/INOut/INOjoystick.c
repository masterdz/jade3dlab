/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/Sdk/Sources/INOut/INOjoystick.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x00425000 - 0x00425057 (Size: 87 bytes)
 * Assertion line 2635: Unable to initialize the input manager | Message: None
 * --------------------------------------------------------------------------- */
void INO_fn_vInitJoystick(void)
{
    /* Line 2635 */ ERR_X_Error(Unable to initialize the input manager, "Unknown error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   425000: 8b 44 24 04                  	movl	4(%esp), %eax
     *   425004: 50                           	pushl	%eax
     *   425005: b9 c0 42 81 00               	movl	$8471232, %ecx          # imm = 0x8142C0
     *   42500a: e8 41 fd ff ff               	calll	0x424d50 <.text+0x23d50>
     *   42500f: 84 c0                        	testb	%al, %al
     *   425011: b9 c0 42 81 00               	movl	$8471232, %ecx          # imm = 0x8142C0
     *   425016: 75 2f                        	jne	0x425047 <.text+0x24047>
     *   425018: e8 13 f6 ff ff               	calll	0x424630 <.text+0x23630>
     *   42501d: 68 e8 03 00 00               	pushl	$1000                   # imm = 0x3E8
     *   425022: e8 d9 60 ff ff               	calll	0x41b100 <.text+0x1a100>
     *   425027: 6a 01                        	pushl	$1
     *   425029: 6a 00                        	pushl	$0
     *   42502b: 68 a0 f1 7a 00               	pushl	$8057248                # imm = 0x7AF1A0
     *   425030: 6a 00                        	pushl	$0
     *   425032: 68 4b 0a 00 00               	pushl	$2635                   # imm = 0xA4B
     *   425037: 68 74 f1 7a 00               	pushl	$8057204                # imm = 0x7AF174
     *   42503c: 6a 00                        	pushl	$0
     *   42503e: e8 8d b4 ff ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   425043: 83 c4 20                     	addl	$32, %esp
     *   425046: c3                           	retl
     *   425047: e8 e4 e3 ff ff               	calll	0x423430 <.text+0x22430>
     *   42504c: c7 05 08 87 7f 00 ff ff ff ff	movl	$4294967295, 8357640    # imm = 0xFFFFFFFF
     *   425056: c3                           	retl
     */
}
