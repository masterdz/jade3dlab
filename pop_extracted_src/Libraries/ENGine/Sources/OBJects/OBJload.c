/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/ENGine/Sources/OBJects/OBJload.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x00684970 - 0x00685E26 (Size: 5302 bytes)
 * Assertion line 850: ulGaoVersion <= 10 | Message: The gao file format is newer than supported by this version of the editor
 * --------------------------------------------------------------------------- */
void OBJ_ul_LoadGAO(void)
{
    /* Line 850 */ ERR_X_Error(ulGaoVersion <= 10, "The gao file format is newer than supported by this version of the editor", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   684970: 83 ec 5c                     	subl	$92, %esp
     *   684973: 8b 4c 24 60                  	movl	96(%esp), %ecx
     *   684977: 6a 01                        	pushl	$1
     *   684979: 8d 44 24 18                  	leal	24(%esp), %eax
     *   68497d: 50                           	pushl	%eax
     *   68497e: 51                           	pushl	%ecx
     *   68497f: e8 cc 3b da ff               	calll	0x428550 <.text+0x27550>
     *   684984: 6a 01                        	pushl	$1
     *   684986: 6a 04                        	pushl	$4
     *   684988: 8d 54 24 18                  	leal	24(%esp), %edx
     *   68498c: 89 44 24 14                  	movl	%eax, 20(%esp)
     *   684990: 52                           	pushl	%edx
     *   684991: 8d 44 24 18                  	leal	24(%esp), %eax
     *   684995: 50                           	pushl	%eax
     *   684996: e8 95 52 da ff               	calll	0x429c30 <.text+0x28c30>
     *   68499b: 6a 04                        	pushl	$4
     *   68499d: 8d 4c 24 24                  	leal	36(%esp), %ecx
     *   6849a1: 68 9c 8a 7b 00               	pushl	$8096412                # imm = 0x7B8A9C
     *   6849a6: 51                           	pushl	%ecx
     *   6849a7: e8 44 b7 0a 00               	calll	0x7300f0 <_SND_fn_bInitMallocSnd@0+0x7b00>
     *   6849ac: 83 c4 28                     	addl	$40, %esp
     *   6849af: 85 c0                        	testl	%eax, %eax
     *   6849b1: 74 06                        	je	0x6849b9 <_SND_fn_vDisplayError@8+0xe829>
     *   6849b3: 33 c0                        	xorl	%eax, %eax
     *   6849b5: 83 c4 5c                     	addl	$92, %esp
     *   6849b8: c3                           	retl
     *   6849b9: 8b 04 24                     	movl	(%esp), %eax
     *   6849bc: 53                           	pushl	%ebx
     *   6849bd: 55                           	pushl	%ebp
     *   6849be: 57                           	pushl	%edi
     *   6849bf: 8b 38                        	movl	(%eax), %edi
     *   6849c1: 83 c0 04                     	addl	$4, %eax
     *   6849c4: 89 44 24 0c                  	movl	%eax, 12(%esp)
     *   6849c8: a1 28 2a 9e 00               	movl	10365480, %eax
     *   6849cd: 33 db                        	xorl	%ebx, %ebx
     *   6849cf: 3b c3                        	cmpl	%ebx, %eax
     *   6849d1: 89 7c 24 18                  	movl	%edi, 24(%esp)
     *   6849d5: 74 2b                        	je	0x684a02 <_SND_fn_vDisplayError@8+0xe872>
     *   6849d7: 8a 44 24 18                  	movb	24(%esp), %al
     *   6849db: 8b d7                        	movl	%edi, %edx
     *   6849dd: c1 ea 18                     	shrl	$24, %edx
     *   6849e0: 88 44 24 1b                  	movb	%al, 27(%esp)
     *   6849e4: 88 54 24 18                  	movb	%dl, 24(%esp)
     *   6849e8: 8b 44 24 18                  	movl	24(%esp), %eax
     *   6849ec: 8b 4c 24 18                  	movl	24(%esp), %ecx
     *   6849f0: c1 e8 08                     	shrl	$8, %eax
     *   6849f3: c1 e9 10                     	shrl	$16, %ecx
     *   6849f6: 88 4c 24 19                  	movb	%cl, 25(%esp)
     *   6849fa: 88 44 24 1a                  	movb	%al, 26(%esp)
     *   6849fe: 8b 7c 24 18                  	movl	24(%esp), %edi
     *   684a02: 83 ff 0a                     	cmpl	$10, %edi
     *   684a05: 76 20                        	jbe	0x684a27 <_SND_fn_vDisplayError@8+0xe897>
     *   684a07: 6a 01                        	pushl	$1
     *   684a09: 53                           	pushl	%ebx
     * ... (1574 more instructions)
     */
}
