#!/usr/bin/env python3
"""POP.EXE Source Code Module Reconstructor & Extractor.

Extracts reverse-engineered C/C++ source modules from POP.EXE using PE metadata,
embedded translation unit paths, assertion line anchors, and disassembly analysis.
Outputs reconstructed source files for comparison with jaded-src.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import struct
import subprocess
from typing import Any, Dict, List, Optional, Tuple


def parse_pe_sections(buf: bytes) -> Tuple[int, List[Dict[str, Any]]]:
    if buf[:2] != b"MZ":
        raise ValueError("Not a valid PE executable.")
    pe_off = struct.unpack_from("<I", buf, 60)[0]
    if buf[pe_off:pe_off + 4] != b"PE\x00\x00":
        raise ValueError("Invalid PE signature.")

    coff = buf[pe_off + 4:pe_off + 24]
    machine, num_sections, time_date, sym_ptr, num_sym, opt_size, charact = struct.unpack("<HHIIIHH", coff)
    opt = buf[pe_off + 24:pe_off + 24 + opt_size]
    image_base = struct.unpack_from("<I", opt, 28)[0]

    sections = []
    sec_base = pe_off + 24 + opt_size
    for i in range(num_sections):
        sdata = buf[sec_base + i * 40:sec_base + (i + 1) * 40]
        sname, vsz, va, rsz, rptr = struct.unpack_from("<8sIIII", sdata, 0)
        clean_name = sname.split(b"\x00")[0].decode("ascii", errors="ignore")
        sections.append({
            "name": clean_name,
            "va": image_base + va,
            "vsz": vsz,
            "raw_off": rptr,
            "raw_size": rsz,
        })
    return image_base, sections


def get_string_at(buf: bytes, off: int, max_len: int = 512) -> Optional[str]:
    if off < 0 or off >= len(buf):
        return None
    end = buf.find(b"\x00", off)
    if end == -1 or end - off > max_len:
        return None
    try:
        return buf[off:end].decode("latin-1")
    except Exception:
        return None


def disassemble_range(exe_path: str, start_va: int, end_va: int) -> str:
    cmd = [
        "objdump",
        "--disassemble",
        "--arch=i386",
        f"--start-address={hex(start_va)}",
        f"--stop-address={hex(end_va)}",
        exe_path,
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return res.stdout
    except Exception:
        return ""


def find_function_bounds(buf: bytes, text_off: int, text_size: int, anchor_off: int) -> Tuple[int, int]:
    """Find start and end of function containing anchor_off."""
    # Walk backwards to find function start (after int3 padding or ret)
    func_start = text_off
    curr = anchor_off
    while curr > text_off:
        if buf[curr] == 0xCC and buf[curr - 1] == 0xCC:
            p = curr + 1
            while p < anchor_off and buf[p] == 0xCC:
                p += 1
            func_start = p
            break
        curr -= 1
        if anchor_off - curr > 0x2000:
            func_start = curr
            break

    # Walk forwards to find function end (int 3 padding or next function)
    func_end = text_off + text_size
    curr = anchor_off
    while curr < text_off + text_size - 1:
        if buf[curr] in (0xC3, 0xC2) and buf[curr + 1] == 0xCC:
            func_end = curr + 1
            break
        curr += 1
        if curr - anchor_off > 0x4000:
            func_end = curr
            break

    return func_start, func_end


def main():
    parser = argparse.ArgumentParser(description="Extract source modules from POP.EXE")
    parser.add_argument("--exe", default="/Users/ibizaprint/Downloads/JadeEngine/POP.EXE")
    parser.add_argument("--outdir", default="/Users/ibizaprint/Downloads/JadeEngine/pop_extracted_src")
    args = parser.parse_args()

    exe_path = args.exe
    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Reading {exe_path}...")
    with open(exe_path, "rb") as f:
        buf = f.read()

    image_base, sections = parse_pe_sections(buf)
    text_sec = next(s for s in sections if s["name"] == ".text")
    rdata_sec = next((s for s in sections if s["name"] == ".rdata"), None)

    text_off = text_sec["raw_off"]
    text_size = text_sec["raw_size"]
    err_func_va = 0x4204D0

    def va_to_off(va: int) -> Optional[int]:
        for s in sections:
            if s["va"] <= va < s["va"] + s["vsz"]:
                return s["raw_off"] + (va - s["va"])
        return None

    print("[*] Scanning for translation units and assertions in POP.EXE...")
    # Map all assertions
    assertions = []
    for off in range(text_off, text_off + text_size - 5):
        if buf[off] == 0xE8:
            rel = struct.unpack_from("<i", buf, off + 1)[0]
            call_va = image_base + off
            if call_va + 5 + rel == err_func_va:
                # Parse pushed arguments
                pushes = []
                p = off - 1
                while p >= max(text_off, off - 50):
                    if buf[p] == 0x68:
                        val = struct.unpack_from("<I", buf, p + 1)[0]
                        pushes.append((p, val))
                    elif buf[p] == 0x6A:
                        val = buf[p + 1]
                        pushes.append((p, val))
                    p -= 1

                file_str = None
                expr_str = None
                msg_str = None
                line_no = None

                for p_off, val in pushes:
                    s_off = va_to_off(val)
                    s = get_string_at(buf, s_off) if s_off is not None else None
                    if s:
                        if (
                            (".c" in s or ".cpp" in s or ".h" in s)
                            and ("\\" in s or "/" in s or "." in s)
                            and file_str is None
                        ):
                            file_str = s
                        elif expr_str is None:
                            expr_str = s
                        elif msg_str is None:
                            msg_str = s
                    elif val < 10000 and line_no is None and val > 0:
                        line_no = val

                f_start, f_end = find_function_bounds(buf, text_off, text_size, off)
                assertions.append({
                    "call_va": call_va,
                    "func_start_va": image_base + f_start,
                    "func_end_va": image_base + f_end,
                    "file": file_str,
                    "line": line_no,
                    "expr": expr_str,
                    "msg": msg_str,
                })

    print(f"[+] Total assertions indexed: {len(assertions)}")

    # Group assertions and functions by source file
    files_map: Dict[str, List[Dict[str, Any]]] = {}
    for a in assertions:
        f = a["file"] or "UnknownModule.c"
        files_map.setdefault(f, []).append(a)

    print(f"[+] Identified {len(files_map)} translation units in POP.EXE")

    manifest = []
    for raw_path, asserts in sorted(files_map.items()):
        clean_rel = raw_path.replace("\\", "/").lstrip("/")
        if clean_rel.startswith("./"):
            clean_rel = clean_rel[2:]
        target_file = out_dir / clean_rel
        target_file.parent.mkdir(parents=True, exist_ok=True)

        print(f"[*] Extracting {clean_rel} ({len(asserts)} assertions)...")

        # Deduplicate functions in this module
        funcs: Dict[int, Dict[str, Any]] = {}
        for a in asserts:
            s_va = a["func_start_va"]
            if s_va not in funcs:
                funcs[s_va] = {
                    "start_va": s_va,
                    "end_va": a["func_end_va"],
                    "asserts": [],
                }
            funcs[s_va]["asserts"].append(a)

        # Generate source content
        lines = []
        lines.append(f"/* ===========================================================================")
        lines.append(f" * RECONSTRUCTED SOURCE MODULE: {clean_rel}")
        lines.append(f" * Extracted from Prince of Persia (2003) executable: POP.EXE")
        lines.append(f" * Total Embedded Assertions: {len(asserts)}")
        lines.append(f" * Unique Functions Mapped: {len(funcs)}")
        lines.append(f" * =========================================================================== */\n")
        lines.append('#include "SDK/Sources/BIGfiles/BIGdefs.h"')
        lines.append('#include "SDK/Sources/BIGfiles/BIGfat.h"')
        lines.append('#include "SDK/Sources/BIGfiles/BIGread.h"')
        lines.append('#include "SDK/Sources/BIGfiles/BIGcomp.h"\n')

        for f_va, f_info in sorted(funcs.items()):
            s_va = f_info["start_va"]
            e_va = f_info["end_va"]
            f_size = e_va - s_va
            disasm = disassemble_range(exe_path, s_va, e_va)

            lines.append(f"/* ---------------------------------------------------------------------------")
            lines.append(f" * Function at VA 0x{s_va:08X} - 0x{e_va:08X} (Size: {f_size} bytes)")
            for fa in f_info["asserts"]:
                lines.append(f" * Assertion line {fa['line']}: {fa['expr']} | Message: {fa['msg']}")
            lines.append(f" * --------------------------------------------------------------------------- */")

            # Determine function name from assertion or known mapping
            func_name = f"sub_{s_va:08X}"
            # Known functions by VA
            known_map = {
                0x425000: "INO_fn_vInitJoystick",
                0x425A00: "BIG_Close",
                0x425AC0: "BIG_Open",
                0x426340: "LOA_ul_SearchKeyToPos",
                0x428160: "BIG_ul_GetLengthFile",
                0x428240: "BIG_pc_ReadFileTmp",
                0x4284E0: "BIG_ul_ReadFile",
                0x4287C0: "BIG_OpenFat",
                0x428AD0: "BIG_ReadFatFile",
                0x428C60: "BIG_ReadFat",
                0x429120: "BIG_SpeedMode_fread",
                0x42AD50: "BIGcomp_DecodeBlocks",
                0x42AEA0: "BIGcomp_DecodeAllAvailableBlocks",
                0x430470: "TEX_fn_vAddTexture",
                0x430700: "TEX_fn_vAddPalette",
                0x67FED0: "WOR_ExpandWorldList",
                0x684970: "OBJ_ul_LoadGAO",
                0x698130: "OBJ_BV_Convert",
                0x6986C0: "OBJ_BV_Merge",
                0x6C5D40: "GRI_fn_vComputeGrid",
                0x6DAF20: "GRI_fn_vAddGrid",
                0x6CB6F0: "COL_fn_vAddCob",
            }
            if s_va in known_map:
                func_name = known_map[s_va]

            lines.append(f"void {func_name}(void)")
            lines.append("{")
            for fa in f_info["asserts"]:
                cond = fa["expr"] or "1"
                msg = fa["msg"] or "Unknown error"
                line_no = fa["line"] or 0
                lines.append(f"    /* Line {line_no} */ ERR_X_Error({cond}, \"{msg}\", NULL);")
            lines.append("\n    /* Disassembly & Logic Flow:")
            for d_line in disasm.splitlines()[:60]:
                if d_line.strip():
                    lines.append(f"     * {d_line}")
            if len(disasm.splitlines()) > 60:
                lines.append(f"     * ... ({len(disasm.splitlines()) - 60} more instructions)")
            lines.append("     */")
            lines.append("}\n")

        with open(target_file, "w", encoding="utf-8") as out_f:
            out_f.write("\n".join(lines))

        manifest.append({
            "source_path": raw_path,
            "target_path": str(target_file.relative_to(out_dir)),
            "assertions": len(asserts),
            "functions": len(funcs),
        })

    manifest_file = out_dir / "extraction_manifest.json"
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n[+] Extracted all {len(manifest)} source modules to {out_dir}!")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
