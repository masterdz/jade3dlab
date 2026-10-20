/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/ENGine/Sources/GRId/GRI_compute.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x006C5D40 - 0x006C60E2 (Size: 930 bytes)
 * Assertion line 2234: GRID_guc_AllGrids_Count > 0 | Message: No Grid Available. Check that the current world has a grid
 * --------------------------------------------------------------------------- */
void GRI_fn_vComputeGrid(void)
{
    /* Line 2234 */ ERR_X_Error(GRID_guc_AllGrids_Count > 0, "No Grid Available. Check that the current world has a grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   6c5d40: 56                           	pushl	%esi
     *   6c5d41: 8b 74 24 08                  	movl	8(%esp), %esi
     *   6c5d45: 85 f6                        	testl	%esi, %esi
     *   6c5d47: 0f 84 f1 00 00 00            	je	0x6c5e3e <_SND_fn_vDisplayError@8+0x4fcae>
     *   6c5d4d: 0f bf 46 2a                  	movswl	42(%esi), %eax
     *   6c5d51: 0f bf 4e 28                  	movswl	40(%esi), %ecx
     *   6c5d55: 0f af c1                     	imull	%ecx, %eax
     *   6c5d58: 57                           	pushl	%edi
     *   6c5d59: 33 ff                        	xorl	%edi, %edi
     *   6c5d5b: 85 c0                        	testl	%eax, %eax
     *   6c5d5d: 7e 32                        	jle	0x6c5d91 <_SND_fn_vDisplayError@8+0x4fc01>
     *   6c5d5f: 90                           	nop
     *   6c5d60: 8b 56 04                     	movl	4(%esi), %edx
     *   6c5d63: 8b 04 ba                     	movl	(%edx,%edi,4), %eax
     *   6c5d66: 85 c0                        	testl	%eax, %eax
     *   6c5d68: 74 17                        	je	0x6c5d81 <_SND_fn_vDisplayError@8+0x4fbf1>
     *   6c5d6a: 50                           	pushl	%eax
     *   6c5d6b: e8 e0 40 f9 ff               	calll	0x659e50 <_SND_fn_vSynchroTimer@0+0x16eb80>
     *   6c5d70: 8b 4e 04                     	movl	4(%esi), %ecx
     *   6c5d73: 8b 0c b9                     	movl	(%ecx,%edi,4), %ecx
     *   6c5d76: 8b 10                        	movl	(%eax), %edx
     *   6c5d78: 83 c4 04                     	addl	$4, %esp
     *   6c5d7b: 51                           	pushl	%ecx
     *   6c5d7c: 8b c8                        	movl	%eax, %ecx
     *   6c5d7e: ff 52 08                     	calll	*8(%edx)
     *   6c5d81: 0f bf 56 2a                  	movswl	42(%esi), %edx
     *   6c5d85: 0f bf 46 28                  	movswl	40(%esi), %eax
     *   6c5d89: 0f af d0                     	imull	%eax, %edx
     *   6c5d8c: 47                           	incl	%edi
     *   6c5d8d: 3b fa                        	cmpl	%edx, %edi
     *   6c5d8f: 7c cf                        	jl	0x6c5d60 <_SND_fn_vDisplayError@8+0x4fbd0>
     *   6c5d91: 8b 46 08                     	movl	8(%esi), %eax
     *   6c5d94: 85 c0                        	testl	%eax, %eax
     *   6c5d96: 5f                           	popl	%edi
     *   6c5d97: 74 24                        	je	0x6c5dbd <_SND_fn_vDisplayError@8+0x4fc2d>
     *   6c5d99: 50                           	pushl	%eax
     *   6c5d9a: e8 51 00 d6 ff               	calll	0x425df0 <.text+0x24df0>
     *   6c5d9f: 8b 46 08                     	movl	8(%esi), %eax
     *   6c5da2: 83 c4 04                     	addl	$4, %esp
     *   6c5da5: 85 c0                        	testl	%eax, %eax
     *   6c5da7: 74 14                        	je	0x6c5dbd <_SND_fn_vDisplayError@8+0x4fc2d>
     *   6c5da9: 50                           	pushl	%eax
     *   6c5daa: e8 a1 40 f9 ff               	calll	0x659e50 <_SND_fn_vSynchroTimer@0+0x16eb80>
     *   6c5daf: 8b 4e 08                     	movl	8(%esi), %ecx
     *   6c5db2: 8b 10                        	movl	(%eax), %edx
     *   6c5db4: 83 c4 04                     	addl	$4, %esp
     *   6c5db7: 51                           	pushl	%ecx
     *   6c5db8: 8b c8                        	movl	%eax, %ecx
     *   6c5dba: ff 52 08                     	calll	*8(%edx)
     *   6c5dbd: 8b 06                        	movl	(%esi), %eax
     *   6c5dbf: 85 c0                        	testl	%eax, %eax
     *   6c5dc1: 74 13                        	je	0x6c5dd6 <_SND_fn_vDisplayError@8+0x4fc46>
     *   6c5dc3: 50                           	pushl	%eax
     *   6c5dc4: e8 87 40 f9 ff               	calll	0x659e50 <_SND_fn_vSynchroTimer@0+0x16eb80>
     * ... (239 more instructions)
     */
}
