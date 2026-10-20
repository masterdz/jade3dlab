/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/Sdk/Sources/BIGfiles/BIGcomp.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 3
 * Unique Functions Mapped: 2
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x0042AD50 - 0x0042AE94 (Size: 324 bytes)
 * Assertion line 301: 0 | Message: Decode error
 * --------------------------------------------------------------------------- */
void BIGcomp_DecodeBlocks(void)
{
    /* Line 301 */ ERR_X_Error(0, "Decode error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   42ad50: a1 24 87 7f 00               	movl	8357668, %eax
     *   42ad55: 83 ec 10                     	subl	$16, %esp
     *   42ad58: 33 c9                        	xorl	%ecx, %ecx
     *   42ad5a: 3b c1                        	cmpl	%ecx, %eax
     *   42ad5c: 56                           	pushl	%esi
     *   42ad5d: 57                           	pushl	%edi
     *   42ad5e: 0f 84 08 01 00 00            	je	0x42ae6c <.text+0x29e6c>
     *   42ad64: 8b 44 24 1c                  	movl	28(%esp), %eax
     *   42ad68: 8b 50 04                     	movl	4(%eax), %edx
     *   42ad6b: 55                           	pushl	%ebp
     *   42ad6c: 8b 28                        	movl	(%eax), %ebp
     *   42ad6e: 89 48 08                     	movl	%ecx, 8(%eax)
     *   42ad71: 39 4c 24 24                  	cmpl	%ecx, 36(%esp)
     *   42ad75: 89 54 24 10                  	movl	%edx, 16(%esp)
     *   42ad79: 89 4c 24 14                  	movl	%ecx, 20(%esp)
     *   42ad7d: 0f 86 e0 00 00 00            	jbe	0x42ae63 <.text+0x29e63>
     *   42ad83: 53                           	pushl	%ebx
     *   42ad84: 0f b6 4d 00                  	movzbl	(%ebp), %ecx
     *   42ad88: 33 db                        	xorl	%ebx, %ebx
     *   42ad8a: 8a 7d 01                     	movb	1(%ebp), %bh
     *   42ad8d: 8d 45 01                     	leal	1(%ebp), %eax
     *   42ad90: 83 c5 04                     	addl	$4, %ebp
     *   42ad93: 0b cb                        	orl	%ebx, %ecx
     *   42ad95: 33 db                        	xorl	%ebx, %ebx
     *   42ad97: 8a 78 02                     	movb	2(%eax), %bh
     *   42ad9a: 40                           	incl	%eax
     *   42ad9b: 8a 18                        	movb	(%eax), %bl
     *   42ad9d: c1 e3 10                     	shll	$16, %ebx
     *   42ada0: 0b d9                        	orl	%ecx, %ebx
     *   42ada2: 8b f3                        	movl	%ebx, %esi
     *   42ada4: 85 f6                        	testl	%esi, %esi
     *   42ada6: 89 74 24 10                  	movl	%esi, 16(%esp)
     *   42adaa: 0f 84 b2 00 00 00            	je	0x42ae62 <.text+0x29e62>
     *   42adb0: 0f b6 4d 00                  	movzbl	(%ebp), %ecx
     *   42adb4: 33 db                        	xorl	%ebx, %ebx
     *   42adb6: 8a 7d 01                     	movb	1(%ebp), %bh
     *   42adb9: 8d 45 01                     	leal	1(%ebp), %eax
     *   42adbc: 83 c5 04                     	addl	$4, %ebp
     *   42adbf: 0b cb                        	orl	%ebx, %ecx
     *   42adc1: 33 db                        	xorl	%ebx, %ebx
     *   42adc3: 8a 78 02                     	movb	2(%eax), %bh
     *   42adc6: 40                           	incl	%eax
     *   42adc7: 8a 18                        	movb	(%eax), %bl
     *   42adc9: c1 e3 10                     	shll	$16, %ebx
     *   42adcc: 0b d9                        	orl	%ecx, %ebx
     *   42adce: 8b c3                        	movl	%ebx, %eax
     *   42add0: 8b f8                        	movl	%eax, %edi
     *   42add2: 81 e7 ff ff ff 7f            	andl	$2147483647, %edi       # imm = 0x7FFFFFFF
     *   42add8: 3b fe                        	cmpl	%esi, %edi
     *   42adda: 89 7c 24 1c                  	movl	%edi, 28(%esp)
     *   42adde: 73 3e                        	jae	0x42ae1e <.text+0x29e1e>
     *   42ade0: 52                           	pushl	%edx
     *   42ade1: 55                           	pushl	%ebp
     *   42ade2: 8d 5c 24 18                  	leal	24(%esp), %ebx
     * ... (63 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x0042AEA0 - 0x0042B085 (Size: 485 bytes)
 * Assertion line 375: 0 | Message: Decode error
 * Assertion line 401: 0 | Message: Code not done yet!!!!
 * --------------------------------------------------------------------------- */
void BIGcomp_DecodeAllAvailableBlocks(void)
{
    /* Line 375 */ ERR_X_Error(0, "Decode error", NULL);
    /* Line 401 */ ERR_X_Error(0, "Code not done yet!!!!", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   42aea0: a1 24 87 7f 00               	movl	8357668, %eax
     *   42aea5: 83 ec 0c                     	subl	$12, %esp
     *   42aea8: 85 c0                        	testl	%eax, %eax
     *   42aeaa: 0f 84 ad 01 00 00            	je	0x42b05d <.text+0x2a05d>
     *   42aeb0: 8b 44 24 10                  	movl	16(%esp), %eax
     *   42aeb4: 53                           	pushl	%ebx
     *   42aeb5: 8b 58 04                     	movl	4(%eax), %ebx
     *   42aeb8: 55                           	pushl	%ebp
     *   42aeb9: 8b 28                        	movl	(%eax), %ebp
     *   42aebb: c7 40 08 00 00 00 00         	movl	$0, 8(%eax)
     *   42aec2: 3b 6c 24 1c                  	cmpl	28(%esp), %ebp
     *   42aec6: 89 5c 24 0c                  	movl	%ebx, 12(%esp)
     *   42aeca: 0f 83 85 01 00 00            	jae	0x42b055 <.text+0x2a055>
     *   42aed0: 56                           	pushl	%esi
     *   42aed1: 57                           	pushl	%edi
     *   42aed2: 8b 4c 24 24                  	movl	36(%esp), %ecx
     *   42aed6: 8b 3d 24 87 7f 00            	movl	8357668, %edi
     *   42aedc: 2b cd                        	subl	%ebp, %ecx
     *   42aede: 85 ff                        	testl	%edi, %edi
     *   42aee0: 74 29                        	je	0x42af0b <.text+0x29f0b>
     *   42aee2: 0f b6 75 04                  	movzbl	4(%ebp), %esi
     *   42aee6: 33 d2                        	xorl	%edx, %edx
     *   42aee8: 8d 45 04                     	leal	4(%ebp), %eax
     *   42aeeb: 8a 70 01                     	movb	1(%eax), %dh
     *   42aeee: 40                           	incl	%eax
     *   42aeef: 0b f2                        	orl	%edx, %esi
     *   42aef1: 33 d2                        	xorl	%edx, %edx
     *   42aef3: 8a 70 02                     	movb	2(%eax), %dh
     *   42aef6: 40                           	incl	%eax
     *   42aef7: 8a 10                        	movb	(%eax), %dl
     *   42aef9: c1 e2 10                     	shll	$16, %edx
     *   42aefc: 0b d6                        	orl	%esi, %edx
     *   42aefe: 81 e2 ff ff ff 7f            	andl	$2147483647, %edx       # imm = 0x7FFFFFFF
     *   42af04: 83 c2 08                     	addl	$8, %edx
     *   42af07: 3b ca                        	cmpl	%edx, %ecx
     *   42af09: eb 06                        	jmp	0x42af11 <.text+0x29f11>
     *   42af0b: 81 f9 00 00 02 00            	cmpl	$131072, %ecx           # imm = 0x20000
     *   42af11: 1b c0                        	sbbl	%eax, %eax
     *   42af13: 40                           	incl	%eax
     *   42af14: 85 c0                        	testl	%eax, %eax
     *   42af16: 0f 84 37 01 00 00            	je	0x42b053 <.text+0x2a053>
     *   42af1c: 85 ff                        	testl	%edi, %edi
     *   42af1e: 74 25                        	je	0x42af45 <.text+0x29f45>
     *   42af20: 0f b6 4d 00                  	movzbl	(%ebp), %ecx
     *   42af24: 33 d2                        	xorl	%edx, %edx
     *   42af26: 8a 75 01                     	movb	1(%ebp), %dh
     *   42af29: 8d 45 01                     	leal	1(%ebp), %eax
     *   42af2c: 0b ca                        	orl	%edx, %ecx
     *   42af2e: 33 d2                        	xorl	%edx, %edx
     *   42af30: 8a 70 02                     	movb	2(%eax), %dh
     *   42af33: 40                           	incl	%eax
     *   42af34: 8a 10                        	movb	(%eax), %dl
     *   42af36: c1 e2 10                     	shll	$16, %edx
     *   42af39: 0b d1                        	orl	%ecx, %edx
     * ... (110 more instructions)
     */
}
