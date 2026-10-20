import sys
import os
import struct
from pathlib import Path
from jade_engine.bf_parser import load_bf, read_bigfile
from jade_engine.bin_parser import decompress_bin
from jade_engine.mesh_extractor import extract_all_meshes, find_gao_names
from jade_engine.textures import extract_all_textures, scan_pop_textures


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 cli.py <bf_file>                           # List all files")
        print("  python3 cli.py <bf_file> <file_name>               # Extract and analyze file")
        print("  python3 cli.py <bf_file> --extract-textures <file> # Extract textures in original format (.dds/.tga)")
        print("  python3 cli.py <bf_file> --extract-all-textures    # Extract all textures from whole archive")
        sys.exit(1)

    bf_path = sys.argv[1]

    # Handle --extract-all-textures
    if len(sys.argv) >= 3 and sys.argv[2] == "--extract-all-textures":
        out_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(bf_path).stem + "_textures_original"
        print(f"Loading {bf_path}...")
        bf = read_bigfile(bf_path)
        total_extracted = 0
        for entry in bf.entries:
            try:
                data = bf.read_entry(entry)
                texs = scan_pop_textures(data)
                if texs:
                    stem = entry.name.replace(".bin", "").replace(".wow", "").replace(".wol", "")
                    entry_out = out_dir / stem
                    results = extract_all_textures(data, entry_out, prefix=f"{stem}_")
                    print(f"  {entry.name:40s} -> Extracted {len(results)} textures")
                    total_extracted += len(results)
            except Exception:
                continue
        print(f"\nDone! Extracted {total_extracted} textures in original format to: {out_dir}")
        return

    # Handle --extract-textures <file_name>
    if len(sys.argv) >= 4 and sys.argv[2] == "--extract-textures":
        target_name = sys.argv[3]
        out_dir = Path(sys.argv[4]) if len(sys.argv) > 4 else Path(f"{target_name}_textures_original")
        print(f"Loading {bf_path}...")
        bf = read_bigfile(bf_path)
        entry = bf.get_entry_by_name(target_name)
        if not entry:
            print(f"File not found: {target_name}")
            return
        data = bf.read_entry(entry)
        results = extract_all_textures(data, out_dir, prefix=f"{Path(target_name).stem}_")
        print(f"Extracted {len(results)} textures in original format (.dds/.tga) to: {out_dir}")
        for tex, path, _ in results:
            print(f"  Key 0x{tex.key:08X} ({tex.format}): {path.name} ({path.stat().st_size:,} bytes)")
        return

    target_name = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Loading {bf_path}...")
    bf = load_bf(bf_path)
    print(f"Version: {bf.version}, Files: {len(bf.files)}")
    print()

    if target_name is None:
        print("Files:")
        for f in bf.files:
            name = f.filename or f"0x{f.key:08X}"
            print(f"  {name:45s} key=0x{f.key:08X} size={f.size:,}")
        return

    bf_file = bf.get_file_by_name(target_name)
    if not bf_file:
        print(f"File not found: {target_name}")
        return

    print(f"File: {bf_file.filename}")
    print(f"Key: 0x{bf_file.key:08X}")
    print(f"Size: {bf_file.size:,} bytes")
    print()

    decompressed = decompress_bin(bf_file.data)
    print(f"Decompressed: {len(decompressed):,} bytes")

    blocks = decompressed.split(b'\x99\xC0\xFF\xEE')
    print(f"Blocks: {len(blocks)}")
    print()

    print("Block types:")
    for i, block in enumerate(blocks):
        if len(block) < 8:
            continue
        hash_id = block[:4][::-1].hex().upper()
        type_str = block[4:8].decode('ascii', errors='replace')
        type_id = block[4:8][::-1].hex().upper()
        print(f"  Block {i:2d}: hash={hash_id}, type={type_str:6s} (0x{type_id}), size={len(block):,}")

    print()
    meshes = extract_all_meshes(blocks)
    print(f"Extracted meshes: {len(meshes)}")
    for hash_id, mesh in list(meshes.items())[:5]:
        verts = mesh['vertices']
        faces = mesh['faces']
        print(f"  {hash_id}: {len(verts)} vertices, {len(faces)} faces")

    print()
    objects = find_gao_names(blocks)
    print(f"Found objects: {len(objects)}")
    for obj in objects[:15]:
        print(f"  {obj['name']:40s} hash={obj['hash']}")


if __name__ == "__main__":
    main()
