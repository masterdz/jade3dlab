/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/ENGine/Sources/WORld/WORDynLoad.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x0067FED0 - 0x006800ED (Size: 541 bytes)
 * Assertion line 206: Invalid key (%08X) found WOR_ExpandWorldList | Message: None
 * --------------------------------------------------------------------------- */
void WOR_ExpandWorldList(void)
{
    /* Line 206 */ ERR_X_Error(Invalid key (%08X) found WOR_ExpandWorldList, "Unknown error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   67fed0: 55                           	pushl	%ebp
     *   67fed1: 8b ec                        	movl	%esp, %ebp
     *   67fed3: 83 e4 f8                     	andl	$-8, %esp
     *   67fed6: 83 ec 2c                     	subl	$44, %esp
     *   67fed9: 53                           	pushl	%ebx
     *   67feda: 56                           	pushl	%esi
     *   67fedb: 57                           	pushl	%edi
     *   67fedc: 8d 44 24 20                  	leal	32(%esp), %eax
     *   67fee0: 50                           	pushl	%eax
     *   67fee1: 8d 4c 24 30                  	leal	48(%esp), %ecx
     *   67fee5: e8 b6 f9 ff ff               	calll	0x67f8a0 <_SND_fn_vDisplayError@8+0x9710>
     *   67feea: 8b 0d 30 59 81 00            	movl	8476976, %ecx
     *   67fef0: 83 cf ff                     	orl	$-1, %edi
     *   67fef3: 33 c0                        	xorl	%eax, %eax
     *   67fef5: 85 c9                        	testl	%ecx, %ecx
     *   67fef7: 89 7c 24 10                  	movl	%edi, 16(%esp)
     *   67fefb: 89 7c 24 1c                  	movl	%edi, 28(%esp)
     *   67feff: 74 09                        	je	0x67ff0a <_SND_fn_vDisplayError@8+0x9d7a>
     *   67ff01: 83 3d f4 29 9e 00 02         	cmpl	$2, 10365428
     *   67ff08: 74 14                        	je	0x67ff1e <_SND_fn_vDisplayError@8+0x9d8e>
     *   67ff0a: 8b 75 08                     	movl	8(%ebp), %esi
     *   67ff0d: 56                           	pushl	%esi
     *   67ff0e: e8 2d 88 da ff               	calll	0x428740 <.text+0x27740>
     *   67ff13: 83 c4 04                     	addl	$4, %esp
     *   67ff16: 3b c7                        	cmpl	%edi, %eax
     *   67ff18: 0f 84 91 01 00 00            	je	0x6800af <_SND_fn_vDisplayError@8+0x9f1f>
     *   67ff1e: 6a 01                        	pushl	$1
     *   67ff20: 8d 4c 24 24                  	leal	36(%esp), %ecx
     *   67ff24: 51                           	pushl	%ecx
     *   67ff25: 50                           	pushl	%eax
     *   67ff26: e8 25 86 da ff               	calll	0x428550 <.text+0x27550>
     *   67ff2b: 8b d8                        	movl	%eax, %ebx
     *   67ff2d: 8b 44 24 2c                  	movl	44(%esp), %eax
     *   67ff31: c1 e8 03                     	shrl	$3, %eax
     *   67ff34: 83 c4 0c                     	addl	$12, %esp
     *   67ff37: 85 c0                        	testl	%eax, %eax
     *   67ff39: 0f 86 25 01 00 00            	jbe	0x680064 <_SND_fn_vDisplayError@8+0x9ed4>
     *   67ff3f: 8b 3d 28 2a 9e 00            	movl	10365480, %edi
     *   67ff45: 89 44 24 18                  	movl	%eax, 24(%esp)
     *   67ff49: 8d a4 24 00 00 00 00         	leal	(%esp), %esp
     *   67ff50: 8b 33                        	movl	(%ebx), %esi
     *   67ff52: 83 c3 04                     	addl	$4, %ebx
     *   67ff55: 85 ff                        	testl	%edi, %edi
     *   67ff57: 89 74 24 0c                  	movl	%esi, 12(%esp)
     *   67ff5b: 74 2b                        	je	0x67ff88 <_SND_fn_vDisplayError@8+0x9df8>
     *   67ff5d: 8a 44 24 0c                  	movb	12(%esp), %al
     *   67ff61: 8b d6                        	movl	%esi, %edx
     *   67ff63: c1 ea 18                     	shrl	$24, %edx
     *   67ff66: 88 44 24 0f                  	movb	%al, 15(%esp)
     *   67ff6a: 88 54 24 0c                  	movb	%dl, 12(%esp)
     *   67ff6e: 8b 44 24 0c                  	movl	12(%esp), %eax
     *   67ff72: 8b 4c 24 0c                  	movl	12(%esp), %ecx
     *   67ff76: c1 e8 08                     	shrl	$8, %eax
     *   67ff79: c1 e9 10                     	shrl	$16, %ecx
     * ... (120 more instructions)
     */
}
