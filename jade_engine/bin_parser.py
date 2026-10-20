import struct
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from io import BytesIO
from .lzo import decompress_pop_lzo, looks_like_pop_lzo, lzo_decompress


@dataclass
class BinEntry:
    hash_id: str
    type_id: str
    data: bytes


@dataclass
class BinFile:
    hash_id: str
    entries: List[BinEntry] = field(default_factory=list)
    raw_data: bytes = b''


def parse_bin(data: bytes) -> BinFile:
    buf = BytesIO(data)
    hash_bytes = buf.read(4)
    hash_id = hash_bytes[::-1].hex().upper()
    bin_file = BinFile(hash_id=hash_id, raw_data=data)
    content = data[4:] if len(data) > 4 else b''
    blocks = content.split(b'\x99\xC0\xFF\xEE')

    for block in blocks:
        if len(block) < 8:
            continue
        block_hash = block[:4][::-1].hex().upper()
        type_id = block[4:8][::-1].hex().upper()
        block_data = block[8:]
        entry = BinEntry(
            hash_id=block_hash,
            type_id=type_id,
            data=block_data,
        )
        bin_file.entries.append(entry)

    return bin_file


def decompress_bin(data: bytes) -> bytes:
    """Decompress BIN data using robust POP-LZO multi-block decompressor."""
    if len(data) < 8:
        return data

    if looks_like_pop_lzo(data):
        return decompress_pop_lzo(data)

    # If first 4 bytes is size/hash prefix and remainder is LZO:
    if len(data) > 12 and looks_like_pop_lzo(data[4:]):
        return decompress_pop_lzo(data[4:])

    # Check if first dword is POP magic
    first_dword = struct.unpack('<I', data[:4])[0]
    if first_dword in (0x99C0FFEE, 0x99C0FFFE):
        return data

    try:
        return decompress_pop_lzo(data)
    except Exception:
        return data


def extract_all_from_bin(data: bytes) -> Dict[str, bytes]:
    result = {}
    decompressed = decompress_bin(data)
    blocks = decompressed.split(b'\x99\xC0\xFF\xEE')

    for block in blocks:
        if len(block) < 8:
            continue
        block_hash = block[:4][::-1].hex().upper()
        type_id = block[4:8][::-1].hex().upper()
        block_data = block[8:]
        key = f"{block_hash}_{type_id}"
        result[key] = block_data

    return result
