/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/GraphicDK/Sources/TEXture/TEXlist.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 2
 * Unique Functions Mapped: 2
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x00430470 - 0x0043056E (Size: 254 bytes)
 * Assertion line 218: (TEX_gst_GlobalTexList.l_NumberOfTextures < TEX_gst_GlobalTexList.l_NumberMaxOfTextures) | Message: Too many referenced textures, check your multi-materials for unused textures
 * --------------------------------------------------------------------------- */
void TEX_fn_vAddTexture(void)
{
    /* Line 218 */ ERR_X_Error((TEX_gst_GlobalTexList.l_NumberOfTextures < TEX_gst_GlobalTexList.l_NumberMaxOfTextures), "Too many referenced textures, check your multi-materials for unused textures", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   430470: 8b 44 24 04                  	movl	4(%esp), %eax
     *   430474: 83 f8 ff                     	cmpl	$-1, %eax
     *   430477: 75 04                        	jne	0x43047d <.text+0x2f47d>
     *   430479: 66 0b c0                     	orw	%ax, %ax
     *   43047c: c3                           	retl
     *   43047d: 53                           	pushl	%ebx
     *   43047e: 8a 5c 24 10                  	movb	16(%esp), %bl
     *   430482: 84 db                        	testb	%bl, %bl
     *   430484: 75 07                        	jne	0x43048d <.text+0x2f48d>
     *   430486: c6 05 7c 4f a7 00 01         	movb	$1, 10964860
     *   43048d: 56                           	pushl	%esi
     *   43048e: 8b 35 74 4f a7 00            	movl	10964852, %esi
     *   430494: 85 f6                        	testl	%esi, %esi
     *   430496: 74 18                        	je	0x4304b0 <.text+0x2f4b0>
     *   430498: 84 db                        	testb	%bl, %bl
     *   43049a: 75 14                        	jne	0x4304b0 <.text+0x2f4b0>
     *   43049c: 50                           	pushl	%eax
     *   43049d: e8 4e fd ff ff               	calll	0x4301f0 <.text+0x2f1f0>
     *   4304a2: 83 c4 04                     	addl	$4, %esp
     *   4304a5: 85 c0                        	testl	%eax, %eax
     *   4304a7: 74 07                        	je	0x4304b0 <.text+0x2f4b0>
     *   4304a9: 66 8b 40 0a                  	movw	10(%eax), %ax
     *   4304ad: 5e                           	popl	%esi
     *   4304ae: 5b                           	popl	%ebx
     *   4304af: c3                           	retl
     *   4304b0: 8b 15 70 4f a7 00            	movl	10964848, %edx
     *   4304b6: 3b f2                        	cmpl	%edx, %esi
     *   4304b8: 7c 28                        	jl	0x4304e2 <.text+0x2f4e2>
     *   4304ba: 6a 01                        	pushl	$1
     *   4304bc: 6a 00                        	pushl	$0
     *   4304be: 68 f0 fe 7a 00               	pushl	$8060656                # imm = 0x7AFEF0
     *   4304c3: 68 90 fe 7a 00               	pushl	$8060560                # imm = 0x7AFE90
     *   4304c8: 68 da 00 00 00               	pushl	$218
     *   4304cd: 68 5c fe 7a 00               	pushl	$8060508                # imm = 0x7AFE5C
     *   4304d2: 6a 00                        	pushl	$0
     *   4304d4: e8 f7 ff fe ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4304d9: 8b 15 70 4f a7 00            	movl	10964848, %edx
     *   4304df: 83 c4 1c                     	addl	$28, %esp
     *   4304e2: a1 80 4f a7 00               	movl	10964864, %eax
     *   4304e7: 8b 0d 78 4f a7 00            	movl	10964856, %ecx
     *   4304ed: 57                           	pushl	%edi
     *   4304ee: 8b 3d 74 4f a7 00            	movl	10964852, %edi
     *   4304f4: 47                           	incl	%edi
     *   4304f5: 8d 34 80                     	leal	(%eax,%eax,4), %esi
     *   4304f8: 89 3d 74 4f a7 00            	movl	%edi, 10964852
     *   4304fe: 8b f8                        	movl	%eax, %edi
     *   430500: 40                           	incl	%eax
     *   430501: 3b c2                        	cmpl	%edx, %eax
     *   430503: 8d 34 b1                     	leal	(%ecx,%esi,4), %esi
     *   430506: 7d 20                        	jge	0x430528 <.text+0x2f528>
     *   430508: 55                           	pushl	%ebp
     *   430509: 8d 2c 80                     	leal	(%eax,%eax,4), %ebp
     *   43050c: 8d 4c a9 0c                  	leal	12(%ecx,%ebp,4), %ecx
     *   430510: f7 01 00 00 00 20            	testl	$536870912, (%ecx)      # imm = 0x20000000
     * ... (33 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00430700 - 0x004307F2 (Size: 242 bytes)
 * Assertion line 506: (TEX_gst_GlobalTexList.l_NumberOfPalettes < TEX_gst_GlobalTexList.l_NumberMaxOfPalettes) | Message: Too many referenced textures, check your multi-materials for unused textures
 * --------------------------------------------------------------------------- */
void TEX_fn_vAddPalette(void)
{
    /* Line 506 */ ERR_X_Error((TEX_gst_GlobalTexList.l_NumberOfPalettes < TEX_gst_GlobalTexList.l_NumberMaxOfPalettes), "Too many referenced textures, check your multi-materials for unused textures", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   430700: 55                           	pushl	%ebp
     *   430701: 8b 6c 24 08                  	movl	8(%esp), %ebp
     *   430705: 83 fd ff                     	cmpl	$-1, %ebp
     *   430708: 75 05                        	jne	0x43070f <.text+0x2f70f>
     *   43070a: 66 0b c5                     	orw	%bp, %ax
     *   43070d: 5d                           	popl	%ebp
     *   43070e: c3                           	retl
     *   43070f: 56                           	pushl	%esi
     *   430710: 8b 35 8c 4f a7 00            	movl	10964876, %esi
     *   430716: 85 f6                        	testl	%esi, %esi
     *   430718: 74 1c                        	je	0x430736 <.text+0x2f736>
     *   43071a: 8a 44 24 10                  	movb	16(%esp), %al
     *   43071e: 84 c0                        	testb	%al, %al
     *   430720: 75 14                        	jne	0x430736 <.text+0x2f736>
     *   430722: 55                           	pushl	%ebp
     *   430723: e8 c8 fb ff ff               	calll	0x4302f0 <.text+0x2f2f0>
     *   430728: 83 c4 04                     	addl	$4, %esp
     *   43072b: 85 c0                        	testl	%eax, %eax
     *   43072d: 74 07                        	je	0x430736 <.text+0x2f736>
     *   43072f: 66 8b 40 0a                  	movw	10(%eax), %ax
     *   430733: 5e                           	popl	%esi
     *   430734: 5d                           	popl	%ebp
     *   430735: c3                           	retl
     *   430736: 8b 15 88 4f a7 00            	movl	10964872, %edx
     *   43073c: 3b f2                        	cmpl	%edx, %esi
     *   43073e: 7c 28                        	jl	0x430768 <.text+0x2f768>
     *   430740: 6a 01                        	pushl	$1
     *   430742: 6a 00                        	pushl	$0
     *   430744: 68 f0 fe 7a 00               	pushl	$8060656                # imm = 0x7AFEF0
     *   430749: 68 40 ff 7a 00               	pushl	$8060736                # imm = 0x7AFF40
     *   43074e: 68 fa 01 00 00               	pushl	$506                    # imm = 0x1FA
     *   430753: 68 5c fe 7a 00               	pushl	$8060508                # imm = 0x7AFE5C
     *   430758: 6a 00                        	pushl	$0
     *   43075a: e8 71 fd fe ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   43075f: 8b 15 88 4f a7 00            	movl	10964872, %edx
     *   430765: 83 c4 1c                     	addl	$28, %esp
     *   430768: a1 84 4f a7 00               	movl	10964868, %eax
     *   43076d: 8b 0d 90 4f a7 00            	movl	10964880, %ecx
     *   430773: 8b f0                        	movl	%eax, %esi
     *   430775: c1 e6 04                     	shll	$4, %esi
     *   430778: 57                           	pushl	%edi
     *   430779: 8b 3d 8c 4f a7 00            	movl	10964876, %edi
     *   43077f: 03 f1                        	addl	%ecx, %esi
     *   430781: 47                           	incl	%edi
     *   430782: 89 3d 8c 4f a7 00            	movl	%edi, 10964876
     *   430788: 8b f8                        	movl	%eax, %edi
     *   43078a: 40                           	incl	%eax
     *   43078b: 3b c2                        	cmpl	%edx, %eax
     *   43078d: 7d 29                        	jge	0x4307b8 <.text+0x2f7b8>
     *   43078f: 53                           	pushl	%ebx
     *   430790: 8b d8                        	movl	%eax, %ebx
     *   430792: c1 e3 04                     	shll	$4, %ebx
     *   430795: 8d 4c 0b 0c                  	leal	12(%ebx,%ecx), %ecx
     *   430799: 8d a4 24 00 00 00 00         	leal	(%esp), %esp
     * ... (30 more instructions)
     */
}
