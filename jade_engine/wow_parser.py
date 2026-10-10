import struct
from typing import Dict, List, Optional, Tuple
from io import BytesIO
import numpy as np
from .mesh import (
    Mesh, GameObject, Material, Texture, LevelData, BinaryReader
)


def get_group(name: str) -> str:
    name_upper = name.upper()
    if "TEC" in name_upper:
        return "Trigger"
    elif "INI_POS" in name_upper:
        return "Set Position"
    elif "SND" in name_upper or "SFX" in name_upper:
        return "Sound"
    elif "PORTAL" in name_upper:
        return "Portal"
    elif "SECTOR" in name_upper:
        return "Sector"
    elif "CAM" in name_upper:
        return "Camera"
    elif "TUT" in name_upper:
        return "Tutorial"
    elif any(x in name_upper for x in ("NET", "FRH", "NAV", "GUY")):
        return "AI"
    elif any(x in name_upper for x in ("LUM", "LAMPE", "LANTERNE")):
        return "Light"
    elif "OBJ" in name_upper:
        return "Object"
    elif any(x in name_upper for x in ("GFX", "PARTICULE", "GP11", "FOG")):
        return "Graphics"
    elif "TRIGGER" in name_upper:
        return "Trigger"
    return "Other"


def parse_mesh_block(reader: BinaryReader, hash_id: str) -> Optional[Mesh]:
    version = reader.read_hex()

    if version not in ("00000007", "00000008"):
        return None

    mesh = Mesh(hash_id=hash_id)

    flags = reader.read_int()
    has_second_mesh = reader.read_int() != 0

    num_vertices = reader.read_int()
    num_unknown = reader.read_int()
    has_unknown_data = reader.read_int() != 0
    num_uvs = reader.read_int()
    num_materials = reader.read_int()

    if flags & 0x8 or flags & 0x10:
        reader.read_float()
        has_normals = reader.read_short() != 0
        num4 = reader.read_short()
        for _ in range(num4):
            reader.read_short()
            num_floats = reader.read_short()
            reader.read_float(16)
            reader.read_hex()
            reader.read_float(num_floats)
        if num4 > 0:
            has_normals = (reader.read_int() != 0) or has_normals
    else:
        reader.read_int()
        has_normals = reader.read_int() != 0

    vert_data = reader.read_float(3 * num_vertices)
    mesh.vertices = np.array(vert_data, dtype=np.float32).reshape(-1, 3)

    if has_unknown_data:
        reader.read_float(num_unknown)

    if has_normals:
        normal_data = reader.read_float(3 * num_vertices)
        mesh.normals = np.array(normal_data, dtype=np.float32).reshape(-1, 3)

    uv_data = reader.read_float(2 * num_uvs)
    mesh.uvs = np.array(uv_data, dtype=np.float32).reshape(-1, 2)

    material_ids = []
    num_faces = 0
    for _ in range(num_materials):
        num_curr = reader.read_int()
        num_faces += num_curr
        mat_id = reader.read_int()
        material_ids.append((mat_id, num_curr))
    mesh.material_ids = material_ids

    faces = []
    uv_indices = []
    for _ in range(num_faces):
        face = reader.read_short(3)
        faces.append(face)
        uv_idx = reader.read_short(3)
        uv_indices.append(uv_idx)
        reader.read_short(2)

    mesh.faces = np.array(faces, dtype=np.int32).reshape(-1, 3)
    mesh.uv_indices = np.array(uv_indices, dtype=np.int32).reshape(-1, 3)

    reader.read_int()
    unknown = reader.read_int()
    while unknown != 0:
        amount = reader.read_int()
        for _ in range(amount):
            size = reader.read_short()
            reader.read_short()
            reader.read_short(2 * size)
        unknown = reader.read_int()
    reader.read_int()

    if has_second_mesh:
        num_faces2 = 0
        for _ in range(num_materials):
            num_curr = reader.read_int()
            num_faces2 += num_curr
            reader.read_int()

        size = reader.read_int()
        reader.read_int()
        num_vertices2 = reader.read_int()
        block_length = reader.read_int()

        for _ in range(num_vertices2):
            reader.read_float(3)
            if block_length >= 32:
                reader.read_float(3)
            if block_length >= 44:
                reader.read_float(3)
            if block_length >= 52:
                reader.read_short(2)
                reader.read_int()
                reader.read_float(3)
            if block_length >= 64:
                reader.read_int()
                reader.read_float(2)

        size = reader.read_int()
        face_data = reader.read_short(size // 2)
        reader.read_int()

    return mesh


def parse_gao_block(reader: BinaryReader, hash_id: str) -> Optional[GameObject]:
    reader.read_int()
    reader.read_int()
    flags = reader.read_int()
    reader.read_int()
    name = reader.read(60).split(b'\x00')[0].decode('ascii', errors='replace').strip()
    reader.read_int()
    reader.read_short()
    reader.read_float()

    rot_x = reader.read_float(3)
    scale_x = reader.read_float()
    rot_y = reader.read_float(3)
    scale_y = reader.read_float()
    rot_z = reader.read_float(3)
    scale_z = reader.read_float()

    rot_matrix = np.array([rot_x, rot_y, rot_z], dtype=np.float32).T
    if scale_x == 0:
        scale_x = 1
    if scale_y == 0:
        scale_y = 1
    if scale_z == 0:
        scale_z = 1
    scale = (scale_x, scale_y, scale_z)

    center = reader.read_float(3)

    if flags & 0x10000:
        reader.read_hex()
    else:
        reader.read_float()

    reader.read_int()

    if flags & 0x80000:
        reader.read_float(6)

    bounding_box = reader.read_float(6)

    mesh_hash = ""
    material_pack_hash = ""
    extra_hash = ""

    if flags & 0x4000:
        mesh_hash = reader.read_hex()
        material_pack_hash = reader.read_hex()
        reader.read_byte(10)
        amount = reader.read_int()
        reader.read_int(amount)
        reader.read_int()
        reader.read_hex()
        reader.read_hex()
        reader.read_hex()
    else:
        reader.pos = reader.length - 8
        extra_hash = reader.read_hex()

    return GameObject(
        name=name,
        hash_id=hash_id,
        center=tuple(center),
        rotation=rot_matrix,
        scale=scale,
        bounding_box=tuple(bounding_box),
        mesh_hash=mesh_hash,
        material_pack_hash=material_pack_hash,
        extra_hash=extra_hash,
        group=get_group(name),
        flags=flags,
    )


def parse_material_block(reader: BinaryReader, hash_id: str) -> Optional[Material]:
    version = reader.read_int()

    if version < 3 or version > 9:
        return None

    reader.read_hex()
    if version >= 8:
        reader.read_hex()
        reader.read_hex()
    reader.read_int()
    reader.read_hex()
    reader.read_int()

    if reader.pos + 4 == reader.length:
        return Material(hash_id=hash_id, version=version)

    reader.read_int()
    if version >= 8:
        reader.read_short()
    reader.read_int()
    specular = reader.read_float()
    diffuse = reader.read_float()
    reader.read_int()
    if version == 9:
        reader.read_byte(9)
        reader.read_hex()

    texture_hash = reader.read_hex()

    return Material(
        hash_id=hash_id,
        texture_hash=texture_hash,
        specular_intensity=specular,
        diffuse_intensity=diffuse,
        version=version,
    )


def parse_texture_block(reader: BinaryReader, hash_id: str, is_second: bool) -> Optional[Texture]:
    if not is_second:
        return None

    texture_type = reader.read_int()

    if texture_type == 286331153:
        return None

    uses_palette = bool(texture_type & 0x40000000 and texture_type & 0x1)

    width = reader.read_short()
    height = reader.read_short()
    reader.read_hex()
    reader.read_hex()
    reader.read_hex()
    reader.read_hex()
    reader.read_hex()

    compression = 0
    num_mipmaps = 0

    if texture_type & 0x80000:
        bool_val = reader.read_int() != 1
        compression = reader.read_int()
        assert reader.read_int() == width
        assert reader.read_int() == height
        num_mipmaps = reader.read_int()
        if bool_val:
            reader.read_int()
    elif texture_type & 0x40000:
        compression = 7
        num_mipmaps = 0
    else:
        reader.read_short()
        compression = reader.read_short()
        reader.read_int()
        reader.read_int()
        reader.read_short()
        reader.read_short()
        num_mipmaps = reader.read_short()

    data = reader.read(reader.length - reader.pos - 4)

    return Texture(
        hash_id=hash_id,
        width=width,
        height=height,
        compression=compression,
        num_mipmaps=num_mipmaps,
        data=data,
        uses_palette=uses_palette,
    )


def parse_wow(data: bytes) -> LevelData:
    level = LevelData()

    blocks = data.split(b'\x99\xC0\xFF\xEE')

    seen_textures = set()
    extra_hashes = {}

    for block in blocks:
        if len(block) < 8:
            continue

        reader = BinaryReader(block)

        hash_id = reader.read_hex()
        type_id = reader.read_hex()

        if hash_id == "000000B0":
            continue
        elif hash_id == "0FF7C0DE":
            break

        if type_id == "776F772E":
            continue

        elif type_id == "6F61672E":
            obj = parse_gao_block(reader, hash_id)
            if obj:
                level.game_objects.append(obj)

        elif type_id == "00000001":
            mesh = parse_mesh_block(reader, hash_id)
            if mesh:
                level.meshes[hash_id] = mesh

        elif type_id == "00000004":
            if reader.end_of_stream():
                continue
            if reader.read_int() != 0:
                continue
            num_materials = reader.read_int()
            if num_materials > 1000:
                continue
            elif num_materials == 0:
                while reader.pos + 4 != reader.length:
                    reader.read_int()
                continue
            mat_hashes = []
            for _ in range(num_materials):
                mat_hashes.append(reader.read_hex())
            level.material_packs[hash_id] = mat_hashes
            reader.read_int()

        elif type_id == "00000005":
            mat = parse_material_block(reader, hash_id)
            if mat:
                level.materials[hash_id] = mat

        elif type_id == "0D0024F1":
            extra_hashes[hash_id] = reader.read_hex()
            reader.read_int()

        elif type_id == hash_id:
            if reader.read_hex() != "FFFFFFFF":
                reader.seek(-8, 1)
                color_data = reader.read(4 * 256)
                palette = []
                for i in range(0, len(color_data), 4):
                    palette.append(tuple(color_data[i:i+4]))
                if hash_id not in level.textures:
                    level.textures[hash_id] = Texture(hash_id=hash_id, palette=palette)
            else:
                is_second = hash_id in seen_textures
                if not is_second:
                    seen_textures.add(hash_id)
                tex = parse_texture_block(reader, hash_id, is_second)
                if tex:
                    level.textures[hash_id] = tex

    return level


def parse_wol(data: bytes) -> List[str]:
    wow_files = []
    buf = BytesIO(data)
    buf.read(12)

    content = data[12:]
    reader = BinaryReader(content)

    while not reader.end_of_stream():
        wow_hash = reader.read_hex()
        ext = reader.read_string(4)
        wow_files.append((wow_hash, ext))

    return wow_files
