/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/AIinterp/Sources/AIengine.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 3
 * Unique Functions Mapped: 2
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x00468E80 - 0x004690A7 (Size: 551 bytes)
 * Assertion line 2074: pst_SrcInst->pc_VarsBufferInit | Message: Invalid Instance Variable buffer
 * --------------------------------------------------------------------------- */
void sub_00468E80(void)
{
    /* Line 2074 */ ERR_X_Error(pst_SrcInst->pc_VarsBufferInit, "Invalid Instance Variable buffer", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   468e80: 8b 44 24 04                  	movl	4(%esp), %eax
     *   468e84: 8b 40 18                     	movl	24(%eax), %eax
     *   468e87: 85 c0                        	testl	%eax, %eax
     *   468e89: 0f 84 17 02 00 00            	je	0x4690a6 <.text+0x680a6>
     *   468e8f: 53                           	pushl	%ebx
     *   468e90: 8b 58 04                     	movl	4(%eax), %ebx
     *   468e93: 85 db                        	testl	%ebx, %ebx
     *   468e95: 89 5c 24 08                  	movl	%ebx, 8(%esp)
     *   468e99: 0f 84 06 02 00 00            	je	0x4690a5 <.text+0x680a5>
     *   468e9f: a1 c0 53 ae 00               	movl	11424704, %eax
     *   468ea4: 85 c0                        	testl	%eax, %eax
     *   468ea6: 75 0a                        	jne	0x468eb2 <.text+0x67eb2>
     *   468ea8: 6a 02                        	pushl	$2
     *   468eaa: e8 21 13 1f 00               	calll	0x65a1d0 <_SND_fn_vSynchroTimer@0+0x16ef00>
     *   468eaf: 83 c4 04                     	addl	$4, %esp
     *   468eb2: 55                           	pushl	%ebp
     *   468eb3: 56                           	pushl	%esi
     *   468eb4: 57                           	pushl	%edi
     *   468eb5: 6a 58                        	pushl	$88
     *   468eb7: 8b c8                        	movl	%eax, %ecx
     *   468eb9: e8 82 79 fb ff               	calll	0x420840 <.text+0x1f840>
     *   468ebe: 8b e8                        	movl	%eax, %ebp
     *   468ec0: b9 16 00 00 00               	movl	$22, %ecx
     *   468ec5: 8b f3                        	movl	%ebx, %esi
     *   468ec7: 8b fd                        	movl	%ebp, %edi
     *   468ec9: f3 a5                        	rep		movsl	(%esi), %es:(%edi)
     *   468ecb: 8b 4c 24 18                  	movl	24(%esp), %ecx
     *   468ecf: 33 f6                        	xorl	%esi, %esi
     *   468ed1: 89 75 48                     	movl	%esi, 72(%ebp)
     *   468ed4: 89 75 4c                     	movl	%esi, 76(%ebp)
     *   468ed7: 8b 51 18                     	movl	24(%ecx), %edx
     *   468eda: 89 6a 04                     	movl	%ebp, 4(%edx)
     *   468edd: 8b 45 00                     	movl	(%ebp), %eax
     *   468ee0: 8b 08                        	movl	(%eax), %ecx
     *   468ee2: 39 71 04                     	cmpl	%esi, 4(%ecx)
     *   468ee5: 0f 84 8d 00 00 00            	je	0x468f78 <.text+0x67f78>
     *   468eeb: a1 c0 53 ae 00               	movl	11424704, %eax
     *   468ef0: 3b c6                        	cmpl	%esi, %eax
     *   468ef2: 75 0a                        	jne	0x468efe <.text+0x67efe>
     *   468ef4: 6a 02                        	pushl	$2
     *   468ef6: e8 d5 12 1f 00               	calll	0x65a1d0 <_SND_fn_vSynchroTimer@0+0x16ef00>
     *   468efb: 83 c4 04                     	addl	$4, %esp
     *   468efe: 8b 55 00                     	movl	(%ebp), %edx
     *   468f01: 8b 0a                        	movl	(%edx), %ecx
     *   468f03: 8b 51 04                     	movl	4(%ecx), %edx
     *   468f06: 52                           	pushl	%edx
     *   468f07: 8b c8                        	movl	%eax, %ecx
     *   468f09: e8 32 79 fb ff               	calll	0x420840 <.text+0x1f840>
     *   468f0e: 89 45 44                     	movl	%eax, 68(%ebp)
     *   468f11: a1 c0 53 ae 00               	movl	11424704, %eax
     *   468f16: 3b c6                        	cmpl	%esi, %eax
     *   468f18: 75 0a                        	jne	0x468f24 <.text+0x67f24>
     *   468f1a: 6a 02                        	pushl	$2
     *   468f1c: e8 af 12 1f 00               	calll	0x65a1d0 <_SND_fn_vSynchroTimer@0+0x16ef00>
     * ... (138 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00469560 - 0x004696C7 (Size: 359 bytes)
 * Assertion line 792: AI_gpst_DynAINodeStack[iIdx][i] | Message: CRASH Expected
 * Assertion line 797: AI_gpast_DynAIFunctionTT[AI_gpst_DynAINodeStack[iIdx][i]->w_Param] | Message: Unknown function ID Ref
 * --------------------------------------------------------------------------- */
void sub_00469560(void)
{
    /* Line 792 */ ERR_X_Error(AI_gpst_DynAINodeStack[iIdx][i], "CRASH Expected", NULL);
    /* Line 797 */ ERR_X_Error(AI_gpast_DynAIFunctionTT[AI_gpst_DynAINodeStack[iIdx][i]->w_Param], "Unknown function ID Ref", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   469560: 53                           	pushl	%ebx
     *   469561: 55                           	pushl	%ebp
     *   469562: 56                           	pushl	%esi
     *   469563: 57                           	pushl	%edi
     *   469564: 33 db                        	xorl	%ebx, %ebx
     *   469566: eb 08                        	jmp	0x469570 <.text+0x68570>
     *   469568: 8d a4 24 00 00 00 00         	leal	(%esp), %esp
     *   46956f: 90                           	nop
     *   469570: 8b 04 9d 34 4a a8 00         	movl	11029044(,%ebx,4), %eax
     *   469577: 33 ff                        	xorl	%edi, %edi
     *   469579: 85 c0                        	testl	%eax, %eax
     *   46957b: 0f 8e fe 00 00 00            	jle	0x46967f <.text+0x6867f>
     *   469581: 8b f3                        	movl	%ebx, %esi
     *   469583: 69 f6 c0 5d 00 00            	imull	$24000, %esi, %esi      # imm = 0x5DC0
     *   469589: 81 c6 40 4a a8 00            	addl	$11029056, %esi         # imm = 0xA84A40
     *   46958f: 90                           	nop
     *   469590: 8b 06                        	movl	(%esi), %eax
     *   469592: 85 c0                        	testl	%eax, %eax
     *   469594: 75 25                        	jne	0x4695bb <.text+0x685bb>
     *   469596: 0f bf 40 04                  	movswl	4(%eax), %eax
     *   46959a: 6a 01                        	pushl	$1
     *   46959c: 50                           	pushl	%eax
     *   46959d: 68 c4 07 7b 00               	pushl	$8062916                # imm = 0x7B07C4
     *   4695a2: 68 a4 07 7b 00               	pushl	$8062884                # imm = 0x7B07A4
     *   4695a7: 68 18 03 00 00               	pushl	$792                    # imm = 0x318
     *   4695ac: 68 d8 06 7b 00               	pushl	$8062680                # imm = 0x7B06D8
     *   4695b1: 6a 00                        	pushl	$0
     *   4695b3: e8 18 6f fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4695b8: 83 c4 1c                     	addl	$28, %esp
     *   4695bb: 8b 0e                        	movl	(%esi), %ecx
     *   4695bd: 0f bf 41 04                  	movswl	4(%ecx), %eax
     *   4695c1: 8b 2d 84 3b ac 00            	movl	11287428, %ebp
     *   4695c7: 3b c5                        	cmpl	%ebp, %eax
     *   4695c9: 7f 45                        	jg	0x469610 <.text+0x68610>
     *   4695cb: 8b 0c 85 c0 45 a9 00         	movl	11093440(,%eax,4), %ecx
     *   4695d2: 85 c9                        	testl	%ecx, %ecx
     *   4695d4: 75 22                        	jne	0x4695f8 <.text+0x685f8>
     *   4695d6: 6a 01                        	pushl	$1
     *   4695d8: 6a 00                        	pushl	$0
     *   4695da: 68 8c 07 7b 00               	pushl	$8062860                # imm = 0x7B078C
     *   4695df: 68 48 07 7b 00               	pushl	$8062792                # imm = 0x7B0748
     *   4695e4: 68 1d 03 00 00               	pushl	$797                    # imm = 0x31D
     *   4695e9: 68 d8 06 7b 00               	pushl	$8062680                # imm = 0x7B06D8
     *   4695ee: 6a 00                        	pushl	$0
     *   4695f0: e8 db 6e fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4695f5: 83 c4 1c                     	addl	$28, %esp
     *   4695f8: 8b 16                        	movl	(%esi), %edx
     *   4695fa: 0f bf 42 04                  	movswl	4(%edx), %eax
     *   4695fe: 8b 0c 85 c0 45 a9 00         	movl	11093440(,%eax,4), %ecx
     *   469605: 8b 51 04                     	movl	4(%ecx), %edx
     *   469608: 8b 2d 84 3b ac 00            	movl	11287428, %ebp
     *   46960e: eb 02                        	jmp	0x469612 <.text+0x68612>
     *   469610: 8b d0                        	movl	%eax, %edx
     *   469612: 33 c0                        	xorl	%eax, %eax
     * ... (57 more instructions)
     */
}
