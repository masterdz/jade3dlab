"""Jade Engine level graph reader, objects, transforms and WOL resolution."""
from __future__ import annotations

import math
import struct
from typing import Dict, Iterator, List, Optional, Set, Tuple

from .models import LevelObject
from .resources import parse_pop_file_entries

GAO_MAGIC = struct.unpack("<I", b".gao")[0]

BOX_FACES = (
    (0, 1, 3, 2), (0, 4, 5, 1), (4, 6, 7, 5),
    (6, 7, 3, 2), (0, 2, 6, 4), (1, 3, 7, 5)
)
BOX_EDGES = tuple((i, i | bit) for i in range(8) for bit in (1, 2, 4) if not i & bit)


def scan_level_objects(data: bytes, source_asset_index: int = 0) -> List[LevelObject]:
    """Scan all GameObjects (.gao) with positions, matrices, and visual links."""
    objects: List[LevelObject] = []
    for entry in parse_pop_file_entries(data):
        if entry.data_type != GAO_MAGIC or entry.size < 80:
            continue
        payload = data[entry.data_offset + 4:entry.data_offset + entry.size]
        try:
            _version, _flags, identity, name_len = struct.unpack_from("<4I", payload)
            if not 1 <= name_len <= 4096 or 16 + name_len + 78 > len(payload):
                continue
            name = payload[16:16 + name_len].rstrip(b"\0").decode("latin-1", "replace")
            matrix = 16 + name_len + 10
            values = struct.unpack_from("<16f", payload, matrix)
            if not all(math.isfinite(v) for v in values):
                continue
            basis = tuple(tuple(values[row * 4 + col] for col in range(3)) for row in range(3))
            raw_scale = tuple(values[row * 4 + 3] for row in range(3))
            scale = tuple(value or 1.0 for value in raw_scale)
            position = tuple(values[12:15])
            bounds_at = matrix + 68 + (24 if identity & 0x80000 else 0)
            bounds = struct.unpack_from("<6f", payload, bounds_at)
            visual_at = matrix + 68 + (48 if identity & 0x80000 else 24)
            mesh_key = material_key = None
            if identity & 0x4000 and visual_at + 8 <= len(payload):
                mesh_key, material_key = struct.unpack_from("<II", payload, visual_at)
            lower = name.casefold()
            kind = (
                "bone" if lower.startswith("b_") or "bone" in lower
                else "character" if any(s in lower for s in ("prince", "farah", "sand", "guard", "courtesan", "actor")) and mesh_key is not None
                else "trigger" if any(s in lower for s in ("trigger", "trig", "volume", "portal", "tec", "ini_pos"))
                else "light" if any(s in lower for s in ("light", "lamp", "lum_", "lanterne"))
                else "mesh" if mesh_key is not None else "object"
            )
            objects.append(LevelObject(
                entry.key, entry.index, name or f"Object 0x{entry.key:08X}",
                mesh_key, material_key, entry.data_offset + 4 + matrix,
                basis, position, scale, bounds, kind, source_asset_index,
                raw_scale=raw_scale
            ))
        except (struct.error, ValueError):
            continue
    return objects


def object_basis(obj: LevelObject) -> Tuple[Tuple[float, float, float], ...]:
    """Compute 3x3 orientation matrix from object basis and Euler rotation."""
    rx, ry, rz = (math.radians(v) for v in obj.rotation)
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)
    rows = (
        (cy * cz, cy * sz, -sy),
        (sx * sy * cz - cx * sz, sx * sy * sz + cx * cz, sx * cy),
        (cx * sy * cz + sx * sz, cx * sy * sz - sx * cz, cx * cy)
    )
    rotated = tuple(
        tuple(sum(obj.basis[k][col] * row[k] for k in range(3)) for col in range(3))
        for row in rows
    )
    return rotated


def transformed_vertices(source_vertices, obj: LevelObject) -> Iterator[Tuple[float, float, float]]:
    """Transform mesh local vertices into world coordinates using object basis, scale, and position."""
    bx, by, bz = object_basis(obj)
    sx, sy, sz = obj.scale
    px, py, pz = obj.position
    for x, y, z in source_vertices:
        x, y, z = x * sx, y * sy, z * sz
        yield (
            px + x * bx[0] + y * by[0] + z * bz[0],
            py + x * bx[1] + y * by[1] + z * bz[1],
            pz + x * bx[2] + y * by[2] + z * bz[2]
        )


def vertex_normals(vertices: List[Tuple[float, float, float]], faces: List[Tuple[int, int, int]]) -> List[Tuple[float, float, float]]:
    """Compute per-vertex smoothed surface normals."""
    normals = [[0.0, 0.0, 0.0] for _ in vertices]
    num_verts = len(vertices)
    for face in faces:
        if len(face) != 3 or any(i < 0 or i >= num_verts for i in face):
            continue
        a, b, c = vertices[face[0]], vertices[face[1]], vertices[face[2]]
        ab = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
        ac = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
        normal = (
            ab[1] * ac[2] - ab[2] * ac[1],
            ab[2] * ac[0] - ab[0] * ac[2],
            ab[0] * ac[1] - ab[1] * ac[0]
        )
        for idx in face:
            normals[idx][0] += normal[0]
            normals[idx][1] += normal[1]
            normals[idx][2] += normal[2]
    result = []
    for x, y, z in normals:
        length = math.sqrt(x * x + y * y + z * z) or 1.0
        result.append((x / length, y / length, z / length))
    return result


def level_asset_kind(name: str) -> Optional[str]:
    """Identify whether filename represents a WOL level, character, equipment, or WOW room."""
    lower = name.casefold()
    if any(s in lower for s in ("wol",)) and (".wol" in lower or "_wol_" in lower or lower.endswith("_wol.bin")):
        return "wol"
    if any(s in lower for s in ("costume", "weapon", "sword", "dagger", "actkit", "axe", "mace", "shield", "bow", "blade", "arme")) and "wow" in lower:
        return "equipment"
    if any(s in lower for s in (
        "prince", "farah", "sandman", "sandguard", "sandcourtesan", "indianman", "indianguard",
        "act_enemy", "act_boss", "dahaka", "shahdee", "kaileena", "kaleena", "sandwraith",
        "sandgriffin", "brute", "assassin", "thief", "crow_master", "mahasti", "thrall",
        "vizier", "elika", "darkprince", "horde", "pirate", "disciple", "initiate", "imperial"
    )) and "wow" in lower:
        return "character"
    if ".wow" in lower or "_wow_" in lower or lower.endswith("_wow") or lower.endswith("_wow.bin"):
        return "wow"
    return None


def wol_wow_keys(data: bytes) -> Set[int]:
    """Extract referenced WOW keys from WOL dependency records."""
    keys = set()
    needle = b".wow"
    start = 0
    while True:
        at = data.find(needle, start)
        if at < 0:
            return keys
        if at >= 4:
            keys.add(struct.unpack_from("<I", data, at - 4)[0])
        start = at + 4


def volume_corners(obj: LevelObject) -> Optional[List[Tuple[float, float, float]]]:
    """Get world-space bounding box corners for triggers/volumes."""
    bounds = obj.bounds
    if len(bounds) != 6 or not all(math.isfinite(v) and abs(v) < 100000 for v in bounds):
        return None
    xmin, ymin, zmin, xmax, ymax, zmax = bounds
    if xmin >= xmax or ymin >= ymax or zmin >= zmax:
        return None
    local_pts = [(x, y, z) for x in (xmin, xmax) for y in (ymin, ymax) for z in (zmin, zmax)]
    return list(transformed_vertices(local_pts, obj))


def volume_color(name: str) -> Tuple[float, float, float]:
    lower = name.casefold()
    if "portal" in lower:
        return (0.12, 0.85, 0.28)
    if "ini_pos" in lower or "set position" in lower:
        return (0.22, 0.40, 1.0)
    if "loading" in lower:
        return (1.0, 0.55, 0.12)
    return (0.08, 0.78, 0.95)
