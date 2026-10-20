"""Bounds-checked readers for the Jade / POP FileEntry resource streams."""
from __future__ import annotations

import struct
from .models import PopFileEntry


class PopReader:
    """Bounds-checked binary reader for Jade records."""

    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def _need(self, size: int) -> None:
        if size < 0 or self.pos + size > len(self.data):
            raise ValueError(f"Truncated data at 0x{self.pos:X} ({size} B requested, total={len(self.data)}).")

    def u32(self) -> int:
        self._need(4)
        value = struct.unpack_from("<I", self.data, self.pos)[0]
        self.pos += 4
        return value

    def i32(self) -> int:
        self._need(4)
        value = struct.unpack_from("<i", self.data, self.pos)[0]
        self.pos += 4
        return value

    def u16(self) -> int:
        self._need(2)
        value = struct.unpack_from("<H", self.data, self.pos)[0]
        self.pos += 2
        return value

    def i16(self) -> int:
        self._need(2)
        value = struct.unpack_from("<h", self.data, self.pos)[0]
        self.pos += 2
        return value

    def f32(self) -> float:
        self._need(4)
        value = struct.unpack_from("<f", self.data, self.pos)[0]
        self.pos += 4
        return value

    def bytes(self, size: int) -> bytes:
        self._need(size)
        value = self.data[self.pos:self.pos + size]
        self.pos += size
        return value

    def u32s(self, count: int) -> list[int]:
        if count < 0 or count > 2_000_000:
            raise ValueError(f"Implausible uint32 count: {count}")
        return [self.u32() for _ in range(count)]

    def i16s(self, count: int) -> list[int]:
        if count < 0 or count > 6_000_000:
            raise ValueError(f"Implausible int16 count: {count}")
        return [self.i16() for _ in range(count)]

    def f32s(self, count: int) -> list[float]:
        if count < 0 or count > 6_000_000:
            raise ValueError(f"Implausible float count: {count}")
        return [self.f32() for _ in range(count)]


# Alias for backward compatibility
_PopReader = PopReader


def parse_pop_file_entries(data: bytes) -> list[PopFileEntry]:
    """Parse the FileEntry stream (size, magic, key) in Jade / POP files."""
    entries: list[PopFileEntry] = []
    pos = 0
    total_len = len(data)
    while pos + 12 <= total_len:
        size, magic, key = struct.unpack_from("<III", data, pos)
        data_offset = pos + 12
        end = data_offset + size
        if end > total_len:
            # Reached container padding or truncated block
            break
        data_type = struct.unpack_from("<I", data, data_offset)[0] if size >= 4 else None
        entries.append(PopFileEntry(len(entries), pos, size, magic, key, data_offset, data_type))
        pos = end
    return entries


_parse_pop_file_entries = parse_pop_file_entries
