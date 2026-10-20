/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/ENGine/Sources/COLlision/COLMain.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 4
 * Unique Functions Mapped: 4
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x006B6CE0 - 0x006B728F (Size: 1455 bytes)
 * Assertion line 151: Cannot intersect AABBox BV with that type. | Message: None
 * --------------------------------------------------------------------------- */
void sub_006B6CE0(void)
{
    /* Line 151 */ ERR_X_Error(Cannot intersect AABBox BV with that type., "Unknown error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   6b6ce0: 83 ec 30                     	subl	$48, %esp
     *   6b6ce3: 53                           	pushl	%ebx
     *   6b6ce4: 8b 5c 24 38                  	movl	56(%esp), %ebx
     *   6b6ce8: 55                           	pushl	%ebp
     *   6b6ce9: 8b 6c 24 40                  	movl	64(%esp), %ebp
     *   6b6ced: 56                           	pushl	%esi
     *   6b6cee: 8b 75 10                     	movl	16(%ebp), %esi
     *   6b6cf1: 57                           	pushl	%edi
     *   6b6cf2: 8b 7b 10                     	movl	16(%ebx), %edi
     *   6b6cf5: 57                           	pushl	%edi
     *   6b6cf6: e8 85 11 fe ff               	calll	0x697e80 <_SND_fn_vDisplayError@8+0x21cf0>
     *   6b6cfb: 83 c4 04                     	addl	$4, %esp
     *   6b6cfe: 83 e8 00                     	subl	$0, %eax
     *   6b6d01: 0f 84 3c 03 00 00            	je	0x6b7043 <_SND_fn_vDisplayError@8+0x40eb3>
     *   6b6d07: 48                           	decl	%eax
     *   6b6d08: 0f 84 ad 01 00 00            	je	0x6b6ebb <_SND_fn_vDisplayError@8+0x40d2b>
     *   6b6d0e: 48                           	decl	%eax
     *   6b6d0f: 74 15                        	je	0x6b6d26 <_SND_fn_vDisplayError@8+0x40b96>
     *   6b6d11: 6a 01                        	pushl	$1
     *   6b6d13: 6a 00                        	pushl	$0
     *   6b6d15: 68 00 8c 7b 00               	pushl	$8096768                # imm = 0x7B8C00
     *   6b6d1a: 6a 00                        	pushl	$0
     *   6b6d1c: 68 ef 00 00 00               	pushl	$239
     *   6b6d21: e9 49 03 00 00               	jmp	0x6b706f <_SND_fn_vDisplayError@8+0x40edf>
     *   6b6d26: 56                           	pushl	%esi
     *   6b6d27: e8 54 11 fe ff               	calll	0x697e80 <_SND_fn_vDisplayError@8+0x21cf0>
     *   6b6d2c: 83 c4 04                     	addl	$4, %esp
     *   6b6d2f: 83 e8 00                     	subl	$0, %eax
     *   6b6d32: 0f 84 fb 00 00 00            	je	0x6b6e33 <_SND_fn_vDisplayError@8+0x40ca3>
     *   6b6d38: 48                           	decl	%eax
     *   6b6d39: 0f 84 88 00 00 00            	je	0x6b6dc7 <_SND_fn_vDisplayError@8+0x40c37>
     *   6b6d3f: 48                           	decl	%eax
     *   6b6d40: 74 15                        	je	0x6b6d57 <_SND_fn_vDisplayError@8+0x40bc7>
     *   6b6d42: 6a 01                        	pushl	$1
     *   6b6d44: 6a 00                        	pushl	$0
     *   6b6d46: 68 00 8f 7b 00               	pushl	$8097536                # imm = 0x7B8F00
     *   6b6d4b: 6a 00                        	pushl	$0
     *   6b6d4d: 68 ea 00 00 00               	pushl	$234
     *   6b6d52: e9 18 03 00 00               	jmp	0x6b706f <_SND_fn_vDisplayError@8+0x40edf>
     *   6b6d57: 8b 5b 0c                     	movl	12(%ebx), %ebx
     *   6b6d5a: d9 43 30                     	flds	48(%ebx)
     *   6b6d5d: 8b 6d 0c                     	movl	12(%ebp), %ebp
     *   6b6d60: d8 07                        	fadds	(%edi)
     *   6b6d62: 83 c3 30                     	addl	$48, %ebx
     *   6b6d65: 8b 46 10                     	movl	16(%esi), %eax
     *   6b6d68: 8b 4e 0c                     	movl	12(%esi), %ecx
     *   6b6d6b: d9 5c 24 28                  	fstps	40(%esp)
     *   6b6d6f: d9 43 04                     	flds	4(%ebx)
     *   6b6d72: 83 c5 30                     	addl	$48, %ebp
     *   6b6d75: d8 47 04                     	fadds	4(%edi)
     *   6b6d78: 50                           	pushl	%eax
     *   6b6d79: 8b 47 10                     	movl	16(%edi), %eax
     *   6b6d7c: 51                           	pushl	%ecx
     *   6b6d7d: 8b 4f 0c                     	movl	12(%edi), %ecx
     * ... (448 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x006B9250 - 0x006B954C (Size: 764 bytes)
 * Assertion line 2201: Unknown BV type. | Message: None
 * --------------------------------------------------------------------------- */
void sub_006B9250(void)
{
    /* Line 2201 */ ERR_X_Error(Unknown BV type., "Unknown error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   6b9250: 8b 4c 24 04                  	movl	4(%esp), %ecx
     *   6b9254: 8a 41 04                     	movb	4(%ecx), %al
     *   6b9257: 83 ec 2c                     	subl	$44, %esp
     *   6b925a: a8 01                        	testb	$1, %al
     *   6b925c: 0f 84 e4 02 00 00            	je	0x6b9546 <_SND_fn_vDisplayError@8+0x433b6>
     *   6b9262: 8b 44 24 34                  	movl	52(%esp), %eax
     *   6b9266: f6 40 04 01                  	testb	$1, 4(%eax)
     *   6b926a: 0f 84 d6 02 00 00            	je	0x6b9546 <_SND_fn_vDisplayError@8+0x433b6>
     *   6b9270: 8b 54 24 38                  	movl	56(%esp), %edx
     *   6b9274: 85 d2                        	testl	%edx, %edx
     *   6b9276: 55                           	pushl	%ebp
     *   6b9277: 56                           	pushl	%esi
     *   6b9278: 74 06                        	je	0x6b9280 <_SND_fn_vDisplayError@8+0x430f0>
     *   6b927a: 8b f0                        	movl	%eax, %esi
     *   6b927c: 8b e9                        	movl	%ecx, %ebp
     *   6b927e: eb 04                        	jmp	0x6b9284 <_SND_fn_vDisplayError@8+0x430f4>
     *   6b9280: 8b f1                        	movl	%ecx, %esi
     *   6b9282: 8b e8                        	movl	%eax, %ebp
     *   6b9284: 8b 46 10                     	movl	16(%esi), %eax
     *   6b9287: 50                           	pushl	%eax
     *   6b9288: e8 f3 eb fd ff               	calll	0x697e80 <_SND_fn_vDisplayError@8+0x21cf0>
     *   6b928d: 83 c4 04                     	addl	$4, %esp
     *   6b9290: 83 e8 00                     	subl	$0, %eax
     *   6b9293: 0f 84 a1 01 00 00            	je	0x6b943a <_SND_fn_vDisplayError@8+0x432aa>
     *   6b9299: 48                           	decl	%eax
     *   6b929a: 0f 84 f1 00 00 00            	je	0x6b9391 <_SND_fn_vDisplayError@8+0x43201>
     *   6b92a0: 48                           	decl	%eax
     *   6b92a1: 57                           	pushl	%edi
     *   6b92a2: 74 28                        	je	0x6b92cc <_SND_fn_vDisplayError@8+0x4313c>
     *   6b92a4: 6a 01                        	pushl	$1
     *   6b92a6: 6a 00                        	pushl	$0
     *   6b92a8: 68 30 8f 7b 00               	pushl	$8097584                # imm = 0x7B8F30
     *   6b92ad: 6a 00                        	pushl	$0
     *   6b92af: 68 99 08 00 00               	pushl	$2201                   # imm = 0x899
     *   6b92b4: 68 74 8e 7b 00               	pushl	$8097396                # imm = 0x7B8E74
     *   6b92b9: 6a 00                        	pushl	$0
     *   6b92bb: e8 10 72 d6 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   6b92c0: 83 c4 1c                     	addl	$28, %esp
     *   6b92c3: 5f                           	popl	%edi
     *   6b92c4: 5e                           	popl	%esi
     *   6b92c5: 33 c0                        	xorl	%eax, %eax
     *   6b92c7: 5d                           	popl	%ebp
     *   6b92c8: 83 c4 2c                     	addl	$44, %esp
     *   6b92cb: c3                           	retl
     *   6b92cc: 8b 7e 10                     	movl	16(%esi), %edi
     *   6b92cf: 8b 76 0c                     	movl	12(%esi), %esi
     *   6b92d2: d9 07                        	flds	(%edi)
     *   6b92d4: d8 46 30                     	fadds	48(%esi)
     *   6b92d7: 8b 4f 0c                     	movl	12(%edi), %ecx
     *   6b92da: 83 c6 30                     	addl	$48, %esi
     *   6b92dd: 89 4c 24 3c                  	movl	%ecx, 60(%esp)
     *   6b92e1: d9 5c 24 2c                  	fstps	44(%esp)
     *   6b92e5: d9 47 04                     	flds	4(%edi)
     *   6b92e8: d8 46 04                     	fadds	4(%esi)
     * ... (192 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x006B9550 - 0x006B98AA (Size: 858 bytes)
 * Assertion line 2310: Unknown BV type. | Message: None
 * --------------------------------------------------------------------------- */
void sub_006B9550(void)
{
    /* Line 2310 */ ERR_X_Error(Unknown BV type., "Unknown error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   6b9550: 83 ec 64                     	subl	$100, %esp
     *   6b9553: 56                           	pushl	%esi
     *   6b9554: 8b 74 24 6c                  	movl	108(%esp), %esi
     *   6b9558: 8b 46 10                     	movl	16(%esi), %eax
     *   6b955b: 57                           	pushl	%edi
     *   6b955c: 50                           	pushl	%eax
     *   6b955d: e8 1e e9 fd ff               	calll	0x697e80 <_SND_fn_vDisplayError@8+0x21cf0>
     *   6b9562: 83 c4 04                     	addl	$4, %esp
     *   6b9565: 83 e8 00                     	subl	$0, %eax
     *   6b9568: 0f 84 82 01 00 00            	je	0x6b96f0 <_SND_fn_vDisplayError@8+0x43560>
     *   6b956e: 48                           	decl	%eax
     *   6b956f: 0f 84 e6 00 00 00            	je	0x6b965b <_SND_fn_vDisplayError@8+0x434cb>
     *   6b9575: 48                           	decl	%eax
     *   6b9576: 74 27                        	je	0x6b959f <_SND_fn_vDisplayError@8+0x4340f>
     *   6b9578: 6a 01                        	pushl	$1
     *   6b957a: 6a 00                        	pushl	$0
     *   6b957c: 68 30 8f 7b 00               	pushl	$8097584                # imm = 0x7B8F30
     *   6b9581: 6a 00                        	pushl	$0
     *   6b9583: 68 06 09 00 00               	pushl	$2310                   # imm = 0x906
     *   6b9588: 68 74 8e 7b 00               	pushl	$8097396                # imm = 0x7B8E74
     *   6b958d: 6a 00                        	pushl	$0
     *   6b958f: e8 3c 6f d6 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   6b9594: 83 c4 1c                     	addl	$28, %esp
     *   6b9597: 5f                           	popl	%edi
     *   6b9598: 33 c0                        	xorl	%eax, %eax
     *   6b959a: 5e                           	popl	%esi
     *   6b959b: 83 c4 64                     	addl	$100, %esp
     *   6b959e: c3                           	retl
     *   6b959f: 8b 7e 10                     	movl	16(%esi), %edi
     *   6b95a2: 8b 76 0c                     	movl	12(%esi), %esi
     *   6b95a5: d9 07                        	flds	(%edi)
     *   6b95a7: d8 46 30                     	fadds	48(%esi)
     *   6b95aa: 8b 4f 0c                     	movl	12(%edi), %ecx
     *   6b95ad: 83 c6 30                     	addl	$48, %esi
     *   6b95b0: 89 4c 24 70                  	movl	%ecx, 112(%esp)
     *   6b95b4: d9 5c 24 1c                  	fstps	28(%esp)
     *   6b95b8: d9 47 04                     	flds	4(%edi)
     *   6b95bb: d8 46 04                     	fadds	4(%esi)
     *   6b95be: d9 5c 24 20                  	fstps	32(%esp)
     *   6b95c2: d9 47 08                     	flds	8(%edi)
     *   6b95c5: d8 46 08                     	fadds	8(%esi)
     *   6b95c8: d9 5c 24 24                  	fstps	36(%esp)
     *   6b95cc: d9 05 ac cd 7a 00            	flds	8048044
     *   6b95d2: d9 44 24 70                  	flds	112(%esp)
     *   6b95d6: da e9                        	fucompp
     *   6b95d8: df e0                        	fnstsw	%ax
     *   6b95da: f6 c4 44                     	testb	$68, %ah
     *   6b95dd: 0f 8b bf 02 00 00            	jnp	0x6b98a2 <_SND_fn_vDisplayError@8+0x43712>
     *   6b95e3: 8b 44 24 74                  	movl	116(%esp), %eax
     *   6b95e7: d9 44 24 1c                  	flds	28(%esp)
     *   6b95eb: d8 20                        	fsubs	(%eax)
     *   6b95ed: 8d 54 24 10                  	leal	16(%esp), %edx
     *   6b95f1: 52                           	pushl	%edx
     *   6b95f2: c7 44 24 1c 00 00 00 00      	movl	$0, 28(%esp)
     * ... (214 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x006B98B0 - 0x006B9BD4 (Size: 804 bytes)
 * Assertion line 2508: Unknown BV type | Message: None
 * --------------------------------------------------------------------------- */
void sub_006B98B0(void)
{
    /* Line 2508 */ ERR_X_Error(Unknown BV type, "Unknown error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00676190 <_SND_fn_vDisplayError@8>:
     *   6b98b0: 83 ec 48                     	subl	$72, %esp
     *   6b98b3: 56                           	pushl	%esi
     *   6b98b4: 8b 74 24 50                  	movl	80(%esp), %esi
     *   6b98b8: f6 46 04 01                  	testb	$1, 4(%esi)
     *   6b98bc: 0f 84 0b 03 00 00            	je	0x6b9bcd <_SND_fn_vDisplayError@8+0x43a3d>
     *   6b98c2: 8b 44 24 58                  	movl	88(%esp), %eax
     *   6b98c6: f6 40 04 01                  	testb	$1, 4(%eax)
     *   6b98ca: 0f 84 fd 02 00 00            	je	0x6b9bcd <_SND_fn_vDisplayError@8+0x43a3d>
     *   6b98d0: 8b 4c 24 5c                  	movl	92(%esp), %ecx
     *   6b98d4: 85 c9                        	testl	%ecx, %ecx
     *   6b98d6: 55                           	pushl	%ebp
     *   6b98d7: 74 04                        	je	0x6b98dd <_SND_fn_vDisplayError@8+0x4374d>
     *   6b98d9: 8b e8                        	movl	%eax, %ebp
     *   6b98db: eb 04                        	jmp	0x6b98e1 <_SND_fn_vDisplayError@8+0x43751>
     *   6b98dd: 8b ee                        	movl	%esi, %ebp
     *   6b98df: 8b f0                        	movl	%eax, %esi
     *   6b98e1: 8b 45 00                     	movl	(%ebp), %eax
     *   6b98e4: f6 c4 06                     	testb	$6, %ah
     *   6b98e7: 57                           	pushl	%edi
     *   6b98e8: 74 1a                        	je	0x6b9904 <_SND_fn_vDisplayError@8+0x43774>
     *   6b98ea: 8b 45 18                     	movl	24(%ebp), %eax
     *   6b98ed: 85 c0                        	testl	%eax, %eax
     *   6b98ef: 74 13                        	je	0x6b9904 <_SND_fn_vDisplayError@8+0x43774>
     *   6b98f1: 8b 00                        	movl	(%eax), %eax
     *   6b98f3: 85 c0                        	testl	%eax, %eax
     *   6b98f5: 74 0d                        	je	0x6b9904 <_SND_fn_vDisplayError@8+0x43774>
     *   6b98f7: 8b 78 04                     	movl	4(%eax), %edi
     *   6b98fa: 85 ff                        	testl	%edi, %edi
     *   6b98fc: 74 06                        	je	0x6b9904 <_SND_fn_vDisplayError@8+0x43774>
     *   6b98fe: 8b 07                        	movl	(%edi), %eax
     *   6b9900: 85 c0                        	testl	%eax, %eax
     *   6b9902: 75 09                        	jne	0x6b990d <_SND_fn_vDisplayError@8+0x4377d>
     *   6b9904: 5f                           	popl	%edi
     *   6b9905: 5d                           	popl	%ebp
     *   6b9906: 33 c0                        	xorl	%eax, %eax
     *   6b9908: 5e                           	popl	%esi
     *   6b9909: 83 c4 48                     	addl	$72, %esp
     *   6b990c: c3                           	retl
     *   6b990d: 0f b6 4c 24 5c               	movzbl	92(%esp), %ecx
     *   6b9912: 8b 50 08                     	movl	8(%eax), %edx
     *   6b9915: 8a 47 04                     	movb	4(%edi), %al
     *   6b9918: 53                           	pushl	%ebx
     *   6b9919: 8a 1c 11                     	movb	(%ecx,%edx), %bl
     *   6b991c: 3a d8                        	cmpb	%al, %bl
     *   6b991e: 88 5c 24 5c                  	movb	%bl, 92(%esp)
     *   6b9922: 72 0a                        	jb	0x6b992e <_SND_fn_vDisplayError@8+0x4379e>
     *   6b9924: 5b                           	popl	%ebx
     *   6b9925: 5f                           	popl	%edi
     *   6b9926: 5d                           	popl	%ebp
     *   6b9927: 33 c0                        	xorl	%eax, %eax
     *   6b9929: 5e                           	popl	%esi
     *   6b992a: 83 c4 48                     	addl	$72, %esp
     *   6b992d: c3                           	retl
     *   6b992e: 8b 44 24 5c                  	movl	92(%esp), %eax
     * ... (274 more instructions)
     */
}
