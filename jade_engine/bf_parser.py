"""Jade BigFile (.bf) archive reader, FAT indexing, and entry decompression."""
from __future__ import annotations

from pathlib import Path
import struct
from typing import Dict, List, Optional, Set, Tuple

from .lzo import decompress_pop_lzo, looks_like_pop_lzo
from .models import BigFileEntry, BigFileInfo
from .level_scene import level_asset_kind

LEGACY_BF_HEADER_SIZE = 44
LEGACY_BF_FILE_TABLE_ENTRY_SIZE = 8
LEGACY_BF_FILE_ENTRY_SIZE = 84


class BFArchive:
    """Convenient high-level interface over a loaded BigFile archive."""

    def __init__(self, info: BigFileInfo):
        self.info = info
        self.path = info.path
        self.version = info.version
        self.entries = info.entries
        self._entries_by_key: Dict[int, BigFileEntry] = {e.key: e for e in self.entries}
        self._entries_by_name: Dict[str, BigFileEntry] = {e.name.casefold(): e for e in self.entries}

        # Backwards compatibility: attach archive reference to each entry
        for e in self.entries:
            e._archive = self

    @property
    def files(self) -> List[BigFileEntry]:
        """Backward compatibility alias for entries."""
        return self.entries

    @property
    def elem_count(self) -> int:
        return len(self.entries)

    def get_entry_by_key(self, key: int) -> Optional[BigFileEntry]:
        return self._entries_by_key.get(key)

    def get_entry_by_name(self, name: str) -> Optional[BigFileEntry]:
        return self._entries_by_name.get(name.casefold())

    def get_file_by_name(self, name: str) -> Optional[BigFileEntry]:
        """Backward compatibility alias."""
        return self.get_entry_by_name(name)

    def get_file_by_key(self, key: int) -> Optional[BigFileEntry]:
        """Backward compatibility alias."""
        return self.get_entry_by_key(key)

    def read_file(self, entry: BigFileEntry, decompress: bool = True) -> bytes:
        """Backward compatibility alias for read_entry."""
        return self.read_entry(entry, decompress=decompress)

    def read_entry(self, entry: BigFileEntry, decompress: bool = True) -> bytes:
        """Read raw or decompressed bytes for a specific archive entry."""
        with open(self.path, "rb") as stream:
            stream.seek(entry.position + entry.data_header_size)
            data = stream.read(entry.size & 0x7FFFFFFF)
        if decompress and (entry.compressed or looks_like_pop_lzo(data)):
            try:
                return decompress_pop_lzo(data)
            except Exception:
                return data
        return data

    def get_wol_entries(self) -> List[BigFileEntry]:
        """All World Object List (WOL) level roots."""
        return [e for e in self.entries if level_asset_kind(e.name) == "wol"]

    def get_wow_entries(self) -> List[BigFileEntry]:
        """All World Object Wave (WOW) room / character / asset files."""
        return [e for e in self.entries if level_asset_kind(e.name) == "wow"]

    def get_bin_entries(self) -> List[BigFileEntry]:
        """All .bin files in the archive."""
        return [e for e in self.entries if e.name.casefold().endswith(".bin")]


# Attach filename and data properties to BigFileEntry for backward compatibility
if not hasattr(BigFileEntry, "filename"):
    BigFileEntry.filename = property(lambda self: self.name)

if not hasattr(BigFileEntry, "data"):
    def _entry_data(self):
        archive = getattr(self, "_archive", None)
        if archive:
            return archive.read_entry(self, decompress=False)
        return b""
    BigFileEntry.data = property(_entry_data)


def _read_popdata_archive(path: Path, data: bytes) -> BFArchive:
    """Parse POPData.BF package archive (menus, localized strings, UI textures, fonts)."""
    fat_size = struct.unpack_from("<I", data, 0)[0]
    pos = 4
    entries: List[BigFileEntry] = []
    idx = 0
    while pos < fat_size:
        id1, offset, size, f4, nlen = struct.unpack_from("<5I", data, pos)
        raw_name = data[pos + 20:pos + 20 + nlen].rstrip(b"\0")
        name = raw_name.decode("ascii", errors="replace").strip() or f"file_{idx:03d}"
        pos += 20 + nlen
        key = id1 if id1 != 0 else (0x80000000 | idx)
        data_pos = fat_size + offset
        data_header_size = 4 if name.endswith(".dds") and data[data_pos + 4:data_pos + 8] == b"DDS " else 0
        actual_size = size - data_header_size if data_header_size else size
        entries.append(BigFileEntry(
            idx, data_pos, key, actual_size, name, 0,
            0, idx, False, data_header_size, "none"
        ))
        idx += 1
    info = BigFileInfo(path, 1, len(entries), 1, len(entries), 1, 0, False, entries)
    return BFArchive(info)


def read_bigfile(path: str | Path) -> BFArchive:
    """Parse Jade .bf BigFile archive header, FAT tables, and filenames."""
    path = Path(path)
    file_size = path.stat().st_size
    with open(path, "rb") as stream:
        header = stream.read(44)
        if len(header) != 44:
            raise ValueError(f"File {path.name} is too small to be a Jade BF archive.")
        magic, version, max_file, max_dir, _max_key, _root, _free_file, _free_dir, size_fat, num_fat, universe_key = struct.unpack(
            "<4s10I", header
        )
        if magic not in (b"BIG\0", b"BUG\0"):
            # Check for POPData.BF package format
            stream.seek(0)
            file_data = stream.read()
            if len(file_data) >= 28:
                possible_fat_size = struct.unpack_from("<I", file_data, 0)[0]
                if 16 < possible_fat_size < len(file_data) and 0 < struct.unpack_from("<I", file_data, 20)[0] < 256:
                    return _read_popdata_archive(path, file_data)
            raise ValueError(f"Unrecognized BIG header magic: {magic!r}")

        entries: List[BigFileEntry] = []
        descriptor_pos = 44
        for fat_index in range(num_fat):
            stream.seek(descriptor_pos)
            raw = stream.read(24)
            if len(raw) != 24:
                raise ValueError(f"Truncated FAT descriptor #{fat_index}.")
            fat_max_file, _fat_max_dir, pos_fat, next_pos_fat, first_index, _last_index = struct.unpack("<6I", raw)

            stream.seek(pos_fat)
            file_table = stream.read(fat_max_file * 8)
            ext_base = pos_fat + size_fat * 8
            stream.seek(ext_base)
            ext_table = stream.read(fat_max_file * LEGACY_BF_FILE_ENTRY_SIZE)

            if len(file_table) != fat_max_file * 8 or len(ext_table) != fat_max_file * LEGACY_BF_FILE_ENTRY_SIZE:
                raise ValueError(f"Truncated FAT table #{fat_index}.")

            for i in range(fat_max_file):
                position, key = struct.unpack_from("<2I", file_table, i * 8)
                if key == 0xFFFFFFFF:
                    continue
                ext = ext_table[i * LEGACY_BF_FILE_ENTRY_SIZE:(i + 1) * LEGACY_BF_FILE_ENTRY_SIZE]
                physical_size = struct.unpack_from("<I", ext, 0)[0] & 0x7FFFFFFF
                parent = struct.unpack_from("<I", ext, 12)[0]
                raw_name = ext[20:84].split(b"\0", 1)[0]
                name = raw_name.decode("ascii", errors="replace").strip() or f"<file_{first_index + i:06d}>"

                data_header_size = 0
                compressed = False
                compression = "none"

                if version in (37, 38) and position + 4 <= file_size:
                    stream.seek(position)
                    header_check = struct.unpack("<I", stream.read(4))[0]
                    if header_check == physical_size:
                        data_header_size = 4
                        stream.seek(position + 4)
                        prefix = stream.read(min(32, physical_size))
                        compressed = looks_like_pop_lzo(prefix)
                        compression = "POP-LZO" if compressed else "none"

                entries.append(BigFileEntry(
                    first_index + i, position, key, physical_size, name, parent,
                    fat_index, first_index, compressed, data_header_size, compression
                ))

            descriptor_pos = next_pos_fat - 24 if next_pos_fat != 0xFFFFFFFF else descriptor_pos + 24

        # Resolve directory hierarchy if directory table is present (uncooked BigFiles like Rayman4.bf)
        if max_dir > 0 and file_size > 1024:
            try:
                stream.seek(0)
                scan_buf = stream.read(min(35 * 1024 * 1024, file_size))
                root_pos = scan_buf.find(b"\xff\xff\xff\xffROOT")
                if root_pos >= 16:
                    dir_start = root_pos - 16
                    stream.seek(dir_start)
                    dirs = []
                    for _ in range(min(max_dir, 30000)):
                        raw_dir = stream.read(84)
                        if len(raw_dir) < 84:
                            break
                        first_f, child, nxt, prv, parent = struct.unpack_from("<Iiiii", raw_dir, 0)
                        d_name = raw_dir[20:84].split(b"\0", 1)[0].decode("latin-1", "replace").strip()
                        dirs.append({"name": d_name or "Dir", "parent": parent})

                    dir_cache = {}
                    for d_idx in range(len(dirs)):
                        parts = []
                        cur = d_idx
                        seen = set()
                        while cur != -1 and 0 <= cur < len(dirs) and cur not in seen:
                            seen.add(cur)
                            parts.append(dirs[cur]["name"])
                            cur = dirs[cur]["parent"]
                        dir_cache[d_idx] = "/".join(reversed(parts))

                    for e in entries:
                        if e.parent in dir_cache:
                            e.dir_path = dir_cache[e.parent]
                            e.full_path = f"{e.dir_path}/{e.name}"
            except Exception:
                pass

    entries.sort(key=lambda e: (e.fat_index, e.index))
    info = BigFileInfo(path, version, max_file, max_dir, size_fat, num_fat, universe_key, magic == b"BUG\0", entries)
    return BFArchive(info)


# Alias
load_bf = read_bigfile
load_bf_fast = read_bigfile
BFFile = BigFileEntry
