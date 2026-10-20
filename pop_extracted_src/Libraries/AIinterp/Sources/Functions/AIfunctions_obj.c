/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/AIinterp/Sources/Functions/AIfunctions_obj.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x0047A240 - 0x0047A2A5 (Size: 101 bytes)
 * Assertion line 344: AI_gi_FunctionStackLevel == 0 || pst_GO != AI_gpst_CurrentGameObject | Message: The function [OBJ_Destroy] cannot be use inside a function
 * --------------------------------------------------------------------------- */
void sub_0047A240(void)
{
    /* Line 344 */ ERR_X_Error(AI_gi_FunctionStackLevel == 0 || pst_GO != AI_gpst_CurrentGameObject, "The function [OBJ_Destroy] cannot be use inside a function", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   47a240: 8b 0d 68 3b ac 00            	movl	11287400, %ecx
     *   47a246: a1 70 3b ac 00               	movl	11287408, %eax
     *   47a24b: 89 0d 6c 3b ac 00            	movl	%ecx, 11287404
     *   47a251: 8b 0d 98 3b ac 00            	movl	11287448, %ecx
     *   47a257: 85 c9                        	testl	%ecx, %ecx
     *   47a259: 56                           	pushl	%esi
     *   47a25a: 8b 35 74 3b ac 00            	movl	11287412, %esi
     *   47a260: a3 74 3b ac 00               	movl	%eax, 11287412
     *   47a265: 74 26                        	je	0x47a28d <.text+0x7928d>
     *   47a267: 3b f0                        	cmpl	%eax, %esi
     *   47a269: 75 22                        	jne	0x47a28d <.text+0x7928d>
     *   47a26b: 6a 01                        	pushl	$1
     *   47a26d: 6a 00                        	pushl	$0
     *   47a26f: 68 d0 0a 7b 00               	pushl	$8063696                # imm = 0x7B0AD0
     *   47a274: 68 88 0a 7b 00               	pushl	$8063624                # imm = 0x7B0A88
     *   47a279: 68 58 01 00 00               	pushl	$344                    # imm = 0x158
     *   47a27e: 68 4c 0a 7b 00               	pushl	$8063564                # imm = 0x7B0A4C
     *   47a283: 6a 00                        	pushl	$0
     *   47a285: e8 46 62 fa ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   47a28a: 83 c4 1c                     	addl	$28, %esp
     *   47a28d: 56                           	pushl	%esi
     *   47a28e: e8 3d fe ff ff               	calll	0x47a0d0 <.text+0x790d0>
     *   47a293: 83 c4 04                     	addl	$4, %esp
     *   47a296: 83 f8 06                     	cmpl	$6, %eax
     *   47a299: 5e                           	popl	%esi
     *   47a29a: 75 01                        	jne	0x47a29d <.text+0x7929d>
     *   47a29c: c3                           	retl
     *   47a29d: 8b 44 24 04                  	movl	4(%esp), %eax
     *   47a2a1: 83 c0 08                     	addl	$8, %eax
     *   47a2a4: c3                           	retl
     */
}
