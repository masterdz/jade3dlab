/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/AIinterp/Sources/Functions/AIfunctions_ai.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 2
 * Unique Functions Mapped: 2
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x004A3490 - 0x004A3534 (Size: 164 bytes)
 * Assertion line 84: AI_gi_FunctionStackLevel == 0 | Message: The function [AIExecute] cannot be use inside a function
 * --------------------------------------------------------------------------- */
void sub_004A3490(void)
{
    /* Line 84 */ ERR_X_Error(AI_gi_FunctionStackLevel == 0, "The function [AIExecute] cannot be use inside a function", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   4a3490: a1 98 3b ac 00               	movl	11287448, %eax
     *   4a3495: 83 ec 38                     	subl	$56, %esp
     *   4a3498: 85 c0                        	testl	%eax, %eax
     *   4a349a: 74 1f                        	je	0x4a34bb <.text+0xa24bb>
     *   4a349c: 6a 01                        	pushl	$1
     *   4a349e: 6a 00                        	pushl	$0
     *   4a34a0: 68 00 0d 7b 00               	pushl	$8064256                # imm = 0x7B0D00
     *   4a34a5: 68 18 0c 7b 00               	pushl	$8064024                # imm = 0x7B0C18
     *   4a34aa: 6a 54                        	pushl	$84
     *   4a34ac: 68 c8 0c 7b 00               	pushl	$8064200                # imm = 0x7B0CC8
     *   4a34b1: 6a 00                        	pushl	$0
     *   4a34b3: e8 18 d0 f7 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4a34b8: 83 c4 1c                     	addl	$28, %esp
     *   4a34bb: a1 50 3b ac 00               	movl	11287376, %eax
     *   4a34c0: 66 8b 0c c5 38 b4 aa 00      	movw	11187256(,%eax,8), %cx
     *   4a34c8: 48                           	decl	%eax
     *   4a34c9: 8d 14 24                     	leal	(%esp), %edx
     *   4a34cc: a3 50 3b ac 00               	movl	%eax, 11287376
     *   4a34d1: 8b 04 c5 44 b4 aa 00         	movl	11187268(,%eax,8), %eax
     *   4a34d8: 52                           	pushl	%edx
     *   4a34d9: 0f bf c9                     	movswl	%cx, %ecx
     *   4a34dc: 50                           	pushl	%eax
     *   4a34dd: ff 14 cd 3c b9 7f 00         	calll	*8370492(,%ecx,8)
     *   4a34e4: 8b 15 4c 3b ac 00            	movl	11287372, %edx
     *   4a34ea: 8b 44 24 08                  	movl	8(%esp), %eax
     *   4a34ee: 83 ea 20                     	subl	$32, %edx
     *   4a34f1: 50                           	pushl	%eax
     *   4a34f2: 89 15 4c 3b ac 00            	movl	%edx, 11287372
     *   4a34f8: e8 43 fc ff ff               	calll	0x4a3140 <.text+0xa2140>
     *   4a34fd: 83 c4 0c                     	addl	$12, %esp
     *   4a3500: 83 f8 07                     	cmpl	$7, %eax
     *   4a3503: 73 24                        	jae	0x4a3529 <.text+0xa2529>
     *   4a3505: 83 f8 01                     	cmpl	$1, %eax
     *   4a3508: 75 04                        	jne	0x4a350e <.text+0xa250e>
     *   4a350a: 83 c4 38                     	addl	$56, %esp
     *   4a350d: c3                           	retl
     *   4a350e: 83 f8 03                     	cmpl	$3, %eax
     *   4a3511: 75 04                        	jne	0x4a3517 <.text+0xa2517>
     *   4a3513: 83 c4 38                     	addl	$56, %esp
     *   4a3516: c3                           	retl
     *   4a3517: 83 f8 04                     	cmpl	$4, %eax
     *   4a351a: 75 04                        	jne	0x4a3520 <.text+0xa2520>
     *   4a351c: 83 c4 38                     	addl	$56, %esp
     *   4a351f: c3                           	retl
     *   4a3520: 83 f8 05                     	cmpl	$5, %eax
     *   4a3523: 75 04                        	jne	0x4a3529 <.text+0xa2529>
     *   4a3525: 83 c4 38                     	addl	$56, %esp
     *   4a3528: c3                           	retl
     *   4a3529: 8b 44 24 3c                  	movl	60(%esp), %eax
     *   4a352d: 83 c0 08                     	addl	$8, %eax
     *   4a3530: 83 c4 38                     	addl	$56, %esp
     *   4a3533: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x004A39B0 - 0x004A3A35 (Size: 133 bytes)
 * Assertion line 338: AI_gi_FunctionStackLevel == 0 | Message: The function [AITrackCurChangeNow] cannot be use inside a function
 * --------------------------------------------------------------------------- */
void sub_004A39B0(void)
{
    /* Line 338 */ ERR_X_Error(AI_gi_FunctionStackLevel == 0, "The function [AITrackCurChangeNow] cannot be use inside a function", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   4a39b0: a1 98 3b ac 00               	movl	11287448, %eax
     *   4a39b5: 83 ec 38                     	subl	$56, %esp
     *   4a39b8: 85 c0                        	testl	%eax, %eax
     *   4a39ba: 74 22                        	je	0x4a39de <.text+0xa29de>
     *   4a39bc: 6a 01                        	pushl	$1
     *   4a39be: 6a 00                        	pushl	$0
     *   4a39c0: 68 40 0d 7b 00               	pushl	$8064320                # imm = 0x7B0D40
     *   4a39c5: 68 18 0c 7b 00               	pushl	$8064024                # imm = 0x7B0C18
     *   4a39ca: 68 52 01 00 00               	pushl	$338                    # imm = 0x152
     *   4a39cf: 68 c8 0c 7b 00               	pushl	$8064200                # imm = 0x7B0CC8
     *   4a39d4: 6a 00                        	pushl	$0
     *   4a39d6: e8 f5 ca f7 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4a39db: 83 c4 1c                     	addl	$28, %esp
     *   4a39de: a1 50 3b ac 00               	movl	11287376, %eax
     *   4a39e3: 66 8b 0c c5 38 b4 aa 00      	movw	11187256(,%eax,8), %cx
     *   4a39eb: 48                           	decl	%eax
     *   4a39ec: 8d 14 24                     	leal	(%esp), %edx
     *   4a39ef: a3 50 3b ac 00               	movl	%eax, 11287376
     *   4a39f4: 8b 04 c5 44 b4 aa 00         	movl	11187268(,%eax,8), %eax
     *   4a39fb: 52                           	pushl	%edx
     *   4a39fc: 0f bf c9                     	movswl	%cx, %ecx
     *   4a39ff: 50                           	pushl	%eax
     *   4a3a00: ff 14 cd 3c b9 7f 00         	calll	*8370492(,%ecx,8)
     *   4a3a07: 8b 15 4c 3b ac 00            	movl	11287372, %edx
     *   4a3a0d: 8b 44 24 08                  	movl	8(%esp), %eax
     *   4a3a11: 83 ea 20                     	subl	$32, %edx
     *   4a3a14: 50                           	pushl	%eax
     *   4a3a15: 89 15 4c 3b ac 00            	movl	%edx, 11287372
     *   4a3a1b: e8 30 f8 ff ff               	calll	0x4a3250 <.text+0xa2250>
     *   4a3a20: 83 c4 0c                     	addl	$12, %esp
     *   4a3a23: 3d e8 03 00 00               	cmpl	$1000, %eax             # imm = 0x3E8
     *   4a3a28: 75 07                        	jne	0x4a3a31 <.text+0xa2a31>
     *   4a3a2a: 8b 44 24 3c                  	movl	60(%esp), %eax
     *   4a3a2e: 83 c0 08                     	addl	$8, %eax
     *   4a3a31: 83 c4 38                     	addl	$56, %esp
     *   4a3a34: c3                           	retl
     */
}
