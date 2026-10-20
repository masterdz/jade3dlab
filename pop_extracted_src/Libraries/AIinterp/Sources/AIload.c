/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/AIinterp/Sources/AIload.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 5
 * Unique Functions Mapped: 4
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x00465500 - 0x00465702 (Size: 514 bytes)
 * Assertion line 306: _pst_Node->w_Param >= 0 | Message: Invalid AI Node. See an engineer
 * Assertion line 313: AI_gi_DynAINodeLevel[0] < 6000 | Message: Too Many functions called. See an engineer.
 * --------------------------------------------------------------------------- */
void sub_00465500(void)
{
    /* Line 306 */ ERR_X_Error(_pst_Node->w_Param >= 0, "Invalid AI Node. See an engineer", NULL);
    /* Line 313 */ ERR_X_Error(AI_gi_DynAINodeLevel[0] < 6000, "Too Many functions called. See an engineer.", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   465500: 56                           	pushl	%esi
     *   465501: 8b 74 24 08                  	movl	8(%esp), %esi
     *   465505: 80 7e 07 1f                  	cmpb	$31, 7(%esi)
     *   465509: 0f 84 6d 01 00 00            	je	0x46567c <.text+0x6467c>
     *   46550f: 55                           	pushl	%ebp
     *   465510: 8b 6c 24 14                  	movl	20(%esp), %ebp
     *   465514: 57                           	pushl	%edi
     *   465515: 8b 7c 24 14                  	movl	20(%esp), %edi
     *   465519: 8d a4 24 00 00 00 00         	leal	(%esp), %esp
     *   465520: 8a 46 07                     	movb	7(%esi), %al
     *   465523: 3c 01                        	cmpb	$1, %al
     *   465525: 75 77                        	jne	0x46559e <.text+0x6459e>
     *   465527: 85 ff                        	testl	%edi, %edi
     *   465529: 74 17                        	je	0x465542 <.text+0x64542>
     *   46552b: 66 83 7e 04 26               	cmpw	$38, 4(%esi)
     *   465530: 75 10                        	jne	0x465542 <.text+0x64542>
     *   465532: 8b 47 04                     	movl	4(%edi), %eax
     *   465535: 8b 0c a8                     	movl	(%eax,%ebp,4), %ecx
     *   465538: 8b 51 08                     	movl	8(%ecx), %edx
     *   46553b: 01 16                        	addl	%edx, (%esi)
     *   46553d: e9 f6 00 00 00               	jmp	0x465638 <.text+0x64638>
     *   465542: 0f bf 46 04                  	movswl	4(%esi), %eax
     *   465546: 83 c0 d9                     	addl	$-39, %eax
     *   465549: 83 f8 08                     	cmpl	$8, %eax
     *   46554c: 77 1a                        	ja	0x465568 <.text+0x64568>
     *   46554e: 0f b6 80 88 56 46 00         	movzbl	4609672(%eax), %eax
     *   465555: ff 24 85 80 56 46 00         	jmpl	*4609664(,%eax,4)
     *   46555c: 8b 0e                        	movl	(%esi), %ecx
     *   46555e: 56                           	pushl	%esi
     *   46555f: 51                           	pushl	%ecx
     *   465560: e8 6b 5d 08 00               	calll	0x4eb2d0 <_SND_fn_vSynchroTimer@0>
     *   465565: 83 c4 08                     	addl	$8, %esp
     *   465568: 0f bf 46 04                  	movswl	4(%esi), %eax
     *   46556c: 8b 16                        	movl	(%esi), %edx
     *   46556e: 8d 48 d9                     	leal	-39(%eax), %ecx
     *   465571: 83 f9 08                     	cmpl	$8, %ecx
     *   465574: 77 1f                        	ja	0x465595 <.text+0x64595>
     *   465576: 0f b6 89 9c 56 46 00         	movzbl	4609692(%ecx), %ecx
     *   46557d: ff 24 8d 94 56 46 00         	jmpl	*4609684(,%ecx,4)
     *   465584: 52                           	pushl	%edx
     *   465585: 50                           	pushl	%eax
     *   465586: e8 65 fe ff ff               	calll	0x4653f0 <.text+0x643f0>
     *   46558b: 83 c4 08                     	addl	$8, %esp
     *   46558e: 89 06                        	movl	%eax, (%esi)
     *   465590: e9 a3 00 00 00               	jmp	0x465638 <.text+0x64638>
     *   465595: 8b c2                        	movl	%edx, %eax
     *   465597: 89 06                        	movl	%eax, (%esi)
     *   465599: e9 9a 00 00 00               	jmp	0x465638 <.text+0x64638>
     *   46559e: 3c 1b                        	cmpb	$27, %al
     *   4655a0: 75 57                        	jne	0x4655f9 <.text+0x645f9>
     *   4655a2: 66 83 7e 04 00               	cmpw	$0, 4(%esi)
     *   4655a7: 7d 22                        	jge	0x4655cb <.text+0x645cb>
     *   4655a9: 6a 01                        	pushl	$1
     *   4655ab: 6a 00                        	pushl	$0
     * ... (118 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00465E17 - 0x00466FFC (Size: 4581 bytes)
 * Assertion line 1305: 0 | Message: AI_ul_CallbackLoadVars: Unsupported type
 * --------------------------------------------------------------------------- */
void sub_00465E17(void)
{
    /* Line 1305 */ ERR_X_Error(0, "AI_ul_CallbackLoadVars: Unsupported type", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   465e17: f7 e1                        	mull	%ecx
     *   465e19: c1 ea 05                     	shrl	$5, %edx
     *   465e1c: 33 f6                        	xorl	%esi, %esi
     *   465e1e: 85 d2                        	testl	%edx, %edx
     *   465e20: 76 1d                        	jbe	0x465e3f <.text+0x64e3f>
     *   465e22: 8b fa                        	movl	%edx, %edi
     *   465e24: 6a 02                        	pushl	$2
     *   465e26: 8d 44 24 18                  	leal	24(%esp), %eax
     *   465e2a: 6a 00                        	pushl	$0
     *   465e2c: 50                           	pushl	%eax
     *   465e2d: e8 ee 44 fc ff               	calll	0x42a320 <.text+0x29320>
     *   465e32: 83 c4 0c                     	addl	$12, %esp
     *   465e35: 85 f6                        	testl	%esi, %esi
     *   465e37: 74 03                        	je	0x465e3c <.text+0x64e3c>
     *   465e39: 83 c6 28                     	addl	$40, %esi
     *   465e3c: 4f                           	decl	%edi
     *   465e3d: 75 e5                        	jne	0x465e24 <.text+0x64e24>
     *   465e3f: e8 5c 00 fc ff               	calll	0x425ea0 <.text+0x24ea0>
     *   465e44: 3b 05 ec e1 7f 00            	cmpl	8380908, %eax
     *   465e4a: 75 08                        	jne	0x465e54 <.text+0x64e54>
     *   465e4c: 8b 0b                        	movl	(%ebx), %ecx
     *   465e4e: 89 0d a0 3b ac 00            	movl	%ecx, 11287456
     *   465e54: 5f                           	popl	%edi
     *   465e55: 5e                           	popl	%esi
     *   465e56: 8b c3                        	movl	%ebx, %eax
     *   465e58: 5b                           	popl	%ebx
     *   465e59: 8b e5                        	movl	%ebp, %esp
     *   465e5b: 5d                           	popl	%ebp
     *   465e5c: c3                           	retl
     *   465e5d: 68 80 e8 7a 00               	pushl	$8054912                # imm = 0x7AE880
     *   465e62: 8d 4c 24 24                  	leal	36(%esp), %ecx
     *   465e66: e8 a5 43 1f 00               	calll	0x65a210 <_SND_fn_vSynchroTimer@0+0x16ef40>
     *   465e6b: b9 00 04 00 00               	movl	$1024, %ecx             # imm = 0x400
     *   465e70: 8d 74 24 20                  	leal	32(%esp), %esi
     *   465e74: 8d bc 24 20 10 00 00         	leal	4128(%esp), %edi
     *   465e7b: f3 a5                        	rep		movsl	(%esi), %es:(%edi)
     *   465e7d: 68 70 fa 7e 00               	pushl	$8321648                # imm = 0x7EFA70
     *   465e82: 8d 8c 24 24 10 00 00         	leal	4132(%esp), %ecx
     *   465e89: 51                           	pushl	%ecx
     *   465e8a: e8 34 7b 2c 00               	calll	0x72d9c3 <_SND_fn_bInitMallocSnd@0+0x53d3>
     *   465e8f: cc                           	int3
     *   465e90: 55                           	pushl	%ebp
     *   465e91: 8b ec                        	movl	%esp, %ebp
     *   465e93: 83 e4 f8                     	andl	$-8, %esp
     *   465e96: b8 4c 20 00 00               	movl	$8268, %eax             # imm = 0x204C
     *   465e9b: e8 e0 96 2c 00               	calll	0x72f580 <_SND_fn_bInitMallocSnd@0+0x6f90>
     *   465ea0: a1 24 87 80 00               	movl	8423204, %eax
     *   465ea5: 53                           	pushl	%ebx
     *   465ea6: 89 84 24 4c 20 00 00         	movl	%eax, 8268(%esp)
     *   465ead: a1 c0 53 ae 00               	movl	11424704, %eax
     *   465eb2: 85 c0                        	testl	%eax, %eax
     *   465eb4: 56                           	pushl	%esi
     *   465eb5: 57                           	pushl	%edi
     *   465eb6: 75 0a                        	jne	0x465ec2 <.text+0x64ec2>
     * ... (1365 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00466C30 - 0x00466FFC (Size: 972 bytes)
 * Assertion line 1801: AI_i_DynAIFunctionTTLevel < 4096 | Message: AI Engine Error: Too many Function defined
 * --------------------------------------------------------------------------- */
void sub_00466C30(void)
{
    /* Line 1801 */ ERR_X_Error(AI_i_DynAIFunctionTTLevel < 4096, "AI Engine Error: Too many Function defined", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   466c30: a1 30 59 81 00               	movl	8476976, %eax
     *   466c35: 83 ec 6c                     	subl	$108, %esp
     *   466c38: 85 c0                        	testl	%eax, %eax
     *   466c3a: 53                           	pushl	%ebx
     *   466c3b: 55                           	pushl	%ebp
     *   466c3c: 56                           	pushl	%esi
     *   466c3d: 57                           	pushl	%edi
     *   466c3e: bd 02 00 00 00               	movl	$2, %ebp
     *   466c43: 74 0c                        	je	0x466c51 <.text+0x65c51>
     *   466c45: 39 2d f4 29 9e 00            	cmpl	%ebp, 10365428
     *   466c4b: 0f 84 4c 02 00 00            	je	0x466e9d <.text+0x65e9d>
     *   466c51: 8b b4 24 80 00 00 00         	movl	128(%esp), %esi
     *   466c58: 8d 44 24 10                  	leal	16(%esp), %eax
     *   466c5c: 50                           	pushl	%eax
     *   466c5d: 68 e0 05 7b 00               	pushl	$8062432                # imm = 0x7B05E0
     *   466c62: 56                           	pushl	%esi
     *   466c63: c7 44 24 1c 00 00 00 00      	movl	$0, 28(%esp)
     *   466c6b: e8 f0 7c 2c 00               	calll	0x72e960 <_SND_fn_bInitMallocSnd@0+0x6370>
     *   466c70: 6a 0a                        	pushl	$10
     *   466c72: 56                           	pushl	%esi
     *   466c73: e8 b8 77 2c 00               	calll	0x72e430 <_SND_fn_bInitMallocSnd@0+0x5e40>
     *   466c78: 83 c4 14                     	addl	$20, %esp
     *   466c7b: 85 c0                        	testl	%eax, %eax
     *   466c7d: 0f 84 fb 01 00 00            	je	0x466e7e <.text+0x65e7e>
     *   466c83: 6a 0a                        	pushl	$10
     *   466c85: 56                           	pushl	%esi
     *   466c86: e8 a5 77 2c 00               	calll	0x72e430 <_SND_fn_bInitMallocSnd@0+0x5e40>
     *   466c8b: 8b f0                        	movl	%eax, %esi
     *   466c8d: 8b 44 24 18                  	movl	24(%esp), %eax
     *   466c91: 83 c4 08                     	addl	$8, %esp
     *   466c94: 46                           	incl	%esi
     *   466c95: 48                           	decl	%eax
     *   466c96: 75 31                        	jne	0x466cc9 <.text+0x65cc9>
     *   466c98: 6a 0a                        	pushl	$10
     *   466c9a: 56                           	pushl	%esi
     *   466c9b: e8 90 77 2c 00               	calll	0x72e430 <_SND_fn_bInitMallocSnd@0+0x5e40>
     *   466ca0: 83 c4 08                     	addl	$8, %esp
     *   466ca3: 85 c0                        	testl	%eax, %eax
     *   466ca5: 0f 84 47 03 00 00            	je	0x466ff2 <.text+0x65ff2>
     *   466cab: 6a 0a                        	pushl	$10
     *   466cad: 6a 0a                        	pushl	$10
     *   466caf: 56                           	pushl	%esi
     *   466cb0: e8 7b 77 2c 00               	calll	0x72e430 <_SND_fn_bInitMallocSnd@0+0x5e40>
     *   466cb5: 83 c4 08                     	addl	$8, %esp
     *   466cb8: 50                           	pushl	%eax
     *   466cb9: e8 72 77 2c 00               	calll	0x72e430 <_SND_fn_bInitMallocSnd@0+0x5e40>
     *   466cbe: 83 c4 08                     	addl	$8, %esp
     *   466cc1: 85 c0                        	testl	%eax, %eax
     *   466cc3: 0f 84 29 03 00 00            	je	0x466ff2 <.text+0x65ff2>
     *   466cc9: 8b 44 24 10                  	movl	16(%esp), %eax
     *   466ccd: 48                           	decl	%eax
     *   466cce: 0f 85 c9 01 00 00            	jne	0x466e9d <.text+0x65e9d>
     *   466cd4: 6a 0a                        	pushl	$10
     *   466cd6: 56                           	pushl	%esi
     * ... (255 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00467000 - 0x0046705E (Size: 94 bytes)
 * Assertion line 1044: !sz_Error | Message: None
 * --------------------------------------------------------------------------- */
void sub_00467000(void)
{
    /* Line 1044 */ ERR_X_Error(!sz_Error, "Unknown error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   467000: 51                           	pushl	%ecx
     *   467001: 57                           	pushl	%edi
     *   467002: 8b 7c 24 0c                  	movl	12(%esp), %edi
     *   467006: 6a 01                        	pushl	$1
     *   467008: 8d 44 24 08                  	leal	8(%esp), %eax
     *   46700c: 50                           	pushl	%eax
     *   46700d: 57                           	pushl	%edi
     *   46700e: c7 44 24 10 00 00 00 00      	movl	$0, 16(%esp)
     *   467016: e8 35 15 fc ff               	calll	0x428550 <.text+0x27550>
     *   46701b: 8b 4c 24 10                  	movl	16(%esp), %ecx
     *   46701f: 83 c4 0c                     	addl	$12, %esp
     *   467022: 85 c9                        	testl	%ecx, %ecx
     *   467024: 74 33                        	je	0x467059 <.text+0x66059>
     *   467026: 56                           	pushl	%esi
     *   467027: 50                           	pushl	%eax
     *   467028: e8 03 fc ff ff               	calll	0x466c30 <.text+0x65c30>
     *   46702d: 83 c4 04                     	addl	$4, %esp
     *   467030: 8b f0                        	movl	%eax, %esi
     *   467032: e8 b9 11 fc ff               	calll	0x4281f0 <.text+0x271f0>
     *   467037: 85 f6                        	testl	%esi, %esi
     *   467039: 74 1d                        	je	0x467058 <.text+0x66058>
     *   46703b: 6a 01                        	pushl	$1
     *   46703d: 57                           	pushl	%edi
     *   46703e: 56                           	pushl	%esi
     *   46703f: 68 ec 05 7b 00               	pushl	$8062444                # imm = 0x7B05EC
     *   467044: 68 14 04 00 00               	pushl	$1044                   # imm = 0x414
     *   467049: 68 f8 03 7b 00               	pushl	$8061944                # imm = 0x7B03F8
     *   46704e: 6a 00                        	pushl	$0
     *   467050: e8 7b 94 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   467055: 83 c4 1c                     	addl	$28, %esp
     *   467058: 5e                           	popl	%esi
     *   467059: 33 c0                        	xorl	%eax, %eax
     *   46705b: 5f                           	popl	%edi
     *   46705c: 59                           	popl	%ecx
     *   46705d: c3                           	retl
     */
}
