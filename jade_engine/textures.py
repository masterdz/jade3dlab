"""Jade Engine POP texture discovery, image decoding, and DDS/TGA codecs."""
from __future__ import annotations

import io
import math
from pathlib import Path
import struct
from typing import Dict, List, Optional, Set, Tuple
from PIL import Image

from .models import TextureInfo
from .resources import parse_pop_file_entries


def scan_pop_textures(data: bytes) -> List[TextureInfo]:
    """Find Jade texture entries in data (RAW, PAL8, DXT1, DXT3, DXT5, 4-bit)."""
    textures: List[TextureInfo] = []
    for entry in parse_pop_file_entries(data):
        if entry.size < 56 or entry.data_type is None:
            continue
        # FileEntry data begins with 4 bytes before the Jade texture header
        if (struct.unpack_from("<I", data, entry.data_offset + 4)[0] != 0xFFFFFFFF
                or struct.unpack_from("<I", data, entry.data_offset + 24)[0] != 0xCAD01234
                or struct.unpack_from("<I", data, entry.data_offset + 32)[0] != 0xC0DEC0DE):
            continue
        width, height = struct.unpack_from("<hh", data, entry.data_offset + 12)
        texture_type = struct.unpack_from("<I", data, entry.data_offset + 40)[0]
        version = struct.unpack_from("<I", data, entry.data_offset + 36)[0]
        if texture_type not in (0, 1, 5, 6, 7, 11) or not (1 <= width <= 8192 and 1 <= height <= 8192):
            continue
        data_offset = entry.data_offset + 56
        if texture_type == 0 and version == 0x20000:
            data_offset -= 2
        if texture_type == 1:
            data_offset += 4
        elif texture_type == 5 and version >= 3:
            data_offset += 4
        elif texture_type == 11 and version >= 4:
            data_offset += 8
        data_end = entry.data_offset + entry.size
        if data_end <= data_offset:
            continue
        actual_w, actual_h = struct.unpack_from("<II", data, entry.data_offset + 44)
        stored_w, stored_h = (actual_w, actual_h) if 1 <= actual_w <= 8192 and 1 <= actual_h <= 8192 else (width, height)
        payload_size = data_end - data_offset
        blocks = max(1, (stored_w + 3) // 4) * max(1, (stored_h + 3) // 4)
        minimum_size = {
            0: stored_w * stored_h * 3,
            1: stored_w * stored_h,
            5: blocks * 8, 6: blocks * 16, 7: blocks * 16,
            11: (stored_w * stored_h + 1) // 2
        }.get(texture_type, 0)
        if payload_size < minimum_size:
            continue
        if texture_type == 7:
            fmt = "Raw BGRA8" if payload_size == stored_w * stored_h * 4 else "DXT5"
        elif texture_type == 6:
            fmt = "DXT3"
        elif texture_type == 5:
            fmt = "DXT1"
        elif texture_type == 0:
            fmt = "TGA/BGRA8" if payload_size >= stored_w * stored_h * 4 else "TGA/BGR24"
        elif texture_type == 1:
            fmt = "8-bit palette"
        else:
            fmt = "4-bit grayscale"
        textures.append(TextureInfo(
            len(textures), entry.data_offset, data_offset, data_end,
            stored_w, stored_h, texture_type, entry.key, fmt,
            stored_w, stored_h
        ))
    return textures


_scan_pop_textures = scan_pop_textures


def decode_pop_texture_image(data: bytes, tex: TextureInfo) -> Optional[Image.Image]:
    """Decode a Jade texture entry to a PIL RGBA Image."""
    try:
        if tex.texture_type == 7:
            blob = _dds_blob_for_dump(data, tex)
        elif tex.texture_type in (5, 6):
            blob = _compressed_dds_for_preview(bytes(data[tex.data_offset:tex.data_end]), tex)
        elif tex.texture_type == 0:
            pixel_bytes = tex.storage_width * tex.storage_height
            payload = data[tex.data_offset:tex.data_end]
            depth = 32 if len(payload) >= pixel_bytes * 4 else 24
            blob = _build_tga_header(tex.storage_width, tex.storage_height, depth) + payload[:pixel_bytes * (depth // 8)]
        elif tex.texture_type == 1:
            entries = parse_pop_file_entries(data)
            if tex.data_offset < 4:
                return None
            palette_id = struct.unpack_from("<I", data, tex.data_offset - 4)[0]
            palette_entry = next((entry for entry in entries if entry.key == palette_id), None)
            if palette_entry is None:
                return None
            palette = data[palette_entry.data_offset + 4:palette_entry.data_offset + palette_entry.size]
            blob = _build_palette_tga(tex.width, tex.height, palette, data[tex.data_offset:tex.data_end])
        elif tex.texture_type == 11:
            blob = _build_4bit_tga(tex.width, tex.height, data[tex.data_offset:tex.data_end])
        else:
            return None
        return Image.open(io.BytesIO(blob)).convert("RGBA")
    except Exception:
        return None


_decode_pop_texture_image = decode_pop_texture_image


def get_pop_texture_original_blob(data: bytes, tex: TextureInfo) -> Tuple[bytes, str]:
    """Return the raw texture in its native container format (.dds or .tga) preserving mipmaps and compression."""
    payload = bytes(data[tex.data_offset:tex.data_end])
    try:
        if tex.texture_type in (5, 6, 7) and not tex.format.startswith("Raw BGRA8"):
            blob = _dds_blob_for_dump(data, tex)
            return blob, ".dds"
        elif tex.texture_type == 7 and tex.format.startswith("Raw BGRA8"):
            blob = _build_tga_header(tex.storage_width, tex.storage_height, 32) + payload[:tex.storage_width * tex.storage_height * 4]
            return blob, ".tga"
        elif tex.texture_type == 0:
            pixel_bytes = tex.storage_width * tex.storage_height
            depth = 32 if len(payload) >= pixel_bytes * 4 else 24
            blob = _build_tga_header(tex.storage_width, tex.storage_height, depth) + payload[:pixel_bytes * (depth // 8)]
            return blob, ".tga"
        elif tex.texture_type == 1:
            entries = parse_pop_file_entries(data)
            if tex.data_offset >= 4:
                palette_id = struct.unpack_from("<I", data, tex.data_offset - 4)[0]
                palette_entry = next((entry for entry in entries if entry.key == palette_id), None)
                if palette_entry is not None:
                    palette = data[palette_entry.data_offset + 4:palette_entry.data_offset + palette_entry.size]
                    blob = _build_palette_tga(tex.width, tex.height, palette, payload)
                    return blob, ".tga"
            return payload, ".bin"
        elif tex.texture_type == 11:
            blob = _build_4bit_tga(tex.width, tex.height, payload)
            return blob, ".tga"
        else:
            return payload, ".bin"
    except Exception:
        # Fallback to preview wrapper or raw payload
        try:
            if tex.texture_type in (5, 6):
                return _compressed_dds_for_preview(payload, tex), ".dds"
        except Exception:
            pass
        return payload, ".bin"


def extract_texture_file(
    data: bytes,
    tex: TextureInfo,
    output_dir: Path | str,
    prefix: str = "",
    include_png: bool = False
) -> Tuple[Path, Optional[Path]]:
    """Save the texture in its native container format (.dds / .tga) and optionally as .png."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    blob, ext = get_pop_texture_original_blob(data, tex)
    stem = f"{prefix}tex_{tex.index + 1:03d}_0x{tex.key:08X}_{tex.width}x{tex.height}"
    out_path = output_dir / f"{stem}{ext}"
    out_path.write_bytes(blob)

    png_path = None
    if include_png:
        try:
            img = decode_pop_texture_image(data, tex)
            if img is not None:
                png_path = output_dir / f"{stem}.png"
                img.save(png_path, "PNG")
        except Exception:
            pass

    return out_path, png_path


def extract_all_textures(
    data: bytes,
    output_dir: Path | str,
    prefix: str = "",
    include_png: bool = False
) -> List[Tuple[TextureInfo, Path, Optional[Path]]]:
    """Extract all textures found in data to output_dir in their original format."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    textures = scan_pop_textures(data)
    results = []
    for tex in textures:
        try:
            out_path, png_path = extract_texture_file(data, tex, output_dir, prefix, include_png)
            results.append((tex, out_path, png_path))
        except Exception:
            continue
    return results


def _build_dds(raw_payload: bytes, width: int, height: int, header_template: bytes) -> bytes:
    header = bytearray(header_template)
    struct.pack_into("<I", header, 12, height)
    struct.pack_into("<I", header, 16, width)
    return bytes(header) + raw_payload


def _build_dds_header(width: int, height: int, num_mipmaps: int, compression: int) -> bytes:
    mip_count = max(1, num_mipmaps + 1)
    flags = 0x0002100F if mip_count == 1 else 0x000A1007
    caps = 0x00001000 if mip_count == 1 else 0x00401008
    header = bytearray(128)
    header[0:4] = b"DDS "
    struct.pack_into("<I", header, 4, 124)
    struct.pack_into("<I", header, 8, flags)
    struct.pack_into("<I", header, 12, height)
    struct.pack_into("<I", header, 16, width)
    struct.pack_into("<I", header, 28, mip_count)
    struct.pack_into("<I", header, 76, 32)
    struct.pack_into("<I", header, 80, 0x00000004)
    fourcc = {2: b"DXT1", 5: b"DXT1", 6: b"DXT3", 7: b"DXT5", 11: b"DXT5"}.get(compression)
    if fourcc is not None:
        header[84:88] = fourcc
    else:
        struct.pack_into("<I", header, 80, 0x00000041)
        struct.pack_into("<I", header, 88, 32)
        struct.pack_into("<I", header, 92, 0x00FF0000)
        struct.pack_into("<I", header, 96, 0x0000FF00)
        struct.pack_into("<I", header, 100, 0x000000FF)
        struct.pack_into("<I", header, 104, 0xFF000000)
    struct.pack_into("<I", header, 108, caps)
    return bytes(header)


def _infer_mip_count(width: int, height: int, payload_size: int, bytes_per_block: int) -> int:
    total = 0
    w, h = width, height
    for mip_count in range(1, 17):
        total += max(1, (w + 3) // 4) * max(1, (h + 3) // 4) * bytes_per_block
        if total == payload_size:
            return mip_count
        if total > payload_size or (w == 1 and h == 1):
            break
        w, h = max(1, w // 2), max(1, h // 2)
    raise ValueError("Payload does not match complete mipmap chain.")


def _infer_dxt5_mip_count(width: int, height: int, payload_size: int) -> int:
    total = 0
    mip_count = 0
    w, h = width, height
    while mip_count < 16:
        total += max(1, (w + 3) // 4) * max(1, (h + 3) // 4) * 16
        mip_count += 1
        if total == payload_size:
            return mip_count
        if total > payload_size or (w == 1 and h == 1):
            break
        w, h = max(1, w // 2), max(1, h // 2)
    raise ValueError(f"DXT5 payload does not match mipmaps for {width}x{height}")


def _infer_raw_bgra_mip_count(width: int, height: int, payload_size: int) -> int:
    total = 0
    mip_count = 0
    w, h = width, height
    while mip_count < 16:
        total += max(1, w) * max(1, h) * 4
        mip_count += 1
        if total == payload_size:
            return mip_count
        if total > payload_size or (w == 1 and h == 1):
            break
        w, h = max(1, w // 2), max(1, h // 2)
    raise ValueError(f"Raw BGRA payload does not match mipmaps for {width}x{height}")


def _dds_blob_for_dump(texture_data: bytes, tex: TextureInfo) -> bytes:
    payload = bytes(texture_data[tex.data_offset:tex.data_end])
    if tex.texture_type in (5, 6):
        bytes_per_block = 8 if tex.texture_type == 5 else 16
        try:
            mip_count = _infer_mip_count(tex.storage_width, tex.storage_height, len(payload), bytes_per_block)
        except ValueError:
            if tex.texture_type != 5 or len(payload) <= 4:
                raise
            dds_payload = payload[:-4]
            mip_count = _infer_mip_count(tex.storage_width, tex.storage_height, len(dds_payload), bytes_per_block)
        else:
            dds_payload = payload
        return _build_dds(
            dds_payload, tex.storage_width, tex.storage_height,
            _build_dds_header(tex.storage_width, tex.storage_height, mip_count - 1, tex.texture_type),
        )
    if len(payload) == tex.storage_width * tex.storage_height * 4:
        return _build_tga_header(tex.storage_width, tex.storage_height, 32) + payload
    return _build_type7_dds(payload, tex.storage_width, tex.storage_height)


def _compressed_dds_for_preview(payload: bytes, tex: TextureInfo) -> bytes:
    return _build_dds(payload, tex.width, tex.height, _build_dds_header(tex.width, tex.height, 0, tex.texture_type))


def _build_type7_dds(payload: bytes, width: int, height: int) -> bytes:
    try:
        mip_count = _infer_dxt5_mip_count(width, height, len(payload))
        return _build_dds(payload, width, height, _build_dds_header(width, height, mip_count - 1, 7))
    except ValueError:
        mip_count = _infer_raw_bgra_mip_count(width, height, len(payload))
        return _build_dds(payload, width, height, _build_dds_header(width, height, mip_count - 1, 0))


def _build_tga_header(width: int, height: int, pixel_depth: int = 32) -> bytes:
    header = bytearray(18)
    header[2] = 2
    struct.pack_into("<H", header, 12, width)
    struct.pack_into("<H", header, 14, height)
    header[16] = pixel_depth
    header[17] = 0x20 | (8 if pixel_depth == 32 else 0)
    return bytes(header)


def _build_4bit_tga(width: int, height: int, packed: bytes) -> bytes:
    pixel_count = width * height
    if len(packed) < (pixel_count + 1) // 2:
        raise ValueError("Insufficient 4-bit data")
    decoded = bytearray(pixel_count * 4)
    for pixel in range(pixel_count):
        nibble = (packed[pixel // 2] & 0x0F) if pixel % 2 == 0 else (packed[pixel // 2] >> 4)
        value = nibble * 17
        decoded[pixel * 4:pixel * 4 + 4] = bytes((value, value, value, 255))
    return _build_tga_header(width, height, 32) + bytes(decoded)


def _build_palette_tga(width: int, height: int, palette: bytes, indices: bytes) -> bytes:
    pixel_count = width * height
    if len(palette) < 1024 or len(indices) < pixel_count:
        raise ValueError("Insufficient palette data")
    decoded = bytearray(pixel_count * 4)
    for i, index in enumerate(indices[:pixel_count]):
        palette_pos = index * 4
        decoded[i * 4:i * 4 + 4] = palette[palette_pos:palette_pos + 4]
    return _build_tga_header(width, height, 32) + bytes(decoded)
