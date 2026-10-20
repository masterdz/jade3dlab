/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/AIinterp/Sources/Events/EVEplay.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 2
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x0064B290 - 0x0064B942 (Size: 1714 bytes)
 * Assertion line 741: !(pst_Current->uw_Flags & 0x0008) | Message: EVE_C_EventFlag_WaitFalse no longer supported
 * Assertion line 742: !(pst_Current->uw_Flags & 0x0010) | Message: EVE_C_EventFlag_WaitTrue no longer supported
 * --------------------------------------------------------------------------- */
void sub_0064B290(void)
{
    /* Line 741 */ ERR_X_Error(!(pst_Current->uw_Flags & 0x0008), "EVE_C_EventFlag_WaitFalse no longer supported", NULL);
    /* Line 742 */ ERR_X_Error(!(pst_Current->uw_Flags & 0x0010), "EVE_C_EventFlag_WaitTrue no longer supported", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 004eb2d0 <_SND_fn_vSynchroTimer@0>:
     *   64b290: 55                           	pushl	%ebp
     *   64b291: 8b ec                        	movl	%esp, %ebp
     *   64b293: 83 e4 f8                     	andl	$-8, %esp
     *   64b296: 83 ec 14                     	subl	$20, %esp
     *   64b299: 8b 4d 08                     	movl	8(%ebp), %ecx
     *   64b29c: 8b 41 04                     	movl	4(%ecx), %eax
     *   64b29f: 53                           	pushl	%ebx
     *   64b2a0: 33 d2                        	xorl	%edx, %edx
     *   64b2a2: 3b c2                        	cmpl	%edx, %eax
     *   64b2a4: 56                           	pushl	%esi
     *   64b2a5: 57                           	pushl	%edi
     *   64b2a6: 89 54 24 10                  	movl	%edx, 16(%esp)
     *   64b2aa: 0f 84 89 06 00 00            	je	0x64b939 <_SND_fn_vSynchroTimer@0+0x160669>
     *   64b2b0: a1 cc 43 ae 00               	movl	11420620, %eax
     *   64b2b5: 8b 40 0c                     	movl	12(%eax), %eax
     *   64b2b8: 8b 5d 0c                     	movl	12(%ebp), %ebx
     *   64b2bb: a3 ec 43 ae 00               	movl	%eax, 11420652
     *   64b2c0: 39 55 10                     	cmpl	%edx, 16(%ebp)
     *   64b2c3: 74 56                        	je	0x64b31b <_SND_fn_vSynchroTimer@0+0x16004b>
     *   64b2c5: d9 05 44 3e 81 00            	flds	8470084
     *   64b2cb: d8 1d ac cd 7a 00            	fcomps	8048044
     *   64b2d1: df e0                        	fnstsw	%ax
     *   64b2d3: f6 c4 41                     	testb	$65, %ah
     *   64b2d6: 75 43                        	jne	0x64b31b <_SND_fn_vSynchroTimer@0+0x16004b>
     *   64b2d8: 0f b7 71 0c                  	movzwl	12(%ecx), %esi
     *   64b2dc: 0f b7 43 08                  	movzwl	8(%ebx), %eax
     *   64b2e0: 4e                           	decl	%esi
     *   64b2e1: 3b c6                        	cmpl	%esi, %eax
     *   64b2e3: 75 36                        	jne	0x64b31b <_SND_fn_vSynchroTimer@0+0x16004b>
     *   64b2e5: 8b 71 04                     	movl	4(%ecx), %esi
     *   64b2e8: 0f b7 04 c6                  	movzwl	(%esi,%eax,8), %eax
     *   64b2ec: 89 44 24 18                  	movl	%eax, 24(%esp)
     *   64b2f0: db 44 24 18                  	fildl	24(%esp)
     *   64b2f4: d9 5c 24 18                  	fstps	24(%esp)
     *   64b2f8: d9 44 24 18                  	flds	24(%esp)
     *   64b2fc: d8 35 d8 ff 7a 00            	fdivs	8060888
     *   64b302: d9 03                        	flds	(%ebx)
     *   64b304: da e9                        	fucompp
     *   64b306: df e0                        	fnstsw	%ax
     *   64b308: f6 c4 44                     	testb	$68, %ah
     *   64b30b: 7a 0e                        	jp	0x64b31b <_SND_fn_vSynchroTimer@0+0x16004b>
     *   64b30d: f6 41 0e 02                  	testb	$2, 14(%ecx)
     *   64b311: 74 08                        	je	0x64b31b <_SND_fn_vSynchroTimer@0+0x16004b>
     *   64b313: 80 63 0a fb                  	andb	$-5, 10(%ebx)
     *   64b317: 66 89 53 08                  	movw	%dx, 8(%ebx)
     *   64b31b: 8b 0d 44 3e 81 00            	movl	8470084, %ecx
     *   64b321: 89 4c 24 0c                  	movl	%ecx, 12(%esp)
     *   64b325: 0f b7 53 08                  	movzwl	8(%ebx), %edx
     *   64b329: 8b 45 08                     	movl	8(%ebp), %eax
     *   64b32c: 52                           	pushl	%edx
     *   64b32d: 53                           	pushl	%ebx
     *   64b32e: 50                           	pushl	%eax
     *   64b32f: e8 bc 0c 00 00               	calll	0x64bff0 <_SND_fn_vSynchroTimer@0+0x160d20>
     *   64b334: 8b f0                        	movl	%eax, %esi
     * ... (449 more instructions)
     */
}
