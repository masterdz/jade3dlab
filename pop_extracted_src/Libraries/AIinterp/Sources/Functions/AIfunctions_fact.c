/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/AIinterp/Sources/Functions/AIfunctions_fact.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 10
 * Unique Functions Mapped: 10
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x0046EBA0 - 0x0046EBF6 (Size: 86 bytes)
 * Assertion line 26: pst_Instance->pst_FactoryData != 0L | Message: Factory Not initialize
 * --------------------------------------------------------------------------- */
void sub_0046EBA0(void)
{
    /* Line 26 */ ERR_X_Error(pst_Instance->pst_FactoryData != 0L, "Factory Not initialize", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   46eba0: a1 68 3b ac 00               	movl	11287400, %eax
     *   46eba5: 8b 0d 70 3b ac 00            	movl	11287408, %ecx
     *   46ebab: 56                           	pushl	%esi
     *   46ebac: 8b 35 6c 3b ac 00            	movl	11287404, %esi
     *   46ebb2: a3 6c 3b ac 00               	movl	%eax, 11287404
     *   46ebb7: 89 0d 74 3b ac 00            	movl	%ecx, 11287412
     *   46ebbd: 8b 46 54                     	movl	84(%esi), %eax
     *   46ebc0: 85 c0                        	testl	%eax, %eax
     *   46ebc2: 75 1f                        	jne	0x46ebe3 <.text+0x6dbe3>
     *   46ebc4: 6a 01                        	pushl	$1
     *   46ebc6: 6a 00                        	pushl	$0
     *   46ebc8: 68 2c 0a 7b 00               	pushl	$8063532                # imm = 0x7B0A2C
     *   46ebcd: 68 08 0a 7b 00               	pushl	$8063496                # imm = 0x7B0A08
     *   46ebd2: 6a 1a                        	pushl	$26
     *   46ebd4: 68 cc 09 7b 00               	pushl	$8063436                # imm = 0x7B09CC
     *   46ebd9: 6a 00                        	pushl	$0
     *   46ebdb: e8 f0 18 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   46ebe0: 83 c4 1c                     	addl	$28, %esp
     *   46ebe3: 8b 54 24 08                  	movl	8(%esp), %edx
     *   46ebe7: 8b 46 54                     	movl	84(%esi), %eax
     *   46ebea: 52                           	pushl	%edx
     *   46ebeb: 50                           	pushl	%eax
     *   46ebec: e8 1f b0 ff ff               	calll	0x469c10 <.text+0x68c10>
     *   46ebf1: 83 c4 08                     	addl	$8, %esp
     *   46ebf4: 5e                           	popl	%esi
     *   46ebf5: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x0046EC40 - 0x0046EC96 (Size: 86 bytes)
 * Assertion line 53: pst_Instance->pst_FactoryData != 0L | Message: Factory Not initialize
 * --------------------------------------------------------------------------- */
void sub_0046EC40(void)
{
    /* Line 53 */ ERR_X_Error(pst_Instance->pst_FactoryData != 0L, "Factory Not initialize", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   46ec40: a1 68 3b ac 00               	movl	11287400, %eax
     *   46ec45: 8b 0d 70 3b ac 00            	movl	11287408, %ecx
     *   46ec4b: 56                           	pushl	%esi
     *   46ec4c: 8b 35 6c 3b ac 00            	movl	11287404, %esi
     *   46ec52: a3 6c 3b ac 00               	movl	%eax, 11287404
     *   46ec57: 89 0d 74 3b ac 00            	movl	%ecx, 11287412
     *   46ec5d: 8b 46 54                     	movl	84(%esi), %eax
     *   46ec60: 85 c0                        	testl	%eax, %eax
     *   46ec62: 75 1f                        	jne	0x46ec83 <.text+0x6dc83>
     *   46ec64: 6a 01                        	pushl	$1
     *   46ec66: 6a 00                        	pushl	$0
     *   46ec68: 68 2c 0a 7b 00               	pushl	$8063532                # imm = 0x7B0A2C
     *   46ec6d: 68 08 0a 7b 00               	pushl	$8063496                # imm = 0x7B0A08
     *   46ec72: 6a 35                        	pushl	$53
     *   46ec74: 68 cc 09 7b 00               	pushl	$8063436                # imm = 0x7B09CC
     *   46ec79: 6a 00                        	pushl	$0
     *   46ec7b: e8 50 18 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   46ec80: 83 c4 1c                     	addl	$28, %esp
     *   46ec83: 8b 54 24 08                  	movl	8(%esp), %edx
     *   46ec87: 8b 46 54                     	movl	84(%esi), %eax
     *   46ec8a: 52                           	pushl	%edx
     *   46ec8b: 50                           	pushl	%eax
     *   46ec8c: e8 ef af ff ff               	calll	0x469c80 <.text+0x68c80>
     *   46ec91: 83 c4 08                     	addl	$8, %esp
     *   46ec94: 5e                           	popl	%esi
     *   46ec95: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x0046ECE0 - 0x0046ED36 (Size: 86 bytes)
 * Assertion line 81: pst_Instance->pst_FactoryData != 0L | Message: Factory Not initialize
 * --------------------------------------------------------------------------- */
void sub_0046ECE0(void)
{
    /* Line 81 */ ERR_X_Error(pst_Instance->pst_FactoryData != 0L, "Factory Not initialize", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   46ece0: a1 68 3b ac 00               	movl	11287400, %eax
     *   46ece5: 8b 0d 70 3b ac 00            	movl	11287408, %ecx
     *   46eceb: 56                           	pushl	%esi
     *   46ecec: 8b 35 6c 3b ac 00            	movl	11287404, %esi
     *   46ecf2: a3 6c 3b ac 00               	movl	%eax, 11287404
     *   46ecf7: 89 0d 74 3b ac 00            	movl	%ecx, 11287412
     *   46ecfd: 8b 46 54                     	movl	84(%esi), %eax
     *   46ed00: 85 c0                        	testl	%eax, %eax
     *   46ed02: 75 1f                        	jne	0x46ed23 <.text+0x6dd23>
     *   46ed04: 6a 01                        	pushl	$1
     *   46ed06: 6a 00                        	pushl	$0
     *   46ed08: 68 2c 0a 7b 00               	pushl	$8063532                # imm = 0x7B0A2C
     *   46ed0d: 68 08 0a 7b 00               	pushl	$8063496                # imm = 0x7B0A08
     *   46ed12: 6a 51                        	pushl	$81
     *   46ed14: 68 cc 09 7b 00               	pushl	$8063436                # imm = 0x7B09CC
     *   46ed19: 6a 00                        	pushl	$0
     *   46ed1b: e8 b0 17 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   46ed20: 83 c4 1c                     	addl	$28, %esp
     *   46ed23: 8b 54 24 08                  	movl	8(%esp), %edx
     *   46ed27: 8b 46 54                     	movl	84(%esi), %eax
     *   46ed2a: 52                           	pushl	%edx
     *   46ed2b: 50                           	pushl	%eax
     *   46ed2c: e8 bf af ff ff               	calll	0x469cf0 <.text+0x68cf0>
     *   46ed31: 83 c4 08                     	addl	$8, %esp
     *   46ed34: 5e                           	popl	%esi
     *   46ed35: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x0046EDB0 - 0x0046EE0B (Size: 91 bytes)
 * Assertion line 108: pst_Instance->pst_FactoryData != 0L | Message: Factory Not initialize
 * --------------------------------------------------------------------------- */
void sub_0046EDB0(void)
{
    /* Line 108 */ ERR_X_Error(pst_Instance->pst_FactoryData != 0L, "Factory Not initialize", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   46edb0: a1 68 3b ac 00               	movl	11287400, %eax
     *   46edb5: 8b 0d 70 3b ac 00            	movl	11287408, %ecx
     *   46edbb: 56                           	pushl	%esi
     *   46edbc: 8b 35 6c 3b ac 00            	movl	11287404, %esi
     *   46edc2: a3 6c 3b ac 00               	movl	%eax, 11287404
     *   46edc7: 89 0d 74 3b ac 00            	movl	%ecx, 11287412
     *   46edcd: 8b 46 54                     	movl	84(%esi), %eax
     *   46edd0: 85 c0                        	testl	%eax, %eax
     *   46edd2: 75 1f                        	jne	0x46edf3 <.text+0x6ddf3>
     *   46edd4: 6a 01                        	pushl	$1
     *   46edd6: 6a 00                        	pushl	$0
     *   46edd8: 68 2c 0a 7b 00               	pushl	$8063532                # imm = 0x7B0A2C
     *   46eddd: 68 08 0a 7b 00               	pushl	$8063496                # imm = 0x7B0A08
     *   46ede2: 6a 6c                        	pushl	$108
     *   46ede4: 68 cc 09 7b 00               	pushl	$8063436                # imm = 0x7B09CC
     *   46ede9: 6a 00                        	pushl	$0
     *   46edeb: e8 e0 16 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   46edf0: 83 c4 1c                     	addl	$28, %esp
     *   46edf3: 8b 54 24 0c                  	movl	12(%esp), %edx
     *   46edf7: 8b 44 24 08                  	movl	8(%esp), %eax
     *   46edfb: 8b 4e 54                     	movl	84(%esi), %ecx
     *   46edfe: 52                           	pushl	%edx
     *   46edff: 50                           	pushl	%eax
     *   46ee00: 51                           	pushl	%ecx
     *   46ee01: e8 2a af ff ff               	calll	0x469d30 <.text+0x68d30>
     *   46ee06: 83 c4 0c                     	addl	$12, %esp
     *   46ee09: 5e                           	popl	%esi
     *   46ee0a: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x0046EE10 - 0x0046EEFE (Size: 238 bytes)
 * Assertion line 140: pst_Instance->pst_FactoryData != 0L | Message: Factory Not initialize
 * --------------------------------------------------------------------------- */
void sub_0046EE10(void)
{
    /* Line 140 */ ERR_X_Error(pst_Instance->pst_FactoryData != 0L, "Factory Not initialize", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   46ee10: a1 4c 3b ac 00               	movl	11287372, %eax
     *   46ee15: 8b 0d 50 3b ac 00            	movl	11287376, %ecx
     *   46ee1b: 83 ec 08                     	subl	$8, %esp
     *   46ee1e: 83 e8 20                     	subl	$32, %eax
     *   46ee21: 49                           	decl	%ecx
     *   46ee22: 66 83 3c cd 40 b4 aa 00 02   	cmpw	$2, 11187264(,%ecx,8)
     *   46ee2b: 75 14                        	jne	0x46ee41 <.text+0x6de41>
     *   46ee2d: d9 80 40 b5 ab 00            	flds	11253056(%eax)
     *   46ee33: dc 05 a0 1d b2 00            	faddl	11672992
     *   46ee39: dd 1c 24                     	fstpl	(%esp)
     *   46ee3c: 8b 14 24                     	movl	(%esp), %edx
     *   46ee3f: eb 06                        	jmp	0x46ee47 <.text+0x6de47>
     *   46ee41: 8b 90 40 b5 ab 00            	movl	11253056(%eax), %edx
     *   46ee47: 83 e8 20                     	subl	$32, %eax
     *   46ee4a: 49                           	decl	%ecx
     *   46ee4b: 66 83 3c cd 40 b4 aa 00 02   	cmpw	$2, 11187264(,%ecx,8)
     *   46ee54: a3 4c 3b ac 00               	movl	%eax, 11287372
     *   46ee59: 89 0d 50 3b ac 00            	movl	%ecx, 11287376
     *   46ee5f: 75 26                        	jne	0x46ee87 <.text+0x6de87>
     *   46ee61: d9 80 40 b5 ab 00            	flds	11253056(%eax)
     *   46ee67: 52                           	pushl	%edx
     *   46ee68: dc 05 a0 1d b2 00            	faddl	11672992
     *   46ee6e: dd 5c 24 04                  	fstpl	4(%esp)
     *   46ee72: 8b 44 24 04                  	movl	4(%esp), %eax
     *   46ee76: 50                           	pushl	%eax
     *   46ee77: e8 34 ff ff ff               	calll	0x46edb0 <.text+0x6ddb0>
     *   46ee7c: 8b 44 24 14                  	movl	20(%esp), %eax
     *   46ee80: 83 c0 08                     	addl	$8, %eax
     *   46ee83: 83 c4 10                     	addl	$16, %esp
     *   46ee86: c3                           	retl
     *   46ee87: 8b 80 40 b5 ab 00            	movl	11253056(%eax), %eax
     *   46ee8d: 52                           	pushl	%edx
     *   46ee8e: 50                           	pushl	%eax
     *   46ee8f: e8 1c ff ff ff               	calll	0x46edb0 <.text+0x6ddb0>
     *   46ee94: 8b 44 24 14                  	movl	20(%esp), %eax
     *   46ee98: 83 c0 08                     	addl	$8, %eax
     *   46ee9b: 83 c4 10                     	addl	$16, %esp
     *   46ee9e: c3                           	retl
     *   46ee9f: cc                           	int3
     *   46eea0: a1 68 3b ac 00               	movl	11287400, %eax
     *   46eea5: 8b 0d 70 3b ac 00            	movl	11287408, %ecx
     *   46eeab: 56                           	pushl	%esi
     *   46eeac: 8b 35 6c 3b ac 00            	movl	11287404, %esi
     *   46eeb2: a3 6c 3b ac 00               	movl	%eax, 11287404
     *   46eeb7: 89 0d 74 3b ac 00            	movl	%ecx, 11287412
     *   46eebd: 8b 46 54                     	movl	84(%esi), %eax
     *   46eec0: 85 c0                        	testl	%eax, %eax
     *   46eec2: 75 22                        	jne	0x46eee6 <.text+0x6dee6>
     *   46eec4: 6a 01                        	pushl	$1
     *   46eec6: 6a 00                        	pushl	$0
     *   46eec8: 68 2c 0a 7b 00               	pushl	$8063532                # imm = 0x7B0A2C
     *   46eecd: 68 08 0a 7b 00               	pushl	$8063496                # imm = 0x7B0A08
     *   46eed2: 68 8c 00 00 00               	pushl	$140
     *   46eed7: 68 cc 09 7b 00               	pushl	$8063436                # imm = 0x7B09CC
     * ... (13 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x0046EF00 - 0x0046EFE9 (Size: 233 bytes)
 * Assertion line 172: pst_Instance->pst_FactoryData != 0L | Message: Factory Not initialize
 * --------------------------------------------------------------------------- */
void sub_0046EF00(void)
{
    /* Line 172 */ ERR_X_Error(pst_Instance->pst_FactoryData != 0L, "Factory Not initialize", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   46ef00: a1 4c 3b ac 00               	movl	11287372, %eax
     *   46ef05: 8b 0d 50 3b ac 00            	movl	11287376, %ecx
     *   46ef0b: 83 ec 08                     	subl	$8, %esp
     *   46ef0e: 83 e8 20                     	subl	$32, %eax
     *   46ef11: 49                           	decl	%ecx
     *   46ef12: 66 83 3c cd 40 b4 aa 00 01   	cmpw	$1, 11187264(,%ecx,8)
     *   46ef1b: 75 14                        	jne	0x46ef31 <.text+0x6df31>
     *   46ef1d: db 80 40 b5 ab 00            	fildl	11253056(%eax)
     *   46ef23: d9 1c 24                     	fstps	(%esp)
     *   46ef26: d9 04 24                     	flds	(%esp)
     *   46ef29: d9 1c 24                     	fstps	(%esp)
     *   46ef2c: 8b 14 24                     	movl	(%esp), %edx
     *   46ef2f: eb 06                        	jmp	0x46ef37 <.text+0x6df37>
     *   46ef31: 8b 90 40 b5 ab 00            	movl	11253056(%eax), %edx
     *   46ef37: 83 e8 20                     	subl	$32, %eax
     *   46ef3a: 49                           	decl	%ecx
     *   46ef3b: 66 83 3c cd 40 b4 aa 00 02   	cmpw	$2, 11187264(,%ecx,8)
     *   46ef44: a3 4c 3b ac 00               	movl	%eax, 11287372
     *   46ef49: 89 0d 50 3b ac 00            	movl	%ecx, 11287376
     *   46ef4f: 75 26                        	jne	0x46ef77 <.text+0x6df77>
     *   46ef51: d9 80 40 b5 ab 00            	flds	11253056(%eax)
     *   46ef57: 52                           	pushl	%edx
     *   46ef58: dc 05 a0 1d b2 00            	faddl	11672992
     *   46ef5e: dd 5c 24 04                  	fstpl	4(%esp)
     *   46ef62: 8b 44 24 04                  	movl	4(%esp), %eax
     *   46ef66: 50                           	pushl	%eax
     *   46ef67: e8 34 ff ff ff               	calll	0x46eea0 <.text+0x6dea0>
     *   46ef6c: 8b 44 24 14                  	movl	20(%esp), %eax
     *   46ef70: 83 c0 08                     	addl	$8, %eax
     *   46ef73: 83 c4 10                     	addl	$16, %esp
     *   46ef76: c3                           	retl
     *   46ef77: 8b 80 40 b5 ab 00            	movl	11253056(%eax), %eax
     *   46ef7d: 52                           	pushl	%edx
     *   46ef7e: 50                           	pushl	%eax
     *   46ef7f: e8 1c ff ff ff               	calll	0x46eea0 <.text+0x6dea0>
     *   46ef84: 8b 44 24 14                  	movl	20(%esp), %eax
     *   46ef88: 83 c0 08                     	addl	$8, %eax
     *   46ef8b: 83 c4 10                     	addl	$16, %esp
     *   46ef8e: c3                           	retl
     *   46ef8f: cc                           	int3
     *   46ef90: a1 68 3b ac 00               	movl	11287400, %eax
     *   46ef95: 8b 0d 70 3b ac 00            	movl	11287408, %ecx
     *   46ef9b: 56                           	pushl	%esi
     *   46ef9c: 8b 35 6c 3b ac 00            	movl	11287404, %esi
     *   46efa2: a3 6c 3b ac 00               	movl	%eax, 11287404
     *   46efa7: 89 0d 74 3b ac 00            	movl	%ecx, 11287412
     *   46efad: 8b 46 54                     	movl	84(%esi), %eax
     *   46efb0: 85 c0                        	testl	%eax, %eax
     *   46efb2: 75 22                        	jne	0x46efd6 <.text+0x6dfd6>
     *   46efb4: 6a 01                        	pushl	$1
     *   46efb6: 6a 00                        	pushl	$0
     *   46efb8: 68 2c 0a 7b 00               	pushl	$8063532                # imm = 0x7B0A2C
     *   46efbd: 68 08 0a 7b 00               	pushl	$8063496                # imm = 0x7B0A08
     *   46efc2: 68 ac 00 00 00               	pushl	$172
     * ... (12 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x0046EFF0 - 0x0046F0A9 (Size: 185 bytes)
 * Assertion line 201: pst_Instance->pst_FactoryData != 0L | Message: Factory Not initialize
 * --------------------------------------------------------------------------- */
void sub_0046EFF0(void)
{
    /* Line 201 */ ERR_X_Error(pst_Instance->pst_FactoryData != 0L, "Factory Not initialize", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   46eff0: 8d 44 24 f4                  	leal	-12(%esp), %eax
     *   46eff4: 83 ec 0c                     	subl	$12, %esp
     *   46eff7: 50                           	pushl	%eax
     *   46eff8: e8 93 ff ff ff               	calll	0x46ef90 <.text+0x6df90>
     *   46effd: 8b 0d 4c 3b ac 00            	movl	11287372, %ecx
     *   46f003: 8b 54 24 04                  	movl	4(%esp), %edx
     *   46f007: 8d 81 40 b5 ab 00            	leal	11253056(%ecx), %eax
     *   46f00d: 89 10                        	movl	%edx, (%eax)
     *   46f00f: 8b 54 24 08                  	movl	8(%esp), %edx
     *   46f013: 83 c1 20                     	addl	$32, %ecx
     *   46f016: 89 50 04                     	movl	%edx, 4(%eax)
     *   46f019: 8b 54 24 0c                  	movl	12(%esp), %edx
     *   46f01d: 89 0d 4c 3b ac 00            	movl	%ecx, 11287372
     *   46f023: 8b 0d 50 3b ac 00            	movl	11287376, %ecx
     *   46f029: 89 04 cd 44 b4 aa 00         	movl	%eax, 11187268(,%ecx,8)
     *   46f030: 89 50 08                     	movl	%edx, 8(%eax)
     *   46f033: 8b 44 24 14                  	movl	20(%esp), %eax
     *   46f037: 66 c7 04 cd 40 b4 aa 00 03 00	movw	$3, 11187264(,%ecx,8)
     *   46f041: 41                           	incl	%ecx
     *   46f042: 89 0d 50 3b ac 00            	movl	%ecx, 11287376
     *   46f048: 83 c0 08                     	addl	$8, %eax
     *   46f04b: 83 c4 10                     	addl	$16, %esp
     *   46f04e: c3                           	retl
     *   46f04f: cc                           	int3
     *   46f050: a1 68 3b ac 00               	movl	11287400, %eax
     *   46f055: 8b 0d 70 3b ac 00            	movl	11287408, %ecx
     *   46f05b: 56                           	pushl	%esi
     *   46f05c: 8b 35 6c 3b ac 00            	movl	11287404, %esi
     *   46f062: a3 6c 3b ac 00               	movl	%eax, 11287404
     *   46f067: 89 0d 74 3b ac 00            	movl	%ecx, 11287412
     *   46f06d: 8b 46 54                     	movl	84(%esi), %eax
     *   46f070: 85 c0                        	testl	%eax, %eax
     *   46f072: 75 22                        	jne	0x46f096 <.text+0x6e096>
     *   46f074: 6a 01                        	pushl	$1
     *   46f076: 6a 00                        	pushl	$0
     *   46f078: 68 2c 0a 7b 00               	pushl	$8063532                # imm = 0x7B0A2C
     *   46f07d: 68 08 0a 7b 00               	pushl	$8063496                # imm = 0x7B0A08
     *   46f082: 68 c9 00 00 00               	pushl	$201
     *   46f087: 68 cc 09 7b 00               	pushl	$8063436                # imm = 0x7B09CC
     *   46f08c: 6a 00                        	pushl	$0
     *   46f08e: e8 3d 14 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   46f093: 83 c4 1c                     	addl	$28, %esp
     *   46f096: 8b 54 24 08                  	movl	8(%esp), %edx
     *   46f09a: 8b 46 54                     	movl	84(%esi), %eax
     *   46f09d: 52                           	pushl	%edx
     *   46f09e: 50                           	pushl	%eax
     *   46f09f: e8 fc ad ff ff               	calll	0x469ea0 <.text+0x68ea0>
     *   46f0a4: 83 c4 08                     	addl	$8, %esp
     *   46f0a7: 5e                           	popl	%esi
     *   46f0a8: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x0046F0B0 - 0x0046F164 (Size: 180 bytes)
 * Assertion line 232: pst_Instance->pst_FactoryData != 0L | Message: Factory Not initialize
 * --------------------------------------------------------------------------- */
void sub_0046F0B0(void)
{
    /* Line 232 */ ERR_X_Error(pst_Instance->pst_FactoryData != 0L, "Factory Not initialize", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   46f0b0: 8d 44 24 f4                  	leal	-12(%esp), %eax
     *   46f0b4: 83 ec 0c                     	subl	$12, %esp
     *   46f0b7: 50                           	pushl	%eax
     *   46f0b8: e8 93 ff ff ff               	calll	0x46f050 <.text+0x6e050>
     *   46f0bd: 8b 0d 4c 3b ac 00            	movl	11287372, %ecx
     *   46f0c3: 8b 54 24 04                  	movl	4(%esp), %edx
     *   46f0c7: 8d 81 40 b5 ab 00            	leal	11253056(%ecx), %eax
     *   46f0cd: 89 10                        	movl	%edx, (%eax)
     *   46f0cf: 8b 54 24 08                  	movl	8(%esp), %edx
     *   46f0d3: 83 c1 20                     	addl	$32, %ecx
     *   46f0d6: 89 50 04                     	movl	%edx, 4(%eax)
     *   46f0d9: 8b 54 24 0c                  	movl	12(%esp), %edx
     *   46f0dd: 89 0d 4c 3b ac 00            	movl	%ecx, 11287372
     *   46f0e3: 8b 0d 50 3b ac 00            	movl	11287376, %ecx
     *   46f0e9: 89 04 cd 44 b4 aa 00         	movl	%eax, 11187268(,%ecx,8)
     *   46f0f0: 89 50 08                     	movl	%edx, 8(%eax)
     *   46f0f3: 8b 44 24 14                  	movl	20(%esp), %eax
     *   46f0f7: 66 c7 04 cd 40 b4 aa 00 03 00	movw	$3, 11187264(,%ecx,8)
     *   46f101: 41                           	incl	%ecx
     *   46f102: 89 0d 50 3b ac 00            	movl	%ecx, 11287376
     *   46f108: 83 c0 08                     	addl	$8, %eax
     *   46f10b: 83 c4 10                     	addl	$16, %esp
     *   46f10e: c3                           	retl
     *   46f10f: cc                           	int3
     *   46f110: a1 68 3b ac 00               	movl	11287400, %eax
     *   46f115: 8b 0d 70 3b ac 00            	movl	11287408, %ecx
     *   46f11b: 56                           	pushl	%esi
     *   46f11c: 8b 35 6c 3b ac 00            	movl	11287404, %esi
     *   46f122: a3 6c 3b ac 00               	movl	%eax, 11287404
     *   46f127: 89 0d 74 3b ac 00            	movl	%ecx, 11287412
     *   46f12d: 8b 46 54                     	movl	84(%esi), %eax
     *   46f130: 85 c0                        	testl	%eax, %eax
     *   46f132: 75 22                        	jne	0x46f156 <.text+0x6e156>
     *   46f134: 6a 01                        	pushl	$1
     *   46f136: 6a 00                        	pushl	$0
     *   46f138: 68 2c 0a 7b 00               	pushl	$8063532                # imm = 0x7B0A2C
     *   46f13d: 68 08 0a 7b 00               	pushl	$8063496                # imm = 0x7B0A08
     *   46f142: 68 e8 00 00 00               	pushl	$232
     *   46f147: 68 cc 09 7b 00               	pushl	$8063436                # imm = 0x7B09CC
     *   46f14c: 6a 00                        	pushl	$0
     *   46f14e: e8 7d 13 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   46f153: 83 c4 1c                     	addl	$28, %esp
     *   46f156: 8b 56 54                     	movl	84(%esi), %edx
     *   46f159: 52                           	pushl	%edx
     *   46f15a: e8 d1 ad ff ff               	calll	0x469f30 <.text+0x68f30>
     *   46f15f: 83 c4 04                     	addl	$4, %esp
     *   46f162: 5e                           	popl	%esi
     *   46f163: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x0046F170 - 0x0046F209 (Size: 153 bytes)
 * Assertion line 259: pst_Instance->pst_FactoryData != 0L | Message: Factory Not initialize
 * --------------------------------------------------------------------------- */
void sub_0046F170(void)
{
    /* Line 259 */ ERR_X_Error(pst_Instance->pst_FactoryData != 0L, "Factory Not initialize", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   46f170: e8 9b ff ff ff               	calll	0x46f110 <.text+0x6e110>
     *   46f175: 8b 15 4c 3b ac 00            	movl	11287372, %edx
     *   46f17b: 8d 8a 40 b5 ab 00            	leal	11253056(%edx), %ecx
     *   46f181: 89 01                        	movl	%eax, (%ecx)
     *   46f183: a1 50 3b ac 00               	movl	11287376, %eax
     *   46f188: 66 c7 04 c5 40 b4 aa 00 01 00	movw	$1, 11187264(,%eax,8)
     *   46f192: 89 0c c5 44 b4 aa 00         	movl	%ecx, 11187268(,%eax,8)
     *   46f199: 83 c2 20                     	addl	$32, %edx
     *   46f19c: 40                           	incl	%eax
     *   46f19d: a3 50 3b ac 00               	movl	%eax, 11287376
     *   46f1a2: 8b 44 24 04                  	movl	4(%esp), %eax
     *   46f1a6: 89 15 4c 3b ac 00            	movl	%edx, 11287372
     *   46f1ac: 83 c0 08                     	addl	$8, %eax
     *   46f1af: c3                           	retl
     *   46f1b0: a1 68 3b ac 00               	movl	11287400, %eax
     *   46f1b5: 8b 0d 70 3b ac 00            	movl	11287408, %ecx
     *   46f1bb: 56                           	pushl	%esi
     *   46f1bc: 8b 35 6c 3b ac 00            	movl	11287404, %esi
     *   46f1c2: a3 6c 3b ac 00               	movl	%eax, 11287404
     *   46f1c7: 89 0d 74 3b ac 00            	movl	%ecx, 11287412
     *   46f1cd: 8b 46 54                     	movl	84(%esi), %eax
     *   46f1d0: 85 c0                        	testl	%eax, %eax
     *   46f1d2: 75 22                        	jne	0x46f1f6 <.text+0x6e1f6>
     *   46f1d4: 6a 01                        	pushl	$1
     *   46f1d6: 6a 00                        	pushl	$0
     *   46f1d8: 68 2c 0a 7b 00               	pushl	$8063532                # imm = 0x7B0A2C
     *   46f1dd: 68 08 0a 7b 00               	pushl	$8063496                # imm = 0x7B0A08
     *   46f1e2: 68 03 01 00 00               	pushl	$259                    # imm = 0x103
     *   46f1e7: 68 cc 09 7b 00               	pushl	$8063436                # imm = 0x7B09CC
     *   46f1ec: 6a 00                        	pushl	$0
     *   46f1ee: e8 dd 12 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   46f1f3: 83 c4 1c                     	addl	$28, %esp
     *   46f1f6: 8b 54 24 08                  	movl	8(%esp), %edx
     *   46f1fa: 8b 46 54                     	movl	84(%esi), %eax
     *   46f1fd: 52                           	pushl	%edx
     *   46f1fe: 50                           	pushl	%eax
     *   46f1ff: e8 8c ad ff ff               	calll	0x469f90 <.text+0x68f90>
     *   46f204: 83 c4 08                     	addl	$8, %esp
     *   46f207: 5e                           	popl	%esi
     *   46f208: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x0046F2A0 - 0x0046F2F9 (Size: 89 bytes)
 * Assertion line 287: pst_Instance->pst_FactoryData != 0L | Message: Factory Not initialize
 * --------------------------------------------------------------------------- */
void sub_0046F2A0(void)
{
    /* Line 287 */ ERR_X_Error(pst_Instance->pst_FactoryData != 0L, "Factory Not initialize", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   46f2a0: a1 68 3b ac 00               	movl	11287400, %eax
     *   46f2a5: 8b 0d 70 3b ac 00            	movl	11287408, %ecx
     *   46f2ab: 56                           	pushl	%esi
     *   46f2ac: 8b 35 6c 3b ac 00            	movl	11287404, %esi
     *   46f2b2: a3 6c 3b ac 00               	movl	%eax, 11287404
     *   46f2b7: 89 0d 74 3b ac 00            	movl	%ecx, 11287412
     *   46f2bd: 8b 46 54                     	movl	84(%esi), %eax
     *   46f2c0: 85 c0                        	testl	%eax, %eax
     *   46f2c2: 75 22                        	jne	0x46f2e6 <.text+0x6e2e6>
     *   46f2c4: 6a 01                        	pushl	$1
     *   46f2c6: 6a 00                        	pushl	$0
     *   46f2c8: 68 2c 0a 7b 00               	pushl	$8063532                # imm = 0x7B0A2C
     *   46f2cd: 68 08 0a 7b 00               	pushl	$8063496                # imm = 0x7B0A08
     *   46f2d2: 68 1f 01 00 00               	pushl	$287                    # imm = 0x11F
     *   46f2d7: 68 cc 09 7b 00               	pushl	$8063436                # imm = 0x7B09CC
     *   46f2dc: 6a 00                        	pushl	$0
     *   46f2de: e8 ed 11 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   46f2e3: 83 c4 1c                     	addl	$28, %esp
     *   46f2e6: 8b 54 24 08                  	movl	8(%esp), %edx
     *   46f2ea: 8b 46 54                     	movl	84(%esi), %eax
     *   46f2ed: 52                           	pushl	%edx
     *   46f2ee: 50                           	pushl	%eax
     *   46f2ef: e8 fc ac ff ff               	calll	0x469ff0 <.text+0x68ff0>
     *   46f2f4: 83 c4 08                     	addl	$8, %esp
     *   46f2f7: 5e                           	popl	%esi
     *   46f2f8: c3                           	retl
     */
}
