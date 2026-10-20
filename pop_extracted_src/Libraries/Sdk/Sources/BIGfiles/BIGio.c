/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/Sdk/Sources/BIGfiles/BIGio.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 3
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x00429120 - 0x00429581 (Size: 1121 bytes)
 * Assertion line 896: _i_Size <= BIG_gi_ReadSize | Message: Decompression Buffer not big enough. Need %d bytes to go through decompression.
 * Assertion line 923: BIG_si_BinFileSize != 0 | Message: 
Reached End Of Stream. Looks like a key[%08x] was not found in the stream.

 * Assertion line 963: 0 | Message: Read Buffer not big enough. Need %d bytes..
 * --------------------------------------------------------------------------- */
void BIG_SpeedMode_fread(void)
{
    /* Line 896 */ ERR_X_Error(_i_Size <= BIG_gi_ReadSize, "Decompression Buffer not big enough. Need %d bytes to go through decompression.", NULL);
    /* Line 923 */ ERR_X_Error(BIG_si_BinFileSize != 0, "
Reached End Of Stream. Looks like a key[%08x] was not found in the stream.
", NULL);
    /* Line 963 */ ERR_X_Error(0, "Read Buffer not big enough. Need %d bytes..", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   429120: 8b 0d f8 29 9e 00            	movl	10365432, %ecx
     *   429126: 83 ec 14                     	subl	$20, %esp
     *   429129: 56                           	pushl	%esi
     *   42912a: 57                           	pushl	%edi
     *   42912b: 33 ff                        	xorl	%edi, %edi
     *   42912d: 3b cf                        	cmpl	%edi, %ecx
     *   42912f: 0f 85 b2 01 00 00            	jne	0x4292e7 <.text+0x282e7>
     *   429135: b8 70 59 91 00               	movl	$9525616, %eax          # imm = 0x915970
     *   42913a: 68 00 00 02 00               	pushl	$131072                 # imm = 0x20000
     *   42913f: 50                           	pushl	%eax
     *   429140: 6a 04                        	pushl	$4
     *   429142: c7 05 f8 29 9e 00 70 59 81 00	movl	$8477040, 10365432      # imm = 0x815970
     *   42914c: a3 0c 2a 9e 00               	movl	%eax, 10365452
     *   429151: a3 f0 29 9e 00               	movl	%eax, 10365424
     *   429156: e8 55 ff ff ff               	calll	0x4290b0 <.text+0x280b0>
     *   42915b: 8b 0d 0c 2a 9e 00            	movl	10365452, %ecx
     *   429161: 8b 11                        	movl	(%ecx), %edx
     *   429163: 8b 0d 28 2a 9e 00            	movl	10365480, %ecx
     *   429169: 83 c4 0c                     	addl	$12, %esp
     *   42916c: 3b cf                        	cmpl	%edi, %ecx
     *   42916e: 89 15 1c 2a 9e 00            	movl	%edx, 10365468
     *   429174: 74 2f                        	je	0x4291a5 <.text+0x281a5>
     *   429176: 8a ca                        	movb	%dl, %cl
     *   429178: c1 ea 18                     	shrl	$24, %edx
     *   42917b: 88 15 1c 2a 9e 00            	movb	%dl, 10365468
     *   429181: 88 0d 1f 2a 9e 00            	movb	%cl, 10365471
     *   429187: 8b 0d 1c 2a 9e 00            	movl	10365468, %ecx
     *   42918d: 8b 15 1c 2a 9e 00            	movl	10365468, %edx
     *   429193: c1 e9 08                     	shrl	$8, %ecx
     *   429196: c1 ea 10                     	shrl	$16, %edx
     *   429199: 88 15 1d 2a 9e 00            	movb	%dl, 10365469
     *   42919f: 88 0d 1e 2a 9e 00            	movb	%cl, 10365470
     *   4291a5: 8b 0d 18 59 81 00            	movl	8476952, %ecx
     *   4291ab: 83 f9 ff                     	cmpl	$-1, %ecx
     *   4291ae: 74 06                        	je	0x4291b6 <.text+0x281b6>
     *   4291b0: 89 0d 1c 2a 9e 00            	movl	%ecx, 10365468
     *   4291b6: 8b 15 1c 2a 9e 00            	movl	10365468, %edx
     *   4291bc: 8b 0d 00 2a 9e 00            	movl	10365440, %ecx
     *   4291c2: 03 ca                        	addl	%edx, %ecx
     *   4291c4: 8b 15 24 2a 9e 00            	movl	10365476, %edx
     *   4291ca: 89 4a 10                     	movl	%ecx, 16(%edx)
     *   4291cd: 8b 0d 1c 2a 9e 00            	movl	10365468, %ecx
     *   4291d3: 81 f9 00 00 02 00            	cmpl	$131072, %ecx           # imm = 0x20000
     *   4291d9: ba 00 00 02 00               	movl	$131072, %edx           # imm = 0x20000
     *   4291de: 7f 02                        	jg	0x4291e2 <.text+0x281e2>
     *   4291e0: 8b d1                        	movl	%ecx, %edx
     *   4291e2: 2b ca                        	subl	%edx, %ecx
     *   4291e4: 3b cf                        	cmpl	%edi, %ecx
     *   4291e6: 89 15 10 2a 9e 00            	movl	%edx, 10365456
     *   4291ec: 7e 16                        	jle	0x429204 <.text+0x28204>
     *   4291ee: 81 f9 00 00 02 00            	cmpl	$131072, %ecx           # imm = 0x20000
     *   4291f4: 89 0d 1c 2a 9e 00            	movl	%ecx, 10365468
     *   4291fa: 7d 18                        	jge	0x429214 <.text+0x28214>
     *   4291fc: 89 0d 20 2a 9e 00            	movl	%ecx, 10365472
     * ... (248 more instructions)
     */
}
