/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/AIinterp/Sources/Functions/AIfunctions_wor.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 2
 * Unique Functions Mapped: 2
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x0049CCF0 - 0x0049CD8B (Size: 155 bytes)
 * Assertion line 405: AI_gi_FunctionStackLevel == 0 | Message: The function [WORReinit] cannot be use inside a function
 * --------------------------------------------------------------------------- */
void sub_0049CCF0(void)
{
    /* Line 405 */ ERR_X_Error(AI_gi_FunctionStackLevel == 0, "The function [WORReinit] cannot be use inside a function", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   49ccf0: 56                           	pushl	%esi
     *   49ccf1: 6a 01                        	pushl	$1
     *   49ccf3: e8 d8 e5 04 00               	calll	0x4eb2d0 <_SND_fn_vSynchroTimer@0>
     *   49ccf8: a1 90 c8 af 00               	movl	11520144, %eax
     *   49ccfd: 50                           	pushl	%eax
     *   49ccfe: e8 5d 55 1f 00               	calll	0x692260 <_SND_fn_vDisplayError@8+0x1c0d0>
     *   49cd03: 8b 4c 24 10                  	movl	16(%esp), %ecx
     *   49cd07: 6a 00                        	pushl	$0
     *   49cd09: 51                           	pushl	%ecx
     *   49cd0a: 6a 00                        	pushl	$0
     *   49cd0c: e8 bf 34 1e 00               	calll	0x6801d0 <_SND_fn_vDisplayError@8+0xa040>
     *   49cd11: 83 c4 14                     	addl	$20, %esp
     *   49cd14: e8 77 a5 f7 ff               	calll	0x417290 <.text+0x16290>
     *   49cd19: 8b c8                        	movl	%eax, %ecx
     *   49cd1b: e8 b0 a6 f7 ff               	calll	0x4173d0 <.text+0x163d0>
     *   49cd20: 8b f0                        	movl	%eax, %esi
     *   49cd22: e8 69 a5 f7 ff               	calll	0x417290 <.text+0x16290>
     *   49cd27: 8b c8                        	movl	%eax, %ecx
     *   49cd29: e8 b2 a6 f7 ff               	calll	0x4173e0 <.text+0x163e0>
     *   49cd2e: 85 f6                        	testl	%esi, %esi
     *   49cd30: 74 09                        	je	0x49cd3b <.text+0x9bd3b>
     *   49cd32: 56                           	pushl	%esi
     *   49cd33: e8 88 ec 1d 00               	calll	0x67b9c0 <_SND_fn_vDisplayError@8+0x5830>
     *   49cd38: 83 c4 04                     	addl	$4, %esp
     *   49cd3b: 33 c0                        	xorl	%eax, %eax
     *   49cd3d: 5e                           	popl	%esi
     *   49cd3e: c3                           	retl
     *   49cd3f: cc                           	int3
     *   49cd40: c7 05 c0 b7 af 00 01 00 00 00	movl	$1, 11515840
     *   49cd4a: b8 03 00 00 00               	movl	$3, %eax
     *   49cd4f: c3                           	retl
     *   49cd50: a1 98 3b ac 00               	movl	11287448, %eax
     *   49cd55: 85 c0                        	testl	%eax, %eax
     *   49cd57: 74 22                        	je	0x49cd7b <.text+0x9bd7b>
     *   49cd59: 6a 01                        	pushl	$1
     *   49cd5b: 6a 00                        	pushl	$0
     *   49cd5d: 68 38 0c 7b 00               	pushl	$8064056                # imm = 0x7B0C38
     *   49cd62: 68 18 0c 7b 00               	pushl	$8064024                # imm = 0x7B0C18
     *   49cd67: 68 95 01 00 00               	pushl	$405                    # imm = 0x195
     *   49cd6c: 68 e0 0b 7b 00               	pushl	$8063968                # imm = 0x7B0BE0
     *   49cd71: 6a 00                        	pushl	$0
     *   49cd73: e8 58 37 f8 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   49cd78: 83 c4 1c                     	addl	$28, %esp
     *   49cd7b: c7 05 c0 b7 af 00 01 00 00 00	movl	$1, 11515840
     *   49cd85: b8 03 00 00 00               	movl	$3, %eax
     *   49cd8a: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x0049D5F0 - 0x0049D76C (Size: 380 bytes)
 * Assertion line 665: OBJ_BV_IsSphere(pst_GO->pst_BV) | Message: AddPortal: Object must have a spherical BV
 * --------------------------------------------------------------------------- */
void sub_0049D5F0(void)
{
    /* Line 665 */ ERR_X_Error(OBJ_BV_IsSphere(pst_GO->pst_BV), "AddPortal: Object must have a spherical BV", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   49d5f0: 83 ec 4c                     	subl	$76, %esp
     *   49d5f3: a1 74 3b ac 00               	movl	11287412, %eax
     *   49d5f8: 8b 0d 70 3b ac 00            	movl	11287408, %ecx
     *   49d5fe: 8b 15 68 3b ac 00            	movl	11287400, %edx
     *   49d604: 53                           	pushl	%ebx
     *   49d605: 55                           	pushl	%ebp
     *   49d606: 89 0d 74 3b ac 00            	movl	%ecx, 11287412
     *   49d60c: 8b 0d 4c 3b ac 00            	movl	11287372, %ecx
     *   49d612: 89 44 24 10                  	movl	%eax, 16(%esp)
     *   49d616: a1 50 3b ac 00               	movl	11287376, %eax
     *   49d61b: 56                           	pushl	%esi
     *   49d61c: 83 e9 20                     	subl	$32, %ecx
     *   49d61f: 57                           	pushl	%edi
     *   49d620: 48                           	decl	%eax
     *   49d621: bf 02 00 00 00               	movl	$2, %edi
     *   49d626: 66 39 3c c5 40 b4 aa 00      	cmpw	%di, 11187264(,%eax,8)
     *   49d62e: 89 15 6c 3b ac 00            	movl	%edx, 11287404
     *   49d634: 75 16                        	jne	0x49d64c <.text+0x9c64c>
     *   49d636: d9 81 40 b5 ab 00            	flds	11253056(%ecx)
     *   49d63c: dc 05 a0 1d b2 00            	faddl	11672992
     *   49d642: dd 5c 24 10                  	fstpl	16(%esp)
     *   49d646: 8b 54 24 10                  	movl	16(%esp), %edx
     *   49d64a: eb 06                        	jmp	0x49d652 <.text+0x9c652>
     *   49d64c: 8b 91 40 b5 ab 00            	movl	11253056(%ecx), %edx
     *   49d652: 83 e9 20                     	subl	$32, %ecx
     *   49d655: 48                           	decl	%eax
     *   49d656: 66 39 3c c5 40 b4 aa 00      	cmpw	%di, 11187264(,%eax,8)
     *   49d65e: 89 54 24 10                  	movl	%edx, 16(%esp)
     *   49d662: 89 0d 4c 3b ac 00            	movl	%ecx, 11287372
     *   49d668: 75 16                        	jne	0x49d680 <.text+0x9c680>
     *   49d66a: d9 81 40 b5 ab 00            	flds	11253056(%ecx)
     *   49d670: dc 05 a0 1d b2 00            	faddl	11672992
     *   49d676: dd 5c 24 1c                  	fstpl	28(%esp)
     *   49d67a: 8b 6c 24 1c                  	movl	28(%esp), %ebp
     *   49d67e: eb 06                        	jmp	0x49d686 <.text+0x9c686>
     *   49d680: 8b a9 40 b5 ab 00            	movl	11253056(%ecx), %ebp
     *   49d686: 66 8b 0c c5 38 b4 aa 00      	movw	11187256(,%eax,8), %cx
     *   49d68e: 8b 34 c5 3c b4 aa 00         	movl	11187260(,%eax,8), %esi
     *   49d695: 48                           	decl	%eax
     *   49d696: a3 50 3b ac 00               	movl	%eax, 11287376
     *   49d69b: 0f bf c1                     	movswl	%cx, %eax
     *   49d69e: 8d 4c 24 24                  	leal	36(%esp), %ecx
     *   49d6a2: 51                           	pushl	%ecx
     *   49d6a3: 56                           	pushl	%esi
     *   49d6a4: ff 14 c5 3c b9 7f 00         	calll	*8370492(,%eax,8)
     *   49d6ab: a1 4c 3b ac 00               	movl	11287372, %eax
     *   49d6b0: 8b 0d 50 3b ac 00            	movl	11287376, %ecx
     *   49d6b6: 83 c4 08                     	addl	$8, %esp
     *   49d6b9: 83 e8 40                     	subl	$64, %eax
     *   49d6bc: 49                           	decl	%ecx
     *   49d6bd: 66 39 3c cd 40 b4 aa 00      	cmpw	%di, 11187264(,%ecx,8)
     *   49d6c5: 75 16                        	jne	0x49d6dd <.text+0x9c6dd>
     *   49d6c7: d9 80 40 b5 ab 00            	flds	11253056(%eax)
     *   49d6cd: dc 05 a0 1d b2 00            	faddl	11672992
     * ... (47 more instructions)
     */
}
