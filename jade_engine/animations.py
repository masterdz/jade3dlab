"""Jade Engine TRL/EVE animation track parser and keyframe sampling."""
from __future__ import annotations

import bisect
from dataclasses import dataclass
import math
import struct
from typing import Any, Dict, List, Optional, Tuple

from .resources import parse_pop_file_entries


@dataclass(frozen=True)
class AnimationKey:
    frame: int
    translation: Optional[Tuple[float, float, float]] = None
    rotation: Optional[Tuple[float, float, float, float]] = None
    no_interpolation: bool = False


@dataclass(frozen=True)
class AnimationTrack:
    gizmo: int
    keys: Tuple[AnimationKey, ...]


@dataclass
class AnimationClip:
    key: int
    tracks: Tuple[AnimationTrack, ...]
    frames: int
    entry_index: int
    name: str = ""
    character_group: str = ""


def _read(fmt: str, data: bytes, pos: int):
    size = struct.calcsize(fmt)
    if pos + size > len(data):
        raise ValueError("Truncated TRL track")
    values = struct.unpack_from(fmt, data, pos)
    return (values[0] if len(values) == 1 else values), pos + size


def _packed_quaternion(word: int) -> Tuple[float, float, float, float]:
    """Retail Jade 0x4010: three 10-bit components and omitted axis calculation."""
    omitted = word >> 30
    scale = 1.0 / (511.0 * math.sqrt(2.0))
    components = [(((word >> (10 * i)) & 0x3FF) - 512) * scale for i in range(3)]
    missing = math.sqrt(max(0.0, 1.0 - sum(value * value for value in components)))
    components.insert(omitted, missing)
    length = math.sqrt(sum(value * value for value in components))
    return tuple(value / length for value in components)


def _parse_trl(data: bytes, key: int, entry_index: int) -> AnimationClip:
    count, pos = _read("<H", data, 0)
    _flags, pos = _read("<H", data, pos)
    if not 0 < count <= 256:
        raise ValueError("Invalid TRL track count")
    tracks = []
    total_frames = 0
    for _ in range(count):
        flags, pos = _read("<H", data, pos)
        gizmo, pos = _read("<H", data, pos)
        data_length, pos = _read("<I", data, pos)
        if not flags & 0x8000 or data_length > len(data):
            raise ValueError("Unsupported TRL track")
        if not flags & 0x3F00:
            _track_type, pos = _read("<I", data, pos)
        events, pos = _read("<I", data, pos)
        if events > 100_000:
            raise ValueError("Invalid TRL event count")
        keys = []
        frame = 0
        first_flags = first_size = first_type = None
        for event_index in range(events):
            span, pos = _read("<B" if flags & 0x0200 else "<H", data, pos)
            duration = span & 0x7FFF
            event_flags, pos = _read("<H", data, pos) if event_index == 0 or not flags & 0x0800 else (first_flags & ~0x0100, pos)
            if first_flags is None:
                first_flags = event_flags
            if event_flags & 0x07C0 != 0x0080 or event_flags & 0x0020:
                raise ValueError("Unsupported TRL event type")
            size, pos = _read("<H", data, pos) if event_index == 0 or not flags & 0x2000 else (first_size, pos)
            kind, pos = _read("<H", data, pos) if event_index == 0 or not flags & 0x1000 else (first_type, pos)
            if first_size is None:
                first_size, first_type = size, kind
            if size < 4 or size > 4096:
                raise ValueError("Invalid interpolation key size")
            start = pos
            translation = rotation = None
            available = size - 4
            if kind & 3 and available >= 12:
                translation, pos = _read("<3f", data, pos)
                for _ in range((kind & 3) - 1):
                    _, pos = _read("<3f", data, pos)
            elif kind == 0x4010 and available == 4:
                word, pos = _read("<I", data, pos)
                rotation = _packed_quaternion(word)
            elif kind == 0x1010 and available == 8:
                values, pos = _read("<4h", data, pos)
                rot = tuple(value / 32767.0 for value in values)
                length = math.sqrt(sum(value * value for value in rot))
                rotation = tuple(value / length for value in rot) if length else (0, 0, 0, 1)
            elif kind & 0x10 and available >= (6 if kind & 0x80 else 16):
                if kind & 0x80:
                    xyz, pos = _read("<3h", data, pos)
                    x, y, z = (v / 32767.0 for v in xyz)
                    rotation = (x, y, z, math.sqrt(max(0.0, 1.0 - x * x - y * y - z * z)))
                else:
                    rotation, pos = _read("<4f", data, pos)
            if kind & 0x40:
                next_bytes = (12 if kind & 3 else 0) + (16 if kind & 0x10 else 0)
                pos += next_bytes
            if kind & 0x08:
                pos += 4
            expected = size - 4
            pos = start + expected
            if pos > len(data):
                raise ValueError("Truncated TRL key")
            if translation is not None or rotation is not None:
                if not all(math.isfinite(v) for v in (translation or ()) + (rotation or ())):
                    raise ValueError("Nonfinite TRL key")
                keys.append(AnimationKey(frame, translation, rotation, bool(event_flags & 0x0800)))
            frame += duration
        if keys:
            tracks.append(AnimationTrack(gizmo, tuple(keys)))
            total_frames = max(total_frames, frame)
    if not tracks:
        raise ValueError("TRL contains no playable transform tracks")
    return AnimationClip(key, tuple(tracks), max(1, total_frames), entry_index, f"Clip_0x{key:08X}")


def scan_animations(data: bytes) -> List[AnimationClip]:
    """Scan all Jade TRL/EVE animation clips in FileEntry stream."""
    clips: List[AnimationClip] = []
    for entry in parse_pop_file_entries(data):
        kind = entry.data_type or 0
        if kind >> 16 != 2 or kind & 0xFF in (0x24, 0x30):
            continue
        payload = data[entry.data_offset:entry.data_offset + entry.size]
        try:
            clip = _parse_trl(payload, entry.key, entry.index)
            clips.append(clip)
        except (ValueError, struct.error):
            continue
    return clips


def sample_track_field(keys: Tuple[AnimationKey, ...], frame: float, field: str):
    """Interpolate keyframes at given frame timestamp."""
    usable = [key for key in keys if getattr(key, field) is not None]
    if not usable:
        return None
    frames = [key.frame for key in usable]
    index = bisect.bisect_right(frames, frame)
    if index == 0:
        return getattr(usable[0], field)
    if index == len(usable):
        return getattr(usable[-1], field)
    left, right = usable[index - 1], usable[index]
    if left.no_interpolation:
        return getattr(left, field)
    t = (frame - left.frame) / max(1.0, float(right.frame - left.frame))
    a, b = getattr(left, field), getattr(right, field)
    if field == "rotation":
        if sum(x * y for x, y in zip(a, b)) < 0:
            b = tuple(-x for x in b)
    result = tuple(x + (y - x) * t for x, y in zip(a, b))
    if field == "rotation":
        length = math.sqrt(sum(x * x for x in result))
        return tuple(x / length for x in result) if length else (0.0, 0.0, 0.0, 1.0)
    return result


def inverse_matrix(matrix: Tuple[float, ...] | List[float]) -> List[float]:
    """Invert a 4x4 column-major affine transform matrix (Jade engine native convention).

    Column-major layout (Jade MATH_tdst_Matrix): M[col, row] = matrix[col*4+row].
    Indices: 0-2=I-column, 4-6=J-column, 8-10=K-column, 12-14=translation T.
    """
    rows = [[float(matrix[column * 4 + row]) for column in range(4)] +
            [float(row == column) for column in range(4)] for row in range(4)]
    for column in range(4):
        pivot = max(range(column, 4), key=lambda row: abs(rows[row][column]))
        if abs(rows[pivot][column]) < 1e-12:
            raise ValueError("A character bind matrix is singular.")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        factor = rows[column][column]
        rows[column] = [value / factor for value in rows[column]]
        for row in range(4):
            if row != column:
                factor = rows[row][column]
                rows[row] = [a - factor * b for a, b in zip(rows[row], rows[column])]
    return [rows[row][column + 4] for column in range(4) for row in range(4)]


def mul_matrix(a: Tuple[float, ...] | List[float], b: Tuple[float, ...] | List[float]) -> Tuple[float, ...]:
    """Multiply two 4x4 row-major transformation matrices (official Jade MATH_MulMatrixMatrix)."""
    return (
        a[0] * b[0] + a[1] * b[4] + a[2] * b[8],
        a[0] * b[1] + a[1] * b[5] + a[2] * b[9],
        a[0] * b[2] + a[1] * b[6] + a[2] * b[10],
        0.0,
        a[4] * b[0] + a[5] * b[4] + a[6] * b[8],
        a[4] * b[1] + a[5] * b[5] + a[6] * b[9],
        a[4] * b[2] + a[5] * b[6] + a[6] * b[10],
        0.0,
        a[8] * b[0] + a[9] * b[4] + a[10] * b[8],
        a[8] * b[1] + a[9] * b[5] + a[10] * b[9],
        a[8] * b[2] + a[9] * b[6] + a[10] * b[10],
        0.0,
        a[12] * b[0] + a[13] * b[4] + a[14] * b[8] + b[12],
        a[12] * b[1] + a[13] * b[5] + a[14] * b[9] + b[13],
        a[12] * b[2] + a[13] * b[6] + a[14] * b[10] + b[14],
        1.0,
    )


def _compose_rotation_3x3(anim_rot: Tuple[float, ...], rest_local: List[float]) -> None:
    """Compose animation rotation (3x3) with rest-pose local rotation in-place.

    TRL animation quaternions are relative to the bone's rest-pose local orientation.
    The correct formula is: animated_rotation = anim_rotation * rest_rotation.
    This modifies the first 12 elements (3 columns x 4 rows) of *rest_local* in-place,
    keeping elements [3], [7], [11] (row 3 of each column) at 0.
    """
    # Extract rest 3x3 columns from column-major layout
    r0, r1, r2, r3 = rest_local[0], rest_local[1], rest_local[2], rest_local[3]
    r4, r5, r6, r7 = rest_local[4], rest_local[5], rest_local[6], rest_local[7]
    r8, r9, r10, r11 = rest_local[8], rest_local[9], rest_local[10], rest_local[11]

    # anim_rot 3x3
    a0, a1, a2 = anim_rot[0], anim_rot[1], anim_rot[2]
    a4, a5, a6 = anim_rot[4], anim_rot[5], anim_rot[6]
    a8, a9, a10 = anim_rot[8], anim_rot[9], anim_rot[10]

    # Result = anim * rest (column-major 3x3)
    rest_local[0] = a0 * r0 + a4 * r1 + a8 * r2
    rest_local[1] = a1 * r0 + a5 * r1 + a9 * r2
    rest_local[2] = a2 * r0 + a6 * r1 + a10 * r2
    # rest_local[3] stays 0
    rest_local[4] = a0 * r4 + a4 * r5 + a8 * r6
    rest_local[5] = a1 * r4 + a5 * r5 + a9 * r6
    rest_local[6] = a2 * r4 + a6 * r5 + a10 * r6
    # rest_local[7] stays 0
    rest_local[8] = a0 * r8 + a4 * r9 + a8 * r10
    rest_local[9] = a1 * r8 + a5 * r9 + a9 * r10
    rest_local[10] = a2 * r8 + a6 * r9 + a10 * r10
    # rest_local[11] stays 0


def transform_point(matrix: Tuple[float, ...] | List[float], point: Tuple[float, float, float]) -> Tuple[float, float, float]:
    """Transform a 3D point by a 4x4 column-major matrix (Jade engine native convention).

    Column-major layout: M[col, row] = matrix[col*4+row]. Translation at indices 12,13,14.
    """
    return tuple(sum(matrix[column * 4 + row] * point[column] for column in range(3)) + matrix[12 + row]
                 for row in range(3))


def quat_to_matrix(q: Tuple[float, float, float, float]) -> Tuple[float, ...]:
    """Convert quaternion (x, y, z, w) to a 4x4 column-major rotation matrix.

    Matches Jade MATH_ConvertQuaternionToMatrix exactly (MATHmatrixAdvanced.c:528).
    Column-major: indices 0,1,2=I-column; 4,5,6=J-column; 8,9,10=K-column; 12-14=0.
    """
    x, y, z, w = q
    return (
        1.0 - 2.0 * (y * y + z * z), 2.0 * (x * y + z * w), 2.0 * (x * z - y * w), 0.0,
        2.0 * (x * y - z * w), 1.0 - 2.0 * (x * x + z * z), 2.0 * (y * z + x * w), 0.0,
        2.0 * (x * z + y * w), 2.0 * (y * z - x * w), 1.0 - 2.0 * (x * x + y * y), 0.0,
        0.0, 0.0, 0.0, 1.0,
    )


def build_skin_rest(mesh) -> Dict[int, Tuple[Tuple[float, ...], Tuple[float, float, float], List[Tuple[int, float, Tuple[float, float, float]]], List[float]]]:
    """Extract rest pose, bind matrices, and vertex weights for a skinned mesh."""
    from .jade_mesh import decode_weight
    rest = {}
    for bone in mesh.skin_bones or []:
        try:
            world = inverse_matrix(bone.matrix)
        except ValueError:
            continue
        prepared = []
        ibm = bone.matrix
        for vertex_index, word in bone.weights:
            if not 0 <= vertex_index < len(mesh.vertices):
                continue
            weight = decode_weight(word)
            if not weight:
                continue
            vertex = mesh.vertices[vertex_index]
            bind_local = tuple(sum(ibm[column * 4 + row] * vertex[column] for column in range(3)) + ibm[12 + row]
                               for row in range(3))
            prepared.append((vertex_index, weight, bind_local))
        rest[bone.index] = (tuple(world), tuple(world[12:15]), prepared, list(ibm))
    return rest


# Master Jade Biped Parent Hierarchy (Gizmo 0 = Pelvis root)
MASTER_BIPED_PARENTS: Dict[int, int] = {
    1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 3, 7: 6, 8: 7, 9: 8,
    10: 9, 11: 10, 12: 9, 13: 12, 14: 9, 15: 14,
    16: 3, 17: 16, 18: 17, 19: 18, 20: 19, 21: 20, 22: 19, 23: 22, 24: 19, 25: 24,
    26: 0, 27: 26, 28: 27, 29: 28,
    30: 0, 31: 30, 32: 31, 33: 32,
}

# Farah SkinBone index (0..35) to TRL Animation Gizmo index (1..35)
FARAH_GIZMO_MAP: List[int] = [
    1,   # 0: Pelvis -> Gizmo 1
    2,   # 1: Spine -> Gizmo 2
    3,   # 2: Spine1 -> Gizmo 3
    4,   # 3: Neck -> Gizmo 4
    5,   # 4: Head -> Gizmo 5
    8,   # 5: L Clavicle -> Gizmo 8
    9,   # 6: L UpperArm -> Gizmo 9
    10,  # 7: L Forearm -> Gizmo 10
    11,  # 8: L Hand -> Gizmo 11
    12,  # 9: L Finger0 -> Gizmo 12
    13,  # 10: L Finger01 -> Gizmo 13
    14,  # 11: L Finger1 -> Gizmo 14
    15,  # 12: L Finger11 -> Gizmo 15
    18,  # 13: R Clavicle -> Gizmo 18
    19,  # 14: R UpperArm -> Gizmo 19
    20,  # 15: R Forearm -> Gizmo 20
    21,  # 16: R Hand -> Gizmo 21
    22,  # 17: R Finger0 -> Gizmo 22
    23,  # 18: R Finger01 -> Gizmo 23
    24,  # 19: R Finger1 -> Gizmo 24
    25,  # 20: R Finger11 -> Gizmo 25
    26,  # 21: L Thigh -> Gizmo 26
    27,  # 22: L Calf -> Gizmo 27
    28,  # 23: L Foot -> Gizmo 28
    29,  # 24: L Toe0 -> Gizmo 29
    30,  # 25: R Thigh -> Gizmo 30
    31,  # 26: R Calf -> Gizmo 31
    32,  # 27: R Foot -> Gizmo 32
    33,  # 28: R Toe0 -> Gizmo 33
    3,   # 29: Quiver root -> follows Spine1 (Gizmo 3)
    6,   # 30: Ponytail1 -> Gizmo 6
    26,  # 31: Skirt BackLeft -> follows L Thigh (Gizmo 26)
    30,  # 32: Skirt BackRight -> follows R Thigh (Gizmo 30)
    26,  # 33: Skirt FrontLeft -> follows L Thigh (Gizmo 26)
    30,  # 34: Skirt FrontRight -> follows R Thigh (Gizmo 30)
    35,  # 35: Breast -> Gizmo 35
]

FARAH_GIZMO_PARENTS: Dict[int, int] = {
    1: 0,   # Pelvis -> Actor Root 0
    2: 1,   # Spine -> Pelvis
    3: 2,   # Spine1 -> Spine
    4: 3,   # Neck -> Spine1
    5: 4,   # Head -> Neck
    6: 5,   # Ponytail1 -> Head
    7: 6,   # Ponytail11 -> Ponytail1
    8: 3,   # L Clavicle -> Spine1
    9: 8,   # L UpperArm -> L Clavicle
    10: 9,  # L Forearm -> L UpperArm
    11: 10, # L Hand -> L Forearm
    12: 11, # L Finger0 -> L Hand
    13: 12, # L Finger01 -> L Finger0
    14: 11, # L Finger1 -> L Hand
    15: 14, # L Finger11 -> L Finger1
    16: 11, # Bow -> L Hand
    17: 16, # Bow string -> Bow
    18: 3,  # R Clavicle -> Spine1
    19: 18, # R UpperArm -> R Clavicle
    20: 19, # R Forearm -> R UpperArm
    21: 20, # R Hand -> R Forearm
    22: 21, # R Finger0 -> R Hand
    23: 22, # R Finger01 -> R Finger0
    24: 21, # R Finger1 -> R Hand
    25: 24, # R Finger11 -> R Finger1
    26: 1,  # L Thigh -> Pelvis 1
    27: 26, # L Calf -> L Thigh
    28: 27, # L Foot -> L Calf
    29: 28, # L Toe0 -> L Foot
    30: 1,  # R Thigh -> Pelvis 1
    31: 30, # R Calf -> R Thigh
    32: 31, # R Foot -> R Calf
    33: 32, # R Toe0 -> R Foot
    34: 21, # Arrow -> R Hand 21
    35: 3,  # Breast -> Spine1 3
}

FARAH_BIPED_PARENTS: Dict[int, int] = FARAH_GIZMO_PARENTS


ENVIRONMENT_PROP_KEYWORDS: Tuple[str, ...] = (
    "palmier", "feuille", "arbre", "tree", "plant", "herbe", "grass", "vegetation",
    "drapeau", "flag", "banner", "curtain", "rideau", "tente", "tent", "liane", "corde",
    "rope", "cloth", "toile", "sheet", "cloud", "nuage", "eau", "water", "sand_cloud",
    "fx_", "gfx_", "dust", "smoke", "cascade", "fountain", "torch", "flamme", "fire"
)

CHARACTER_KEYWORDS: Tuple[str, ...] = (
    "prince", "farah", "sandman", "sman", "sguard", "sandguard", "courtesan", "scourtesan",
    "indian", "act_", "enemy", "boss", "dahaka", "shahdee", "kaileena", "kaleena",
    "sandwraith", "sandgriffin", "brute", "assassin", "thief", "crow_master", "crow",
    "mahasti", "thrall", "vizier", "elika", "darkprince", "horde", "pirate", "disciple",
    "initiate", "imperial", "corbeau"
)

ACCESSORY_KEYWORDS: Tuple[str, ...] = (
    "face", "hair", "cheveux", "yeux", "eyelid", "veil", "voile", "shoulder",
    "sword", "dagger", "arme", "carquois", "medaillon", "breast", "fleche",
    "head", "helmet", "casque", "weapon", "epee", "sabre", "shield", "bouclier",
)

CHARACTER_GROUP_TOKENS: Tuple[str, ...] = (
    "farah", "kaileena", "kaleena", "shahdee", "dahaka", "sandwraith",
    "sandgriffin", "sandguard", "sguard", "sandman", "sman", "courtesan",
    "crow_master", "mahasti", "vizier", "elika", "darkprince", "prince",
    "pirate", "initiate", "initie", "imperial", "brute", "assassin",
    "thief", "thrall", "horde", "disciple", "indian",
)


def infer_character_group(name: str) -> str:
    """Best-effort character kit name from a GameObject, mesh, clip, or archive entry."""
    low = (name or "").casefold()
    for token in CHARACTER_GROUP_TOKENS:
        if token in low:
            return token
    return ""


def is_rigid_accessory(name: str) -> bool:
    """True for modular parts that should follow a single bone instead of LBS skinning."""
    low = (name or "").casefold()
    if is_environment_prop(low):
        return False
    return any(k in low for k in ACCESSORY_KEYWORDS)


def mul_matrix_col(a: Tuple[float, ...] | List[float], b: Tuple[float, ...] | List[float]) -> Tuple[float, ...]:
    """Column-major 4x4 multiply C = A * B (same convention as transform_point)."""
    return tuple(
        sum(a[k * 4 + row] * b[col * 4 + k] for k in range(4))
        for col in range(4)
        for row in range(4)
    )


def object_world_matrix(obj) -> Tuple[float, ...]:
    """Column-major world matrix matching transformed_vertices()."""
    from .level_scene import object_basis
    bx, by, bz = object_basis(obj)
    sx, sy, sz = obj.scale
    px, py, pz = obj.position
    return (
        bx[0] * sx, bx[1] * sx, bx[2] * sx, 0.0,
        by[0] * sy, by[1] * sy, by[2] * sy, 0.0,
        bz[0] * sz, bz[1] * sz, bz[2] * sz, 0.0,
        px, py, pz, 1.0,
    )


def follow_bone_world_vertices(
    rest_world_verts: List[Tuple[float, float, float]],
    rest_bone: Tuple[float, ...] | List[float],
    anim_bone: Tuple[float, ...] | List[float],
    body_matrix: Optional[Tuple[float, ...] | List[float]] = None,
) -> List[Tuple[float, float, float]]:
    """Glue rest-pose world vertices to a bone using Anim * inverse(Rest) in world space."""
    if body_matrix is None:
        rest_w, anim_w = tuple(rest_bone), tuple(anim_bone)
    else:
        rest_w = mul_matrix_col(body_matrix, rest_bone)
        anim_w = mul_matrix_col(body_matrix, anim_bone)
    try:
        glue = mul_matrix_col(anim_w, inverse_matrix(rest_w))
    except ValueError:
        return list(rest_world_verts)
    return [transform_point(glue, vertex) for vertex in rest_world_verts]


def _matrix_from_object(obj) -> Tuple[float, ...]:
    """Rebuild a Jade row-major local matrix from a .gao bone GameObject."""
    basis = obj.basis
    raw = getattr(obj, "raw_scale", (1.0, 1.0, 1.0))
    px, py, pz = obj.position
    return (
        basis[0][0], basis[0][1], basis[0][2], raw[0],
        basis[1][0], basis[1][1], basis[1][2], raw[1],
        basis[2][0], basis[2][1], basis[2][2], raw[2],
        px, py, pz, 1.0,
    )


def _matrices_close(a, b, tol: float = 5e-3) -> bool:
    """Compare the 3x3 basis and the translation of two Jade matrices."""
    for i in (0, 1, 2, 4, 5, 6, 8, 9, 10):
        if abs(a[i] - b[i]) > tol:
            return False
    for i in (12, 13, 14):
        if abs(a[i] - b[i]) > tol:
            return False
    return True


def derive_character_rig(
    level,
    character_hint: str,
    skin_bones,
    bind_worlds: Dict[int, Tuple[float, ...]],
) -> Tuple[Dict[int, int], Dict[int, int]]:
    """Derive a character's bone hierarchy and TRL gizmo mapping from game data.

    The retail rig is a chain of "B_<name> *.gao" GameObjects that carries the
    rest-pose local matrix of every bone.  The skinned mesh stores the inverse
    bind matrix of every bone it is weighted to.  Comparing the two reveals
    both the parent of every bone and which TRL gizmo drives it, because the
    gizmo numbering follows the .gao chain (gizmo 0 is the actor root node,
    which sits above the first skinned bone).

    Returns (parents, gizmo_of_bone) or ({}, {}) when the rig cannot be resolved.
    """
    hint = (character_hint or "").casefold()
    chain = [obj for obj in level.objects
             if (obj.name or "").casefold().startswith("b_")
             and (not hint or hint in (obj.name or "").casefold())]
    if len(chain) < 2 or not skin_bones or not bind_worlds:
        return {}, {}

    chain_locals = [_matrix_from_object(obj) for obj in chain]

    # Bind-space world matrix of every skinned bone.
    inv_world = {}
    for index, world in bind_worlds.items():
        try:
            inv_world[index] = inverse_matrix(world)
        except ValueError:
            continue
    if not inv_world:
        return {}, {}

    # Candidate parent/child relations: local = inv(world_parent) * world_child.
    # Match that local against the .gao chain to identify the bone and its node.
    parents: Dict[int, int] = {}
    node_of: Dict[int, int] = {}

    def creates_cycle(bone: int, parent: int) -> bool:
        seen = {bone}
        node = parent
        while node is not None:
            if node in seen:
                return True
            seen.add(node)
            node = parents.get(node)
        return False

    for child, world in bind_worlds.items():
        for parent, inv in inv_world.items():
            if parent == child:
                continue
            # local = world_child * inverse(world_parent)
            local = mul_matrix(world, inv)
            for node, chain_local in enumerate(chain_locals):
                if _matrices_close(local, chain_local):
                    parents[child] = parent
                    node_of[child] = node
                    break
            if child in parents:
                break

    # Accessory bones (hair, quiver, skirt roots) keep their own local frame in
    # the .gao data, so their transforms do not match the bind matrices
    # exactly.  Resolve them with a relaxed match, then fall back to the
    # closest already resolved bone.
    if len(parents) < len(bind_worlds):
        for child, world in bind_worlds.items():
            if child in parents:
                continue
            best = None
            for parent, inv in inv_world.items():
                if parent == child:
                    continue
                local = mul_matrix(world, inv)
                for node, chain_local in enumerate(chain_locals):
                    diff = max(abs(local[i] - chain_local[i])
                               for i in (0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14))
                    if best is None or diff < best[0]:
                        best = (diff, parent, node)
            if best and best[0] < 0.25 and not creates_cycle(child, best[1]):
                parents[child] = best[1]
                node_of[child] = best[2]

    if len(parents) < len(bind_worlds) and parents:
        resolved = list(parents)
        for child, world in bind_worlds.items():
            if child in parents:
                continue
            pos = world[12:15]
            best = None
            for parent in resolved:
                if creates_cycle(child, parent):
                    continue
                ppos = bind_worlds[parent][12:15]
                d = sum((pos[i] - ppos[i]) ** 2 for i in range(3))
                if best is None or d < best[0]:
                    best = (d, parent)
            if best:
                parents[child] = best[1]

    if len(parents) < 2:
        return {}, {}

    # Break any parent cycle introduced by the relaxed matching: a bone whose
    # parent chain loops back onto itself becomes a root.
    for bone in list(parents):
        seen = {bone}
        node = parents[bone]
        while node is not None and node in parents:
            if node in seen:
                parents[bone] = None
                break
            seen.add(node)
            node = parents.get(node)
    parents = {b: p for b, p in parents.items() if p is not None}

    if len(parents) < 2:
        return {}, {}

    gizmo_of = {bone: node for bone, node in node_of.items()}
    return parents, gizmo_of


def detect_gizmo_offset(
    level,
    clip: AnimationClip,
    mesh,
    rest: Dict[int, Any],
    parents: Dict[int, int],
    candidates: Tuple[int, ...] = (-3, -2, -1, 0, 1),
) -> int:
    """Find the offset between TRL gizmo ids and skinned bone indices.

    The TRL gizmo numbering is the retail bone order, which starts one node
    above the first skinned bone (the actor root), so the gizmo of a bone is
    normally its skin index plus one.  The offset is verified empirically: a
    correct offset makes the animated local orientations stay close to their
    rest-pose local orientations, while a wrong one applies unrelated
    rotations to the bones and tears the rig apart.
    """
    bone_indices = [b.index for b in (getattr(mesh, "skin_bones", None) or [])]
    if not bone_indices:
        return 0
    rest_world = {i: rest[i][0] for i in rest if i in bone_indices}

    local_bind: Dict[int, Tuple[float, ...]] = {}
    for g in sorted(rest_world):
        p = parents.get(g)
        local_bind[g] = (mul_matrix(rest_world[g], rest[p][3])
                         if (p is not None and p in rest_world and p != g) else rest_world[g])

    frames = [0, max(1, clip.frames // 3), max(1, (2 * clip.frames) // 3)]
    best = None
    for offset in candidates:
        # Gizmo 0 is the actor root node; it drives no skinned bone, so it is
        # excluded from both the mapping and the count.
        mapped = 0
        for track in clip.tracks:
            if track.gizmo == 0xFFFF or track.gizmo == 0:
                continue
            bone = track.gizmo + offset
            if bone in rest_world:
                mapped += 1
        if not mapped:
            continue

        deviation = 0.0
        samples = 0
        for frame in frames:
            if frame >= clip.frames:
                continue
            for track in clip.tracks:
                if track.gizmo == 0xFFFF or track.gizmo == 0:
                    continue
                bone = track.gizmo + offset
                if bone not in rest_world:
                    continue
                r = sample_track_field(track.keys, float(frame), "rotation")
                if r is None:
                    continue
                rm = quat_to_matrix(r)
                lb = local_bind[bone]
                for i in (0, 1, 2, 4, 5, 6, 8, 9, 10):
                    deviation += (rm[i] - lb[i]) ** 2
                samples += 1
        if not samples:
            continue
        score = (deviation / samples, -mapped)
        if best is None or score < best[0]:
            best = (score, offset)

    return best[1] if best else 0


def pick_closest_gizmo(
    centroid: Tuple[float, float, float],
    master_anim: Dict[int, Any],
    body_matrix: Optional[Tuple[float, ...] | List[float]] = None,
) -> Optional[int]:
    """Pick the rest-pose bone whose world origin is nearest to a mesh centroid."""
    best_giz: Optional[int] = None
    best_d: Optional[float] = None
    for giz, pose in master_anim.items():
        rest = pose[3] if len(pose) > 3 else None
        if rest is None:
            continue
        pos = (rest[12], rest[13], rest[14])
        if body_matrix is not None:
            pos = transform_point(body_matrix, pos)
        dx, dy, dz = pos[0] - centroid[0], pos[1] - centroid[1], pos[2] - centroid[2]
        dist = dx * dx + dy * dy + dz * dz
        if best_d is None or dist < best_d:
            best_d = dist
            best_giz = giz
    return best_giz


def find_character_anchor_object(level, target_character: str = "", accessory_obj=None):
    """Find the skinned body GameObject whose transform maps skeleton space to world."""
    if not level:
        return accessory_obj
    best = None
    best_bones = -1
    for obj in level.objects:
        if obj.kind == "bone" or obj.name.startswith("B_") or obj.position[2] <= -20000:
            continue
        lower = (obj.name or "").casefold()
        if is_rigid_accessory(lower) or is_environment_prop(lower):
            continue
        if target_character == "prince":
            if "farah" in lower:
                continue
            if not any(k in lower for k in ("prince", "plate_body", "legs", "sleeve", "pr_", "corps", "body")):
                continue
        elif target_character and target_character not in lower:
            continue
        bone_count = 0
        for mesh_key in level.mesh_links.get(id(obj), []):
            mesh = level.meshes.get(mesh_key)
            if mesh and mesh.skin_bones:
                bone_count += len(mesh.skin_bones)
        score = bone_count
        if any(k in lower for k in ("plate_body", "farah_body", "_body", "corps")):
            score += 1000
        if score > best_bones:
            best_bones = score
            best = obj
    return best or accessory_obj


def is_environment_prop(name: str) -> bool:
    """Returns True if object or mesh name represents environmental scenery (trees, flags, cloth, fx)."""
    low = (name or "").casefold()
    return any(k in low for k in ENVIRONMENT_PROP_KEYWORDS)


def is_character_object(obj_name: str, mesh_name: str = "") -> bool:
    """Returns True if this is an actor/character or modular character equipment."""
    combined = f"{obj_name} {mesh_name}".casefold()
    if is_environment_prop(combined):
        return False
    if any(k in combined for k in CHARACTER_KEYWORDS):
        return True
    if any(k in combined for k in ("plate_body", "sleeve", "legs", "corps", "body")):
        return True
    if any(k in combined for k in ACCESSORY_KEYWORDS):
        return True
    if any(k in combined for k in ("_arc", "arc_", "m_arc", "b_arc", "bow")):
        return True
    return False


CHARACTER_CLIP_LABELS: Dict[str, str] = {
    "prince": "👑 Prince",
    "farah": "🏹 Farah",
    "kaileena": "👑 Kaileena",
    "kaleena": "👑 Kaileena",
    "shahdee": "⚔️ Shahdee",
    "dahaka": "💀 Dahaka",
    "sandwraith": "👻 Sand Wraith",
    "sandgriffin": "🦅 Sand Griffin",
    "sandguard": "⚔️ Sand Guard",
    "sguard": "⚔️ Sand Guard",
    "sandman": "⚔️ Sand Man",
    "sman": "⚔️ Sand Man",
    "courtesan": "⚔️ Courtesan",
    "crow_master": "🦅 Crow Master",
    "mahasti": "⚔️ Mahasti",
    "vizier": "🧙 Vizier",
    "elika": "✨ Elika",
    "darkprince": "👑 Dark Prince",
    "pirate": "⚔️ Pirate",
    "initiate": "⚔️ Initiate",
    "initie": "⚔️ Initiate",
    "imperial": "⚔️ Imperial",
    "brute": "🧌 Brute",
    "assassin": "🥷 Assassin",
    "thief": "🥷 Thief",
    "thrall": "⚔️ Thrall",
    "horde": "⚔️ Horde",
    "disciple": "⚔️ Disciple",
    "indian": "⚔️ Indian Guard",
}


def format_clip_character(group: str) -> str:
    """Human-readable character owner for an animation clip."""
    key = (group or "").casefold().strip()
    if not key:
        return "❓ Unknown"
    return CHARACTER_CLIP_LABELS.get(key, f"👤 {key.replace('_', ' ').title()}")


def tag_animation_clips(clips: List[AnimationClip], source_name: str = "", objects=None) -> None:
    """Stamp clips with the character kit they were loaded from."""
    group = infer_character_group(source_name)
    if not group and objects:
        for obj in objects:
            group = infer_character_group(getattr(obj, "name", "") or "")
            if group:
                break
    for clip in clips:
        if not getattr(clip, "character_group", ""):
            clip.character_group = group


def infer_biped_parents_from_bind(bind: Dict[int, Any]) -> Dict[int, int]:
    """Rebuild a skeleton parent map from rest-pose bone origins (nearest inner bone)."""
    if not bind:
        return {}
    pos: Dict[int, Tuple[float, float, float]] = {}
    for giz, data in bind.items():
        mat = data[0]
        pos[giz] = (float(mat[12]), float(mat[13]), float(mat[14]))
    gizmos = list(bind.keys())
    root = min(gizmos)
    origin = pos[root]

    def dist2(a: int, b: int) -> float:
        pa, pb = pos[a], pos[b]
        return (pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2 + (pa[2] - pb[2]) ** 2

    root_dist = {
        giz: (pos[giz][0] - origin[0]) ** 2 + (pos[giz][1] - origin[1]) ** 2 + (pos[giz][2] - origin[2]) ** 2
        for giz in gizmos
    }
    parents: Dict[int, int] = {}
    for giz in gizmos:
        if giz == root:
            continue
        best = root
        best_d = dist2(giz, root)
        for parent in gizmos:
            # Jade gizmo indices are packed so a parent always has a lower id than its child.
            if parent >= giz:
                continue
            d = dist2(giz, parent)
            if d < best_d - 1e-10:
                best_d = d
                best = parent
            elif abs(d - best_d) <= 1e-10 and parent < best:
                best = parent
        parents[giz] = best
    return parents


def _is_prince_modular_mesh(obj_name: str, mesh_name: str) -> bool:
    combined = f"{obj_name} {mesh_name}".casefold()
    if "farah" in combined:
        return False
    return any(k in combined for k in ("prince", "pr_", "plate_body", "sleeve_left", "sleeve_right"))


def get_biped_parents(char_name: str, num_bones: int) -> Dict[int, int]:
    """Retrieve the correct anatomical parent hierarchy for any character rig."""
    low = (char_name or "").casefold()
    if "farah" in low:
        return FARAH_BIPED_PARENTS
    if num_bones == 22 or "pirate" in low:
        return {
            1: 0, 2: 1, 3: 2, 4: 3,
            5: 2, 6: 5, 7: 6, 8: 7,
            9: 2, 10: 9, 11: 10, 12: 11,
            13: 0, 14: 13, 15: 14, 16: 15,
            17: 0, 18: 17, 19: 18, 20: 19,
            21: 0
        }
    if num_bones == 27 or "guard" in low:
        return {
            1: 0, 2: 1, 3: 2, 4: 3,
            5: 2, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9,
            11: 2, 12: 11, 13: 12, 14: 13, 15: 14, 16: 15,
            17: 0, 18: 17, 19: 18,
            20: 0, 21: 20, 22: 21,
            23: 0, 24: 0, 25: 2, 26: 2
        }
    if num_bones == 24 or "initie" in low or "initiate" in low:
        return {
            1: 0, 2: 1, 3: 2, 4: 3,
            5: 2, 6: 5, 7: 6, 8: 7, 9: 8,
            10: 2, 11: 10, 12: 11, 13: 12, 14: 13,
            15: 0, 16: 15, 17: 16, 18: 17,
            19: 0, 20: 19, 21: 20, 22: 21,
            23: 0
        }
    return MASTER_BIPED_PARENTS


# Prince modular costume bone configurations (mapping local mesh bone indices to master biped gizmos)
PRINCE_MESH_CONFIGS: Dict[str, Dict[str, Any]] = {
    "plate_body": {
        "gizmo_map": [0, 1, 2, 3, 4, 5, 6, 7, 16, 17],
    },
    "sleeve_left": {
        "gizmo_map": [2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        "helper_map": {12: 8, 13: 8},
    },
    "sleeve_right": {
        "gizmo_map": [2, 3, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
        "helper_map": {12: 18, 13: 18},
    },
    "legs": {
        "gizmo_map": [0, 1, 26, 27, 28, 29, 30, 31, 32, 33],
        "helper_map": {10: 0, 11: 0, 12: 26, 13: 26, 14: 26, 15: 26, 16: 26, 17: 26,
                       18: 30, 19: 30, 20: 30, 21: 30, 22: 30, 23: 30, 24: 0},
    },
    "veil": {
        "gizmo_map": [0, 0, 0, 0],
    },
}


_gizmo_offset_cache: Dict[Tuple[int, str], Tuple[int, int]] = {}


def character_bone_parents(level, clip: AnimationClip, target_character: str = "") -> Dict[int, int]:
    """Return the bone hierarchy used to pose a character, for rig drawing.

    Mirrors the hierarchy selection inside compute_character_skeleton_poses so
    that the drawn rig links always match the animated skeleton.
    """
    low = (target_character or "").casefold()
    if "farah" in low:
        return dict(FARAH_GIZMO_PARENTS)
    if "prince" in low:
        return dict(MASTER_BIPED_PARENTS)
    rest: Dict[int, Any] = {}
    for obj in level.objects:
        if obj.kind == "bone" or (obj.name or "").startswith("B_"):
            continue
        lower = (obj.name or "").casefold()
        if low and low not in lower:
            continue
        for mk in level.mesh_links.get(id(obj), []):
            mesh = level.meshes.get(mk)
            if mesh is None or not mesh.skin_bones:
                continue
            built = build_skin_rest(mesh)
            for b in mesh.skin_bones:
                if b.index not in rest and b.index in built:
                    rest[b.index] = built[b.index]
    if not rest:
        return {}
    derived, _ = derive_character_rig(
        level, low, list(rest), {i: rest[i][0] for i in rest})
    if derived and len(derived) >= max(2, len(rest) // 2):
        return derived
    if "farah" in low:
        return dict(FARAH_BIPED_PARENTS)
    return infer_biped_parents_from_bind({i: rest[i] for i in rest})


def _detect_gizmo_offset_from_skeleton(level, character_hint: str, rest: Dict[int, Any]) -> int:
    """Determine gizmo offset by locating the pelvis/root bone in the level B_<char> object list.

    The TRL gizmo index is the position of a bone's GameObject in the level object list
    (0-indexed).  Bone index 0 in the IBM is the pelvis/root — we find its position in the
    level list by matching the bone name and return -(that index) as the offset so that
    bone = gizmo + offset.  Returns 0 if the pelvis cannot be located.
    """
    hint = (character_hint or "").casefold()
    # Collect B_<char> skeleton objects in level order
    bone_gaos = [o for o in level.objects if (o.name or "").casefold().startswith("b_")
                 and (not hint or hint in (o.name or "").casefold())]
    if len(bone_gaos) < 2 or not rest:
        return 0

    # IBM bone 0 is always the root/pelvis. Find it in the level-order list by name.
    pelvis_keywords = ("pelvis", "bip01", "root", "hip", "hanche")
    for gi, o in enumerate(bone_gaos):
        low = (o.name or "").casefold()
        if any(k in low for k in pelvis_keywords):
            # gizmo gi corresponds to bone index 0, so bone = gizmo + offset → offset = 0 - gi
            return -gi

    return 0



def compute_character_skeleton_poses(
    level,
    clip: AnimationClip,
    frame: float,
    target_character: str = "",
) -> Dict[int, Tuple[Tuple[float, ...], Tuple[float, float, float], Optional[Tuple[float, float, float, float]], Tuple[float, ...]]]:
    """Compute master biped forward kinematic world poses for a character scene."""
    master_bind: Dict[int, Tuple[Tuple[float, ...], Tuple[float, float, float], List[Any], List[float]]] = {}
    char_name = target_character or ""

    if not target_character:
        clip_name = (clip.name or "").casefold()
        group = getattr(clip, "character_group", "")
        if group:
            target_character = group
        elif "farah" in clip_name:
            target_character = "farah"
        elif "prince" in clip_name:
            target_character = "prince"

    # 1. Harvest bind matrices strictly from character body meshes.
    # Exclude environmental props (trees, flags, clouds) and facial/accessory rigs (eyelids, hair).
    skinned_meshes = []
    for obj in level.objects:
        if obj.kind == "bone" or obj.name.startswith("B_") or obj.position[2] <= -20000:
            continue
        lower_obj = (obj.name or "").casefold()
        if target_character == "prince":
            if not any(k in lower_obj for k in ("prince", "plate_body", "legs", "sleeve", "pr_")):
                continue
        elif target_character == "farah":
            if "farah" not in lower_obj:
                continue
        elif target_character:
            if target_character not in lower_obj:
                continue

        for mk in level.mesh_links.get(id(obj), []):
            if mk not in level.meshes:
                continue
            m = level.meshes[mk]
            if not m.skin_bones:
                continue
            lower_m = (m.object_name or "").casefold()

            # Skip environmental scenery props (palm tree leaves, flags, banners, cloth)
            if is_environment_prop(lower_obj) or is_environment_prop(lower_m):
                continue

            # Skip weapons and Prince-only modular extras from the master bind.
            # Farah hair/face often carry needed bind bones and must not be dropped.
            skip = ("carquois", "medaillon", "arc", "arme", "sword", "dagger")
            if target_character != "farah":
                skip = skip + ("face", "hair", "cheveux", "yeux", "eyelid", "veil", "voile", "breast")
            if any(s in lower_m or s in lower_obj for s in skip):
                continue

            skinned_meshes.append((obj, m, lower_obj, lower_m))

    # Prioritize body meshes first (anchor for skeleton), then modular parts, then accessories.
    # Face/hair/accessory meshes must NOT pollute the master bind even for Farah.
    def _mesh_priority(item):
        comb = item[3] + " " + item[2]
        # Face, hair, and facial accessories get very low priority (high number)
        # so they never overwrite body bone bind matrices in master_bind.
        if any(k in comb for k in ("face", "hair", "cheveux", "yeux", "eyelid",
                                   "ponytail", "carquois", "medaillon", "fleche",
                                   "breast", "veil", "voile")):
            return 100
        if "farah_body" in comb or ("farah" in comb and "body" in comb):
            return -1
        if "plate_body" in comb:
            return 0
        if _is_prince_modular_mesh(item[2], item[3]) and "legs" in comb:
            return 1
        if "sleeve_left" in comb:
            return 2
        if "sleeve_right" in comb:
            return 3
        return 10 - len(item[1].skin_bones)

    skinned_meshes.sort(key=_mesh_priority)

    for obj, m, lower_obj, lower_m in skinned_meshes:
        if not char_name:
            char_name = lower_obj or lower_m
        rest = build_skin_rest(m)
        cfg_key = None
        if _is_prince_modular_mesh(lower_obj, lower_m):
            cfg_key = next((k for k in PRINCE_MESH_CONFIGS if k in lower_m or k in lower_obj), None)
        if cfg_key:
            gmap = PRINCE_MESH_CONFIGS[cfg_key]["gizmo_map"]
            for b in m.skin_bones:
                if b.index < len(gmap):
                    giz = gmap[b.index]
                    if giz not in master_bind and b.index in rest:
                        master_bind[giz] = rest[b.index]
        elif "farah" in lower_obj or "farah" in lower_m or target_character == "farah":
            for b in m.skin_bones:
                if b.index < len(FARAH_GIZMO_MAP):
                    giz = FARAH_GIZMO_MAP[b.index]
                    if giz not in master_bind and b.index in rest:
                        master_bind[giz] = rest[b.index]
        else:
            # Unified character mesh (SandGuard, Pirate, Initiate, etc.)
            for b in m.skin_bones:
                if b.index not in master_bind and b.index in rest:
                    master_bind[b.index] = rest[b.index]

    if not master_bind:
        return {}

    low_char = (char_name or target_character or "").casefold()

    if "farah" in low_char or target_character == "farah":
        parents = dict(FARAH_GIZMO_PARENTS)
        if 0 not in master_bind:
            ident = (1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0)
            master_bind[0] = (ident, (0.0, 0.0, 0.0), [], list(ident))
        gizmo_offset = 0
    else:
        derived_parents, _gizmo_of = derive_character_rig(
            level, low_char,
            skin_bones=[b.index for b in skinned_meshes[0][1].skin_bones] if skinned_meshes else [],
            bind_worlds={i: rest[i][0] for i in rest},
        )
        if derived_parents and len(derived_parents) >= max(2, len(master_bind) // 2):
            parents = derived_parents
        elif target_character == "prince" or _is_prince_modular_mesh(char_name, char_name):
            parents = get_biped_parents("prince", len(master_bind))
        else:
            parents = infer_biped_parents_from_bind(master_bind)
        gizmo_offset = 0

    # 2. Precompute rest-pose local transform matrices: local_bind[g] = child_bind * inv(parent_bind)
    local_bind: Dict[int, Tuple[float, ...]] = {}
    for g in sorted(master_bind.keys()):
        p = parents.get(g)
        if p is not None and p in master_bind and p != g:
            p_ibm = master_bind[p][3]
            local_bind[g] = mul_matrix(master_bind[g][0], p_ibm)
        else:
            local_bind[g] = master_bind[g][0]

    # 3. Sample clip rotation & root translation tracks at current frame.
    rotations: Dict[int, Optional[Tuple[float, float, float, float]]] = {}
    root_trans: Optional[Tuple[float, float, float]] = None
    root_trans_0: Optional[Tuple[float, float, float]] = None
    for track in clip.tracks:
        if track.gizmo == 0xFFFF:
            continue
        rot = sample_track_field(track.keys, frame, "rotation")
        bone = track.gizmo + gizmo_offset
        if rot is not None and bone in master_bind and bone not in rotations:
            rotations[bone] = rot
        if track.gizmo == 0:
            t = sample_track_field(track.keys, frame, "translation")
            if t is not None:
                root_trans = t
            t0 = sample_track_field(track.keys, 0.0, "translation")
            if t0 is not None:
                root_trans_0 = t0

    # 4. Matrix Forward Kinematics (FK)
    # In Jade Engine, st_LocalMatrix orientation is set directly from the track quaternion (MATH_Copy33Matrix).
    # Forward Kinematics is computed as: Child_World = Child_Local * Father_World (MATH_MulMatrixMatrix).
    _IDENTITY = (1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    raw_worlds: Dict[int, Tuple[float, ...]] = {}
    poses: Dict[int, Tuple[Tuple[float, ...], Tuple[float, float, float], Optional[Tuple[float, float, float, float]], Tuple[float, ...]]] = {}
    visiting: set = set()

    def world_pose(giz: int):
        if giz in raw_worlds:
            return raw_worlds[giz]
        if giz in visiting:
            return local_bind.get(giz, _IDENTITY)
        visiting.add(giz)

        p = parents.get(giz)
        p_world = world_pose(p) if (p is not None and p in master_bind and p != giz) else None

        r = rotations.get(giz)
        loc = list(local_bind[giz])

        # The TRL quaternion directly stores the bone's local orientation for this frame
        # (MATH_Copy33Matrix into st_LocalMatrix, EVEnt_interpolationkey.c:1594).
        # Replace the rotation 3x3; the rest-pose translation stays in local_bind.
        if r:
            r_mat = quat_to_matrix(r)
            loc[:12] = list(r_mat[:12])

        if p_world is None:
            # Root pelvis translation
            if root_trans and root_trans_0:
                dx = root_trans[0] - root_trans_0[0]
                dy = root_trans[1] - root_trans_0[1]
                dz = root_trans[2] - root_trans_0[2]
                loc[12] = local_bind[giz][12] + dx
                loc[13] = local_bind[giz][13] + dy
                loc[14] = local_bind[giz][14] + dz

        # Child local is operand 1, Father world is operand 2 (OBJorient.c:692)
        world = mul_matrix(loc, p_world) if p_world is not None else tuple(loc)
        raw_worlds[giz] = world
        pos = (world[12], world[13], world[14])
        poses[giz] = (world, pos, r, master_bind[giz][0])
        visiting.discard(giz)
        return world

    for giz in sorted(master_bind.keys()):
        world_pose(giz)

    return poses


def compute_bone_poses(
    clip: AnimationClip,
    frame: float,
    rest: Dict[int, Any],
    parents: Optional[Dict[int, int]] = None,
    gizmo_map: Optional[List[int]] = None,
) -> Dict[int, Tuple[Tuple[float, ...], Tuple[float, float, float], Optional[Tuple[float, float, float, float]], Tuple[float, ...]]]:
    """Compute animated world-space bone transform matrices for a single skinned mesh."""
    parents = parents or MASTER_BIPED_PARENTS

    rotations: Dict[int, Optional[Tuple[float, float, float, float]]] = {}
    root_trans: Optional[Tuple[float, float, float]] = None
    root_trans_0: Optional[Tuple[float, float, float]] = None
    for track in clip.tracks:
        if track.gizmo == 0xFFFF:
            continue
        r = sample_track_field(track.keys, frame, "rotation")
        if r is not None and track.gizmo not in rotations:
            rotations[track.gizmo] = r
        if track.gizmo == 0:
            t = sample_track_field(track.keys, frame, "translation")
            if t is not None:
                root_trans = t
            t0 = sample_track_field(track.keys, 0.0, "translation")
            if t0 is not None:
                root_trans_0 = t0

    local_bind: Dict[int, Tuple[float, ...]] = {}
    for idx in sorted(rest.keys()):
        p = parents.get(idx)
        if p is not None and p in rest and p != idx:
            p_ibm = rest[p][3]
            local_bind[idx] = mul_matrix(rest[idx][0], p_ibm)
        else:
            local_bind[idx] = rest[idx][0]

    _IDENTITY = (1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    raw_worlds: Dict[int, Tuple[float, ...]] = {}
    poses: Dict[int, Tuple[Tuple[float, ...], Tuple[float, float, float], Optional[Tuple[float, float, float, float]], Tuple[float, ...]]] = {}
    visiting: set = set()

    def world_pose(idx: int):
        if idx in raw_worlds:
            return raw_worlds[idx]
        if idx in visiting:
            return local_bind.get(idx, _IDENTITY)
        visiting.add(idx)

        p = parents.get(idx)
        p_world = world_pose(p) if (p is not None and p in rest and p != idx) else None

        giz = gizmo_map[idx] if (gizmo_map is not None and idx < len(gizmo_map)) else idx
        r = rotations.get(giz) if giz is not None else None
        loc = list(local_bind[idx])

        # TRL quaternion directly stores the bone's absolute local orientation.
        if r:
            r_mat = quat_to_matrix(r)
            loc[:12] = list(r_mat[:12])

        if p_world is None:
            if root_trans and root_trans_0:
                dx = root_trans[0] - root_trans_0[0]
                dy = root_trans[1] - root_trans_0[1]
                dz = root_trans[2] - root_trans_0[2]
                loc[12] = local_bind[idx][12] + dx
                loc[13] = local_bind[idx][13] + dy
                loc[14] = local_bind[idx][14] + dz

        world = mul_matrix(loc, p_world) if p_world is not None else tuple(loc)
        raw_worlds[idx] = world
        pos = (world[12], world[13], world[14])
        poses[idx] = (world, pos, r, rest[idx][0])
        visiting.discard(idx)
        return world

    for bone_index in sorted(rest.keys()):
        world_pose(bone_index)
    return poses


def pose_mesh_vertices(
    mesh,
    clip: AnimationClip,
    frame: float,
    rest: Optional[Dict[int, Any]] = None,
    master_anim: Optional[Dict[int, Any]] = None,
    level=None,
    char_pos: Tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> List[Tuple[float, float, float]]:
    """Apply linear blend skinning (LBS) to deform mesh vertices along animation timeline."""
    bones = mesh.skin_bones or []
    if not bones:
        return mesh.vertices

    lower_name = (mesh.object_name or "").casefold()

    if rest is None:
        rest = build_skin_rest(mesh)

    # Prince modular costume only — never remap Farah/guard meshes via "legs"/"veil" substrings.
    matched_cfg = None
    if _is_prince_modular_mesh(lower_name, lower_name):
        for key, cfg in PRINCE_MESH_CONFIGS.items():
            if key in lower_name:
                matched_cfg = cfg
                break

    is_farah = "farah" in lower_name or "farah" in (getattr(mesh, "name", "") or "").casefold()

    if master_anim is None:
        if level is not None:
            master_anim = compute_character_skeleton_poses(level, clip, frame)
        else:
            gmap = matched_cfg["gizmo_map"] if matched_cfg else (FARAH_GIZMO_MAP if is_farah else None)
            return mesh.vertices

    gmap = matched_cfg["gizmo_map"] if matched_cfg else (FARAH_GIZMO_MAP if is_farah else None)
    hmap = matched_cfg.get("helper_map", {}) if matched_cfg else {}

    sums = [[0.0, 0.0, 0.0, 0.0] for _ in mesh.vertices]
    for bone in bones:
        bone_data = rest.get(bone.index)
        if not bone_data:
            continue

        giz = gmap[bone.index] if (gmap is not None and bone.index < len(gmap)) else (None if gmap is not None else bone.index)
        if giz is not None and giz in master_anim:
            world = master_anim[giz][0]
        elif bone.index in hmap:
            p_giz = hmap[bone.index]
            if p_giz in master_anim:
                p_world = master_anim[p_giz][0]
                p_bone = next((idx for idx, gz in enumerate(gmap) if gz == p_giz), None) if gmap else None
                p_rest = rest[p_bone][0] if (p_bone is not None and p_bone in rest) else (
                    master_anim[p_giz][3] if len(master_anim[p_giz]) > 3 else None
                )
                if p_rest is not None:
                    p_ibm = inverse_matrix(p_rest)
                    rel = mul_matrix(bone_data[0], p_ibm)
                    world = mul_matrix(rel, p_world)
                else:
                    world = p_world
            else:
                world = bone_data[0]
        else:
            world = bone_data[0]

        for vertex_index, weight, bind_local in bone_data[2]:
            target = transform_point(world, bind_local)
            acc = sums[vertex_index]
            for i in range(3):
                acc[i] += weight * target[i]
            acc[3] += weight

    # Standard linear blend skinning: divide by the accumulated weight so the
    # result is independent of how the influences are distributed.
    # CRITICAL FIX: For vertices with no weights, we must use the rest-pose position
    # transformed to world space using an appropriate bone transform, NOT the
    # local mesh vertex which causes T-pose deformation during animation.
    fallback_transform = None
    if rest and master_anim:
        # Try to find the root/pelvis bone (typically bone 0 or 1) for unweighted vertices
        # This ensures the entire mesh moves with the character's body
        for candidate_bone in [0, 1]:
            if candidate_bone in rest and candidate_bone in master_anim:
                fallback_transform = master_anim[candidate_bone][0]
                break
        # If no root bone found, use the first available bone
        if fallback_transform is None:
            first_bone_idx = next(iter(rest.keys()), None)
            if first_bone_idx is not None and first_bone_idx in master_anim:
                fallback_transform = master_anim[first_bone_idx][0]
    
    result = []
    for orig, acc in zip(mesh.vertices, sums):
        if acc[3] > 1e-6:
            # Vertex has bone weights - use standard LBS
            result.append(tuple(acc[i] / acc[3] for i in range(3)))
        elif fallback_transform is not None:
            # Vertex has no weights - transform by root bone to stay attached to skeleton
            result.append(transform_point(fallback_transform, orig))
        else:
            # No bones available - keep original vertex (shouldn't happen for skinned mesh)
            result.append(orig)
    
    return result


