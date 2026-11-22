/* =======================================================================================================================
 *  BIGcooked.h
 *  Prince of Persia: Sands of Time & Warrior Within Cooked BigFile (v37 / v38) Container & Sub-Entry Subsystem
 * ======================================================================================================================= */

#pragma once

#ifndef __BIGCOOKED_H__
#define __BIGCOOKED_H__

#include "Precomp.h"
#include "BASe/BAStypes.h"
#include "BIGfiles/BIGdefs.h"
#include "BIGfiles/BIGfat.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Virtual position flag for cooked sub-entries (bit 31 set) */
#define BIG_C_CookedPosFlag     0x80000000
#define BIG_C_CookedMagic       0xEEFFC099

/*
 =======================================================================================================================
    Structure describing a sub-entry packed inside a cooked .bin container
 =======================================================================================================================
 */
typedef struct BIG_tdst_CookedSubEntry_
{
    BIG_KEY     ul_Key;             /* 32-bit Jade asset key (e.g. 0x2200492B for WOW, 0xCC0003FD for WOL, GAO, etc.) */
    ULONG       ul_BinPos;          /* File offset of the parent .bin container in the BigFile */
    BIG_KEY     ul_BinKey;          /* 32-bit key of the parent .bin container in the FAT (e.g. 0xFF02492B) */
    BIG_INDEX   ul_BinFatIndex;     /* FAT index of the parent .bin file */
    ULONG       ul_OffsetInBin;     /* Byte offset of asset payload inside uncompressed .bin */
    ULONG       ul_Size;            /* Byte size of uncompressed asset payload */
    ULONG       ul_Type;            /* 4-byte magic/type tag (e.g. 0x776F772E for .wow, 0x6F61672E for .gao) */
    ULONG       ul_NextInHash;      /* Hash table chain index */
} BIG_tdst_CookedSubEntry;

/*
 =======================================================================================================================
    Subsystem Interface
 =======================================================================================================================
 */
extern BOOL                     BIG_gb_IsCooked;
extern ULONG                    BIG_gul_CookedSubEntryCount;
extern BIG_tdst_CookedSubEntry  *BIG_gast_CookedSubEntries;

BOOL                            BIG_b_IsCookedBigFile(void);
BOOL                            BIG_b_DetectCookedBigFile(void);
void                            BIG_Cooked_Init(void);
void                            BIG_Cooked_Close(void);

ULONG                           BIG_Cooked_SearchKeyToPos(BIG_KEY _ul_Key);
BIG_INDEX                       BIG_Cooked_SearchKeyToFat(BIG_KEY _ul_Key);
char*                           BIG_pc_Cooked_ReadFileTmp(ULONG _ul_Pos, ULONG *_pul_Length);
BOOL                            BIG_b_Cooked_IsFileExtension(BIG_INDEX _ul_File, char *_psz_Ext);
BIG_tdst_CookedSubEntry*        BIG_pst_Cooked_FindSubEntry(BIG_KEY _ul_Key);

#ifdef __cplusplus
}
#endif

#endif /* __BIGCOOKED_H__ */

