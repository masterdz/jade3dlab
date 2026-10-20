/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/ENGine/Sources/OBJects/OBJBoundingvolume.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 15
 * Unique Functions Mapped: 2
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x00698130 - 0x00698289 (Size: 345 bytes)
 * Assertion line 195: Unknown BV type | Message: None
 * Assertion line 191: Cannot convert cylinder BV to that type. | Message: None
 * Assertion line 163: Cannot convert spherical BV to that type. | Message: None
 * Assertion line 177: Cannot convert AABBox BV to that type. | Message: None
 * --------------------------------------------------------------------------- */
void OBJ_BV_Convert(void)
{
    /* Line 195 */ ERR_X_Error(Unknown BV type, "Unknown error", NULL);
    /* Line 191 */ ERR_X_Error(Cannot convert cylinder BV to that type., "Unknown error", NULL);
    /* Line 163 */ ERR_X_Error(Cannot convert spherical BV to that type., "Unknown error", NULL);
    /* Line 177 */ ERR_X_Error(Cannot convert AABBox BV to that type., "Unknown error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   698130: 8b 44 24 08                  	movl	8(%esp), %eax
     *   698134: 83 f8 03                     	cmpl	$3, %eax
     *   698137: 0f 84 4b 01 00 00            	je	0x698288 <_SND_fn_vDisplayError@8+0x220f8>
     *   69813d: 83 e8 00                     	subl	$0, %eax
     *   698140: 0f 84 ea 00 00 00            	je	0x698230 <_SND_fn_vDisplayError@8+0x220a0>
     *   698146: 48                           	decl	%eax
     *   698147: 0f 84 84 00 00 00            	je	0x6981d1 <_SND_fn_vDisplayError@8+0x22041>
     *   69814d: 48                           	decl	%eax
     *   69814e: 74 20                        	je	0x698170 <_SND_fn_vDisplayError@8+0x21fe0>
     *   698150: 6a 01                        	pushl	$1
     *   698152: 6a 00                        	pushl	$0
     *   698154: 68 00 8c 7b 00               	pushl	$8096768                # imm = 0x7B8C00
     *   698159: 6a 00                        	pushl	$0
     *   69815b: 68 c3 00 00 00               	pushl	$195
     *   698160: 68 c8 8b 7b 00               	pushl	$8096712                # imm = 0x7B8BC8
     *   698165: 6a 00                        	pushl	$0
     *   698167: e8 64 83 d8 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   69816c: 83 c4 1c                     	addl	$28, %esp
     *   69816f: c3                           	retl
     *   698170: 8b 4c 24 04                  	movl	4(%esp), %ecx
     *   698174: 8b 41 14                     	movl	20(%ecx), %eax
     *   698177: 83 f8 ff                     	cmpl	$-1, %eax
     *   69817a: 75 07                        	jne	0x698183 <_SND_fn_vDisplayError@8+0x21ff3>
     *   69817c: b8 01 00 00 00               	movl	$1, %eax
     *   698181: eb 0e                        	jmp	0x698191 <_SND_fn_vDisplayError@8+0x22001>
     *   698183: 33 d2                        	xorl	%edx, %edx
     *   698185: 83 f8 fe                     	cmpl	$-2, %eax
     *   698188: 0f 95 c2                     	setne	%dl
     *   69818b: 4a                           	decl	%edx
     *   69818c: 83 e2 02                     	andl	$2, %edx
     *   69818f: 8b c2                        	movl	%edx, %eax
     *   698191: 83 e8 00                     	subl	$0, %eax
     *   698194: 74 31                        	je	0x6981c7 <_SND_fn_vDisplayError@8+0x22037>
     *   698196: 48                           	decl	%eax
     *   698197: 74 20                        	je	0x6981b9 <_SND_fn_vDisplayError@8+0x22029>
     *   698199: 6a 01                        	pushl	$1
     *   69819b: 6a 00                        	pushl	$0
     *   69819d: 68 9c 8b 7b 00               	pushl	$8096668                # imm = 0x7B8B9C
     *   6981a2: 6a 00                        	pushl	$0
     *   6981a4: 68 bf 00 00 00               	pushl	$191
     *   6981a9: 68 c8 8b 7b 00               	pushl	$8096712                # imm = 0x7B8BC8
     *   6981ae: 6a 00                        	pushl	$0
     *   6981b0: e8 1b 83 d8 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   6981b5: 83 c4 1c                     	addl	$28, %esp
     *   6981b8: c3                           	retl
     *   6981b9: 8b 41 0c                     	movl	12(%ecx), %eax
     *   6981bc: 89 41 10                     	movl	%eax, 16(%ecx)
     *   6981bf: c7 41 14 fe ff ff ff         	movl	$4294967294, 20(%ecx)   # imm = 0xFFFFFFFE
     *   6981c6: c3                           	retl
     *   6981c7: 51                           	pushl	%ecx
     *   6981c8: e8 73 fd ff ff               	calll	0x697f40 <_SND_fn_vDisplayError@8+0x21db0>
     *   6981cd: 83 c4 04                     	addl	$4, %esp
     *   6981d0: c3                           	retl
     *   6981d1: 8b 4c 24 04                  	movl	4(%esp), %ecx
     * ... (67 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x006986C0 - 0x006989EF (Size: 815 bytes)
 * Assertion line 642: Unknown BV type | Message: None
 * Assertion line 637: Operation not supported | Message: Modify OBJ_MergeBVs
 * Assertion line 634: \Libraries\ENGine\Sources\OBJects\OBJBoundingvolume.c | Message: None
 * Assertion line 631: \Libraries\ENGine\Sources\OBJects\OBJBoundingvolume.c | Message: None
 * Assertion line 628: \Libraries\ENGine\Sources\OBJects\OBJBoundingvolume.c | Message: None
 * Assertion line 619: Operation not supported | Message: Modify OBJ_MergeBVs
 * Assertion line 616: \Libraries\ENGine\Sources\OBJects\OBJBoundingvolume.c | Message: None
 * Assertion line 613: \Libraries\ENGine\Sources\OBJects\OBJBoundingvolume.c | Message: None
 * Assertion line 610: \Libraries\ENGine\Sources\OBJects\OBJBoundingvolume.c | Message: None
 * Assertion line 600: Operation not supported | Message: Modify OBJ_MergeBVs
 * Assertion line 576: \Libraries\ENGine\Sources\OBJects\OBJBoundingvolume.c | Message: Operation not supported
 * --------------------------------------------------------------------------- */
void OBJ_BV_Merge(void)
{
    /* Line 642 */ ERR_X_Error(Unknown BV type, "Unknown error", NULL);
    /* Line 637 */ ERR_X_Error(Operation not supported, "Modify OBJ_MergeBVs", NULL);
    /* Line 634 */ ERR_X_Error(\Libraries\ENGine\Sources\OBJects\OBJBoundingvolume.c, "Unknown error", NULL);
    /* Line 631 */ ERR_X_Error(\Libraries\ENGine\Sources\OBJects\OBJBoundingvolume.c, "Unknown error", NULL);
    /* Line 628 */ ERR_X_Error(\Libraries\ENGine\Sources\OBJects\OBJBoundingvolume.c, "Unknown error", NULL);
    /* Line 619 */ ERR_X_Error(Operation not supported, "Modify OBJ_MergeBVs", NULL);
    /* Line 616 */ ERR_X_Error(\Libraries\ENGine\Sources\OBJects\OBJBoundingvolume.c, "Unknown error", NULL);
    /* Line 613 */ ERR_X_Error(\Libraries\ENGine\Sources\OBJects\OBJBoundingvolume.c, "Unknown error", NULL);
    /* Line 610 */ ERR_X_Error(\Libraries\ENGine\Sources\OBJects\OBJBoundingvolume.c, "Unknown error", NULL);
    /* Line 600 */ ERR_X_Error(Operation not supported, "Modify OBJ_MergeBVs", NULL);
    /* Line 576 */ ERR_X_Error(\Libraries\ENGine\Sources\OBJects\OBJBoundingvolume.c, "Operation not supported", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   6986c0: 83 ec 18                     	subl	$24, %esp
     *   6986c3: 55                           	pushl	%ebp
     *   6986c4: 8b 6c 24 20                  	movl	32(%esp), %ebp
     *   6986c8: 8b 4d 10                     	movl	16(%ebp), %ecx
     *   6986cb: 8b 41 14                     	movl	20(%ecx), %eax
     *   6986ce: 83 f8 ff                     	cmpl	$-1, %eax
     *   6986d1: 75 07                        	jne	0x6986da <_SND_fn_vDisplayError@8+0x2254a>
     *   6986d3: b8 01 00 00 00               	movl	$1, %eax
     *   6986d8: eb 0e                        	jmp	0x6986e8 <_SND_fn_vDisplayError@8+0x22558>
     *   6986da: 33 d2                        	xorl	%edx, %edx
     *   6986dc: 83 f8 fe                     	cmpl	$-2, %eax
     *   6986df: 0f 95 c2                     	setne	%dl
     *   6986e2: 4a                           	decl	%edx
     *   6986e3: 83 e2 02                     	andl	$2, %edx
     *   6986e6: 8b c2                        	movl	%edx, %eax
     *   6986e8: 83 e8 00                     	subl	$0, %eax
     *   6986eb: 0f 84 70 01 00 00            	je	0x698861 <_SND_fn_vDisplayError@8+0x226d1>
     *   6986f1: 48                           	decl	%eax
     *   6986f2: 0f 84 c8 00 00 00            	je	0x6987c0 <_SND_fn_vDisplayError@8+0x22630>
     *   6986f8: 48                           	decl	%eax
     *   6986f9: 74 24                        	je	0x69871f <_SND_fn_vDisplayError@8+0x2258f>
     *   6986fb: 6a 01                        	pushl	$1
     *   6986fd: 6a 00                        	pushl	$0
     *   6986ff: 68 00 8c 7b 00               	pushl	$8096768                # imm = 0x7B8C00
     *   698704: 6a 00                        	pushl	$0
     *   698706: 68 82 02 00 00               	pushl	$642                    # imm = 0x282
     *   69870b: 68 c8 8b 7b 00               	pushl	$8096712                # imm = 0x7B8BC8
     *   698710: 6a 00                        	pushl	$0
     *   698712: e8 b9 7d d8 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   698717: 83 c4 1c                     	addl	$28, %esp
     *   69871a: 5d                           	popl	%ebp
     *   69871b: 83 c4 18                     	addl	$24, %esp
     *   69871e: c3                           	retl
     *   69871f: 8b 44 24 24                  	movl	36(%esp), %eax
     *   698723: 8b 40 10                     	movl	16(%eax), %eax
     *   698726: 8b 40 14                     	movl	20(%eax), %eax
     *   698729: 83 f8 ff                     	cmpl	$-1, %eax
     *   69872c: 75 07                        	jne	0x698735 <_SND_fn_vDisplayError@8+0x225a5>
     *   69872e: b8 01 00 00 00               	movl	$1, %eax
     *   698733: eb 0e                        	jmp	0x698743 <_SND_fn_vDisplayError@8+0x225b3>
     *   698735: 33 c9                        	xorl	%ecx, %ecx
     *   698737: 83 f8 fe                     	cmpl	$-2, %eax
     *   69873a: 0f 95 c1                     	setne	%cl
     *   69873d: 49                           	decl	%ecx
     *   69873e: 83 e1 02                     	andl	$2, %ecx
     *   698741: 8b c1                        	movl	%ecx, %eax
     *   698743: 83 e8 00                     	subl	$0, %eax
     *   698746: 6a 01                        	pushl	$1
     *   698748: 68 28 8c 7b 00               	pushl	$8096808                # imm = 0x7B8C28
     *   69874d: 68 10 8c 7b 00               	pushl	$8096784                # imm = 0x7B8C10
     *   698752: 6a 00                        	pushl	$0
     *   698754: 74 51                        	je	0x6987a7 <_SND_fn_vDisplayError@8+0x22617>
     *   698756: 48                           	decl	%eax
     *   698757: 74 35                        	je	0x69878e <_SND_fn_vDisplayError@8+0x225fe>
     * ... (224 more instructions)
     */
}
