"""High-level level loader that resolves WOL level scenes, WOW rooms, meshes, materials, and textures."""
from __future__ import annotations

from pathlib import Path
import struct
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from .bf_parser import BFArchive
from .level_scene import level_asset_kind, scan_level_objects, wol_wow_keys
from .materials import associate_mesh_material_packs, jade_color_rgba, scan_pop_material_records, scan_pop_materials
from .mesh_parser import scan_pop_meshes
from .models import BigFileEntry, LevelObject, LevelSceneData, MeshInfo, PopFileEntry, TextureInfo
from .resources import parse_pop_file_entries
from .animations import scan_animations, tag_animation_clips
from .textures import decode_pop_texture_image, scan_pop_textures, get_pop_texture_original_blob
from .lzo import decompress_pop_lzo, looks_like_pop_lzo
from .ai_decompiler import scan_ai_scripts_from_payload


def resolve_object_mesh_links(
    local_objects: List[LevelObject],
    mesh_keys: Set[int],
    entries_by_key: Dict[int, PopFileEntry],
    payload: bytes
) -> Dict[int, List[int]]:
    """Resolve each GameObject to its appropriate Mesh key(s), selecting LOD 0 for LOD groups."""
    all_mesh_links: Dict[int, List[int]] = {}
    for obj in local_objects:
        links: List[int] = []
        if obj.mesh_key is not None and obj.mesh_key in mesh_keys:
            links = [obj.mesh_key]
        elif obj.mesh_key is not None and obj.mesh_key in entries_by_key:
            group = entries_by_key[obj.mesh_key]
            group_data = payload[group.data_offset:group.data_offset + group.size]
            type_id = struct.unpack_from("<I", group_data, 0)[0] if len(group_data) >= 4 else 0

            # Collect referenced mesh keys preserving their sequential order
            ordered_keys: List[int] = []
            for i in range(0, len(group_data) - 4):
                val = struct.unpack_from("<I", group_data, i)[0]
                if val in mesh_keys and val not in ordered_keys:
                    ordered_keys.append(val)

            # In Jade Engine GRO_tdst_LOD (type 8), dpst_Id[0] is the primary base mesh.
            # Never render distance/bind-pose LODs simultaneously with the primary mesh.
            if type_id == 8 and ordered_keys:
                links = [ordered_keys[0]]
            else:
                links = ordered_keys
        all_mesh_links[id(obj)] = links
    return all_mesh_links


def align_character_head_objects(objects: List[LevelObject]):
    """Align modular character head, face, and shoulder objects to their proper body height."""
    for obj in objects:
        lower = obj.name.casefold()
        dist_sq = obj.position[0] ** 2 + obj.position[1] ** 2 + obj.position[2] ** 2
        # Prince face & hair: modeled at local (0, 0, 0), attaches to head bone at Z=1.6375m
        if lower in ("m_pr_face.gao", "pr_face.gao", "m_prince_hair.gao", "pr_hair.gao"):
            if dist_sq < 0.05:
                obj.position = (0.0, -0.0165, 1.6375)
        # Prince shoulder armor plates: modeled at local (0, 0, 0), attach to shoulders at Z=1.55m
        elif lower in ("m_prince_plate_shoulder_left.gao", "m_prince_plate_shoulder_right.gao"):
            if dist_sq < 0.05:
                obj.position = (0.0, 0.0, 1.55)
        # Farah face: modeled at local (0, 0, 0), attaches to Farah head bone at Z=1.54m
        elif lower in ("farah_face.gao", "m_farah_face.gao"):
            if dist_sq < 0.05:
                obj.position = (0.0, 0.0, 1.54)
        # Prince veil / sash: modeled around local (0, 0, 0), attaches to belt/pelvis at waist level (Z=1.0588m)
        elif "veil" in lower or "voile" in lower:
            if abs(obj.position[2] - 1.6375) < 0.1 or dist_sq < 0.05:
                obj.position = (0.0, 0.0, 1.0588)


def load_level_from_archive(
    archive: BFArchive,
    target_entry: BigFileEntry,
    progress_callback: Optional[Callable[[str], None]] = None,
    selected_costume_key: Optional[int] = None
) -> LevelSceneData:
    """Load a 3D level (WOL world or WOW room) from a BigFile archive with all textures and materials."""
    if progress_callback:
        progress_callback(f"Opening {target_entry.name}...")

    is_wol = level_asset_kind(target_entry.name) == "wol"
    sources: List[BigFileEntry] = [target_entry]

    if is_wol:
        wol_data = archive.read_entry(target_entry)
        wanted_keys = wol_wow_keys(wol_data)
        wanted_low16 = {k & 0xFFFF for k in wanted_keys}

        # Find all corresponding WOW entries in archive
        wow_matches = [
            e for e in archive.entries
            if level_asset_kind(e.name) == "wow" and ((e.key & 0xFFFF) in wanted_low16 or e.key in wanted_keys)
        ]
        if progress_callback:
            progress_callback(f"WOL links to {len(wow_matches)} room/character assets...")
        sources.extend(wow_matches)
    else:
        # Check if loading a character or modular costume WOW (e.g. Prince_wow or PrinceCostume)
        target_lower = target_entry.name.casefold()
        if "prince_wow" in target_lower or "prince_for_load_wow" in target_lower:
            costumes = [e for e in archive.entries if "princecostume" in e.name.casefold() and e.key != target_entry.key]
            costumes.sort(key=lambda e: e.name.casefold())
            chosen_costume = None
            if selected_costume_key:
                chosen_costume = next((c for c in costumes if c.key == selected_costume_key), None)
            if not chosen_costume and costumes:
                chosen_costume = costumes[0]
            if chosen_costume:
                sources.append(chosen_costume)
            weapons = [
                e for e in archive.entries
                if any(w in e.name.casefold() for w in ("prince_sword01_wow", "prince_sword02_wow", "prince_weapons_wow"))
                and e.key != target_entry.key
            ]
            weapons.sort(key=lambda e: e.name.casefold())
            if weapons:
                sources.append(weapons[0])
            if progress_callback:
                progress_callback(f"Character companion: added costume {sources[1].name if len(sources) > 1 else ''}...")
        elif "princecostume" in target_lower:
            prince_roots = [e for e in archive.entries if ("prince_wow" in e.name.casefold() or "prince_for_load_wow" in e.name.casefold()) and e.key != target_entry.key]
            if prince_roots:
                sources.append(prince_roots[0])
            weapons = [
                e for e in archive.entries
                if any(w in e.name.casefold() for w in ("prince_sword01_wow", "prince_sword02_wow", "prince_weapons_wow"))
                and e.key != target_entry.key
            ]
            weapons.sort(key=lambda e: e.name.casefold())
            if weapons:
                sources.append(weapons[0])
            if progress_callback:
                progress_callback(f"Character companion: added base skeleton & head {prince_roots[0].name if prince_roots else ''}...")

    all_objects: List[LevelObject] = []
    all_meshes: Dict[int, MeshInfo] = {}
    all_images: Dict[int, object] = {}  # key -> PIL.Image
    all_tex_infos: Dict[int, TextureInfo] = {}
    all_original_blobs: Dict[int, Tuple[bytes, str]] = {}
    all_tex_sources: Dict[int, str] = {}
    all_texture_maps: Dict[int, Dict[int, int]] = {}  # mesh_key -> {mat_id: tex_key}
    all_color_maps: Dict[int, Dict[int, Tuple[float, float, float, float]]] = {}  # mesh_key -> {mat_id: rgba}
    all_mesh_links: Dict[int, List[int]] = {}  # id(obj) -> [mesh_keys]
    all_clips: List[object] = []
    all_ai_scripts: List[Dict[str, Any]] = []
    wanted_missing_textures: Set[int] = set()

    for idx, source in enumerate(sources):
        if progress_callback:
            progress_callback(f"Loading {source.name} ({idx + 1}/{len(sources)})...")

        payload = archive.read_entry(source)
        local_objects = scan_level_objects(payload, source.index)
        local_meshes = scan_pop_meshes(payload)
        associate_mesh_material_packs(payload, local_meshes)
        local_clips = scan_animations(payload)
        tag_animation_clips(local_clips, source.name, local_objects)
        all_clips.extend(local_clips)
        all_ai_scripts.extend(scan_ai_scripts_from_payload(payload, source_name=source.name))

        mesh_keys = {m.key for m in local_meshes}
        entries = parse_pop_file_entries(payload)
        entries_by_key = {entry.key: entry for entry in entries}

        # Resolve object -> mesh links with LOD 0 selection
        links_for_local = resolve_object_mesh_links(local_objects, mesh_keys, entries_by_key, payload)
        all_mesh_links.update(links_for_local)

        all_objects.extend(local_objects)
        for m in local_meshes:
            all_meshes[m.key] = m

        if local_meshes:
            # Decode textures and materials
            local_tex_inventory: Dict[int, TextureInfo] = {}
            for tex in scan_pop_textures(payload):
                cur = local_tex_inventory.get(tex.key)
                if cur is None or (tex.data_end - tex.data_offset) > (cur.data_end - cur.data_offset):
                    local_tex_inventory[tex.key] = tex

            packs, legacy_materials = scan_pop_materials(payload)
            records = scan_pop_material_records(payload, set(local_tex_inventory.keys()))

            wanted_local_keys: Set[int] = set()
            for mesh in local_meshes:
                tex_map: Dict[int, int] = {}
                col_map: Dict[int, Tuple[float, float, float, float]] = {}

                pack: List[int] = []
                if mesh.material_pack_key is not None:
                    pack = packs.get(mesh.material_pack_key, [])
                    if not pack and (mesh.material_pack_key in records or mesh.material_pack_key in legacy_materials):
                        pack = [mesh.material_pack_key]

                for mat_id, _cnt in mesh.material_ids:
                    mat_key = None
                    if pack:
                        pack_idx = 0 if mat_id < 0 else min(mat_id, len(pack) - 1)
                        mat_key = pack[pack_idx]

                    record = records.get(mat_key) if mat_key is not None else None
                    texture_key = record.texture_key if record is not None else legacy_materials.get(mat_key)
                    if texture_key is None:
                        direct = records.get(mat_id)
                        if direct is not None:
                            record = direct
                            texture_key = direct.texture_key
                        else:
                            texture_key = legacy_materials.get(mat_id)

                    if texture_key not in (None, 0, 0xFFFFFFFF):
                        tex_map[mat_id] = texture_key
                        wanted_local_keys.add(texture_key)

                    if record is not None:
                        r, g, b, a = jade_color_rgba(record.diffuse_color)
                        mat_alpha = record.alpha if record.alpha > 0.0 else 1.0
                        col_map[mat_id] = (r, g, b, max(0.0, min(1.0, a * mat_alpha)))
                    else:
                        col_map[mat_id] = (1.0, 1.0, 1.0, 1.0)

                all_texture_maps[mesh.key] = tex_map
                all_color_maps[mesh.key] = col_map

            # Decode local textures (wanted + inventory)
            keys_to_decode = set(wanted_local_keys) | set(local_tex_inventory.keys())
            for tex_key in keys_to_decode:
                if tex_key in all_images:
                    continue
                tex_info = local_tex_inventory.get(tex_key)
                if tex_info is not None:
                    img = decode_pop_texture_image(payload, tex_info)
                    if img is not None:
                        all_images[tex_key] = img
                        all_tex_infos[tex_key] = tex_info
                        all_original_blobs[tex_key] = get_pop_texture_original_blob(payload, tex_info)
                        all_tex_sources[tex_key] = source.name
                    elif tex_key in wanted_local_keys:
                        wanted_missing_textures.add(tex_key)
                elif tex_key in wanted_local_keys:
                    wanted_missing_textures.add(tex_key)

    # Search for missing textures in other archive assets (optimized candidate filter)
    unresolved = wanted_missing_textures - set(all_images.keys())
    if unresolved and archive:
        wanted_low16 = {k & 0xFFFF for k in unresolved}
        # Prioritize entries matching keys or texture keywords
        candidates = [
            e for e in archive.entries
            if e.key in unresolved
            or (e.key & 0xFFFF) in wanted_low16
            or any(kw in e.name.casefold() for kw in ("tx_", "_tx", "texture", ".dds", "material", "pal"))
        ]
        # Cap candidates to max 60 entries so loading remains fast
        candidates = candidates[:60]
        if candidates and progress_callback:
            progress_callback(f"Checking {len(candidates)} texture banks for {len(unresolved)} textures...")
        for entry in candidates:
            if not unresolved:
                break
            try:
                candidate_data = archive.read_entry(entry)
                for tex in scan_pop_textures(candidate_data):
                    if tex.key in unresolved and tex.data_end - tex.data_offset > 4:
                        img = decode_pop_texture_image(candidate_data, tex)
                        if img is not None:
                            all_images[tex.key] = img
                            all_tex_infos[tex.key] = tex
                            all_original_blobs[tex.key] = get_pop_texture_original_blob(candidate_data, tex)
                            all_tex_sources[tex.key] = entry.name
                            unresolved.discard(tex.key)
            except Exception:
                continue

    align_character_head_objects(all_objects)

    return LevelSceneData(
        name=target_entry.name,
        objects=all_objects,
        meshes=all_meshes,
        textures=all_images,
        texture_maps=all_texture_maps,
        color_maps=all_color_maps,
        mesh_links=all_mesh_links,
        source_assets=[s.name for s in sources],
        texture_infos=all_tex_infos,
        texture_original_blobs=all_original_blobs,
        texture_sources=all_tex_sources,
        animation_clips=all_clips,
        ai_scripts=all_ai_scripts,
    )


def load_level_from_raw_data(
    name: str,
    raw_data: bytes,
    archive: Optional[BFArchive] = None,
    progress_callback: Optional[Callable[[str], None]] = None
) -> LevelSceneData:
    """Load a 3D level directly from raw bytes (with auto LZO decompression)."""
    if looks_like_pop_lzo(raw_data):
        payload = decompress_pop_lzo(raw_data)
    else:
        payload = raw_data

    local_objects = scan_level_objects(payload)
    local_meshes = scan_pop_meshes(payload)
    associate_mesh_material_packs(payload, local_meshes)
    local_clips = scan_animations(payload)
    tag_animation_clips(local_clips, name, local_objects)
    local_scripts = scan_ai_scripts_from_payload(payload, source_name=name)

    mesh_keys = {m.key for m in local_meshes}
    entries = parse_pop_file_entries(payload)
    entries_by_key = {entry.key: entry for entry in entries}

    all_mesh_links = resolve_object_mesh_links(local_objects, mesh_keys, entries_by_key, payload)

    all_meshes = {m.key: m for m in local_meshes}
    all_images: Dict[int, object] = {}
    all_tex_infos: Dict[int, TextureInfo] = {}
    all_original_blobs: Dict[int, Tuple[bytes, str]] = {}
    all_tex_sources: Dict[int, str] = {}
    all_texture_maps: Dict[int, Dict[int, int]] = {}
    all_color_maps: Dict[int, Dict[int, Tuple[float, float, float, float]]] = {}

    local_tex_inventory: Dict[int, TextureInfo] = {}
    for tex in scan_pop_textures(payload):
        cur = local_tex_inventory.get(tex.key)
        if cur is None or (tex.data_end - tex.data_offset) > (cur.data_end - cur.data_offset):
            local_tex_inventory[tex.key] = tex

    packs, legacy_materials = scan_pop_materials(payload)
    records = scan_pop_material_records(payload, set(local_tex_inventory.keys()))

    wanted_keys: Set[int] = set()
    for mesh in local_meshes:
        tex_map: Dict[int, int] = {}
        col_map: Dict[int, Tuple[float, float, float, float]] = {}

        pack: List[int] = []
        if mesh.material_pack_key is not None:
            pack = packs.get(mesh.material_pack_key, [])
            if not pack and (mesh.material_pack_key in records or mesh.material_pack_key in legacy_materials):
                pack = [mesh.material_pack_key]

        for mat_id, _cnt in mesh.material_ids:
            mat_key = None
            if pack:
                pack_idx = 0 if mat_id < 0 else min(mat_id, len(pack) - 1)
                mat_key = pack[pack_idx]

            record = records.get(mat_key) if mat_key is not None else None
            texture_key = record.texture_key if record is not None else legacy_materials.get(mat_key)
            if texture_key is None:
                direct = records.get(mat_id)
                if direct is not None:
                    record = direct
                    texture_key = direct.texture_key
                else:
                    texture_key = legacy_materials.get(mat_id)

            if texture_key not in (None, 0, 0xFFFFFFFF):
                tex_map[mat_id] = texture_key
                wanted_keys.add(texture_key)

            if record is not None:
                r, g, b, a = jade_color_rgba(record.diffuse_color)
                mat_alpha = record.alpha if record.alpha > 0.0 else 1.0
                col_map[mat_id] = (r, g, b, max(0.0, min(1.0, a * mat_alpha)))
            else:
                col_map[mat_id] = (1.0, 1.0, 1.0, 1.0)

        all_texture_maps[mesh.key] = tex_map
        all_color_maps[mesh.key] = col_map

    keys_to_decode = set(wanted_keys) | set(local_tex_inventory.keys())
    for tex_key in keys_to_decode:
        tex_info = local_tex_inventory.get(tex_key)
        if tex_info is not None:
            img = decode_pop_texture_image(payload, tex_info)
            if img is not None:
                all_images[tex_key] = img
                all_tex_infos[tex_key] = tex_info
                all_original_blobs[tex_key] = get_pop_texture_original_blob(payload, tex_info)
                all_tex_sources[tex_key] = name

    align_character_head_objects(local_objects)

    return LevelSceneData(
        name=name,
        objects=local_objects,
        meshes=all_meshes,
        textures=all_images,
        texture_maps=all_texture_maps,
        color_maps=all_color_maps,
        mesh_links=all_mesh_links,
        source_assets=[name],
        texture_infos=all_tex_infos,
        texture_original_blobs=all_original_blobs,
        texture_sources=all_tex_sources,
        animation_clips=local_clips,
        ai_scripts=local_scripts,
    )
