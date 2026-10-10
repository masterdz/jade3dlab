import struct
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from io import BytesIO
import numpy as np


@dataclass
class Mesh:
    hash_id: str
    vertices: np.ndarray = field(default_factory=lambda: np.array([]))
    normals: np.ndarray = field(default_factory=lambda: np.array([]))
    uvs: np.ndarray = field(default_factory=lambda: np.array([]))
    faces: np.ndarray = field(default_factory=lambda: np.array([]))
    uv_indices: np.ndarray = field(default_factory=lambda: np.array([]))
    material_ids: List[Tuple[int, int]] = field(default_factory=list)
    material_groups: List[int] = field(default_factory=list)


@dataclass
class GameObject:
    name: str
    hash_id: str
    center: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: np.ndarray = field(default_factory=lambda: np.eye(3))
    scale: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    bounding_box: Tuple[float, ...] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    mesh_hash: str = ""
    material_pack_hash: str = ""
    extra_hash: str = ""
    group: str = "Other"
    flags: int = 0


@dataclass
class Material:
    hash_id: str
    texture_hash: str = ""
    specular_intensity: float = 0.0
    diffuse_intensity: float = 0.0
    version: int = 0


@dataclass
class Texture:
    hash_id: str
    width: int = 0
    height: int = 0
    compression: int = 0
    num_mipmaps: int = 0
    data: bytes = b''
    uses_palette: bool = False
    palette: Optional[List[Tuple[int, int, int, int]]] = None


@dataclass
class LevelData:
    meshes: Dict[str, Mesh] = field(default_factory=dict)
    game_objects: List[GameObject] = field(default_factory=list)
    materials: Dict[str, Material] = field(default_factory=dict)
    textures: Dict[str, Texture] = field(default_factory=dict)
    material_packs: Dict[str, List[str]] = field(default_factory=dict)
    wow_files: List[str] = field(default_factory=list)
    wol_files: List[str] = field(default_factory=list)


class BinaryReader:
    def __init__(self, buffer: bytes):
        self.__buffer = buffer
        self.length = len(buffer)
        self.pos = 0

    def read(self, num=None):
        if num is None:
            ret = self.__buffer[self.pos:]
            self.pos = self.length
            return ret
        ret = self.__buffer[self.pos:self.pos + num]
        self.pos += num
        return ret

    def read_byte(self, num=None):
        if num is None:
            return struct.unpack('B', self.read(1))[0]
        return struct.unpack(f'{num}B', self.read(num))

    def read_hex(self):
        b = self.read_byte(4)
        return ''.join(f'{x:02x}' for x in reversed(b)).upper()

    def read_short(self, num=None):
        if num is None:
            return struct.unpack('<H', self.read(2))[0]
        return struct.unpack(f'<{num}H', self.read(num * 2))

    def read_int(self, num=None):
        if num is None:
            return struct.unpack('<I', self.read(4))[0]
        return struct.unpack(f'<{num}I', self.read(num * 4))

    def read_float(self, num=None):
        if num is None:
            return struct.unpack('<f', self.read(4))[0]
        return struct.unpack(f'<{num}f', self.read(num * 4))

    def read_string(self, num=None):
        if num is None:
            chars = []
            while True:
                c = self.read(1)
                if c == b'\x00':
                    break
                chars.append(c)
            return b''.join(chars).decode('utf-8', errors='replace')
        return self.read(num).rstrip(b'\x00').decode('utf-8', errors='replace')

    def seek(self, offset, whence=0):
        if whence == 0:
            self.pos = offset
        elif whence == 1:
            self.pos += offset
        elif whence == 2:
            self.pos = self.length - offset

    def end_of_stream(self):
        return self.pos >= self.length
