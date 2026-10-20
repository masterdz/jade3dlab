#!/usr/bin/env python3
"""POP.EXE Source Module Extractor & Reverse Engineering Mapper.

Analyzes the Prince of Persia (2003) executable (POP.EXE), discovers all embedded
C/C++ translation units, extracts assertion anchors and line numbers, and maps
them to corresponding Jade Engine source implementations.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import struct
import subprocess
from typing import Any, Dict, List, Tuple


def parse_pe_sections(exe_bytes: bytes) -> Tuple[int, List[Dict[str, Any]]]:
    """Extract PE ImageBase and section headers."""
    if exe_bytes[:2] != b"MZ":
        raise ValueError("Not a valid DOS/PE executable.")
    pe_off = struct.unpack_from("<I", exe_bytes, 60)[0]
    if exe_bytes[pe_off:pe_off + 4] != b"PE\x00\x00":
        raise ValueError("Invalid PE signature.")

    coff = exe_bytes[pe_off + 4:pe_off + 24]
    machine, num_sections, time_date, sym_ptr, num_sym, opt_size, charact = struct.unpack("<HHIIIHH", coff)
    opt = exe_bytes[pe_off + 24:pe_off + 24 + opt_size]
    image_base = struct.unpack_from("<I", opt, 28)[0]

    sections = []
    sec_base = pe_off + 24 + opt_size
    for i in range(num_sections):
        sdata = exe_bytes[sec_base + i * 40:sec_base + (i + 1) * 40]
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


def find_source_modules(exe_bytes: bytes, image_base: int, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Scan the binary for embedded source file paths and trace their code XREFs."""
    # Find all path strings ending in .c, .cpp, or .h
    pattern = rb"[\\\.A-Za-z0-9_][A-Za-z0-9_\\\/\.:-]+\.(?:c|cpp|h)"
    matches = list(re.finditer(pattern, exe_bytes, re.IGNORECASE))
    
    unique_paths: Dict[str, Dict[str, Any]] = {}
    
    for m in matches:
        start = m.start()
        # Find start of null-terminated string
        str_start = exe_bytes.rfind(b"\x00", 0, start) + 1
        str_end = exe_bytes.find(b"\x00", start)
        if str_end == -1:
            continue
        raw_str = exe_bytes[str_start:str_end]
        try:
            path_str = raw_str.decode("latin-1")
        except Exception:
            continue

        # Clean non-ascii prefixes
        clean_path = re.sub(r"^[^\w\\./]+", "", path_str).strip()
        if len(clean_path) < 5 or "." not in clean_path:
            continue

        # Filter out common false positives and assertions
        if any(bad in clean_path.lower() for bad in ["kernel", "msvc", ".dll", "directx", "windows", "==", "!=", "fclose", "big_f"]):
            continue

        if not (clean_path.startswith("\\") or clean_path.startswith(".") or (len(clean_path) > 2 and clean_path[1] == ":")):
            continue

        if clean_path not in unique_paths:
            str_va = 0
            for sec in sections:
                if sec["raw_off"] <= str_start < sec["raw_off"] + sec["raw_size"]:
                    str_va = sec["va"] + (str_start - sec["raw_off"])
                    break

            unique_paths[clean_path] = {
                "path": clean_path,
                "file_offset": str_start,
                "virtual_address": str_va,
                "xrefs": [],
                "subsystem": categorize_module(clean_path),
            }

    # Find 32-bit pointer XREFs to these strings in .text section
    text_sec = next((s for s in sections if s["name"] == ".text"), None)
    if text_sec:
        text_data = exe_bytes[text_sec["raw_off"]:text_sec["raw_off"] + text_sec["raw_size"]]
        for mod in unique_paths.values():
            if not mod["virtual_address"]:
                continue
            va_bytes = struct.pack("<I", mod["virtual_address"])
            pos = 0
            while True:
                pos = text_data.find(va_bytes, pos)
                if pos == -1:
                    break
                xref_file_off = text_sec["raw_off"] + pos
                xref_va = text_sec["va"] + pos
                mod["xrefs"].append({
                    "file_offset": hex(xref_file_off),
                    "code_va": hex(xref_va),
                })
                pos += 1

    return list(unique_paths.values())


def categorize_module(path: str) -> str:
    """Classify the module into its functional engine architecture subsystem."""
    p_lower = path.lower()
    if "bigfiles" in p_lower or "packfiles" in p_lower:
        return "Jade BigFile Archive Subsystem (BIG)"
    if "aiinterp" in p_lower:
        return "Jade AI Scripting & Virtual Machine (AI)"
    if "objects" in p_lower or "modifier" in p_lower:
        return "Jade GameObject & Transform Pipeline (OBJ)"
    if "collision" in p_lower:
        return "Jade Physics & Collision Subsystem (COL)"
    if "grid" in p_lower:
        return "Jade Spatial Partitioning & Culling (GRI)"
    if "dare" in p_lower:
        return "Ubisoft DARE 3D Audio Engine"
    if "mnu_" in p_lower:
        return "PoP Interactive Menu UI Framework"
    if "fnt_" in p_lower:
        return "PoP Typography & Font Subsystem"
    if "graphicdk" in p_lower or "texture" in p_lower:
        return "Jade Graphics & Texture Subsystem (GRO/TEX)"
    if "text" in p_lower:
        return "Jade Localization & Text Subsystem"
    return "Core System & Miscellaneous"


def main():
    parser = argparse.ArgumentParser(description="Extract source modules and XREFs from POP.EXE.")
    parser.add_argument("exe_path", nargs="?", default="POP.EXE", help="Path to POP.EXE binary")
    parser.add_argument("-o", "--output", default="pop_extracted_modules.json", help="Output JSON path")
    args = parser.parse_args()

    exe_file = Path(args.exe_path)
    if not exe_file.exists():
        print(f"Error: {exe_file} not found.")
        return 1

    print(f"[*] Reading {exe_file.name} ({exe_file.stat().st_size:,} bytes)...")
    data = exe_file.read_bytes()

    image_base, sections = parse_pe_sections(data)
    print(f"[+] PE Image Base: {hex(image_base)}")
    for s in sections:
        print(f"    Section {s['name']:8}: VA={hex(s['va'])} (Raw Size: {s['raw_size']:,} bytes)")

    modules = find_source_modules(data, image_base, sections)
    print(f"\n[+] Successfully extracted {len(modules)} C/C++ source module anchors!")

    # Group by subsystem
    by_subsystem: Dict[str, List[Dict[str, Any]]] = {}
    for m in modules:
        by_subsystem.setdefault(m["subsystem"], []).append(m)

    for sub, mods in sorted(by_subsystem.items()):
        print(f"\n--- {sub} ({len(mods)} modules) ---")
        for m in mods:
            xref_cnt = len(m["xrefs"])
            print(f"  • {m['path']} (VA: {hex(m['virtual_address'])}, XREFs: {xref_cnt})")

    out_path = Path(args.output)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "binary": exe_file.name,
            "image_base": hex(image_base),
            "total_modules": len(modules),
            "subsystems": by_subsystem,
        }, f, indent=2)

    print(f"\n[+] Extraction manifest written to: {out_path.resolve()}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
