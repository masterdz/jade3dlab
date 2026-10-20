/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/Sdk/Sources/BIGfiles/BIGopen.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 2
 * Unique Functions Mapped: 2
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x00425A00 - 0x00425A3E (Size: 62 bytes)
 * Assertion line 229: fclose(BIG_gst.h_CLibFileHandle) == 0 | Message: fclose error
 * --------------------------------------------------------------------------- */
void BIG_Close(void)
{
    /* Line 229 */ ERR_X_Error(fclose(BIG_gst.h_CLibFileHandle) == 0, "fclose error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   425a00: e8 7b 2d 00 00               	calll	0x428780 <.text+0x27780>
     *   425a05: a1 48 48 81 00               	movl	8472648, %eax
     *   425a0a: 85 c0                        	testl	%eax, %eax
     *   425a0c: 74 2f                        	je	0x425a3d <.text+0x24a3d>
     *   425a0e: 50                           	pushl	%eax
     *   425a0f: e8 26 8b 30 00               	calll	0x72e53a <_SND_fn_bInitMallocSnd@0+0x5f4a>
     *   425a14: 83 c4 04                     	addl	$4, %esp
     *   425a17: 85 c0                        	testl	%eax, %eax
     *   425a19: 74 22                        	je	0x425a3d <.text+0x24a3d>
     *   425a1b: 6a 01                        	pushl	$1
     *   425a1d: 6a 00                        	pushl	$0
     *   425a1f: 68 1c f2 7a 00               	pushl	$8057372                # imm = 0x7AF21C
     *   425a24: 68 f4 f1 7a 00               	pushl	$8057332                # imm = 0x7AF1F4
     *   425a29: 68 e5 00 00 00               	pushl	$229
     *   425a2e: 68 c8 f1 7a 00               	pushl	$8057288                # imm = 0x7AF1C8
     *   425a33: 6a 00                        	pushl	$0
     *   425a35: e8 96 aa ff ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   425a3a: 83 c4 1c                     	addl	$28, %esp
     *   425a3d: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00425AC0 - 0x00425BFD (Size: 317 bytes)
 * Assertion line 169: (BIG_gst.h_CLibFileHandle != 0L) | Message: Unable to open file
 * --------------------------------------------------------------------------- */
void BIG_Open(void)
{
    /* Line 169 */ ERR_X_Error((BIG_gst.h_CLibFileHandle != 0L), "Unable to open file", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   425ac0: 81 ec 04 01 00 00            	subl	$260, %esp              # imm = 0x104
     *   425ac6: a1 24 87 80 00               	movl	8423204, %eax
     *   425acb: 56                           	pushl	%esi
     *   425acc: 8b b4 24 0c 01 00 00         	movl	268(%esp), %esi
     *   425ad3: 57                           	pushl	%edi
     *   425ad4: 89 84 24 08 01 00 00         	movl	%eax, 264(%esp)
     *   425adb: 33 c0                        	xorl	%eax, %eax
     *   425add: 68 68 f2 7a 00               	pushl	$8057448                # imm = 0x7AF268
     *   425ae2: b9 54 00 00 00               	movl	$84, %ecx
     *   425ae7: bf 18 47 81 00               	movl	$8472344, %edi          # imm = 0x814718
     *   425aec: 56                           	pushl	%esi
     *   425aed: f3 ab                        	rep		stosl	%eax, %es:(%edi)
     *   425aef: e8 00 8d 30 00               	calll	0x72e7f4 <_SND_fn_bInitMallocSnd@0+0x6204>
     *   425af4: 8b 3d ac 53 ae 00            	movl	11424684, %edi
     *   425afa: 83 c4 08                     	addl	$8, %esp
     *   425afd: 85 ff                        	testl	%edi, %edi
     *   425aff: a3 48 48 81 00               	movl	%eax, 8472648
     *   425b04: 75 07                        	jne	0x425b0d <.text+0x24b0d>
     *   425b06: e8 d5 3b 23 00               	calll	0x6596e0 <_SND_fn_vSynchroTimer@0+0x16e410>
     *   425b0b: 8b f8                        	movl	%eax, %edi
     *   425b0d: 68 00 01 00 00               	pushl	$256                    # imm = 0x100
     *   425b12: 8d 44 24 0c                  	leal	12(%esp), %eax
     *   425b16: 50                           	pushl	%eax
     *   425b17: 56                           	pushl	%esi
     *   425b18: 8b cf                        	movl	%edi, %ecx
     *   425b1a: e8 b1 15 23 00               	calll	0x6570d0 <_SND_fn_vSynchroTimer@0+0x16be00>
     *   425b1f: 6a 01                        	pushl	$1
     *   425b21: 8d 4c 24 0c                  	leal	12(%esp), %ecx
     *   425b25: 51                           	pushl	%ecx
     *   425b26: 8b cf                        	movl	%edi, %ecx
     *   425b28: e8 83 2a 23 00               	calll	0x6585b0 <_SND_fn_vSynchroTimer@0+0x16d2e0>
     *   425b2d: 85 c0                        	testl	%eax, %eax
     *   425b2f: a3 4c 48 81 00               	movl	%eax, 8472652
     *   425b34: 74 16                        	je	0x425b4c <.text+0x24b4c>
     *   425b36: 8b 0d 08 54 ae 00            	movl	11424776, %ecx
     *   425b3c: 68 00 00 30 00               	pushl	$3145728                # imm = 0x300000
     *   425b41: 50                           	pushl	%eax
     *   425b42: e8 b9 47 23 00               	calll	0x65a300 <_SND_fn_vSynchroTimer@0+0x16f030>
     *   425b47: a3 24 2a 9e 00               	movl	%eax, 10365476
     *   425b4c: a1 48 48 81 00               	movl	8472648, %eax
     *   425b51: 85 c0                        	testl	%eax, %eax
     *   425b53: 75 57                        	jne	0x425bac <.text+0x24bac>
     *   425b55: 6a 02                        	pushl	$2
     *   425b57: 56                           	pushl	%esi
     *   425b58: e8 bd 9a 30 00               	calll	0x72f61a <_SND_fn_bInitMallocSnd@0+0x702a>
     *   425b5d: 83 c4 08                     	addl	$8, %esp
     *   425b60: 85 c0                        	testl	%eax, %eax
     *   425b62: 74 1e                        	je	0x425b82 <.text+0x24b82>
     *   425b64: 68 80 00 00 00               	pushl	$128
     *   425b69: 56                           	pushl	%esi
     *   425b6a: e8 6a 9a 30 00               	calll	0x72f5d9 <_SND_fn_bInitMallocSnd@0+0x6fe9>
     *   425b6f: 68 64 f2 7a 00               	pushl	$8057444                # imm = 0x7AF264
     *   425b74: 56                           	pushl	%esi
     *   425b75: e8 7a 8c 30 00               	calll	0x72e7f4 <_SND_fn_bInitMallocSnd@0+0x6204>
     * ... (38 more instructions)
     */
}
