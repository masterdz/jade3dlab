/* ===========================================================================
 * RECONSTRUCTED SOURCE MODULE: Libraries/AIinterp/Sources/Events/EVEinit.c
 * Extracted from Prince of Persia (2003) executable: POP.EXE
 * Total Embedded Assertions: 2
 * Unique Functions Mapped: 1
 * =========================================================================== */

#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGcomp.h"

/* ---------------------------------------------------------------------------
 * Function at VA 0x0064BF20 - 0x0064BFE6 (Size: 198 bytes)
 * Assertion line 322: Unknown Event type in EVE_PreallocTrackEvent | Message: None
 * Assertion line 319: Unsupported event type in EVE_PreallocTrackEvent | Message: None
 * --------------------------------------------------------------------------- */
void sub_0064BF20(void)
{
    /* Line 322 */ ERR_X_Error(Unknown Event type in EVE_PreallocTrackEvent, "Unknown error", NULL);
    /* Line 319 */ ERR_X_Error(Unsupported event type in EVE_PreallocTrackEvent, "Unknown error", NULL);

    /* Disassembly & Logic Flow:
     * /Users/ibizaprint/Downloads/JadeEngine/POP.EXE:	file format coff-i386
     * Disassembly of section .text:
     * 004eb2d0 <_SND_fn_vSynchroTimer@0>:
     *   64bf20: 8b 44 24 0c                  	movl	12(%esp), %eax
     *   64bf24: 3d 00 02 00 00               	cmpl	$512, %eax              # imm = 0x200
     *   64bf29: 7f 50                        	jg	0x64bf7b <_SND_fn_vSynchroTimer@0+0x160cab>
     *   64bf2b: 0f 84 95 00 00 00            	je	0x64bfc6 <_SND_fn_vSynchroTimer@0+0x160cf6>
     *   64bf31: 83 e8 40                     	subl	$64, %eax
     *   64bf34: 0f 84 8c 00 00 00            	je	0x64bfc6 <_SND_fn_vSynchroTimer@0+0x160cf6>
     *   64bf3a: 83 e8 40                     	subl	$64, %eax
     *   64bf3d: 74 1f                        	je	0x64bf5e <_SND_fn_vSynchroTimer@0+0x160c8e>
     *   64bf3f: 2d 80 00 00 00               	subl	$128, %eax
     *   64bf44: 75 43                        	jne	0x64bf89 <_SND_fn_vSynchroTimer@0+0x160cb9>
     *   64bf46: 8b 44 24 14                  	movl	20(%esp), %eax
     *   64bf4a: 8b 4c 24 08                  	movl	8(%esp), %ecx
     *   64bf4e: 8b 54 24 04                  	movl	4(%esp), %edx
     *   64bf52: 50                           	pushl	%eax
     *   64bf53: 51                           	pushl	%ecx
     *   64bf54: 52                           	pushl	%edx
     *   64bf55: e8 06 2d 00 00               	calll	0x64ec60 <_SND_fn_vSynchroTimer@0+0x163990>
     *   64bf5a: 83 c4 0c                     	addl	$12, %esp
     *   64bf5d: c3                           	retl
     *   64bf5e: 8b 44 24 10                  	movl	16(%esp), %eax
     *   64bf62: 8b 4c 24 08                  	movl	8(%esp), %ecx
     *   64bf66: 8b 54 24 04                  	movl	4(%esp), %edx
     *   64bf6a: 50                           	pushl	%eax
     *   64bf6b: 68 80 00 00 00               	pushl	$128
     *   64bf70: 51                           	pushl	%ecx
     *   64bf71: 52                           	pushl	%edx
     *   64bf72: e8 69 17 00 00               	calll	0x64d6e0 <_SND_fn_vSynchroTimer@0+0x162410>
     *   64bf77: 83 c4 10                     	addl	$16, %esp
     *   64bf7a: c3                           	retl
     *   64bf7b: 3d 00 04 00 00               	cmpl	$1024, %eax             # imm = 0x400
     *   64bf80: 74 44                        	je	0x64bfc6 <_SND_fn_vSynchroTimer@0+0x160cf6>
     *   64bf82: 3d 00 10 00 00               	cmpl	$4096, %eax             # imm = 0x1000
     *   64bf87: 74 20                        	je	0x64bfa9 <_SND_fn_vSynchroTimer@0+0x160cd9>
     *   64bf89: 6a 01                        	pushl	$1
     *   64bf8b: 6a 00                        	pushl	$0
     *   64bf8d: 68 9c 52 7b 00               	pushl	$8082076                # imm = 0x7B529C
     *   64bf92: 6a 00                        	pushl	$0
     *   64bf94: 68 42 01 00 00               	pushl	$322                    # imm = 0x142
     *   64bf99: 68 6c 52 7b 00               	pushl	$8082028                # imm = 0x7B526C
     *   64bf9e: 6a 00                        	pushl	$0
     *   64bfa0: e8 2b 45 dd ff               	calll	0x4204d0 <.text+0x1f4d0>
     *   64bfa5: 83 c4 1c                     	addl	$28, %esp
     *   64bfa8: c3                           	retl
     *   64bfa9: 8b 44 24 14                  	movl	20(%esp), %eax
     *   64bfad: 8b 4c 24 10                  	movl	16(%esp), %ecx
     *   64bfb1: 8b 54 24 08                  	movl	8(%esp), %edx
     *   64bfb5: 50                           	pushl	%eax
     *   64bfb6: 8b 44 24 08                  	movl	8(%esp), %eax
     *   64bfba: 51                           	pushl	%ecx
     *   64bfbb: 52                           	pushl	%edx
     *   64bfbc: 50                           	pushl	%eax
     *   64bfbd: e8 ae 07 00 00               	calll	0x64c770 <_SND_fn_vSynchroTimer@0+0x1614a0>
     *   64bfc2: 83 c4 10                     	addl	$16, %esp
     *   64bfc5: c3                           	retl
     * ... (10 more instructions)
     */
}
