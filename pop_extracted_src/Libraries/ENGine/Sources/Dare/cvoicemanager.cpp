/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/ENGine/Sources/Dare/cvoicemanager.cpp
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x006A54D0 - 0x006A5616 (Size: 326 bytes)
 * Assertion line 249: 0 | Message: CVoiceManager::PlayVoice: Bank %d is not loaded.
 * --------------------------------------------------------------------------- */
void sub_006A54D0(void)
{
    /* Line 249 */ ERR_X_Error(0, "CVoiceManager::PlayVoice: Bank %d is not loaded.", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   6a54d0: 8b 51 04                     	movl	4(%ecx), %edx
     *   6a54d3: 33 c0                        	xorl	%eax, %eax
     *   6a54d5: 85 d2                        	testl	%edx, %edx
     *   6a54d7: 56                           	pushl	%esi
     *   6a54d8: 76 1a                        	jbe	0x6a54f4 <_SND_fn_vDisplayError@8+0x2f364>
     *   6a54da: 57                           	pushl	%edi
     *   6a54db: 8b 7c 24 10                  	movl	16(%esp), %edi
     *   6a54df: 53                           	pushl	%ebx
     *   6a54e0: 8d 71 08                     	leal	8(%ecx), %esi
     *   6a54e3: 8b 1e                        	movl	(%esi), %ebx
     *   6a54e5: 39 7b 04                     	cmpl	%edi, 4(%ebx)
     *   6a54e8: 74 08                        	je	0x6a54f2 <_SND_fn_vDisplayError@8+0x2f362>
     *   6a54ea: 40                           	incl	%eax
     *   6a54eb: 83 c6 04                     	addl	$4, %esi
     *   6a54ee: 3b c2                        	cmpl	%edx, %eax
     *   6a54f0: 72 f1                        	jb	0x6a54e3 <_SND_fn_vDisplayError@8+0x2f353>
     *   6a54f2: 5b                           	popl	%ebx
     *   6a54f3: 5f                           	popl	%edi
     *   6a54f4: 3b c2                        	cmpl	%edx, %eax
     *   6a54f6: 73 68                        	jae	0x6a5560 <_SND_fn_vDisplayError@8+0x2f3d0>
     *   6a54f8: 8b 54 81 08                  	movl	8(%ecx,%eax,4), %edx
     *   6a54fc: 8b 72 10                     	movl	16(%edx), %esi
     *   6a54ff: 85 f6                        	testl	%esi, %esi
     *   6a5501: 74 35                        	je	0x6a5538 <_SND_fn_vDisplayError@8+0x2f3a8>
     *   6a5503: 83 fe 04                     	cmpl	$4, %esi
     *   6a5506: 74 30                        	je	0x6a5538 <_SND_fn_vDisplayError@8+0x2f3a8>
     *   6a5508: 6a 01                        	pushl	$1
     *   6a550a: 6a 00                        	pushl	$0
     *   6a550c: 50                           	pushl	%eax
     *   6a550d: 68 18 8e 7b 00               	pushl	$8097304                # imm = 0x7B8E18
     *   6a5512: e8 c9 8a 07 00               	calll	0x71dfe0 <_SND_fn_ulGetNumberOfSoundEventGroup@0>
     *   6a5517: 83 c4 08                     	addl	$8, %esp
     *   6a551a: 50                           	pushl	%eax
     *   6a551b: 68 b8 f2 7a 00               	pushl	$8057528                # imm = 0x7AF2B8
     *   6a5520: 68 f9 00 00 00               	pushl	$249
     *   6a5525: 68 e4 8d 7b 00               	pushl	$8097252                # imm = 0x7B8DE4
     *   6a552a: 6a 00                        	pushl	$0
     *   6a552c: e8 9f af d7 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   6a5531: 83 c4 1c                     	addl	$28, %esp
     *   6a5534: 5e                           	popl	%esi
     *   6a5535: c2 14 00                     	retl	$20
     *   6a5538: 8b 44 24 10                  	movl	16(%esp), %eax
     *   6a553c: 3b 42 08                     	cmpl	8(%edx), %eax
     *   6a553f: 73 1f                        	jae	0x6a5560 <_SND_fn_vDisplayError@8+0x2f3d0>
     *   6a5541: 8b 52 0c                     	movl	12(%edx), %edx
     *   6a5544: 8b 04 82                     	movl	(%edx,%eax,4), %eax
     *   6a5547: 85 c0                        	testl	%eax, %eax
     *   6a5549: 74 15                        	je	0x6a5560 <_SND_fn_vDisplayError@8+0x2f3d0>
     *   6a554b: 8b 54 24 18                  	movl	24(%esp), %edx
     *   6a554f: 52                           	pushl	%edx
     *   6a5550: 8b 54 24 18                  	movl	24(%esp), %edx
     *   6a5554: 52                           	pushl	%edx
     *   6a5555: 50                           	pushl	%eax
     *   6a5556: 8b 44 24 14                  	movl	20(%esp), %eax
     * ... (79 more instructions)
     */
}
