/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/AIinterp/Sources/Functions/AIfunctions_grid.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 20
 * Unique Functions Mapped: 18
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x00487C90 - 0x00487DF4 (Size: 356 bytes)
 * Assertion line 104: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_00487C90(void)
{
    /* Line 104 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   487c90: a1 4c 3b ac 00               	movl	11287372, %eax
     *   487c95: 8b 0d 50 3b ac 00            	movl	11287376, %ecx
     *   487c9b: 83 e8 20                     	subl	$32, %eax
     *   487c9e: 83 ec 08                     	subl	$8, %esp
     *   487ca1: 49                           	decl	%ecx
     *   487ca2: 66 83 3c cd 40 b4 aa 00 02   	cmpw	$2, 11187264(,%ecx,8)
     *   487cab: a3 4c 3b ac 00               	movl	%eax, 11287372
     *   487cb0: 89 0d 50 3b ac 00            	movl	%ecx, 11287376
     *   487cb6: 75 22                        	jne	0x487cda <.text+0x86cda>
     *   487cb8: d9 80 40 b5 ab 00            	flds	11253056(%eax)
     *   487cbe: dc 05 a0 1d b2 00            	faddl	11672992
     *   487cc4: dd 1c 24                     	fstpl	(%esp)
     *   487cc7: 8b 04 24                     	movl	(%esp), %eax
     *   487cca: a3 44 e9 af 00               	movl	%eax, 11528516
     *   487ccf: 8b 44 24 0c                  	movl	12(%esp), %eax
     *   487cd3: 83 c0 08                     	addl	$8, %eax
     *   487cd6: 83 c4 08                     	addl	$8, %esp
     *   487cd9: c3                           	retl
     *   487cda: 8b 80 40 b5 ab 00            	movl	11253056(%eax), %eax
     *   487ce0: a3 44 e9 af 00               	movl	%eax, 11528516
     *   487ce5: 8b 44 24 0c                  	movl	12(%esp), %eax
     *   487ce9: 83 c0 08                     	addl	$8, %eax
     *   487cec: 83 c4 08                     	addl	$8, %esp
     *   487cef: c3                           	retl
     *   487cf0: a1 4c 3b ac 00               	movl	11287372, %eax
     *   487cf5: 8b 0d 50 3b ac 00            	movl	11287376, %ecx
     *   487cfb: 83 e8 20                     	subl	$32, %eax
     *   487cfe: 83 ec 08                     	subl	$8, %esp
     *   487d01: 49                           	decl	%ecx
     *   487d02: 66 83 3c cd 40 b4 aa 00 02   	cmpw	$2, 11187264(,%ecx,8)
     *   487d0b: a3 4c 3b ac 00               	movl	%eax, 11287372
     *   487d10: 89 0d 50 3b ac 00            	movl	%ecx, 11287376
     *   487d16: 75 22                        	jne	0x487d3a <.text+0x86d3a>
     *   487d18: d9 80 40 b5 ab 00            	flds	11253056(%eax)
     *   487d1e: dc 05 a0 1d b2 00            	faddl	11672992
     *   487d24: dd 1c 24                     	fstpl	(%esp)
     *   487d27: 8b 04 24                     	movl	(%esp), %eax
     *   487d2a: a3 a8 8e ac 00               	movl	%eax, 11308712
     *   487d2f: 8b 44 24 0c                  	movl	12(%esp), %eax
     *   487d33: 83 c0 08                     	addl	$8, %eax
     *   487d36: 83 c4 08                     	addl	$8, %esp
     *   487d39: c3                           	retl
     *   487d3a: 8b 80 40 b5 ab 00            	movl	11253056(%eax), %eax
     *   487d40: a3 a8 8e ac 00               	movl	%eax, 11308712
     *   487d45: 8b 44 24 0c                  	movl	12(%esp), %eax
     *   487d49: 83 c0 08                     	addl	$8, %eax
     *   487d4c: 83 c4 08                     	addl	$8, %esp
     *   487d4f: c3                           	retl
     *   487d50: a1 4c 3b ac 00               	movl	11287372, %eax
     *   487d55: 8b 0d 50 3b ac 00            	movl	11287376, %ecx
     *   487d5b: 83 e8 20                     	subl	$32, %eax
     *   487d5e: 83 ec 08                     	subl	$8, %esp
     *   487d61: 49                           	decl	%ecx
     *   487d62: 66 83 3c cd 40 b4 aa 00 02   	cmpw	$2, 11187264(,%ecx,8)
     * ... (45 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00487E00 - 0x00487ECA (Size: 202 bytes)
 * Assertion line 104: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_00487E00(void)
{
    /* Line 104 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   487e00: a1 70 3b ac 00               	movl	11287408, %eax
     *   487e05: 8b 0d 68 3b ac 00            	movl	11287400, %ecx
     *   487e0b: a3 74 3b ac 00               	movl	%eax, 11287412
     *   487e10: a1 4c 3b ac 00               	movl	11287372, %eax
     *   487e15: 83 ec 0c                     	subl	$12, %esp
     *   487e18: 89 0d 6c 3b ac 00            	movl	%ecx, 11287404
     *   487e1e: 8b 0d 50 3b ac 00            	movl	11287376, %ecx
     *   487e24: 83 e8 20                     	subl	$32, %eax
     *   487e27: 49                           	decl	%ecx
     *   487e28: 66 83 3c cd 40 b4 aa 00 02   	cmpw	$2, 11187264(,%ecx,8)
     *   487e31: 56                           	pushl	%esi
     *   487e32: 57                           	pushl	%edi
     *   487e33: 75 16                        	jne	0x487e4b <.text+0x86e4b>
     *   487e35: d9 80 40 b5 ab 00            	flds	11253056(%eax)
     *   487e3b: dc 05 a0 1d b2 00            	faddl	11672992
     *   487e41: dd 5c 24 08                  	fstpl	8(%esp)
     *   487e45: 8b 7c 24 08                  	movl	8(%esp), %edi
     *   487e49: eb 06                        	jmp	0x487e51 <.text+0x86e51>
     *   487e4b: 8b b8 40 b5 ab 00            	movl	11253056(%eax), %edi
     *   487e51: 8b 90 20 b5 ab 00            	movl	11253024(%eax), %edx
     *   487e57: 83 e8 20                     	subl	$32, %eax
     *   487e5a: 49                           	decl	%ecx
     *   487e5b: 89 0d 50 3b ac 00            	movl	%ecx, 11287376
     *   487e61: 8b 88 44 b5 ab 00            	movl	11253060(%eax), %ecx
     *   487e67: 89 54 24 08                  	movl	%edx, 8(%esp)
     *   487e6b: 8b 90 48 b5 ab 00            	movl	11253064(%eax), %edx
     *   487e71: a3 4c 3b ac 00               	movl	%eax, 11287372
     *   487e76: 8d 44 24 08                  	leal	8(%esp), %eax
     *   487e7a: 50                           	pushl	%eax
     *   487e7b: 89 4c 24 10                  	movl	%ecx, 16(%esp)
     *   487e7f: 89 54 24 14                  	movl	%edx, 20(%esp)
     *   487e83: e8 b8 df 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   487e88: 8b f0                        	movl	%eax, %esi
     *   487e8a: 83 c4 04                     	addl	$4, %esp
     *   487e8d: 85 f6                        	testl	%esi, %esi
     *   487e8f: 75 1d                        	jne	0x487eae <.text+0x86eae>
     *   487e91: 6a 01                        	pushl	$1
     *   487e93: 50                           	pushl	%eax
     *   487e94: 68 64 0b 7b 00               	pushl	$8063844                # imm = 0x7B0B64
     *   487e99: 68 58 0b 7b 00               	pushl	$8063832                # imm = 0x7B0B58
     *   487e9e: 6a 6a                        	pushl	$106
     *   487ea0: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   487ea5: 50                           	pushl	%eax
     *   487ea6: e8 25 86 f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   487eab: 83 c4 1c                     	addl	$28, %esp
     *   487eae: 57                           	pushl	%edi
     *   487eaf: 8d 4c 24 0c                  	leal	12(%esp), %ecx
     *   487eb3: 51                           	pushl	%ecx
     *   487eb4: 56                           	pushl	%esi
     *   487eb5: e8 16 d4 23 00               	calll	0x6c52d0 <_SND_fn_vDisplayError@8+0x4f140>
     *   487eba: 8b 44 24 24                  	movl	36(%esp), %eax
     *   487ebe: 83 c4 0c                     	addl	$12, %esp
     *   487ec1: 5f                           	popl	%edi
     *   487ec2: 83 c0 08                     	addl	$8, %eax
     * ... (3 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00487ED0 - 0x00487F17 (Size: 71 bytes)
 * Assertion line 142: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_00487ED0(void)
{
    /* Line 142 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   487ed0: 56                           	pushl	%esi
     *   487ed1: 57                           	pushl	%edi
     *   487ed2: 8b 7c 24 10                  	movl	16(%esp), %edi
     *   487ed6: 57                           	pushl	%edi
     *   487ed7: e8 64 df 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   487edc: 8b f0                        	movl	%eax, %esi
     *   487ede: 83 c4 04                     	addl	$4, %esp
     *   487ee1: 85 f6                        	testl	%esi, %esi
     *   487ee3: 75 20                        	jne	0x487f05 <.text+0x86f05>
     *   487ee5: 6a 01                        	pushl	$1
     *   487ee7: 50                           	pushl	%eax
     *   487ee8: 68 64 0b 7b 00               	pushl	$8063844                # imm = 0x7B0B64
     *   487eed: 68 58 0b 7b 00               	pushl	$8063832                # imm = 0x7B0B58
     *   487ef2: 68 8e 00 00 00               	pushl	$142
     *   487ef7: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   487efc: 50                           	pushl	%eax
     *   487efd: e8 ce 85 f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   487f02: 83 c4 1c                     	addl	$28, %esp
     *   487f05: 8b 44 24 14                  	movl	20(%esp), %eax
     *   487f09: 50                           	pushl	%eax
     *   487f0a: 57                           	pushl	%edi
     *   487f0b: 56                           	pushl	%esi
     *   487f0c: e8 3f d4 23 00               	calll	0x6c5350 <_SND_fn_vDisplayError@8+0x4f1c0>
     *   487f11: 83 c4 0c                     	addl	$12, %esp
     *   487f14: 5f                           	popl	%edi
     *   487f15: 5e                           	popl	%esi
     *   487f16: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00487F20 - 0x00487FED (Size: 205 bytes)
 * Assertion line 142: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_00487F20(void)
{
    /* Line 142 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   487f20: a1 70 3b ac 00               	movl	11287408, %eax
     *   487f25: 8b 0d 68 3b ac 00            	movl	11287400, %ecx
     *   487f2b: a3 74 3b ac 00               	movl	%eax, 11287412
     *   487f30: a1 4c 3b ac 00               	movl	11287372, %eax
     *   487f35: 83 ec 0c                     	subl	$12, %esp
     *   487f38: 89 0d 6c 3b ac 00            	movl	%ecx, 11287404
     *   487f3e: 8b 0d 50 3b ac 00            	movl	11287376, %ecx
     *   487f44: 83 e8 20                     	subl	$32, %eax
     *   487f47: 49                           	decl	%ecx
     *   487f48: 66 83 3c cd 40 b4 aa 00 02   	cmpw	$2, 11187264(,%ecx,8)
     *   487f51: 56                           	pushl	%esi
     *   487f52: 57                           	pushl	%edi
     *   487f53: 75 16                        	jne	0x487f6b <.text+0x86f6b>
     *   487f55: d9 80 40 b5 ab 00            	flds	11253056(%eax)
     *   487f5b: dc 05 a0 1d b2 00            	faddl	11672992
     *   487f61: dd 5c 24 08                  	fstpl	8(%esp)
     *   487f65: 8b 7c 24 08                  	movl	8(%esp), %edi
     *   487f69: eb 06                        	jmp	0x487f71 <.text+0x86f71>
     *   487f6b: 8b b8 40 b5 ab 00            	movl	11253056(%eax), %edi
     *   487f71: 8b 90 20 b5 ab 00            	movl	11253024(%eax), %edx
     *   487f77: 83 e8 20                     	subl	$32, %eax
     *   487f7a: 49                           	decl	%ecx
     *   487f7b: 89 0d 50 3b ac 00            	movl	%ecx, 11287376
     *   487f81: 8b 88 44 b5 ab 00            	movl	11253060(%eax), %ecx
     *   487f87: 89 54 24 08                  	movl	%edx, 8(%esp)
     *   487f8b: 8b 90 48 b5 ab 00            	movl	11253064(%eax), %edx
     *   487f91: a3 4c 3b ac 00               	movl	%eax, 11287372
     *   487f96: 8d 44 24 08                  	leal	8(%esp), %eax
     *   487f9a: 50                           	pushl	%eax
     *   487f9b: 89 4c 24 10                  	movl	%ecx, 16(%esp)
     *   487f9f: 89 54 24 14                  	movl	%edx, 20(%esp)
     *   487fa3: e8 98 de 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   487fa8: 8b f0                        	movl	%eax, %esi
     *   487faa: 83 c4 04                     	addl	$4, %esp
     *   487fad: 85 f6                        	testl	%esi, %esi
     *   487faf: 75 20                        	jne	0x487fd1 <.text+0x86fd1>
     *   487fb1: 6a 01                        	pushl	$1
     *   487fb3: 50                           	pushl	%eax
     *   487fb4: 68 64 0b 7b 00               	pushl	$8063844                # imm = 0x7B0B64
     *   487fb9: 68 58 0b 7b 00               	pushl	$8063832                # imm = 0x7B0B58
     *   487fbe: 68 8e 00 00 00               	pushl	$142
     *   487fc3: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   487fc8: 50                           	pushl	%eax
     *   487fc9: e8 02 85 f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   487fce: 83 c4 1c                     	addl	$28, %esp
     *   487fd1: 57                           	pushl	%edi
     *   487fd2: 8d 4c 24 0c                  	leal	12(%esp), %ecx
     *   487fd6: 51                           	pushl	%ecx
     *   487fd7: 56                           	pushl	%esi
     *   487fd8: e8 73 d3 23 00               	calll	0x6c5350 <_SND_fn_vDisplayError@8+0x4f1c0>
     *   487fdd: 8b 44 24 24                  	movl	36(%esp), %eax
     *   487fe1: 83 c4 0c                     	addl	$12, %esp
     *   487fe4: 5f                           	popl	%edi
     *   487fe5: 83 c0 08                     	addl	$8, %eax
     * ... (3 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00487FF0 - 0x00488032 (Size: 66 bytes)
 * Assertion line 184: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_00487FF0(void)
{
    /* Line 184 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   487ff0: 56                           	pushl	%esi
     *   487ff1: 57                           	pushl	%edi
     *   487ff2: 8b 7c 24 10                  	movl	16(%esp), %edi
     *   487ff6: 57                           	pushl	%edi
     *   487ff7: e8 44 de 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   487ffc: 8b f0                        	movl	%eax, %esi
     *   487ffe: 83 c4 04                     	addl	$4, %esp
     *   488001: 85 f6                        	testl	%esi, %esi
     *   488003: 75 20                        	jne	0x488025 <.text+0x87025>
     *   488005: 6a 01                        	pushl	$1
     *   488007: 50                           	pushl	%eax
     *   488008: 68 64 0b 7b 00               	pushl	$8063844                # imm = 0x7B0B64
     *   48800d: 68 58 0b 7b 00               	pushl	$8063832                # imm = 0x7B0B58
     *   488012: 68 b8 00 00 00               	pushl	$184
     *   488017: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   48801c: 50                           	pushl	%eax
     *   48801d: e8 ae 84 f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   488022: 83 c4 1c                     	addl	$28, %esp
     *   488025: 57                           	pushl	%edi
     *   488026: 56                           	pushl	%esi
     *   488027: e8 44 d4 23 00               	calll	0x6c5470 <_SND_fn_vDisplayError@8+0x4f2e0>
     *   48802c: 83 c4 08                     	addl	$8, %esp
     *   48802f: 5f                           	popl	%edi
     *   488030: 5e                           	popl	%esi
     *   488031: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00488040 - 0x00488112 (Size: 210 bytes)
 * Assertion line 184: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_00488040(void)
{
    /* Line 184 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   488040: 83 ec 0c                     	subl	$12, %esp
     *   488043: a1 70 3b ac 00               	movl	11287408, %eax
     *   488048: 8b 0d 68 3b ac 00            	movl	11287400, %ecx
     *   48804e: a3 74 3b ac 00               	movl	%eax, 11287412
     *   488053: a1 4c 3b ac 00               	movl	11287372, %eax
     *   488058: 8b 90 20 b5 ab 00            	movl	11253024(%eax), %edx
     *   48805e: 83 e8 20                     	subl	$32, %eax
     *   488061: 56                           	pushl	%esi
     *   488062: 8b 35 50 3b ac 00            	movl	11287376, %esi
     *   488068: 89 0d 6c 3b ac 00            	movl	%ecx, 11287404
     *   48806e: 8b 88 44 b5 ab 00            	movl	11253060(%eax), %ecx
     *   488074: 89 54 24 04                  	movl	%edx, 4(%esp)
     *   488078: 8b 90 48 b5 ab 00            	movl	11253064(%eax), %edx
     *   48807e: a3 4c 3b ac 00               	movl	%eax, 11287372
     *   488083: 8d 44 24 04                  	leal	4(%esp), %eax
     *   488087: 4e                           	decl	%esi
     *   488088: 50                           	pushl	%eax
     *   488089: 89 35 50 3b ac 00            	movl	%esi, 11287376
     *   48808f: 89 4c 24 0c                  	movl	%ecx, 12(%esp)
     *   488093: 89 54 24 10                  	movl	%edx, 16(%esp)
     *   488097: e8 a4 dd 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   48809c: 8b f0                        	movl	%eax, %esi
     *   48809e: 83 c4 04                     	addl	$4, %esp
     *   4880a1: 85 f6                        	testl	%esi, %esi
     *   4880a3: 75 20                        	jne	0x4880c5 <.text+0x870c5>
     *   4880a5: 6a 01                        	pushl	$1
     *   4880a7: 50                           	pushl	%eax
     *   4880a8: 68 64 0b 7b 00               	pushl	$8063844                # imm = 0x7B0B64
     *   4880ad: 68 58 0b 7b 00               	pushl	$8063832                # imm = 0x7B0B58
     *   4880b2: 68 b8 00 00 00               	pushl	$184
     *   4880b7: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   4880bc: 50                           	pushl	%eax
     *   4880bd: e8 0e 84 f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4880c2: 83 c4 1c                     	addl	$28, %esp
     *   4880c5: 8d 4c 24 04                  	leal	4(%esp), %ecx
     *   4880c9: 51                           	pushl	%ecx
     *   4880ca: 56                           	pushl	%esi
     *   4880cb: e8 a0 d3 23 00               	calll	0x6c5470 <_SND_fn_vDisplayError@8+0x4f2e0>
     *   4880d0: 8b 15 4c 3b ac 00            	movl	11287372, %edx
     *   4880d6: 8d 8a 40 b5 ab 00            	leal	11253056(%edx), %ecx
     *   4880dc: 89 01                        	movl	%eax, (%ecx)
     *   4880de: a1 50 3b ac 00               	movl	11287376, %eax
     *   4880e3: 83 c4 08                     	addl	$8, %esp
     *   4880e6: 83 c2 20                     	addl	$32, %edx
     *   4880e9: 66 c7 04 c5 40 b4 aa 00 01 00	movw	$1, 11187264(,%eax,8)
     *   4880f3: 89 0c c5 44 b4 aa 00         	movl	%ecx, 11187268(,%eax,8)
     *   4880fa: 40                           	incl	%eax
     *   4880fb: a3 50 3b ac 00               	movl	%eax, 11287376
     *   488100: 8b 44 24 14                  	movl	20(%esp), %eax
     *   488104: 89 15 4c 3b ac 00            	movl	%edx, 11287372
     *   48810a: 83 c0 08                     	addl	$8, %eax
     *   48810d: 5e                           	popl	%esi
     *   48810e: 83 c4 0c                     	addl	$12, %esp
     *   488111: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00488120 - 0x004881D8 (Size: 184 bytes)
 * Assertion line 234: pst_Grid | Message: Current world has no grid
 * Assertion line 235: pst_GridDest | Message: Current world has no Destination grid
 * --------------------------------------------------------------------------- */
void sub_00488120(void)
{
    /* Line 234 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);
    /* Line 235 */ ERR_X_Error(pst_GridDest, "Current world has no Destination grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   488120: 53                           	pushl	%ebx
     *   488121: 8b 5c 24 10                  	movl	16(%esp), %ebx
     *   488125: 55                           	pushl	%ebp
     *   488126: 56                           	pushl	%esi
     *   488127: 57                           	pushl	%edi
     *   488128: 53                           	pushl	%ebx
     *   488129: e8 12 dd 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   48812e: 8b 6c 24 24                  	movl	36(%esp), %ebp
     *   488132: 55                           	pushl	%ebp
     *   488133: 8b f0                        	movl	%eax, %esi
     *   488135: e8 06 dd 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   48813a: 83 c4 08                     	addl	$8, %esp
     *   48813d: 85 f6                        	testl	%esi, %esi
     *   48813f: 8b f8                        	movl	%eax, %edi
     *   488141: 75 20                        	jne	0x488163 <.text+0x87163>
     *   488143: 6a 01                        	pushl	$1
     *   488145: 56                           	pushl	%esi
     *   488146: 68 64 0b 7b 00               	pushl	$8063844                # imm = 0x7B0B64
     *   48814b: 68 58 0b 7b 00               	pushl	$8063832                # imm = 0x7B0B58
     *   488150: 68 ea 00 00 00               	pushl	$234
     *   488155: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   48815a: 56                           	pushl	%esi
     *   48815b: e8 70 83 f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   488160: 83 c4 1c                     	addl	$28, %esp
     *   488163: 85 ff                        	testl	%edi, %edi
     *   488165: 75 20                        	jne	0x488187 <.text+0x87187>
     *   488167: 6a 01                        	pushl	$1
     *   488169: 57                           	pushl	%edi
     *   48816a: 68 90 0b 7b 00               	pushl	$8063888                # imm = 0x7B0B90
     *   48816f: 68 80 0b 7b 00               	pushl	$8063872                # imm = 0x7B0B80
     *   488174: 68 eb 00 00 00               	pushl	$235
     *   488179: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   48817e: 57                           	pushl	%edi
     *   48817f: e8 4c 83 f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   488184: 83 c4 1c                     	addl	$28, %esp
     *   488187: a1 b0 8e ac 00               	movl	11308720, %eax
     *   48818c: 85 c0                        	testl	%eax, %eax
     *   48818e: 75 0a                        	jne	0x48819a <.text+0x8719a>
     *   488190: c7 05 b0 8e ac 00 01 00 00 00	movl	$1, 11308720
     *   48819a: 8b 44 24 34                  	movl	52(%esp), %eax
     *   48819e: 8b 4c 24 30                  	movl	48(%esp), %ecx
     *   4881a2: 8b 54 24 2c                  	movl	44(%esp), %edx
     *   4881a6: 50                           	pushl	%eax
     *   4881a7: 8b 44 24 2c                  	movl	44(%esp), %eax
     *   4881ab: 51                           	pushl	%ecx
     *   4881ac: 8b 4c 24 2c                  	movl	44(%esp), %ecx
     *   4881b0: 52                           	pushl	%edx
     *   4881b1: 8b 54 24 24                  	movl	36(%esp), %edx
     *   4881b5: 50                           	pushl	%eax
     *   4881b6: 8b 44 24 24                  	movl	36(%esp), %eax
     *   4881ba: 51                           	pushl	%ecx
     *   4881bb: 52                           	pushl	%edx
     *   4881bc: 55                           	pushl	%ebp
     *   4881bd: 53                           	pushl	%ebx
     * ... (11 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x004883E0 - 0x00488479 (Size: 153 bytes)
 * Assertion line 330: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_004883E0(void)
{
    /* Line 330 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   4883e0: 51                           	pushl	%ecx
     *   4883e1: 53                           	pushl	%ebx
     *   4883e2: 8b 5c 24 10                  	movl	16(%esp), %ebx
     *   4883e6: 56                           	pushl	%esi
     *   4883e7: 57                           	pushl	%edi
     *   4883e8: 53                           	pushl	%ebx
     *   4883e9: e8 52 da 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   4883ee: 8b f8                        	movl	%eax, %edi
     *   4883f0: 83 c4 04                     	addl	$4, %esp
     *   4883f3: 85 ff                        	testl	%edi, %edi
     *   4883f5: 75 20                        	jne	0x488417 <.text+0x87417>
     *   4883f7: 6a 01                        	pushl	$1
     *   4883f9: 50                           	pushl	%eax
     *   4883fa: 68 64 0b 7b 00               	pushl	$8063844                # imm = 0x7B0B64
     *   4883ff: 68 58 0b 7b 00               	pushl	$8063832                # imm = 0x7B0B58
     *   488404: 68 4a 01 00 00               	pushl	$330                    # imm = 0x14A
     *   488409: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   48840e: 50                           	pushl	%eax
     *   48840f: e8 bc 80 f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   488414: 83 c4 1c                     	addl	$28, %esp
     *   488417: 8b 03                        	movl	(%ebx), %eax
     *   488419: 8b 74 24 1c                  	movl	28(%esp), %esi
     *   48841d: 89 06                        	movl	%eax, (%esi)
     *   48841f: 8b 4b 04                     	movl	4(%ebx), %ecx
     *   488422: 89 4e 04                     	movl	%ecx, 4(%esi)
     *   488425: 8b 53 08                     	movl	8(%ebx), %edx
     *   488428: 8d 44 24 0c                  	leal	12(%esp), %eax
     *   48842c: 50                           	pushl	%eax
     *   48842d: 8d 4c 24 1c                  	leal	28(%esp), %ecx
     *   488431: 51                           	pushl	%ecx
     *   488432: 56                           	pushl	%esi
     *   488433: 57                           	pushl	%edi
     *   488434: 89 56 08                     	movl	%edx, 8(%esi)
     *   488437: e8 44 cd 23 00               	calll	0x6c5180 <_SND_fn_vDisplayError@8+0x4eff0>
     *   48843c: db 44 24 28                  	fildl	40(%esp)
     *   488440: 83 c4 10                     	addl	$16, %esp
     *   488443: d9 5c 24 1c                  	fstps	28(%esp)
     *   488447: d9 44 24 1c                  	flds	28(%esp)
     *   48844b: d8 47 14                     	fadds	20(%edi)
     *   48844e: d8 05 38 c9 7a 00            	fadds	8046904
     *   488454: d9 1e                        	fstps	(%esi)
     *   488456: db 44 24 0c                  	fildl	12(%esp)
     *   48845a: d9 5c 24 1c                  	fstps	28(%esp)
     *   48845e: d9 44 24 1c                  	flds	28(%esp)
     *   488462: d8 47 18                     	fadds	24(%edi)
     *   488465: d8 05 38 c9 7a 00            	fadds	8046904
     *   48846b: d9 5e 04                     	fstps	4(%esi)
     *   48846e: 8b 57 1c                     	movl	28(%edi), %edx
     *   488471: 5f                           	popl	%edi
     *   488472: 89 56 08                     	movl	%edx, 8(%esi)
     *   488475: 5e                           	popl	%esi
     *   488476: 5b                           	popl	%ebx
     *   488477: 59                           	popl	%ecx
     *   488478: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00488540 - 0x004885CD (Size: 141 bytes)
 * Assertion line 372: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_00488540(void)
{
    /* Line 372 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   488540: 51                           	pushl	%ecx
     *   488541: 8b 44 24 08                  	movl	8(%esp), %eax
     *   488545: 56                           	pushl	%esi
     *   488546: 57                           	pushl	%edi
     *   488547: 8b 78 24                     	movl	36(%eax), %edi
     *   48854a: 6a 01                        	pushl	$1
     *   48854c: 6a 00                        	pushl	$0
     *   48854e: 68 64 0b 7b 00               	pushl	$8063844                # imm = 0x7B0B64
     *   488553: 68 58 0b 7b 00               	pushl	$8063832                # imm = 0x7B0B58
     *   488558: 68 74 01 00 00               	pushl	$372                    # imm = 0x174
     *   48855d: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   488562: 6a 00                        	pushl	$0
     *   488564: e8 67 7f f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   488569: 8b 87 14 02 00 00            	movl	532(%edi), %eax
     *   48856f: 83 c4 1c                     	addl	$28, %esp
     *   488572: 33 f6                        	xorl	%esi, %esi
     *   488574: 85 c0                        	testl	%eax, %eax
     *   488576: 74 51                        	je	0x4885c9 <.text+0x875c9>
     *   488578: 53                           	pushl	%ebx
     *   488579: 8b 5c 24 18                  	movl	24(%esp), %ebx
     *   48857d: 8d 49 00                     	leal	(%ecx), %ecx
     *   488580: 3b 70 04                     	cmpl	4(%eax), %esi
     *   488583: 73 43                        	jae	0x4885c8 <.text+0x875c8>
     *   488585: 8b 08                        	movl	(%eax), %ecx
     *   488587: 8b 04 b1                     	movl	(%ecx,%esi,4), %eax
     *   48858a: 85 c0                        	testl	%eax, %eax
     *   48858c: 74 2f                        	je	0x4885bd <.text+0x875bd>
     *   48858e: 8d 54 24 14                  	leal	20(%esp), %edx
     *   488592: 52                           	pushl	%edx
     *   488593: 8d 4c 24 10                  	leal	16(%esp), %ecx
     *   488597: 51                           	pushl	%ecx
     *   488598: 53                           	pushl	%ebx
     *   488599: 50                           	pushl	%eax
     *   48859a: e8 e1 cb 23 00               	calll	0x6c5180 <_SND_fn_vDisplayError@8+0x4eff0>
     *   48859f: 8b 54 24 24                  	movl	36(%esp), %edx
     *   4885a3: 8b 44 24 1c                  	movl	28(%esp), %eax
     *   4885a7: 8b 8f 14 02 00 00            	movl	532(%edi), %ecx
     *   4885ad: 52                           	pushl	%edx
     *   4885ae: 8b 11                        	movl	(%ecx), %edx
     *   4885b0: 50                           	pushl	%eax
     *   4885b1: 8b 04 b2                     	movl	(%edx,%esi,4), %eax
     *   4885b4: 50                           	pushl	%eax
     *   4885b5: e8 26 0a 24 00               	calll	0x6c8fe0 <_SND_fn_vDisplayError@8+0x52e50>
     *   4885ba: 83 c4 1c                     	addl	$28, %esp
     *   4885bd: 8b 87 14 02 00 00            	movl	532(%edi), %eax
     *   4885c3: 46                           	incl	%esi
     *   4885c4: 85 c0                        	testl	%eax, %eax
     *   4885c6: 75 b8                        	jne	0x488580 <.text+0x87580>
     *   4885c8: 5b                           	popl	%ebx
     *   4885c9: 5f                           	popl	%edi
     *   4885ca: 5e                           	popl	%esi
     *   4885cb: 59                           	popl	%ecx
     *   4885cc: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00488640 - 0x00488698 (Size: 88 bytes)
 * Assertion line 429: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_00488640(void)
{
    /* Line 429 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   488640: 83 ec 08                     	subl	$8, %esp
     *   488643: 56                           	pushl	%esi
     *   488644: 57                           	pushl	%edi
     *   488645: 8b 7c 24 18                  	movl	24(%esp), %edi
     *   488649: 57                           	pushl	%edi
     *   48864a: e8 f1 d7 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   48864f: 8b f0                        	movl	%eax, %esi
     *   488651: 83 c4 04                     	addl	$4, %esp
     *   488654: 85 f6                        	testl	%esi, %esi
     *   488656: 75 20                        	jne	0x488678 <.text+0x87678>
     *   488658: 6a 01                        	pushl	$1
     *   48865a: 50                           	pushl	%eax
     *   48865b: 68 64 0b 7b 00               	pushl	$8063844                # imm = 0x7B0B64
     *   488660: 68 58 0b 7b 00               	pushl	$8063832                # imm = 0x7B0B58
     *   488665: 68 ad 01 00 00               	pushl	$429                    # imm = 0x1AD
     *   48866a: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   48866f: 50                           	pushl	%eax
     *   488670: e8 5b 7e f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   488675: 83 c4 1c                     	addl	$28, %esp
     *   488678: 8d 44 24 08                  	leal	8(%esp), %eax
     *   48867c: 50                           	pushl	%eax
     *   48867d: 8d 4c 24 10                  	leal	16(%esp), %ecx
     *   488681: 51                           	pushl	%ecx
     *   488682: 57                           	pushl	%edi
     *   488683: 56                           	pushl	%esi
     *   488684: e8 57 d0 23 00               	calll	0x6c56e0 <_SND_fn_vDisplayError@8+0x4f550>
     *   488689: 83 c4 10                     	addl	$16, %esp
     *   48868c: f7 d8                        	negl	%eax
     *   48868e: 1b c0                        	sbbl	%eax, %eax
     *   488690: 5f                           	popl	%edi
     *   488691: f7 d8                        	negl	%eax
     *   488693: 5e                           	popl	%esi
     *   488694: 83 c4 08                     	addl	$8, %esp
     *   488697: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00488740 - 0x00488871 (Size: 305 bytes)
 * Assertion line 465: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_00488740(void)
{
    /* Line 465 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   488740: a1 70 3b ac 00               	movl	11287408, %eax
     *   488745: 8b 0d 68 3b ac 00            	movl	11287400, %ecx
     *   48874b: 83 ec 0c                     	subl	$12, %esp
     *   48874e: a3 74 3b ac 00               	movl	%eax, 11287412
     *   488753: a1 4c 3b ac 00               	movl	11287372, %eax
     *   488758: 89 0d 6c 3b ac 00            	movl	%ecx, 11287404
     *   48875e: 8b 0d 50 3b ac 00            	movl	11287376, %ecx
     *   488764: 53                           	pushl	%ebx
     *   488765: 83 e8 20                     	subl	$32, %eax
     *   488768: 49                           	decl	%ecx
     *   488769: ba 02 00 00 00               	movl	$2, %edx
     *   48876e: 66 39 14 cd 40 b4 aa 00      	cmpw	%dx, 11187264(,%ecx,8)
     *   488776: 56                           	pushl	%esi
     *   488777: 57                           	pushl	%edi
     *   488778: 75 16                        	jne	0x488790 <.text+0x87790>
     *   48877a: d9 80 40 b5 ab 00            	flds	11253056(%eax)
     *   488780: dc 05 a0 1d b2 00            	faddl	11672992
     *   488786: dd 5c 24 0c                  	fstpl	12(%esp)
     *   48878a: 8b 5c 24 0c                  	movl	12(%esp), %ebx
     *   48878e: eb 06                        	jmp	0x488796 <.text+0x87796>
     *   488790: 8b 98 40 b5 ab 00            	movl	11253056(%eax), %ebx
     *   488796: 83 e8 20                     	subl	$32, %eax
     *   488799: 49                           	decl	%ecx
     *   48879a: 66 39 14 cd 40 b4 aa 00      	cmpw	%dx, 11187264(,%ecx,8)
     *   4887a2: 75 16                        	jne	0x4887ba <.text+0x877ba>
     *   4887a4: d9 80 40 b5 ab 00            	flds	11253056(%eax)
     *   4887aa: dc 05 a0 1d b2 00            	faddl	11672992
     *   4887b0: dd 5c 24 0c                  	fstpl	12(%esp)
     *   4887b4: 8b 7c 24 0c                  	movl	12(%esp), %edi
     *   4887b8: eb 06                        	jmp	0x4887c0 <.text+0x877c0>
     *   4887ba: 8b b8 40 b5 ab 00            	movl	11253056(%eax), %edi
     *   4887c0: 8b 90 20 b5 ab 00            	movl	11253024(%eax), %edx
     *   4887c6: 83 e8 20                     	subl	$32, %eax
     *   4887c9: 49                           	decl	%ecx
     *   4887ca: 89 0d 50 3b ac 00            	movl	%ecx, 11287376
     *   4887d0: 8b 88 44 b5 ab 00            	movl	11253060(%eax), %ecx
     *   4887d6: 89 54 24 0c                  	movl	%edx, 12(%esp)
     *   4887da: 8b 90 48 b5 ab 00            	movl	11253064(%eax), %edx
     *   4887e0: a3 4c 3b ac 00               	movl	%eax, 11287372
     *   4887e5: 8d 44 24 0c                  	leal	12(%esp), %eax
     *   4887e9: 50                           	pushl	%eax
     *   4887ea: 89 4c 24 14                  	movl	%ecx, 20(%esp)
     *   4887ee: 89 54 24 18                  	movl	%edx, 24(%esp)
     *   4887f2: e8 49 d6 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   4887f7: 8b f0                        	movl	%eax, %esi
     *   4887f9: 83 c4 04                     	addl	$4, %esp
     *   4887fc: 85 f6                        	testl	%esi, %esi
     *   4887fe: 75 20                        	jne	0x488820 <.text+0x87820>
     *   488800: 6a 01                        	pushl	$1
     *   488802: 50                           	pushl	%eax
     *   488803: 68 64 0b 7b 00               	pushl	$8063844                # imm = 0x7B0B64
     *   488808: 68 58 0b 7b 00               	pushl	$8063832                # imm = 0x7B0B58
     *   48880d: 68 d1 01 00 00               	pushl	$465                    # imm = 0x1D1
     *   488812: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     * ... (27 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00488880 - 0x004888CC (Size: 76 bytes)
 * Assertion line 502: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_00488880(void)
{
    /* Line 502 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   488880: 56                           	pushl	%esi
     *   488881: 57                           	pushl	%edi
     *   488882: 8b 7c 24 10                  	movl	16(%esp), %edi
     *   488886: 57                           	pushl	%edi
     *   488887: e8 b4 d5 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   48888c: 8b f0                        	movl	%eax, %esi
     *   48888e: 83 c4 04                     	addl	$4, %esp
     *   488891: 85 f6                        	testl	%esi, %esi
     *   488893: 75 20                        	jne	0x4888b5 <.text+0x878b5>
     *   488895: 6a 01                        	pushl	$1
     *   488897: 50                           	pushl	%eax
     *   488898: 68 64 0b 7b 00               	pushl	$8063844                # imm = 0x7B0B64
     *   48889d: 68 58 0b 7b 00               	pushl	$8063832                # imm = 0x7B0B58
     *   4888a2: 68 f6 01 00 00               	pushl	$502                    # imm = 0x1F6
     *   4888a7: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   4888ac: 50                           	pushl	%eax
     *   4888ad: e8 1e 7c f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4888b2: 83 c4 1c                     	addl	$28, %esp
     *   4888b5: 8b 44 24 18                  	movl	24(%esp), %eax
     *   4888b9: 8b 4c 24 14                  	movl	20(%esp), %ecx
     *   4888bd: 50                           	pushl	%eax
     *   4888be: 51                           	pushl	%ecx
     *   4888bf: 57                           	pushl	%edi
     *   4888c0: 56                           	pushl	%esi
     *   4888c1: e8 9a e1 23 00               	calll	0x6c6a60 <_SND_fn_vDisplayError@8+0x508d0>
     *   4888c6: 83 c4 10                     	addl	$16, %esp
     *   4888c9: 5f                           	popl	%edi
     *   4888ca: 5e                           	popl	%esi
     *   4888cb: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x004888D0 - 0x004889F8 (Size: 296 bytes)
 * Assertion line 502: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_004888D0(void)
{
    /* Line 502 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   4888d0: a1 70 3b ac 00               	movl	11287408, %eax
     *   4888d5: 8b 0d 68 3b ac 00            	movl	11287400, %ecx
     *   4888db: a3 74 3b ac 00               	movl	%eax, 11287412
     *   4888e0: a1 4c 3b ac 00               	movl	11287372, %eax
     *   4888e5: 83 ec 18                     	subl	$24, %esp
     *   4888e8: 89 0d 6c 3b ac 00            	movl	%ecx, 11287404
     *   4888ee: 8b 0d 50 3b ac 00            	movl	11287376, %ecx
     *   4888f4: 83 e8 20                     	subl	$32, %eax
     *   4888f7: 49                           	decl	%ecx
     *   4888f8: 66 83 3c cd 40 b4 aa 00 02   	cmpw	$2, 11187264(,%ecx,8)
     *   488901: 56                           	pushl	%esi
     *   488902: 57                           	pushl	%edi
     *   488903: 75 16                        	jne	0x48891b <.text+0x8791b>
     *   488905: d9 80 40 b5 ab 00            	flds	11253056(%eax)
     *   48890b: dc 05 a0 1d b2 00            	faddl	11672992
     *   488911: dd 5c 24 08                  	fstpl	8(%esp)
     *   488915: 8b 7c 24 08                  	movl	8(%esp), %edi
     *   488919: eb 06                        	jmp	0x488921 <.text+0x87921>
     *   48891b: 8b b8 40 b5 ab 00            	movl	11253056(%eax), %edi
     *   488921: 8b 90 20 b5 ab 00            	movl	11253024(%eax), %edx
     *   488927: 83 e8 20                     	subl	$32, %eax
     *   48892a: 89 54 24 14                  	movl	%edx, 20(%esp)
     *   48892e: 8b 90 44 b5 ab 00            	movl	11253060(%eax), %edx
     *   488934: 89 54 24 18                  	movl	%edx, 24(%esp)
     *   488938: 8b 90 48 b5 ab 00            	movl	11253064(%eax), %edx
     *   48893e: 83 e8 20                     	subl	$32, %eax
     *   488941: 83 e9 02                     	subl	$2, %ecx
     *   488944: 89 0d 50 3b ac 00            	movl	%ecx, 11287376
     *   48894a: 8b 88 40 b5 ab 00            	movl	11253056(%eax), %ecx
     *   488950: 89 54 24 1c                  	movl	%edx, 28(%esp)
     *   488954: 8b 90 44 b5 ab 00            	movl	11253060(%eax), %edx
     *   48895a: 89 4c 24 08                  	movl	%ecx, 8(%esp)
     *   48895e: a3 4c 3b ac 00               	movl	%eax, 11287372
     *   488963: 8b 80 48 b5 ab 00            	movl	11253064(%eax), %eax
     *   488969: 8d 4c 24 08                  	leal	8(%esp), %ecx
     *   48896d: 51                           	pushl	%ecx
     *   48896e: 89 54 24 10                  	movl	%edx, 16(%esp)
     *   488972: 89 44 24 14                  	movl	%eax, 20(%esp)
     *   488976: e8 c5 d4 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   48897b: 8b f0                        	movl	%eax, %esi
     *   48897d: 83 c4 04                     	addl	$4, %esp
     *   488980: 85 f6                        	testl	%esi, %esi
     *   488982: 75 20                        	jne	0x4889a4 <.text+0x879a4>
     *   488984: 6a 01                        	pushl	$1
     *   488986: 50                           	pushl	%eax
     *   488987: 68 64 0b 7b 00               	pushl	$8063844                # imm = 0x7B0B64
     *   48898c: 68 58 0b 7b 00               	pushl	$8063832                # imm = 0x7B0B58
     *   488991: 68 f6 01 00 00               	pushl	$502                    # imm = 0x1F6
     *   488996: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   48899b: 50                           	pushl	%eax
     *   48899c: e8 2f 7b f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   4889a1: 83 c4 1c                     	addl	$28, %esp
     *   4889a4: 57                           	pushl	%edi
     *   4889a5: 8d 54 24 18                  	leal	24(%esp), %edx
     * ... (22 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00488A00 - 0x00488B69 (Size: 361 bytes)
 * Assertion line 544: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_00488A00(void)
{
    /* Line 544 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   488a00: 8b 0d 68 3b ac 00            	movl	11287400, %ecx
     *   488a06: a1 70 3b ac 00               	movl	11287408, %eax
     *   488a0b: 83 ec 44                     	subl	$68, %esp
     *   488a0e: 53                           	pushl	%ebx
     *   488a0f: 89 0d 6c 3b ac 00            	movl	%ecx, 11287404
     *   488a15: 8b 0d 4c 3b ac 00            	movl	11287372, %ecx
     *   488a1b: a3 74 3b ac 00               	movl	%eax, 11287412
     *   488a20: a1 50 3b ac 00               	movl	11287376, %eax
     *   488a25: 55                           	pushl	%ebp
     *   488a26: 83 e9 20                     	subl	$32, %ecx
     *   488a29: 48                           	decl	%eax
     *   488a2a: 66 83 3c c5 40 b4 aa 00 02   	cmpw	$2, 11187264(,%eax,8)
     *   488a33: 56                           	pushl	%esi
     *   488a34: 57                           	pushl	%edi
     *   488a35: 75 16                        	jne	0x488a4d <.text+0x87a4d>
     *   488a37: d9 81 40 b5 ab 00            	flds	11253056(%ecx)
     *   488a3d: dc 05 a0 1d b2 00            	faddl	11672992
     *   488a43: dd 5c 24 10                  	fstpl	16(%esp)
     *   488a47: 8b 6c 24 10                  	movl	16(%esp), %ebp
     *   488a4b: eb 06                        	jmp	0x488a53 <.text+0x87a53>
     *   488a4d: 8b a9 40 b5 ab 00            	movl	11253056(%ecx), %ebp
     *   488a53: 83 e9 20                     	subl	$32, %ecx
     *   488a56: 48                           	decl	%eax
     *   488a57: 66 83 3c c5 40 b4 aa 00 01   	cmpw	$1, 11187264(,%eax,8)
     *   488a60: 89 0d 4c 3b ac 00            	movl	%ecx, 11287372
     *   488a66: 75 18                        	jne	0x488a80 <.text+0x87a80>
     *   488a68: db 81 40 b5 ab 00            	fildl	11253056(%ecx)
     *   488a6e: d9 5c 24 10                  	fstps	16(%esp)
     *   488a72: d9 44 24 10                  	flds	16(%esp)
     *   488a76: d9 5c 24 10                  	fstps	16(%esp)
     *   488a7a: 8b 5c 24 10                  	movl	16(%esp), %ebx
     *   488a7e: eb 06                        	jmp	0x488a86 <.text+0x87a86>
     *   488a80: 8b 99 40 b5 ab 00            	movl	11253056(%ecx), %ebx
     *   488a86: 66 8b 0c c5 38 b4 aa 00      	movw	11187256(,%eax,8), %cx
     *   488a8e: 8b 34 c5 3c b4 aa 00         	movl	11187260(,%eax,8), %esi
     *   488a95: 48                           	decl	%eax
     *   488a96: a3 50 3b ac 00               	movl	%eax, 11287376
     *   488a9b: 8d 44 24 1c                  	leal	28(%esp), %eax
     *   488a9f: 50                           	pushl	%eax
     *   488aa0: 0f bf d1                     	movswl	%cx, %edx
     *   488aa3: 56                           	pushl	%esi
     *   488aa4: ff 14 d5 3c b9 7f 00         	calll	*8370492(,%edx,8)
     *   488aab: a1 4c 3b ac 00               	movl	11287372, %eax
     *   488ab0: 8b 88 00 b5 ab 00            	movl	11252992(%eax), %ecx
     *   488ab6: 8b 3d 50 3b ac 00            	movl	11287376, %edi
     *   488abc: 8b 90 04 b5 ab 00            	movl	11252996(%eax), %edx
     *   488ac2: 83 e8 40                     	subl	$64, %eax
     *   488ac5: 89 4c 24 18                  	movl	%ecx, 24(%esp)
     *   488ac9: a3 4c 3b ac 00               	movl	%eax, 11287372
     *   488ace: 8b 80 48 b5 ab 00            	movl	11253064(%eax), %eax
     *   488ad4: 8d 4c 24 18                  	leal	24(%esp), %ecx
     *   488ad8: 4f                           	decl	%edi
     *   488ad9: 51                           	pushl	%ecx
     *   488ada: 89 3d 50 3b ac 00            	movl	%edi, 11287376
     * ... (42 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00488B70 - 0x00488CC8 (Size: 344 bytes)
 * Assertion line 594: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_00488B70(void)
{
    /* Line 594 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   488b70: 83 ec 18                     	subl	$24, %esp
     *   488b73: a1 70 3b ac 00               	movl	11287408, %eax
     *   488b78: 8b 0d 68 3b ac 00            	movl	11287400, %ecx
     *   488b7e: a3 74 3b ac 00               	movl	%eax, 11287412
     *   488b83: a1 4c 3b ac 00               	movl	11287372, %eax
     *   488b88: 8b 90 20 b5 ab 00            	movl	11253024(%eax), %edx
     *   488b8e: 83 e8 20                     	subl	$32, %eax
     *   488b91: 89 0d 6c 3b ac 00            	movl	%ecx, 11287404
     *   488b97: 8b 88 44 b5 ab 00            	movl	11253060(%eax), %ecx
     *   488b9d: 89 54 24 0c                  	movl	%edx, 12(%esp)
     *   488ba1: 8b 90 48 b5 ab 00            	movl	11253064(%eax), %edx
     *   488ba7: 89 4c 24 10                  	movl	%ecx, 16(%esp)
     *   488bab: 8b 0d 50 3b ac 00            	movl	11287376, %ecx
     *   488bb1: 89 54 24 14                  	movl	%edx, 20(%esp)
     *   488bb5: ba 02 00 00 00               	movl	$2, %edx
     *   488bba: 53                           	pushl	%ebx
     *   488bbb: 2b ca                        	subl	%edx, %ecx
     *   488bbd: 56                           	pushl	%esi
     *   488bbe: 83 e8 20                     	subl	$32, %eax
     *   488bc1: 66 39 14 cd 40 b4 aa 00      	cmpw	%dx, 11187264(,%ecx,8)
     *   488bc9: 57                           	pushl	%edi
     *   488bca: 75 16                        	jne	0x488be2 <.text+0x87be2>
     *   488bcc: d9 80 40 b5 ab 00            	flds	11253056(%eax)
     *   488bd2: dc 05 a0 1d b2 00            	faddl	11672992
     *   488bd8: dd 5c 24 0c                  	fstpl	12(%esp)
     *   488bdc: 8b 5c 24 0c                  	movl	12(%esp), %ebx
     *   488be0: eb 06                        	jmp	0x488be8 <.text+0x87be8>
     *   488be2: 8b 98 40 b5 ab 00            	movl	11253056(%eax), %ebx
     *   488be8: 83 e8 20                     	subl	$32, %eax
     *   488beb: 49                           	decl	%ecx
     *   488bec: 66 39 14 cd 40 b4 aa 00      	cmpw	%dx, 11187264(,%ecx,8)
     *   488bf4: 75 16                        	jne	0x488c0c <.text+0x87c0c>
     *   488bf6: d9 80 40 b5 ab 00            	flds	11253056(%eax)
     *   488bfc: dc 05 a0 1d b2 00            	faddl	11672992
     *   488c02: dd 5c 24 0c                  	fstpl	12(%esp)
     *   488c06: 8b 7c 24 0c                  	movl	12(%esp), %edi
     *   488c0a: eb 06                        	jmp	0x488c12 <.text+0x87c12>
     *   488c0c: 8b b8 40 b5 ab 00            	movl	11253056(%eax), %edi
     *   488c12: 8b 90 24 b5 ab 00            	movl	11253028(%eax), %edx
     *   488c18: 83 e8 20                     	subl	$32, %eax
     *   488c1b: 49                           	decl	%ecx
     *   488c1c: 89 0d 50 3b ac 00            	movl	%ecx, 11287376
     *   488c22: 8b 88 40 b5 ab 00            	movl	11253056(%eax), %ecx
     *   488c28: 89 4c 24 0c                  	movl	%ecx, 12(%esp)
     *   488c2c: a3 4c 3b ac 00               	movl	%eax, 11287372
     *   488c31: 8b 80 48 b5 ab 00            	movl	11253064(%eax), %eax
     *   488c37: 8d 4c 24 0c                  	leal	12(%esp), %ecx
     *   488c3b: 51                           	pushl	%ecx
     *   488c3c: 89 54 24 14                  	movl	%edx, 20(%esp)
     *   488c40: 89 44 24 18                  	movl	%eax, 24(%esp)
     *   488c44: e8 f7 d1 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   488c49: 8b f0                        	movl	%eax, %esi
     *   488c4b: 83 c4 04                     	addl	$4, %esp
     *   488c4e: 85 f6                        	testl	%esi, %esi
     * ... (36 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00488CD0 - 0x00488D4F (Size: 127 bytes)
 * Assertion line 637: pst_Grid | Message: Current world has no grid
 * Assertion line 638: pst_GridDest | Message: Current world has no destination grid
 * --------------------------------------------------------------------------- */
void sub_00488CD0(void)
{
    /* Line 637 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);
    /* Line 638 */ ERR_X_Error(pst_GridDest, "Current world has no destination grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   488cd0: 53                           	pushl	%ebx
     *   488cd1: 55                           	pushl	%ebp
     *   488cd2: 56                           	pushl	%esi
     *   488cd3: 8b 74 24 14                  	movl	20(%esp), %esi
     *   488cd7: 57                           	pushl	%edi
     *   488cd8: 56                           	pushl	%esi
     *   488cd9: e8 62 d1 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   488cde: 8b 5c 24 20                  	movl	32(%esp), %ebx
     *   488ce2: 8b f8                        	movl	%eax, %edi
     *   488ce4: 8d 04 5b                     	leal	(%ebx,%ebx,2), %eax
     *   488ce7: 8d 4c 86 f4                  	leal	-12(%esi,%eax,4), %ecx
     *   488ceb: 51                           	pushl	%ecx
     *   488cec: e8 4f d1 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   488cf1: 83 c4 08                     	addl	$8, %esp
     *   488cf4: 85 ff                        	testl	%edi, %edi
     *   488cf6: 8b e8                        	movl	%eax, %ebp
     *   488cf8: 75 20                        	jne	0x488d1a <.text+0x87d1a>
     *   488cfa: 6a 01                        	pushl	$1
     *   488cfc: 57                           	pushl	%edi
     *   488cfd: 68 64 0b 7b 00               	pushl	$8063844                # imm = 0x7B0B64
     *   488d02: 68 58 0b 7b 00               	pushl	$8063832                # imm = 0x7B0B58
     *   488d07: 68 7d 02 00 00               	pushl	$637                    # imm = 0x27D
     *   488d0c: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   488d11: 57                           	pushl	%edi
     *   488d12: e8 b9 77 f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   488d17: 83 c4 1c                     	addl	$28, %esp
     *   488d1a: 85 ed                        	testl	%ebp, %ebp
     *   488d1c: 75 20                        	jne	0x488d3e <.text+0x87d3e>
     *   488d1e: 6a 01                        	pushl	$1
     *   488d20: 55                           	pushl	%ebp
     *   488d21: 68 b8 0b 7b 00               	pushl	$8063928                # imm = 0x7B0BB8
     *   488d26: 68 80 0b 7b 00               	pushl	$8063872                # imm = 0x7B0B80
     *   488d2b: 68 7e 02 00 00               	pushl	$638                    # imm = 0x27E
     *   488d30: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   488d35: 55                           	pushl	%ebp
     *   488d36: e8 95 77 f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   488d3b: 83 c4 1c                     	addl	$28, %esp
     *   488d3e: 53                           	pushl	%ebx
     *   488d3f: 56                           	pushl	%esi
     *   488d40: 57                           	pushl	%edi
     *   488d41: 55                           	pushl	%ebp
     *   488d42: e8 09 cb 23 00               	calll	0x6c5850 <_SND_fn_vDisplayError@8+0x4f6c0>
     *   488d47: 83 c4 10                     	addl	$16, %esp
     *   488d4a: 5f                           	popl	%edi
     *   488d4b: 5e                           	popl	%esi
     *   488d4c: 5d                           	popl	%ebp
     *   488d4d: 5b                           	popl	%ebx
     *   488d4e: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00488E30 - 0x00488E94 (Size: 100 bytes)
 * Assertion line 683: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_00488E30(void)
{
    /* Line 683 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   488e30: 83 ec 0c                     	subl	$12, %esp
     *   488e33: 56                           	pushl	%esi
     *   488e34: 57                           	pushl	%edi
     *   488e35: 8b 7c 24 18                  	movl	24(%esp), %edi
     *   488e39: 8b 47 0c                     	movl	12(%edi), %eax
     *   488e3c: 83 c0 30                     	addl	$48, %eax
     *   488e3f: 50                           	pushl	%eax
     *   488e40: e8 fb cf 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   488e45: 8b f0                        	movl	%eax, %esi
     *   488e47: 83 c4 04                     	addl	$4, %esp
     *   488e4a: 85 f6                        	testl	%esi, %esi
     *   488e4c: 75 20                        	jne	0x488e6e <.text+0x87e6e>
     *   488e4e: 6a 01                        	pushl	$1
     *   488e50: 50                           	pushl	%eax
     *   488e51: 68 64 0b 7b 00               	pushl	$8063844                # imm = 0x7B0B64
     *   488e56: 68 58 0b 7b 00               	pushl	$8063832                # imm = 0x7B0B58
     *   488e5b: 68 ab 02 00 00               	pushl	$683                    # imm = 0x2AB
     *   488e60: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   488e65: 50                           	pushl	%eax
     *   488e66: e8 65 76 f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   488e6b: 83 c4 1c                     	addl	$28, %esp
     *   488e6e: 8d 44 24 08                  	leal	8(%esp), %eax
     *   488e72: 50                           	pushl	%eax
     *   488e73: 57                           	pushl	%edi
     *   488e74: e8 e7 1a 21 00               	calll	0x69a960 <_SND_fn_vDisplayError@8+0x247d0>
     *   488e79: 8b 57 0c                     	movl	12(%edi), %edx
     *   488e7c: 8d 4c 24 10                  	leal	16(%esp), %ecx
     *   488e80: 51                           	pushl	%ecx
     *   488e81: 83 c2 30                     	addl	$48, %edx
     *   488e84: 52                           	pushl	%edx
     *   488e85: 56                           	pushl	%esi
     *   488e86: e8 c5 dd 23 00               	calll	0x6c6c50 <_SND_fn_vDisplayError@8+0x50ac0>
     *   488e8b: 83 c4 14                     	addl	$20, %esp
     *   488e8e: 5f                           	popl	%edi
     *   488e8f: 5e                           	popl	%esi
     *   488e90: 83 c4 0c                     	addl	$12, %esp
     *   488e93: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00488F10 - 0x00489005 (Size: 245 bytes)
 * Assertion line 723: pst_Grid | Message: Current world has no grid
 * --------------------------------------------------------------------------- */
void sub_00488F10(void)
{
    /* Line 723 */ ERR_X_Error(pst_Grid, "Current world has no grid", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   488f10: 53                           	pushl	%ebx
     *   488f11: 55                           	pushl	%ebp
     *   488f12: 56                           	pushl	%esi
     *   488f13: 57                           	pushl	%edi
     *   488f14: 8b 7c 24 18                  	movl	24(%esp), %edi
     *   488f18: 57                           	pushl	%edi
     *   488f19: e8 22 cf 23 00               	calll	0x6c5e40 <_SND_fn_vDisplayError@8+0x4fcb0>
     *   488f1e: 8b e8                        	movl	%eax, %ebp
     *   488f20: 83 c4 04                     	addl	$4, %esp
     *   488f23: 85 ed                        	testl	%ebp, %ebp
     *   488f25: 75 20                        	jne	0x488f47 <.text+0x87f47>
     *   488f27: 6a 01                        	pushl	$1
     *   488f29: 50                           	pushl	%eax
     *   488f2a: 68 64 0b 7b 00               	pushl	$8063844                # imm = 0x7B0B64
     *   488f2f: 68 58 0b 7b 00               	pushl	$8063832                # imm = 0x7B0B58
     *   488f34: 68 d3 02 00 00               	pushl	$723                    # imm = 0x2D3
     *   488f39: 68 1c 0b 7b 00               	pushl	$8063772                # imm = 0x7B0B1C
     *   488f3e: 50                           	pushl	%eax
     *   488f3f: e8 8c 75 f9 ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   488f44: 83 c4 1c                     	addl	$28, %esp
     *   488f47: 8b 5c 24 14                  	movl	20(%esp), %ebx
     *   488f4b: d9 07                        	flds	(%edi)
     *   488f4d: 8b 43 0c                     	movl	12(%ebx), %eax
     *   488f50: d8 60 30                     	fsubs	48(%eax)
     *   488f53: 8b 74 24 20                  	movl	32(%esp), %esi
     *   488f57: 83 c0 30                     	addl	$48, %eax
     *   488f5a: 56                           	pushl	%esi
     *   488f5b: d9 1e                        	fstps	(%esi)
     *   488f5d: d9 47 04                     	flds	4(%edi)
     *   488f60: d8 60 04                     	fsubs	4(%eax)
     *   488f63: d9 5e 04                     	fstps	4(%esi)
     *   488f66: d9 47 08                     	flds	8(%edi)
     *   488f69: d8 60 08                     	fsubs	8(%eax)
     *   488f6c: d9 5e 08                     	fstps	8(%esi)
     *   488f6f: e8 7c 80 fa ff               	calll	0x430ff0 <.text+0x2fff0>
     *   488f74: d9 5c 24 1c                  	fstps	28(%esp)
     *   488f78: d9 05 ac cd 7a 00            	flds	8048044
     *   488f7e: 83 c4 04                     	addl	$4, %esp
     *   488f81: d9 44 24 18                  	flds	24(%esp)
     *   488f85: da e9                        	fucompp
     *   488f87: df e0                        	fnstsw	%ax
     *   488f89: f6 c4 44                     	testb	$68, %ah
     *   488f8c: 7b 72                        	jnp	0x489000 <.text+0x88000>
     *   488f8e: d9 44 24 18                  	flds	24(%esp)
     *   488f92: d8 5c 24 1c                  	fcomps	28(%esp)
     *   488f96: df e0                        	fnstsw	%ax
     *   488f98: f6 c4 05                     	testb	$5, %ah
     *   488f9b: 7a 0a                        	jp	0x488fa7 <.text+0x87fa7>
     *   488f9d: 8b 4c 24 18                  	movl	24(%esp), %ecx
     *   488fa1: 89 4c 24 1c                  	movl	%ecx, 28(%esp)
     *   488fa5: eb 04                        	jmp	0x488fab <.text+0x87fab>
     *   488fa7: 8b 4c 24 1c                  	movl	28(%esp), %ecx
     *   488fab: d9 05 ac cd 7a 00            	flds	8048044
     *   488fb1: d9 44 24 1c                  	flds	28(%esp)
     * ... (34 more instructions)
     */
}
