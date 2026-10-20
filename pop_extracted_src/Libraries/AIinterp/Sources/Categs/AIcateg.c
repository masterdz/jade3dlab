/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/AIinterp/Sources/Categs/AIcateg.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 2
 * Unique Functions Mapped: 2
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x004A7970 - 0x004A799A (Size: 42 bytes)
 * Assertion line 720: 0 | Message: DEBUG
 * --------------------------------------------------------------------------- */
void sub_004A7970(void)
{
    /* Line 720 */ ERR_X_Error(0, "DEBUG", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   4a7970: 6a 01                        	pushl	$1
     *   4a7972: 68 2c 0e 7b 00               	pushl	$8064556                # imm = 0x7B0E2C
     *   4a7977: 68 24 0e 7b 00               	pushl	$8064548                # imm = 0x7B0E24
     *   4a797c: 68 b8 f2 7a 00               	pushl	$8057528                # imm = 0x7AF2B8
     *   4a7981: 68 d0 02 00 00               	pushl	$720                    # imm = 0x2D0
     *   4a7986: 68 f4 0d 7b 00               	pushl	$8064500                # imm = 0x7B0DF4
     *   4a798b: 6a 00                        	pushl	$0
     *   4a798d: e8 3e 8b f7 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4a7992: 8b 44 24 20                  	movl	32(%esp), %eax
     *   4a7996: 83 c4 1c                     	addl	$28, %esp
     *   4a7999: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x004A8000 - 0x004A81DA (Size: 474 bytes)
 * Assertion line 630: (AI_gul_SizeLocalStack + 200) < 10024 | Message: AI Engine Error: DynAIFunction:Local Dynamic stack is full
 * --------------------------------------------------------------------------- */
void sub_004A8000(void)
{
    /* Line 630 */ ERR_X_Error((AI_gul_SizeLocalStack + 200) < 10024, "AI Engine Error: DynAIFunction:Local Dynamic stack is full", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   4a8000: 83 ec 08                     	subl	$8, %esp
     *   4a8003: 55                           	pushl	%ebp
     *   4a8004: 56                           	pushl	%esi
     *   4a8005: 8b 74 24 14                  	movl	20(%esp), %esi
     *   4a8009: 0f bf 46 04                  	movswl	4(%esi), %eax
     *   4a800d: 57                           	pushl	%edi
     *   4a800e: 8b 3c 85 c0 45 a9 00         	movl	11093440(,%eax,4), %edi
     *   4a8015: e8 a6 f7 ff ff               	calll	0x4a77c0 <.text+0xa67c0>
     *   4a801a: 8b 0d 68 3b ac 00            	movl	11287400, %ecx
     *   4a8020: 8b 15 70 3b ac 00            	movl	11287408, %edx
     *   4a8026: 89 0d 6c 3b ac 00            	movl	%ecx, 11287404
     *   4a802c: 89 15 74 3b ac 00            	movl	%edx, 11287412
     *   4a8032: e8 89 f7 ff ff               	calll	0x4a77c0 <.text+0xa67c0>
     *   4a8037: a1 4c 3b ac 00               	movl	11287372, %eax
     *   4a803c: 8b 0d 50 3b ac 00            	movl	11287376, %ecx
     *   4a8042: 83 c6 08                     	addl	$8, %esi
     *   4a8045: 89 44 24 18                  	movl	%eax, 24(%esp)
     *   4a8049: 8a 46 07                     	movb	7(%esi), %al
     *   4a804c: 3c 10                        	cmpb	$16, %al
     *   4a804e: 89 4c 24 0c                  	movl	%ecx, 12(%esp)
     *   4a8052: 74 17                        	je	0x4a806b <.text+0xa706b>
     *   4a8054: 0f be d0                     	movsbl	%al, %edx
     *   4a8057: 56                           	pushl	%esi
     *   4a8058: ff 14 d5 8c b8 7f 00         	calll	*8370316(,%edx,8)
     *   4a805f: 8b f0                        	movl	%eax, %esi
     *   4a8061: 8a 46 07                     	movb	7(%esi), %al
     *   4a8064: 83 c4 04                     	addl	$4, %esp
     *   4a8067: 3c 10                        	cmpb	$16, %al
     *   4a8069: 75 e9                        	jne	0x4a8054 <.text+0xa7054>
     *   4a806b: a1 9c 3b ac 00               	movl	11287452, %eax
     *   4a8070: 8b 15 98 3b ac 00            	movl	11287448, %edx
     *   4a8076: 85 d2                        	testl	%edx, %edx
     *   4a8078: 8b 0d 48 3b ac 00            	movl	11287368, %ecx
     *   4a807e: 8b e8                        	movl	%eax, %ebp
     *   4a8080: 89 4c 24 10                  	movl	%ecx, 16(%esp)
     *   4a8084: c7 05 9c 3b ac 00 00 00 00 00	movl	$0, 11287452
     *   4a808e: 74 3c                        	je	0x4a80cc <.text+0xa70cc>
     *   4a8090: 8d 84 01 80 00 00 00         	leal	128(%ecx,%eax), %eax
     *   4a8097: a3 48 3b ac 00               	movl	%eax, 11287368
     *   4a809c: 05 c8 00 00 00               	addl	$200, %eax
     *   4a80a1: 3d 28 27 00 00               	cmpl	$10024, %eax            # imm = 0x2728
     *   4a80a6: 72 2e                        	jb	0x4a80d6 <.text+0xa70d6>
     *   4a80a8: 6a 01                        	pushl	$1
     *   4a80aa: 6a 00                        	pushl	$0
     *   4a80ac: 68 70 0e 7b 00               	pushl	$8064624                # imm = 0x7B0E70
     *   4a80b1: 68 48 0e 7b 00               	pushl	$8064584                # imm = 0x7B0E48
     *   4a80b6: 68 76 02 00 00               	pushl	$630                    # imm = 0x276
     *   4a80bb: 68 f4 0d 7b 00               	pushl	$8064500                # imm = 0x7B0DF4
     *   4a80c0: 6a 00                        	pushl	$0
     *   4a80c2: e8 09 84 f7 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4a80c7: 83 c4 1c                     	addl	$28, %esp
     *   4a80ca: eb 0a                        	jmp	0x4a80d6 <.text+0xa70d6>
     *   4a80cc: c7 05 48 3b ac 00 00 1c 00 00	movl	$7168, 11287368         # imm = 0x1C00
     *   4a80d6: a1 98 3b ac 00               	movl	11287448, %eax
     * ... (67 more instructions)
     */
}
