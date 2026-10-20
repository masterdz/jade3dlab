/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Source/PCTextureMgr.cpp
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x0066B040 - 0x0066B166 (Size: 294 bytes)
 * Assertion line 834: dwTextureNum < MaxShadows | Message: PCTextureMgr::BindTexture(): Maximum number of shadows exceeded
 * --------------------------------------------------------------------------- */
void sub_0066B040(void)
{
    /* Line 834 */ ERR_X_Error(dwTextureNum < MaxShadows, "PCTextureMgr::BindTexture(): Maximum number of shadows exceeded", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 0065e5b0 <_SND_fn_ulGetListOfSoundEventNameInGroup@12>:
     *   66b040: 8b 41 08                     	movl	8(%ecx), %eax
     *   66b043: 8b 4c 24 04                  	movl	4(%esp), %ecx
     *   66b047: 8d 0c 49                     	leal	(%ecx,%ecx,2), %ecx
     *   66b04a: 8d 14 c8                     	leal	(%eax,%ecx,8), %edx
     *   66b04d: 8b 4c 24 08                  	movl	8(%esp), %ecx
     *   66b051: 8d 0c 49                     	leal	(%ecx,%ecx,2), %ecx
     *   66b054: 8d 0c c8                     	leal	(%eax,%ecx,8), %ecx
     *   66b057: 52                           	pushl	%edx
     *   66b058: e8 43 f3 ff ff               	calll	0x66a3a0 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xbdf0>
     *   66b05d: c2 08 00                     	retl	$8
     *   66b060: 56                           	pushl	%esi
     *   66b061: 8b 74 24 0c                  	movl	12(%esp), %esi
     *   66b065: 83 fe ff                     	cmpl	$-1, %esi
     *   66b068: 57                           	pushl	%edi
     *   66b069: 8b f9                        	movl	%ecx, %edi
     *   66b06b: 0f 84 89 00 00 00            	je	0x66b0fa <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xcb4a>
     *   66b071: 53                           	pushl	%ebx
     *   66b072: 33 db                        	xorl	%ebx, %ebx
     *   66b074: 85 f6                        	testl	%esi, %esi
     *   66b076: 79 7d                        	jns	0x66b0f5 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xcb45>
     *   66b078: 81 e6 ff ff ff 7f            	andl	$2147483647, %esi       # imm = 0x7FFFFFFF
     *   66b07e: 83 fe 10                     	cmpl	$16, %esi
     *   66b081: 72 20                        	jb	0x66b0a3 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xcaf3>
     *   66b083: 6a 01                        	pushl	$1
     *   66b085: 53                           	pushl	%ebx
     *   66b086: 68 48 6d 7b 00               	pushl	$8088904                # imm = 0x7B6D48
     *   66b08b: 68 2c 6d 7b 00               	pushl	$8088876                # imm = 0x7B6D2C
     *   66b090: 68 42 03 00 00               	pushl	$834                    # imm = 0x342
     *   66b095: 68 10 6d 7b 00               	pushl	$8088848                # imm = 0x7B6D10
     *   66b09a: 53                           	pushl	%ebx
     *   66b09b: e8 30 54 db ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   66b0a0: 83 c4 1c                     	addl	$28, %esp
     *   66b0a3: 8b 4f 34                     	movl	52(%edi), %ecx
     *   66b0a6: 8d 04 76                     	leal	(%esi,%esi,2), %eax
     *   66b0a9: 8d 34 c1                     	leal	(%ecx,%eax,8), %esi
     *   66b0ac: 8b 46 08                     	movl	8(%esi), %eax
     *   66b0af: 85 c0                        	testl	%eax, %eax
     *   66b0b1: 74 26                        	je	0x66b0d9 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xcb29>
     *   66b0b3: 8b 47 18                     	movl	24(%edi), %eax
     *   66b0b6: 8b 56 0c                     	movl	12(%esi), %edx
     *   66b0b9: 8b 1c 90                     	movl	(%eax,%edx,4), %ebx
     *   66b0bc: 8d 04 90                     	leal	(%eax,%edx,4), %eax
     *   66b0bf: 8b 46 08                     	movl	8(%esi), %eax
     *   66b0c2: 85 c0                        	testl	%eax, %eax
     *   66b0c4: 74 13                        	je	0x66b0d9 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xcb29>
     *   66b0c6: 8b 46 10                     	movl	16(%esi), %eax
     *   66b0c9: 85 c0                        	testl	%eax, %eax
     *   66b0cb: 74 0c                        	je	0x66b0d9 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xcb29>
     *   66b0cd: 85 db                        	testl	%ebx, %ebx
     *   66b0cf: 74 08                        	je	0x66b0d9 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xcb29>
     *   66b0d1: 53                           	pushl	%ebx
     *   66b0d2: 8b ce                        	movl	%esi, %ecx
     *   66b0d4: e8 c7 f5 ff ff               	calll	0x66a6a0 <_SND_fn_ulGetListOfSoundEventNameInGroup@12+0xc0f0>
     *   66b0d9: 8b 16                        	movl	(%esi), %edx
     * ... (69 more instructions)
     */
}
