/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/ENGine/Sources/MoDiFier/MDFmodifier_GEN.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x006E9580 - 0x006E9687 (Size: 263 bytes)
 * Assertion line 1048: 0 | Message: Sound modifier inconsistency detected in your BigFile
 * --------------------------------------------------------------------------- */
void sub_006E9580(void)
{
    /* Line 1048 */ ERR_X_Error(0, "Sound modifier inconsistency detected in your BigFile", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   6e9580: 51                           	pushl	%ecx
     *   6e9581: 56                           	pushl	%esi
     *   6e9582: 8b 74 24 10                  	movl	16(%esp), %esi
     *   6e9586: 89 74 24 04                  	movl	%esi, 4(%esp)
     *   6e958a: e8 11 c9 d3 ff               	calll	0x425ea0 <.text+0x24ea0>
     *   6e958f: 8b 44 24 04                  	movl	4(%esp), %eax
     *   6e9593: 8b 08                        	movl	(%eax), %ecx
     *   6e9595: 89 4c 24 10                  	movl	%ecx, 16(%esp)
     *   6e9599: 8b 0d 28 2a 9e 00            	movl	10365480, %ecx
     *   6e959f: 83 c0 04                     	addl	$4, %eax
     *   6e95a2: 85 c9                        	testl	%ecx, %ecx
     *   6e95a4: 89 44 24 04                  	movl	%eax, 4(%esp)
     *   6e95a8: 74 29                        	je	0x6e95d3 <_SND_fn_vDisplayError@8+0x73443>
     *   6e95aa: 8b 54 24 10                  	movl	16(%esp), %edx
     *   6e95ae: 8a 4c 24 10                  	movb	16(%esp), %cl
     *   6e95b2: c1 ea 18                     	shrl	$24, %edx
     *   6e95b5: 88 54 24 10                  	movb	%dl, 16(%esp)
     *   6e95b9: 88 4c 24 13                  	movb	%cl, 19(%esp)
     *   6e95bd: 8b 4c 24 10                  	movl	16(%esp), %ecx
     *   6e95c1: 8b 54 24 10                  	movl	16(%esp), %edx
     *   6e95c5: c1 e9 08                     	shrl	$8, %ecx
     *   6e95c8: c1 ea 10                     	shrl	$16, %edx
     *   6e95cb: 88 54 24 11                  	movb	%dl, 17(%esp)
     *   6e95cf: 88 4c 24 12                  	movb	%cl, 18(%esp)
     *   6e95d3: 81 7c 24 10 0a 01 00 00      	cmpl	$266, 16(%esp)          # imm = 0x10A
     *   6e95db: 74 2b                        	je	0x6e9608 <_SND_fn_vDisplayError@8+0x73478>
     *   6e95dd: 6a 01                        	pushl	$1
     *   6e95df: 6a 00                        	pushl	$0
     *   6e95e1: 68 34 93 7b 00               	pushl	$8098612                # imm = 0x7B9334
     *   6e95e6: 68 b8 f2 7a 00               	pushl	$8057528                # imm = 0x7AF2B8
     *   6e95eb: 68 18 04 00 00               	pushl	$1048                   # imm = 0x418
     *   6e95f0: 68 fc 92 7b 00               	pushl	$8098556                # imm = 0x7B92FC
     *   6e95f5: 6a 00                        	pushl	$0
     *   6e95f7: e8 d4 6e d3 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   6e95fc: 8b 44 24 20                  	movl	32(%esp), %eax
     *   6e9600: 83 c4 1c                     	addl	$28, %esp
     *   6e9603: 2b c6                        	subl	%esi, %eax
     *   6e9605: 5e                           	popl	%esi
     *   6e9606: 59                           	popl	%ecx
     *   6e9607: c3                           	retl
     *   6e9608: 8b 0d 30 59 81 00            	movl	8476976, %ecx
     *   6e960e: 8b 15 f4 29 9e 00            	movl	10365428, %edx
     *   6e9614: 83 c0 18                     	addl	$24, %eax
     *   6e9617: 85 c9                        	testl	%ecx, %ecx
     *   6e9619: 74 05                        	je	0x6e9620 <_SND_fn_vDisplayError@8+0x73490>
     *   6e961b: 83 fa 02                     	cmpl	$2, %edx
     *   6e961e: 74 03                        	je	0x6e9623 <_SND_fn_vDisplayError@8+0x73493>
     *   6e9620: 83 c0 04                     	addl	$4, %eax
     *   6e9623: 83 c0 10                     	addl	$16, %eax
     *   6e9626: 85 c9                        	testl	%ecx, %ecx
     *   6e9628: 74 05                        	je	0x6e962f <_SND_fn_vDisplayError@8+0x7349f>
     *   6e962a: 83 fa 02                     	cmpl	$2, %edx
     *   6e962d: 74 03                        	je	0x6e9632 <_SND_fn_vDisplayError@8+0x734a2>
     *   6e962f: 83 c0 04                     	addl	$4, %eax
     * ... (32 more instructions)
     */
}
