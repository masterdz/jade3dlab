/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/Sdk/Sources/BIGfiles/BIGread.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 12
 * Unique Functions Mapped: 3
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x00428160 - 0x004281E3 (Size: 131 bytes)
 * Assertion line 141: BIG_fseek((BIG_gst.h_CLibFileHandle), _ul_Pos, 0) == 0 | Message: fseek error
 * Assertion line 144: BIG_fread((UCHAR *) _p_Buffer, _ul_Length, (BIG_gst.h_CLibFileHandle)) == 1 | Message: Error while reading file
 * --------------------------------------------------------------------------- */
void BIG_ul_GetLengthFile(void)
{
    /* Line 141 */ ERR_X_Error(BIG_fseek((BIG_gst.h_CLibFileHandle), _ul_Pos, 0) == 0, "fseek error", NULL);
    /* Line 144 */ ERR_X_Error(BIG_fread((UCHAR *) _p_Buffer, _ul_Length, (BIG_gst.h_CLibFileHandle)) == 1, "Error while reading file", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   428160: 56                           	pushl	%esi
     *   428161: 8b 74 24 10                  	movl	16(%esp), %esi
     *   428165: 85 f6                        	testl	%esi, %esi
     *   428167: 74 78                        	je	0x4281e1 <.text+0x271e1>
     *   428169: 8b 44 24 08                  	movl	8(%esp), %eax
     *   42816d: 8b 0d 48 48 81 00            	movl	8472648, %ecx
     *   428173: 6a 00                        	pushl	$0
     *   428175: 50                           	pushl	%eax
     *   428176: 51                           	pushl	%ecx
     *   428177: e8 24 0f 00 00               	calll	0x4290a0 <.text+0x280a0>
     *   42817c: 83 c4 0c                     	addl	$12, %esp
     *   42817f: 85 c0                        	testl	%eax, %eax
     *   428181: 74 22                        	je	0x4281a5 <.text+0x271a5>
     *   428183: 6a 01                        	pushl	$1
     *   428185: 6a 00                        	pushl	$0
     *   428187: 68 4c f8 7a 00               	pushl	$8058956                # imm = 0x7AF84C
     *   42818c: 68 14 f8 7a 00               	pushl	$8058900                # imm = 0x7AF814
     *   428191: 68 8d 00 00 00               	pushl	$141
     *   428196: 68 e8 f7 7a 00               	pushl	$8058856                # imm = 0x7AF7E8
     *   42819b: 6a 00                        	pushl	$0
     *   42819d: e8 2e 83 ff ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4281a2: 83 c4 1c                     	addl	$28, %esp
     *   4281a5: 8b 15 48 48 81 00            	movl	8472648, %edx
     *   4281ab: 8b 44 24 0c                  	movl	12(%esp), %eax
     *   4281af: 52                           	pushl	%edx
     *   4281b0: 56                           	pushl	%esi
     *   4281b1: 50                           	pushl	%eax
     *   4281b2: e8 e9 13 00 00               	calll	0x4295a0 <.text+0x285a0>
     *   4281b7: 83 c4 0c                     	addl	$12, %esp
     *   4281ba: 83 f8 01                     	cmpl	$1, %eax
     *   4281bd: 74 22                        	je	0x4281e1 <.text+0x271e1>
     *   4281bf: 6a 01                        	pushl	$1
     *   4281c1: 6a 00                        	pushl	$0
     *   4281c3: 68 cc f7 7a 00               	pushl	$8058828                # imm = 0x7AF7CC
     *   4281c8: 68 80 f7 7a 00               	pushl	$8058752                # imm = 0x7AF780
     *   4281cd: 68 90 00 00 00               	pushl	$144
     *   4281d2: 68 e8 f7 7a 00               	pushl	$8058856                # imm = 0x7AF7E8
     *   4281d7: 6a 00                        	pushl	$0
     *   4281d9: e8 f2 82 ff ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4281de: 83 c4 1c                     	addl	$28, %esp
     *   4281e1: 5e                           	popl	%esi
     *   4281e2: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00428240 - 0x0042834F (Size: 271 bytes)
 * Assertion line 87: BIG_fseek((BIG_gst.h_CLibFileHandle), _ul_Pos, 0) == 0 | Message: fseek error
 * Assertion line 98: BIG_fread((UCHAR *) &ul_Length, sizeof(ULONG), (BIG_gst.h_CLibFileHandle)) == 1 | Message: Error while reading file
 * Assertion line 336: BIG_fseek((BIG_gst.h_CLibFileHandle), _ul_Pos, 0) == 0 | Message: fseek error
 * Assertion line 342: BIG_fread((UCHAR *) &ul_Length, sizeof(ULONG), (BIG_gst.h_CLibFileHandle)) == 1 | Message: Error while reading file
 * Assertion line 358: p_Buffer != 0L | Message: Not enough memory
 * Assertion line 361: BIG_fread((UCHAR *) p_Buffer, ul_Length, (BIG_gst.h_CLibFileHandle)) == 1 | Message: Error while reading file
 * --------------------------------------------------------------------------- */
void BIG_pc_ReadFileTmp(void)
{
    /* Line 87 */ ERR_X_Error(BIG_fseek((BIG_gst.h_CLibFileHandle), _ul_Pos, 0) == 0, "fseek error", NULL);
    /* Line 98 */ ERR_X_Error(BIG_fread((UCHAR *) &ul_Length, sizeof(ULONG), (BIG_gst.h_CLibFileHandle)) == 1, "Error while reading file", NULL);
    /* Line 336 */ ERR_X_Error(BIG_fseek((BIG_gst.h_CLibFileHandle), _ul_Pos, 0) == 0, "fseek error", NULL);
    /* Line 342 */ ERR_X_Error(BIG_fread((UCHAR *) &ul_Length, sizeof(ULONG), (BIG_gst.h_CLibFileHandle)) == 1, "Error while reading file", NULL);
    /* Line 358 */ ERR_X_Error(p_Buffer != 0L, "Not enough memory", NULL);
    /* Line 361 */ ERR_X_Error(BIG_fread((UCHAR *) p_Buffer, ul_Length, (BIG_gst.h_CLibFileHandle)) == 1, "Error while reading file", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   428240: 51                           	pushl	%ecx
     *   428241: 83 3d f4 29 9e 00 02         	cmpl	$2, 10365428
     *   428248: 74 39                        	je	0x428283 <.text+0x27283>
     *   42824a: 8b 44 24 08                  	movl	8(%esp), %eax
     *   42824e: 8b 0d 48 48 81 00            	movl	8472648, %ecx
     *   428254: 6a 00                        	pushl	$0
     *   428256: 50                           	pushl	%eax
     *   428257: 51                           	pushl	%ecx
     *   428258: e8 43 0e 00 00               	calll	0x4290a0 <.text+0x280a0>
     *   42825d: 83 c4 0c                     	addl	$12, %esp
     *   428260: 85 c0                        	testl	%eax, %eax
     *   428262: 74 1f                        	je	0x428283 <.text+0x27283>
     *   428264: 6a 01                        	pushl	$1
     *   428266: 6a 00                        	pushl	$0
     *   428268: 68 4c f8 7a 00               	pushl	$8058956                # imm = 0x7AF84C
     *   42826d: 68 14 f8 7a 00               	pushl	$8058900                # imm = 0x7AF814
     *   428272: 6a 57                        	pushl	$87
     *   428274: 68 e8 f7 7a 00               	pushl	$8058856                # imm = 0x7AF7E8
     *   428279: 6a 00                        	pushl	$0
     *   42827b: e8 50 82 ff ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   428280: 83 c4 1c                     	addl	$28, %esp
     *   428283: a1 30 59 81 00               	movl	8476976, %eax
     *   428288: 85 c0                        	testl	%eax, %eax
     *   42828a: 74 09                        	je	0x428295 <.text+0x27295>
     *   42828c: 83 3d f4 29 9e 00 02         	cmpl	$2, 10365428
     *   428293: 74 61                        	je	0x4282f6 <.text+0x272f6>
     *   428295: 8b 15 48 48 81 00            	movl	8472648, %edx
     *   42829b: 52                           	pushl	%edx
     *   42829c: 8d 44 24 04                  	leal	4(%esp), %eax
     *   4282a0: 6a 04                        	pushl	$4
     *   4282a2: 50                           	pushl	%eax
     *   4282a3: e8 f8 12 00 00               	calll	0x4295a0 <.text+0x285a0>
     *   4282a8: 83 c4 0c                     	addl	$12, %esp
     *   4282ab: 83 f8 01                     	cmpl	$1, %eax
     *   4282ae: 74 1f                        	je	0x4282cf <.text+0x272cf>
     *   4282b0: 6a 01                        	pushl	$1
     *   4282b2: 6a 00                        	pushl	$0
     *   4282b4: 68 cc f7 7a 00               	pushl	$8058828                # imm = 0x7AF7CC
     *   4282b9: 68 58 f8 7a 00               	pushl	$8058968                # imm = 0x7AF858
     *   4282be: 6a 62                        	pushl	$98
     *   4282c0: 68 e8 f7 7a 00               	pushl	$8058856                # imm = 0x7AF7E8
     *   4282c5: 6a 00                        	pushl	$0
     *   4282c7: e8 04 82 ff ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4282cc: 83 c4 1c                     	addl	$28, %esp
     *   4282cf: a1 28 2a 9e 00               	movl	10365480, %eax
     *   4282d4: 85 c0                        	testl	%eax, %eax
     *   4282d6: 74 1e                        	je	0x4282f6 <.text+0x272f6>
     *   4282d8: 8a 04 24                     	movb	(%esp), %al
     *   4282db: 8a 4c 24 03                  	movb	3(%esp), %cl
     *   4282df: 8a 54 24 02                  	movb	2(%esp), %dl
     *   4282e3: 88 44 24 03                  	movb	%al, 3(%esp)
     *   4282e7: 8a 44 24 01                  	movb	1(%esp), %al
     *   4282eb: 88 0c 24                     	movb	%cl, (%esp)
     *   4282ee: 88 54 24 01                  	movb	%dl, 1(%esp)
     * ... (29 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x004284E0 - 0x00428718 (Size: 568 bytes)
 * Assertion line 254: BIG_fseek((BIG_gst.h_CLibFileHandle), _ul_Pos, 0) == 0 | Message: fseek error
 * Assertion line 260: BIG_fread(p_Buffer, sizeof(ULONG), (BIG_gst.h_CLibFileHandle)) == 1 | Message: Error while reading file
 * Assertion line 280: p_Buffer != 0L | Message: Not enough memory
 * Assertion line 285: BIG_fread((UCHAR *) p_Buffer, ul_Length, (BIG_gst.h_CLibFileHandle)) == 1 | Message: Error while reading file
 * --------------------------------------------------------------------------- */
void BIG_ul_ReadFile(void)
{
    /* Line 254 */ ERR_X_Error(BIG_fseek((BIG_gst.h_CLibFileHandle), _ul_Pos, 0) == 0, "fseek error", NULL);
    /* Line 260 */ ERR_X_Error(BIG_fread(p_Buffer, sizeof(ULONG), (BIG_gst.h_CLibFileHandle)) == 1, "Error while reading file", NULL);
    /* Line 280 */ ERR_X_Error(p_Buffer != 0L, "Not enough memory", NULL);
    /* Line 285 */ ERR_X_Error(BIG_fread((UCHAR *) p_Buffer, ul_Length, (BIG_gst.h_CLibFileHandle)) == 1, "Error while reading file", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   4284e0: 8b 44 24 04                  	movl	4(%esp), %eax
     *   4284e4: 3b 05 68 59 81 00            	cmpl	8477032, %eax
     *   4284ea: 7e 5e                        	jle	0x42854a <.text+0x2754a>
     *   4284ec: a3 68 59 81 00               	movl	%eax, 8477032
     *   4284f1: a1 64 59 81 00               	movl	8477028, %eax
     *   4284f6: 85 c0                        	testl	%eax, %eax
     *   4284f8: a1 c0 53 ae 00               	movl	11424704, %eax
     *   4284fd: 74 29                        	je	0x428528 <.text+0x27528>
     *   4284ff: 85 c0                        	testl	%eax, %eax
     *   428501: 75 0a                        	jne	0x42850d <.text+0x2750d>
     *   428503: 6a 02                        	pushl	$2
     *   428505: e8 c6 1c 23 00               	calll	0x65a1d0 <_SND_fn_vSynchroTimer@0+0x16ef00>
     *   42850a: 83 c4 04                     	addl	$4, %esp
     *   42850d: 8b 0d 68 59 81 00            	movl	8477032, %ecx
     *   428513: 8b 15 64 59 81 00            	movl	8477028, %edx
     *   428519: 51                           	pushl	%ecx
     *   42851a: 52                           	pushl	%edx
     *   42851b: 8b c8                        	movl	%eax, %ecx
     *   42851d: e8 6e d2 ff ff               	calll	0x425790 <.text+0x24790>
     *   428522: a3 64 59 81 00               	movl	%eax, 8477028
     *   428527: c3                           	retl
     *   428528: 85 c0                        	testl	%eax, %eax
     *   42852a: 75 0a                        	jne	0x428536 <.text+0x27536>
     *   42852c: 6a 02                        	pushl	$2
     *   42852e: e8 9d 1c 23 00               	calll	0x65a1d0 <_SND_fn_vSynchroTimer@0+0x16ef00>
     *   428533: 83 c4 04                     	addl	$4, %esp
     *   428536: 8b 0d 68 59 81 00            	movl	8477032, %ecx
     *   42853c: 51                           	pushl	%ecx
     *   42853d: 8b c8                        	movl	%eax, %ecx
     *   42853f: e8 fc 82 ff ff               	calll	0x420840 <.text+0x1f840>
     *   428544: a3 64 59 81 00               	movl	%eax, 8477028
     *   428549: c3                           	retl
     *   42854a: a1 64 59 81 00               	movl	8477028, %eax
     *   42854f: c3                           	retl
     *   428550: 51                           	pushl	%ecx
     *   428551: 83 3d f4 29 9e 00 02         	cmpl	$2, 10365428
     *   428558: 55                           	pushl	%ebp
     *   428559: 56                           	pushl	%esi
     *   42855a: 57                           	pushl	%edi
     *   42855b: 75 1c                        	jne	0x428579 <.text+0x27579>
     *   42855d: 8b 44 24 18                  	movl	24(%esp), %eax
     *   428561: 50                           	pushl	%eax
     *   428562: e8 59 1f 00 00               	calll	0x42a4c0 <.text+0x294c0>
     *   428567: 83 c4 04                     	addl	$4, %esp
     *   42856a: 85 c0                        	testl	%eax, %eax
     *   42856c: 75 06                        	jne	0x428574 <.text+0x27574>
     *   42856e: 8b 7c 24 0c                  	movl	12(%esp), %edi
     *   428572: 8b c7                        	movl	%edi, %eax
     *   428574: 5f                           	popl	%edi
     *   428575: 5e                           	popl	%esi
     *   428576: 5d                           	popl	%ebp
     *   428577: 59                           	popl	%ecx
     *   428578: c3                           	retl
     *   428579: 8b 4c 24 14                  	movl	20(%esp), %ecx
     * ... (137 more instructions)
     */
}
