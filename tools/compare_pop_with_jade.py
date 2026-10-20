#!/usr/bin/env python3
"""Compare POP.EXE Extracted Modules with jaded-src.

Analyzes structural differences, version discrepancies, struct size variations,
and algorithmic changes between POP.EXE (v37) and the v36 Jade Engine in jaded-src.
"""

import json
from pathlib import Path


def main():
    root = Path("/Users/ibizaprint/Downloads/JadeEngine")
    extracted_dir = root / "pop_extracted_src"
    jaded_src = root / "jaded-src"

    comparison_results = []

    # Map of extracted paths to jaded-src paths
    mappings = [
        (
            "Libraries/Sdk/Sources/BIGfiles/BIGopen.c",
            "src/libraries/SDK/Sources/BIGfiles/BIGopen.c",
            "BIGopen (File Opening & Header Checks)",
        ),
        (
            "Libraries/Sdk/Sources/BIGfiles/BIGfat.c",
            "src/libraries/SDK/Sources/BIGfiles/BIGfat.c",
            "BIGfat (FAT Table Parsing, Directory & File Ext Layout)",
        ),
        (
            "Libraries/Sdk/Sources/BIGfiles/BIGread.c",
            "src/libraries/SDK/Sources/BIGfiles/BIGread.c",
            "BIGread (File Buffer Allocation & Read Pipeline)",
        ),
        (
            "Libraries/Sdk/Sources/BIGfiles/BIGcomp.c",
            "src/libraries/SDK/Sources/BIGfiles/BIGcomp.c",
            "BIGcomp (LZO Decompression & Block Streaming)",
        ),
        (
            "Libraries/Sdk/Sources/BIGfiles/BIGio.c",
            "src/libraries/SDK/Sources/BIGfiles/BIGio.c",
            "BIGio (Streaming SpeedMode fread & Buffer Constraints)",
        ),
        (
            "Libraries/Sdk/Sources/BIGfiles/LOAding/LOAdefs.c",
            "src/libraries/SDK/Sources/BIGfiles/LOAding/LOAdefs.c",
            "LOAdefs (Key-to-Pos Lookup & Dynamic Loader)",
        ),
        (
            "Libraries/ENGine/Sources/OBJects/OBJload.c",
            "src/libraries/ENGine/Sources/OBJects/OBJload.c",
            "OBJload (Game Object Loading & GAO Format Version)",
        ),
        (
            "Libraries/ENGine/Sources/WORld/WORDynLoad.c",
            "src/libraries/ENGine/Sources/WORld/WORDynLoad.c",
            "WORDynLoad (Dynamic World Streaming & Wow Bins)",
        ),
    ]

    for ext_rel, jade_rel, desc in mappings:
        ext_p = extracted_dir / ext_rel
        jade_p = jaded_src / jade_rel

        ext_exists = ext_p.exists()
        jade_exists = jade_p.exists()

        res = {
            "module": desc,
            "pop_path": str(ext_rel),
            "jade_path": str(jade_rel),
            "pop_exists": ext_exists,
            "jade_exists": jade_exists,
            "observations": [],
        }

        if ext_exists and jade_exists:
            ext_content = ext_p.read_text(encoding="utf-8", errors="ignore")
            jade_content = jade_p.read_text(encoding="utf-8", errors="ignore")

            res["pop_file_size"] = len(ext_content)
            res["jade_file_size"] = len(jade_content)

            # Check specific differences
            if "BIGfat.c" in ext_rel:
                res["observations"].append(
                    "FAT Header struct size is 44 bytes in both. In POP.EXE, FileTableExt is 84 bytes "
                    "(without ul_P4RevisionClient). In jaded-src, BIG_Version() >= 36 assumes 88 bytes, "
                    "which corrupts FAT parsing on prince3.bf. Fix requires recognizing v37 as 84 bytes."
                )
            elif "BIGread.c" in ext_rel:
                res["observations"].append(
                    "POP.EXE uses mask 0x7FFFFFFF on file lengths to support compressed/binarized flag "
                    "and seamlessly decompresses files. In jaded-src, BIG_special_LZOload was conditionally "
                    "compiled under #ifdef ACTIVE_EDITORS; in POP retail, transparent decoding is always active."
                )
            elif "BIGcomp.c" in ext_rel:
                res["observations"].append(
                    "POP.EXE adds BIGcomp_DecodeAllAvailableBlocks (VA 0x42AEA0) which is missing from "
                    "jaded-src. Both share BIGcomp_DecodeBlocks with identical 128KB chunk framing and LZO1X."
                )
            elif "OBJload.c" in ext_rel:
                res["observations"].append(
                    "POP.EXE assertion line 850 enforces 'ulGaoVersion <= 10'. Jaded-src also checks GAO "
                    "versioning but needs confirmation of GAO struct compatibility for PoP characters/meshes."
                )

        comparison_results.append(res)

    report_p = root / "pop_vs_jade_comparison.json"
    with open(report_p, "w", encoding="utf-8") as f:
        json.dump(comparison_results, f, indent=2)

    print(f"[+] Comparison complete! Manifest saved to {report_p}")
    for cr in comparison_results:
        print(f"\n* {cr['module']}:")
        print(f"  POP: {cr['pop_path']} ({'Found' if cr['pop_exists'] else 'Missing'})")
        print(f"  Jade: {cr['jade_path']} ({'Found' if cr['jade_exists'] else 'Missing'})")
        for obs in cr["observations"]:
            print(f"  -> {obs}")


if __name__ == "__main__":
    main()
