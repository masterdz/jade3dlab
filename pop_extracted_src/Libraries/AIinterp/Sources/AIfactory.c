/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/AIinterp/Sources/AIfactory.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 23
 * Unique Functions Mapped: 7
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x00469C10 - 0x00469C7C (Size: 108 bytes)
 * Assertion line 239: _pst_FactoryData | Message: No Factory Data allocated. See an engineer
 * Assertion line 240: _v_Position | Message: Invalid Position to save
 * --------------------------------------------------------------------------- */
void sub_00469C10(void)
{
    /* Line 239 */ ERR_X_Error(_pst_FactoryData, "No Factory Data allocated. See an engineer", NULL);
    /* Line 240 */ ERR_X_Error(_v_Position, "Invalid Position to save", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   469c10: 56                           	pushl	%esi
     *   469c11: 57                           	pushl	%edi
     *   469c12: 8b 7c 24 0c                  	movl	12(%esp), %edi
     *   469c16: 85 ff                        	testl	%edi, %edi
     *   469c18: 75 20                        	jne	0x469c3a <.text+0x68c3a>
     *   469c1a: 6a 01                        	pushl	$1
     *   469c1c: 57                           	pushl	%edi
     *   469c1d: 68 3c 08 7b 00               	pushl	$8063036                # imm = 0x7B083C
     *   469c22: 68 28 08 7b 00               	pushl	$8063016                # imm = 0x7B0828
     *   469c27: 68 ef 00 00 00               	pushl	$239
     *   469c2c: 68 00 08 7b 00               	pushl	$8062976                # imm = 0x7B0800
     *   469c31: 57                           	pushl	%edi
     *   469c32: e8 99 68 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   469c37: 83 c4 1c                     	addl	$28, %esp
     *   469c3a: 8b 74 24 10                  	movl	16(%esp), %esi
     *   469c3e: 85 f6                        	testl	%esi, %esi
     *   469c40: 75 20                        	jne	0x469c62 <.text+0x68c62>
     *   469c42: 6a 01                        	pushl	$1
     *   469c44: 56                           	pushl	%esi
     *   469c45: 68 e4 07 7b 00               	pushl	$8062948                # imm = 0x7B07E4
     *   469c4a: 68 d8 07 7b 00               	pushl	$8062936                # imm = 0x7B07D8
     *   469c4f: 68 f0 00 00 00               	pushl	$240
     *   469c54: 68 00 08 7b 00               	pushl	$8062976                # imm = 0x7B0800
     *   469c59: 56                           	pushl	%esi
     *   469c5a: e8 71 68 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   469c5f: 83 c4 1c                     	addl	$28, %esp
     *   469c62: 80 4f 20 08                  	orb	$8, 32(%edi)
     *   469c66: 8b 06                        	movl	(%esi), %eax
     *   469c68: 83 c7 04                     	addl	$4, %edi
     *   469c6b: 89 07                        	movl	%eax, (%edi)
     *   469c6d: 8b 4e 04                     	movl	4(%esi), %ecx
     *   469c70: 89 4f 04                     	movl	%ecx, 4(%edi)
     *   469c73: 8b 56 08                     	movl	8(%esi), %edx
     *   469c76: 89 57 08                     	movl	%edx, 8(%edi)
     *   469c79: 5f                           	popl	%edi
     *   469c7a: 5e                           	popl	%esi
     *   469c7b: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00469C80 - 0x00469CEC (Size: 108 bytes)
 * Assertion line 251: _pst_FactoryData | Message: No Factory Data allocated. See an engineer
 * Assertion line 252: _v_Sight | Message: Invalid Sighting to save
 * --------------------------------------------------------------------------- */
void sub_00469C80(void)
{
    /* Line 251 */ ERR_X_Error(_pst_FactoryData, "No Factory Data allocated. See an engineer", NULL);
    /* Line 252 */ ERR_X_Error(_v_Sight, "Invalid Sighting to save", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   469c80: 56                           	pushl	%esi
     *   469c81: 57                           	pushl	%edi
     *   469c82: 8b 7c 24 0c                  	movl	12(%esp), %edi
     *   469c86: 85 ff                        	testl	%edi, %edi
     *   469c88: 75 20                        	jne	0x469caa <.text+0x68caa>
     *   469c8a: 6a 01                        	pushl	$1
     *   469c8c: 57                           	pushl	%edi
     *   469c8d: 68 3c 08 7b 00               	pushl	$8063036                # imm = 0x7B083C
     *   469c92: 68 28 08 7b 00               	pushl	$8063016                # imm = 0x7B0828
     *   469c97: 68 fb 00 00 00               	pushl	$251
     *   469c9c: 68 00 08 7b 00               	pushl	$8062976                # imm = 0x7B0800
     *   469ca1: 57                           	pushl	%edi
     *   469ca2: e8 29 68 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   469ca7: 83 c4 1c                     	addl	$28, %esp
     *   469caa: 8b 74 24 10                  	movl	16(%esp), %esi
     *   469cae: 85 f6                        	testl	%esi, %esi
     *   469cb0: 75 20                        	jne	0x469cd2 <.text+0x68cd2>
     *   469cb2: 6a 01                        	pushl	$1
     *   469cb4: 56                           	pushl	%esi
     *   469cb5: 68 74 08 7b 00               	pushl	$8063092                # imm = 0x7B0874
     *   469cba: 68 68 08 7b 00               	pushl	$8063080                # imm = 0x7B0868
     *   469cbf: 68 fc 00 00 00               	pushl	$252
     *   469cc4: 68 00 08 7b 00               	pushl	$8062976                # imm = 0x7B0800
     *   469cc9: 56                           	pushl	%esi
     *   469cca: e8 01 68 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   469ccf: 83 c4 1c                     	addl	$28, %esp
     *   469cd2: 80 4f 20 10                  	orb	$16, 32(%edi)
     *   469cd6: 8b 06                        	movl	(%esi), %eax
     *   469cd8: 83 c7 10                     	addl	$16, %edi
     *   469cdb: 89 07                        	movl	%eax, (%edi)
     *   469cdd: 8b 4e 04                     	movl	4(%esi), %ecx
     *   469ce0: 89 4f 04                     	movl	%ecx, 4(%edi)
     *   469ce3: 8b 56 08                     	movl	8(%esi), %edx
     *   469ce6: 89 57 08                     	movl	%edx, 8(%edi)
     *   469ce9: 5f                           	popl	%edi
     *   469cea: 5e                           	popl	%esi
     *   469ceb: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00469CF0 - 0x00469D26 (Size: 54 bytes)
 * Assertion line 263: _pst_FactoryData | Message: No Factory Data allocated. See an engineer
 * --------------------------------------------------------------------------- */
void sub_00469CF0(void)
{
    /* Line 263 */ ERR_X_Error(_pst_FactoryData, "No Factory Data allocated. See an engineer", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   469cf0: 56                           	pushl	%esi
     *   469cf1: 8b 74 24 08                  	movl	8(%esp), %esi
     *   469cf5: 85 f6                        	testl	%esi, %esi
     *   469cf7: 75 20                        	jne	0x469d19 <.text+0x68d19>
     *   469cf9: 6a 01                        	pushl	$1
     *   469cfb: 56                           	pushl	%esi
     *   469cfc: 68 3c 08 7b 00               	pushl	$8063036                # imm = 0x7B083C
     *   469d01: 68 28 08 7b 00               	pushl	$8063016                # imm = 0x7B0828
     *   469d06: 68 07 01 00 00               	pushl	$263                    # imm = 0x107
     *   469d0b: 68 00 08 7b 00               	pushl	$8062976                # imm = 0x7B0800
     *   469d10: 56                           	pushl	%esi
     *   469d11: e8 ba 67 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   469d16: 83 c4 1c                     	addl	$28, %esp
     *   469d19: 80 4e 20 20                  	orb	$32, 32(%esi)
     *   469d1d: 8b 44 24 0c                  	movl	12(%esp), %eax
     *   469d21: 89 46 1c                     	movl	%eax, 28(%esi)
     *   469d24: 5e                           	popl	%esi
     *   469d25: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00469D30 - 0x00469D9F (Size: 111 bytes)
 * Assertion line 274: _pst_FactoryData | Message: No Factory Data allocated. See an engineer
 * Assertion line 275: ((_i_Offset >= 0) && (_i_Offset <= 6)) | Message: Incorrect offset
 * Assertion line 286: _pst_FactoryData | Message: No Factory Data allocated. See an engineer
 * Assertion line 287: ((_i_Offset >= 0) && (_i_Offset <= 6)) | Message: Incorrect offset
 * Assertion line 297: _pst_FactoryData | Message: No Factory Data allocated. See an engineer
 * Assertion line 298: _v_Position | Message: Invalid Position to save
 * Assertion line 299: _pst_FactoryData->uc_Flag & 0x08 | Message: No position available in the factory
 * Assertion line 309: _pst_FactoryData | Message: No Factory Data allocated. See an engineer
 * Assertion line 310: _v_Sight | Message: Invalid Sighting to save
 * Assertion line 311: _pst_FactoryData->uc_Flag & 0x10 | Message: No sight available in the factory
 * Assertion line 321: _pst_FactoryData | Message: No Factory Data allocated. See an engineer
 * Assertion line 322: _pst_FactoryData->uc_Flag & 0x20 | Message: No Integer available in the factory
 * --------------------------------------------------------------------------- */
void sub_00469D30(void)
{
    /* Line 274 */ ERR_X_Error(_pst_FactoryData, "No Factory Data allocated. See an engineer", NULL);
    /* Line 275 */ ERR_X_Error(((_i_Offset >= 0) && (_i_Offset <= 6)), "Incorrect offset", NULL);
    /* Line 286 */ ERR_X_Error(_pst_FactoryData, "No Factory Data allocated. See an engineer", NULL);
    /* Line 287 */ ERR_X_Error(((_i_Offset >= 0) && (_i_Offset <= 6)), "Incorrect offset", NULL);
    /* Line 297 */ ERR_X_Error(_pst_FactoryData, "No Factory Data allocated. See an engineer", NULL);
    /* Line 298 */ ERR_X_Error(_v_Position, "Invalid Position to save", NULL);
    /* Line 299 */ ERR_X_Error(_pst_FactoryData->uc_Flag & 0x08, "No position available in the factory", NULL);
    /* Line 309 */ ERR_X_Error(_pst_FactoryData, "No Factory Data allocated. See an engineer", NULL);
    /* Line 310 */ ERR_X_Error(_v_Sight, "Invalid Sighting to save", NULL);
    /* Line 311 */ ERR_X_Error(_pst_FactoryData->uc_Flag & 0x10, "No sight available in the factory", NULL);
    /* Line 321 */ ERR_X_Error(_pst_FactoryData, "No Factory Data allocated. See an engineer", NULL);
    /* Line 322 */ ERR_X_Error(_pst_FactoryData->uc_Flag & 0x20, "No Integer available in the factory", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   469d30: 56                           	pushl	%esi
     *   469d31: 57                           	pushl	%edi
     *   469d32: 8b 7c 24 0c                  	movl	12(%esp), %edi
     *   469d36: 85 ff                        	testl	%edi, %edi
     *   469d38: 75 20                        	jne	0x469d5a <.text+0x68d5a>
     *   469d3a: 6a 01                        	pushl	$1
     *   469d3c: 57                           	pushl	%edi
     *   469d3d: 68 3c 08 7b 00               	pushl	$8063036                # imm = 0x7B083C
     *   469d42: 68 28 08 7b 00               	pushl	$8063016                # imm = 0x7B0828
     *   469d47: 68 12 01 00 00               	pushl	$274                    # imm = 0x112
     *   469d4c: 68 00 08 7b 00               	pushl	$8062976                # imm = 0x7B0800
     *   469d51: 57                           	pushl	%edi
     *   469d52: e8 79 67 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   469d57: 83 c4 1c                     	addl	$28, %esp
     *   469d5a: 8b 74 24 10                  	movl	16(%esp), %esi
     *   469d5e: 85 f6                        	testl	%esi, %esi
     *   469d60: 7c 05                        	jl	0x469d67 <.text+0x68d67>
     *   469d62: 83 fe 06                     	cmpl	$6, %esi
     *   469d65: 7e 2d                        	jle	0x469d94 <.text+0x68d94>
     *   469d67: 6a 01                        	pushl	$1
     *   469d69: 6a 00                        	pushl	$0
     *   469d6b: 68 b8 08 7b 00               	pushl	$8063160                # imm = 0x7B08B8
     *   469d70: 68 90 08 7b 00               	pushl	$8063120                # imm = 0x7B0890
     *   469d75: 68 13 01 00 00               	pushl	$275                    # imm = 0x113
     *   469d7a: 68 00 08 7b 00               	pushl	$8062976                # imm = 0x7B0800
     *   469d7f: 6a 00                        	pushl	$0
     *   469d81: e8 4a 67 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   469d86: 8b 44 24 30                  	movl	48(%esp), %eax
     *   469d8a: 83 c4 1c                     	addl	$28, %esp
     *   469d8d: 89 44 b7 04                  	movl	%eax, 4(%edi,%esi,4)
     *   469d91: 5f                           	popl	%edi
     *   469d92: 5e                           	popl	%esi
     *   469d93: c3                           	retl
     *   469d94: 8b 4c 24 14                  	movl	20(%esp), %ecx
     *   469d98: 89 4c b7 04                  	movl	%ecx, 4(%edi,%esi,4)
     *   469d9c: 5f                           	popl	%edi
     *   469d9d: 5e                           	popl	%esi
     *   469d9e: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x00469F90 - 0x0046A063 (Size: 211 bytes)
 * Assertion line 332: _pst_FactoryData | Message: No Factory Data allocated. See an engineer
 * Assertion line 333: ((_i_Offset >= 0) && (_i_Offset <= 6)) | Message: Incorrect offset
 * Assertion line 343: _pst_FactoryData | Message: No Factory Data allocated. See an engineer
 * Assertion line 344: ((_i_Offset >= 0) && (_i_Offset <= 6)) | Message: Incorrect offset
 * --------------------------------------------------------------------------- */
void sub_00469F90(void)
{
    /* Line 332 */ ERR_X_Error(_pst_FactoryData, "No Factory Data allocated. See an engineer", NULL);
    /* Line 333 */ ERR_X_Error(((_i_Offset >= 0) && (_i_Offset <= 6)), "Incorrect offset", NULL);
    /* Line 343 */ ERR_X_Error(_pst_FactoryData, "No Factory Data allocated. See an engineer", NULL);
    /* Line 344 */ ERR_X_Error(((_i_Offset >= 0) && (_i_Offset <= 6)), "Incorrect offset", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   469f90: 56                           	pushl	%esi
     *   469f91: 57                           	pushl	%edi
     *   469f92: 8b 7c 24 0c                  	movl	12(%esp), %edi
     *   469f96: 85 ff                        	testl	%edi, %edi
     *   469f98: 75 20                        	jne	0x469fba <.text+0x68fba>
     *   469f9a: 6a 01                        	pushl	$1
     *   469f9c: 57                           	pushl	%edi
     *   469f9d: 68 3c 08 7b 00               	pushl	$8063036                # imm = 0x7B083C
     *   469fa2: 68 28 08 7b 00               	pushl	$8063016                # imm = 0x7B0828
     *   469fa7: 68 4c 01 00 00               	pushl	$332                    # imm = 0x14C
     *   469fac: 68 00 08 7b 00               	pushl	$8062976                # imm = 0x7B0800
     *   469fb1: 57                           	pushl	%edi
     *   469fb2: e8 19 65 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   469fb7: 83 c4 1c                     	addl	$28, %esp
     *   469fba: 8b 74 24 10                  	movl	16(%esp), %esi
     *   469fbe: 85 f6                        	testl	%esi, %esi
     *   469fc0: 7c 05                        	jl	0x469fc7 <.text+0x68fc7>
     *   469fc2: 83 fe 06                     	cmpl	$6, %esi
     *   469fc5: 7e 22                        	jle	0x469fe9 <.text+0x68fe9>
     *   469fc7: 6a 01                        	pushl	$1
     *   469fc9: 6a 00                        	pushl	$0
     *   469fcb: 68 b8 08 7b 00               	pushl	$8063160                # imm = 0x7B08B8
     *   469fd0: 68 90 08 7b 00               	pushl	$8063120                # imm = 0x7B0890
     *   469fd5: 68 4d 01 00 00               	pushl	$333                    # imm = 0x14D
     *   469fda: 68 00 08 7b 00               	pushl	$8062976                # imm = 0x7B0800
     *   469fdf: 6a 00                        	pushl	$0
     *   469fe1: e8 ea 64 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   469fe6: 83 c4 1c                     	addl	$28, %esp
     *   469fe9: 8b 44 b7 04                  	movl	4(%edi,%esi,4), %eax
     *   469fed: 5f                           	popl	%edi
     *   469fee: 5e                           	popl	%esi
     *   469fef: c3                           	retl
     *   469ff0: 56                           	pushl	%esi
     *   469ff1: 57                           	pushl	%edi
     *   469ff2: 8b 7c 24 0c                  	movl	12(%esp), %edi
     *   469ff6: 85 ff                        	testl	%edi, %edi
     *   469ff8: 75 20                        	jne	0x46a01a <.text+0x6901a>
     *   469ffa: 6a 01                        	pushl	$1
     *   469ffc: 57                           	pushl	%edi
     *   469ffd: 68 3c 08 7b 00               	pushl	$8063036                # imm = 0x7B083C
     *   46a002: 68 28 08 7b 00               	pushl	$8063016                # imm = 0x7B0828
     *   46a007: 68 57 01 00 00               	pushl	$343                    # imm = 0x157
     *   46a00c: 68 00 08 7b 00               	pushl	$8062976                # imm = 0x7B0800
     *   46a011: 57                           	pushl	%edi
     *   46a012: e8 b9 64 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   46a017: 83 c4 1c                     	addl	$28, %esp
     *   46a01a: 8b 74 24 10                  	movl	16(%esp), %esi
     *   46a01e: 85 f6                        	testl	%esi, %esi
     *   46a020: 7c 05                        	jl	0x46a027 <.text+0x69027>
     *   46a022: 83 fe 06                     	cmpl	$6, %esi
     *   46a025: 7e 22                        	jle	0x46a049 <.text+0x69049>
     *   46a027: 6a 01                        	pushl	$1
     *   46a029: 6a 00                        	pushl	$0
     *   46a02b: 68 b8 08 7b 00               	pushl	$8063160                # imm = 0x7B08B8
     * ... (16 more instructions)
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x0046AB20 - 0x0046AB5E (Size: 62 bytes)
 * Assertion line 219: ul_Key != -1 | Message: Invalid Key used
 * --------------------------------------------------------------------------- */
void sub_0046AB20(void)
{
    /* Line 219 */ ERR_X_Error(ul_Key != -1, "Invalid Key used", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   46ab20: 56                           	pushl	%esi
     *   46ab21: 8b 74 24 08                  	movl	8(%esp), %esi
     *   46ab25: 83 fe ff                     	cmpl	$-1, %esi
     *   46ab28: 75 22                        	jne	0x46ab4c <.text+0x69b4c>
     *   46ab2a: 6a 01                        	pushl	$1
     *   46ab2c: 6a 00                        	pushl	$0
     *   46ab2e: 68 b8 09 7b 00               	pushl	$8063416                # imm = 0x7B09B8
     *   46ab33: 68 a8 09 7b 00               	pushl	$8063400                # imm = 0x7B09A8
     *   46ab38: 68 db 00 00 00               	pushl	$219
     *   46ab3d: 68 00 08 7b 00               	pushl	$8062976                # imm = 0x7B0800
     *   46ab42: 6a 00                        	pushl	$0
     *   46ab44: e8 87 59 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   46ab49: 83 c4 1c                     	addl	$28, %esp
     *   46ab4c: 8b 44 24 0c                  	movl	12(%esp), %eax
     *   46ab50: 6a 01                        	pushl	$1
     *   46ab52: 50                           	pushl	%eax
     *   46ab53: 56                           	pushl	%esi
     *   46ab54: e8 17 fe ff ff               	calll	0x46a970 <.text+0x69970>
     *   46ab59: 83 c4 0c                     	addl	$12, %esp
     *   46ab5c: 5e                           	popl	%esi
     *   46ab5d: c3                           	retl
     */
}

/* ---------------------------------------------------------------------------
 * Function at VA 0x0046AB60 - 0x0046AB9E (Size: 62 bytes)
 * Assertion line 229: ul_Key != -1 | Message: Invalid Key used
 * --------------------------------------------------------------------------- */
void sub_0046AB60(void)
{
    /* Line 229 */ ERR_X_Error(ul_Key != -1, "Invalid Key used", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 00401000 <.text>:
     *   46ab60: 56                           	pushl	%esi
     *   46ab61: 8b 74 24 08                  	movl	8(%esp), %esi
     *   46ab65: 83 fe ff                     	cmpl	$-1, %esi
     *   46ab68: 75 22                        	jne	0x46ab8c <.text+0x69b8c>
     *   46ab6a: 6a 01                        	pushl	$1
     *   46ab6c: 6a 00                        	pushl	$0
     *   46ab6e: 68 b8 09 7b 00               	pushl	$8063416                # imm = 0x7B09B8
     *   46ab73: 68 a8 09 7b 00               	pushl	$8063400                # imm = 0x7B09A8
     *   46ab78: 68 e5 00 00 00               	pushl	$229
     *   46ab7d: 68 00 08 7b 00               	pushl	$8062976                # imm = 0x7B0800
     *   46ab82: 6a 00                        	pushl	$0
     *   46ab84: e8 47 59 fb ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   46ab89: 83 c4 1c                     	addl	$28, %esp
     *   46ab8c: 8b 44 24 0c                  	movl	12(%esp), %eax
     *   46ab90: 6a 00                        	pushl	$0
     *   46ab92: 50                           	pushl	%eax
     *   46ab93: 56                           	pushl	%esi
     *   46ab94: e8 d7 fd ff ff               	calll	0x46a970 <.text+0x69970>
     *   46ab99: 83 c4 0c                     	addl	$12, %esp
     *   46ab9c: 5e                           	popl	%esi
     *   46ab9d: c3                           	retl
     */
}
