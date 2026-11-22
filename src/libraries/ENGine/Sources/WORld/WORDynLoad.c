/* =======================================================================================================================
 *  WORDynLoad.c
 *  Dynamic World Object List (.wol) expansion & room streaming pipeline
 *  Reconstructed from Prince of Persia (2003) executable: POP.EXE (VA 0x0067FED0)
 * ======================================================================================================================= */

#include "Precomp.h"
#include "SDK/Sources/BIGfiles/BIGdefs.h"
#include "SDK/Sources/BIGfiles/BIGfat.h"
#include "SDK/Sources/BIGfiles/BIGread.h"
#include "SDK/Sources/BIGfiles/BIGkey.h"
#include "SDK/Sources/BIGfiles/BIGcooked.h"
#include "ENGine/Sources/WORld/WORstruct.h"
#include "ENGine/Sources/WORld/WORuniverse.h"
#include "ENGine/Sources/WORld/WORload.h"
#include "ENGine/Sources/WORld/WORDynLoad.h"

/*
 =======================================================================================================================
    WOR_ExpandWorldList (Reconstructed from POP.EXE VA 0x0067FED0)
    Expands a World Object List (.wol) container and validates referenced WOW rooms
 =======================================================================================================================
 */
void WOR_ExpandWorldList(BIG_KEY _ul_WolKey)
{
    ULONG ul_Pos, ul_Length = 0;
    char *pc_Buf;
    ULONG i, ul_NbEntries;

    if(_ul_WolKey == 0 || _ul_WolKey == BIG_C_InvalidKey) return;

    ul_Pos = BIG_ul_SearchKeyToPos(_ul_WolKey);
    if(ul_Pos == BIG_C_InvalidIndex)
    {
        ERR_X_Error(0, "Invalid key (%08X) found WOR_ExpandWorldList", (void*)(uintptr_t)_ul_WolKey);
        return;
    }

    pc_Buf = BIG_pc_ReadFileTmp(ul_Pos, &ul_Length);
    if(!pc_Buf || ul_Length < 8) return;

    /* Skip cooked .bin chunk header if present */
    if(ul_Length >= 12 && *(ULONG*)(pc_Buf + 4) == BIG_C_CookedMagic)
    {
        pc_Buf += 12;
        ul_Length -= 12;
    }

    ul_NbEntries = ul_Length >> 3;
    for(i = 0; i < ul_NbEntries; i++)
    {
        ULONG ul_RoomKey = *(ULONG*)(pc_Buf + i * 8);
        ULONG ul_Type    = *(ULONG*)(pc_Buf + i * 8 + 4);

        if(ul_RoomKey == 0 || ul_RoomKey == BIG_C_InvalidKey) continue;

        if(ul_Type != 0x776F772E /* ".wow" */)
        {
            ERR_X_Warning(0, "Non-WOW entry in WorldList", (void*)(uintptr_t)ul_RoomKey);
            continue;
        }

        /* Verify that room key can be resolved in BigFile */
        if(BIG_ul_SearchKeyToPos(ul_RoomKey) == BIG_C_InvalidIndex)
        {
            ERR_X_Warning(0, "WorldList references unresolvable room", (void*)(uintptr_t)ul_RoomKey);
        }
    }
}

/*
 =======================================================================================================================
    WOR_LoadWorldList
    High-level entry point to expand and load a complete WOL level scene
 =======================================================================================================================
 */
WOR_tdst_World *WOR_LoadWorldList(BIG_KEY _ul_WolKey, char _c_ForEditor)
{
    WOR_ExpandWorldList(_ul_WolKey);
    return WOR_pst_Universe_AddWorldList(NULL, _ul_WolKey, _c_ForEditor);
}

