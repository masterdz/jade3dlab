/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/ENGine/Sources/Text/TEXTload.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 2
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x0069D250 - 0x0069D379 (Size: 297 bytes)
 * Assertion line 64: DOH | Message: None
 * Assertion line 67: DOH | Message: \Libraries\ENGine\Sources\Text\TEXTload.c
 * --------------------------------------------------------------------------- */
void sub_0069D250(void)
{
    /* Line 64 */ ERR_X_Error(DOH, "Unknown error", NULL);
    /* Line 67 */ ERR_X_Error(DOH, "\Libraries\ENGine\Sources\Text\TEXTload.c", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   69d250: e8 8b 0d 08 00               	calll	0x71dfe0 <_SND_fn_ulGetNumberOfSoundEventGroup@0>
     *   69d255: 8b 0d 88 d1 af 00            	movl	11522440, %ecx
     *   69d25b: 2b c8                        	subl	%eax, %ecx
     *   69d25d: 8b c1                        	movl	%ecx, %eax
     *   69d25f: c3                           	retl
     *   69d260: 83 ec 0c                     	subl	$12, %esp
     *   69d263: 8b 4c 24 10                  	movl	16(%esp), %ecx
     *   69d267: 56                           	pushl	%esi
     *   69d268: 6a 01                        	pushl	$1
     *   69d26a: 8d 44 24 10                  	leal	16(%esp), %eax
     *   69d26e: 50                           	pushl	%eax
     *   69d26f: 51                           	pushl	%ecx
     *   69d270: e8 db b2 d8 ff               	calll	0x428550 <.text+0x27550>
     *   69d275: 83 c4 0c                     	addl	$12, %esp
     *   69d278: 33 f6                        	xorl	%esi, %esi
     *   69d27a: 85 c0                        	testl	%eax, %eax
     *   69d27c: 89 44 24 08                  	movl	%eax, 8(%esp)
     *   69d280: 0f 84 d0 00 00 00            	je	0x69d356 <_SND_fn_vDisplayError@8+0x271c6>
     *   69d286: a1 c0 53 ae 00               	movl	11424704, %eax
     *   69d28b: 85 c0                        	testl	%eax, %eax
     *   69d28d: 75 0a                        	jne	0x69d299 <_SND_fn_vDisplayError@8+0x27109>
     *   69d28f: 6a 02                        	pushl	$2
     *   69d291: e8 3a cf fb ff               	calll	0x65a1d0 <_SND_fn_vSynchroTimer@0+0x16ef00>
     *   69d296: 83 c4 04                     	addl	$4, %esp
     *   69d299: 8b 54 24 0c                  	movl	12(%esp), %edx
     *   69d29d: 53                           	pushl	%ebx
     *   69d29e: 57                           	pushl	%edi
     *   69d29f: 83 c2 04                     	addl	$4, %edx
     *   69d2a2: 52                           	pushl	%edx
     *   69d2a3: 8b c8                        	movl	%eax, %ecx
     *   69d2a5: e8 96 35 d8 ff               	calll	0x420840 <.text+0x1f840>
     *   69d2aa: 8b f0                        	movl	%eax, %esi
     *   69d2ac: 8b 44 24 14                  	movl	20(%esp), %eax
     *   69d2b0: 33 ff                        	xorl	%edi, %edi
     *   69d2b2: a9 fc ff ff ff               	testl	$4294967292, %eax       # imm = 0xFFFFFFFC
     *   69d2b7: 8b de                        	movl	%esi, %ebx
     *   69d2b9: 76 6e                        	jbe	0x69d329 <_SND_fn_vDisplayError@8+0x27199>
     *   69d2bb: eb 03                        	jmp	0x69d2c0 <_SND_fn_vDisplayError@8+0x27130>
     *   69d2bd: 8d 49 00                     	leal	(%ecx), %ecx
     *   69d2c0: 8b 44 24 10                  	movl	16(%esp), %eax
     *   69d2c4: 8b 08                        	movl	(%eax), %ecx
     *   69d2c6: 83 c0 04                     	addl	$4, %eax
     *   69d2c9: 89 44 24 10                  	movl	%eax, 16(%esp)
     *   69d2cd: a1 28 2a 9e 00               	movl	10365480, %eax
     *   69d2d2: 85 c0                        	testl	%eax, %eax
     *   69d2d4: 89 4c 24 0c                  	movl	%ecx, 12(%esp)
     *   69d2d8: 74 25                        	je	0x69d2ff <_SND_fn_vDisplayError@8+0x2716f>
     *   69d2da: 8b d1                        	movl	%ecx, %edx
     *   69d2dc: 8a c1                        	movb	%cl, %al
     *   69d2de: c1 ea 18                     	shrl	$24, %edx
     *   69d2e1: 88 44 24 0f                  	movb	%al, 15(%esp)
     *   69d2e5: 88 54 24 0c                  	movb	%dl, 12(%esp)
     *   69d2e9: 8b 44 24 0c                  	movl	12(%esp), %eax
     *   69d2ed: 8b 4c 24 0c                  	movl	12(%esp), %ecx
     * ... (51 more instructions)
     */
}
