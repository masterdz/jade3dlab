"""Jade Engine BigFile Uncooker & De-consolidator.

Reverses retail Prince of Persia: Sands of Time consolidated .bin archives (prince3.bf)
back into their uncooked development state of individual .gao, .gro, .grm, .wow, .wol,
.ova, and .ofc assets.
"""
from __future__ import annotations

import argparse
import io
import json
import os
from pathlib import Path
import struct
import sys
from typing import Dict, List, Optional, Tuple

# Ensure jade_engine is importable from root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from jade_engine.bf_parser import read_bigfile
from jade_engine.bin_parser import decompress_bin
from jade_engine.level_scene import level_asset_kind


GRO_INTERFACES = {
    0: "unknown",
    1: "gro",     # Geometric mesh
    2: "grl",     # Light
    3: "grm_single",
    4: "grm",     # Single material
    5: "grm",     # Multi material
    6: "grm_multitex",
    7: "camera",
    8: "lod",     # Static LOD
    9: "sprite",  # 2D Sprite list
    10: "text2d",
    11: "part",   # Particle generator
}


def parse_gao_name(payload: bytes) -> Optional[str]:
    """Extract string name from a .gao GameObject payload."""
    if len(payload) < 20:
        return None
    try:
        # In a valid Jade .gao file, payload starts with b".gao" (4 bytes),
        # followed by version (4 bytes), editor flags (4 bytes), id flags (4 bytes),
        # then name length (4 bytes) at offset 16, and string at offset 20.
        name_len = struct.unpack_from("<I", payload, 16)[0]
        if 0 < name_len < 512 and 20 + name_len <= len(payload):
            name = payload[20:20 + name_len].rstrip(b"\0").decode("latin-1", "replace")
            # Sanitize for filesystem
            return "".join(c if c.isalnum() or c in "._- " else "_" for c in name).strip()
    except Exception:
        pass
    return None


def expand_wow_for_editor(data: bytes) -> bytes:
    """Expand 180-byte binarized PoP .wow world files into 232-byte development format
    expected by Jade Editor WORload.c by restoring editor padding & dummy blocks."""
    if len(data) == 180 and data[:4] == b".wow":
        part1 = data[:76]    # Header (4), Version (4), NbObj (4), Ambient (4), Name (60)
        part2 = data[76:144]  # Camera Matrix (68)
        part3 = data[144:156] # FOV (4), BGColor (4), AmbientColor2 (4)
        part4 = data[156:180] # Grid1 (4), Grid2 (4), GOG (4), Networks (4), WorldText (4), Sectors (4)
        return part1 + b"\x00" * 4 + part2 + part3 + b"\x00" * 4 + b"\x00" * 44 + part4
    return data


def uncook_bin_data(data: bytes, container_name: str) -> List[Dict]:
    """Split a consolidated BIN file into individual uncooked Jade assets."""
    decompressed = decompress_bin(data)
    blocks = decompressed.split(b"\x99\xC0\xFF\xEE")

    assets = []
    seen_filenames = {}
    stem = Path(container_name).stem

    for i, blk in enumerate(blocks):
        if len(blk) < 8:
            continue
        key = struct.unpack("<I", blk[:4])[0]
        payload = blk[4:]  # Full asset payload preserving 4-byte header tag
        type_id = struct.unpack("<I", payload[:4])[0]
        raw_type = payload[:4]

        ext = None
        asset_name = None

        if raw_type == b".gao":
            ext = ".gao"
            asset_name = parse_gao_name(payload)
        elif raw_type == b".wow":
            ext = ".wow"
            asset_name = stem.split("_wow_")[0] if "_wow_" in stem else stem
            payload = expand_wow_for_editor(payload)
        elif raw_type == b".wol":
            ext = ".wol"
            asset_name = stem.split("_wol_")[0] if "_wol_" in stem else stem
        elif type_id in GRO_INTERFACES and type_id != 0:
            ext = f".{GRO_INTERFACES[type_id]}"
        elif payload.startswith(b"RIFF") and b"WAVE" in payload[:16]:
            ext = ".wav"
        elif payload.startswith(b"DDS "):
            ext = ".dds"
        else:
            # Fallback for unknown block types
            ext = f".dat_{type_id:08X}"

        if not asset_name:
            asset_name = f"0x{key:08X}"

        final_filename = f"{asset_name}{ext}" if not asset_name.endswith(ext) else asset_name

        # Disambiguate if duplicate filename in same container
        if final_filename in seen_filenames and seen_filenames[final_filename] != key:
            base = Path(final_filename).stem
            final_filename = f"{base}_{key:08X}{ext}"

        seen_filenames[final_filename] = key

        assets.append({
            "key": key,
            "filename": final_filename,
            "ext": ext,
            "size": len(payload),
            "payload": payload,
            "container": container_name,
        })

    return assets


def uncook_archive(bf_path: Path, output_dir: Path, filter_name: Optional[str] = None):
    """Uncook all or selected entries from a BigFile archive into loose files."""
    archive = read_bigfile(bf_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "source_archive": str(bf_path.name),
        "total_archive_entries": len(archive.entries),
        "assets": [],
    }

    print(f"[*] Processing {bf_path.name} (Total entries: {len(archive.entries)})")

    uncooked_count = 0
    total_bytes = 0

    for idx, entry in enumerate(archive.entries):
        name = entry.name
        if filter_name and filter_name.casefold() not in name.casefold():
            continue

        raw = archive.read_entry(entry)
        kind = level_asset_kind(name)

        # Categorize output subfolder
        if kind == "character":
            folder = output_dir / "Characters" / Path(name).stem
        elif kind == "equipment":
            folder = output_dir / "Equipment" / Path(name).stem
        elif kind == "wol" or kind == "wow":
            folder = output_dir / "Levels" / Path(name).stem
        elif name.lower().endswith(".dds"):
            folder = output_dir / "Textures" / "UI"
        else:
            folder = output_dir / "Assets" / Path(name).stem

        folder.mkdir(parents=True, exist_ok=True)

        if name.lower().endswith(".bin") and (b"\x99\xC0\xFF\xEE" in raw or len(raw) > 32):
            sub_assets = uncook_bin_data(raw, name)
            if sub_assets:
                for sub in sub_assets:
                    out_path = folder / sub["filename"]
                    with open(out_path, "wb") as f:
                        f.write(sub["payload"])

                    manifest["assets"].append({
                        "key": f"0x{sub['key']:08X}",
                        "filename": sub["filename"],
                        "size": sub["size"],
                        "relative_path": str(out_path.relative_to(output_dir)),
                        "source_container": name,
                    })
                    uncooked_count += 1
                    total_bytes += sub["size"]
            else:
                out_path = folder / name
                with open(out_path, "wb") as f:
                    f.write(raw)
        else:
            out_path = folder / name
            with open(out_path, "wb") as f:
                f.write(raw)
            uncooked_count += 1
            total_bytes += len(raw)

        if (idx + 1) % 10 == 0 or idx + 1 == len(archive.entries):
            print(f"    [{idx + 1}/{len(archive.entries)}] Processed {name} -> {uncooked_count} unbaked files extracted")

    manifest_path = output_dir / "uncooked_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n[+] Successfully unbaked {uncooked_count} assets ({total_bytes:,} bytes)")
    print(f"[+] Output directory: {output_dir.resolve()}")
    print(f"[+] Master Manifest:  {manifest_path.resolve()}")


def main():
    parser = argparse.ArgumentParser(description="Jade Engine BigFile Uncooker (Reverses prince3.bf to development state)")
    parser.add_argument("archive", type=str, help="Path to prince3.bf or target archive")
    parser.add_argument("-o", "--output", type=str, default="uncooked_prince3", help="Output directory for unbaked assets")
    parser.add_argument("-f", "--filter", type=str, default=None, help="Filter entry name (e.g. Couloir, Prince, Farah)")

    args = parser.parse_args()
    archive_path = Path(args.archive)
    if not archive_path.exists():
        print(f"Error: Archive not found: {archive_path}")
        sys.exit(1)

    uncook_archive(archive_path, Path(args.output), args.filter)


if __name__ == "__main__":
    main()
