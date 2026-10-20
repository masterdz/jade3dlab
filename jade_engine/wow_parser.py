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


def _read_u32_from_block(block: bytes, pos: int) -> int:
    return struct.unpack_from('<I', block, pos)[0]


def _skip_pos(pos: int, n: int) -> int:
    return pos + n


def parse_mesh_from_block(block: bytes) -> Optional[Mesh]:
    """Parse a mesh from a block that starts after the 99C0FFEE separator.
    The block layout after separator is:
    - u32: header/marker (e.g., 0x1B003A16)
    - u32: ".wow" magic (0x776F772E)
    - 1 byte: separator (0x0A)
    - null-terminated ASCII filename
    - mesh vertex data follows
    """
    length = len(block)
    pos = 0

    # Step 1: Read header u32
    header = _read_u32_from_block(block, pos)
    pos += 4
    print(f'Header: 0x{header:08X}')

    # Step 2: Read .wow magic
    wow_magic = _read_u32_from_block(block, pos)
    print(f'.wow magic: 0x{wow_magic:08X}')
    pos += 4

    # Step 3: Skip 1 separator byte (0x0A)
    if pos + 1 <= length:
        sep = block[pos]
        print(f'Separator byte: 0x{sep:02X}')
        pos += 1

    # Step 4: Read null-terminated filename starting at pos
    # Scan for null terminator
    fname_start = pos
    while pos < length and block[pos] != 0:
        pos += 1
    fname_end = pos
    if fname_start < fname_end:
        filename = block[fname_start:fname_end].decode('ascii', errors='replace')
    else:
        filename = ""

    print(f'Filename: "{filename}" at pos {fname_start}-{fname_end}')

    # Create mesh
    mesh = Mesh(hash_id=filename if filename else "unknown")

    # Step 5: Read flags u32 (next 4 bytes after filename null terminator)
    # pos is currently at the null terminator, advance past it
    pos += 1
    if pos + 4 <= length:
        flags = _read_u32_from_block(block, pos)
        pos += 4
    else:
        flags = 0

    # Step 6: Read has_second flag
    has_second = False
    if pos + 4 <= length:
        has_second = _read_u32_from_block(block, pos) != 0
        pos += 4

    # Step 7: Read num_vertices
    if pos + 4 <= length:
        num_vertices = _read_u32_from_block(block, pos)
        pos += 4
    else:
        num_vertices = 0

    # Step 8: Read num_unknown
    num_unknown = 0
    if pos + 4 <= length:
        num_unknown = _read_u32_from_block(block, pos)
        pos += 4

    # Step 9: Read has_unknown
    has_unknown = False
    if pos + 4 <= length:
        has_unknown = _read_u32_from_block(block, pos) != 0
        pos += 4

    # Step 10: Read num_uvs
    num_uvs = 0
    if pos + 4 <= length:
        num_uvs = _read_u32_from_block(block, pos)
        pos += 4

    # Step 11: Read num_materials
    num_materials = 0
    if pos + 4 <= length:
        num_materials = _read_u32_from_block(block, pos)
        pos += 4

    # Step 12: Read vertex positions (3 floats each = 12 bytes)
    vert_data = []
    for _ in range(num_vertices):
        if pos + 12 <= length:
            vx = struct.unpack_from('<f', block, pos)[0]
            vy = struct.unpack_from('<f', block, pos + 4)[0]
            vz = struct.unpack_from('<f', block, pos + 8)[0]
            vert_data.append((vx, vy, vz))
            pos += 12
        else:
            break

    mesh.vertices = np.array(vert_data, dtype=np.float32) if vert_data else np.zeros((num_vertices, 3), dtype=np.float32)

    # Step 13: Read normals (if indicated by flags)
    has_normals = bool(flags & 0x8) or bool(flags & 0x10)
    normals = []
    if has_normals and num_vertices > 0:
        for _ in range(num_vertices):
            if pos + 12 <= length:
                nx = struct.unpack_from('<f', block, pos)[0]
                ny = struct.unpack_from('<f', block, pos + 4)[0]
                nz = struct.unpack_from('<f', block, pos + 8)[0]
                normals.append((nx, ny, nz))
                pos += 12
            else:
                break
        mesh.normals = np.array(normals, dtype=np.float32)
    else:
        # Skip normal data if present
        expected_skip = num_vertices * 12
        if pos + expected_skip <= length:
            pos += expected_skip
        mesh.normals = np.zeros((num_vertices, 3), dtype=np.float32)

    # Step 14: Skip unknown data if present
    if has_unknown and num_unknown > 0:
        skip_size = num_unknown * 4
        if pos + skip_size <= length:
            pos += skip_size

    # Step 15: Read UVs
    uv_data = []
    for _ in range(num_uvs):
        if pos + 8 <= length:
            u = struct.unpack_from('<f', block, pos)[0]
            v = struct.unpack_from('<f', block, pos + 4)[0]
            uv_data.append((u, v))
            pos += 8
        else:
            break
    mesh.uvs = np.array(uv_data, dtype=np.float32).reshape(-1, 2) if uv_data else np.zeros((num_uvs, 2), dtype=np.float32)

    # Step 16: Read materials and faces
    material_ids = []
    faces = []
    uv_indices = []
    num_faces = 0

    for _ in range(num_materials):
        if pos + 8 > length:
            break
        num_curr = struct.unpack_from('<i', block, pos)[0]
        pos += 4
        mat_id = struct.unpack_from('<i', block, pos)[0]
        pos += 4
        material_ids.append((mat_id, num_curr))
        num_faces += num_curr

    # Step 17: Read face indices
    for _ in range(num_faces):
        if pos + 6 > length:
            break
        v1 = struct.unpack_from('<h', block, pos)[0]
        v2 = struct.unpack_from('<h', block, pos + 2)[0]
        v3 = struct.unpack_from('<h', block, pos + 4)[0]
        faces.append((v1, v2, v3))
        pos += 6

        # Read UV indices if available
        if num_uvs > 0 and pos + 6 <= length:
            u1 = struct.unpack_from('<h', block, pos)[0]
            u2 = struct.unpack_from('<h', block, pos + 2)[0]
            u3 = struct.unpack_from('<h', block, pos + 4)[0]
            uv_indices.append((u1, u2, u3))
            pos += 6
        else:
            # Skip 6 bytes (3 UV indices)
            pos += 6

    mesh.faces = np.array(faces, dtype=np.int32).reshape(-1, 3) if faces else np.zeros((num_faces, 3), dtype=np.int32)
    mesh.uv_indices = np.array(uv_indices, dtype=np.int32).reshape(-1, 3) if uv_indices else np.zeros((num_faces, 3), dtype=np.int32)
    mesh.material_ids = material_ids

    # Step 18: Handle second mesh if present
    if has_second:
        # Skip remaining data in block
        if pos < length:
            pos = length

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

    # First, split on 99C0FFEE markers
    blocks = data.split(b'\x99\xC0\xFF\xEE')

    seen_textures = set()
    extra_hashes = {}

    for block in blocks:
        if len(block) < 8:
            continue

        # Parse mesh from block (starting after 99C0FFEE)
        # The block data starts immediately, first u32 is header
        if len(block) < 12:
            continue

        mesh = parse_mesh_from_block(block)
        if mesh and mesh.hash_id and mesh.hash_id != "unknown" and len(mesh.vertices) > 0:
            level.meshes[mesh.hash_id] = mesh

        # Also try the old-style parsing for compatibility
        reader = BinaryReader(block)

        # Read hash_id (u32)
        try:
            hash_id = reader.read_int()
        except Exception:
            continue

        # Read type_id (u32)
        try:
            type_id = reader.read_int()
        except Exception:
            continue

        if hash_id == 0x000000B0:
            continue
        elif hash_id == 0x0FF7C0DE:
            break

        # Check for ".wow" type (type_id = 0x776F772E)
        if type_id == 0x776F772E:
            # Already parsed above via parse_mesh_from_block
            continue

        # Check for ".gao" type (type_id = 0x6F61672E)
        elif type_id == 0x6F61672E:
            obj = parse_gao_block(reader, f'{hash_id:08X}')
            if obj:
                level.game_objects.append(obj)

        elif type_id == 0x00000001:
            # Standard mesh block - try old parser
            # Reset reader position and try
            reader.pos = 0
            mesh = parse_mesh_block(reader, f'{hash_id:08X}')
            if mesh:
                level.meshes[hash_id] = mesh

        elif type_id == 0x00000004:
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

        elif type_id == 0x00000005:
            mat = parse_material_block(reader, f'{hash_id:08X}')
            if mat:
                level.materials[hash_id] = mat

        elif type_id == 0x0D0024F1:
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