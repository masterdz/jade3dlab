import struct
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from io import BytesIO
from .lzo import lzo_decompress


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
    if len(data) < 8:
        return data

    buf = BytesIO(data)
    hash_bytes = buf.read(4)
    hash_id = hash_bytes[::-1].hex().upper()

    content = data[4:]

    if len(content) < 4:
        return content

    first_dword = struct.unpack('<I', content[:4])[0]

    if first_dword == 0x99C0FFEE:
        return content

    try:
        decompressed = lzo_decompress(content, len(content) * 10)
        return decompressed
    except Exception:
        return content


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
