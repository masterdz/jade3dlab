import struct
import numpy as np
from typing import List, Dict, Optional


class Reader:
    def __init__(self, buf: bytes):
        self.b = buf
        self.pos = 0
        self.length = len(buf)

    def remaining(self):
        return self.length - self.pos

    def read(self, n):
        if self.pos + n > self.length:
            raise IndexError("read past end")
        r = self.b[self.pos:self.pos + n]
        self.pos += n
        return r

    def read_hex(self):
        return self.read(4)[::-1].hex().upper()

    def u8(self, n=None):
        if n is None:
            return struct.unpack('<B', self.read(1))[0]
        return struct.unpack(f'<{n}B', self.read(n))

    def u16(self, n=None):
        if n is None:
            return struct.unpack('<H', self.read(2))[0]
        return struct.unpack(f'<{n}H', self.read(n * 2))

    def u32(self, n=None):
        if n is None:
            return struct.unpack('<I', self.read(4))[0]
        return struct.unpack(f'<{n}I', self.read(n * 4))

    def f32(self, n=None):
        if n is None:
            return struct.unpack('<f', self.read(4))[0]
        return struct.unpack(f'<{n}f', self.read(n * 4))

    def cstr(self):
        out = bytearray()
        while self.pos < self.length:
            c = self.read(1)
            if c == b'\x00':
                break
            out += c
        return out.decode('ascii', errors='replace')

    def eof(self):
        return self.pos >= self.length


def _parse_mesh_block(block: bytes, hash_id: str) -> Optional[Dict]:
    try:
        r = Reader(block)
        r.read_hex()
        r.read_hex()
        version = r.read_hex()
        if version not in ("00000007", "00000008"):
            return None

        flags = r.u32()
        has_second = r.u32() != 0
        num_vertices = r.u32()
        num_unknown = r.u32()
        has_unknown = r.u32() != 0
        num_uvs = r.u32()
        num_materials = r.u32()

        if not (1 <= num_vertices <= 100000):
            return None
        if not (0 <= num_uvs <= 100000):
            return None
        if not (1 <= num_materials <= 256):
            return None

        if flags & 0x8 or flags & 0x10:
            r.f32()
            has_normals = r.u16() != 0
            num4 = r.u16()
            for _ in range(num4):
                r.u16()
                nf = r.u16()
                r.f32(16)
                r.read_hex()
                r.f32(nf)
            if num4 > 0:
                has_normals = (r.u32() != 0) or has_normals
        else:
            r.u32()
            has_normals = r.u32() != 0

        vert_data = r.f32(3 * num_vertices)
        vertices = np.array(vert_data, dtype=np.float32).reshape(-1, 3)

        if has_unknown:
            r.f32(num_unknown)

        if has_normals:
            r.f32(3 * num_vertices)

        uv_data = r.f32(2 * num_uvs) if num_uvs else []
        uvs = np.array(uv_data, dtype=np.float32).reshape(-1, 2) if num_uvs else np.zeros((0, 2), dtype=np.float32)

        material_ids = []
        num_faces = 0
        for _ in range(num_materials):
            n = r.u32()
            mid = r.u32()
            num_faces += n
            material_ids.append((mid, n))

        if not (0 < num_faces <= 200000):
            return None

        faces, uv_idx = [], []
        for _ in range(num_faces):
            faces.append(r.u16(3))
            uv_idx.append(r.u16(3))
            r.u16(2)

        return {
            'vertices': vertices,
            'uvs': uvs,
            'faces': np.array(faces, dtype=np.int32),
            'uv_indices': np.array(uv_idx, dtype=np.int32),
            'material_ids': material_ids,
        }
    except Exception:
        return None


def extract_all_meshes(blocks: List[bytes]) -> Dict[str, Dict]:
    meshes = {}
    for block in blocks:
        if len(block) < 100:
            continue
        type_id = block[4:8][::-1].hex().upper()
        if type_id != "00000001":
            continue
        hash_id = block[:4][::-1].hex().upper()
        m = _parse_mesh_block(block, hash_id)
        if m is not None and len(m['faces']) > 0:
            meshes[hash_id] = m
    if meshes:
        return meshes
    return extract_vertex_soups(blocks)


def _find_float_runs(arr: np.ndarray, lo: float = -20000.0, hi: float = 20000.0,
                      start: int = 2) -> List[tuple]:
    with np.errstate(invalid='ignore'):
        finite = np.isfinite(arr)
        sane = finite & (arr >= lo) & (arr <= hi)
    runs = []
    cur_start, cur_len = 0, 0
    for idx in range(start, len(arr)):
        if sane[idx]:
            if cur_len == 0:
                cur_start = idx
            cur_len += 1
        else:
            if cur_len > 0:
                runs.append((cur_start, cur_len))
            cur_len = 0
    if cur_len > 0:
        runs.append((cur_start, cur_len))
    return runs


def extract_vertex_soups(blocks: List[bytes], min_tris: int = 12) -> Dict[str, Dict]:
    soups = {}
    for block in blocks:
        if len(block) < 64:
            continue
        hash_id = block[:4][::-1].hex().upper()
        type_id = block[4:8][::-1].hex().upper()
        if type_id in ("776F772E", "6F61672E", "00000004", "00000005"):
            continue
        try:
            arr = np.frombuffer(block, dtype='<f4')
        except Exception:
            continue
        best = None
        for (s, ln) in _find_float_runs(arr):
            n_floats = (ln // 3) * 3
            if n_floats < min_tris * 3:
                continue
            verts = np.array(arr[s:s + n_floats], dtype=np.float32).reshape(-1, 3)
            with np.errstate(invalid='ignore', over='ignore'):
                if not bool(np.isfinite(verts).all()):
                    continue
                span = float(verts.max() - verts.min())
                if not span == span or span < 1e-3 or span > 40000.0:
                    continue
                spans = verts.max(axis=0) - verts.min(axis=0)
            if int((spans > 1e-3).sum()) < 2:
                continue
            nv = len(verts)
            score = nv * min(span, 500.0)
            if best is None or score > best[0]:
                best = (score, s, verts)
        if best is None:
            continue
        _, s, verts = best
        if len(verts) > 8000:
            step = len(verts) // 8000 + 1
            verts = verts[::step].copy()
        faces = _find_faces_after(block, s, len(verts))
        soups[hash_id + '_soup'] = {
            'vertices': verts,
            'uvs': np.zeros((0, 2), dtype=np.float32),
            'faces': faces,
            'uv_indices': np.zeros((0, 3), dtype=np.int32),
            'material_ids': [],
            'offset': s * 4,
            'soup': len(faces) == 0,
        }
    return soups


def _find_faces_after(block: bytes, vert_start_f: int, nverts: int) -> np.ndarray:
    import struct as _st
    v_end = (vert_start_f + nverts) * 3 * 4
    best = None
    for gap in range(0, 4096, 2):
        pos = v_end + gap
        if pos + 18 > len(block):
            break
        idx = np.frombuffer(block[pos:pos + 4096], dtype='<u2') if pos + 4096 <= len(block) else np.frombuffer(block[pos:], dtype='<u2')
        if len(idx) < 12:
            continue
        ok = int(((idx < nverts)).sum())
        if ok < 12:
            continue
        run = 0
        for v in idx:
            if v < nverts:
                run += 1
            else:
                break
        run -= run % 3
        if run >= 12 and (best is None or run > len(best)) and run <= nverts * 8:
            best = np.array(idx[:run].reshape(-1, 3), dtype=np.int32)
        if best is not None and run < 12:
            break
    if best is None:
        return np.zeros((0, 3), dtype=np.int32)
    return best


def _scan_name(block: bytes):
    import re as _re
    best = ('', 0)
    for m in _re.finditer(rb'[A-Za-z0-9_][A-Za-z0-9_\-]{3,60}', block[8:128]):
        s = m.group(0).decode('ascii')
        if '_' in s and len(s) > len(best[0]):
            best = (s, 8 + m.start())
    return best


def find_object_transforms(blocks: List[bytes]) -> List[Dict]:
    import struct as _st
    keys = set()
    for b in blocks:
        if len(b) >= 4:
            keys.add(_st.unpack('<I', b[:4])[0])
    out = []
    for block in blocks:
        if len(block) < 200:
            continue
        if block[4:8] != b'.gao':
            continue
        hid = block[:4][::-1].hex().upper()
        name, name_off = _scan_name(block)
        if len(name) < 3:
            continue
        n4 = (len(block) // 4) * 4
        try:
            arr = np.frombuffer(block[:n4], dtype='<f4')
        except Exception:
            continue
        with np.errstate(invalid='ignore'):
            finite = np.isfinite(arr)
        pos = None
        box = None
        start_i = 2
        for i in range(start_i, len(arr) - 16):
            if not bool(finite[i:i + 16].all()):
                continue
            m = arr[i:i + 16]
            if abs(m[12]) < 1e-3 and abs(m[13]) < 1e-3 and abs(m[14]) < 1e-3 and abs(m[15] - 1.0) < 1e-2:
                if not bool((np.abs(m[:12]) < 20000).all()):
                    continue
                r0 = m[0:3]
                r1 = m[4:7]
                r2 = m[8:11]
                n0, n1, n2 = float(np.dot(r0, r0)), float(np.dot(r1, r1)), float(np.dot(r2, r2))
                if n0 < 1e-6 or n1 < 1e-6 or n2 < 1e-6:
                    continue
                if max(n0, n1, n2) / min(n0, n1, n2) > 4.0:
                    continue
                if abs(float(np.dot(r0, r1))) / (n0 * n1) ** 0.5 > 0.05:
                    continue
                if abs(float(np.dot(r0, r2))) / (n0 * n2) ** 0.5 > 0.05:
                    continue
                if abs(float(np.dot(r1, r2))) / (n1 * n2) ** 0.5 > 0.05:
                    continue
                tx, ty, tz = float(m[3]), float(m[7]), float(m[11])
                if abs(tx) < 20000 and abs(ty) < 20000 and abs(tz) < 20000:
                    pos = (tx, ty, tz)
                    break
        for i in range(start_i, len(arr) - 6):
            if not bool(finite[i:i + 6].all()):
                continue
            mn = arr[i:i + 3]
            mx = arr[i + 3:i + 6]
            if bool(((mx - mn) > 0.05).all()) and bool(((mx - mn) < 20000.0).all()):
                if bool((np.abs(mn) < 20000).all()) and bool((np.abs(mx) < 20000).all()):
                    bmn = tuple(float(v) for v in mn)
                    bmx = tuple(float(v) for v in mx)
                    if pos is not None:
                        if not all(bmn[k] - 0.5 <= pos[k] <= bmx[k] + 0.5 for k in range(3)):
                            continue
                    box = (bmn, bmx)
                    if pos is None:
                        pos = tuple(float((a + b) / 2) for a, b in zip(bmn, bmx))
                    break
        mesh_key = None
        for o in range(0, min(len(block) - 4, 4096), 4):
            k = _st.unpack('<I', block[o:o + 4])[0]
            if k in keys and f'{k:08X}' != hid:
                mesh_key = f'{k:08X}'
                break
        out.append({'name': name, 'hash': hid, 'block_size': len(block),
                    'pos': pos, 'box': box, 'mesh_key': mesh_key})
    return out


def find_gao_names(blocks: List[bytes]) -> List[Dict]:
    return [
        {'name': o['name'], 'hash': o['hash'], 'block_size': o['block_size'],
         'name_offset': 24}
        for o in find_object_transforms(blocks)
    ]
