/* =======================================================================================================================
 *  BIGcooked.c
 *  Prince of Persia: Sands of Time & Warrior Within Cooked BigFile (v37 / v38) Container & Sub-Entry Subsystem
 * ======================================================================================================================= */

#include "Precomp.h"
#include "BASe/MEMory/MEM.h"
#include "BASe/CLIbrary/CLIstr.h"
#include "BASe/CLIbrary/CLImem.h"
#include "BASe/ERRors/ERRasser.h"
#include "BIGfiles/BIGcooked.h"
#include "BIGfiles/BIGread.h"
#include "BIGfiles/BIGkey.h"
#include "BIGfiles/BIGfat.h"
#include "BIGfiles/BIGspecial.h"
#include "BIGfiles/VERsion/VERsion_Number.h"

#define BIG_COOKED_HASH_SIZE    65536
#define BIG_COOKED_HASH_MASK    (BIG_COOKED_HASH_SIZE - 1)
#define BIG_COOKED_BIN_CACHE    16

/* Global Subsystem State */
BOOL                            BIG_gb_IsCooked = FALSE;
ULONG                           BIG_gul_CookedSubEntryCount = 0;
BIG_tdst_CookedSubEntry         *BIG_gast_CookedSubEntries = NULL;
static ULONG                    s_ul_CookedCapacity = 0;
static ULONG                    s_aul_CookedHash[BIG_COOKED_HASH_SIZE];

/* Decompressed .bin Cache Entry */
typedef struct BIG_tdst_CookedBinCacheEntry_
{
    BIG_KEY     ul_BinKey;
    ULONG       ul_BinPos;
    char        *pc_Data;
    ULONG       ul_Size;
    ULONG       ul_AccessTick;
} BIG_tdst_CookedBinCacheEntry;

static BIG_tdst_CookedBinCacheEntry s_ast_BinCache[BIG_COOKED_BIN_CACHE];
static ULONG                        s_ul_CacheClock = 0;

/*
 =======================================================================================================================
    Hash Function for 32-bit Jade Keys
 =======================================================================================================================
 */
static _inline_ ULONG BIG_Cooked_HashKey(BIG_KEY _ul_Key)
{
    ULONG h = _ul_Key;
    h ^= (h >> 16);
    h *= 0x45d9f3b;
    h ^= (h >> 16);
    return h & BIG_COOKED_HASH_MASK;
}

/*
 =======================================================================================================================
    Aim:    Determine if the current BigFile is a Prince of Persia cooked container format.
 =======================================================================================================================
 */
BOOL BIG_b_IsCookedBigFile(void)
{
    return BIG_gb_IsCooked;
}

/*
 =======================================================================================================================
    Aim:    Detect whether the loaded BigFile contains consolidated .bin packages (Prince of Persia retail).
 =======================================================================================================================
 */
BOOL BIG_b_DetectCookedBigFile(void)
{
    ULONG i, ul_BinCount = 0;

    if(BIG_Version() == BIG_Cu4_Version_POP || BIG_Version() == BIG_Cu4_Version_POP2)
        return TRUE;

    for(i = 0; i < BIG_gst.st_ToSave.ul_MaxFile; i++)
    {
        char *psz_Name = BIG_NameFile(i);
        if(psz_Name && *psz_Name)
        {
            if(strstr(psz_Name, ".bin") || strstr(psz_Name, "_wow_") || strstr(psz_Name, "_wol_"))
            {
                ul_BinCount++;
                if(ul_BinCount >= 5) return TRUE;
            }
        }
    }

    return FALSE;
}

/*
 =======================================================================================================================
    Aim:    Add a sub-entry to the cooked index.
 =======================================================================================================================
 */
static void BIG_Cooked_AddSubEntry(BIG_KEY _ul_Key, ULONG _ul_BinPos, BIG_KEY _ul_BinKey, BIG_INDEX _ul_BinFatIndex,
                                   ULONG _ul_Offset, ULONG _ul_Size, ULONG _ul_Type)
{
    ULONG ul_Idx, ul_Bucket;

    if(_ul_Key == 0 || _ul_Key == BIG_C_InvalidKey) return;

    /* Expand capacity if needed */
    if(BIG_gul_CookedSubEntryCount >= s_ul_CookedCapacity)
    {
        ULONG ul_NewCap = s_ul_CookedCapacity ? (s_ul_CookedCapacity * 2) : 32768;
        BIG_tdst_CookedSubEntry *p_New = (BIG_tdst_CookedSubEntry*)MEM_p_Alloc(ul_NewCap * sizeof(BIG_tdst_CookedSubEntry));
        if(!p_New) return;

        if(BIG_gast_CookedSubEntries)
        {
            L_memcpy(p_New, BIG_gast_CookedSubEntries, BIG_gul_CookedSubEntryCount * sizeof(BIG_tdst_CookedSubEntry));
            MEM_Free(BIG_gast_CookedSubEntries);
        }
        BIG_gast_CookedSubEntries = p_New;
        s_ul_CookedCapacity = ul_NewCap;
    }

    ul_Idx = BIG_gul_CookedSubEntryCount++;
    BIG_gast_CookedSubEntries[ul_Idx].ul_Key = _ul_Key;
    BIG_gast_CookedSubEntries[ul_Idx].ul_BinPos = _ul_BinPos;
    BIG_gast_CookedSubEntries[ul_Idx].ul_BinKey = _ul_BinKey;
    BIG_gast_CookedSubEntries[ul_Idx].ul_BinFatIndex = _ul_BinFatIndex;
    BIG_gast_CookedSubEntries[ul_Idx].ul_OffsetInBin = _ul_Offset;
    BIG_gast_CookedSubEntries[ul_Idx].ul_Size = _ul_Size;
    BIG_gast_CookedSubEntries[ul_Idx].ul_Type = _ul_Type;

    ul_Bucket = BIG_Cooked_HashKey(_ul_Key);
    BIG_gast_CookedSubEntries[ul_Idx].ul_NextInHash = s_aul_CookedHash[ul_Bucket];
    s_aul_CookedHash[ul_Bucket] = ul_Idx;
}

/*
 =======================================================================================================================
    Aim:    Find sub-entry by key in the cooked hash table.
 =======================================================================================================================
 */
BIG_tdst_CookedSubEntry* BIG_pst_Cooked_FindSubEntry(BIG_KEY _ul_Key)
{
    ULONG ul_Bucket;
    ULONG ul_Idx;

    if(!BIG_gb_IsCooked || !BIG_gast_CookedSubEntries || _ul_Key == 0 || _ul_Key == BIG_C_InvalidKey)
        return NULL;

    ul_Bucket = BIG_Cooked_HashKey(_ul_Key);
    ul_Idx = s_aul_CookedHash[ul_Bucket];

    while(ul_Idx != BIG_C_InvalidIndex)
    {
        if(BIG_gast_CookedSubEntries[ul_Idx].ul_Key == _ul_Key)
            return &BIG_gast_CookedSubEntries[ul_Idx];
        ul_Idx = BIG_gast_CookedSubEntries[ul_Idx].ul_NextInHash;
    }

    return NULL;
}

/*
 =======================================================================================================================
    Aim:    Get or load decompressed .bin container into cache.
 =======================================================================================================================
 */
static char* BIG_Cooked_GetCachedBin(ULONG _ul_BinPos, BIG_KEY _ul_BinKey, ULONG *_pul_Size)
{
    ULONG i, ul_OldestIdx = 0, ul_OldestTick = 0xFFFFFFFF;
    ULONG ul_Length, r;
    void *p_Raw;
    char *p_Dec;

    s_ul_CacheClock++;

    /* 1. Check existing cache */
    for(i = 0; i < BIG_COOKED_BIN_CACHE; i++)
    {
        if(s_ast_BinCache[i].pc_Data && s_ast_BinCache[i].ul_BinPos == _ul_BinPos)
        {
            s_ast_BinCache[i].ul_AccessTick = s_ul_CacheClock;
            if(_pul_Size) *_pul_Size = s_ast_BinCache[i].ul_Size;
            return s_ast_BinCache[i].pc_Data;
        }
        if(s_ast_BinCache[i].ul_AccessTick < ul_OldestTick)
        {
            ul_OldestTick = s_ast_BinCache[i].ul_AccessTick;
            ul_OldestIdx = i;
        }
    }

    /* 2. Read from disk */
    r = SeekSeek(BIG_Handle(), _ul_BinPos, L_SEEK_SET);
    if(r != 0) return NULL;

    r = ReadRead((UCHAR*)&ul_Length, sizeof(ULONG), BIG_Handle());
    if(r != 1) return NULL;
    ul_Length &= 0x7FFFFFFF;
    if(ul_Length == 0) return NULL;

    p_Raw = MEM_p_Alloc(ul_Length + 1);
    if(!p_Raw) return NULL;

    r = ReadRead((UCHAR*)p_Raw, ul_Length, BIG_Handle());
    if(r != 1)
    {
        MEM_Free(p_Raw);
        return NULL;
    }
    ((char*)p_Raw)[ul_Length] = 0;

    /* 3. Decompress multi-block LZO if compressed */
    p_Dec = BIG_special_LZOload((char*)p_Raw, &ul_Length);
    if(p_Dec != (char*)p_Raw)
    {
        char *p_Owned = (char*)MEM_p_Alloc(ul_Length + 1);
        if(p_Owned)
        {
            L_memcpy(p_Owned, p_Dec, ul_Length);
            p_Owned[ul_Length] = 0;
            p_Dec = p_Owned;
        }
        MEM_Free(p_Raw);
    }

    /* 4. Store in cache slot */
    if(s_ast_BinCache[ul_OldestIdx].pc_Data)
    {
        MEM_Free(s_ast_BinCache[ul_OldestIdx].pc_Data);
        s_ast_BinCache[ul_OldestIdx].pc_Data = NULL;
    }

    s_ast_BinCache[ul_OldestIdx].ul_BinKey = _ul_BinKey;
    s_ast_BinCache[ul_OldestIdx].ul_BinPos = _ul_BinPos;
    s_ast_BinCache[ul_OldestIdx].pc_Data = p_Dec;
    s_ast_BinCache[ul_OldestIdx].ul_Size = ul_Length;
    s_ast_BinCache[ul_OldestIdx].ul_AccessTick = s_ul_CacheClock;

    if(_pul_Size) *_pul_Size = ul_Length;
    return p_Dec;
}

/*
 =======================================================================================================================
    Aim:    Scan a .bin file for 0xEEFFC099 chunks and register its sub-entries.
 =======================================================================================================================
 */
static void BIG_Cooked_IndexOneBin(BIG_INDEX _ul_FatIdx)
{
    ULONG ul_BinPos = BIG_PosFile(_ul_FatIdx);
    BIG_KEY ul_BinKey = BIG_FileKey(_ul_FatIdx);
    ULONG ul_BinSize = 0;
    char *pc_Data = BIG_Cooked_GetCachedBin(ul_BinPos, ul_BinKey, &ul_BinSize);
    ULONG pos = 0;

    if(!pc_Data || ul_BinSize < 12) return;

    while(pos + 12 <= ul_BinSize)
    {
        ULONG ul_SubSize = *(ULONG*)(pc_Data + pos);
        ULONG ul_Magic   = *(ULONG*)(pc_Data + pos + 4);
        ULONG ul_Key     = *(ULONG*)(pc_Data + pos + 8);
        ULONG ul_Type    = 0;

        if(ul_Magic != BIG_C_CookedMagic)
            break;

        if(pos + 12 + ul_SubSize > ul_BinSize)
            break;

        if(ul_SubSize >= 4)
            ul_Type = *(ULONG*)(pc_Data + pos + 12);

        BIG_Cooked_AddSubEntry(ul_Key, ul_BinPos, ul_BinKey, _ul_FatIdx, pos + 12, ul_SubSize, ul_Type);

        pos += 12 + ul_SubSize;
    }
}

/*
 =======================================================================================================================
    Aim:    Initialize the cooked BigFile subsystem and scan all container files.
 =======================================================================================================================
 */
void BIG_Cooked_Init(void)
{
    ULONG i;

    BIG_Cooked_Close();

    if(!BIG_b_DetectCookedBigFile())
    {
        BIG_gb_IsCooked = FALSE;
        return;
    }

    BIG_gb_IsCooked = TRUE;

    for(i = 0; i < BIG_COOKED_HASH_SIZE; i++)
        s_aul_CookedHash[i] = BIG_C_InvalidIndex;

    /* Scan each file in FAT */
    for(i = 0; i < BIG_gst.st_ToSave.ul_MaxFile; i++)
    {
        char *psz_Name = BIG_NameFile(i);
        if(psz_Name && *psz_Name)
        {
            if(strstr(psz_Name, ".bin") || strstr(psz_Name, "_wow_") || strstr(psz_Name, "_wol_"))
            {
                BIG_Cooked_IndexOneBin(i);
            }
        }
    }
}

/*
 =======================================================================================================================
    Aim:    Cleanup cooked BigFile subsystem.
 =======================================================================================================================
 */
void BIG_Cooked_Close(void)
{
    ULONG i;

    if(BIG_gast_CookedSubEntries)
    {
        MEM_Free(BIG_gast_CookedSubEntries);
        BIG_gast_CookedSubEntries = NULL;
    }
    BIG_gul_CookedSubEntryCount = 0;
    s_ul_CookedCapacity = 0;

    for(i = 0; i < BIG_COOKED_BIN_CACHE; i++)
    {
        if(s_ast_BinCache[i].pc_Data)
        {
            MEM_Free(s_ast_BinCache[i].pc_Data);
            s_ast_BinCache[i].pc_Data = NULL;
        }
        s_ast_BinCache[i].ul_BinKey = 0;
        s_ast_BinCache[i].ul_BinPos = 0;
        s_ast_BinCache[i].ul_Size = 0;
        s_ast_BinCache[i].ul_AccessTick = 0;
    }

    for(i = 0; i < BIG_COOKED_HASH_SIZE; i++)
        s_aul_CookedHash[i] = BIG_C_InvalidIndex;

    BIG_gb_IsCooked = FALSE;
}

/*
 =======================================================================================================================
    Aim:    Resolve key to a cooked virtual position.
 =======================================================================================================================
 */
ULONG BIG_Cooked_SearchKeyToPos(BIG_KEY _ul_Key)
{
    BIG_tdst_CookedSubEntry *pst_Sub = BIG_pst_Cooked_FindSubEntry(_ul_Key);
    if(pst_Sub)
    {
        ULONG ul_Idx = (ULONG)(pst_Sub - BIG_gast_CookedSubEntries);
        return BIG_C_CookedPosFlag | ul_Idx;
    }
    return BIG_C_InvalidIndex;
}

/*
 =======================================================================================================================
    Aim:    Resolve sub-key to parent .bin FAT index.
 =======================================================================================================================
 */
BIG_INDEX BIG_Cooked_SearchKeyToFat(BIG_KEY _ul_Key)
{
    BIG_tdst_CookedSubEntry *pst_Sub = BIG_pst_Cooked_FindSubEntry(_ul_Key);
    if(pst_Sub)
    {
        return pst_Sub->ul_BinFatIndex;
    }
    return BIG_C_InvalidIndex;
}

/*
 =======================================================================================================================
    Aim:    Read a cooked sub-entry from memory buffer.
 =======================================================================================================================
 */
char* BIG_pc_Cooked_ReadFileTmp(ULONG _ul_Pos, ULONG *_pul_Length)
{
    ULONG ul_Idx;
    BIG_tdst_CookedSubEntry *pst_Sub;
    char *pc_BinData;
    ULONG ul_BinSize = 0;

    if(!(_ul_Pos & BIG_C_CookedPosFlag))
        return NULL;

    ul_Idx = _ul_Pos & ~BIG_C_CookedPosFlag;
    if(ul_Idx >= BIG_gul_CookedSubEntryCount)
        return NULL;

    pst_Sub = &BIG_gast_CookedSubEntries[ul_Idx];
    pc_BinData = BIG_Cooked_GetCachedBin(pst_Sub->ul_BinPos, pst_Sub->ul_BinKey, &ul_BinSize);
    if(!pc_BinData) return NULL;

    if(_pul_Length)
        *_pul_Length = pst_Sub->ul_Size;

    return pc_BinData + pst_Sub->ul_OffsetInBin;
}

/*
 =======================================================================================================================
    Aim:    Check if a file or sub-entry matches the requested extension.
 =======================================================================================================================
 */
BOOL BIG_b_Cooked_IsFileExtension(BIG_INDEX _ul_File, char *_psz_Ext)
{
    char *psz_Name;

    if(!_psz_Ext || !*_psz_Ext) return TRUE;
    if(_ul_File == BIG_C_InvalidIndex) return FALSE;

    psz_Name = BIG_NameFile(_ul_File);
    if(!psz_Name || !*psz_Name) return FALSE;

    /* Check WOL */
    if(!L_strnicmp(_psz_Ext, ".wol", 4))
    {
        if(strstr(psz_Name, "_wol_") || strstr(psz_Name, ".wol"))
            return TRUE;
    }

    /* Check WOW */
    if(!L_strnicmp(_psz_Ext, ".wow", 4))
    {
        if(strstr(psz_Name, "_wow_") || strstr(psz_Name, ".wow"))
            return TRUE;
    }

    /* Check GAO */
    if(!L_strnicmp(_psz_Ext, ".gao", 4))
    {
        if(strstr(psz_Name, "_gao_") || strstr(psz_Name, ".gao"))
            return TRUE;
    }

    return FALSE;
}

