/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/ENGine/Sources/COLlision/COLcob.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x006CB6F0 - 0x006CB8AD (Size: 445 bytes)
 * Assertion line 459: Sorry, Max number of Cobs reached | Message: None
 * --------------------------------------------------------------------------- */
void COL_fn_vAddCob(void)
{
    /* Line 459 */ ERR_X_Error(Sorry, Max number of Cobs reached, "Unknown error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   6cb6f0: 55                           	pushl	%ebp
     *   6cb6f1: 8b 6c 24 08                  	movl	8(%esp), %ebp
     *   6cb6f5: 8b 45 18                     	movl	24(%ebp), %eax
     *   6cb6f8: 8b 08                        	movl	(%eax), %ecx
     *   6cb6fa: 57                           	pushl	%edi
     *   6cb6fb: 8b 79 08                     	movl	8(%ecx), %edi
     *   6cb6fe: 8a 07                        	movb	(%edi), %al
     *   6cb700: 3c 08                        	cmpb	$8, %al
     *   6cb702: 75 22                        	jne	0x6cb726 <_SND_fn_vDisplayError@8+0x55596>
     *   6cb704: 6a 01                        	pushl	$1
     *   6cb706: 6a 00                        	pushl	$0
     *   6cb708: 68 4c 90 7b 00               	pushl	$8097868                # imm = 0x7B904C
     *   6cb70d: 6a 00                        	pushl	$0
     *   6cb70f: 68 cb 01 00 00               	pushl	$459                    # imm = 0x1CB
     *   6cb714: 68 1c 90 7b 00               	pushl	$8097820                # imm = 0x7B901C
     *   6cb719: 6a 00                        	pushl	$0
     *   6cb71b: e8 b0 4d d5 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   6cb720: 83 c4 1c                     	addl	$28, %esp
     *   6cb723: 5f                           	popl	%edi
     *   6cb724: 5d                           	popl	%ebp
     *   6cb725: c3                           	retl
     *   6cb726: 84 c0                        	testb	%al, %al
     *   6cb728: a1 c0 53 ae 00               	movl	11424704, %eax
     *   6cb72d: 56                           	pushl	%esi
     *   6cb72e: 75 42                        	jne	0x6cb772 <_SND_fn_vDisplayError@8+0x555e2>
     *   6cb730: 85 c0                        	testl	%eax, %eax
     *   6cb732: 75 0a                        	jne	0x6cb73e <_SND_fn_vDisplayError@8+0x555ae>
     *   6cb734: 6a 02                        	pushl	$2
     *   6cb736: e8 95 ea f8 ff               	calll	0x65a1d0 <_SND_fn_vSynchroTimer@0+0x16ef00>
     *   6cb73b: 83 c4 04                     	addl	$4, %esp
     *   6cb73e: 6a 04                        	pushl	$4
     *   6cb740: 8b c8                        	movl	%eax, %ecx
     *   6cb742: e8 f9 50 d5 ff               	calll	0x420840 <.text+0x1f840>
     *   6cb747: 89 47 04                     	movl	%eax, 4(%edi)
     *   6cb74a: a1 c0 53 ae 00               	movl	11424704, %eax
     *   6cb74f: 85 c0                        	testl	%eax, %eax
     *   6cb751: 75 0a                        	jne	0x6cb75d <_SND_fn_vDisplayError@8+0x555cd>
     *   6cb753: 6a 02                        	pushl	$2
     *   6cb755: e8 76 ea f8 ff               	calll	0x65a1d0 <_SND_fn_vSynchroTimer@0+0x16ef00>
     *   6cb75a: 83 c4 04                     	addl	$4, %esp
     *   6cb75d: 6a 10                        	pushl	$16
     *   6cb75f: 8b c8                        	movl	%eax, %ecx
     *   6cb761: e8 da 50 d5 ff               	calll	0x420840 <.text+0x1f840>
     *   6cb766: 8b 57 04                     	movl	4(%edi), %edx
     *   6cb769: 89 02                        	movl	%eax, (%edx)
     *   6cb76b: 8b 47 04                     	movl	4(%edi), %eax
     *   6cb76e: 8b 30                        	movl	(%eax), %esi
     *   6cb770: eb 55                        	jmp	0x6cb7c7 <_SND_fn_vDisplayError@8+0x55637>
     *   6cb772: 85 c0                        	testl	%eax, %eax
     *   6cb774: 75 0a                        	jne	0x6cb780 <_SND_fn_vDisplayError@8+0x555f0>
     *   6cb776: 6a 02                        	pushl	$2
     *   6cb778: e8 53 ea f8 ff               	calll	0x65a1d0 <_SND_fn_vSynchroTimer@0+0x16ef00>
     *   6cb77d: 83 c4 04                     	addl	$4, %esp
     *   6cb780: 0f b6 0f                     	movzbl	(%edi), %ecx
     * ... (110 more instructions)
     */
}
