import struct
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from io import BytesIO


@dataclass
class BFFile:
    offset: int
    key: int
    size: int
    data: bytes
    filename: str = ""


@dataclass
class BFArchive:
    version: int
    elem_count: int
    files: List[BFFile] = field(default_factory=list)
    filenames: Dict[int, str] = field(default_factory=dict)

    def get_file_by_key(self, key: int) -> Optional[BFFile]:
        for f in self.files:
            if f.key == key:
                return f
        return None

    def get_file_by_name(self, name: str) -> Optional[BFFile]:
        norm = name.lstrip('?').strip().lower()
        for f in self.files:
            if f.filename and f.filename.lstrip('?').strip().lower() == norm:
                return f
            if f.filename and f.filename.lower() == name.lower():
                return f
        return None

    def get_files_by_extension(self, ext: str) -> List[BFFile]:
        if not ext.startswith('.'):
            ext = '.' + ext
        return [f for f in self.files if f.filename.lower().endswith(ext.lower())]


def _extract_filenames_from_data(data: bytes) -> Dict[str, str]:
    hash_to_filename = {}
    patterns = [
        rb'[\x20-\x7e]{3,60}_(?:wow|wol)_([0-9a-f]{8})\.bin\x00',
        rb'[\x20-\x7e]{3,60}_([0-9a-f]{8})\.bin\x00',
        rb'[\x20-\x7e]{3,60}\.bin\x00',
    ]
    for pattern in patterns:
        for m in re.finditer(pattern, data):
            filename = m.group(0).rstrip(b'\x00').decode('ascii', errors='replace')
            if filename.startswith('?'):
                filename = filename[1:]
            hash_match = re.search(r'_([0-9a-f]{8})\.bin$', filename)
            if hash_match:
                hash_str = hash_match.group(1).upper()
                hash_to_filename[hash_str] = filename
    return hash_to_filename


def parse_bf(data: bytes) -> BFArchive:
    buf = BytesIO(data)

    magic = buf.read(4)
    if magic != b'BIG\x00':
        raise ValueError(f"Invalid BF magic: {magic!r}")

    version = struct.unpack('<I', buf.read(4))[0]
    elem_count = struct.unpack('<I', buf.read(4))[0]
    buf.read(4)
    buf.read(8)
    buf.read(8)
    buf.read(4)
    buf.read(4)
    buf.read(4)

    archive = BFArchive(version=version, elem_count=elem_count)

    buf.read(4)
    buf.read(4)
    buf.read(4)
    buf.read(4)
    buf.read(4)
    buf.read(4)

    fat_entries = []
    for _ in range(elem_count):
        offset = struct.unpack('<I', buf.read(4))[0]
        key = struct.unpack('<I', buf.read(4))[0]
        fat_entries.append((offset, key))

    hash_to_filename = _extract_filenames_from_data(data)

    for i, (offset, key) in enumerate(fat_entries):
        buf.seek(offset)
        file_size = struct.unpack('<I', buf.read(4))[0]
        file_data = buf.read(file_size)

        key_str = f'{key:08X}'
        filename = hash_to_filename.get(key_str, "")

        bf_file = BFFile(
            offset=offset,
            key=key,
            size=file_size,
            data=file_data,
            filename=filename,
        )
        archive.files.append(bf_file)

    return archive


def load_bf(path: str) -> BFArchive:
    with open(path, 'rb') as f:
        data = f.read()
    return parse_bf(data)


def _scan_hash_names(f) -> Dict[str, str]:
    import os as _os
    f.seek(0, _os.SEEK_END)
    size = f.tell()
    step = 1 << 20
    hash_to_filename = {}
    overlap = 128
    buf = b''
    pos = 0
    f.seek(0)
    while pos < size:
        chunk = f.read(step)
        if not chunk:
            break
        data = buf + chunk
        for m in re.finditer(rb'[\x20-\x7e]{3,60}_([0-9a-fA-F]{8})\.bin\x00', data):
            filename = m.group(0).rstrip(b'\x00').decode('ascii', errors='replace')
            filename = filename.lstrip('?').strip()
            hm = re.search(r'_([0-9a-fA-F]{8})\.bin$', filename)
            if hm:
                hash_to_filename[hm.group(1).upper()] = filename
        buf = data[-overlap:] if len(data) > overlap else data
        pos += len(chunk)
    return hash_to_filename


def _find_string_table(f, fat_data: bytes, elem_count: int, version: int):
    import os as _os
    keys = [struct.unpack('<I', fat_data[i*8+4:i*8+8])[0] for i in range(elem_count)]
    f.seek(0, _os.SEEK_END)
    size = f.tell()
    step = 1 << 20
    overlap = 256
    buf = b''
    base = 0
    pos = 0
    f.seek(0)
    first = None
    while pos < size:
        chunk = f.read(step)
        if not chunk:
            break
        data = buf + chunk
        for m in re.finditer(rb'[\x20-\x7e]{3,60}_[0-9a-fA-F]{8}\.bin\x00', data):
            first = base + m.start()
            break
        if first is not None:
            break
        buf = data[-overlap:] if len(data) > overlap else data
        base = pos - len(buf) + overlap if buf else pos
        pos += len(chunk)
    if first is None:
        return None
    for k in range(min(elem_count, 400)):
        start = first - 20 - k * 84
        if start < 0:
            continue
        f.seek(start)
        try:
            raw = f.read(84 * min(elem_count, 12))
        except Exception:
            continue
        if len(raw) < 84:
            continue
        score = tested = 0
        for i in range(min(elem_count, 12)):
            off = i * 84
            nm = raw[off+20:off+84].split(b'\x00')[0]
            try:
                s = nm.decode('ascii')
            except Exception:
                break
            import re as _re
            hm = _re.search(r'_([0-9a-fA-F]{8})\.bin$', s)
            if not hm:
                break
            tested += 1
            if hm.group(1).upper() == f'{keys[i]:08X}':
                score += 1
        if tested >= 8 and score == tested:
            return start
    return None


def load_bf_fast(path: str) -> BFArchive:
    with open(path, 'rb') as f:
        header = f.read(68)
        magic = header[0:4]
        if magic != b'BIG\x00':
            raise ValueError(f"Invalid BF magic: {magic!r}")

        version = struct.unpack('<I', header[4:8])[0]
        elem_count = struct.unpack('<I', header[8:12])[0]

        archive = BFArchive(version=version, elem_count=elem_count)

        fat_start = 68
        f.seek(fat_start)
        fat_data = f.read(elem_count * 8)

        known_offsets = {
            (37, 3308): 0x1796EC,
            (38, 5346): 0x1C90AC,
            (38, 6648): 0x1C34EC,
            (38, 3897): 0x1B5E84,
            (38, 5272): 0x1C07F4,
            (38, 538): 0x10F34C,
            (42, 2517): 0x009C84,
            (38, 6432): 0x1A2DF4,
            (37, 159): 0x152B9C,
            (37, 102): None,
        }

        string_table = []
        table_off = known_offsets.get((version, elem_count), 'auto')
        if table_off is None:
            table_off = _find_string_table(f, fat_data, elem_count, version)

        if table_off is not None:
            f.seek(table_off)
            for i in range(elem_count):
                aligned_len = struct.unpack('<i', f.read(4))[0]
                next_idx = struct.unpack('<i', f.read(4))[0]
                prev_idx = struct.unpack('<i', f.read(4))[0]
                d = struct.unpack('<I', f.read(4))[0]
                e = struct.unpack('<I', f.read(4))[0]
                raw_name = f.read(64)
                filename = raw_name.split(b'\x00')[0].decode('ascii', errors='replace')
                filename = filename.lstrip('?').strip()
                filename = ''.join(c for c in filename if c.isprintable() or c in ('_', '-', '.', ' '))

                if version >= 42:
                    f.read(4)
                    f.read(32)
                    f.read(4)

                string_table.append({
                    'aligned_len': aligned_len,
                    'next': next_idx,
                    'prev': prev_idx,
                    'd': d,
                    'e': e,
                    'filename': filename,
                    'index': i,
                })

            for i, entry in enumerate(string_table):
                archive.filenames[i] = entry['filename']

        hash_names = None
        if not string_table:
            hash_names = _scan_hash_names(f)

        for i in range(elem_count):
            offset = struct.unpack('<I', fat_data[i*8:i*8+4])[0]
            key = struct.unpack('<I', fat_data[i*8+4:i*8+8])[0]

            filename = ""
            if i < len(string_table):
                filename = string_table[i]['filename']
            elif hash_names is not None:
                filename = hash_names.get(f'{key:08X}', '')

            f.seek(offset)
            file_size = struct.unpack('<I', f.read(4))[0]
            file_data = f.read(file_size)

            bf_file = BFFile(
                offset=offset,
                key=key,
                size=file_size,
                data=file_data,
                filename=filename,
            )
            archive.files.append(bf_file)

    return archive
