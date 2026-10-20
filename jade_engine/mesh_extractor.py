import re
import struct
import numpy as np
from typing import List, Dict, Optional


class Reader:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def u32(self):
        v = struct.unpack_from('<I', self.data, self.pos)[0]
        self.pos += 4
        return v

    def i32(self):
        v = struct.unpack_from('<i', self.data, self.pos)[0]
        self.pos += 4
        return v

    def u16(self):
        v = struct.unpack_from('<H', self.data, self.pos)[0]
        self.pos += 2
        return v

    def i16(self):
        v = struct.unpack_from('<h', self.data, self.pos)[0]
        self.pos += 2
        return v

    def f32(self, n=None):
        if n is None:
            v = struct.unpack_from('<f', self.data, self.pos)[0]
            self.pos += 4
            return v
        vals = struct.unpack_from(f'<{n}f', self.data, self.pos)
        self.pos += n * 4
        return list(vals)

    def bytes(self, n):
        v = self.data[self.pos:self.pos + n]
        self.pos += n
        return v


def decode_mesh_block(block: bytes) -> Optional[Dict]:
    try:
        r = Reader(block)
        r.u32()
        magic = r.bytes(4)
        type_str = magic.decode('ascii', errors='replace')
        if type_str != '.gao':
            return None

        version = r.u32()
        if version not in (7, 8):
            return None

        flags = r.u32()
        has_second = r.u32() != 0
        num_vertices = r.u32()
        num_unknown = r.u32()
        has_unknown = r.u32() != 0
        num_uvs = r.u32()
        num_materials = r.u32()

        if num_vertices == 0 or num_vertices > 500000:
            return None
        if num_materials == 0 or num_materials > 4096:
            return None

        vert_data = r.f32(3 * num_vertices)

        if has_unknown:
            r.f32(num_unknown)

        if has_unknown:
            r.f32(3 * num_vertices)
            normal_data = []
        else:
            normal_data = r.f32(3 * num_vertices)

        uv_data = r.f32(2 * num_uvs)

        material_ids = []
        num_faces = 0
        for _ in range(num_materials):
            count = r.i32()
            mat_id = r.i32()
            material_ids.append((mat_id, count))
            num_faces += count

        if num_faces == 0 or num_faces > 2000000:
            return None

        faces = []
        uv_indices = []
        for _ in range(num_faces):
            v1 = r.i16()
            v2 = r.i16()
            v3 = r.i16()
            faces.append((v1, v2, v3))
            if num_uvs > 0:
                u1 = r.i16()
                u2 = r.i16()
                u3 = r.i16()
                uv_indices.append((u1, u2, u3))
            r.i16()
            r.i16()

        if has_second:
            r.u32()
            r.u32()
            nv2 = r.u32()
            r.bytes(nv2 * 12)
            if num_uvs > 0:
                size2 = r.u32()
                r.bytes(size2 * 6)

        return {
            'vertices': np.array(vert_data, dtype=np.float32).reshape(-1, 3),
            'normals': np.array(normal_data, dtype=np.float32).reshape(-1, 3) if normal_data else np.array([]),
            'uvs': np.array(uv_data, dtype=np.float32).reshape(-1, 2),
            'faces': np.array(faces, dtype=np.int32),
            'uv_indices': np.array(uv_indices, dtype=np.int32),
            'material_ids': material_ids,
            'layout_name': 'Character / skin' if has_unknown else 'Static mesh',
        }
    except (ValueError, IndexError, struct.error):
        return None


def extract_all_meshes(blocks: List[bytes]) -> Dict[str, Dict]:
    meshes = {}
    for i, block in enumerate(blocks):
        m = decode_mesh_block(block)
        if m:
            hash_id = block[:4][::-1].hex().upper() if len(block) >= 4 else f"{i:04d}"
            meshes[hash_id] = m
    return meshes


def find_gao_names(blocks: List[bytes]) -> List[Dict]:
    objects = []
    for i, block in enumerate(blocks):
        if len(block) < 32:
            continue
        hash_id = block[:4][::-1].hex().upper()
        # Look for GAO strings
        for m in re.finditer(rb'[\x20-\x7e]{3,60}\.gao\x00', block):
            name = m.group(0).rstrip(b'\x00').decode('ascii', errors='replace')
            objects.append({'name': name, 'hash': hash_id})
    return objects
