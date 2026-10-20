import struct
import numpy as np
from typing import Dict, List, Optional, Tuple


def decode_mesh_block(block: bytes) -> Optional[Dict]:
    if len(block) < 40:
        return None

    r = Reader(block)

    first_long = r.u32()

    has_version = (first_long == 0xC0DE2002)

    if has_version:
        version = r.u32()
        num_vertices = r.u32()
        has_mrm = r.u32()
        if version >= 3:
            num_mrm_levels = r.u32()
    else:
        version = 0
        num_vertices = first_long
        has_mrm = 0

    if num_vertices == 0 or num_vertices > 500000:
        return None

    point_colors = r.u32()
    num_uvs = r.u32()
    num_elements = r.u32()
    editor_flags = r.u32()
    skin_flags = r.u32()

    if num_elements == 0 or num_elements > 10000:
        return None
    if num_uvs > 500000:
        return None

    verts = np.zeros((num_vertices, 3), dtype=np.float32)
    for i in range(num_vertices):
        verts[i, 0] = r.f32()
        verts[i, 1] = r.f32()
        verts[i, 2] = r.f32()

    if has_mrm:
        num_mrm_points = r.u32()
        if num_mrm_points > 0 and num_mrm_points <= 500000:
            r.skip(num_mrm_points * 2)

    normals = None
    if point_colors != 0:
        normals = np.zeros((num_vertices, 3), dtype=np.float32)
        for i in range(num_vertices):
            normals[i, 0] = r.f32()
            normals[i, 1] = r.f32()
            normals[i, 2] = r.f32()

    uvs = np.zeros((num_uvs, 2), dtype=np.float32)
    for i in range(num_uvs):
        uvs[i, 0] = r.f32()
        uvs[i, 1] = r.f32()

    faces = []
    uv_indices = []
    material_ids = []

    for _ in range(num_elements):
        face_count = r.i32()
        mat_id = r.i32()

        if face_count <= 0 or face_count > 500000:
            continue

        r.u32()
        r.u32()
        r.u32()
        r.u32()
        r.u32()
        r.u32()
        r.u32()

        for _ in range(face_count):
            v1 = r.i16()
            v2 = r.i16()
            v3 = r.i16()
            uv1 = r.i16()
            uv2 = r.i16()
            uv3 = r.i16()
            r.u32()
            r.u32()

            if v1 < num_vertices and v2 < num_vertices and v3 < num_vertices:
                faces.append((v1, v2, v3))
                uv_indices.append((uv1, uv2, uv3))
                material_ids.append(mat_id)

    if len(faces) == 0:
        return None

    return {
        'vertices': verts,
        'normals': normals,
        'uvs': uvs,
        'faces': np.array(faces, dtype=np.int32),
        'uv_indices': np.array(uv_indices, dtype=np.int32),
        'material_ids': material_ids,
    }


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

    def i16(self):
        v = struct.unpack_from('<h', self.data, self.pos)[0]
        self.pos += 2
        return v

    def f32(self):
        v = struct.unpack_from('<f', self.data, self.pos)[0]
        self.pos += 4
        return v

    def skip(self, n):
        self.pos += n
