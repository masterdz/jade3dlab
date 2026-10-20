/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/ENGine/Sources/MoDiFier/MDFstruct.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x00688280 - 0x006882FF (Size: 127 bytes)
 * Assertion line 1084: 0L | Message: Modifier Type is Not Implemented for multiple instance
 * --------------------------------------------------------------------------- */
void sub_00688280(void)
{
    /* Line 1084 */ ERR_X_Error(0L, "Modifier Type is Not Implemented for multiple instance", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   688280: 8b 44 24 04                  	movl	4(%esp), %eax
     *   688284: 8b 40 18                     	movl	24(%eax), %eax
     *   688287: 55                           	pushl	%ebp
     *   688288: 33 ed                        	xorl	%ebp, %ebp
     *   68828a: 85 c0                        	testl	%eax, %eax
     *   68828c: 75 02                        	jne	0x688290 <_SND_fn_vDisplayError@8+0x12100>
     *   68828e: 5d                           	popl	%ebp
     *   68828f: c3                           	retl
     *   688290: 53                           	pushl	%ebx
     *   688291: 56                           	pushl	%esi
     *   688292: 8b 70 1c                     	movl	28(%eax), %esi
     *   688295: 85 f6                        	testl	%esi, %esi
     *   688297: 57                           	pushl	%edi
     *   688298: 74 57                        	je	0x6882f1 <_SND_fn_vDisplayError@8+0x12161>
     *   68829a: 8b 7c 24 20                  	movl	32(%esp), %edi
     *   68829e: 8b 5c 24 18                  	movl	24(%esp), %ebx
     *   6882a2: 8b 0e                        	movl	(%esi), %ecx
     *   6882a4: 8b 01                        	movl	(%ecx), %eax
     *   6882a6: 3b c3                        	cmpl	%ebx, %eax
     *   6882a8: 75 40                        	jne	0x6882ea <_SND_fn_vDisplayError@8+0x1215a>
     *   6882aa: 8b 4c 24 1c                  	movl	28(%esp), %ecx
     *   6882ae: 85 c9                        	testl	%ecx, %ecx
     *   6882b0: 74 07                        	je	0x6882b9 <_SND_fn_vDisplayError@8+0x12129>
     *   6882b2: 3b fd                        	cmpl	%ebp, %edi
     *   6882b4: 74 42                        	je	0x6882f8 <_SND_fn_vDisplayError@8+0x12168>
     *   6882b6: 45                           	incl	%ebp
     *   6882b7: eb 31                        	jmp	0x6882ea <_SND_fn_vDisplayError@8+0x1215a>
     *   6882b9: 83 f8 17                     	cmpl	$23, %eax
     *   6882bc: 74 24                        	je	0x6882e2 <_SND_fn_vDisplayError@8+0x12152>
     *   6882be: 6a 01                        	pushl	$1
     *   6882c0: 6a 00                        	pushl	$0
     *   6882c2: 68 dc 8a 7b 00               	pushl	$8096476                # imm = 0x7B8ADC
     *   6882c7: 68 d8 8a 7b 00               	pushl	$8096472                # imm = 0x7B8AD8
     *   6882cc: 68 3c 04 00 00               	pushl	$1084                   # imm = 0x43C
     *   6882d1: 68 a8 8a 7b 00               	pushl	$8096424                # imm = 0x7B8AA8
     *   6882d6: 6a 00                        	pushl	$0
     *   6882d8: e8 f3 81 d9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   6882dd: 83 c4 1c                     	addl	$28, %esp
     *   6882e0: eb 08                        	jmp	0x6882ea <_SND_fn_vDisplayError@8+0x1215a>
     *   6882e2: 8b 56 08                     	movl	8(%esi), %edx
     *   6882e5: 39 7a 60                     	cmpl	%edi, 96(%edx)
     *   6882e8: 74 0e                        	je	0x6882f8 <_SND_fn_vDisplayError@8+0x12168>
     *   6882ea: 8b 76 0c                     	movl	12(%esi), %esi
     *   6882ed: 85 f6                        	testl	%esi, %esi
     *   6882ef: 75 b1                        	jne	0x6882a2 <_SND_fn_vDisplayError@8+0x12112>
     *   6882f1: 5f                           	popl	%edi
     *   6882f2: 5e                           	popl	%esi
     *   6882f3: 5b                           	popl	%ebx
     *   6882f4: 33 c0                        	xorl	%eax, %eax
     *   6882f6: 5d                           	popl	%ebp
     *   6882f7: c3                           	retl
     *   6882f8: 5f                           	popl	%edi
     *   6882f9: 8b c6                        	movl	%esi, %eax
     *   6882fb: 5e                           	popl	%esi
     * ... (3 more instructions)
     */
}
