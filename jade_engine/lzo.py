"""High-performance LZO compression and decompression for Prince of Persia Jade BigFiles and BINs."""
from __future__ import annotations

import ctypes
import os
import platform
import struct
import subprocess
import sys
from pathlib import Path

LZO_BLOCK_SIZE = 131072  # 128 KB
MODULE_DIR = Path(__file__).resolve().parent

_lib_instance = None


def _get_lzo_library():
    """Load or build the native LZO shared library."""
    global _lib_instance
    if _lib_instance is not None:
        return _lib_instance

    system = platform.system().lower()
    candidate_paths = []

    if system == "darwin":
        candidate_paths.append(MODULE_DIR / "libminilzo.dylib")
    elif system == "linux":
        candidate_paths.append(MODULE_DIR / "libminilzo.so")
    elif system == "windows":
        candidate_paths.extend([
            MODULE_DIR / "lzo_compat.dll",
            MODULE_DIR / "lzo.dll",
            MODULE_DIR / "libminilzo.dll",
        ])

    for path in candidate_paths:
        if path.is_file():
            try:
                lib = ctypes.CDLL(str(path))
                if hasattr(lib, "lzo1x_decompress_safe"):
                    _lib_instance = lib
                    return _lib_instance
                if hasattr(lib, "lzo_bridge_decompress"):
                    _lib_instance = lib
                    return _lib_instance
            except Exception:
                pass

    # If on macOS or Linux and shared library not found, attempt compilation of minilzo.c
    minilzo_c = MODULE_DIR / "minilzo.c"
    if minilzo_c.is_file() and system in ("darwin", "linux"):
        target_name = "libminilzo.dylib" if system == "darwin" else "libminilzo.so"
        target_path = MODULE_DIR / target_name
        compiler = "clang" if subprocess.run(["which", "clang"], capture_output=True).returncode == 0 else "gcc"
        cmd = [compiler, "-O3", "-shared", "-fPIC", "-o", str(target_path), str(minilzo_c)]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            if target_path.is_file():
                _lib_instance = ctypes.CDLL(str(target_path))
                return _lib_instance
        except Exception:
            pass

    return None


def looks_like_pop_lzo(data: bytes) -> bool:
    """Check if data starts with POP block-LZO header."""
    if len(data) < 18:
        return False
    dec_size, enc_size = struct.unpack_from("<2I", data, 0)
    if dec_size <= enc_size or enc_size <= 0 or dec_size > 16 * 1024 * 1024:
        return False
    markers = (b"\x99\xC0\xFF\xEE", b"\x99\xC0\xFF\xFE")
    return any(data[13:17] == marker or data[14:18] == marker for marker in markers)


_looks_like_pop_lzo = looks_like_pop_lzo


def _python_decompress_lzo1x_block(block: bytes, expected_size: int) -> bytes:
    """Pure-Python LZO1X decoder fallback."""
    ip = 0
    op = bytearray()
    blen = len(block)

    def need(n: int) -> None:
        if ip + n > blen:
            raise ValueError("Truncated LZO block.")

    def copy_literals(n: int) -> None:
        nonlocal ip
        need(n)
        op.extend(block[ip:ip + n])
        ip += n

    if not block:
        raise ValueError("Empty LZO block.")
    t = block[ip]
    ip += 1
    if t > 17:
        copy_literals(t - 17)
    else:
        t = 0

    while ip < blen:
        if t <= 15:
            if t == 0:
                zeros = 0
                while ip < blen and block[ip] == 0:
                    zeros += 1
                    ip += 1
                if ip >= blen:
                    raise ValueError("Truncated LZO literal length.")
                t = 18 + zeros * 255 + block[ip]
                ip += 1
            else:
                t += 3
            copy_literals(t)
            if ip >= blen:
                break
            t = block[ip]
            ip += 1
        elif t <= 31:
            need(1)
            m_off = (t & 8) << 11
            m_off += block[ip] << 3
            m_off += (t >> 2) & 7
            m_off += 1
            match_len = (t & 3) + 2
            ip += 1
            need(1)
            m_off += block[ip] >> 5
            ip += 1
            if m_off > len(op):
                raise ValueError("Invalid LZO match offset.")
            for _ in range(match_len):
                op.append(op[-m_off])
            t = block[ip] if ip < blen else 17
            if ip < blen:
                ip += 1
        else:
            if t >= 64:
                need(1)
                m_off = ((t >> 2) & 7) | (block[ip] << 3)
                m_off += 1
                match_len = (t >> 5) + 1
                ip += 1
            elif t >= 32:
                match_len = (t & 31) + 2
                need(2)
                m_off = (block[ip] >> 2) | ((t & 8) << 11)
                m_off += 1
                ip += 2
            else:
                if t == 17 and ip + 2 <= blen:
                    break
                match_len = t & 7
                need(2)
                m_off = (block[ip] >> 2) | ((t & 8) << 11)
                m_off += 1
                ip += 2
                if match_len == 0:
                    while ip < blen and block[ip] == 0:
                        match_len += 255
                        ip += 1
                    need(1)
                    match_len += 31 + block[ip] + 2
                    ip += 1
                else:
                    match_len += 2
            if m_off > len(op):
                raise ValueError("Invalid LZO match offset.")
            for _ in range(match_len):
                op.append(op[-m_off])
            if ip >= blen:
                break
            t = block[ip]
            ip += 1

    if len(op) != expected_size:
        raise ValueError(f"LZO decompression size mismatch: got {len(op)}, expected {expected_size}")
    return bytes(op)


def decompress_pop_lzo(data: bytes) -> bytes:
    """Decompress POP's little-endian LZO multi-block stream (128KB chunks)."""
    if len(data) < 8:
        return data

    lib = _get_lzo_library()
    has_lzo1x = lib is not None and hasattr(lib, "lzo1x_decompress_safe")
    has_bridge = lib is not None and hasattr(lib, "lzo_bridge_decompress")

    pos = 0
    total_len = len(data)
    output = bytearray()

    while pos + 8 <= total_len:
        dec_size, enc_size = struct.unpack_from("<2I", data, pos)
        if dec_size == 0 or enc_size == 0:
            break
        pos += 8
        if enc_size > total_len - pos:
            break
        block = data[pos:pos + enc_size]
        pos += enc_size

        if dec_size == enc_size:
            output.extend(block)
        elif has_lzo1x:
            dst = (ctypes.c_ubyte * dec_size)()
            dst_len = ctypes.c_size_t(dec_size)
            rc = lib.lzo1x_decompress_safe(block, enc_size, dst, ctypes.byref(dst_len), None)
            if rc != 0:
                raise ValueError(f"LZO1X decompression failed: rc={rc}")
            output.extend(bytes(dst[:dst_len.value]))
        elif has_bridge:
            src = (ctypes.c_ubyte * len(block)).from_buffer_copy(block)
            dst = (ctypes.c_ubyte * dec_size)()
            out_size = ctypes.c_size_t(dec_size)
            rc = lib.lzo_bridge_decompress(src, len(block), dst, ctypes.byref(out_size))
            if rc != 0 or out_size.value != dec_size:
                raise ValueError(f"LZO bridge decompression failed (rc={rc})")
            output.extend(bytes(dst[:out_size.value]))
        else:
            output.extend(_python_decompress_lzo1x_block(block, dec_size))

        if dec_size < LZO_BLOCK_SIZE:
            break

    if not output:
        return data
    return bytes(output)


# Backward compatibility
lzo_decompress = decompress_pop_lzo
