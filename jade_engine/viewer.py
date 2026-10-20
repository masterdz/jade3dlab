"""Interactive OpenGL 3D viewer for Jade Engine levels with textures, materials, and lighting."""
from __future__ import annotations

import math
import time
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np
from PIL import Image
from PySide6.QtCore import Qt, QPoint, Signal, QTimer
from PySide6.QtWidgets import QLabel
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *

from .models import LevelObject, LevelSceneData, MeshInfo
from .animations import (
    AnimationClip,
    build_skin_rest,
    pose_mesh_vertices,
    compute_character_skeleton_poses,
    find_character_anchor_object,
    follow_bone_world_vertices,
    get_biped_parents,
    character_bone_parents,
    infer_character_group,
    is_character_object,
    is_environment_prop,
    is_rigid_accessory,
    mul_matrix_col,
    object_world_matrix,
    pick_closest_gizmo,
    transform_point,
)
from .level_scene import (
    BOX_EDGES,
    BOX_FACES,
    object_basis,
    transformed_vertices,
    vertex_normals,
    volume_color,
    volume_corners,
)


def _jade_uv_to_standard(uv: Tuple[float, float]) -> Tuple[float, float]:
    """Convert Jade's top-left V origin to standard OpenGL bottom-left."""
    return uv[0], 1.0 - uv[1]


class GLViewer(QOpenGLWidget):
    """Modern OpenGL 3D viewport for Prince of Persia Jade Engine levels."""

    object_selected = Signal(object)  # Emitted when an object is clicked
    transform_changed = Signal(object)  # Emitted when an object's transform changes
    mode_changed = Signal(str)  # Emitted when transform mode changes ('select', 'translate', 'rotate', 'scale')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.level: Optional[LevelSceneData] = None
        self.selected_object: Optional[LevelObject] = None

        # Transform Manipulation & Interactive Gizmo
        self.transform_mode: str = "translate"  # "select", "translate", "rotate", "scale"
        self.active_axis: Optional[str] = None  # "X", "Y", "Z", "CENTER"
        self.hovered_axis: Optional[str] = None
        self.is_transforming: bool = False
        self.move_whole_character: bool = True
        self.drag_start_screen: Optional[QPoint] = None
        self.drag_start_transforms: Dict[int, Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]] = {}

        # Camera state (Z-up coordinate system)
        self.yaw: float = -0.75
        self.pitch: float = 0.45
        self.distance: float = 50.0
        self.target: List[float] = [0.0, 0.0, 0.0]

        # Mouse interaction
        self.last_pos: Optional[QPoint] = None
        self.is_panning: bool = False
        self.is_orbiting: bool = False
        self.clicked_on_object: bool = False

        # Rendering options
        self.show_meshes: bool = True
        self.show_textures: bool = True
        self.show_objects: bool = True
        self.show_wireframe: bool = False
        self.show_grid: bool = True
        self.show_bones: bool = True
        self.enable_lighting: bool = True
        self.lighting_mode: str = "ingame"  # "ingame", "golden", "studio", "unlit"
        self.light_intensity: float = 1.0
        self.bg_color: Tuple[float, float, float] = (0.09, 0.10, 0.14)
        self.enable_fog: bool = False
        self.cull_backfaces: bool = False

        # OpenGL resources
        self.gl_textures: Dict[int, int] = {}
        self.display_lists: Dict[int, int] = {}  # id(obj) -> list_id

        # Animation & Dynamic Scene Effects
        self.animate_scene: bool = False
        self.turntable_active: bool = False
        self.wind_speed_u: float = 0.04
        self.wind_speed_v: float = 0.015
        self.anim_start_time: float = time.time()
        self.anim_timer = QTimer(self)
        self.anim_timer.setInterval(16)  # ~60 FPS
        self.anim_timer.timeout.connect(self._on_anim_frame)

        # Character Skeletal Animation & Fast Display List Cache
        self.active_clip: Optional[AnimationClip] = None
        self.anim_playing: bool = False
        self.anim_mode_active: bool = False
        self.anim_loop: bool = True
        self.anim_speed: float = 1.0
        self.current_anim_frame: float = 0.0
        self._skin_rest_cache: Dict[int, Any] = {}
        self._skeleton_anim_cache: Dict[Tuple[int, int, str], Any] = {}
        self._anim_vertex_cache: Dict[Tuple[int, int, int, int], List[Tuple[float, float, float]]] = {}
        self._anim_display_lists: Dict[Tuple[int, int, int], int] = {}  # (clip_key, frame_int, id(obj)) -> list_id
        self._accessory_bone_cache: Dict[int, int] = {}
        self.on_anim_frame_changed = None

        # Performance & Real-Time On-Screen FPS Monitor
        self._last_fps_time: float = time.perf_counter()
        self._current_fps: float = 60.0
        self._current_frame_ms: float = 16.6

        self.fps_badge = QLabel("⚡ 60 FPS (16.6 ms)", self)
        self.fps_badge.setObjectName("FpsBadge")
        self.fps_badge.setStyleSheet("""
            QLabel#FpsBadge {
                background-color: rgba(18, 19, 28, 0.85);
                color: #00e676;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
                font-size: 11px;
                font-weight: bold;
                border: 1px solid #2d3040;
                border-radius: 4px;
                padding: 3px 8px;
            }
        """)
        self.fps_badge.adjustSize()
        self.fps_badge.show()

        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "fps_badge") and self.fps_badge:
            self.fps_badge.adjustSize()
            self.fps_badge.move(max(10, self.width() - self.fps_badge.width() - 12), 12)

    def _clear_anim_display_lists(self):
        """Free OpenGL display lists cached for animated playback frames."""
        if hasattr(self, "_anim_display_lists") and self._anim_display_lists and self.isValid():
            try:
                self.makeCurrent()
                for lid in self._anim_display_lists.values():
                    glDeleteLists(lid, 1)
            except Exception:
                pass
            self._anim_display_lists.clear()
        self._anim_vertex_cache.clear()
        self._skeleton_anim_cache.clear()
        self._accessory_bone_cache.clear()

    def _on_anim_frame(self):
        if self.turntable_active:
            self.yaw += 0.005
        if self.anim_playing and self.active_clip and self.active_clip.frames > 0:
            self.current_anim_frame += self.anim_speed
            if self.current_anim_frame >= self.active_clip.frames:
                if self.anim_loop:
                    self.current_anim_frame = self.current_anim_frame % max(1.0, float(self.active_clip.frames))
                else:
                    self.current_anim_frame = float(max(0, self.active_clip.frames - 1))
                    self.anim_playing = False
            if self.on_anim_frame_changed:
                self.on_anim_frame_changed(self.current_anim_frame)
        self.update()

    def set_active_clip(self, clip: Optional[AnimationClip], activate_mode: bool = False):
        """Set the active skeletal animation clip for real-time playback."""
        self._clear_anim_display_lists()
        self.active_clip = clip
        self.current_anim_frame = 0.0
        self.anim_mode_active = (clip is not None) if activate_mode else False
        if clip and self.level:
            for m in self.level.meshes.values():
                if m.skin_bones and m.key not in self._skin_rest_cache:
                    try:
                        self._skin_rest_cache[m.key] = build_skin_rest(m)
                    except Exception:
                        pass
        self.update()

    def set_anim_playing(self, playing: bool):
        self.anim_playing = playing
        if playing:
            self.anim_mode_active = True
        if playing or self.animate_scene or self.turntable_active:
            if not self.anim_timer.isActive():
                self.anim_timer.start()
        else:
            if not (self.animate_scene or self.turntable_active):
                self.anim_timer.stop()
        self.update()

    def set_anim_frame(self, frame: float):
        self.current_anim_frame = frame
        self.anim_mode_active = True
        self.update()

    def reset_animation(self):
        """Reset animation playback and restore character to static rest pose."""
        self._clear_anim_display_lists()
        self.anim_playing = False
        self.anim_mode_active = False
        self.current_anim_frame = 0.0
        self.update()

    def set_anim_loop(self, loop: bool):
        self.anim_loop = loop

    def set_anim_speed(self, speed: float):
        self.anim_speed = speed

    def set_scene_animation(self, enabled: bool):
        self.animate_scene = enabled
        if self.animate_scene or self.turntable_active or self.anim_playing:
            if not self.anim_timer.isActive():
                self.anim_start_time = time.time()
                self.anim_timer.start()
        else:
            if not (self.turntable_active or self.anim_playing):
                self.anim_timer.stop()
        self.update()

    def set_turntable(self, enabled: bool):
        self.turntable_active = enabled
        if self.turntable_active or self.animate_scene or self.anim_playing:
            if not self.anim_timer.isActive():
                self.anim_timer.start()
        else:
            if not (self.animate_scene or self.anim_playing):
                self.anim_timer.stop()
        self.update()

    def set_light_intensity(self, val: float):
        self.light_intensity = max(0.05, min(5.0, val))
        self.update()

    def set_background_color(self, r: float, g: float, b: float):
        self.bg_color = (r, g, b)
        if self.isValid():
            self.makeCurrent()
            glClearColor(r, g, b, 1.0)
        self.update()

    def initializeGL(self):
        glClearColor(self.bg_color[0], self.bg_color[1], self.bg_color[2], 1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Alpha testing: relaxed threshold so textures with specular / detail alpha maps on stone walls are preserved
        glEnable(GL_ALPHA_TEST)
        glAlphaFunc(GL_GREATER, 0.02)

        # Double-sided rendering so single-sided walls, arches, and doorways are solid from all angles
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
        glDisable(GL_CULL_FACE)

        # Lighting setup
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.5, 2.5, 0.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.85, 0.85, 0.85, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.4, 0.4, 0.4, 1.0])

        glEnable(GL_LIGHT1)
        glLightfv(GL_LIGHT1, GL_POSITION, [-1.0, -1.0, 1.0, 0.0])
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.35, 0.35, 0.4, 1.0])

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.35, 0.35, 0.38, 1.0])

        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    def resizeGL(self, w: int, h: int):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h if h > 0 else 1.0
        far_plane = max(25000.0, self.distance * 4.0)
        near_plane = max(0.1, min(1.0, self.distance * 0.01))
        gluPerspective(50.0, aspect, near_plane, far_plane)
        glMatrixMode(GL_MODELVIEW)

    def _clear_gl_resources(self):
        self._clear_anim_display_lists()
        if self.display_lists and self.isValid():
            self.makeCurrent()
            for list_id in self.display_lists.values():
                glDeleteLists(list_id, 1)
            self.display_lists.clear()

        if self.gl_textures and self.isValid():
            self.makeCurrent()
            glDeleteTextures(list(self.gl_textures.values()))
            self.gl_textures.clear()

    def set_level(self, level: LevelSceneData):
        """Set the active level scene and prepare display lists."""
        self._clear_gl_resources()
        self.level = level
        self.selected_object = None
        self.active_clip = None
        self.anim_playing = False
        self._skin_rest_cache.clear()
        self._skeleton_anim_cache.clear()
        self._anim_vertex_cache.clear()
        self._accessory_bone_cache.clear()

        # Upload textures
        if self.isValid():
            self.makeCurrent()
            for key, img in level.textures.items():
                self._upload_texture(key, img)

        # Center camera on scene
        self.frame_level()

        # Prebuild display lists
        if self.isValid():
            self.makeCurrent()
            self._rebuild_display_lists()

        self.update()

    def add_spawned_character(
        self,
        new_objects: List[LevelObject],
        new_textures: Dict[int, Any],
        focus_pos: Optional[Tuple[float, float, float]] = None,
    ):
        """Incrementally register newly spawned character objects and textures into OpenGL viewport."""
        if not self.level:
            return

        if self.isValid():
            self.makeCurrent()
            for key, img in new_textures.items():
                self._upload_texture(key, img)

            for obj in new_objects:
                if obj.kind == "bone" or obj.name.startswith("B_") or obj.position[2] <= -20000:
                    continue
                mesh_keys = self.level.mesh_links.get(id(obj), [])
                linked_meshes = [self.level.meshes[k] for k in mesh_keys if k in self.level.meshes]
                if not linked_meshes:
                    continue
                list_id = glGenLists(1)
                glNewList(list_id, GL_COMPILE)
                for mesh in linked_meshes:
                    world_verts = list(transformed_vertices(mesh.vertices, obj))
                    normals = vertex_normals(world_verts, mesh.faces) if not mesh.normals else mesh.normals
                    tex_map = self.level.texture_maps.get(mesh.key, {})
                    col_map = self.level.color_maps.get(mesh.key, {})
                    self._render_mesh_triangles(mesh, world_verts, normals, tex_map, col_map)
                glEndList()
                self.display_lists[id(obj)] = list_id

        self._clear_anim_display_lists()
        self._skin_rest_cache.clear()
        self._skeleton_anim_cache.clear()
        self._anim_vertex_cache.clear()
        self._accessory_bone_cache.clear()

        if focus_pos is not None:
            self.target = [focus_pos[0], focus_pos[1], focus_pos[2] + 1.0]
            self.distance = 5.0
            self.yaw = 25.0
            self.pitch = 15.0

        self.update()

    def frame_level(self):
        """Fit camera to all objects in the scene, ignoring offscreen/pooled inactive entities."""
        if not self.level or not self.level.objects:
            self.target = [0.0, 0.0, 0.0]
            self.distance = 50.0
            return

        points = []
        for obj in self.level.objects:
            if obj.kind == "bone" or obj.name.startswith("B_"):
                continue
            # Filter out parked/offscreen pooled objects in v38 (e.g. Z <= -10000 or Z >= 20000 or coords > 25000)
            if abs(obj.position[2]) > 10000 or abs(obj.position[0]) > 25000 or abs(obj.position[1]) > 25000:
                continue
            links = self.level.mesh_links.get(id(obj), [])
            if links:
                points.append(obj.position)

        if not points:
            points = [o.position for o in self.level.objects if o.kind != "bone" and abs(o.position[2]) < 10000 and abs(o.position[0]) < 25000]
        if not points:
            points = [o.position for o in self.level.objects if abs(o.position[2]) < 10000]
        if not points:
            points = [o.position for o in self.level.objects]

        if points:
            cx = sum(p[0] for p in points) / len(points)
            cy = sum(p[1] for p in points) / len(points)
            cz = sum(p[2] for p in points) / len(points)
            self.target = [cx, cy, cz]
            radius = max(math.dist(p, self.target) for p in points)
            if radius < 5.0:
                self.distance = max(2.5, radius * 2.2)
                # For characters standing upright, focus around chest/head (Z ~ 1.0m)
                if cz < 0.5 and any(p[2] > 1.0 for p in points):
                    self.target[2] = 1.0
            else:
                self.distance = max(10.0, radius * 1.8)

    def select_object(self, obj: Optional[LevelObject]):
        self.selected_object = obj
        if obj is not None and self.transform_mode == "select":
            self.transform_mode = "translate"
        self.update()

    def focus_object(self, obj: LevelObject):
        self.selected_object = obj
        self.target = list(obj.position)
        linked = [self.level.meshes[k] for k in self.level.mesh_links.get(id(obj), []) if k in self.level.meshes]
        if linked:
            v_radius = 5.0
            for m in linked:
                for v in m.vertices:
                    v_radius = max(v_radius, math.hypot(v[0], v[1], v[2]))
            self.distance = max(4.0, v_radius * 2.5)
        else:
            self.distance = 12.0
        self.update()

    def _upload_texture(self, key: int, image) -> Optional[int]:
        if key in self.gl_textures:
            return self.gl_textures[key]
        if image is None:
            return None
        try:
            rgba_img = image.convert("RGBA").transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            tex_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, rgba_img.width, rgba_img.height, 0,
                         GL_RGBA, GL_UNSIGNED_BYTE, rgba_img.tobytes())
            glGenerateMipmap(GL_TEXTURE_2D)
            self.gl_textures[key] = tex_id
            return tex_id
        except Exception:
            return None

    def _rebuild_display_lists(self):
        if not self.level:
            return

        for obj in self.level.objects:
            # Skip bone collision/proxy meshes so character models display cleanly
            if obj.kind == "bone" or obj.name.startswith("B_"):
                continue
            # Skip parked pooled objects hidden at extreme depths (e.g. Z <= -20000)
            if obj.position[2] <= -20000:
                continue

            mesh_keys = self.level.mesh_links.get(id(obj), [])
            linked_meshes = [self.level.meshes[k] for k in mesh_keys if k in self.level.meshes]
            if not linked_meshes:
                continue

            list_id = glGenLists(1)
            glNewList(list_id, GL_COMPILE)
            for mesh in linked_meshes:
                world_verts = list(transformed_vertices(mesh.vertices, obj))
                normals = vertex_normals(world_verts, mesh.faces) if not mesh.normals else mesh.normals
                tex_map = self.level.texture_maps.get(mesh.key, {})
                col_map = self.level.color_maps.get(mesh.key, {})
                self._render_mesh_triangles(mesh, world_verts, normals, tex_map, col_map)
            glEndList()
            self.display_lists[id(obj)] = list_id

    def _render_mesh_triangles(
        self,
        mesh: MeshInfo,
        vertices: List[Tuple[float, float, float]],
        normals: Optional[List[Tuple[float, float, float]]],
        tex_map: Dict[int, int],
        col_map: Dict[int, Tuple[float, float, float, float]],
    ):
        faces = mesh.faces
        uvs = mesh.uvs
        uv_indices = mesh.uv_indices
        vcolors = mesh.vertex_colors

        face_materials = [0] * len(faces)
        cursor = 0
        for mat_id, count in mesh.material_ids or []:
            for i in range(cursor, min(cursor + count, len(faces))):
                face_materials[i] = mat_id
            cursor += count

        current_tex_id = None

        for face_idx, face in enumerate(faces):
            if len(face) != 3:
                continue

            mat_id = face_materials[face_idx] if face_idx < len(face_materials) else 0
            tex_key = tex_map.get(mat_id)
            tex_id = self.gl_textures.get(tex_key) if (tex_key is not None and self.show_textures) else None
            r, g, b, a = col_map.get(mat_id, (0.8, 0.8, 0.8, 1.0))

            if tex_id != current_tex_id:
                if current_tex_id is not None:
                    glEnd()
                current_tex_id = tex_id
                if tex_id:
                    glEnable(GL_TEXTURE_2D)
                    glBindTexture(GL_TEXTURE_2D, tex_id)
                else:
                    glDisable(GL_TEXTURE_2D)
                glBegin(GL_TRIANGLES)
            elif face_idx == 0:
                if tex_id:
                    glEnable(GL_TEXTURE_2D)
                    glBindTexture(GL_TEXTURE_2D, tex_id)
                else:
                    glDisable(GL_TEXTURE_2D)
                glBegin(GL_TRIANGLES)

            for corner, vi in enumerate(face):
                if vcolors and 0 <= vi < len(vcolors):
                    vr, vg, vb, _va = vcolors[vi]
                    # In Jade Engine, vertex colors represent RLI vertex lighting (RGB); maintain material opacity a
                    glColor4f(r * vr, g * vg, b * vb, a)
                else:
                    glColor4f(r, g, b, a)

                if uv_indices and face_idx < len(uv_indices) and uvs:
                    ui = uv_indices[face_idx][corner]
                    if 0 <= ui < len(uvs):
                        u, v = _jade_uv_to_standard(uvs[ui])
                        glTexCoord2f(float(u), float(v))

                if normals and 0 <= vi < len(normals):
                    nx, ny, nz = normals[vi]
                    glNormal3f(float(nx), float(ny), float(nz))

                x, y, z = vertices[vi]
                glVertex3f(float(x), float(y), float(z))

        if current_tex_id is not None or faces:
            glEnd()
            glDisable(GL_TEXTURE_2D)

    def _get_skeleton_anim_poses(self, clip: AnimationClip, frame: float, target_char: str = "") -> Dict[int, Any]:
        """Compute or retrieve cached master biped poses (Gizmos 0..33) for character scene."""
        frame_int = int(round(frame))
        cache_key = (clip.key, frame_int, target_char)
        if cache_key in self._skeleton_anim_cache:
            return self._skeleton_anim_cache[cache_key]
        if self.level:
            poses = compute_character_skeleton_poses(self.level, clip, float(frame_int), target_character=target_char)
        else:
            poses = {}
        self._skeleton_anim_cache[cache_key] = poses
        return poses

    def _resolve_clip_character(self, clip: AnimationClip, mesh: Optional[MeshInfo] = None, obj: Optional[LevelObject] = None) -> str:
        group = getattr(clip, "character_group", "") or ""
        if group:
            return group
        names = " ".join(part for part in (
            clip.name,
            getattr(mesh, "object_name", "") if mesh else "",
            getattr(obj, "name", "") if obj else "",
        ) if part)
        inferred = infer_character_group(names)
        if inferred:
            return inferred
        lower = names.casefold()
        if any(k in lower for k in ("plate_body", "legs", "sleeve", "pr_")):
            return "prince"
        return ""

    def _get_animated_vertices(self, mesh: MeshInfo, clip: AnimationClip, frame: float, obj: LevelObject) -> List[Tuple[float, float, float]]:
        """Compute or retrieve cached deformed vertices for a character mesh at the current animation frame."""
        frame_int = int(round(frame))
        cache_key = (clip.key, frame_int, mesh.key)
        if cache_key in self._anim_vertex_cache:
            return self._anim_vertex_cache[cache_key]

        lower_name = f"{mesh.object_name or ''} {obj.name or ''}".casefold()
        mesh_char = infer_character_group(lower_name)
        clip_char = getattr(clip, "character_group", "") or ""
        if clip_char and mesh_char and clip_char != mesh_char:
            world_verts = list(transformed_vertices(mesh.vertices, obj))
            self._anim_vertex_cache[cache_key] = world_verts
            return world_verts
        target_char = clip_char or mesh_char or self._resolve_clip_character(clip, mesh, obj)
        master_anim = self._get_skeleton_anim_poses(clip, frame, target_char)
        body_obj = find_character_anchor_object(self.level, target_char, obj)
        char_pos = body_obj.position if body_obj is not None else (0.0, 0.0, 0.0)

        has_skin = bool(mesh.skin_bones)
        if (is_rigid_accessory(lower_name) or any(w in lower_name for w in ("_arc", "arc_", "m_arc", "bow"))) and not has_skin:
            world_verts = self._transform_rigid_accessory(mesh, obj, master_anim, body_obj)
            self._anim_vertex_cache[cache_key] = world_verts
            return world_verts

        rest = self._skin_rest_cache.get(mesh.key)
        if rest is None:
            try:
                rest = build_skin_rest(mesh)
                self._skin_rest_cache[mesh.key] = rest
            except Exception:
                rest = {}

        try:
            posed = pose_mesh_vertices(
                mesh, clip, float(frame_int),
                rest=rest, master_anim=master_anim, level=self.level, char_pos=char_pos
            )
            world_verts = list(transformed_vertices(posed, obj))
        except Exception:
            world_verts = list(transformed_vertices(mesh.vertices, obj))

        self._anim_vertex_cache[cache_key] = world_verts
        return world_verts

    def paintGL(self):
        # Real-time FPS counter calculation & badge update
        now = time.perf_counter()
        dt = now - self._last_fps_time
        self._last_fps_time = now
        if dt > 0.0:
            instant_fps = 1.0 / dt
            self._current_fps = 0.9 * self._current_fps + 0.1 * instant_fps
            self._current_frame_ms = 0.9 * self._current_frame_ms + 0.1 * (dt * 1000.0)
            if hasattr(self, "fps_badge") and self.fps_badge:
                color = "#00e676" if self._current_fps >= 45.0 else ("#ffab00" if self._current_fps >= 25.0 else "#ff5252")
                self.fps_badge.setStyleSheet(f"""
                    QLabel#FpsBadge {{
                        background-color: rgba(18, 19, 28, 0.85);
                        color: {color};
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
                        font-size: 11px;
                        font-weight: bold;
                        border: 1px solid #2d3040;
                        border-radius: 4px;
                        padding: 3px 8px;
                    }}
                """)
                self.fps_badge.setText(f"⚡ {self._current_fps:.0f} FPS ({self._current_frame_ms:.1f} ms)")
                self.fps_badge.adjustSize()
                self.fps_badge.move(max(10, self.width() - self.fps_badge.width() - 12), 12)

        glClearColor(self.bg_color[0], self.bg_color[1], self.bg_color[2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Dynamic perspective projection adapting to distance
        w = max(1, self.width())
        h = max(1, self.height())
        aspect = w / h
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        far_plane = max(25000.0, self.distance * 4.0)
        near_plane = max(0.1, min(1.0, self.distance * 0.01))
        gluPerspective(50.0, aspect, near_plane, far_plane)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Eye position in Z-up system
        cp, sp = math.cos(self.pitch), math.sin(self.pitch)
        cy, sy = math.cos(self.yaw), math.sin(self.yaw)
        eye_x = self.target[0] + self.distance * cp * cy
        eye_y = self.target[1] + self.distance * cp * sy
        eye_z = self.target[2] + self.distance * sp

        gluLookAt(eye_x, eye_y, eye_z, self.target[0], self.target[1], self.target[2], 0.0, 0.0, 1.0)

        # Backface culling state
        if self.cull_backfaces:
            glEnable(GL_CULL_FACE)
            glCullFace(GL_BACK)
        else:
            glDisable(GL_CULL_FACE)

        # Fog simulation (Sands of Time atmospheric palace mist)
        if self.enable_fog:
            glEnable(GL_FOG)
            glFogi(GL_FOG_MODE, GL_LINEAR)
            glFogfv(GL_FOG_COLOR, [0.38, 0.34, 0.28, 1.0])
            glFogf(GL_FOG_START, max(5.0, self.distance * 0.3))
            glFogf(GL_FOG_END, max(40.0, self.distance * 2.8))
        else:
            glDisable(GL_FOG)

        # Lighting state & mode with light volume / intensity scaling
        if self.enable_lighting:
            glEnable(GL_LIGHTING)
            li = self.light_intensity
            if self.lighting_mode == "ingame":
                # In-Game Atmosphere: Prioritizes baked RLI vertex radiosity with balanced ambient
                glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [min(1.0, 0.65 * li), min(1.0, 0.65 * li), min(1.0, 0.68 * li), 1.0])
                glLightfv(GL_LIGHT0, GL_DIFFUSE, [min(1.0, 0.45 * li), min(1.0, 0.45 * li), min(1.0, 0.45 * li), 1.0])
                glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.5, 2.5, 0.0])
                glEnable(GL_LIGHT0)
                glDisable(GL_LIGHT1)
            elif self.lighting_mode == "golden":
                # Sands of Time warm palace torchlight & amber mood
                glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [min(1.0, 0.45 * li), min(1.0, 0.38 * li), min(1.0, 0.26 * li), 1.0])
                glLightfv(GL_LIGHT0, GL_DIFFUSE, [min(1.0, 1.0 * li), min(1.0, 0.85 * li), min(1.0, 0.55 * li), 1.0])
                glLightfv(GL_LIGHT0, GL_POSITION, [1.5, 1.0, 2.0, 0.0])
                glEnable(GL_LIGHT0)
                glDisable(GL_LIGHT1)
            elif self.lighting_mode == "studio":
                # Studio Key + Fill for geometric clarity
                glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [min(1.0, 0.30 * li), min(1.0, 0.30 * li), min(1.0, 0.35 * li), 1.0])
                glLightfv(GL_LIGHT0, GL_DIFFUSE, [min(1.0, 0.95 * li), min(1.0, 0.95 * li), min(1.0, 0.95 * li), 1.0])
                glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.5, 2.5, 0.0])
                glEnable(GL_LIGHT0)
                glLightfv(GL_LIGHT1, GL_DIFFUSE, [min(1.0, 0.40 * li), min(1.0, 0.40 * li), min(1.0, 0.45 * li), 1.0])
                glLightfv(GL_LIGHT1, GL_POSITION, [-1.0, -1.0, 1.0, 0.0])
                glEnable(GL_LIGHT1)
            elif self.lighting_mode == "unlit":
                glDisable(GL_LIGHTING)
        else:
            glDisable(GL_LIGHTING)

        # Grid
        if self.show_grid:
            self._draw_grid()

        if self.level:
            # Wireframe polygon mode
            if self.show_wireframe:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

            # Draw level meshes
            if self.show_meshes:
                u_shift = 0.0
                v_shift = 0.0
                if self.animate_scene:
                    elapsed = time.time() - self.anim_start_time
                    u_shift = (elapsed * self.wind_speed_u) % 1.0
                    v_shift = (elapsed * self.wind_speed_v) % 1.0

                clip = self.active_clip
                frame_int = int(round(self.current_anim_frame)) if clip else 0
                clip_char = self._resolve_clip_character(clip) if clip else ""

                for obj in self.level.objects:
                    # Skip bone collision/proxy meshes so character models display cleanly
                    if obj.kind == "bone" or obj.name.startswith("B_"):
                        continue
                    # Skip parked pooled objects hidden at extreme depths (e.g. Z <= -20000)
                    if obj.position[2] <= -20000:
                        continue

                    mesh_keys = self.level.mesh_links.get(id(obj), [])
                    linked_meshes = [self.level.meshes[k] for k in mesh_keys if k in self.level.meshes]
                    if not linked_meshes:
                        continue
                    # Check if this object is a character or character accessory.
                    # Environmental props (trees, flags, banners, cloth, foliage) are strictly excluded.
                    is_character_part = any(
                        is_character_object(obj.name, m.object_name)
                        for m in linked_meshes
                    )

                    matches_clip = False
                    if clip and is_character_part:
                        obj_low = (obj.name or "").casefold()
                        mesh_low = " ".join((m.object_name or "") for m in linked_meshes).casefold()
                        combined = f"{obj_low} {mesh_low}"
                        if not clip_char:
                            matches_clip = True
                        elif clip_char == "prince":
                            matches_clip = "farah" not in combined and (
                                infer_character_group(combined) in ("", "prince")
                                or any(k in combined for k in ("plate_body", "legs", "sleeve", "pr_", "sword", "dagger", "arme"))
                            )
                        else:
                            matches_clip = clip_char in combined or infer_character_group(combined) == clip_char

                    # Only characters are deformed by skeletal animation tracks.
                    # Animation applies when playing or paused with active animation mode.
                    if clip is not None and is_character_part and matches_clip and (self.anim_playing or self.anim_mode_active):
                        anim_key = (clip.key, frame_int, id(obj))
                        cached_list = self._anim_display_lists.get(anim_key)
                        if cached_list is not None:
                            glCallList(cached_list)
                        else:
                            anim_list = glGenLists(1)
                            glNewList(anim_list, GL_COMPILE_AND_EXECUTE)
                            for mesh in linked_meshes:
                                world_verts = self._get_animated_vertices(mesh, clip, float(frame_int), obj)
                                normals = vertex_normals(world_verts, mesh.faces)
                                tex_map = self.level.texture_maps.get(mesh.key, {})
                                col_map = self.level.color_maps.get(mesh.key, {})
                                self._render_mesh_triangles(mesh, world_verts, normals, tex_map, col_map)
                            glEndList()
                            self._anim_display_lists[anim_key] = anim_list
                    else:
                        list_id = self.display_lists.get(id(obj))
                        if list_id is not None:
                            lower_name = obj.name.casefold()
                            is_env = any(s in lower_name for s in ("sky", "ciel", "cloud", "nuage", "wind", "vent", "eau", "water", "sand", "sable", "casc", "voile"))
                            if self.animate_scene and is_env:
                                glMatrixMode(GL_TEXTURE)
                                glPushMatrix()
                                glTranslatef(u_shift, v_shift, 0.0)
                                glMatrixMode(GL_MODELVIEW)

                            glCallList(list_id)

                            if self.animate_scene and is_env:
                                glMatrixMode(GL_TEXTURE)
                                glPopMatrix()
                                glMatrixMode(GL_MODELVIEW)

            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

            # Draw bones & character rigs
            if self.show_bones:
                self._draw_bones()

            # Draw markers & triggers
            if self.show_objects:
                for obj in self.level.objects:
                    if not self.level.mesh_links.get(id(obj)) and obj.kind != "bone":
                        self._draw_marker(obj)

            # Selection highlight
            if self.selected_object:
                self._draw_selection(self.selected_object)
                self._draw_gizmo(self.selected_object)

    def _draw_grid(self):
        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        glColor4f(0.25, 0.28, 0.35, 0.6)
        glLineWidth(1.0)

        step = 10.0
        limit = 100.0
        z = self.target[2]  # Draw grid at camera floor level or Z=0
        gz = 0.0 if abs(z) < 50.0 else round(z / 10.0) * 10.0

        glBegin(GL_LINES)
        for i in range(-10, 11):
            pos = i * step + self.target[0]
            pos = round(pos / step) * step
            glVertex3f(pos, self.target[1] - limit, gz)
            glVertex3f(pos, self.target[1] + limit, gz)

            pos_y = i * step + self.target[1]
            pos_y = round(pos_y / step) * step
            glVertex3f(self.target[0] - limit, pos_y, gz)
            glVertex3f(self.target[0] + limit, pos_y, gz)
        glEnd()

        if self.enable_lighting:
            glEnable(GL_LIGHTING)

    def _draw_marker(self, obj: LevelObject):
        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        x, y, z = obj.position

        corners = volume_corners(obj)
        if corners:
            color = volume_color(obj.name)
            glDepthMask(GL_FALSE)
            glColor4f(*color, 0.15)
            glBegin(GL_QUADS)
            for face in BOX_FACES:
                for idx in face:
                    glVertex3f(*corners[idx])
            glEnd()
            glDepthMask(GL_TRUE)

            glColor3f(*color)
            glLineWidth(1.5 if obj is self.selected_object else 1.0)
            glBegin(GL_LINES)
            for a, b in BOX_EDGES:
                glVertex3f(*corners[a])
                glVertex3f(*corners[b])
            glEnd()
        else:
            # Diamond marker
            s = max(0.5, self.distance * 0.015)
            if obj.kind == "light":
                glColor3f(1.0, 0.9, 0.2)
            elif obj.kind == "trigger":
                glColor3f(0.2, 0.8, 1.0)
            else:
                glColor3f(0.6, 0.7, 0.8)

            glBegin(GL_LINES)
            glVertex3f(x - s, y, z); glVertex3f(x + s, y, z)
            glVertex3f(x, y - s, z); glVertex3f(x, y + s, z)
            glVertex3f(x, y, z - s); glVertex3f(x, y, z + s)
            glEnd()

        if self.enable_lighting:
            glEnable(GL_LIGHTING)

    def _transform_rigid_accessory(
        self,
        mesh: MeshInfo,
        obj: LevelObject,
        master_anim: Dict[int, Any],
        body_obj: Optional[LevelObject],
    ) -> List[Tuple[float, float, float]]:
        """Keep modular accessories glued to the appropriate bone during animation."""
        rest_world = list(transformed_vertices(mesh.vertices, obj))
        if not rest_world or not master_anim:
            return rest_world
        body_matrix = object_world_matrix(body_obj) if body_obj is not None else None

        # 1. Check explicit bone mapping by accessory name tokens
        lower_name = f"{obj.name} {mesh.object_name or ''}".casefold()
        giz = None
        is_weapon = any(k in lower_name for k in ("sword", "dagger", "arme", "weapon", "blade"))
        is_bow = any(k in lower_name for k in ("_arc", "arc_", "m_arc", "b_arc", "bow"))
        is_arrow = any(k in lower_name for k in ("fleche", "arrow"))
        is_head = any(k in lower_name for k in ("hair", "cheveux", "face", "yeux", "eye", "head", "eyelid", "eyebrow", "jaw", "lips"))
        is_quiver = any(k in lower_name for k in ("carquois", "quiver"))

        is_farah = any("farah" in (o.name or "").casefold() for o in self.level.objects) if self.level else False

        if is_farah:
            if is_head:
                giz = 5   # Head
            elif is_bow:
                giz = 11  # L Hand
            elif is_arrow:
                giz = 21  # R Hand
            elif is_quiver:
                giz = 3   # Spine1
        else:
            if is_head:
                giz = 5   # Head
            elif is_weapon:
                giz = 19  # Right Hand
            elif is_quiver:
                giz = 3   # Spine2

        if giz is None or giz not in master_anim:
            giz = self._accessory_bone_cache.get(mesh.key)
            if giz not in master_anim:
                cx = sum(v[0] for v in rest_world) / len(rest_world)
                cy = sum(v[1] for v in rest_world) / len(rest_world)
                cz = sum(v[2] for v in rest_world) / len(rest_world)
                giz = pick_closest_gizmo((cx, cy, cz), master_anim, body_matrix)
                if giz is not None:
                    self._accessory_bone_cache[mesh.key] = giz

        pose = master_anim.get(giz) if giz is not None else None
        if not pose or len(pose) < 4 or pose[3] is None:
            return rest_world

        # For unattached weapons (like sword whose rest position was on the floor at (0.5, 0, 0)),
        # attach hilt directly to hand bone:
        if is_weapon or is_bow:
            hand_world = mul_matrix_col(body_matrix, pose[0]) if body_matrix is not None else pose[0]
            return [transform_point(hand_world, v) for v in mesh.vertices]

        return follow_bone_world_vertices(rest_world, pose[3], pose[0], body_matrix)

    def _draw_bones(self):
        """Render character skeletal bones and hierarchy linkages in 3D viewport."""
        if not self.level or not self.level.objects:
            return

        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)

        clip = self.active_clip
        if clip and (self.anim_playing or self.anim_mode_active):
            if any("farah" in (o.name or "").lower() for o in self.level.objects):
                target_char = "farah"
            elif any(any(k in (o.name or "").lower() for k in ("prince", "plate_body", "legs", "sleeve")) for o in self.level.objects):
                target_char = "prince"
            else:
                target_char = ""
            master_anim = self._get_skeleton_anim_poses(clip, self.current_anim_frame, target_char)
            if master_anim:
                char_pos = (0.0, 0.0, 0.0)
                for o in self.level.objects:
                    if o.kind == "bone" or o.name.startswith("B_") or o.position[2] <= -20000:
                        continue
                    low_o = (o.name or "").casefold()
                    if target_char == "farah" and "farah_body" in low_o:
                        char_pos = o.position
                        break
                    elif target_char == "prince" and any(k in low_o for k in ("plate_body", "corps", "body")) and "farah" not in low_o:
                        char_pos = o.position
                        break
                    elif not target_char and any(k in low_o for k in ("body", "corps", "root", "pelvis")):
                        char_pos = o.position
                        break

                s = max(0.04, min(0.25, self.distance * 0.006))
                glLineWidth(2.0)

                # 1. Draw joint crosses for all animated biped gizmos
                glBegin(GL_LINES)
                glColor3f(0.0, 0.9, 1.0)  # Bright cyan
                for giz, pose_data in master_anim.items():
                    gx, gy, gz = pose_data[1]
                    wx, wy, wz = char_pos[0] + gx, char_pos[1] + gy, char_pos[2] + gz
                    glVertex3f(wx - s, wy, wz); glVertex3f(wx + s, wy, wz)
                    glVertex3f(wx, wy - s, wz); glVertex3f(wx, wy + s, wz)
                    glVertex3f(wx, wy, wz - s); glVertex3f(wx, wy, wz + s)
                glEnd()

                # 2. Draw bone connection links between child and parent
                parents = character_bone_parents(self.level, clip, target_char)
                if not parents:
                    parents = get_biped_parents(target_char, len(master_anim))
                glColor4f(1.0, 0.8, 0.2, 0.85)  # Amber rig link
                glLineWidth(2.0)
                glBegin(GL_LINES)
                for giz, p in parents.items():
                    if giz in master_anim and p in master_anim:
                        gx, gy, gz = master_anim[giz][1]
                        px, py, pz = master_anim[p][1]
                        glVertex3f(char_pos[0] + gx, char_pos[1] + gy, char_pos[2] + gz)
                        glVertex3f(char_pos[0] + px, char_pos[1] + py, char_pos[2] + pz)
                glEnd()

                glLineWidth(1.0)
                if self.enable_lighting:
                    glEnable(GL_LIGHTING)
                return

        # Rest/unanimated mode: draw level bone objects
        bones = [o for o in self.level.objects if (o.kind == "bone" or o.name.startswith("B_") or "bone" in o.name.casefold()) and abs(o.position[2]) < 20000]
        if not bones:
            if self.enable_lighting:
                glEnable(GL_LIGHTING)
            return

        s = max(0.04, min(0.25, self.distance * 0.006))
        glLineWidth(2.0)

        # Draw joint nodes
        glBegin(GL_LINES)
        for b in bones:
            bx, by, bz = b.position
            # Draw joint cross
            if b is self.selected_object:
                glColor3f(1.0, 0.55, 0.05)
            else:
                glColor3f(0.0, 0.9, 1.0)  # Bright cyan
            glVertex3f(bx - s, by, bz); glVertex3f(bx + s, by, bz)
            glVertex3f(bx, by - s, bz); glVertex3f(bx, by + s, bz)
            glVertex3f(bx, by, bz - s); glVertex3f(bx, by + s, bz)
        glEnd()

        # 2. Draw bone connection links between logically related bones
        glColor4f(1.0, 0.8, 0.2, 0.85)  # Amber rig link
        glLineWidth(1.5)
        glBegin(GL_LINES)
        for i, b1 in enumerate(bones):
            p1 = b1.position
            b1_name = b1.name.casefold()
            for j, b2 in enumerate(bones):
                if i == j:
                    continue
                b2_name = b2.name.casefold()
                p2 = b2.position
                dist = math.dist(p1, p2)
                is_link = False
                if "_root" in b1_name and "_end" in b2_name and b1_name.replace("_root", "") == b2_name.replace("_end", ""):
                    is_link = True
                elif dist < 3.0 and dist > 0.02 and any(sub in b1_name and sub in b2_name for sub in ("spine", "arm", "leg", "hair", "hand", "foot", "head", "clavicle", "pelvis")):
                    is_link = True
                elif len(bones) < 80 and 0.05 < dist < 1.5:
                    is_link = True

                if is_link:
                    glVertex3f(*p1)
                    glVertex3f(*p2)
                    break
        glEnd()

        glLineWidth(1.0)
        if self.enable_lighting:
            glEnable(GL_LIGHTING)


    def _draw_selection(self, obj: LevelObject):
        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLineWidth(2.0)
        glColor3f(1.0, 0.55, 0.05)

        mesh_keys = self.level.mesh_links.get(id(obj), []) if self.level else []
        linked_meshes = [self.level.meshes[k] for k in mesh_keys if k in self.level.meshes] if self.level else []

        if linked_meshes:
            is_char = any(is_character_object(obj.name, m.object_name) for m in linked_meshes)
            clip = self.active_clip
            frame = self.current_anim_frame
            frame_int = int(round(frame))
            for mesh in linked_meshes:
                if clip is not None and is_char and (self.anim_playing or self.anim_mode_active):
                    world_verts = self._get_animated_vertices(mesh, clip, float(frame_int), obj)
                else:
                    world_verts = list(transformed_vertices(mesh.vertices, obj))
                glBegin(GL_TRIANGLES)
                for f in mesh.faces:
                    for vi in f:
                        glVertex3f(*world_verts[vi])
                glEnd()
        else:
            corners = volume_corners(obj)
            if corners:
                glBegin(GL_LINES)
                for a, b in BOX_EDGES:
                    glVertex3f(*corners[a])
                    glVertex3f(*corners[b])
                glEnd()

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glLineWidth(1.0)
        if self.enable_lighting:
            glEnable(GL_LIGHTING)

    # ================= 3D TRANSFORM MANIPULATION & GIZMO =================

    def set_transform_mode(self, mode: str):
        """Set active transformation tool mode ('select', 'translate', 'rotate', 'scale')."""
        self.transform_mode = mode
        self.active_axis = None
        self.hovered_axis = None
        self.unsetCursor()
        self.mode_changed.emit(mode)
        self.update()

    def set_move_whole_character(self, enable: bool):
        """Enable or disable linked transformation of whole character groups."""
        self.move_whole_character = enable

    def get_target_objects(self, obj: Optional[LevelObject] = None) -> List[LevelObject]:
        """Get all GameObjects affected by transform manipulation."""
        target = obj or self.selected_object
        if not target or not self.level:
            return []
        if not self.move_whole_character:
            return [target]

        low_name = target.name.casefold()
        if not is_character_object(target.name):
            return [target]

        # Identify character grouping keyword
        prefix = ""
        if "prince" in low_name or "pr_" in low_name:
            prefix = "prince"
        elif "farah" in low_name:
            prefix = "farah"
        elif "sandman" in low_name:
            prefix = "sandman"
        elif "sandguard" in low_name:
            prefix = "sandguard"
        elif "courtesan" in low_name:
            prefix = "courtesan"
        elif "pirate" in low_name:
            prefix = "pirate"
        elif "dahaka" in low_name:
            prefix = "dahaka"
        elif "crow" in low_name:
            prefix = "crow"
        elif "brute" in low_name:
            prefix = "brute"
        elif "act_" in low_name:
            parts = target.name.split("_")
            prefix = f"{parts[0]}_{parts[1]}".casefold() if len(parts) >= 2 else parts[0].casefold()

        if not prefix:
            return [target]

        group = []
        for o in self.level.objects:
            o_low = o.name.casefold()
            if prefix in o_low or (prefix == "prince" and any(k in o_low for k in ("pr_", "b_pr", "plate_body", "sleeve", "legs", "pr_face", "pr_hair", "sword01", "dagger"))):
                group.append(o)
        return group or [target]

    def update_object_display_list(self, obj: LevelObject):
        """Rebuild OpenGL display list for a transformed object."""
        if not self.level or not self.isValid():
            return
        self.makeCurrent()
        old_id = self.display_lists.get(id(obj))
        if old_id is not None:
            glDeleteLists(old_id, 1)
            del self.display_lists[id(obj)]

        mesh_keys = self.level.mesh_links.get(id(obj), [])
        linked_meshes = [self.level.meshes[k] for k in mesh_keys if k in self.level.meshes]
        if linked_meshes:
            list_id = glGenLists(1)
            glNewList(list_id, GL_COMPILE)
            for mesh in linked_meshes:
                world_verts = list(transformed_vertices(mesh.vertices, obj))
                normals = vertex_normals(world_verts, mesh.faces) if not mesh.normals else mesh.normals
                tex_map = self.level.texture_maps.get(mesh.key, {})
                col_map = self.level.color_maps.get(mesh.key, {})
                self._render_mesh_triangles(mesh, world_verts, normals, tex_map, col_map)
            glEndList()
            self.display_lists[id(obj)] = list_id
        self._anim_vertex_cache.clear()

    def update_objects_display_lists(self, objects: List[LevelObject]):
        """Rebuild OpenGL display lists for multiple transformed objects."""
        for o in objects:
            self.update_object_display_list(o)
        self.update()

    def set_selected_object_transform(
        self,
        pos: Optional[Tuple[float, float, float]] = None,
        rot: Optional[Tuple[float, float, float]] = None,
        scale: Optional[Tuple[float, float, float]] = None,
    ):
        """Explicitly set transform values from the inspector panel."""
        if not self.selected_object:
            return

        target_objs = self.get_target_objects(self.selected_object)
        old_pos = self.selected_object.position
        old_rot = self.selected_object.rotation
        old_scale = self.selected_object.scale

        delta_pos = (pos[0] - old_pos[0], pos[1] - old_pos[1], pos[2] - old_pos[2]) if pos is not None else (0.0, 0.0, 0.0)
        delta_rot = (rot[0] - old_rot[0], rot[1] - old_rot[1], rot[2] - old_rot[2]) if rot is not None else (0.0, 0.0, 0.0)

        for o in target_objs:
            if pos is not None:
                o.position = (o.position[0] + delta_pos[0], o.position[1] + delta_pos[1], o.position[2] + delta_pos[2])
            if rot is not None:
                o.rotation = (o.rotation[0] + delta_rot[0], o.rotation[1] + delta_rot[1], o.rotation[2] + delta_rot[2])
            if scale is not None:
                if o is self.selected_object:
                    o.scale = scale
                else:
                    rx = scale[0] / max(1e-4, old_scale[0])
                    ry = scale[1] / max(1e-4, old_scale[1])
                    rz = scale[2] / max(1e-4, old_scale[2])
                    o.scale = (o.scale[0] * rx, o.scale[1] * ry, o.scale[2] * rz)

        self.update_objects_display_lists(target_objs)
        self.transform_changed.emit(self.selected_object)
        self.update()

    def pick_object_at(self, mx: int, my: int) -> Optional[LevelObject]:
        """Cast 3D ray through viewport pixel to pick and select a scene object or character."""
        if not self.level or not self.level.objects or not self.isValid():
            return None

        self.makeCurrent()
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)

        gl_y = viewport[3] - my
        try:
            p_near = gluUnProject(mx, gl_y, 0.0, modelview, projection, viewport)
            p_far = gluUnProject(mx, gl_y, 1.0, modelview, projection, viewport)
        except Exception:
            return None

        ro = np.array(p_near, dtype=np.float64)
        rd = np.array(p_far, dtype=np.float64) - ro
        norm = np.linalg.norm(rd)
        if norm == 0:
            return None
        rd /= norm

        best_hit = None
        best_score = (99, float("inf"), float("inf"))

        for obj in self.level.objects:
            if obj.position[2] <= -20000:
                continue

            cx, cy, cz = obj.position
            has_bounds = (
                obj.bounds
                and len(obj.bounds) == 6
                and all(math.isfinite(b) for b in obj.bounds)
            )
            if has_bounds:
                min_x, min_y, min_z, max_x, max_y, max_z = obj.bounds
                bx = max(abs(max_x - min_x) * 0.5, 0.4)
                by = max(abs(max_y - min_y) * 0.5, 0.4)
                bz = max(abs(max_z - min_z) * 0.5, 0.4)
                box_cx = (min_x + max_x) * 0.5
                box_cy = (min_y + max_y) * 0.5
                box_cz = (min_z + max_z) * 0.5
                center = np.array([cx + box_cx, cy + box_cy, cz + box_cz], dtype=np.float64)
                radius = max(math.sqrt(bx * bx + by * by + bz * bz), 1.0)
            elif self.level.mesh_links.get(id(obj)):
                center = np.array([cx, cy, cz], dtype=np.float64)
                radius = 2.5
            elif obj.kind == "bone":
                center = np.array([cx, cy, cz], dtype=np.float64)
                radius = 0.6
            else:
                center = np.array([cx, cy, cz], dtype=np.float64)
                radius = 1.0

            is_char = is_character_object(obj.name)
            is_env = radius >= 15.0 or is_environment_prop(obj.name)
            cat = 0 if is_char else (2 if is_env else 1)

            # Test ray against geometry bounding sphere
            v = center - ro
            t_proj = float(np.dot(v, rd))
            if t_proj > 0:
                d_sq = float(np.dot(v, v) - t_proj * t_proj)
                eff_radius = max(radius, 0.8)
                if d_sq <= eff_radius * eff_radius:
                    t_hit = t_proj - math.sqrt(max(0.0, eff_radius * eff_radius - d_sq))
                    score = (cat, d_sq / (eff_radius * eff_radius), t_hit)
                    if score < best_score:
                        best_score = score
                        best_hit = obj
                        continue

            # Also test direct pivot point (for bones, markers, lights)
            v_pivot = np.array([cx, cy, cz], dtype=np.float64) - ro
            t_pivot = float(np.dot(v_pivot, rd))
            if t_pivot > 0:
                d_sq_p = float(np.dot(v_pivot, v_pivot) - t_pivot * t_pivot)
                if d_sq_p <= 1.44:
                    t_hit_p = t_pivot - math.sqrt(max(0.0, 1.44 - d_sq_p))
                    score_p = (cat, d_sq_p / 1.44, t_hit_p)
                    if score_p < best_score:
                        best_score = score_p
                        best_hit = obj

        return best_hit

    def hit_test_gizmo(self, mx: int, my: int) -> Optional[str]:
        """Test if screen coordinate (mx, my) is hovering over a gizmo axis or handle."""
        if not self.selected_object or not self.isValid() or self.transform_mode == "select":
            return None

        self.makeCurrent()
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)

        cx, cy, cz = self.selected_object.position
        length = max(1.5, self.distance * 0.12)

        try:
            c_proj = gluProject(cx, cy, cz, modelview, projection, viewport)
        except Exception:
            return None
        c_sx, c_sy = c_proj[0], viewport[3] - c_proj[1]

        # Check center handle
        if math.hypot(mx - c_sx, my - c_sy) <= 15.0:
            return "CENTER"

        if self.transform_mode in ("translate", "scale"):
            def _pt_seg_dist(px, py, ax, ay, bx, by):
                abx, aby = bx - ax, by - ay
                apx, apy = px - ax, py - ay
                ab_sq = abx * abx + aby * aby
                if ab_sq == 0:
                    return math.hypot(apx, apy)
                t = max(0.0, min(1.0, (apx * abx + apy * aby) / ab_sq))
                return math.hypot(px - (ax + t * abx), py - (ay + t * aby))

            # X axis
            try:
                x_proj = gluProject(cx + length, cy, cz, modelview, projection, viewport)
                x_sx, x_sy = x_proj[0], viewport[3] - x_proj[1]
                dist_x = _pt_seg_dist(mx, my, c_sx, c_sy, x_sx, x_sy)
            except Exception:
                dist_x = float("inf")

            # Y axis
            try:
                y_proj = gluProject(cx, cy + length, cz, modelview, projection, viewport)
                y_sx, y_sy = y_proj[0], viewport[3] - y_proj[1]
                dist_y = _pt_seg_dist(mx, my, c_sx, c_sy, y_sx, y_sy)
            except Exception:
                dist_y = float("inf")

            # Z axis
            try:
                z_proj = gluProject(cx, cy, cz + length, modelview, projection, viewport)
                z_sx, z_sy = z_proj[0], viewport[3] - z_proj[1]
                dist_z = _pt_seg_dist(mx, my, c_sx, c_sy, z_sx, z_sy)
            except Exception:
                dist_z = float("inf")

            candidates = [("X", dist_x), ("Y", dist_y), ("Z", dist_z)]
            candidates.sort(key=lambda item: item[1])
            if candidates[0][1] <= 16.0:
                return candidates[0][0]

        elif self.transform_mode == "rotate":
            radius = length * 0.95
            rings = [("X", (0, 1, 2)), ("Y", (1, 0, 2)), ("Z", (2, 0, 1))]
            best_ring = None
            min_ring_dist = float("inf")

            for axis_name, (fixed, a1, a2) in rings:
                pts_screen = []
                for i in range(24):
                    ang = i * (2.0 * math.pi / 24.0)
                    offset = [0.0, 0.0, 0.0]
                    offset[a1] = radius * math.cos(ang)
                    offset[a2] = radius * math.sin(ang)
                    try:
                        p = gluProject(cx + offset[0], cy + offset[1], cz + offset[2], modelview, projection, viewport)
                        pts_screen.append((p[0], viewport[3] - p[1]))
                    except Exception:
                        pass
                for i in range(len(pts_screen)):
                    p1 = pts_screen[i]
                    p2 = pts_screen[(i + 1) % len(pts_screen)]
                    abx, aby = p2[0] - p1[0], p2[1] - p1[1]
                    apx, apy = mx - p1[0], my - p1[1]
                    ab_sq = abx * abx + aby * aby
                    if ab_sq > 0:
                        t = max(0.0, min(1.0, (apx * abx + apy * aby) / ab_sq))
                        d = math.hypot(mx - (p1[0] + t * abx), my - (p1[1] + t * aby))
                        if d < min_ring_dist:
                            min_ring_dist = d
                            best_ring = axis_name

            if min_ring_dist <= 16.0:
                return best_ring

        return None

    def _handle_gizmo_drag(self, dx: int, dy: int):
        """Compute and apply transform deltas during interactive mouse drag on gizmo."""
        if not self.selected_object or not self.active_axis:
            return

        target_objs = self.get_target_objects(self.selected_object)
        if not target_objs:
            return

        cx, cy, cz = self.selected_object.position
        length = max(1.5, self.distance * 0.12)

        if self.transform_mode == "translate":
            factor = max(0.01, self.distance * 0.002)
            if self.active_axis == "CENTER":
                # Screen-space translation
                c_yaw, s_yaw = math.cos(self.yaw), math.sin(self.yaw)
                right = np.array([-s_yaw, c_yaw, 0.0])
                up = np.array([-math.sin(self.pitch) * c_yaw, -math.sin(self.pitch) * s_yaw, math.cos(self.pitch)])
                delta = (dx * right - dy * up) * factor
            else:
                axis_vec = [0.0, 0.0, 0.0]
                if self.active_axis == "X":
                    axis_vec[0] = 1.0
                elif self.active_axis == "Y":
                    axis_vec[1] = 1.0
                elif self.active_axis == "Z":
                    axis_vec[2] = 1.0

                v_len = 50.0
                try:
                    self.makeCurrent()
                    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
                    projection = glGetDoublev(GL_PROJECTION_MATRIX)
                    viewport = glGetIntegerv(GL_VIEWPORT)
                    c_p = gluProject(cx, cy, cz, modelview, projection, viewport)
                    a_p = gluProject(cx + axis_vec[0] * length, cy + axis_vec[1] * length, cz + axis_vec[2] * length, modelview, projection, viewport)
                    v_screen = (a_p[0] - c_p[0], -(a_p[1] - c_p[1]))
                    v_len = math.hypot(v_screen[0], v_screen[1])
                    if v_len > 1e-4:
                        proj = (dx * v_screen[0] + dy * v_screen[1]) / v_len
                    else:
                        proj = dx - dy
                except Exception:
                    proj = dx - dy

                dist_world = proj * (length / max(30.0, v_len))
                delta = [axis_vec[i] * dist_world for i in range(3)]

            for o in target_objs:
                init_pos = self.drag_start_transforms.get(id(o), (o.position, o.rotation, o.scale))[0]
                o.position = (init_pos[0] + delta[0], init_pos[1] + delta[1], init_pos[2] + delta[2])

        elif self.transform_mode == "rotate":
            deg = (dx - dy) * 0.7
            delta_rot = [0.0, 0.0, 0.0]
            if self.active_axis == "X":
                delta_rot[0] = deg
            elif self.active_axis == "Y":
                delta_rot[1] = deg
            elif self.active_axis == "Z":
                delta_rot[2] = deg
            else:
                delta_rot[2] = deg

            for o in target_objs:
                init_rot = self.drag_start_transforms.get(id(o), (o.position, o.rotation, o.scale))[1]
                o.rotation = (
                    (init_rot[0] + delta_rot[0]) % 360.0,
                    (init_rot[1] + delta_rot[1]) % 360.0,
                    (init_rot[2] + delta_rot[2]) % 360.0,
                )

        elif self.transform_mode == "scale":
            drag = (dx - dy) * 0.015
            factor = max(0.01, 1.0 + drag)
            scale_mult = [1.0, 1.0, 1.0]
            if self.active_axis == "CENTER":
                scale_mult = [factor, factor, factor]
            elif self.active_axis == "X":
                scale_mult[0] = factor
            elif self.active_axis == "Y":
                scale_mult[1] = factor
            elif self.active_axis == "Z":
                scale_mult[2] = factor

            for o in target_objs:
                init_scale = self.drag_start_transforms.get(id(o), (o.position, o.rotation, o.scale))[2]
                o.scale = (
                    max(0.001, init_scale[0] * scale_mult[0]),
                    max(0.001, init_scale[1] * scale_mult[1]),
                    max(0.001, init_scale[2] * scale_mult[2]),
                )

        self.update_objects_display_lists(target_objs)
        self.transform_changed.emit(self.selected_object)

    def _draw_cone_head(self, x: float, y: float, z: float, axis: str, size: float):
        w = size * 0.35
        glBegin(GL_TRIANGLES)
        if axis == "X":
            b = x - size
            base = [(b, y - w, z - w), (b, y + w, z - w), (b, y + w, z + w), (b, y - w, z + w)]
            for i in range(4):
                glVertex3f(x, y, z); glVertex3f(*base[i]); glVertex3f(*base[(i + 1) % 4])
        elif axis == "Y":
            b = y - size
            base = [(x - w, b, z - w), (x + w, b, z - w), (x + w, b, z + w), (x - w, b, z + w)]
            for i in range(4):
                glVertex3f(x, y, z); glVertex3f(*base[i]); glVertex3f(*base[(i + 1) % 4])
        else:
            b = z - size
            base = [(x - w, y - w, b), (x + w, y - w, b), (x + w, y + w, b), (x - w, y + w, b)]
            for i in range(4):
                glVertex3f(x, y, z); glVertex3f(*base[i]); glVertex3f(*base[(i + 1) % 4])
        glEnd()

    def _draw_cube(self, x: float, y: float, z: float, size: float):
        s = size * 0.5
        glBegin(GL_QUADS)
        # Front
        glVertex3f(x - s, y - s, z + s); glVertex3f(x + s, y - s, z + s); glVertex3f(x + s, y + s, z + s); glVertex3f(x - s, y + s, z + s)
        # Back
        glVertex3f(x - s, y - s, z - s); glVertex3f(x - s, y + s, z - s); glVertex3f(x + s, y + s, z - s); glVertex3f(x + s, y - s, z - s)
        # Top
        glVertex3f(x - s, y + s, z - s); glVertex3f(x - s, y + s, z + s); glVertex3f(x + s, y + s, z + s); glVertex3f(x + s, y + s, z - s)
        # Bottom
        glVertex3f(x - s, y - s, z - s); glVertex3f(x + s, y - s, z - s); glVertex3f(x + s, y - s, z + s); glVertex3f(x - s, y - s, z + s)
        # Right
        glVertex3f(x + s, y - s, z - s); glVertex3f(x + s, y + s, z - s); glVertex3f(x + s, y + s, z + s); glVertex3f(x + s, y - s, z + s)
        # Left
        glVertex3f(x - s, y - s, z - s); glVertex3f(x - s, y - s, z + s); glVertex3f(x - s, y + s, z + s); glVertex3f(x - s, y + s, z - s)
        glEnd()

    def _draw_gizmo(self, obj: LevelObject):
        """Draw interactive 3D transformation gizmo (Translate, Rotate, Scale)."""
        if self.transform_mode == "select":
            return

        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)

        cx, cy, cz = obj.position
        length = max(1.5, self.distance * 0.12)
        head = length * 0.22

        # Colors
        col_x = (1.0, 0.9, 0.1) if self.hovered_axis == "X" or self.active_axis == "X" else (1.0, 0.25, 0.25)
        col_y = (1.0, 0.9, 0.1) if self.hovered_axis == "Y" or self.active_axis == "Y" else (0.25, 0.95, 0.3)
        col_z = (1.0, 0.9, 0.1) if self.hovered_axis == "Z" or self.active_axis == "Z" else (0.3, 0.6, 1.0)
        col_c = (1.0, 0.9, 0.1) if self.hovered_axis == "CENTER" or self.active_axis == "CENTER" else (0.9, 0.9, 0.9)

        if self.transform_mode == "translate":
            # Center handle
            glColor3f(*col_c)
            glPointSize(8.0)
            glBegin(GL_POINTS)
            glVertex3f(cx, cy, cz)
            glEnd()

            glLineWidth(3.5)

            # X Axis
            glColor3f(*col_x)
            glBegin(GL_LINES)
            glVertex3f(cx, cy, cz); glVertex3f(cx + length, cy, cz)
            glEnd()
            self._draw_cone_head(cx + length, cy, cz, "X", head)

            # Y Axis
            glColor3f(*col_y)
            glBegin(GL_LINES)
            glVertex3f(cx, cy, cz); glVertex3f(cx, cy + length, cz)
            glEnd()
            self._draw_cone_head(cx, cy + length, cz, "Y", head)

            # Z Axis
            glColor3f(*col_z)
            glBegin(GL_LINES)
            glVertex3f(cx, cy, cz); glVertex3f(cx, cy, cz + length)
            glEnd()
            self._draw_cone_head(cx, cy, cz + length, "Z", head)

        elif self.transform_mode == "rotate":
            radius = length * 0.95
            glLineWidth(3.0)

            # Pitch (X Axis - YZ plane)
            glColor3f(*col_x)
            glBegin(GL_LINE_LOOP)
            for i in range(36):
                ang = i * (2.0 * math.pi / 36.0)
                glVertex3f(cx, cy + radius * math.cos(ang), cz + radius * math.sin(ang))
            glEnd()

            # Roll (Y Axis - XZ plane)
            glColor3f(*col_y)
            glBegin(GL_LINE_LOOP)
            for i in range(36):
                ang = i * (2.0 * math.pi / 36.0)
                glVertex3f(cx + radius * math.cos(ang), cy, cz + radius * math.sin(ang))
            glEnd()

            # Yaw (Z Axis - XY plane)
            glColor3f(*col_z)
            glBegin(GL_LINE_LOOP)
            for i in range(36):
                ang = i * (2.0 * math.pi / 36.0)
                glVertex3f(cx + radius * math.cos(ang), cy + radius * math.sin(ang), cz)
            glEnd()

        elif self.transform_mode == "scale":
            # Center uniform cube
            glColor3f(*col_c)
            self._draw_cube(cx, cy, cz, head * 0.6)

            glLineWidth(3.5)

            # X Axis
            glColor3f(*col_x)
            glBegin(GL_LINES)
            glVertex3f(cx, cy, cz); glVertex3f(cx + length, cy, cz)
            glEnd()
            self._draw_cube(cx + length, cy, cz, head * 0.5)

            # Y Axis
            glColor3f(*col_y)
            glBegin(GL_LINES)
            glVertex3f(cx, cy, cz); glVertex3f(cx, cy + length, cz)
            glEnd()
            self._draw_cube(cx, cy + length, cz, head * 0.5)

            # Z Axis
            glColor3f(*col_z)
            glBegin(GL_LINES)
            glVertex3f(cx, cy, cz); glVertex3f(cx, cy, cz + length)
            glEnd()
            self._draw_cube(cx, cy, cz + length, head * 0.5)

        glEnable(GL_DEPTH_TEST)
        glLineWidth(1.0)
        if self.enable_lighting:
            glEnable(GL_LIGHTING)

    # --- Mouse & Navigation Controls ---

    def mousePressEvent(self, event):
        self.last_pos = event.pos()
        is_alt = bool(event.modifiers() & Qt.AltModifier)

        # 1. Alt + Left Mouse: Rotate / Orbit Camera Scene
        #    Alt + Right Mouse: Move / Pan Camera Scene
        if is_alt:
            if event.button() == Qt.LeftButton:
                self.is_orbiting = True
                self.is_panning = False
                return
            elif event.button() == Qt.RightButton:
                self.is_panning = True
                self.is_orbiting = False
                return

        # 2. Middle Mouse or Shift + Left: Pan camera scene
        if (event.buttons() & Qt.MiddleButton) or (
            (event.buttons() & Qt.LeftButton) and (event.modifiers() & Qt.ShiftModifier)
        ):
            self.is_panning = True
            self.is_orbiting = False
            return

        # 3. Regular Left Click (without Alt):
        if event.button() == Qt.LeftButton:
            # 3A. Test clicking on interactive gizmo handle
            if self.selected_object and self.transform_mode != "select":
                axis = self.hit_test_gizmo(event.pos().x(), event.pos().y())
                if axis:
                    self.is_transforming = True
                    self.active_axis = axis
                    self.drag_start_screen = event.pos()
                    target_objs = self.get_target_objects(self.selected_object)
                    self.drag_start_transforms = {
                        id(o): (o.position, o.rotation, o.scale) for o in target_objs
                    }
                    self.update()
                    return

            # 3B. Click on any object or character in the scene to select it
            hit_obj = self.pick_object_at(event.pos().x(), event.pos().y())
            if hit_obj is not None:
                self.selected_object = hit_obj
                if self.transform_mode == "select":
                    self.transform_mode = "translate"
                self.object_selected.emit(hit_obj)
                self.clicked_on_object = True
                self.update()
                return
            else:
                self.clicked_on_object = False

        elif event.button() == Qt.RightButton:
            # Right click without Alt: zoom drag preparation
            pass

    def mouseMoveEvent(self, event):
        # 1. Active Gizmo Drag
        if self.is_transforming and self.selected_object and self.drag_start_screen:
            dx = event.pos().x() - self.drag_start_screen.x()
            dy = event.pos().y() - self.drag_start_screen.y()
            self._handle_gizmo_drag(dx, dy)
            self.update()
            return

        # 2. Gizmo Hover test (when not holding mouse buttons)
        if not event.buttons():
            if self.selected_object and self.transform_mode != "select":
                hovered = self.hit_test_gizmo(event.pos().x(), event.pos().y())
                if hovered != self.hovered_axis:
                    self.hovered_axis = hovered
                    if hovered:
                        self.setCursor(Qt.SizeAllCursor if self.transform_mode == "translate" else Qt.CrossCursor)
                    else:
                        self.unsetCursor()
                    self.update()
            return

        if self.last_pos is None:
            return

        dx = event.pos().x() - self.last_pos.x()
        dy = event.pos().y() - self.last_pos.y()
        self.last_pos = event.pos()

        is_alt = bool(event.modifiers() & Qt.AltModifier)

        # Alt + Right Mouse OR Middle Mouse: Move / Pan camera scene
        if (is_alt and (event.buttons() & Qt.RightButton)) or self.is_panning or (event.buttons() & Qt.MiddleButton):
            cy, sy = math.cos(self.yaw), math.sin(self.yaw)
            right = [-sy, cy, 0.0]
            up = [-math.sin(self.pitch) * cy, -math.sin(self.pitch) * sy, math.cos(self.pitch)]
            scale = max(0.01, self.distance * 0.0015)
            self.target[0] -= (dx * right[0] - dy * up[0]) * scale
            self.target[1] -= (dx * right[1] - dy * up[1]) * scale
            self.target[2] -= (dx * right[2] - dy * up[2]) * scale
            self.update()
        # Alt + Left Mouse OR Left Drag on empty background: Rotate / Orbit camera scene
        elif (is_alt and (event.buttons() & Qt.LeftButton)) or self.is_orbiting or ((event.buttons() & Qt.LeftButton) and not getattr(self, 'clicked_on_object', False)):
            self.yaw -= dx * 0.008
            self.pitch = max(-math.pi / 2 + 0.05, min(math.pi / 2 - 0.05, self.pitch + dy * 0.008))
            self.update()
        # Right Button without Alt: Right drag zoom
        elif (event.buttons() & Qt.RightButton) and not is_alt:
            self.distance = max(1.0, self.distance * (1.0 + dy * 0.005))
            self.update()

    def mouseReleaseEvent(self, event):
        if self.is_transforming:
            self.is_transforming = False
            self.active_axis = None
            self.drag_start_screen = None
            self.drag_start_transforms.clear()
            if self.selected_object:
                target_objs = self.get_target_objects(self.selected_object)
                self.update_objects_display_lists(target_objs)
                self.transform_changed.emit(self.selected_object)
            self.unsetCursor()
            self.update()

        self.last_pos = None
        self.is_panning = False
        self.is_orbiting = False
        self.clicked_on_object = False

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        factor = 0.9 if delta > 0 else 1.1
        self.distance = max(1.0, self.distance * factor)
        self.update()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Alt:
            event.accept()
            return

        # Transform Gizmo Mode Hotkeys
        if key == Qt.Key_1:
            self.set_transform_mode("select")
            return
        elif key == Qt.Key_2 or key == Qt.Key_G or key == Qt.Key_T:
            self.set_transform_mode("translate")
            return
        elif key == Qt.Key_3:
            self.set_transform_mode("rotate")
            return
        elif key == Qt.Key_4:
            self.set_transform_mode("scale")
            return

        speed = max(1.0, self.distance * 0.05)
        cy, sy = math.cos(self.yaw), math.sin(self.yaw)
        forward = [-cy, -sy, 0.0]
        right = [-sy, cy, 0.0]

        if key == Qt.Key_W:
            self.target[0] += forward[0] * speed
            self.target[1] += forward[1] * speed
            self.update()
        elif key == Qt.Key_S:
            self.target[0] -= forward[0] * speed
            self.target[1] -= forward[1] * speed
            self.update()
        elif key == Qt.Key_A:
            self.target[0] -= right[0] * speed
            self.target[1] -= right[1] * speed
            self.update()
        elif key == Qt.Key_D:
            self.target[0] += right[0] * speed
            self.target[1] += right[1] * speed
            self.update()
        elif key == Qt.Key_Q:
            self.target[2] -= speed
            self.update()
        elif key == Qt.Key_E:
            self.target[2] += speed
            self.update()
        elif key == Qt.Key_F or key == Qt.Key_R:
            self.frame_level()
            self.update()
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Alt:
            event.accept()
            return
        super().keyReleaseEvent(event)
