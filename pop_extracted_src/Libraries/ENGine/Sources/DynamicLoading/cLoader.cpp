/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/ENGine/Sources/DynamicLoading/cLoader.cpp
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 2
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x0067DA40 - 0x0067DF77 (Size: 1335 bytes)
 * Assertion line 460: Doh!!!! Pas suppose de passer ici... | Message: None
 * Assertion line 437: 0 | Message: This case is not supported yet
 * --------------------------------------------------------------------------- */
void sub_0067DA40(void)
{
    /* Line 460 */ ERR_X_Error(Doh!!!! Pas suppose de passer ici..., "Unknown error", NULL);
    /* Line 437 */ ERR_X_Error(0, "This case is not supported yet", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   67da40: 55                           	pushl	%ebp
     *   67da41: 8b ec                        	movl	%esp, %ebp
     *   67da43: 83 e4 f8                     	andl	$-8, %esp
     *   67da46: 83 ec 20                     	subl	$32, %esp
     *   67da49: 53                           	pushl	%ebx
     *   67da4a: 55                           	pushl	%ebp
     *   67da4b: 56                           	pushl	%esi
     *   67da4c: 57                           	pushl	%edi
     *   67da4d: 8b e9                        	movl	%ecx, %ebp
     *   67da4f: 8b b5 24 40 00 00            	movl	16420(%ebp), %esi
     *   67da55: 8b 46 04                     	movl	4(%esi), %eax
     *   67da58: 8b 48 04                     	movl	4(%eax), %ecx
     *   67da5b: 33 ff                        	xorl	%edi, %edi
     *   67da5d: 51                           	pushl	%ecx
     *   67da5e: 8b ce                        	movl	%esi, %ecx
     *   67da60: 89 7c 24 18                  	movl	%edi, 24(%esp)
     *   67da64: 89 7c 24 14                  	movl	%edi, 20(%esp)
     *   67da68: 89 7c 24 1c                  	movl	%edi, 28(%esp)
     *   67da6c: e8 8f e9 ff ff               	calll	0x67c400 <_SND_fn_vDisplayError@8+0x6270>
     *   67da71: 8b 46 04                     	movl	4(%esi), %eax
     *   67da74: 89 40 04                     	movl	%eax, 4(%eax)
     *   67da77: 8b 46 04                     	movl	4(%esi), %eax
     *   67da7a: 89 7e 08                     	movl	%edi, 8(%esi)
     *   67da7d: 89 00                        	movl	%eax, (%eax)
     *   67da7f: 8b 76 04                     	movl	4(%esi), %esi
     *   67da82: 89 76 08                     	movl	%esi, 8(%esi)
     *   67da85: 8b 95 00 40 00 00            	movl	16384(%ebp), %edx
     *   67da8b: 52                           	pushl	%edx
     *   67da8c: e8 8f 41 00 00               	calll	0x681c20 <_SND_fn_vDisplayError@8+0xba90>
     *   67da91: 8b f0                        	movl	%eax, %esi
     *   67da93: 83 c4 04                     	addl	$4, %esp
     *   67da96: 83 fe ff                     	cmpl	$-1, %esi
     *   67da99: 74 34                        	je	0x67dacf <_SND_fn_vDisplayError@8+0x793f>
     *   67da9b: 39 3e                        	cmpl	%edi, (%esi)
     *   67da9d: 7e 1f                        	jle	0x67dabe <_SND_fn_vDisplayError@8+0x792e>
     *   67da9f: 90                           	nop
     *   67daa0: 8b 46 04                     	movl	4(%esi), %eax
     *   67daa3: 8d 0c b8                     	leal	(%eax,%edi,4), %ecx
     *   67daa6: 51                           	pushl	%ecx
     *   67daa7: 8b 8d 24 40 00 00            	movl	16420(%ebp), %ecx
     *   67daad: 8d 54 24 2c                  	leal	44(%esp), %edx
     *   67dab1: 52                           	pushl	%edx
     *   67dab2: e8 49 fd ff ff               	calll	0x67d800 <_SND_fn_vDisplayError@8+0x7670>
     *   67dab7: 8b 06                        	movl	(%esi), %eax
     *   67dab9: 47                           	incl	%edi
     *   67daba: 3b f8                        	cmpl	%eax, %edi
     *   67dabc: 7c e2                        	jl	0x67daa0 <_SND_fn_vDisplayError@8+0x7910>
     *   67dabe: 8b 06                        	movl	(%esi), %eax
     *   67dac0: 8b 4e 04                     	movl	4(%esi), %ecx
     *   67dac3: 8b 54 81 fc                  	movl	-4(%ecx,%eax,4), %edx
     *   67dac7: 89 95 0c 40 00 00            	movl	%edx, 16396(%ebp)
     *   67dacd: eb 58                        	jmp	0x67db27 <_SND_fn_vDisplayError@8+0x7997>
     *   67dacf: 6a 01                        	pushl	$1
     *   67dad1: e8 1a c2 da ff               	calll	0x429cf0 <.text+0x28cf0>
     * ... (373 more instructions)
     */
}
