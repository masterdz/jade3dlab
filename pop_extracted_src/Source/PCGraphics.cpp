/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Source/PCGraphics.cpp
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x00665DE0 - 0x00666B82 (Size: 3490 bytes)
 * Assertion line 667: ÁùÊ;ÁA | Message: ÁùÊ;ÁA
 * --------------------------------------------------------------------------- */
void sub_00665DE0(void)
{
    /* Line 667 */ ERR_X_Error(ÁùÊ;ÁA, "ÁùÊ;ÁA", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 0065e5b0 <_SND_fn_ulGetListOfSoundEventNameInGroup@12>:
     *   665de0: 83 ec 2c                     	subl	$44, %esp
     *   665de3: 8b 0d 58 37 9f 00            	movl	10434392, %ecx
     *   665de9: 8b 81 08 08 00 00            	movl	2056(%ecx), %eax
     *   665def: 8b 90 c8 ee 0b 00            	movl	782024(%eax), %edx
     *   665df5: 8b 80 9c dc 01 00            	movl	122012(%eax), %eax
     *   665dfb: 85 c0                        	testl	%eax, %eax
     *   665dfd: 53                           	pushl	%ebx
     *   665dfe: 55                           	pushl	%ebp
     *   665dff: 56                           	pushl	%esi
     *   665e00: 57                           	pushl	%edi
     *   665e01: be 80 80 80 ff               	movl	$4286611584, %esi       # imm = 0xFF808080
     *   665e06: c7 44 24 28 00 00 00 00      	movl	$0, 40(%esp)
     *   665e0e: 89 54 24 18                  	movl	%edx, 24(%esp)
     *   665e12: 89 44 24 14                  	movl	%eax, 20(%esp)
     *   665e16: 75 2e                        	jne	0x665e46 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0x7896>
     *   665e18: 8b 81 08 08 00 00            	movl	2056(%ecx), %eax
     *   665e1e: 8b 40 04                     	movl	4(%eax), %eax
     *   665e21: 0b 05 a4 89 ae 00            	orl	11438500, %eax
     *   665e27: 33 c2                        	xorl	%edx, %eax
     *   665e29: 89 44 24 10                  	movl	%eax, 16(%esp)
     *   665e2d: 0f b6 74 24 12               	movzbl	18(%esp), %esi
     *   665e32: 8b c8                        	movl	%eax, %ecx
     *   665e34: 81 e1 ff 00 00 00            	andl	$255, %ecx
     *   665e3a: c1 e1 10                     	shll	$16, %ecx
     *   665e3d: 0b f1                        	orl	%ecx, %esi
     *   665e3f: 25 00 ff 00 ff               	andl	$4278255360, %eax       # imm = 0xFF00FF00
     *   665e44: 0b f0                        	orl	%eax, %esi
     *   665e46: 6a 00                        	pushl	$0
     *   665e48: 6a 00                        	pushl	$0
     *   665e4a: 6a 06                        	pushl	$6
     *   665e4c: b9 70 96 ae 00               	movl	$11441776, %ecx         # imm = 0xAE9670
     *   665e51: e8 ba 74 00 00               	calll	0x66d310 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xed60>
     *   665e56: a1 d4 89 ae 00               	movl	11438548, %eax
     *   665e5b: d1 e8                        	shrl	%eax
     *   665e5d: 83 e0 01                     	andl	$1, %eax
     *   665e60: 6a 00                        	pushl	$0
     *   665e62: b9 c8 89 ae 00               	movl	$11438536, %ecx         # imm = 0xAE89C8
     *   665e67: 89 44 24 3c                  	movl	%eax, 60(%esp)
     *   665e6b: e8 30 7f 00 00               	calll	0x66dda0 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xf7f0>
     *   665e70: 6a 01                        	pushl	$1
     *   665e72: b9 c8 89 ae 00               	movl	$11438536, %ecx         # imm = 0xAE89C8
     *   665e77: e8 a4 7a 00 00               	calll	0x66d920 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xf370>
     *   665e7c: b9 c8 89 ae 00               	movl	$11438536, %ecx         # imm = 0xAE89C8
     *   665e81: e8 9a 77 00 00               	calll	0x66d620 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xf070>
     *   665e86: 8b 15 58 37 9f 00            	movl	10434392, %edx
     *   665e8c: 8b 42 74                     	movl	116(%edx), %eax
     *   665e8f: 50                           	pushl	%eax
     *   665e90: b9 8c 89 ae 00               	movl	$11438476, %ecx         # imm = 0xAE898C
     *   665e95: e8 36 93 00 00               	calll	0x66f1d0 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0x10c20>
     *   665e9a: 8b 0d 58 37 9f 00            	movl	10434392, %ecx
     *   665ea0: 8b 91 94 00 00 00            	movl	148(%ecx), %edx
     *   665ea6: 8b 5a 10                     	movl	16(%edx), %ebx
     *   665ea9: 8b 54 24 40                  	movl	64(%esp), %edx
     *   665ead: 8b 42 0c                     	movl	12(%edx), %eax
     * ... (1040 more instructions)
     */
}
