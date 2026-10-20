/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/AIinterp/Sources/Functions/AIfunctions_msg.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x00464190 - 0x004642DC (Size: 332 bytes)
 * Assertion line 315: The function AI_EvalFunc_MSGSendAllOwner doesn't have a C implemantation. | Message: None
 * --------------------------------------------------------------------------- */
void sub_00464190(void)
{
    /* Line 315 */ ERR_X_Error(The function AI_EvalFunc_MSGSendAllOwner doesn't have a C implemantation., "Unknown error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   464190: 83 ec 34                     	subl	$52, %esp
     *   464193: 8b 0d 70 3b ac 00            	movl	11287408, %ecx
     *   464199: 8b 15 68 3b ac 00            	movl	11287400, %edx
     *   46419f: 33 c0                        	xorl	%eax, %eax
     *   4641a1: 56                           	pushl	%esi
     *   4641a2: 8b 35 74 3b ac 00            	movl	11287412, %esi
     *   4641a8: 89 0d 74 3b ac 00            	movl	%ecx, 11287412
     *   4641ae: 8b 0d 90 46 a8 00            	movl	11028112, %ecx
     *   4641b4: 3b c8                        	cmpl	%eax, %ecx
     *   4641b6: 89 44 24 04                  	movl	%eax, 4(%esp)
     *   4641ba: 89 44 24 08                  	movl	%eax, 8(%esp)
     *   4641be: 89 44 24 20                  	movl	%eax, 32(%esp)
     *   4641c2: 89 44 24 1c                  	movl	%eax, 28(%esp)
     *   4641c6: 89 44 24 18                  	movl	%eax, 24(%esp)
     *   4641ca: 89 44 24 14                  	movl	%eax, 20(%esp)
     *   4641ce: 89 44 24 10                  	movl	%eax, 16(%esp)
     *   4641d2: 89 44 24 0c                  	movl	%eax, 12(%esp)
     *   4641d6: 89 44 24 24                  	movl	%eax, 36(%esp)
     *   4641da: 89 44 24 28                  	movl	%eax, 40(%esp)
     *   4641de: 89 44 24 2c                  	movl	%eax, 44(%esp)
     *   4641e2: 89 44 24 30                  	movl	%eax, 48(%esp)
     *   4641e6: 89 44 24 34                  	movl	%eax, 52(%esp)
     *   4641ea: 89 15 6c 3b ac 00            	movl	%edx, 11287404
     *   4641f0: 0f 84 da 00 00 00            	je	0x4642d0 <.text+0x632d0>
     *   4641f6: 8b 49 18                     	movl	24(%ecx), %ecx
     *   4641f9: 3b c8                        	cmpl	%eax, %ecx
     *   4641fb: 0f 84 cf 00 00 00            	je	0x4642d0 <.text+0x632d0>
     *   464201: 39 41 14                     	cmpl	%eax, 20(%ecx)
     *   464204: 0f 84 c6 00 00 00            	je	0x4642d0 <.text+0x632d0>
     *   46420a: 6a 01                        	pushl	$1
     *   46420c: 50                           	pushl	%eax
     *   46420d: 68 40 03 7b 00               	pushl	$8061760                # imm = 0x7B0340
     *   464212: 50                           	pushl	%eax
     *   464213: 68 3b 01 00 00               	pushl	$315                    # imm = 0x13B
     *   464218: 68 08 03 7b 00               	pushl	$8061704                # imm = 0x7B0308
     *   46421d: 50                           	pushl	%eax
     *   46421e: e8 ad c2 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   464223: e8 58 f9 ff ff               	calll	0x463b80 <.text+0x62b80>
     *   464228: 89 44 24 4c                  	movl	%eax, 76(%esp)
     *   46422c: e8 4f f9 ff ff               	calll	0x463b80 <.text+0x62b80>
     *   464231: 89 44 24 48                  	movl	%eax, 72(%esp)
     *   464235: e8 96 f9 ff ff               	calll	0x463bd0 <.text+0x62bd0>
     *   46423a: d9 5c 24 44                  	fstps	68(%esp)
     *   46423e: e8 8d f9 ff ff               	calll	0x463bd0 <.text+0x62bd0>
     *   464243: d9 5c 24 40                  	fstps	64(%esp)
     *   464247: a1 4c 3b ac 00               	movl	11287372, %eax
     *   46424c: 8b 88 20 b5 ab 00            	movl	11253024(%eax), %ecx
     *   464252: 8b 90 24 b5 ab 00            	movl	11253028(%eax), %edx
     *   464258: 83 e8 20                     	subl	$32, %eax
     *   46425b: 89 4c 24 34                  	movl	%ecx, 52(%esp)
     *   46425f: 8b 88 48 b5 ab 00            	movl	11253064(%eax), %ecx
     *   464265: 83 e8 20                     	subl	$32, %eax
     *   464268: 89 4c 24 3c                  	movl	%ecx, 60(%esp)
     *   46426c: 8b 88 44 b5 ab 00            	movl	11253060(%eax), %ecx
     * ... (27 more instructions)
     */
}
