/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/Sdk/Sources/PackFiles/bigfile.cpp
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x007A5FE0 - 0x007A6B4E (Size: 2926 bytes)
 * Assertion line 57: SeekFile_Current not supported | Message: None
 * --------------------------------------------------------------------------- */
void sub_007A5FE0(void)
{
    /* Line 57 */ ERR_X_Error(SeekFile_Current not supported, "Unknown error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 007a4d30 <_SND_fn_vDestroyStreamAsyncSnd@4>:
     *   7a5fe0: 8b 44 24 08                  	movl	8(%esp), %eax
     *   7a5fe4: 83 e8 00                     	subl	$0, %eax
     *   7a5fe7: 56                           	pushl	%esi
     *   7a5fe8: 57                           	pushl	%edi
     *   7a5fe9: 8b f1                        	movl	%ecx, %esi
     *   7a5feb: 74 3d                        	je	0x7a602a <_SND_fn_vDestroyStreamAsyncSnd@4+0x12fa>
     *   7a5fed: 48                           	decl	%eax
     *   7a5fee: 74 1e                        	je	0x7a600e <_SND_fn_vDestroyStreamAsyncSnd@4+0x12de>
     *   7a5ff0: 48                           	decl	%eax
     *   7a5ff1: 74 08                        	je	0x7a5ffb <_SND_fn_vDestroyStreamAsyncSnd@4+0x12cb>
     *   7a5ff3: 5f                           	popl	%edi
     *   7a5ff4: 83 c8 ff                     	orl	$-1, %eax
     *   7a5ff7: 5e                           	popl	%esi
     *   7a5ff8: c2 08 00                     	retl	$8
     *   7a5ffb: 8b 7e 0c                     	movl	12(%esi), %edi
     *   7a5ffe: 8b 44 24 0c                  	movl	12(%esp), %eax
     *   7a6002: 3b c7                        	cmpl	%edi, %eax
     *   7a6004: 73 04                        	jae	0x7a600a <_SND_fn_vDestroyStreamAsyncSnd@4+0x12da>
     *   7a6006: 2b f8                        	subl	%eax, %edi
     *   7a6008: eb 24                        	jmp	0x7a602e <_SND_fn_vDestroyStreamAsyncSnd@4+0x12fe>
     *   7a600a: 33 ff                        	xorl	%edi, %edi
     *   7a600c: eb 20                        	jmp	0x7a602e <_SND_fn_vDestroyStreamAsyncSnd@4+0x12fe>
     *   7a600e: 6a 01                        	pushl	$1
     *   7a6010: 6a 00                        	pushl	$0
     *   7a6012: 68 88 e7 7e 00               	pushl	$8316808                # imm = 0x7EE788
     *   7a6017: 6a 00                        	pushl	$0
     *   7a6019: 6a 39                        	pushl	$57
     *   7a601b: 68 58 e7 7e 00               	pushl	$8316760                # imm = 0x7EE758
     *   7a6020: 6a 00                        	pushl	$0
     *   7a6022: e8 a9 a4 c7 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   7a6027: 83 c4 1c                     	addl	$28, %esp
     *   7a602a: 8b 7c 24 0c                  	movl	12(%esp), %edi
     *   7a602e: 8b 46 0c                     	movl	12(%esi), %eax
     *   7a6031: 3b f8                        	cmpl	%eax, %edi
     *   7a6033: 76 02                        	jbe	0x7a6037 <_SND_fn_vDestroyStreamAsyncSnd@4+0x1307>
     *   7a6035: 8b f8                        	movl	%eax, %edi
     *   7a6037: 8b 46 04                     	movl	4(%esi), %eax
     *   7a603a: 8b 0d 08 54 ae 00            	movl	11424776, %ecx
     *   7a6040: 50                           	pushl	%eax
     *   7a6041: e8 aa 43 eb ff               	calll	0x65a3f0 <_SND_fn_vSynchroTimer@0+0x16f120>
     *   7a6046: 8b 46 0c                     	movl	12(%esi), %eax
     *   7a6049: 8b 4e 08                     	movl	8(%esi), %ecx
     *   7a604c: 8b 56 04                     	movl	4(%esi), %edx
     *   7a604f: 2b c7                        	subl	%edi, %eax
     *   7a6051: 50                           	pushl	%eax
     *   7a6052: 03 cf                        	addl	%edi, %ecx
     *   7a6054: 51                           	pushl	%ecx
     *   7a6055: c7 46 14 00 00 00 00         	movl	$0, 20(%esi)
     *   7a605c: 89 46 10                     	movl	%eax, 16(%esi)
     *   7a605f: 8b 0d 08 54 ae 00            	movl	11424776, %ecx
     *   7a6065: 52                           	pushl	%edx
     *   7a6066: e8 b5 49 eb ff               	calll	0x65aa20 <_SND_fn_vSynchroTimer@0+0x16f750>
     *   7a606b: 8b 0d 08 54 ae 00            	movl	11424776, %ecx
     *   7a6071: e8 1a 4c eb ff               	calll	0x65ac90 <_SND_fn_vSynchroTimer@0+0x16f9c0>
     * ... (1085 more instructions)
     */
}
