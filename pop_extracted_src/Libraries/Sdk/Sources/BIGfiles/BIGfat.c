/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/Sdk/Sources/BIGfiles/BIGfat.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 7
 * Unique Functions Mapped: 3
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x004287C0 - 0x00428AC1 (Size: 769 bytes)
 * Assertion line 55: BIG_fread(&BIG_gst.st_ToSave, sizeof(BIG_gst.st_ToSave), (BIG_gst.h_CLibFileHandle)) == 1 | Message: Error while reading file
 * Assertion line 79: strcmp(BIG_gst.st_ToSave.ac_Def, "BIG\0") == 0 | Message: Big file corrupt
 * --------------------------------------------------------------------------- */
void BIG_OpenFat(void)
{
    /* Line 55 */ ERR_X_Error(BIG_fread(&BIG_gst.st_ToSave, sizeof(BIG_gst.st_ToSave), (BIG_gst.h_CLibFileHandle)) == 1, "Error while reading file", NULL);
    /* Line 79 */ ERR_X_Error(strcmp(BIG_gst.st_ToSave.ac_Def, "BIG\0") == 0, "Big file corrupt", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   4287c0: a1 48 48 81 00               	movl	8472648, %eax
     *   4287c5: 83 ec 08                     	subl	$8, %esp
     *   4287c8: 56                           	pushl	%esi
     *   4287c9: 57                           	pushl	%edi
     *   4287ca: 50                           	pushl	%eax
     *   4287cb: 6a 2c                        	pushl	$44
     *   4287cd: be 18 47 81 00               	movl	$8472344, %esi          # imm = 0x814718
     *   4287d2: 56                           	pushl	%esi
     *   4287d3: e8 c8 0d 00 00               	calll	0x4295a0 <.text+0x285a0>
     *   4287d8: 83 c4 0c                     	addl	$12, %esp
     *   4287db: 83 f8 01                     	cmpl	$1, %eax
     *   4287de: 74 1f                        	je	0x4287ff <.text+0x277ff>
     *   4287e0: 6a 01                        	pushl	$1
     *   4287e2: 6a 00                        	pushl	$0
     *   4287e4: 68 cc f7 7a 00               	pushl	$8058828                # imm = 0x7AF7CC
     *   4287e9: 68 d8 f9 7a 00               	pushl	$8059352                # imm = 0x7AF9D8
     *   4287ee: 6a 37                        	pushl	$55
     *   4287f0: 68 a8 f9 7a 00               	pushl	$8059304                # imm = 0x7AF9A8
     *   4287f5: 6a 00                        	pushl	$0
     *   4287f7: e8 d4 7c ff ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4287fc: 83 c4 1c                     	addl	$28, %esp
     *   4287ff: 53                           	pushl	%ebx
     *   428800: 6a 01                        	pushl	$1
     *   428802: 6a 04                        	pushl	$4
     *   428804: 8d 4c 24 14                  	leal	20(%esp), %ecx
     *   428808: 56                           	pushl	%esi
     *   428809: 51                           	pushl	%ecx
     *   42880a: 89 74 24 1c                  	movl	%esi, 28(%esp)
     *   42880e: e8 1d 14 00 00               	calll	0x429c30 <.text+0x28c30>
     *   428813: 8b 44 24 1c                  	movl	28(%esp), %eax
     *   428817: 8b 10                        	movl	(%eax), %edx
     *   428819: 8b 0d 28 2a 9e 00            	movl	10365480, %ecx
     *   42881f: 83 c0 04                     	addl	$4, %eax
     *   428822: 83 c4 10                     	addl	$16, %esp
     *   428825: 85 c9                        	testl	%ecx, %ecx
     *   428827: 89 54 24 10                  	movl	%edx, 16(%esp)
     *   42882b: 89 44 24 0c                  	movl	%eax, 12(%esp)
     *   42882f: 74 23                        	je	0x428854 <.text+0x27854>
     *   428831: 8b da                        	movl	%edx, %ebx
     *   428833: c1 eb 18                     	shrl	$24, %ebx
     *   428836: 88 5c 24 10                  	movb	%bl, 16(%esp)
     *   42883a: 88 54 24 13                  	movb	%dl, 19(%esp)
     *   42883e: 8b 54 24 10                  	movl	16(%esp), %edx
     *   428842: 8b 5c 24 10                  	movl	16(%esp), %ebx
     *   428846: c1 ea 08                     	shrl	$8, %edx
     *   428849: c1 eb 10                     	shrl	$16, %ebx
     *   42884c: 88 5c 24 11                  	movb	%bl, 17(%esp)
     *   428850: 88 54 24 12                  	movb	%dl, 18(%esp)
     *   428854: 8b 54 24 10                  	movl	16(%esp), %edx
     *   428858: 89 15 1c 47 81 00            	movl	%edx, 8472348
     *   42885e: 8b 10                        	movl	(%eax), %edx
     *   428860: 83 c0 04                     	addl	$4, %eax
     *   428863: 85 c9                        	testl	%ecx, %ecx
     *   428865: 89 54 24 10                  	movl	%edx, 16(%esp)
     * ... (178 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00428AD0 - 0x00428C53 (Size: 387 bytes)
 * Assertion line 156: BIG_fseek((BIG_gst.h_CLibFileHandle), _pst_Fat->ul_PosFat + (0), 0) == 0 | Message: fseek error
 * Assertion line 177: BIG_fread ( (UCHAR *) BIG_gst.dst_FileTable, ul_NumRead * sizeof(BIG_tdst_File), (BIG_gst.h_CLibFileHandle) ) == 1 | Message: Error while reading file
 * --------------------------------------------------------------------------- */
void BIG_ReadFatFile(void)
{
    /* Line 156 */ ERR_X_Error(BIG_fseek((BIG_gst.h_CLibFileHandle), _pst_Fat->ul_PosFat + (0), 0) == 0, "fseek error", NULL);
    /* Line 177 */ ERR_X_Error(BIG_fread ( (UCHAR *) BIG_gst.dst_FileTable, ul_NumRead * sizeof(BIG_tdst_File), (BIG_gst.h_CLibFileHandle) ) == 1, "Error while reading file", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   428ad0: 51                           	pushl	%ecx
     *   428ad1: 56                           	pushl	%esi
     *   428ad2: 8b 74 24 0c                  	movl	12(%esp), %esi
     *   428ad6: 83 3e 00                     	cmpl	$0, (%esi)
     *   428ad9: 0f 84 71 01 00 00            	je	0x428c50 <.text+0x27c50>
     *   428adf: 8b 46 08                     	movl	8(%esi), %eax
     *   428ae2: 8b 0d 48 48 81 00            	movl	8472648, %ecx
     *   428ae8: 6a 00                        	pushl	$0
     *   428aea: 50                           	pushl	%eax
     *   428aeb: 51                           	pushl	%ecx
     *   428aec: e8 af 05 00 00               	calll	0x4290a0 <.text+0x280a0>
     *   428af1: 83 c4 0c                     	addl	$12, %esp
     *   428af4: 85 c0                        	testl	%eax, %eax
     *   428af6: 74 22                        	je	0x428b1a <.text+0x27b1a>
     *   428af8: 6a 01                        	pushl	$1
     *   428afa: 6a 00                        	pushl	$0
     *   428afc: 68 4c f8 7a 00               	pushl	$8058956                # imm = 0x7AF84C
     *   428b01: 68 b0 fa 7a 00               	pushl	$8059568                # imm = 0x7AFAB0
     *   428b06: 68 9c 00 00 00               	pushl	$156
     *   428b0b: 68 a8 f9 7a 00               	pushl	$8059304                # imm = 0x7AF9A8
     *   428b10: 6a 00                        	pushl	$0
     *   428b12: e8 b9 79 ff ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   428b17: 83 c4 1c                     	addl	$28, %esp
     *   428b1a: 8b 06                        	movl	(%esi), %eax
     *   428b1c: 33 d2                        	xorl	%edx, %edx
     *   428b1e: 85 c0                        	testl	%eax, %eax
     *   428b20: 0f 86 2a 01 00 00            	jbe	0x428c50 <.text+0x27c50>
     *   428b26: 8b 0d 60 48 81 00            	movl	8472672, %ecx
     *   428b2c: 53                           	pushl	%ebx
     *   428b2d: 55                           	pushl	%ebp
     *   428b2e: 57                           	pushl	%edi
     *   428b2f: 90                           	nop
     *   428b30: 8d 5a 64                     	leal	100(%edx), %ebx
     *   428b33: 3b d8                        	cmpl	%eax, %ebx
     *   428b35: bd 64 00 00 00               	movl	$100, %ebp
     *   428b3a: 76 04                        	jbe	0x428b40 <.text+0x27b40>
     *   428b3c: 2b c2                        	subl	%edx, %eax
     *   428b3e: 8b e8                        	movl	%eax, %ebp
     *   428b40: 8b 15 48 48 81 00            	movl	8472648, %edx
     *   428b46: 52                           	pushl	%edx
     *   428b47: 8d 04 ed 00 00 00 00         	leal	(,%ebp,8), %eax
     *   428b4e: 50                           	pushl	%eax
     *   428b4f: 51                           	pushl	%ecx
     *   428b50: e8 4b 0a 00 00               	calll	0x4295a0 <.text+0x285a0>
     *   428b55: 83 c4 0c                     	addl	$12, %esp
     *   428b58: 83 f8 01                     	cmpl	$1, %eax
     *   428b5b: 74 22                        	je	0x428b7f <.text+0x27b7f>
     *   428b5d: 6a 01                        	pushl	$1
     *   428b5f: 6a 00                        	pushl	$0
     *   428b61: 68 cc f7 7a 00               	pushl	$8058828                # imm = 0x7AF7CC
     *   428b66: 68 38 fa 7a 00               	pushl	$8059448                # imm = 0x7AFA38
     *   428b6b: 68 b1 00 00 00               	pushl	$177
     *   428b70: 68 a8 f9 7a 00               	pushl	$8059304                # imm = 0x7AF9A8
     *   428b75: 6a 00                        	pushl	$0
     * ... (69 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00428C60 - 0x00429116 (Size: 1206 bytes)
 * Assertion line 332: BIG_gst.dst_FatTable != 0L | Message: Not enough memory
 * Assertion line 348: BIG_fread ( (UCHAR *) &(BIG_gst.dst_FatTable[i]), sizeof(BIG_gst.dst_FatTable[i]), (BIG_gst.h_CLibFileHandle) ) == 1 | Message: Error while reading file
 * Assertion line 371: BIG_fseek ( (BIG_gst.h_CLibFileHandle), BIG_gst.dst_FatTable[i].ul_NextPosFat - sizeof(BIG_tdst_FatDes), 0 ) == 0 | Message: fseek error
 * --------------------------------------------------------------------------- */
void BIG_ReadFat(void)
{
    /* Line 332 */ ERR_X_Error(BIG_gst.dst_FatTable != 0L, "Not enough memory", NULL);
    /* Line 348 */ ERR_X_Error(BIG_fread ( (UCHAR *) &(BIG_gst.dst_FatTable[i]), sizeof(BIG_gst.dst_FatTable[i]), (BIG_gst.h_CLibFileHandle) ) == 1, "Error while reading file", NULL);
    /* Line 371 */ ERR_X_Error(BIG_fseek ( (BIG_gst.h_CLibFileHandle), BIG_gst.dst_FatTable[i].ul_NextPosFat - sizeof(BIG_tdst_FatDes), 0 ) == 0, "fseek error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   428c60: 55                           	pushl	%ebp
     *   428c61: 8b ec                        	movl	%esp, %ebp
     *   428c63: 83 e4 f8                     	andl	$-8, %esp
     *   428c66: b8 04 20 00 00               	movl	$8196, %eax             # imm = 0x2004
     *   428c6b: e8 10 69 30 00               	calll	0x72f580 <_SND_fn_bInitMallocSnd@0+0x6f90>
     *   428c70: a1 c0 53 ae 00               	movl	11424704, %eax
     *   428c75: 85 c0                        	testl	%eax, %eax
     *   428c77: 53                           	pushl	%ebx
     *   428c78: 56                           	pushl	%esi
     *   428c79: 57                           	pushl	%edi
     *   428c7a: 75 0a                        	jne	0x428c86 <.text+0x27c86>
     *   428c7c: 6a 02                        	pushl	$2
     *   428c7e: e8 4d 15 23 00               	calll	0x65a1d0 <_SND_fn_vSynchroTimer@0+0x16ef00>
     *   428c83: 83 c4 04                     	addl	$4, %esp
     *   428c86: 8b 15 3c 47 81 00            	movl	8472380, %edx
     *   428c8c: 8d 0c 52                     	leal	(%edx,%edx,2), %ecx
     *   428c8f: c1 e1 03                     	shll	$3, %ecx
     *   428c92: 51                           	pushl	%ecx
     *   428c93: 8b c8                        	movl	%eax, %ecx
     *   428c95: e8 a6 7b ff ff               	calll	0x420840 <.text+0x1f840>
     *   428c9a: 85 c0                        	testl	%eax, %eax
     *   428c9c: a3 64 48 81 00               	movl	%eax, 8472676
     *   428ca1: 75 20                        	jne	0x428cc3 <.text+0x27cc3>
     *   428ca3: 6a 01                        	pushl	$1
     *   428ca5: 50                           	pushl	%eax
     *   428ca6: 68 04 f9 7a 00               	pushl	$8059140                # imm = 0x7AF904
     *   428cab: 68 f0 fb 7a 00               	pushl	$8059888                # imm = 0x7AFBF0
     *   428cb0: 68 4c 01 00 00               	pushl	$332                    # imm = 0x14C
     *   428cb5: 68 a8 f9 7a 00               	pushl	$8059304                # imm = 0x7AF9A8
     *   428cba: 50                           	pushl	%eax
     *   428cbb: e8 10 78 ff ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   428cc0: 83 c4 1c                     	addl	$28, %esp
     *   428cc3: a1 3c 47 81 00               	movl	8472380, %eax
     *   428cc8: 33 ff                        	xorl	%edi, %edi
     *   428cca: 85 c0                        	testl	%eax, %eax
     *   428ccc: 0f 86 57 02 00 00            	jbe	0x428f29 <.text+0x27f29>
     *   428cd2: 33 f6                        	xorl	%esi, %esi
     *   428cd4: 8b 15 48 48 81 00            	movl	8472648, %edx
     *   428cda: a1 64 48 81 00               	movl	8472676, %eax
     *   428cdf: 52                           	pushl	%edx
     *   428ce0: 8d 0c 06                     	leal	(%esi,%eax), %ecx
     *   428ce3: 6a 18                        	pushl	$24
     *   428ce5: 51                           	pushl	%ecx
     *   428ce6: e8 b5 08 00 00               	calll	0x4295a0 <.text+0x285a0>
     *   428ceb: 83 c4 0c                     	addl	$12, %esp
     *   428cee: 83 f8 01                     	cmpl	$1, %eax
     *   428cf1: 74 22                        	je	0x428d15 <.text+0x27d15>
     *   428cf3: 6a 01                        	pushl	$1
     *   428cf5: 6a 00                        	pushl	$0
     *   428cf7: 68 cc f7 7a 00               	pushl	$8058828                # imm = 0x7AF7CC
     *   428cfc: 68 78 fb 7a 00               	pushl	$8059768                # imm = 0x7AFB78
     *   428d01: 68 5c 01 00 00               	pushl	$348                    # imm = 0x15C
     *   428d06: 68 a8 f9 7a 00               	pushl	$8059304                # imm = 0x7AF9A8
     *   428d0b: 6a 00                        	pushl	$0
     * ... (305 more instructions)
     */
}
