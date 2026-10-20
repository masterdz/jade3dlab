/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/Sdk/Sources/BIGfiles/LOAding/LOAdefs.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 1
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x00426340 - 0x004264C2 (Size: 386 bytes)
 * Assertion line 937: 0 | Message: Key does not exists (%x)
 * --------------------------------------------------------------------------- */
void LOA_ul_SearchKeyToPos(void)
{
    /* Line 937 */ ERR_X_Error(0, "Key does not exists (%x)", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   426340: 83 ec 68                     	subl	$104, %esp
     *   426343: a1 24 87 80 00               	movl	8423204, %eax
     *   426348: 56                           	pushl	%esi
     *   426349: 68 40 59 81 00               	pushl	$8476992                # imm = 0x815940
     *   42634e: 89 44 24 6c                  	movl	%eax, 108(%esp)
     *   426352: ff 15 54 c0 7a 00            	calll	*8044628
     *   426358: 8b 0d 28 59 81 00            	movl	8476968, %ecx
     *   42635e: 8b c1                        	movl	%ecx, %eax
     *   426360: 99                           	cltd
     *   426361: be 88 13 00 00               	movl	$5000, %esi             # imm = 0x1388
     *   426366: f7 fe                        	idivl	%esi
     *   426368: 3b 15 2c 59 81 00            	cmpl	8476972, %edx
     *   42636e: 0f 84 26 01 00 00            	je	0x42649a <.text+0x2549a>
     *   426374: 53                           	pushl	%ebx
     *   426375: 57                           	pushl	%edi
     *   426376: eb 08                        	jmp	0x426380 <.text+0x25380>
     *   426378: 8d a4 24 00 00 00 00         	leal	(%esp), %esp
     *   42637f: 90                           	nop
     *   426380: 8b 15 28 87 7f 00            	movl	8357672, %edx
     *   426386: a1 2c 87 7f 00               	movl	8357676, %eax
     *   42638b: c1 e1 04                     	shll	$4, %ecx
     *   42638e: 03 ca                        	addl	%edx, %ecx
     *   426390: 8b f1                        	movl	%ecx, %esi
     *   426392: 39 06                        	cmpl	%eax, (%esi)
     *   426394: 75 02                        	jne	0x426398 <.text+0x25398>
     *   426396: 89 06                        	movl	%eax, (%esi)
     *   426398: 8b 06                        	movl	(%esi), %eax
     *   42639a: 50                           	pushl	%eax
     *   42639b: e8 a0 23 00 00               	calll	0x428740 <.text+0x27740>
     *   4263a0: 8b d8                        	movl	%eax, %ebx
     *   4263a2: 83 c4 04                     	addl	$4, %esp
     *   4263a5: 83 fb ff                     	cmpl	$-1, %ebx
     *   4263a8: 75 40                        	jne	0x4263ea <.text+0x253ea>
     *   4263aa: f6 46 0c 01                  	testb	$1, 12(%esi)
     *   4263ae: 0f 84 94 00 00 00            	je	0x426448 <.text+0x25448>
     *   4263b4: 8b 0e                        	movl	(%esi), %ecx
     *   4263b6: 51                           	pushl	%ecx
     *   4263b7: 8d 54 24 10                  	leal	16(%esp), %edx
     *   4263bb: 68 bc f2 7a 00               	pushl	$8057532                # imm = 0x7AF2BC
     *   4263c0: 52                           	pushl	%edx
     *   4263c1: e8 de 6b 30 00               	calll	0x72cfa4 <_SND_fn_bInitMallocSnd@0+0x49b4>
     *   4263c6: 6a 01                        	pushl	$1
     *   4263c8: 6a 00                        	pushl	$0
     *   4263ca: 8d 44 24 20                  	leal	32(%esp), %eax
     *   4263ce: 50                           	pushl	%eax
     *   4263cf: 68 b8 f2 7a 00               	pushl	$8057528                # imm = 0x7AF2B8
     *   4263d4: 68 a9 03 00 00               	pushl	$937                    # imm = 0x3A9
     *   4263d9: 68 84 f2 7a 00               	pushl	$8057476                # imm = 0x7AF284
     *   4263de: 6a 00                        	pushl	$0
     *   4263e0: e8 eb a0 ff ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4263e5: 83 c4 28                     	addl	$40, %esp
     *   4263e8: eb 5e                        	jmp	0x426448 <.text+0x25448>
     *   4263ea: 83 fb ff                     	cmpl	$-1, %ebx
     *   4263ed: 74 59                        	je	0x426448 <.text+0x25448>
     * ... (71 more instructions)
     */
}
