"""Data models for Jade Engine BigFiles, levels, meshes, and textures."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
import numpy as np


@dataclass
class PopFileEntry:
    index: int
    offset: int
    size: int
    magic: int
    key: int
    data_offset: int
    data_type: Optional[int]


@dataclass
class TextureInfo:
    index: int
    offset: int
    data_offset: int
    data_end: int
    width: int
    height: int
    texture_type: int
    key: int
    format: str
    storage_width: int
    storage_height: int


@dataclass
class MeshInfo:
    index: int
    key: int
    entry_index: int
    version: int
    vertices: List[Tuple[float, float, float]]
    faces: List[Tuple[int, int, int]]
    uvs: List[Tuple[float, float]]
    uv_indices: List[Tuple[int, int, int]]
    material_ids: List[Tuple[int, int]]
    material_pack_key: Optional[int] = None
    object_name: str = ""
    second_vertices: Optional[List[Tuple[float, float, float]]] = None
    second_faces: Optional[List[Tuple[int, int, int]]] = None
    second_uvs: Optional[List[Tuple[float, float]]] = None
    second_uv_indices: Optional[List[Tuple[int, int, int]]] = None
    second_material_ids: Optional[List[Tuple[int, int]]] = None
    normals: Optional[List[Tuple[float, float, float]]] = None
    skin_bones: Optional[list] = None
    skin_flags: int = 0
    layout_name: str = ""
    vertex_colors: Optional[List[Tuple[float, float, float, float]]] = None


@dataclass
class MaterialInfo:
    index: int
    material_id: int
    material_key: Optional[int]
    texture_key: Optional[int]
    normal_key: Optional[int] = None
    secondary_key: Optional[int] = None
    metallic: float = 0.0
    alpha: float = 1.0
    source_meshes: Optional[List[int]] = None
    texture_offset: Optional[int] = None
    specular_offset: Optional[int] = None
    diffuse_offset: Optional[int] = None
    ambient: int = 0xFFFFFFFF
    diffuse_color: int = 0xFFFFFFFF
    specular_color: int = 0x00000000
    opacity: float = 1.0
    specular_exponent: float = 0.0
    material_kind: Optional[int] = None


@dataclass
class LevelObject:
    key: int
    entry_index: int
    name: str
    mesh_key: Optional[int]
    material_key: Optional[int]
    matrix_offset: int
    basis: Tuple[Tuple[float, float, float], ...]
    position: Tuple[float, float, float]
    scale: Tuple[float, float, float]
    bounds: Tuple[float, ...]
    kind: str
    source_asset_index: int = 0
    rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    raw_scale: Tuple[float, float, float] = (1.0, 1.0, 1.0)


@dataclass
class BigFileEntry:
    index: int
    position: int
    key: int
    size: int
    name: str
    parent: int
    fat_index: int
    first_index: int
    compressed: bool = False
    data_header_size: int = 0
    compression: str = "none"
    dir_path: str = ""
    full_path: str = ""


@dataclass
class BigFileInfo:
    path: Path
    version: int
    max_file: int
    max_dir: int
    size_fat: int
    num_fat: int
    universe_key: int
    encrypted_fat: bool
    entries: List[BigFileEntry]

    def get_entry_by_key(self, key: int) -> Optional[BigFileEntry]:
        for e in self.entries:
            if e.key == key:
                return e
        return None

    def get_entry_by_name(self, name: str) -> Optional[BigFileEntry]:
        norm = name.strip().lower()
        for e in self.entries:
            if e.name.strip().lower() == norm:
                return e
        return None


@dataclass
class LevelSceneData:
    name: str
    objects: List[LevelObject] = field(default_factory=list)
    meshes: Dict[int, MeshInfo] = field(default_factory=dict)
    textures: Dict[int, object] = field(default_factory=dict)  # key -> PIL.Image
    texture_maps: Dict[int, Dict[int, int]] = field(default_factory=dict)  # mesh_key -> {mat_id: tex_key}
    color_maps: Dict[int, Dict[int, Tuple[float, float, float, float]]] = field(default_factory=dict)  # mesh_key -> {mat_id: rgba}
    mesh_links: Dict[int, List[int]] = field(default_factory=dict)  # id(obj) -> [mesh_keys]
    source_assets: List[str] = field(default_factory=list)
    texture_infos: Dict[int, TextureInfo] = field(default_factory=dict)  # key -> TextureInfo
    texture_original_blobs: Dict[int, Tuple[bytes, str]] = field(default_factory=dict)  # key -> (blob, ext)
    texture_sources: Dict[int, str] = field(default_factory=dict)  # key -> asset filename
    animation_clips: List[object] = field(default_factory=list)  # list of AnimationClip
    ai_scripts: List[Dict[str, Any]] = field(default_factory=list)  # list of AI scripts/models
