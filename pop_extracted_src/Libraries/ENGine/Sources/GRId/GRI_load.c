/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/ENGine/Sources/GRId/GRI_load.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 5
 * Unique Functions Mapped: 4
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x006DAF20 - 0x006DAFC2 (Size: 162 bytes)
 * Assertion line 400: _pst_Grids->ppst_AllGrids[i] | Message: Not a real Grid to add
 * Assertion line 370: GRID_guc_AllGrids_Count < 100 | Message: Grid Out of Bound
 * --------------------------------------------------------------------------- */
void GRI_fn_vAddGrid(void)
{
    /* Line 400 */ ERR_X_Error(_pst_Grids->ppst_AllGrids[i], "Not a real Grid to add", NULL);
    /* Line 370 */ ERR_X_Error(GRID_guc_AllGrids_Count < 100, "Grid Out of Bound", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   6daf20: 56                           	pushl	%esi
     *   6daf21: 57                           	pushl	%edi
     *   6daf22: 8b 7c 24 0c                  	movl	12(%esp), %edi
     *   6daf26: 8b 47 04                     	movl	4(%edi), %eax
     *   6daf29: 33 f6                        	xorl	%esi, %esi
     *   6daf2b: 85 c0                        	testl	%eax, %eax
     *   6daf2d: 0f 86 8c 00 00 00            	jbe	0x6dafbf <_SND_fn_vDisplayError@8+0x64e2f>
     *   6daf33: 53                           	pushl	%ebx
     *   6daf34: 8b 07                        	movl	(%edi), %eax
     *   6daf36: 83 3c b0 00                  	cmpl	$0, (%eax,%esi,4)
     *   6daf3a: 75 22                        	jne	0x6daf5e <_SND_fn_vDisplayError@8+0x64dce>
     *   6daf3c: 6a 01                        	pushl	$1
     *   6daf3e: 6a 00                        	pushl	$0
     *   6daf40: 68 c0 91 7b 00               	pushl	$8098240                # imm = 0x7B91C0
     *   6daf45: 68 a0 91 7b 00               	pushl	$8098208                # imm = 0x7B91A0
     *   6daf4a: 68 90 01 00 00               	pushl	$400                    # imm = 0x190
     *   6daf4f: 68 40 91 7b 00               	pushl	$8098112                # imm = 0x7B9140
     *   6daf54: 6a 00                        	pushl	$0
     *   6daf56: e8 75 55 d4 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   6daf5b: 83 c4 1c                     	addl	$28, %esp
     *   6daf5e: 80 3d 50 e9 af 00 64         	cmpb	$100, 11528528
     *   6daf65: 8b 0f                        	movl	(%edi), %ecx
     *   6daf67: 8b 1c b1                     	movl	(%ecx,%esi,4), %ebx
     *   6daf6a: 72 22                        	jb	0x6daf8e <_SND_fn_vDisplayError@8+0x64dfe>
     *   6daf6c: 6a 01                        	pushl	$1
     *   6daf6e: 6a 00                        	pushl	$0
     *   6daf70: 68 8c 91 7b 00               	pushl	$8098188                # imm = 0x7B918C
     *   6daf75: 68 6c 91 7b 00               	pushl	$8098156                # imm = 0x7B916C
     *   6daf7a: 68 72 01 00 00               	pushl	$370                    # imm = 0x172
     *   6daf7f: 68 40 91 7b 00               	pushl	$8098112                # imm = 0x7B9140
     *   6daf84: 6a 00                        	pushl	$0
     *   6daf86: e8 45 55 d4 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   6daf8b: 83 c4 1c                     	addl	$28, %esp
     *   6daf8e: a0 50 e9 af 00               	movb	11528528, %al
     *   6daf93: 0f b6 d0                     	movzbl	%al, %edx
     *   6daf96: fe c0                        	incb	%al
     *   6daf98: 89 1c 95 58 e9 af 00         	movl	%ebx, 11528536(,%edx,4)
     *   6daf9f: a2 50 e9 af 00               	movb	%al, 11528528
     *   6dafa4: 8b 07                        	movl	(%edi), %eax
     *   6dafa6: 8b 0c b0                     	movl	(%eax,%esi,4), %ecx
     *   6dafa9: 51                           	pushl	%ecx
     *   6dafaa: e8 41 b1 fe ff               	calll	0x6c60f0 <_SND_fn_vDisplayError@8+0x4ff60>
     *   6dafaf: 8b 47 04                     	movl	4(%edi), %eax
     *   6dafb2: 83 c4 04                     	addl	$4, %esp
     *   6dafb5: 46                           	incl	%esi
     *   6dafb6: 3b f0                        	cmpl	%eax, %esi
     *   6dafb8: 0f 82 76 ff ff ff            	jb	0x6daf34 <_SND_fn_vDisplayError@8+0x64da4>
     *   6dafbe: 5b                           	popl	%ebx
     *   6dafbf: 5f                           	popl	%edi
     *   6dafc0: 5e                           	popl	%esi
     *   6dafc1: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x006DAFD0 - 0x006DB084 (Size: 180 bytes)
 * Assertion line 425: GRID_guc_AllGrids_Count > 0 | Message: Grid Out of Bound
 * --------------------------------------------------------------------------- */
void sub_006DAFD0(void)
{
    /* Line 425 */ ERR_X_Error(GRID_guc_AllGrids_Count > 0, "Grid Out of Bound", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   6dafd0: a0 50 e9 af 00               	movb	11528528, %al
     *   6dafd5: 84 c0                        	testb	%al, %al
     *   6dafd7: 77 27                        	ja	0x6db000 <_SND_fn_vDisplayError@8+0x64e70>
     *   6dafd9: 6a 01                        	pushl	$1
     *   6dafdb: 6a 00                        	pushl	$0
     *   6dafdd: 68 8c 91 7b 00               	pushl	$8098188                # imm = 0x7B918C
     *   6dafe2: 68 c4 8f 7b 00               	pushl	$8097732                # imm = 0x7B8FC4
     *   6dafe7: 68 a9 01 00 00               	pushl	$425                    # imm = 0x1A9
     *   6dafec: 68 40 91 7b 00               	pushl	$8098112                # imm = 0x7B9140
     *   6daff1: 6a 00                        	pushl	$0
     *   6daff3: e8 d8 54 d4 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   6daff8: a0 50 e9 af 00               	movb	11528528, %al
     *   6daffd: 83 c4 1c                     	addl	$28, %esp
     *   6db000: 53                           	pushl	%ebx
     *   6db001: 32 db                        	xorb	%bl, %bl
     *   6db003: 84 c0                        	testb	%al, %al
     *   6db005: 76 7b                        	jbe	0x6db082 <_SND_fn_vDisplayError@8+0x64ef2>
     *   6db007: 8b 4c 24 08                  	movl	8(%esp), %ecx
     *   6db00b: eb 03                        	jmp	0x6db010 <_SND_fn_vDisplayError@8+0x64e80>
     *   6db00d: 8d 49 00                     	leal	(%ecx), %ecx
     *   6db010: 0f b6 d3                     	movzbl	%bl, %edx
     *   6db013: 39 0c 95 58 e9 af 00         	cmpl	%ecx, 11528536(,%edx,4)
     *   6db01a: 74 08                        	je	0x6db024 <_SND_fn_vDisplayError@8+0x64e94>
     *   6db01c: fe c3                        	incb	%bl
     *   6db01e: 3a d8                        	cmpb	%al, %bl
     *   6db020: 72 ee                        	jb	0x6db010 <_SND_fn_vDisplayError@8+0x64e80>
     *   6db022: 5b                           	popl	%ebx
     *   6db023: c3                           	retl
     *   6db024: 8b 4c 24 0c                  	movl	12(%esp), %ecx
     *   6db028: fe c8                        	decb	%al
     *   6db02a: 85 c9                        	testl	%ecx, %ecx
     *   6db02c: a2 50 e9 af 00               	movb	%al, 11528528
     *   6db031: 74 18                        	je	0x6db04b <_SND_fn_vDisplayError@8+0x64ebb>
     *   6db033: 0f b6 c3                     	movzbl	%bl, %eax
     *   6db036: 8b 0c 85 58 e9 af 00         	movl	11528536(,%eax,4), %ecx
     *   6db03d: 51                           	pushl	%ecx
     *   6db03e: e8 fd ac fe ff               	calll	0x6c5d40 <_SND_fn_vDisplayError@8+0x4fbb0>
     *   6db043: a0 50 e9 af 00               	movb	11528528, %al
     *   6db048: 83 c4 04                     	addl	$4, %esp
     *   6db04b: 84 c0                        	testb	%al, %al
     *   6db04d: 76 25                        	jbe	0x6db074 <_SND_fn_vDisplayError@8+0x64ee4>
     *   6db04f: 3a d8                        	cmpb	%al, %bl
     *   6db051: 73 21                        	jae	0x6db074 <_SND_fn_vDisplayError@8+0x64ee4>
     *   6db053: 0f b6 c0                     	movzbl	%al, %eax
     *   6db056: 8b 0c 85 58 e9 af 00         	movl	11528536(,%eax,4), %ecx
     *   6db05d: 0f b6 d3                     	movzbl	%bl, %edx
     *   6db060: 89 0c 95 58 e9 af 00         	movl	%ecx, 11528536(,%edx,4)
     *   6db067: c7 04 85 58 e9 af 00 00 00 00 00     	movl	$0, 11528536(,%eax,4)
     *   6db072: 5b                           	popl	%ebx
     *   6db073: c3                           	retl
     *   6db074: 0f b6 d3                     	movzbl	%bl, %edx
     *   6db077: c7 04 95 58 e9 af 00 00 00 00 00     	movl	$0, 11528536(,%edx,4)
     *   6db082: 5b                           	popl	%ebx
     *   6db083: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x006DB120 - 0x006DB195 (Size: 117 bytes)
 * Assertion line 515: pst_World && pst_World->pst_AllGrids | Message: Invalid Group Grid
 * --------------------------------------------------------------------------- */
void sub_006DB120(void)
{
    /* Line 515 */ ERR_X_Error(pst_World && pst_World->pst_AllGrids, "Invalid Group Grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   6db120: 56                           	pushl	%esi
     *   6db121: 8b 74 24 08                  	movl	8(%esp), %esi
     *   6db125: 85 f6                        	testl	%esi, %esi
     *   6db127: 74 0a                        	je	0x6db133 <_SND_fn_vDisplayError@8+0x64fa3>
     *   6db129: 8b 86 14 02 00 00            	movl	532(%esi), %eax
     *   6db12f: 85 c0                        	testl	%eax, %eax
     *   6db131: 75 22                        	jne	0x6db155 <_SND_fn_vDisplayError@8+0x64fc5>
     *   6db133: 6a 01                        	pushl	$1
     *   6db135: 6a 00                        	pushl	$0
     *   6db137: 68 00 92 7b 00               	pushl	$8098304                # imm = 0x7B9200
     *   6db13c: 68 d8 91 7b 00               	pushl	$8098264                # imm = 0x7B91D8
     *   6db141: 68 03 02 00 00               	pushl	$515                    # imm = 0x203
     *   6db146: 68 40 91 7b 00               	pushl	$8098112                # imm = 0x7B9140
     *   6db14b: 6a 00                        	pushl	$0
     *   6db14d: e8 7e 53 d4 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   6db152: 83 c4 1c                     	addl	$28, %esp
     *   6db155: 8b 86 14 02 00 00            	movl	532(%esi), %eax
     *   6db15b: 8b 00                        	movl	(%eax), %eax
     *   6db15d: 85 c0                        	testl	%eax, %eax
     *   6db15f: 74 19                        	je	0x6db17a <_SND_fn_vDisplayError@8+0x64fea>
     *   6db161: 50                           	pushl	%eax
     *   6db162: e8 e9 ec f7 ff               	calll	0x659e50 <_SND_fn_vSynchroTimer@0+0x16eb80>
     *   6db167: 8b 8e 14 02 00 00            	movl	532(%esi), %ecx
     *   6db16d: 8b 09                        	movl	(%ecx), %ecx
     *   6db16f: 8b 10                        	movl	(%eax), %edx
     *   6db171: 83 c4 04                     	addl	$4, %esp
     *   6db174: 51                           	pushl	%ecx
     *   6db175: 8b c8                        	movl	%eax, %ecx
     *   6db177: ff 52 08                     	calll	*8(%edx)
     *   6db17a: 8b 96 14 02 00 00            	movl	532(%esi), %edx
     *   6db180: c7 02 00 00 00 00            	movl	$0, (%edx)
     *   6db186: 8b 86 14 02 00 00            	movl	532(%esi), %eax
     *   6db18c: c7 40 04 00 00 00 00         	movl	$0, 4(%eax)
     *   6db193: 5e                           	popl	%esi
     *   6db194: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x006DB910 - 0x006DBB02 (Size: 498 bytes)
 * Assertion line 330: 0L | Message: Grid LINK not supported YET
 * --------------------------------------------------------------------------- */
void sub_006DB910(void)
{
    /* Line 330 */ ERR_X_Error(0L, "Grid LINK not supported YET", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   6db910: a1 c0 53 ae 00               	movl	11424704, %eax
     *   6db915: 83 ec 0c                     	subl	$12, %esp
     *   6db918: 85 c0                        	testl	%eax, %eax
     *   6db91a: 75 0a                        	jne	0x6db926 <_SND_fn_vDisplayError@8+0x65796>
     *   6db91c: 6a 02                        	pushl	$2
     *   6db91e: e8 ad e8 f7 ff               	calll	0x65a1d0 <_SND_fn_vSynchroTimer@0+0x16ef00>
     *   6db923: 83 c4 04                     	addl	$4, %esp
     *   6db926: 53                           	pushl	%ebx
     *   6db927: 56                           	pushl	%esi
     *   6db928: 6a 08                        	pushl	$8
     *   6db92a: 8b c8                        	movl	%eax, %ecx
     *   6db92c: e8 0f 4f d4 ff               	calll	0x420840 <.text+0x1f840>
     *   6db931: 8b f0                        	movl	%eax, %esi
     *   6db933: 33 c0                        	xorl	%eax, %eax
     *   6db935: 8b ce                        	movl	%esi, %ecx
     *   6db937: 89 01                        	movl	%eax, (%ecx)
     *   6db939: 6a 01                        	pushl	$1
     *   6db93b: 8d 54 24 14                  	leal	20(%esp), %edx
     *   6db93f: 89 41 04                     	movl	%eax, 4(%ecx)
     *   6db942: 8b 44 24 1c                  	movl	28(%esp), %eax
     *   6db946: 52                           	pushl	%edx
     *   6db947: 50                           	pushl	%eax
     *   6db948: e8 03 cc d4 ff               	calll	0x428550 <.text+0x27550>
     *   6db94d: 8b d8                        	movl	%eax, %ebx
     *   6db94f: 83 c4 0c                     	addl	$12, %esp
     *   6db952: 85 db                        	testl	%ebx, %ebx
     *   6db954: 75 06                        	jne	0x6db95c <_SND_fn_vDisplayError@8+0x657cc>
     *   6db956: 5e                           	popl	%esi
     *   6db957: 5b                           	popl	%ebx
     *   6db958: 83 c4 0c                     	addl	$12, %esp
     *   6db95b: c3                           	retl
     *   6db95c: 8b 44 24 10                  	movl	16(%esp), %eax
     *   6db960: c1 e8 03                     	shrl	$3, %eax
     *   6db963: 85 c0                        	testl	%eax, %eax
     *   6db965: 89 44 24 10                  	movl	%eax, 16(%esp)
     *   6db969: 0f 84 8b 01 00 00            	je	0x6dbafa <_SND_fn_vDisplayError@8+0x6596a>
     *   6db96f: a1 c0 53 ae 00               	movl	11424704, %eax
     *   6db974: 85 c0                        	testl	%eax, %eax
     *   6db976: 75 0a                        	jne	0x6db982 <_SND_fn_vDisplayError@8+0x657f2>
     *   6db978: 6a 02                        	pushl	$2
     *   6db97a: e8 51 e8 f7 ff               	calll	0x65a1d0 <_SND_fn_vSynchroTimer@0+0x16ef00>
     *   6db97f: 83 c4 04                     	addl	$4, %esp
     *   6db982: 8b 4c 24 10                  	movl	16(%esp), %ecx
     *   6db986: 8d 14 8d 00 00 00 00         	leal	(,%ecx,4), %edx
     *   6db98d: 55                           	pushl	%ebp
     *   6db98e: 52                           	pushl	%edx
     *   6db98f: 8b c8                        	movl	%eax, %ecx
     *   6db991: e8 aa 4e d4 ff               	calll	0x420840 <.text+0x1f840>
     *   6db996: 89 06                        	movl	%eax, (%esi)
     *   6db998: 8b 44 24 14                  	movl	20(%esp), %eax
     *   6db99c: 33 ed                        	xorl	%ebp, %ebp
     *   6db99e: 85 c0                        	testl	%eax, %eax
     *   6db9a0: 0f 86 2d 01 00 00            	jbe	0x6dbad3 <_SND_fn_vDisplayError@8+0x65943>
     *   6db9a6: 57                           	pushl	%edi
     * ... (116 more instructions)
     */
}
