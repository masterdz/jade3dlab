#!/usr/bin/env python3
"""Jade Engine Uncooked Asset Repacker.

Builds a development-ready BigFile (prince3_dev.bf) for Jade Engine Editor
(Jaded.exe /editor /console) from the 28,000+ uncooked assets in 'Uncooked Prince3BF'.

Constructs the full Jade Bank directory hierarchy:
  ROOT/
  ├── EditorDatas/        (Editor UI, INIs, Desktop layouts, Display Datas)
  └── EngineDatas/
      ├── 01 Texture Bank/
      ├── 02 Modelisation Bank/
      │   ├── Assets/     (Environment props, background assets)
      │   ├── Characters/ (Prince, Farah, SandGuards, etc.)
      │   └── Equipment/  (Swords, Costumes, Action Kits)
      ├── 03 Animation Bank/
      ├── 04 Technical Bank/
      └── 06 Levels/      (All 64 Prince of Persia rooms and cutscenes)

Format: Version 37 BigFile with 84-byte non-P4 structure format, 100% compatible
with jaded-src and the compiled Jaded.exe binary.
"""

from __future__ import annotations

import io
import json
import os
from pathlib import Path
import struct
import sys
import time
from typing import Dict, List, Optional, Set, Tuple

# Constants
BIG_VERSION_POP_SOT = 36
BIG_FILE_EXT_SIZE = 88
BIG_INVALID_INDEX = 0xFFFFFFFF
BIG_INVALID_KEY = 0xFFFFFFFF
UNIVERSE_KEY = 0xCC00008E  # Prince of Persia: The Sands of Time universe key

MAX_NAME_LEN = 64  # Includes null terminator (max 63 chars)


class DirNode:
    def __init__(self, name: str, parent_idx: int = BIG_INVALID_INDEX):
        self.name: str = name[: MAX_NAME_LEN - 1]
        self.parent_idx: int = parent_idx
        self.first_file_idx: int = BIG_INVALID_INDEX
        self.first_subdir_idx: int = BIG_INVALID_INDEX
        self.prev_sibling_idx: int = BIG_INVALID_INDEX
        self.next_sibling_idx: int = BIG_INVALID_INDEX
        self.subdirs: List[int] = []
        self.files: List[int] = []


class FileEntry:
    def __init__(
        self,
        name: str,
        parent_dir_idx: int,
        key: int,
        payload_source: str,  # Filepath on disk
        length_on_disk: int = 0,
    ):
        self.name: str = name[: MAX_NAME_LEN - 1]
        self.parent_dir_idx: int = parent_dir_idx
        self.key: int = key
        self.payload_source: str = payload_source
        self.length_on_disk: int = max(4, length_on_disk)
        self.disk_pos: int = 0
        self.prev_file_idx: int = BIG_INVALID_INDEX
        self.next_file_idx: int = BIG_INVALID_INDEX


class BigFileBuilder:
    def __init__(self, workspace_root: Path):
        self.root_path = workspace_root
        self.dirs: List[DirNode] = []
        self.files: List[FileEntry] = []
        self.dir_path_to_idx: Dict[str, int] = {}
        self.used_keys: Set[int] = set()
        self.synthetic_key_counter: int = 0xE0000001

        # Create ROOT dir (index 0)
        self._get_or_create_dir("ROOT")

    def _get_or_create_dir(self, full_path: str) -> int:
        norm_path = full_path.replace("\\", "/").strip("/")
        if norm_path in self.dir_path_to_idx:
            return self.dir_path_to_idx[norm_path]

        parts = norm_path.split("/")
        if len(parts) == 1 and parts[0] == "ROOT":
            idx = len(self.dirs)
            node = DirNode("ROOT", BIG_INVALID_INDEX)
            self.dirs.append(node)
            self.dir_path_to_idx["ROOT"] = idx
            return idx

        # Ensure parent exists
        parent_path = "/".join(parts[:-1])
        parent_idx = self._get_or_create_dir(parent_path)

        idx = len(self.dirs)
        node = DirNode(parts[-1], parent_idx)
        self.dirs.append(node)
        self.dir_path_to_idx[norm_path] = idx

        # Add to parent's subdirs list
        self.dirs[parent_idx].subdirs.append(idx)
        return idx

    def add_file(self, target_dir_path: str, filename: str, filepath: Path, key: int):
        dir_idx = self._get_or_create_dir(target_dir_path)

        # Ensure unique key
        assigned_key = key
        if assigned_key == 0 or assigned_key == BIG_INVALID_KEY or assigned_key in self.used_keys:
            assigned_key = self.synthetic_key_counter
            self.synthetic_key_counter += 1

        self.used_keys.add(assigned_key)

        file_sz = filepath.stat().st_size
        entry = FileEntry(
            name=filename,
            parent_dir_idx=dir_idx,
            key=assigned_key,
            payload_source=str(filepath),
            length_on_disk=file_sz,
        )

        file_idx = len(self.files)
        self.files.append(entry)
        self.dirs[dir_idx].files.append(file_idx)

    def link_structures(self):
        """Construct doubly-linked lists for directory subdirs and files."""
        print("[*] Linking directory tree and file tables...")
        for d_idx, d in enumerate(self.dirs):
            # Link subdirs: head insertion order or sequential
            if d.subdirs:
                d.first_subdir_idx = d.subdirs[0]
                for s_i, sub_idx in enumerate(d.subdirs):
                    prev_idx = d.subdirs[s_i - 1] if s_i > 0 else BIG_INVALID_INDEX
                    next_idx = d.subdirs[s_i + 1] if s_i < len(d.subdirs) - 1 else BIG_INVALID_INDEX
                    self.dirs[sub_idx].prev_sibling_idx = prev_idx
                    self.dirs[sub_idx].next_sibling_idx = next_idx
            else:
                d.first_subdir_idx = BIG_INVALID_INDEX

            # Link files in directory
            if d.files:
                d.first_file_idx = d.files[0]
                for f_i, file_idx in enumerate(d.files):
                    prev_idx = d.files[f_i - 1] if f_i > 0 else BIG_INVALID_INDEX
                    next_idx = d.files[f_i + 1] if f_i < len(d.files) - 1 else BIG_INVALID_INDEX
                    self.files[file_idx].prev_file_idx = prev_idx
                    self.files[file_idx].next_file_idx = next_idx
            else:
                d.first_file_idx = BIG_INVALID_INDEX

    def build(self, output_bf: Path):
        self.link_structures()

        total_files = len(self.files)
        total_dirs = len(self.dirs)
        sz_fat = total_files

        print(f"[+] Total files to pack: {total_files:,}")
        print(f"[+] Total directories:   {total_dirs:,}")
        print(f"[+] Target BigFile:      {output_bf.resolve()}")

        # Offsets calculation:
        # Header: 44 bytes
        # Fat Descriptor: 24 bytes
        # Offset 0x44 (68 bytes):
        # FileTable: sz_fat * 8 bytes
        # FileTableExt: sz_fat * 84 bytes
        # DirTable: total_dirs * 84 bytes
        fat_des_pos = 44
        pos_fat = 0x44
        pos_file_table = pos_fat
        pos_file_ext = pos_file_table + (sz_fat * 8)
        pos_dir_table = pos_file_ext + (sz_fat * BIG_FILE_EXT_SIZE)
        end_of_fat = pos_dir_table + (total_dirs * 84)

        # Align payload start to 64-byte boundary
        data_start = (end_of_fat + 63) & ~63
        fat_padding = data_start - end_of_fat

        print(f"[+] Layout:")
        print(f"    - Header:        0x00 .. 0x2C (44 bytes)")
        print(f"    - FAT Des:       0x2C .. 0x44 (24 bytes)")
        print(f"    - FileTable:     0x{pos_file_table:X} ({sz_fat * 8:,} bytes)")
        print(f"    - FileTableExt:  0x{pos_file_ext:X} ({sz_fat * 84:,} bytes)")
        print(f"    - DirTable:      0x{pos_dir_table:X} ({total_dirs * 84:,} bytes)")
        print(f"    - Payloads:      0x{data_start:X}")

        output_bf.parent.mkdir(parents=True, exist_ok=True)
        with open(output_bf, "wb") as out_f:
            # Reserve space for Header, FAT Des, FileTable, FileTableExt, DirTable
            out_f.seek(data_start)

            print("[*] Streaming file payloads to disk...")
            total_bytes_written = 0
            t0 = time.time()

            for i, f_entry in enumerate(self.files):
                pos = out_f.tell()
                f_entry.disk_pos = pos

                # Read source payload
                src_path = f_entry.payload_source
                with open(src_path, "rb") as in_f:
                    payload = in_f.read()

                length = len(payload)
                # Pad to at least 4 bytes if empty/short
                if length < 4:
                    payload = payload + b"\x00" * (4 - length)
                    length = 4

                # Write 4-byte length prefix
                out_f.write(struct.pack("<I", length))
                # Write data
                out_f.write(payload)

                total_bytes_written += 4 + length

                if (i + 1) % 5000 == 0 or (i + 1) == total_files:
                    elapsed = time.time() - t0
                    print(f"    [{i + 1:,}/{total_files:,}] Written {total_bytes_written / 1024 / 1024:.1f} MB ({elapsed:.1f}s)")

            final_file_size = out_f.tell()
            print(f"[+] Payload writing completed ({final_file_size:,} bytes on disk).")

            # Now write the FAT tables and Header
            print("[*] Writing BigFile Header and FAT tables...")

            # 1. Header (44 bytes)
            out_f.seek(0)
            hdr = struct.pack(
                "<4s10I",
                b"BIG\x00",
                BIG_VERSION_POP_SOT,
                total_files,
                total_dirs,
                0,                  # ul_MaxKey
                0,                  # ul_Root
                BIG_INVALID_INDEX,  # ul_FirstFreeFile
                BIG_INVALID_INDEX,  # ul_FirstFreeDir
                sz_fat,             # ul_SizeOfFat
                1,                  # ul_NumFat
                UNIVERSE_KEY,       # ul_UniverseKey
            )
            out_f.write(hdr)

            # 2. FAT Descriptor #0 (24 bytes)
            out_f.seek(fat_des_pos)
            fat_des = struct.pack(
                "<6I",
                total_files,        # ul_MaxFile
                total_dirs,         # ul_MaxDir
                pos_fat,            # ul_PosFat
                BIG_INVALID_INDEX,  # ul_NextPosFat (-1)
                0,                  # ul_FirstIndex
                sz_fat - 1,         # ul_LastIndex
            )
            out_f.write(fat_des)

            # 3. FileTable (sz_fat * 8 bytes)
            out_f.seek(pos_file_table)
            file_table_buf = bytearray(sz_fat * 8)
            for i, f_entry in enumerate(self.files):
                struct.pack_into("<2I", file_table_buf, i * 8, f_entry.disk_pos, f_entry.key)
            out_f.write(file_table_buf)

            # 4. FileTableExt (sz_fat * 84 bytes)
            out_f.seek(pos_file_ext)
            file_ext_buf = bytearray(sz_fat * BIG_FILE_EXT_SIZE)
            for i, f_entry in enumerate(self.files):
                name_bytes = f_entry.name.encode("latin-1", "replace")[:63]
                name_padded = name_bytes + b"\x00" * (64 - len(name_bytes))
                struct.pack_into(
                    "<5I64sI",
                    file_ext_buf,
                    i * BIG_FILE_EXT_SIZE,
                    f_entry.length_on_disk,
                    f_entry.prev_file_idx,
                    f_entry.next_file_idx,
                    f_entry.parent_dir_idx,
                    0,  # x_Time
                    name_padded,
                    0,  # ul_P4RevisionClient
                )
            out_f.write(file_ext_buf)

            # 5. DirTable (total_dirs * 84 bytes)
            out_f.seek(pos_dir_table)
            dir_table_buf = bytearray(total_dirs * 84)
            for i, d in enumerate(self.dirs):
                name_bytes = d.name.encode("latin-1", "replace")[:63]
                name_padded = name_bytes + b"\x00" * (64 - len(name_bytes))
                struct.pack_into(
                    "<5I64s",
                    dir_table_buf,
                    i * 84,
                    d.first_file_idx,
                    d.first_subdir_idx,
                    d.prev_sibling_idx,
                    d.next_sibling_idx,
                    d.parent_idx,
                    name_padded,
                )
            out_f.write(dir_table_buf)

            # 6. Padding to data_start
            if fat_padding > 0:
                out_f.write(b"\x00" * fat_padding)

        print(f"\n[SUCCESS] Repacked development BigFile generated successfully!")
        print(f"[+] Output: {output_bf.resolve()} ({output_bf.stat().st_size:,} bytes)")


def collect_and_build(workspace_root: Path, output_bf: Path):
    builder = BigFileBuilder(workspace_root)

    # 1. Base Bank directories
    print("[*] Creating official Jade Bank directory skeleton...")
    builder._get_or_create_dir("ROOT/EditorDatas")
    builder._get_or_create_dir("ROOT/EngineDatas")
    builder._get_or_create_dir("ROOT/EngineDatas/01 Texture Bank")
    builder._get_or_create_dir("ROOT/EngineDatas/02 Modelisation Bank")
    builder._get_or_create_dir("ROOT/EngineDatas/02 Modelisation Bank/Assets")
    builder._get_or_create_dir("ROOT/EngineDatas/02 Modelisation Bank/Characters")
    builder._get_or_create_dir("ROOT/EngineDatas/02 Modelisation Bank/Equipment")
    builder._get_or_create_dir("ROOT/EngineDatas/03 Animation Bank")
    builder._get_or_create_dir("ROOT/EngineDatas/04 Technical Bank")
    builder._get_or_create_dir("ROOT/EngineDatas/06 Levels")

    # 2. Add EditorDatas files (from scratch/EditorDatas or Rayman4.bf)
    editor_datas_dir = workspace_root / "scratch" / "EditorDatas"
    if editor_datas_dir.exists():
        print("[*] Adding EditorDatas (UI and Desktop configurations)...")
        # Load keys from Rayman4.bf if available
        rayman4_bf = workspace_root / "Rayman4.bf"
        rayman_keys = {}
        if rayman4_bf.exists():
            with open(rayman4_bf, "rb") as rf:
                rf.seek(44)
                mf, md, pos, next_pos, first_idx, last_idx = struct.unpack("<6I", rf.read(24))
                sz_fat = 161090
                pos_file_ext = pos + sz_fat * 8
                pos_dir = pos_file_ext + sz_fat * 88
                
                # Read all file keys
                rf.seek(pos)
                fkeys = [struct.unpack("<2I", rf.read(8))[1] for _ in range(mf)]
                
                # Read all file names
                rf.seek(pos_file_ext)
                for i in range(mf):
                    fchunk = rf.read(88)
                    fname = fchunk[20:84].split(b"\0")[0].decode("ascii", errors="replace")
                    rayman_keys[fname] = fkeys[i]

        for root, dirs, files in os.walk(editor_datas_dir):
            rel_dir = Path(root).relative_to(workspace_root / "scratch")
            target_jade_dir = f"ROOT/{rel_dir.as_posix()}"
            for f in files:
                if f == ".DS_Store":
                    continue
                file_path = Path(root) / f
                key = rayman_keys.get(f, 0)
                builder.add_file(target_jade_dir, f, file_path, key)

    # 3. Load manifest for Prince of Persia keys
    manifest_path = workspace_root / "Uncooked Prince3BF" / "uncooked_manifest.json"
    manifest_keys: Dict[str, int] = {}
    if manifest_path.exists():
        print("[*] Loading Uncooked Prince3BF manifest...")
        with open(manifest_path, "r", encoding="utf-8") as mf:
            m_data = json.load(mf)
            for item in m_data.get("assets", []):
                manifest_keys[item["relative_path"]] = int(item["key"], 16)

    # 4. Add all uncooked Prince of Persia assets
    uncooked_dir = workspace_root / "Uncooked Prince3BF"
    print("[*] Indexing uncooked assets from Uncooked Prince3BF/...")

    for category in ["Assets", "Characters", "Equipment", "Levels"]:
        cat_dir = uncooked_dir / category
        if not cat_dir.exists():
            continue

        if category == "Assets":
            jade_cat_prefix = "ROOT/EngineDatas/02 Modelisation Bank/Assets"
        elif category == "Characters":
            jade_cat_prefix = "ROOT/EngineDatas/02 Modelisation Bank/Characters"
        elif category == "Equipment":
            jade_cat_prefix = "ROOT/EngineDatas/02 Modelisation Bank/Equipment"
        elif category == "Levels":
            jade_cat_prefix = "ROOT/EngineDatas/06 Levels"
        else:
            jade_cat_prefix = "ROOT/EngineDatas/04 Technical Bank"

        for root, dirs, files in os.walk(cat_dir):
            rel_from_cat = Path(root).relative_to(cat_dir)
            if str(rel_from_cat) == ".":
                target_jade_dir = jade_cat_prefix
            else:
                target_jade_dir = f"{jade_cat_prefix}/{rel_from_cat.as_posix()}"

            for f in files:
                if f == ".DS_Store" or f == "uncooked_manifest.json":
                    continue
                file_path = Path(root) / f
                rel_from_uncooked = file_path.relative_to(uncooked_dir).as_posix()

                # Determine key
                key = manifest_keys.get(rel_from_uncooked, 0)
                if key == 0 and f.startswith("0x") and len(f) >= 10:
                    try:
                        key = int(f[2:10], 16)
                    except ValueError:
                        key = 0

                builder.add_file(target_jade_dir, f, file_path, key)

    # 5. Build BigFile
    builder.build(output_bf)


def main():
    workspace = Path("/Users/ibizaprint/Downloads/JadeEngine")
    output_bf = workspace / "prince3_dev.bf"

    if len(sys.argv) > 1:
        output_bf = Path(sys.argv[1])

    collect_and_build(workspace, output_bf)


if __name__ == "__main__":
    main()
