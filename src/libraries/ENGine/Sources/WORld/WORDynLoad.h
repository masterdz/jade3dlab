/* =======================================================================================================================
 *  WORDynLoad.h
 *  Dynamic World Object List (.wol) expansion & room streaming pipeline
 *  Reconstructed from Prince of Persia (2003) executable: POP.EXE (VA 0x0067FED0)
 * ======================================================================================================================= */

#pragma once

#ifndef __WORDYNLOAD_H__
#define __WORDYNLOAD_H__

#include "BASe/BAStypes.h"
#include "BIGfiles/BIGdefs.h"
#include "WORld/WORstruct.h"

#ifdef __cplusplus
extern "C" {
#endif

void            WOR_ExpandWorldList(BIG_KEY _ul_WolKey);
WOR_tdst_World* WOR_LoadWorldList(BIG_KEY _ul_WolKey, char _c_ForEditor);

#ifdef __cplusplus
}
#endif

#endif /* __WORDYNLOAD_H__ */

