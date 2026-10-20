# JadeEngine — Prince of Persia 3D Level Viewer & Extractor

An interactive, high-performance 3D level viewer, asset extractor, and reverse-engineering tool for Ubisoft's **Jade Engine**, specifically built for the ***Prince of Persia: The Sands of Time* trilogy** (*The Sands of Time*, *Warrior Within*, and *The Two Thrones*).

Directly inspects and renders complete 3D levels, rooms, character kits, materials, and textures from retail BigFiles (`PRINCE.BF`, `prince2.bf`, `prince3.bf`) and extracted `.bin`, `.wow`, and `.wol` files.

---

## ✨ Features

- **Direct BigFile (`.bf`) Support**: Reads FAT tables and extracted assets directly from `prince3.bf`, `PRINCE.BF`, and `prince2.bf`.
- **WOL & WOW Level Resolution**: Automatically stitches complete game levels by resolving World Object List (`.wol`) master files to their constituent World Object Wave (`.wow`) rooms, character kits, and weapon models.
- **Hardware-Accelerated POP-LZO**: High-speed multi-block 128 KB stream decompressor utilizing a native C extension (`libminilzo`) with pure-Python fallback.
- **Full Texture Decoding & Native Extraction**:
  - Decodes DXT1 (BC1), DXT3 (BC2), DXT5 (BC3), uncompressed 32-bit BGRA / 24-bit BGR, 8-bit paletted (PAL8), and 4-bit textures.
  - **Extract Textures in Original Native Format (`.dds` / `.tga`)**: Dumps raw compressed blocks into standard DirectDraw Surface (`.dds`) and Truevision TGA (`.tga`) files preserving complete mipmap chains and zero recompression loss.
  - Export single or batch textures directly from the UI or command line.
- **Modern OpenGL 3D Viewport**:
  - Textured and shaded 3D rendering with dual-light Phong illumination.
  - **Dynamic Scene Animation**: Real-time GPU texture coordinate scrolling for drifting clouds, wind streams, and flowing water (`🌀 Dynamic Wind & Clouds`).
  - **Turntable Orbit**: Smooth 60 FPS automated presentation camera rotation (`🔄 Turntable`).
  - Hardware mipmapped textures with automatic $V$-axis coordinate inversion ($V_{\text{gl}} = 1.0 - V_{\text{jade}}$).
  - Alpha testing (`glAlphaFunc`) for crisp decorative cutouts (curtains, grates, chains, foliage).
  - Display list acceleration achieving smooth 60+ FPS navigation over massive levels.
  - Orbit, Pan, Zoom, and WASDQE Fly camera controls.
- **Animation Track Support (`animations.py`)**:
  - Native parser for Jade `TRL`/`EVE` skeletal and trajectory animation tracks.
  - Decodes quaternion rotation keyframes (normalized `0x1010` and packed `0x4010`) and 3D translation vectors.
  - Discovers playable action clips in character kits (e.g. `Prince_wow`) and animated room traps.
- **Interactive UI (PySide6)**:
  - Dark-themed level explorer with category grouping (WOL Levels, WOW Rooms, Generic BINs).
  - Real-time search filter and object hierarchy tree inspector.
  - Visual texture gallery with image thumbnails, format badges, and one-click extraction buttons.
  - Asset tree context menus to extract textures from any `.wow` or `.bin` archive asset without loading 3D levels.
  - Wavefront OBJ Exporter with multi-mesh hierarchy, UVs, and world transforms.

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.9+
- `pip install -r requirements.txt` (Installs `PySide6`, `PyOpenGL`, `numpy`, `pillow`)

### 2. Launch the GUI
```bash
python3 main.py
```
*If `prince3.bf` is present in the working directory, it will automatically load on startup.*

### 3. CLI Mode
```bash
# List all files in archive
python3 cli.py prince3.bf

# Extract and inspect specific BIN file
python3 cli.py prince3.bf 0103_Couloir_wol_ff02b5ae.bin

# Extract textures from a specific file in original format (.dds / .tga)
python3 cli.py prince3.bf --extract-textures 0103_Couloir_wow_ff02b598.bin

# Extract all textures across the entire archive in original format
python3 cli.py prince3.bf --extract-all-textures
```

---

## 🎮 3D Navigation Controls

| Key / Mouse | Action |
| :--- | :--- |
| **Left Mouse Drag** | Orbit camera around level |
| **Middle Mouse Drag** (or **Shift + Left Drag**) | Pan camera |
| **Mouse Scroll Wheel** (or **Right Mouse Drag**) | Zoom in / out |
| **W, A, S, D, Q, E** | Free-fly camera navigation |
| **F or R Key** | Frame entire level to fit screen |
| **Double-Click Object** | Focus camera directly on selected object |

---

## 📚 Technical Documentation

For an in-depth reverse-engineering guide covering:
- BigFile header layouts and FAT tables
- POP-LZO 128KB multi-block compression format
- FileEntry resource streams
- GEO mesh v7/v8 layouts and vertex lighting (RLI)
- Texture signatures and DXT/TGA/PAL codecs
- GameObject (`.gao`) 3x3 orientation matrices and transform math
- WOL dependency resolution algorithms

Please refer to the comprehensive **[DOCUMENTATION.md](DOCUMENTATION.md)**.
