/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/ENGine/Sources/MoDiFier/Rope2D.cpp
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x006EED50 - 0x006EEEDC (Size: 396 bytes)
 * Assertion line 61: m_fAccelarationTime != 0.0f | Message: None
 * --------------------------------------------------------------------------- */
void sub_006EED50(void)
{
    /* Line 61 */ ERR_X_Error(m_fAccelarationTime != 0.0f, "Unknown error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   6eed50: 51                           	pushl	%ecx
     *   6eed51: d9 44 24 08                  	flds	8(%esp)
     *   6eed55: 56                           	pushl	%esi
     *   6eed56: 8b f1                        	movl	%ecx, %esi
     *   6eed58: d8 76 14                     	fdivs	20(%esi)
     *   6eed5b: d8 46 20                     	fadds	32(%esi)
     *   6eed5e: d9 5c 24 04                  	fstps	4(%esp)
     *   6eed62: d9 46 0c                     	flds	12(%esi)
     *   6eed65: 8b 4c 24 04                  	movl	4(%esp), %ecx
     *   6eed69: d8 1d 34 c9 7a 00            	fcomps	8046900
     *   6eed6f: 89 4e 20                     	movl	%ecx, 32(%esi)
     *   6eed72: df e0                        	fnstsw	%ax
     *   6eed74: f6 c4 05                     	testb	$5, %ah
     *   6eed77: 7a 69                        	jp	0x6eede2 <_SND_fn_vDisplayError@8+0x78c52>
     *   6eed79: d9 05 ac cd 7a 00            	flds	8048044
     *   6eed7f: d9 46 18                     	flds	24(%esi)
     *   6eed82: da e9                        	fucompp
     *   6eed84: df e0                        	fnstsw	%ax
     *   6eed86: f6 c4 44                     	testb	$68, %ah
     *   6eed89: 7a 1c                        	jp	0x6eeda7 <_SND_fn_vDisplayError@8+0x78c17>
     *   6eed8b: 6a 01                        	pushl	$1
     *   6eed8d: 6a 00                        	pushl	$0
     *   6eed8f: 6a 00                        	pushl	$0
     *   6eed91: 68 0c 94 7b 00               	pushl	$8098828                # imm = 0x7B940C
     *   6eed96: 6a 3d                        	pushl	$61
     *   6eed98: 68 dc 93 7b 00               	pushl	$8098780                # imm = 0x7B93DC
     *   6eed9d: 6a 00                        	pushl	$0
     *   6eed9f: e8 2c 17 d3 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   6eeda4: 83 c4 1c                     	addl	$28, %esp
     *   6eeda7: d9 44 24 0c                  	flds	12(%esp)
     *   6eedab: 8b 46 20                     	movl	32(%esi), %eax
     *   6eedae: d8 76 18                     	fdivs	24(%esi)
     *   6eedb1: 89 44 24 0c                  	movl	%eax, 12(%esp)
     *   6eedb5: 83 ec 08                     	subl	$8, %esp
     *   6eedb8: d8 46 0c                     	fadds	12(%esi)
     *   6eedbb: d9 5e 0c                     	fstps	12(%esi)
     *   6eedbe: d9 44 24 14                  	flds	20(%esp)
     *   6eedc2: dd 1c 24                     	fstpl	(%esp)
     *   6eedc5: e8 ea 0e 04 00               	calll	0x72fcb4 <_SND_fn_bInitMallocSnd@0+0x76c4>
     *   6eedca: d9 5c 24 14                  	fstps	20(%esp)
     *   6eedce: d9 44 24 14                  	flds	20(%esp)
     *   6eedd2: d9 5c 24 14                  	fstps	20(%esp)
     *   6eedd6: d9 44 24 14                  	flds	20(%esp)
     *   6eedda: d8 4e 10                     	fmuls	16(%esi)
     *   6eeddd: d8 4e 0c                     	fmuls	12(%esi)
     *   6eede0: eb 1e                        	jmp	0x6eee00 <_SND_fn_vDisplayError@8+0x78c70>
     *   6eede2: 89 4c 24 0c                  	movl	%ecx, 12(%esp)
     *   6eede6: d9 44 24 0c                  	flds	12(%esp)
     *   6eedea: 83 ec 08                     	subl	$8, %esp
     *   6eeded: dd 1c 24                     	fstpl	(%esp)
     *   6eedf0: e8 bf 0e 04 00               	calll	0x72fcb4 <_SND_fn_bInitMallocSnd@0+0x76c4>
     *   6eedf5: d9 5c 24 14                  	fstps	20(%esp)
     *   6eedf9: d9 44 24 14                  	flds	20(%esp)
     *   6eedfd: d8 4e 10                     	fmuls	16(%esi)
     * ... (79 more instructions)
     */
}
