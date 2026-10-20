/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Source/ShadowMgr.cpp
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 2
 * Unique Functions Mapped: 2
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x0066E3E0 - 0x0066EE4B (Size: 2667 bytes)
 * Assertion line 50: iIndex < MaxShadowStates | Message: ShadowMgr::CreateShadow
 * --------------------------------------------------------------------------- */
void sub_0066E3E0(void)
{
    /* Line 50 */ ERR_X_Error(iIndex < MaxShadowStates, "ShadowMgr::CreateShadow", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 0065e5b0 <_SND_fn_ulGetListOfSoundEventNameInGroup@12>:
     *   66e3e0: 56                           	pushl	%esi
     *   66e3e1: 8b f1                        	movl	%ecx, %esi
     *   66e3e3: b9 c8 89 ae 00               	movl	$11438536, %ecx         # imm = 0xAE89C8
     *   66e3e8: e8 33 f2 ff ff               	calll	0x66d620 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xf070>
     *   66e3ed: a1 58 37 9f 00               	movl	10434392, %eax
     *   66e3f2: 8b 48 74                     	movl	116(%eax), %ecx
     *   66e3f5: 51                           	pushl	%ecx
     *   66e3f6: b9 8c 89 ae 00               	movl	$11438476, %ecx         # imm = 0xAE898C
     *   66e3fb: e8 d0 0d 00 00               	calll	0x66f1d0 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0x10c20>
     *   66e400: 8b 54 24 08                  	movl	8(%esp), %edx
     *   66e404: 52                           	pushl	%edx
     *   66e405: 8b ce                        	movl	%esi, %ecx
     *   66e407: e8 64 ff ff ff               	calll	0x66e370 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xfdc0>
     *   66e40c: 5e                           	popl	%esi
     *   66e40d: c2 04 00                     	retl	$4
     *   66e410: 56                           	pushl	%esi
     *   66e411: 57                           	pushl	%edi
     *   66e412: 8b f9                        	movl	%ecx, %edi
     *   66e414: 33 f6                        	xorl	%esi, %esi
     *   66e416: 8d 87 24 01 00 00            	leal	292(%edi), %eax
     *   66e41c: 8d 64 24 00                  	leal	(%esp), %esp
     *   66e420: 8b 88 6c ff ff ff            	movl	-148(%eax), %ecx
     *   66e426: 85 c9                        	testl	%ecx, %ecx
     *   66e428: 74 33                        	je	0x66e45d <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xfead>
     *   66e42a: 83 38 00                     	cmpl	$0, (%eax)
     *   66e42d: 74 23                        	je	0x66e452 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xfea2>
     *   66e42f: 8b 88 94 00 00 00            	movl	148(%eax), %ecx
     *   66e435: 85 c9                        	testl	%ecx, %ecx
     *   66e437: 74 1c                        	je	0x66e455 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xfea5>
     *   66e439: 8b 88 28 01 00 00            	movl	296(%eax), %ecx
     *   66e43f: 85 c9                        	testl	%ecx, %ecx
     *   66e441: 74 17                        	je	0x66e45a <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xfeaa>
     *   66e443: 83 c6 04                     	addl	$4, %esi
     *   66e446: 05 50 02 00 00               	addl	$592, %eax              # imm = 0x250
     *   66e44b: 83 fe 20                     	cmpl	$32, %esi
     *   66e44e: 7c d0                        	jl	0x66e420 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xfe70>
     *   66e450: eb 10                        	jmp	0x66e462 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xfeb2>
     *   66e452: 46                           	incl	%esi
     *   66e453: eb 08                        	jmp	0x66e45d <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xfead>
     *   66e455: 83 c6 02                     	addl	$2, %esi
     *   66e458: eb 03                        	jmp	0x66e45d <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xfead>
     *   66e45a: 83 c6 03                     	addl	$3, %esi
     *   66e45d: 83 fe 20                     	cmpl	$32, %esi
     *   66e460: 7c 22                        	jl	0x66e484 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xfed4>
     *   66e462: 6a 01                        	pushl	$1
     *   66e464: 68 70 6e 7b 00               	pushl	$8089200                # imm = 0x7B6E70
     *   66e469: 68 58 6e 7b 00               	pushl	$8089176                # imm = 0x7B6E58
     *   66e46e: 68 70 6e 7b 00               	pushl	$8089200                # imm = 0x7B6E70
     *   66e473: 6a 32                        	pushl	$50
     *   66e475: 68 40 6e 7b 00               	pushl	$8089152                # imm = 0x7B6E40
     *   66e47a: 6a 00                        	pushl	$0
     *   66e47c: e8 4f 20 db ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   66e481: 83 c4 1c                     	addl	$28, %esp
     *   66e484: 8b 54 24 0c                  	movl	12(%esp), %edx
     * ... (772 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x0066E4E0 - 0x0066EE4B (Size: 2411 bytes)
 * Assertion line 462: iIndex < PCTextureMgr::MaxShadows | Message: ShadowMgr::AssignShadowTextureIndex
 * --------------------------------------------------------------------------- */
void sub_0066E4E0(void)
{
    /* Line 462 */ ERR_X_Error(iIndex < PCTextureMgr::MaxShadows, "ShadowMgr::AssignShadowTextureIndex", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 0065e5b0 <_SND_fn_ulGetListOfSoundEventNameInGroup@12>:
     *   66e4e0: 56                           	pushl	%esi
     *   66e4e1: 57                           	pushl	%edi
     *   66e4e2: 8b f9                        	movl	%ecx, %edi
     *   66e4e4: 33 f6                        	xorl	%esi, %esi
     *   66e4e6: eb 08                        	jmp	0x66e4f0 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xff40>
     *   66e4e8: 8d a4 24 00 00 00 00         	leal	(%esp), %esp
     *   66e4ef: 90                           	nop
     *   66e4f0: 8a 84 37 88 9a 00 00         	movb	39560(%edi,%esi), %al
     *   66e4f7: 84 c0                        	testb	%al, %al
     *   66e4f9: 74 36                        	je	0x66e531 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xff81>
     *   66e4fb: 8a 84 3e 89 9a 00 00         	movb	39561(%esi,%edi), %al
     *   66e502: 84 c0                        	testb	%al, %al
     *   66e504: 74 20                        	je	0x66e526 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xff76>
     *   66e506: 8a 84 3e 8a 9a 00 00         	movb	39562(%esi,%edi), %al
     *   66e50d: 84 c0                        	testb	%al, %al
     *   66e50f: 74 18                        	je	0x66e529 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xff79>
     *   66e511: 8a 84 3e 8b 9a 00 00         	movb	39563(%esi,%edi), %al
     *   66e518: 84 c0                        	testb	%al, %al
     *   66e51a: 74 12                        	je	0x66e52e <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xff7e>
     *   66e51c: 83 c6 04                     	addl	$4, %esi
     *   66e51f: 83 fe 10                     	cmpl	$16, %esi
     *   66e522: 7c cc                        	jl	0x66e4f0 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xff40>
     *   66e524: eb 10                        	jmp	0x66e536 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xff86>
     *   66e526: 46                           	incl	%esi
     *   66e527: eb 08                        	jmp	0x66e531 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xff81>
     *   66e529: 83 c6 02                     	addl	$2, %esi
     *   66e52c: eb 03                        	jmp	0x66e531 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xff81>
     *   66e52e: 83 c6 03                     	addl	$3, %esi
     *   66e531: 83 fe 10                     	cmpl	$16, %esi
     *   66e534: 7c 39                        	jl	0x66e56f <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xffbf>
     *   66e536: 6a 01                        	pushl	$1
     *   66e538: 68 d4 6e 7b 00               	pushl	$8089300                # imm = 0x7B6ED4
     *   66e53d: 68 b0 6e 7b 00               	pushl	$8089264                # imm = 0x7B6EB0
     *   66e542: 68 8c 6e 7b 00               	pushl	$8089228                # imm = 0x7B6E8C
     *   66e547: 68 ce 01 00 00               	pushl	$462                    # imm = 0x1CE
     *   66e54c: 68 40 6e 7b 00               	pushl	$8089152                # imm = 0x7B6E40
     *   66e551: 6a 00                        	pushl	$0
     *   66e553: e8 78 1f db ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   66e558: 8b 44 24 28                  	movl	40(%esp), %eax
     *   66e55c: 83 c4 1c                     	addl	$28, %esp
     *   66e55f: 89 70 04                     	movl	%esi, 4(%eax)
     *   66e562: c6 84 3e 88 9a 00 00 01      	movb	$1, 39560(%esi,%edi)
     *   66e56a: 5f                           	popl	%edi
     *   66e56b: 5e                           	popl	%esi
     *   66e56c: c2 04 00                     	retl	$4
     *   66e56f: 8b 4c 24 0c                  	movl	12(%esp), %ecx
     *   66e573: 89 71 04                     	movl	%esi, 4(%ecx)
     *   66e576: c6 84 3e 88 9a 00 00 01      	movb	$1, 39560(%esi,%edi)
     *   66e57e: 5f                           	popl	%edi
     *   66e57f: 5e                           	popl	%esi
     *   66e580: c2 04 00                     	retl	$4
     *   66e583: cc                           	int3
     *   66e584: cc                           	int3
     *   66e585: cc                           	int3
     * ... (677 more instructions)
     */
}
