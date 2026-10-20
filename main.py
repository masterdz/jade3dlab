"""Jade Engine 3D Level Editor & Viewer for Prince of Persia BigFiles and BINs."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PySide6.QtCore import QPoint, Qt, QThread, Signal
from PySide6.QtGui import QAction, QColor, QFont, QIcon, QPixmap, QImage
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDialog,
    QDockWidget,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSlider,
    QPlainTextEdit,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from jade_engine.ai_decompiler import (
    AIFunction,
    AIModel,
    decompile_ai_function,
    disassemble_ai_function,
    export_decompiled_scripts_to_dir,
    parse_ai_function,
    parse_ai_model,
    scan_all_ai_scripts_in_archive,
)
from jade_engine.bf_parser import BFArchive, read_bigfile
from jade_engine.level_loader import load_level_from_archive, load_level_from_raw_data
from jade_engine.level_scene import level_asset_kind
from jade_engine.models import BigFileEntry, LevelObject, LevelSceneData
from jade_engine.textures import (
    extract_all_textures,
    extract_texture_file,
    get_pop_texture_original_blob,
    scan_pop_textures,
)
from jade_engine.animations import AnimationClip, format_clip_character, infer_character_group
from jade_engine.viewer import GLViewer
def format_character_label(entry_name: str) -> str:
    """Format character asset name with recognizable emoji and display title."""
    low = entry_name.casefold()
    if "prince" in low:
        return f"👑 Prince ({entry_name})"
    if "farah" in low:
        return f"🏹 Farah ({entry_name})"
    if "sandman" in low or "sman" in low:
        return f"⚔️ Sand Man ({entry_name})"
    if "sandguard" in low or "sguard" in low:
        return f"⚔️ Sand Guard ({entry_name})"
    if "courtesan" in low:
        return f"⚔️ Sand Courtesan ({entry_name})"
    if "indianman" in low:
        return f"⚔️ Indian Man ({entry_name})"
    if "indianguard" in low:
        return f"⚔️ Indian Guard ({entry_name})"
    if "pirate" in low:
        return f"⚔️ Pirate Enemy ({entry_name})"
    if "disciple" in low:
        return f"⚔️ Disciple Enemy ({entry_name})"
    if "crow_master" in low:
        return f"🦅 Crow Master ({entry_name})"
    if "crow" in low:
        return f"🦅 Crow ({entry_name})"
    if "dahaka" in low:
        return f"💀 Dahaka Boss ({entry_name})"
    if "kaileena" in low or "kaleena" in low:
        return f"👑 Kaileena ({entry_name})"
    if "shahdee" in low:
        return f"⚔️ Shahdee ({entry_name})"
    if "brute" in low:
        return f"🧌 Brute ({entry_name})"
    if "assassin" in low:
        return f"🥷 Assassin ({entry_name})"
    if "thief" in low:
        return f"🥷 Thief ({entry_name})"
    if "mahasti" in low:
        return f"⚔️ Mahasti ({entry_name})"
    if "initiate" in low:
        return f"⚔️ Initiate ({entry_name})"
    return f"👤 {entry_name}"


def get_archive_characters(bf: Optional[BFArchive]) -> List[BigFileEntry]:
    """Scan and retrieve available character models in the loaded BigFile archive."""
    if not bf:
        return []
    chars = []
    seen_keys = set()
    for e in bf.entries:
        if e.key in seen_keys:
            continue
        low = e.name.casefold()
        if any(skip in low for skip in ("actkit", "costume", "weapon", "sword", "dagger", "_fx_", "mark_", "_snd_", "_sound_")):
            continue
        if "prince_wow" in low or "farah_wow" in low or (low.startswith("act_") and "_wow" in low):
            chars.append(e)
            seen_keys.add(e.key)
        elif level_asset_kind(e.name) == "character":
            chars.append(e)
            seen_keys.add(e.key)

    def _char_sort_key(entry):
        n = entry.name.casefold()
        if "prince_wow" in n:
            return (0, n)
        if "farah_wow" in n:
            return (1, n)
        return (2, n)

    chars.sort(key=_char_sort_key)
    return chars


def get_scene_spawn_markers(scene: LevelSceneData) -> List[Tuple[str, Tuple[float, float, float]]]:
    """Find all potential player/character spawn markers, checkpoints, and waypoints in the level scene."""
    pri_keywords = ("arrivee", "checkpoint", "ini_pos", "cam_arrivee", "tec_checkpoint", "start")
    sec_keywords = ("spawn", "frh_", "wp_", "cam_zone", "gate", "porte", "door")

    pri_list = []
    sec_list = []
    seen = set()

    for obj in scene.objects:
        if abs(obj.position[0]) > 25000 or abs(obj.position[1]) > 25000 or abs(obj.position[2]) > 10000:
            continue
        low = obj.name.casefold()
        if obj.name in seen:
            continue
        if any(k in low for k in pri_keywords):
            pri_list.append((obj.name, obj.position))
            seen.add(obj.name)
        elif any(k in low for k in sec_keywords):
            sec_list.append((obj.name, obj.position))
            seen.add(obj.name)

    def _pri_sort(item):
        low = item[0].casefold()
        if "cam_arrivee" in low or "arrivee" in low:
            return 0
        if "checkpoint" in low:
            return 1
        if "ini_pos" in low:
            return 2
        return 3

    pri_list.sort(key=_pri_sort)
    return pri_list + sec_list


class SpawnCharacterDialog(QDialog):
    """Dialog allowing the user to select and spawn a character into the active 3D level."""

    def __init__(
        self,
        parent: QWidget,
        archive: Optional[BFArchive],
        scene: LevelSceneData,
        selected_obj: Optional[LevelObject] = None,
        cam_target: Optional[List[float]] = None,
        default_entry: Optional[BigFileEntry] = None,
        default_pos: Optional[Tuple[float, float, float]] = None,
    ):
        super().__init__(parent)
        self.archive = archive
        self.scene = scene
        self.selected_obj = selected_obj
        self.cam_target = cam_target or [0.0, 0.0, 0.0]
        self.default_entry = default_entry
        self.default_pos = default_pos
        self.custom_file_path: Optional[Path] = None

        self.setWindowTitle("👤 Spawn Character into Level")
        self.resize(560, 520)
        self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        header = QLabel(
            "<h3>👤 Spawn Character into Active 3D Level</h3>"
            "<p style='color: #90caf9; margin: 0;'>"
            "Instantiate character geometry, materials, and animation clips at a level spawn point."
            "</p>"
        )
        layout.addWidget(header)

        # Group 1: Character Selection
        grp_char = QGroupBox("1. Choose Character Model")
        layout_char = QVBoxLayout(grp_char)

        self.combo_char = QComboBox()
        self.combo_char.setMinimumHeight(32)

        chars = get_archive_characters(self.archive)
        default_idx = 0
        for idx, entry in enumerate(chars):
            label = format_character_label(entry.name)
            self.combo_char.addItem(label, entry)
            if self.default_entry and entry.key == self.default_entry.key:
                default_idx = idx

        if chars:
            self.combo_char.setCurrentIndex(default_idx)
        else:
            self.combo_char.addItem("No characters found in current archive", None)

        layout_char.addWidget(self.combo_char)

        btn_browse = QPushButton("📁 Or Browse External WOW / BIN File...")
        btn_browse.clicked.connect(self._browse_external_char)
        layout_char.addWidget(btn_browse)

        layout.addWidget(grp_char)

        # Group 2: Spawn Location
        grp_pos = QGroupBox("2. Spawn Location in Level")
        layout_pos = QVBoxLayout(grp_pos)

        self.btn_group = QButtonGroup(self)

        # Radio 1: Detected Markers
        self.markers = get_scene_spawn_markers(self.scene)
        self.radio_marker = QRadioButton("Level Arrival Marker / Checkpoint:")
        self.btn_group.addButton(self.radio_marker)
        layout_pos.addWidget(self.radio_marker)

        self.combo_markers = QComboBox()
        self.combo_markers.setMinimumHeight(28)
        if self.markers:
            for name, pos in self.markers:
                self.combo_markers.addItem(f"{name}  →  ({pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f})", pos)
            self.combo_markers.currentIndexChanged.connect(self._on_marker_changed)
        else:
            self.combo_markers.addItem("No arrival/checkpoint markers detected in level", (0.0, 0.0, 0.0))
            self.combo_markers.setEnabled(False)
        layout_pos.addWidget(self.combo_markers)

        # Radio 2: Selected Scene Object
        if self.selected_obj:
            obj_pos = self.selected_obj.position
            self.radio_selected = QRadioButton(
                f"At Selected Object: {self.selected_obj.name}  →  ({obj_pos[0]:.1f}, {obj_pos[1]:.1f}, {obj_pos[2]:.1f})"
            )
            self.radio_selected.setEnabled(True)
        else:
            self.radio_selected = QRadioButton("At Selected Object: (No object selected in viewport)")
            self.radio_selected.setEnabled(False)
        self.btn_group.addButton(self.radio_selected)
        layout_pos.addWidget(self.radio_selected)

        # Radio 3: Current Camera Target
        cam_x, cam_y, cam_z = self.cam_target
        self.radio_camera = QRadioButton(
            f"At Viewport Camera Focus: ({cam_x:.1f}, {cam_y:.1f}, {cam_z:.1f})"
        )
        self.btn_group.addButton(self.radio_camera)
        layout_pos.addWidget(self.radio_camera)

        # Radio 4: Custom Coordinates
        self.radio_custom = QRadioButton("Manual Coordinates (X, Y, Z):")
        self.btn_group.addButton(self.radio_custom)
        layout_pos.addWidget(self.radio_custom)

        # Coordinate spinboxes
        coord_layout = QHBoxLayout()
        coord_layout.addWidget(QLabel("X:"))
        self.spin_x = QDoubleSpinBox()
        self.spin_x.setRange(-99999.0, 99999.0)
        self.spin_x.setDecimals(2)
        coord_layout.addWidget(self.spin_x)

        coord_layout.addWidget(QLabel("Y:"))
        self.spin_y = QDoubleSpinBox()
        self.spin_y.setRange(-99999.0, 99999.0)
        self.spin_y.setDecimals(2)
        coord_layout.addWidget(self.spin_y)

        coord_layout.addWidget(QLabel("Z (Height):"))
        self.spin_z = QDoubleSpinBox()
        self.spin_z.setRange(-99999.0, 99999.0)
        self.spin_z.setDecimals(2)
        coord_layout.addWidget(self.spin_z)

        layout_pos.addLayout(coord_layout)
        layout.addWidget(grp_pos)

        # Radio button change connections
        self.radio_marker.toggled.connect(self._on_radio_toggled)
        self.radio_selected.toggled.connect(self._on_radio_toggled)
        self.radio_camera.toggled.connect(self._on_radio_toggled)
        self.radio_custom.toggled.connect(self._on_radio_toggled)

        # Determine initial selection
        if self.default_pos is not None:
            self.radio_custom.setChecked(True)
            self._set_coords(*self.default_pos)
        elif self.markers:
            self.radio_marker.setChecked(True)
            self._set_coords(*self.markers[0][1])
        elif self.selected_obj:
            self.radio_selected.setChecked(True)
            self._set_coords(*self.selected_obj.position)
        else:
            self.radio_camera.setChecked(True)
            self._set_coords(*self.cam_target)

        # Group 3: Options
        grp_opts = QGroupBox("3. Spawn Options")
        layout_opts = QVBoxLayout(grp_opts)

        self.chk_focus = QCheckBox("🎯 Frame 3D Viewport Camera on Spawned Character")
        self.chk_focus.setChecked(True)
        layout_opts.addWidget(self.chk_focus)

        self.chk_autoplay = QCheckBox("🎬 Auto-Play First Animation Clip (Walk / Combat / Idle)")
        self.chk_autoplay.setChecked(False)
        layout_opts.addWidget(self.chk_autoplay)

        layout.addWidget(grp_opts)

        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_spawn = QPushButton("👤 Spawn Character")
        self.btn_spawn.setObjectName("ActionBtn")
        self.btn_spawn.setMinimumHeight(36)
        self.btn_spawn.setStyleSheet("background-color: #00897b; color: white; font-weight: bold; padding: 6px 20px; font-size: 14px;")
        self.btn_spawn.clicked.connect(self._on_spawn_clicked)
        btn_layout.addWidget(self.btn_spawn)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setMinimumHeight(36)
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        layout.addLayout(btn_layout)

    def _browse_external_char(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Character WOW or BIN File", "", "Character Models (*.bin *.wow);;All Files (*)"
        )
        if path:
            p = Path(path)
            self.custom_file_path = p
            label = f"📁 External: {p.name}"
            self.combo_char.addItem(label, None)
            self.combo_char.setCurrentIndex(self.combo_char.count() - 1)

    def _set_coords(self, x: float, y: float, z: float):
        self.spin_x.setValue(x)
        self.spin_y.setValue(y)
        self.spin_z.setValue(z)

    def _on_marker_changed(self, idx: int):
        if self.radio_marker.isChecked() and idx >= 0:
            pos = self.combo_markers.itemData(idx)
            if pos:
                self._set_coords(*pos)

    def _on_radio_toggled(self):
        if self.radio_marker.isChecked():
            idx = self.combo_markers.currentIndex()
            pos = self.combo_markers.itemData(idx)
            if pos:
                self._set_coords(*pos)
        elif self.radio_selected.isChecked() and self.selected_obj:
            self._set_coords(*self.selected_obj.position)
        elif self.radio_camera.isChecked():
            self._set_coords(*self.cam_target)

    def _on_spawn_clicked(self):
        if self.combo_char.currentData() is None and self.custom_file_path is None:
            QMessageBox.warning(self, "No Character Selected", "Please select a character to spawn from the list or browse for a file.")
            return
        self.accept()

    def get_selected_entry(self) -> Optional[BigFileEntry]:
        return self.combo_char.currentData()

    def get_custom_file_path(self) -> Optional[Path]:
        return self.custom_file_path

    def get_spawn_position(self) -> Tuple[float, float, float]:
        return (self.spin_x.value(), self.spin_y.value(), self.spin_z.value())

    def get_focus_camera(self) -> bool:
        return self.chk_focus.isChecked()

    def get_auto_play(self) -> bool:
        return self.chk_autoplay.isChecked()


class LevelLoadWorker(QThread):
    """Background worker to load levels without freezing the Qt GUI."""

    progress = Signal(str)
    finished_success = Signal(object)
    finished_error = Signal(str)

    def __init__(
        self,
        archive: Optional[BFArchive],
        entry: Optional[BigFileEntry],
        raw_path: Optional[Path] = None,
        selected_costume_key: Optional[int] = None
    ):
        super().__init__()
        self.archive = archive
        self.entry = entry
        self.raw_path = raw_path
        self.selected_costume_key = selected_costume_key

    def run(self):
        try:
            if self.archive and self.entry:
                scene = load_level_from_archive(
                    self.archive,
                    self.entry,
                    progress_callback=self.progress.emit,
                    selected_costume_key=self.selected_costume_key
                )
            elif self.raw_path:
                self.progress.emit(f"Reading {self.raw_path.name}...")
                raw_bytes = self.raw_path.read_bytes()
                scene = load_level_from_raw_data(self.raw_path.name, raw_bytes, self.archive, progress_callback=self.progress.emit)
            else:
                raise ValueError("No target asset specified for level loading.")
            self.finished_success.emit(scene)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.finished_error.emit(str(e))


class LevelEditor(QMainWindow):
    """Main Application Window for Jade Engine Level Editor."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jade Engine — Prince of Persia 3D Level Viewer")
        self.resize(1500, 950)

        self.bf_archive: Optional[BFArchive] = None
        self.current_scene: Optional[LevelSceneData] = None
        self.load_worker: Optional[LevelLoadWorker] = None
        self._updating_inspector: bool = False

        self._apply_dark_theme()
        self._create_menu()
        self._create_ui()
        self.statusBar().showMessage("Ready — Open prince3.bf or a .bin level to begin")

        # Automatically open prince3.bf if present in working directory
        default_bf = Path("prince3.bf")
        if default_bf.is_file():
            self._load_bf_path(default_bf)

    def _apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1f26;
                color: #e0e0e0;
            }
            QWidget {
                color: #e0e0e0;
                font-size: 13px;
            }
            QGroupBox {
                border: 1px solid #333644;
                border-radius: 6px;
                margin-top: 18px;
                font-weight: bold;
                padding-top: 10px;
                background-color: #242630;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
                color: #64b5f6;
            }
            QTreeWidget, QTableWidget, QTextEdit {
                background-color: #1b1c24;
                border: 1px solid #333644;
                border-radius: 4px;
                selection-background-color: #2d558a;
                selection-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #2b2d3a;
                color: #b0bec5;
                padding: 4px;
                border: 1px solid #333644;
                font-weight: bold;
            }
            QDockWidget {
                color: #e0e0e0;
                font-weight: bold;
            }
            QDockWidget::title {
                background: #242634;
                padding: 6px 10px;
                border: 1px solid #36394d;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                color: #64b5f6;
                font-weight: bold;
            }
            QDockWidget::close-button, QDockWidget::float-button {
                background: #2b2d3c;
                border: 1px solid #3d4158;
                border-radius: 3px;
                padding: 2px;
            }
            QDockWidget::close-button:hover, QDockWidget::float-button:hover {
                background: #3b3e54;
                border-color: #64b5f6;
            }
            QPushButton {
                background-color: #2e66b0;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3b7ed6;
            }
            QPushButton:disabled {
                background-color: #373b4d;
                color: #787d91;
            }
            QPushButton#ActionBtn {
                background-color: #00897b;
            }
            QPushButton#ActionBtn:hover {
                background-color: #00a896;
            }
            QLineEdit {
                background-color: #1b1c24;
                border: 1px solid #3f4459;
                border-radius: 4px;
                padding: 4px 8px;
                color: #ffffff;
            }
            QCheckBox {
                spacing: 6px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QTabWidget::pane {
                border: 1px solid #333644;
                background-color: #242630;
            }
            QTabBar::tab {
                background: #1b1c24;
                color: #b0bec5;
                padding: 8px 16px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #242630;
                color: #64b5f6;
                font-weight: bold;
            }
            QProgressBar {
                border: 1px solid #333644;
                border-radius: 3px;
                text-align: center;
                background-color: #1b1c24;
            }
            QProgressBar::chunk {
                background-color: #2e66b0;
            }
        """)

    def _create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")

        open_bf_action = QAction("&Open BF Archive (prince.bf / prince3.bf)...", self)
        open_bf_action.setShortcut("Ctrl+O")
        open_bf_action.triggered.connect(self._open_bf_dialog)
        file_menu.addAction(open_bf_action)

        open_bin_action = QAction("Open &Standalone BIN / WOW / WOL File...", self)
        open_bin_action.setShortcut("Ctrl+B")
        open_bin_action.triggered.connect(self._open_bin_dialog)
        file_menu.addAction(open_bin_action)

        file_menu.addSeparator()

        spawn_char_action = QAction("👤 &Spawn Character into Level...", self)
        spawn_char_action.setShortcut("Ctrl+Shift+S")
        spawn_char_action.setToolTip("Spawn Prince, Farah, or enemies into the active 3D level")
        spawn_char_action.triggered.connect(self._open_spawn_character_dialog)
        file_menu.addAction(spawn_char_action)

        file_menu.addSeparator()

        export_obj_action = QAction("&Export Level / Meshes to OBJ...", self)
        export_obj_action.setShortcut("Ctrl+E")
        export_obj_action.triggered.connect(self._export_to_obj)
        file_menu.addAction(export_obj_action)

        extract_menu = menubar.addMenu("&Extract")
        extract_orig_action = QAction("Extract All Level Textures (&Original DDS/TGA)...", self)
        extract_orig_action.setShortcut("Ctrl+Shift+E")
        extract_orig_action.triggered.connect(self._extract_all_textures_original)
        extract_menu.addAction(extract_orig_action)

        extract_png_action = QAction("Extract All Level Textures (&PNG)...", self)
        extract_png_action.triggered.connect(self._extract_all_textures_png)
        extract_menu.addAction(extract_png_action)

        extract_menu.addSeparator()

        uncook_selected_action = QAction("⚡ Uncook Selected Level to Loose Files (.gao, .gro, .wow)...", self)
        uncook_selected_action.triggered.connect(self._uncook_selected_level)
        extract_menu.addAction(uncook_selected_action)

        uncook_all_action = QAction("🚀 Uncook Entire BigFile to Development State (All Assets)...", self)
        uncook_all_action.triggered.connect(self._uncook_entire_bigfile)
        extract_menu.addAction(uncook_all_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        view_menu = menubar.addMenu("&View")

        reset_cam_action = QAction("&Reset Camera (Frame Level)", self)
        reset_cam_action.setShortcut("F")
        reset_cam_action.triggered.connect(self._reset_camera)
        view_menu.addAction(reset_cam_action)

        toggle_wireframe = QAction("&Wireframe Mode", self)
        toggle_wireframe.setShortcut("W")
        toggle_wireframe.setCheckable(True)
        toggle_wireframe.triggered.connect(self._toggle_wireframe_menu)
        view_menu.addAction(toggle_wireframe)

        toggle_textures = QAction("&Textures", self)
        toggle_textures.setShortcut("T")
        toggle_textures.setCheckable(True)
        toggle_textures.setChecked(True)
        toggle_textures.triggered.connect(self._toggle_textures_menu)
        view_menu.addAction(toggle_textures)

        toggle_two_sided = QAction("Two-&Sided Walls", self)
        toggle_two_sided.setShortcut("B")
        toggle_two_sided.setCheckable(True)
        toggle_two_sided.setChecked(True)
        toggle_two_sided.triggered.connect(lambda checked: self.chk_two_sided.setChecked(checked))
        view_menu.addAction(toggle_two_sided)

        view_menu.addSeparator()
        self.toggle_inspector_action = QAction("🛠️ &Transform Inspector Panel", self)
        self.toggle_inspector_action.setShortcut("I")
        self.toggle_inspector_action.triggered.connect(self._toggle_inspector_visibility)
        view_menu.addAction(self.toggle_inspector_action)

        help_menu = menubar.addMenu("&Help")
        controls_action = QAction("&Controls & Navigation...", self)
        controls_action.triggered.connect(self._show_controls_help)
        help_menu.addAction(controls_action)

        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _create_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(6, 6, 6, 6)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # ================= LEFT SIDEBAR =================
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(2, 2, 2, 2)

        # Archive Info Group
        archive_group = QGroupBox("BF Archive & Levels")
        archive_layout = QVBoxLayout(archive_group)

        self.archive_info_label = QLabel("No archive loaded")
        self.archive_info_label.setStyleSheet("color: #90caf9; font-weight: bold;")
        archive_layout.addWidget(self.archive_info_label)

        # Search filter
        search_box = QHBoxLayout()
        search_box.addWidget(QLabel("Filter:"))
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("Search level (e.g. Couloir, menu, start)...")
        self.filter_edit.textChanged.connect(self._filter_tree)
        search_box.addWidget(self.filter_edit)
        archive_layout.addLayout(search_box)

        # File Tree
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabels(["Asset Name", "Size", "Type"])
        self.file_tree.setColumnWidth(0, 240)
        self.file_tree.setColumnWidth(1, 80)
        self.file_tree.itemClicked.connect(self._on_tree_item_clicked)
        self.file_tree.itemDoubleClicked.connect(self._on_tree_item_double_clicked)
        self.file_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self._on_file_tree_context_menu)
        archive_layout.addWidget(self.file_tree)

        # Load Level Button
        self.btn_load_level = QPushButton("Load 3D Level")
        self.btn_load_level.setObjectName("ActionBtn")
        self.btn_load_level.setEnabled(False)
        self.btn_load_level.clicked.connect(self._load_selected_level)
        archive_layout.addWidget(self.btn_load_level)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        archive_layout.addWidget(self.progress_bar)

        left_layout.addWidget(archive_group, stretch=5)

        # Scene Objects Inspector Group
        objects_group = QGroupBox("Scene Hierarchy & Objects")
        objects_layout = QVBoxLayout(objects_group)

        self.object_search = QLineEdit()
        self.object_search.setPlaceholderText("Search objects in scene...")
        self.object_search.textChanged.connect(self._filter_objects)
        objects_layout.addWidget(self.object_search)

        self.objects_tree = QTreeWidget()
        self.objects_tree.setHeaderLabels(["GameObject", "Kind", "Position"])
        self.objects_tree.setColumnWidth(0, 180)
        self.objects_tree.setColumnWidth(1, 70)
        self.objects_tree.itemClicked.connect(self._on_object_selected)
        self.objects_tree.itemDoubleClicked.connect(self._on_object_double_clicked)
        self.objects_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.objects_tree.customContextMenuRequested.connect(self._on_objects_tree_context_menu)
        objects_layout.addWidget(self.objects_tree)

        self.selection_info = QTextEdit()
        self.selection_info.setReadOnly(True)
        self.selection_info.setMaximumHeight(75)
        objects_layout.addWidget(self.selection_info)

        left_layout.addWidget(objects_group, stretch=4)
        splitter.addWidget(left_panel)

        # ================= RIGHT PANEL =================
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(2, 2, 2, 2)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.btn_frame_cam = QPushButton("Frame Level (F)")
        self.btn_frame_cam.clicked.connect(self._reset_camera)
        toolbar.addWidget(self.btn_frame_cam)

        self.btn_spawn_char = QPushButton("👤 Spawn Character...")
        self.btn_spawn_char.setObjectName("SpawnBtn")
        self.btn_spawn_char.setToolTip("Spawn Prince, Farah, or Enemies into the active 3D level scene")
        self.btn_spawn_char.setStyleSheet("""
            QPushButton#SpawnBtn {
                background-color: #00897b;
                color: #ffffff;
                font-weight: bold;
                padding: 6px 14px;
                border-radius: 4px;
            }
            QPushButton#SpawnBtn:hover {
                background-color: #00a896;
            }
            QPushButton#SpawnBtn:disabled {
                background-color: #2b2d3a;
                color: #616161;
            }
        """)
        self.btn_spawn_char.setEnabled(False)
        self.btn_spawn_char.clicked.connect(self._open_spawn_character_dialog)
        toolbar.addWidget(self.btn_spawn_char)

        toolbar.addWidget(QLabel("|"))

        self.chk_textures = QCheckBox("Textures")
        self.chk_textures.setChecked(True)
        self.chk_textures.toggled.connect(self._update_viewer_options)
        toolbar.addWidget(self.chk_textures)

        self.chk_meshes = QCheckBox("Meshes")
        self.chk_meshes.setChecked(True)
        self.chk_meshes.toggled.connect(self._update_viewer_options)
        toolbar.addWidget(self.chk_meshes)

        self.chk_bones = QCheckBox("🦴 Skeleton / Rig")
        self.chk_bones.setChecked(True)
        self.chk_bones.toggled.connect(self._update_viewer_options)
        toolbar.addWidget(self.chk_bones)

        self.chk_wireframe = QCheckBox("Wireframe")
        self.chk_wireframe.setChecked(False)
        self.chk_wireframe.toggled.connect(self._update_viewer_options)
        toolbar.addWidget(self.chk_wireframe)

        self.chk_objects = QCheckBox("Markers")
        self.chk_objects.setChecked(True)
        self.chk_objects.toggled.connect(self._update_viewer_options)
        toolbar.addWidget(self.chk_objects)

        toolbar.addWidget(QLabel("|"))

        toolbar.addWidget(QLabel("Lighting:"))
        self.combo_lighting = QComboBox()
        self.combo_lighting.addItems([
            "🎮 In-Game Radiosity",
            "🕯️ Sands Palace Torch",
            "☀️ Studio Directional",
            "🎨 Unlit Textures",
        ])
        self.combo_lighting.currentIndexChanged.connect(self._update_viewer_options)
        toolbar.addWidget(self.combo_lighting)

        self.chk_fog = QCheckBox("🌫️ Sands Mist")
        self.chk_fog.setToolTip("Atmospheric distance fog simulating the Sands of Time palace mist")
        self.chk_fog.setChecked(False)
        self.chk_fog.toggled.connect(self._update_viewer_options)
        toolbar.addWidget(self.chk_fog)

        self.chk_two_sided = QCheckBox("Two-Sided")
        self.chk_two_sided.setToolTip("Render walls and modular geometry from both sides (prevents single-sided wall holes)")
        self.chk_two_sided.setChecked(True)
        self.chk_two_sided.toggled.connect(self._update_viewer_options)
        toolbar.addWidget(self.chk_two_sided)

        self.chk_animate = QCheckBox("🌀 Wind & Clouds")
        self.chk_animate.setChecked(False)
        self.chk_animate.toggled.connect(self._toggle_scene_animation)
        toolbar.addWidget(self.chk_animate)

        self.chk_turntable = QCheckBox("🔄 Orbit")
        self.chk_turntable.setChecked(False)
        self.chk_turntable.toggled.connect(self._toggle_turntable)
        toolbar.addWidget(self.chk_turntable)

        self.label_costume_sep = QLabel("|")
        self.label_costume_sep.setVisible(False)
        toolbar.addWidget(self.label_costume_sep)

        self.label_costume = QLabel("Costume:")
        self.label_costume.setVisible(False)
        toolbar.addWidget(self.label_costume)

        self.combo_costume = QComboBox()
        self.combo_costume.setVisible(False)
        self.combo_costume.currentIndexChanged.connect(self._on_costume_changed)
        toolbar.addWidget(self.combo_costume)

        toolbar.addStretch()
        right_layout.addLayout(toolbar)

        # Secondary Details & Controls Bar (Under checkboxes)
        details_bar = QHBoxLayout()
        details_bar.setContentsMargins(4, 2, 4, 4)
        details_bar.setSpacing(8)

        # Yellow text of level details moved under the check boxes
        self.stats_badge = QLabel("No level loaded")
        self.stats_badge.setStyleSheet(
            "color: #ffb74d; font-weight: bold; background: #1c1d27; "
            "border: 1px solid #363a4d; padding: 4px 12px; border-radius: 4px; font-size: 11px;"
        )
        details_bar.addWidget(self.stats_badge)

        details_bar.addWidget(QLabel("|"))

        # Transform Gizmo Mode Buttons (Moved to second row to free header space)
        self.gizmo_btn_group = QButtonGroup(self)
        self.gizmo_btn_group.setExclusive(True)

        self.btn_tool_select = QPushButton("✋ Select (1)")
        self.btn_tool_select.setCheckable(True)
        self.btn_tool_select.setChecked(False)
        self.btn_tool_select.setToolTip("Click to select objects or characters in 3D scene (Hotkey: 1)")

        self.btn_tool_move = QPushButton("✥ Move (2)")
        self.btn_tool_move.setCheckable(True)
        self.btn_tool_move.setChecked(True)
        self.btn_tool_move.setToolTip("Move / Translate Gizmo: Drag X, Y, Z arrows or center handle (Hotkey: 2 or G/T)")

        self.btn_tool_rotate = QPushButton("🔄 Rotate (3)")
        self.btn_tool_rotate.setCheckable(True)
        self.btn_tool_rotate.setToolTip("Rotate Gizmo: Drag Pitch (Red), Roll (Green), or Yaw (Blue) rings (Hotkey: 3)")

        self.btn_tool_scale = QPushButton("📐 Scale (4)")
        self.btn_tool_scale.setCheckable(True)
        self.btn_tool_scale.setToolTip("Scale Gizmo: Drag X, Y, Z cubes or center handle (Hotkey: 4)")

        gizmo_style = """
            QPushButton {
                background-color: #242634;
                border: 1px solid #3d4158;
                border-radius: 4px;
                color: #cfd8dc;
                padding: 3px 9px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2e3244;
                border-color: #64b5f6;
                color: #ffffff;
            }
            QPushButton:checked {
                background-color: #1565c0;
                border: 1px solid #64b5f6;
                color: #ffffff;
                font-weight: bold;
            }
        """
        for btn in (self.btn_tool_select, self.btn_tool_move, self.btn_tool_rotate, self.btn_tool_scale):
            btn.setStyleSheet(gizmo_style)
            details_bar.addWidget(btn)

        self.gizmo_btn_group.addButton(self.btn_tool_select, 0)
        self.gizmo_btn_group.addButton(self.btn_tool_move, 1)
        self.gizmo_btn_group.addButton(self.btn_tool_rotate, 2)
        self.gizmo_btn_group.addButton(self.btn_tool_scale, 3)

        self.btn_tool_select.clicked.connect(lambda: self.viewer.set_transform_mode("select"))
        self.btn_tool_move.clicked.connect(lambda: self.viewer.set_transform_mode("translate"))
        self.btn_tool_rotate.clicked.connect(lambda: self.viewer.set_transform_mode("rotate"))
        self.btn_tool_scale.clicked.connect(lambda: self.viewer.set_transform_mode("scale"))

        self.btn_show_inspector = QPushButton("🛠️ Inspector (I)")
        self.btn_show_inspector.setToolTip("Show / Hide floating Transform Inspector window (Hotkey: I)")
        self.btn_show_inspector.setStyleSheet("""
            QPushButton {
                background-color: #1b2636;
                border: 1px solid #2d4560;
                border-radius: 4px;
                color: #90caf9;
                padding: 3px 9px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #26384d;
                border-color: #64b5f6;
                color: #ffffff;
            }
        """)
        self.btn_show_inspector.clicked.connect(self._toggle_inspector_visibility)
        details_bar.addWidget(self.btn_show_inspector)

        details_bar.addStretch()

        # Feature: Light Volume / Intensity
        details_bar.addWidget(QLabel("💡 Light Volume:"))
        self.slider_light = QSlider(Qt.Horizontal)
        self.slider_light.setRange(10, 300)
        self.slider_light.setValue(100)
        self.slider_light.setFixedWidth(110)
        self.slider_light.setToolTip("Adjust light volume and brightness of the 3D scene (10% to 300%)")
        self.slider_light.valueChanged.connect(self._on_light_volume_changed)
        details_bar.addWidget(self.slider_light)

        self.label_light_val = QLabel("100%")
        self.label_light_val.setStyleSheet("color: #64b5f6; font-weight: bold; font-family: monospace; min-width: 38px;")
        details_bar.addWidget(self.label_light_val)

        details_bar.addWidget(QLabel("|"))

        # Feature: Scene Background Color
        details_bar.addWidget(QLabel("🎨 Background:"))
        self.combo_bg_color = QComboBox()
        self.combo_bg_color.addItems([
            "🌌 Dark Slate",
            "⬛ Pitch Black",
            "🏰 Sands Amber",
            "🌊 Deep Navy",
            "🌫️ Neutral Gray",
            "⚪ Pure White",
            "🎨 Custom Color..."
        ])
        self.combo_bg_color.setToolTip("Change the viewport 3D background color")
        self.combo_bg_color.currentIndexChanged.connect(self._on_bg_color_changed)
        details_bar.addWidget(self.combo_bg_color)

        self.btn_custom_bg = QPushButton("🎨")
        self.btn_custom_bg.setToolTip("Pick custom background color dialog")
        self.btn_custom_bg.setFixedWidth(30)
        self.btn_custom_bg.clicked.connect(self._pick_custom_bg_color)
        details_bar.addWidget(self.btn_custom_bg)

        right_layout.addLayout(details_bar)

        # Tabs: 3D Viewport, Textures Gallery & Animation Clips
        self.tabs = QTabWidget()

        # Tab 1: 3D Viewport + Bottom Animation Player Bar
        viewport_container = QWidget()
        viewport_layout = QVBoxLayout(viewport_container)
        viewport_layout.setContentsMargins(0, 0, 0, 0)
        viewport_layout.setSpacing(0)

        self.viewer = GLViewer()
        self.viewer.on_anim_frame_changed = self._on_anim_frame_tick
        self.viewer.object_selected.connect(self._on_viewer_object_picked)
        self.viewer.transform_changed.connect(self._on_viewer_transform_changed)
        self.viewer.mode_changed.connect(self._on_viewer_mode_changed)
        viewport_layout.addWidget(self.viewer, 1)

        # Bottom Animation Playback Bar (docked below 3D viewport)
        self.anim_bar = QWidget()
        self.anim_bar.setStyleSheet("""
            QWidget#AnimBar {
                background: #171821;
                border-top: 1px solid #2d303e;
            }
            QPushButton {
                background: #2b2d3a;
                border: 1px solid #3d4154;
                border-radius: 4px;
                color: #e0e0e0;
                padding: 4px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #3a3d4f;
                border-color: #64b5f6;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #2b2d3a;
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: #e57373;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #ffcdd2;
                border: 1px solid #e57373;
                width: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }
        """)
        self.anim_bar.setObjectName("AnimBar")
        anim_bar_layout = QHBoxLayout(self.anim_bar)
        anim_bar_layout.setContentsMargins(10, 6, 10, 6)
        anim_bar_layout.setSpacing(8)

        self.btn_anim_play = QPushButton("▶ Play")
        self.btn_anim_play.setToolTip("Play or pause character animation")
        self.btn_anim_play.clicked.connect(self._toggle_anim_play)
        anim_bar_layout.addWidget(self.btn_anim_play)

        self.btn_anim_stop = QPushButton("⏹ Stop")
        self.btn_anim_stop.setToolTip("Reset animation to frame 0")
        self.btn_anim_stop.clicked.connect(self._stop_anim)
        anim_bar_layout.addWidget(self.btn_anim_stop)

        self.chk_anim_loop = QCheckBox("🔁 Loop")
        self.chk_anim_loop.setChecked(True)
        self.chk_anim_loop.toggled.connect(self.viewer.set_anim_loop)
        anim_bar_layout.addWidget(self.chk_anim_loop)

        anim_bar_layout.addWidget(QLabel("|"))
        anim_bar_layout.addWidget(QLabel("🎬 Clip:"))

        self.combo_anim_clip = QComboBox()
        self.combo_anim_clip.setMinimumWidth(360)
        self.combo_anim_clip.currentIndexChanged.connect(self._on_anim_clip_changed)
        anim_bar_layout.addWidget(self.combo_anim_clip)

        self.slider_anim_frame = QSlider(Qt.Horizontal)
        self.slider_anim_frame.setRange(0, 100)
        self.slider_anim_frame.setValue(0)
        self.slider_anim_frame.sliderMoved.connect(self._on_anim_slider_moved)
        anim_bar_layout.addWidget(self.slider_anim_frame, 1)

        self.label_anim_frame = QLabel("Frame: 0 / 0 (0.00s)")
        self.label_anim_frame.setStyleSheet("color: #ffb74d; font-family: monospace; font-weight: bold; font-size: 11px;")
        anim_bar_layout.addWidget(self.label_anim_frame)

        anim_bar_layout.addWidget(QLabel("Speed:"))
        self.combo_anim_speed = QComboBox()
        self.combo_anim_speed.addItems(["0.25x", "0.5x", "1.0x", "1.5x", "2.0x"])
        self.combo_anim_speed.setCurrentIndex(2)
        self.combo_anim_speed.currentIndexChanged.connect(self._on_anim_speed_changed)
        anim_bar_layout.addWidget(self.combo_anim_speed)

        self.anim_bar.setVisible(False)
        viewport_layout.addWidget(self.anim_bar)

        self.tabs.addTab(viewport_container, "🎮 3D Level Viewport")

        # Tab 2: Textures Gallery
        self.textures_tab = QWidget()
        tex_layout = QVBoxLayout(self.textures_tab)

        tex_toolbar = QHBoxLayout()
        self.btn_extract_selected_tex = QPushButton("💾 Extract Selected (Original)")
        self.btn_extract_selected_tex.clicked.connect(self._extract_selected_texture_original)
        tex_toolbar.addWidget(self.btn_extract_selected_tex)

        self.btn_extract_all_tex = QPushButton("📦 Extract All (Original DDS/TGA)")
        self.btn_extract_all_tex.setObjectName("ActionBtn")
        self.btn_extract_all_tex.clicked.connect(self._extract_all_textures_original)
        tex_toolbar.addWidget(self.btn_extract_all_tex)

        self.btn_extract_all_png = QPushButton("🖼️ Extract All (PNG)")
        self.btn_extract_all_png.clicked.connect(self._extract_all_textures_png)
        tex_toolbar.addWidget(self.btn_extract_all_png)

        tex_toolbar.addSpacing(15)
        self.tex_search_input = QLineEdit()
        self.tex_search_input.setPlaceholderText("Filter textures by key, format, or asset...")
        self.tex_search_input.textChanged.connect(self._filter_textures_gallery)
        tex_toolbar.addWidget(self.tex_search_input)

        self.tex_count_badge = QLabel("0 textures")
        self.tex_count_badge.setStyleSheet("color: #64b5f6; font-weight: bold; background: #1b1c24; padding: 4px 8px; border-radius: 4px; border: 1px solid #333644;")
        tex_toolbar.addWidget(self.tex_count_badge)

        tex_layout.addLayout(tex_toolbar)

        self.textures_table = QTableWidget()
        self.textures_table.setColumnCount(6)
        self.textures_table.setHorizontalHeaderLabels(["Thumbnail", "Key", "Dimensions", "Original Format", "Source Asset", "File Size"])
        self.textures_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.textures_table.verticalHeader().setDefaultSectionSize(70)
        self.textures_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.textures_table.customContextMenuRequested.connect(self._on_texture_context_menu)
        tex_layout.addWidget(self.textures_table)
        self.tabs.addTab(self.textures_tab, "🖼️ Textures Gallery")

        # Tab 3: Animation Clips Browser
        self.animations_tab = QWidget()
        anim_tab_layout = QVBoxLayout(self.animations_tab)

        anim_toolbar = QHBoxLayout()
        self.btn_play_selected_anim = QPushButton("▶ Play in Viewport")
        self.btn_play_selected_anim.setObjectName("ActionBtn")
        self.btn_play_selected_anim.clicked.connect(self._play_selected_anim_from_tab)
        anim_toolbar.addWidget(self.btn_play_selected_anim)

        anim_toolbar.addSpacing(15)
        self.anim_search_input = QLineEdit()
        self.anim_search_input.setPlaceholderText("Filter clips by character, key, tracks, or frames...")
        self.anim_search_input.textChanged.connect(self._filter_animations_table)
        anim_toolbar.addWidget(self.anim_search_input)

        self.anim_count_badge = QLabel("0 animation clips")
        self.anim_count_badge.setStyleSheet("color: #ffb74d; font-weight: bold; background: #1b1c24; padding: 4px 8px; border-radius: 4px; border: 1px solid #333644;")
        anim_toolbar.addWidget(self.anim_count_badge)

        anim_tab_layout.addLayout(anim_toolbar)

        self.animations_table = QTableWidget()
        self.animations_table.setColumnCount(6)
        self.animations_table.setHorizontalHeaderLabels(
            ["#", "Character", "Clip Key", "Total Frames", "Bone Tracks", "Duration (at 60 FPS)"]
        )
        self.animations_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.animations_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.animations_table.itemDoubleClicked.connect(self._on_anim_table_double_clicked)
        anim_tab_layout.addWidget(self.animations_table)

        self.tabs.addTab(self.animations_tab, "🎬 Animation Clips")

        # Tab 4: AI & Gameplay Scripts (Decompiler & Disassembler)
        self.ai_scripts_tab = QWidget()
        ai_tab_layout = QVBoxLayout(self.ai_scripts_tab)
        ai_tab_layout.setContentsMargins(8, 8, 8, 8)

        ai_top_bar = QHBoxLayout()

        self.btn_scan_all_bf_scripts = QPushButton("🔍 Scan Entire BigFile")
        self.btn_scan_all_bf_scripts.setObjectName("ActionBtn")
        self.btn_scan_all_bf_scripts.setToolTip("Scan and decompile all AI scripts across the opened BigFile")
        self.btn_scan_all_bf_scripts.clicked.connect(self._scan_all_bigfile_scripts)
        ai_top_bar.addWidget(self.btn_scan_all_bf_scripts)

        self.btn_export_selected_script = QPushButton("💾 Export Selected (.jade / .asm)")
        self.btn_export_selected_script.clicked.connect(self._export_selected_script)
        ai_top_bar.addWidget(self.btn_export_selected_script)

        self.btn_export_all_scripts = QPushButton("📦 Export All Scripts...")
        self.btn_export_all_scripts.clicked.connect(self._export_all_scripts)
        ai_top_bar.addWidget(self.btn_export_all_scripts)

        ai_top_bar.addSpacing(15)

        self.ai_script_filter_combo = QComboBox()
        self.ai_script_filter_combo.addItems(["All Scripts", "Functions Only (.ofc)", "Models Only (.omd)"])
        self.ai_script_filter_combo.currentIndexChanged.connect(self._filter_ai_scripts_table)
        ai_top_bar.addWidget(self.ai_script_filter_combo)

        self.ai_search_input = QLineEdit()
        self.ai_search_input.setPlaceholderText("Search scripts by name, key, native functions...")
        self.ai_search_input.textChanged.connect(self._filter_ai_scripts_table)
        ai_top_bar.addWidget(self.ai_search_input)

        self.ai_count_badge = QLabel("0 scripts")
        self.ai_count_badge.setStyleSheet("color: #64b5f6; font-weight: bold; background: #1b1c24; padding: 4px 8px; border-radius: 4px; border: 1px solid #333644;")
        ai_top_bar.addWidget(self.ai_count_badge)

        ai_tab_layout.addLayout(ai_top_bar)

        ai_splitter = QSplitter(Qt.Horizontal)

        # Left panel: Scripts Table
        self.ai_scripts_table = QTableWidget()
        self.ai_scripts_table.setColumnCount(4)
        self.ai_scripts_table.setHorizontalHeaderLabels(["Kind", "Key", "Script / Model Name", "Size"])
        self.ai_scripts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ai_scripts_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.ai_scripts_table.setSelectionMode(QTableWidget.SingleSelection)
        self.ai_scripts_table.itemSelectionChanged.connect(self._on_ai_script_selected)
        ai_splitter.addWidget(self.ai_scripts_table)

        # Right panel: Code & Disassembly Viewer
        right_code_panel = QWidget()
        right_code_layout = QVBoxLayout(right_code_panel)
        right_code_layout.setContentsMargins(0, 0, 0, 0)

        code_header = QHBoxLayout()
        self.ai_script_header_lbl = QLabel("No script selected")
        self.ai_script_header_lbl.setStyleSheet("font-weight: bold; color: #90caf9; font-size: 13px;")
        code_header.addWidget(self.ai_script_header_lbl)
        code_header.addStretch()

        self.btn_copy_ai_code = QPushButton("📋 Copy to Clipboard")
        self.btn_copy_ai_code.clicked.connect(self._copy_ai_script_to_clipboard)
        code_header.addWidget(self.btn_copy_ai_code)

        right_code_layout.addLayout(code_header)

        self.ai_code_tabs = QTabWidget()

        font = QFont("Courier", 11)
        font.setStyleHint(QFont.Monospace)

        self.ai_decompiled_view = QPlainTextEdit()
        self.ai_decompiled_view.setReadOnly(True)
        self.ai_decompiled_view.setFont(font)
        self.ai_decompiled_view.setStyleSheet("background-color: #0f111a; color: #a6accd; border: 1px solid #282a36; line-height: 1.4;")
        self.ai_code_tabs.addTab(self.ai_decompiled_view, "📜 Decompiled Jade Code")

        self.ai_disasm_view = QPlainTextEdit()
        self.ai_disasm_view.setReadOnly(True)
        self.ai_disasm_view.setFont(font)
        self.ai_disasm_view.setStyleSheet("background-color: #0f111a; color: #82aaff; border: 1px solid #282a36; line-height: 1.4;")
        self.ai_code_tabs.addTab(self.ai_disasm_view, "⚙️ Bytecode Disassembly")

        right_code_layout.addWidget(self.ai_code_tabs)
        ai_splitter.addWidget(right_code_panel)

        ai_splitter.setSizes([450, 750])
        ai_tab_layout.addWidget(ai_splitter)

        self.tabs.addTab(self.ai_scripts_tab, "📜 AI & Gameplay Scripts")

        right_layout.addWidget(self.tabs)

        splitter.addWidget(right_panel)
        splitter.setSizes([450, 1050])

        self._create_floating_transform_inspector()

    # ================= ARCHIVE & TREE POPULATION =================

    def _open_bf_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Prince of Persia BigFile Archive", "", "BigFiles (*.bf *.bin);;All Files (*)"
        )
        if path:
            self._load_bf_path(Path(path))

    def _open_bin_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open BIN / WOW / WOL Level File", "", "BIN/WOW/WOL Files (*.bin *.wow *.wol);;All Files (*)"
        )
        if path:
            self._load_standalone_level(Path(path))

    def _load_bf_path(self, path: Path):
        try:
            self.statusBar().showMessage(f"Indexing {path.name}...")
            self.bf_archive = read_bigfile(path)
            wols = self.bf_archive.get_wol_entries()
            wows = self.bf_archive.get_wow_entries()

            self.archive_info_label.setText(
                f"{path.name} (v{self.bf_archive.version})\n"
                f"Total entries: {self.bf_archive.elem_count:,} | WOL Worlds: {len(wols)} | WOW Rooms: {len(wows)}"
            )
            self._populate_file_tree()
            self.statusBar().showMessage(f"Loaded {path.name} — {len(wols)} WOL level worlds, {len(wows)} WOW rooms available")
        except Exception as e:
            QMessageBox.critical(self, "Failed to Open Archive", f"Could not parse {path.name}:\n{e}")

    def _populate_file_tree(self):
        self.file_tree.clear()
        if not self.bf_archive:
            return

        needle = self.filter_edit.text().strip().casefold()

        wol_root = QTreeWidgetItem(["🌍 World Object Lists (WOL Levels)", "", ""])
        wol_root.setForeground(0, QColor("#81c784"))
        wol_root.setFont(0, QFont("Segoe UI", 10, QFont.Bold))

        char_root = QTreeWidgetItem(["👤 Characters & Cast (Prince, Farah, Enemies)", "", ""])
        char_root.setForeground(0, QColor("#80d8ff"))
        char_root.setFont(0, QFont("Segoe UI", 10, QFont.Bold))

        equip_root = QTreeWidgetItem(["⚔️ Weapons & Costumes", "", ""])
        equip_root.setForeground(0, QColor("#ffd54f"))
        equip_root.setFont(0, QFont("Segoe UI", 10, QFont.Bold))

        wow_root = QTreeWidgetItem(["🏛️ World Object Waves (WOW Rooms)", "", ""])
        wow_root.setForeground(0, QColor("#64b5f6"))
        wow_root.setFont(0, QFont("Segoe UI", 10, QFont.Bold))

        dds_root = QTreeWidgetItem(["🎨 UI & Menu Textures (DDS)", "", ""])
        dds_root.setForeground(0, QColor("#e040fb"))
        dds_root.setFont(0, QFont("Segoe UI", 10, QFont.Bold))

        bin_root = QTreeWidgetItem(["📦 Other BIN Assets", "", ""])
        bin_root.setForeground(0, QColor("#ffb74d"))

        other_root = QTreeWidgetItem(["📁 Other Files", "", ""])
        other_root.setForeground(0, QColor("#b0bec5"))

        dds_entries = []
        for entry in self.bf_archive.entries:
            name = entry.name
            size_str = f"{entry.size:,} B"
            kind = level_asset_kind(name)

            if needle and needle not in name.casefold() and needle not in (entry.full_path or "").casefold():
                continue

            item = QTreeWidgetItem([name, size_str, "POP-LZO" if entry.compressed else "Raw"])
            if entry.full_path:
                item.setToolTip(0, entry.full_path)
            item.setData(0, Qt.UserRole, entry)

            if kind == "wol":
                wol_root.addChild(item)
            elif kind == "character":
                char_root.addChild(item)
            elif kind == "equipment":
                equip_root.addChild(item)
            elif kind == "wow":
                wow_root.addChild(item)
            elif name.lower().endswith(".dds"):
                dds_root.addChild(item)
                dds_entries.append(entry)
            elif name.lower().endswith(".bin"):
                bin_root.addChild(item)
            else:
                other_root.addChild(item)

        for root in [wol_root, char_root, equip_root, wow_root, dds_root, bin_root, other_root]:
            if root.childCount() > 0:
                self.file_tree.addTopLevelItem(root)
                root.setExpanded(True)

        # If package archive with textures (like POPData.BF), auto-load textures into Gallery
        if wol_root.childCount() == 0 and wow_root.childCount() == 0 and dds_entries:
            self._load_package_textures(dds_entries)

    def _load_package_textures(self, dds_entries: List[BigFileEntry]):
        """Load and display DDS textures directly from package archives (POPData.BF)."""
        import io
        from PIL import Image
        textures = {}
        blobs = {}
        sources = {}
        for e in dds_entries:
            raw = self.bf_archive.read_entry(e)
            try:
                im = Image.open(io.BytesIO(raw))
                textures[e.key] = im
                blobs[e.key] = (raw, ".dds")
                sources[e.key] = e.name
            except Exception:
                pass
        if textures:
            scene = LevelSceneData(
                name=self.bf_archive.path.name, objects=[], meshes={},
                textures=textures, texture_sources=sources, texture_original_blobs=blobs
            )
            self.current_scene = scene
            self._populate_textures_gallery(scene)
            self.stats_badge.setText(f"{self.bf_archive.path.name} | Textures: {len(textures)}")
            self.tabs.setCurrentIndex(1)  # Switch to Texture Gallery tab

    def _filter_tree(self):
        self._populate_file_tree()

    def _on_tree_item_clicked(self, item: QTreeWidgetItem, column: int):
        entry: Optional[BigFileEntry] = item.data(0, Qt.UserRole)
        if not entry:
            self.btn_load_level.setEnabled(False)
            return

        kind = level_asset_kind(entry.name)
        ext = entry.name.lower().split(".")[-1] if "." in entry.name else ""

        if ext in ("ofc", "fct", "omd", "mdl", "ova", "oin"):
            self.btn_load_level.setEnabled(False)
            self.statusBar().showMessage(f"AI Script '{entry.name}' ({entry.size:,} B). Double-click to view and decompile in AI Scripts tab.")
            return

        if entry.name.lower().endswith(".dds"):
            self.btn_load_level.setEnabled(False)
            self.statusBar().showMessage(f"UI Texture {entry.name} ({entry.size:,} bytes). View in Texture Gallery tab.")
            return

        self.btn_load_level.setEnabled(True)
        type_desc = "World Object List (Complete Level)" if kind == "wol" else (
            "World Object Wave (Room / Character)" if kind == "wow" else "Binary Data"
        )
        self.statusBar().showMessage(f"Selected {entry.name} ({type_desc}, {entry.size:,} bytes). Click 'Load 3D Level' to view.")

    def _on_tree_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        entry: Optional[BigFileEntry] = item.data(0, Qt.UserRole)
        if entry:
            ext = entry.name.lower().split(".")[-1] if "." in entry.name else ""
            if ext in ("ofc", "fct", "omd", "mdl", "ova", "oin"):
                self._load_and_show_ai_entry(entry)
            elif entry.name.lower().endswith(".dds"):
                self.tabs.setCurrentIndex(1)
            else:
                self._load_selected_level()

    # ================= LEVEL LOADING =================

    def _load_selected_level(self):
        item = self.file_tree.currentItem()
        if not item:
            return
        entry: Optional[BigFileEntry] = item.data(0, Qt.UserRole)
        if not entry:
            return

        self.btn_load_level.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.statusBar().showMessage(f"Loading 3D level from {entry.name}...")

        self.load_worker = LevelLoadWorker(self.bf_archive, entry)
        self.load_worker.progress.connect(self._on_load_progress)
        self.load_worker.finished_success.connect(self._on_level_loaded)
        self.load_worker.finished_error.connect(self._on_level_error)
        self.load_worker.start()

    def _load_standalone_level(self, path: Path):
        self.btn_load_level.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.statusBar().showMessage(f"Loading standalone level {path.name}...")

        self.load_worker = LevelLoadWorker(self.bf_archive, None, raw_path=path)
        self.load_worker.progress.connect(self._on_load_progress)
        self.load_worker.finished_success.connect(self._on_level_loaded)
        self.load_worker.finished_error.connect(self._on_level_error)
        self.load_worker.start()

    def _on_load_progress(self, msg: str):
        self.statusBar().showMessage(msg)

    def _on_level_loaded(self, scene: LevelSceneData):
        self.progress_bar.setVisible(False)
        self.btn_load_level.setEnabled(True)
        self.btn_spawn_char.setEnabled(True)
        self.current_scene = scene

        # Set viewer scene
        self.viewer.set_level(scene)

        # Update stats
        total_poly = sum(len(m.faces) for m in scene.meshes.values())
        total_verts = sum(len(m.vertices) for m in scene.meshes.values())
        stats_text = (
            f"Level: {scene.name} | "
            f"Objects: {len(scene.objects):,} | "
            f"Meshes: {len(scene.meshes):,} | "
            f"Polygons: {total_poly:,} | "
            f"Textures: {len(scene.textures)}"
        )
        self.stats_badge.setText(stats_text)
        self.statusBar().showMessage(f"Successfully loaded {scene.name} ({stats_text})")

        # Check if Prince / character model with costumes is loaded
        is_prince = any("prince" in s.casefold() for s in scene.source_assets) or "prince" in scene.name.casefold()
        if is_prince and self.bf_archive:
            costumes = [e for e in self.bf_archive.entries if "princecostume" in e.name.casefold()]
            costumes.sort(key=lambda e: e.name.casefold())
            if len(costumes) > 1:
                self.combo_costume.blockSignals(True)
                self.combo_costume.clear()
                for c in costumes:
                    label = c.name.replace(".bin", "").replace("_wow_", " ")
                    self.combo_costume.addItem(label, c.key)
                for idx, c in enumerate(costumes):
                    if any(c.name in src for src in scene.source_assets):
                        self.combo_costume.setCurrentIndex(idx)
                        break
                self.combo_costume.blockSignals(False)
                self.label_costume_sep.setVisible(True)
                self.label_costume.setVisible(True)
                self.combo_costume.setVisible(True)
            else:
                self.label_costume_sep.setVisible(False)
                self.label_costume.setVisible(False)
                self.combo_costume.setVisible(False)
        else:
            self.label_costume_sep.setVisible(False)
            self.label_costume.setVisible(False)
            self.combo_costume.setVisible(False)

        # Populate hierarchy
        self._populate_scene_objects(scene)

        # Populate textures gallery
        self._populate_textures_gallery(scene)

        # Populate animations
        self._populate_animations_tab(scene)

        # Populate AI scripts
        self._populate_ai_scripts_tab(scene)

        # Switch to 3D Viewport tab
        self.tabs.setCurrentIndex(0)

    def _on_costume_changed(self, idx: int):
        if idx < 0 or not self.bf_archive:
            return
        costume_key = self.combo_costume.itemData(idx)
        prince_entry = next((e for e in self.bf_archive.entries if "prince_wow" in e.name.casefold()), None)
        if not prince_entry:
            prince_entry = next((e for e in self.bf_archive.entries if e.key == costume_key), None)
        if not prince_entry:
            return

        self.btn_load_level.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.statusBar().showMessage(f"Switching costume to {self.combo_costume.currentText()}...")

        self.load_worker = LevelLoadWorker(self.bf_archive, prince_entry, selected_costume_key=costume_key)
        self.load_worker.progress.connect(self._on_load_progress)
        self.load_worker.finished_success.connect(self._on_level_loaded)
        self.load_worker.finished_error.connect(self._on_level_error)
        self.load_worker.start()

    def _on_level_error(self, err_msg: str):
        self.progress_bar.setVisible(False)
        self.btn_load_level.setEnabled(True)
        QMessageBox.critical(self, "Level Loading Failed", f"An error occurred while parsing the level:\n{err_msg}")
        self.statusBar().showMessage(f"Error loading level: {err_msg}")

    # ================= SCENE OBJECTS & TEXTURES GALLERY =================

    def _populate_scene_objects(self, scene: LevelSceneData):
        self.objects_tree.clear()
        needle = self.object_search.text().strip().casefold()

        bone_branch = QTreeWidgetItem(["🦴 Skeleton & Bones", "", ""])
        bone_branch.setForeground(0, QColor("#00e5ff"))
        bone_branch.setFont(0, QFont("Segoe UI", 9, QFont.Bold))

        char_branch = QTreeWidgetItem(["👤 Character Nodes", "", ""])
        char_branch.setForeground(0, QColor("#80d8ff"))
        char_branch.setFont(0, QFont("Segoe UI", 9, QFont.Bold))

        mesh_branch = QTreeWidgetItem(["🧱 Meshes & Architecture", "", ""])
        mesh_branch.setForeground(0, QColor("#81c784"))
        mesh_branch.setFont(0, QFont("Segoe UI", 9, QFont.Bold))

        light_branch = QTreeWidgetItem(["💡 Lights & Visual FX", "", ""])
        light_branch.setForeground(0, QColor("#fff176"))

        trig_branch = QTreeWidgetItem(["🎯 Triggers & Logic", "", ""])
        trig_branch.setForeground(0, QColor("#4dd0e1"))

        other_branch = QTreeWidgetItem(["📁 Other Objects", "", ""])
        other_branch.setForeground(0, QColor("#b0bec5"))

        for obj in scene.objects:
            if needle and needle not in obj.name.casefold():
                continue
            pos_str = f"({obj.position[0]:.1f}, {obj.position[1]:.1f}, {obj.position[2]:.1f})"
            item = QTreeWidgetItem([obj.name, obj.kind, pos_str])
            item.setData(0, Qt.UserRole, obj)

            if obj.kind == "bone" or obj.name.startswith("B_") or "bone" in obj.name.casefold():
                item.setForeground(0, QColor("#00e5ff"))
                bone_branch.addChild(item)
            elif obj.kind == "character":
                item.setForeground(0, QColor("#80d8ff"))
                char_branch.addChild(item)
            elif obj.kind == "mesh":
                item.setForeground(0, QColor("#81c784"))
                mesh_branch.addChild(item)
            elif obj.kind == "light":
                item.setForeground(0, QColor("#fff176"))
                light_branch.addChild(item)
            elif obj.kind == "trigger":
                item.setForeground(0, QColor("#4dd0e1"))
                trig_branch.addChild(item)
            else:
                other_branch.addChild(item)

        for branch in [bone_branch, char_branch, mesh_branch, light_branch, trig_branch, other_branch]:
            if branch.childCount() > 0:
                self.objects_tree.addTopLevelItem(branch)
                branch.setExpanded(True)

    def _filter_objects(self):
        if self.current_scene:
            self._populate_scene_objects(self.current_scene)

    def _on_object_selected(self, item: QTreeWidgetItem, col: int):
        obj: Optional[LevelObject] = item.data(0, Qt.UserRole)
        if not obj:
            return
        self.viewer.select_object(obj)
        self._sync_inspector_values(obj)

        info = [
            f"<b>{obj.name}</b>",
            f"Kind: {obj.kind} | Key: 0x{obj.key:08X}",
            f"Mesh Key: {hex(obj.mesh_key) if obj.mesh_key else 'None'} | Mat Key: {hex(obj.material_key) if obj.material_key else 'None'}",
            f"Position: ({obj.position[0]:.2f}, {obj.position[1]:.2f}, {obj.position[2]:.2f})",
            f"Scale: ({obj.scale[0]:.2f}, {obj.scale[1]:.2f}, {obj.scale[2]:.2f})",
        ]
        if self.current_scene and self.current_scene.animation_clips:
            info.append(f"<b>Animation Tracks:</b> {len(self.current_scene.animation_clips)} clips in scene")
        self.selection_info.setHtml("<br>".join(info))

    def _on_object_double_clicked(self, item: QTreeWidgetItem, col: int):
        obj: Optional[LevelObject] = item.data(0, Qt.UserRole)
        if obj:
            self.viewer.focus_object(obj)
            self.tabs.setCurrentIndex(0)

    # ================= TRANSFORM INSPECTOR & 3D MANIPULATION =================

    def _create_floating_transform_inspector(self):
        """Create the dedicated floating / movable 3D Transform Inspector dock window."""
        self.dock_transform = QDockWidget("🛠️ Transform Inspector", self)
        self.dock_transform.setObjectName("DockTransformInspector")
        self.dock_transform.setAllowedAreas(
            Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea
        )
        self.dock_transform.setFeatures(
            QDockWidget.DockWidgetMovable |
            QDockWidget.DockWidgetFloatable |
            QDockWidget.DockWidgetClosable
        )

        container = QWidget()
        container.setStyleSheet("background-color: #1e1f2b;")
        t_layout = QVBoxLayout(container)
        t_layout.setContentsMargins(10, 10, 10, 10)
        t_layout.setSpacing(6)

        # Header box with selection banner and Dock/Float quick toggle
        hdr_box = QHBoxLayout()
        self.lbl_selected_title = QLabel("No object selected (Click any object in 3D scene)")
        self.lbl_selected_title.setWordWrap(True)
        self.lbl_selected_title.setStyleSheet(
            "color: #90caf9; font-weight: bold; font-size: 11px; padding: 4px 6px; "
            "background: #171822; border: 1px solid #2d3040; border-radius: 4px;"
        )
        hdr_box.addWidget(self.lbl_selected_title, 1)

        self.btn_dock_toggle = QPushButton("⧉")
        self.btn_dock_toggle.setFixedSize(26, 26)
        self.btn_dock_toggle.setToolTip("Toggle between Floating window and Docked in sidebar")
        self.btn_dock_toggle.setStyleSheet("""
            QPushButton {
                background: #2b2d3c;
                border: 1px solid #3d4158;
                border-radius: 3px;
                color: #90caf9;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #3b3e54;
                color: #ffffff;
                border-color: #64b5f6;
            }
        """)
        self.btn_dock_toggle.clicked.connect(self._toggle_inspector_dock)
        hdr_box.addWidget(self.btn_dock_toggle)
        t_layout.addLayout(hdr_box)

        self.transform_controls = QWidget()
        ctrl_layout = QVBoxLayout(self.transform_controls)
        ctrl_layout.setContentsMargins(0, 0, 0, 0)
        ctrl_layout.setSpacing(5)

        spin_style = """
            QDoubleSpinBox {
                background-color: #171822;
                border: 1px solid #36394d;
                border-radius: 3px;
                color: #eceff1;
                font-family: monospace;
                font-size: 11px;
                padding: 2px 4px;
            }
            QDoubleSpinBox:focus {
                border-color: #64b5f6;
            }
        """

        btn_mini_style = """
            QPushButton {
                background: #252837;
                border: 1px solid #3d4158;
                border-radius: 3px;
                color: #b0bec5;
                font-size: 10px;
                padding: 2px 5px;
            }
            QPushButton:hover {
                background: #3b3e54;
                color: #ffffff;
                border-color: #64b5f6;
            }
        """

        # --- Position Row ---
        pos_header = QHBoxLayout()
        pos_header.addWidget(QLabel("📍 <b>Position:</b>"))
        pos_header.addStretch()
        self.btn_reset_pos = QPushButton("↺ 0")
        self.btn_reset_pos.setToolTip("Reset position to (0, 0, 0)")
        self.btn_reset_pos.setStyleSheet(btn_mini_style)
        self.btn_reset_pos.clicked.connect(self._reset_position)
        pos_header.addWidget(self.btn_reset_pos)
        ctrl_layout.addLayout(pos_header)

        pos_row = QHBoxLayout()
        pos_row.setSpacing(3)
        self.spin_pos_x = QDoubleSpinBox()
        self.spin_pos_x.setRange(-99999.0, 99999.0)
        self.spin_pos_x.setDecimals(2)
        self.spin_pos_x.setSingleStep(0.5)
        self.spin_pos_x.setPrefix("X: ")
        self.spin_pos_x.setStyleSheet(spin_style)
        self.spin_pos_x.valueChanged.connect(self._on_inspector_transform_edited)
        pos_row.addWidget(self.spin_pos_x)

        self.spin_pos_y = QDoubleSpinBox()
        self.spin_pos_y.setRange(-99999.0, 99999.0)
        self.spin_pos_y.setDecimals(2)
        self.spin_pos_y.setSingleStep(0.5)
        self.spin_pos_y.setPrefix("Y: ")
        self.spin_pos_y.setStyleSheet(spin_style)
        self.spin_pos_y.valueChanged.connect(self._on_inspector_transform_edited)
        pos_row.addWidget(self.spin_pos_y)

        self.spin_pos_z = QDoubleSpinBox()
        self.spin_pos_z.setRange(-99999.0, 99999.0)
        self.spin_pos_z.setDecimals(2)
        self.spin_pos_z.setSingleStep(0.5)
        self.spin_pos_z.setPrefix("Z: ")
        self.spin_pos_z.setStyleSheet(spin_style)
        self.spin_pos_z.valueChanged.connect(self._on_inspector_transform_edited)
        pos_row.addWidget(self.spin_pos_z)
        ctrl_layout.addLayout(pos_row)

        # --- Rotation Row ---
        rot_header = QHBoxLayout()
        rot_header.addWidget(QLabel("🔄 <b>Rotation:</b>"))
        rot_header.addStretch()
        self.btn_reset_rot = QPushButton("↺ 0°")
        self.btn_reset_rot.setToolTip("Reset rotation to (0°, 0°, 0°)")
        self.btn_reset_rot.setStyleSheet(btn_mini_style)
        self.btn_reset_rot.clicked.connect(self._reset_rotation)
        rot_header.addWidget(self.btn_reset_rot)
        ctrl_layout.addLayout(rot_header)

        rot_row = QHBoxLayout()
        rot_row.setSpacing(3)
        self.spin_rot_x = QDoubleSpinBox()
        self.spin_rot_x.setRange(-360.0, 360.0)
        self.spin_rot_x.setDecimals(1)
        self.spin_rot_x.setSingleStep(5.0)
        self.spin_rot_x.setPrefix("X: ")
        self.spin_rot_x.setSuffix("°")
        self.spin_rot_x.setStyleSheet(spin_style)
        self.spin_rot_x.valueChanged.connect(self._on_inspector_transform_edited)
        rot_row.addWidget(self.spin_rot_x)

        self.spin_rot_y = QDoubleSpinBox()
        self.spin_rot_y.setRange(-360.0, 360.0)
        self.spin_rot_y.setDecimals(1)
        self.spin_rot_y.setSingleStep(5.0)
        self.spin_rot_y.setPrefix("Y: ")
        self.spin_rot_y.setSuffix("°")
        self.spin_rot_y.setStyleSheet(spin_style)
        self.spin_rot_y.valueChanged.connect(self._on_inspector_transform_edited)
        rot_row.addWidget(self.spin_rot_y)

        self.spin_rot_z = QDoubleSpinBox()
        self.spin_rot_z.setRange(-360.0, 360.0)
        self.spin_rot_z.setDecimals(1)
        self.spin_rot_z.setSingleStep(5.0)
        self.spin_rot_z.setPrefix("Z: ")
        self.spin_rot_z.setSuffix("°")
        self.spin_rot_z.setStyleSheet(spin_style)
        self.spin_rot_z.valueChanged.connect(self._on_inspector_transform_edited)
        rot_row.addWidget(self.spin_rot_z)
        ctrl_layout.addLayout(rot_row)

        # --- Scale Row ---
        scale_header = QHBoxLayout()
        scale_header.addWidget(QLabel("📐 <b>Scale:</b>"))
        scale_header.addStretch()
        self.btn_reset_scale = QPushButton("↺ 1.0")
        self.btn_reset_scale.setToolTip("Reset scale to (1.0, 1.0, 1.0)")
        self.btn_reset_scale.setStyleSheet(btn_mini_style)
        self.btn_reset_scale.clicked.connect(self._reset_scale)
        scale_header.addWidget(self.btn_reset_scale)
        ctrl_layout.addLayout(scale_header)

        scale_row = QHBoxLayout()
        scale_row.setSpacing(3)
        self.spin_scale_x = QDoubleSpinBox()
        self.spin_scale_x.setRange(0.001, 100.0)
        self.spin_scale_x.setDecimals(3)
        self.spin_scale_x.setSingleStep(0.05)
        self.spin_scale_x.setValue(1.0)
        self.spin_scale_x.setPrefix("X: ")
        self.spin_scale_x.setStyleSheet(spin_style)
        self.spin_scale_x.valueChanged.connect(self._on_scale_x_changed)
        scale_row.addWidget(self.spin_scale_x)

        self.spin_scale_y = QDoubleSpinBox()
        self.spin_scale_y.setRange(0.001, 100.0)
        self.spin_scale_y.setDecimals(3)
        self.spin_scale_y.setSingleStep(0.05)
        self.spin_scale_y.setValue(1.0)
        self.spin_scale_y.setPrefix("Y: ")
        self.spin_scale_y.setStyleSheet(spin_style)
        self.spin_scale_y.valueChanged.connect(self._on_scale_y_changed)
        scale_row.addWidget(self.spin_scale_y)

        self.spin_scale_z = QDoubleSpinBox()
        self.spin_scale_z.setRange(0.001, 100.0)
        self.spin_scale_z.setDecimals(3)
        self.spin_scale_z.setSingleStep(0.05)
        self.spin_scale_z.setValue(1.0)
        self.spin_scale_z.setPrefix("Z: ")
        self.spin_scale_z.setStyleSheet(spin_style)
        self.spin_scale_z.valueChanged.connect(self._on_scale_z_changed)
        scale_row.addWidget(self.spin_scale_z)
        ctrl_layout.addLayout(scale_row)

        # --- Options Checkboxes ---
        opts_layout = QVBoxLayout()
        opts_layout.setSpacing(3)

        self.chk_uniform_scale = QCheckBox("🔗 Uniform Scale")
        self.chk_uniform_scale.setChecked(True)
        self.chk_uniform_scale.setToolTip("Keep X, Y, and Z scale in sync when editing values")
        opts_layout.addWidget(self.chk_uniform_scale)

        self.chk_whole_char = QCheckBox("👥 Transform Whole Character Group")
        self.chk_whole_char.setChecked(True)
        self.chk_whole_char.setToolTip(
            "When checked, moving, rotating, or scaling any modular part (torso, hair, weapon, bone) "
            "moves all parts and skeleton of the character together in sync."
        )
        self.chk_whole_char.toggled.connect(lambda chk: self.viewer.set_move_whole_character(chk))
        opts_layout.addWidget(self.chk_whole_char)

        ctrl_layout.addLayout(opts_layout)

        t_layout.addWidget(self.transform_controls)
        self.transform_controls.setEnabled(False)

        self.dock_transform.setWidget(container)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_transform)
        self.dock_transform.setFloating(True)
        self.dock_transform.resize(320, 380)
        self.dock_transform.move(self.x() + 450, self.y() + 150)

    def _toggle_inspector_dock(self):
        """Toggle inspector between floating freely and docked."""
        self.dock_transform.setFloating(not self.dock_transform.isFloating())

    def _toggle_inspector_visibility(self):
        """Show or hide the floating Transform Inspector."""
        self.dock_transform.setVisible(not self.dock_transform.isVisible())
        if self.dock_transform.isVisible():
            self.dock_transform.raise_()
            self.dock_transform.activateWindow()

    def _sync_inspector_values(self, obj: Optional[LevelObject]):
        """Synchronize transform inspector spinboxes with an object's current transform."""
        if not obj:
            self.lbl_selected_title.setText("No object selected (Click any object in 3D scene)")
            self.transform_controls.setEnabled(False)
            return

        self._updating_inspector = True
        try:
            self.lbl_selected_title.setText(f"🎯 <b>{obj.name}</b> ({obj.kind})")
            self.transform_controls.setEnabled(True)
            self.spin_pos_x.setValue(obj.position[0])
            self.spin_pos_y.setValue(obj.position[1])
            self.spin_pos_z.setValue(obj.position[2])

            self.spin_rot_x.setValue(obj.rotation[0])
            self.spin_rot_y.setValue(obj.rotation[1])
            self.spin_rot_z.setValue(obj.rotation[2])

            self.spin_scale_x.setValue(obj.scale[0])
            self.spin_scale_y.setValue(obj.scale[1])
            self.spin_scale_z.setValue(obj.scale[2])
        finally:
            self._updating_inspector = False

    def _on_viewer_object_picked(self, obj: Optional[LevelObject]):
        """Handle object selected directly by 3D click in the viewport."""
        if not obj:
            if self.viewer.selected_object:
                self.viewer.select_object(None)
            self._sync_inspector_values(None)
            self.selection_info.clear()
            return

        if self.viewer.selected_object is not obj:
            self.viewer.selected_object = obj

        if self.btn_tool_select.isChecked():
            self.btn_tool_move.setChecked(True)
            self.viewer.set_transform_mode("translate")

        self._sync_inspector_values(obj)

        info = [
            f"<b>{obj.name}</b>",
            f"Kind: {obj.kind} | Key: 0x{obj.key:08X}",
            f"Mesh Key: {hex(obj.mesh_key) if obj.mesh_key else 'None'} | Mat Key: {hex(obj.material_key) if obj.material_key else 'None'}",
            f"Position: ({obj.position[0]:.2f}, {obj.position[1]:.2f}, {obj.position[2]:.2f})",
            f"Scale: ({obj.scale[0]:.2f}, {obj.scale[1]:.2f}, {obj.scale[2]:.2f})",
        ]
        if self.current_scene and self.current_scene.animation_clips:
            info.append(f"<b>Animation Tracks:</b> {len(self.current_scene.animation_clips)} clips in scene")
        self.selection_info.setHtml("<br>".join(info))

        self._select_tree_item_for_object(obj)
        self.statusBar().showMessage(f"Selected: {obj.name} ({obj.kind}) at ({obj.position[0]:.1f}, {obj.position[1]:.1f}, {obj.position[2]:.1f})")

    def _on_viewer_transform_changed(self, obj: LevelObject):
        """Update inspector spinboxes and hierarchy tree in real time as gizmo is dragged."""
        if not obj:
            return
        self._sync_inspector_values(obj)

        info = [
            f"<b>{obj.name}</b>",
            f"Kind: {obj.kind} | Key: 0x{obj.key:08X}",
            f"Mesh Key: {hex(obj.mesh_key) if obj.mesh_key else 'None'} | Mat Key: {hex(obj.material_key) if obj.material_key else 'None'}",
            f"Position: ({obj.position[0]:.2f}, {obj.position[1]:.2f}, {obj.position[2]:.2f})",
            f"Scale: ({obj.scale[0]:.2f}, {obj.scale[1]:.2f}, {obj.scale[2]:.2f})",
        ]
        if self.current_scene and self.current_scene.animation_clips:
            info.append(f"<b>Animation Tracks:</b> {len(self.current_scene.animation_clips)} clips in scene")
        self.selection_info.setHtml("<br>".join(info))

        self._update_tree_item_pos(obj)
        self.statusBar().showMessage(
            f"Transformed {obj.name}: Pos=({obj.position[0]:.1f}, {obj.position[1]:.1f}, {obj.position[2]:.1f}), "
            f"Rot=({obj.rotation[0]:.0f}°, {obj.rotation[1]:.0f}°, {obj.rotation[2]:.0f}°), "
            f"Scale=({obj.scale[0]:.2f}, {obj.scale[1]:.2f}, {obj.scale[2]:.2f})"
        )

    def _on_viewer_mode_changed(self, mode: str):
        """Keep toolbar mode buttons in sync when mode changes via hotkeys."""
        self.btn_tool_select.blockSignals(True)
        self.btn_tool_move.blockSignals(True)
        self.btn_tool_rotate.blockSignals(True)
        self.btn_tool_scale.blockSignals(True)
        try:
            self.btn_tool_select.setChecked(mode == "select")
            self.btn_tool_move.setChecked(mode == "translate")
            self.btn_tool_rotate.setChecked(mode == "rotate")
            self.btn_tool_scale.setChecked(mode == "scale")
        finally:
            self.btn_tool_select.blockSignals(False)
            self.btn_tool_move.blockSignals(False)
            self.btn_tool_rotate.blockSignals(False)
            self.btn_tool_scale.blockSignals(False)

    def _on_inspector_transform_edited(self):
        """Apply precision transform edited from inspector spinboxes."""
        if self._updating_inspector or not self.viewer.selected_object:
            return
        pos = (self.spin_pos_x.value(), self.spin_pos_y.value(), self.spin_pos_z.value())
        rot = (self.spin_rot_x.value(), self.spin_rot_y.value(), self.spin_rot_z.value())
        scale = (self.spin_scale_x.value(), self.spin_scale_y.value(), self.spin_scale_z.value())
        self.viewer.set_selected_object_transform(pos, rot, scale)
        self._update_tree_item_pos(self.viewer.selected_object)

    def _on_scale_x_changed(self, val: float):
        if self._updating_inspector:
            return
        if self.chk_uniform_scale.isChecked():
            self._updating_inspector = True
            try:
                self.spin_scale_y.setValue(val)
                self.spin_scale_z.setValue(val)
            finally:
                self._updating_inspector = False
        self._on_inspector_transform_edited()

    def _on_scale_y_changed(self, val: float):
        if self._updating_inspector:
            return
        if self.chk_uniform_scale.isChecked():
            self._updating_inspector = True
            try:
                self.spin_scale_x.setValue(val)
                self.spin_scale_z.setValue(val)
            finally:
                self._updating_inspector = False
        self._on_inspector_transform_edited()

    def _on_scale_z_changed(self, val: float):
        if self._updating_inspector:
            return
        if self.chk_uniform_scale.isChecked():
            self._updating_inspector = True
            try:
                self.spin_scale_x.setValue(val)
                self.spin_scale_y.setValue(val)
            finally:
                self._updating_inspector = False
        self._on_inspector_transform_edited()

    def _reset_position(self):
        if not self.viewer.selected_object:
            return
        self.spin_pos_x.setValue(0.0)
        self.spin_pos_y.setValue(0.0)
        self.spin_pos_z.setValue(0.0)
        self._on_inspector_transform_edited()

    def _reset_rotation(self):
        if not self.viewer.selected_object:
            return
        self.spin_rot_x.setValue(0.0)
        self.spin_rot_y.setValue(0.0)
        self.spin_rot_z.setValue(0.0)
        self._on_inspector_transform_edited()

    def _reset_scale(self):
        if not self.viewer.selected_object:
            return
        self.spin_scale_x.setValue(1.0)
        self.spin_scale_y.setValue(1.0)
        self.spin_scale_z.setValue(1.0)
        self._on_inspector_transform_edited()

    def _select_tree_item_for_object(self, target_obj: LevelObject):
        """Highlight and scroll to target_obj in the hierarchy tree."""
        for i in range(self.objects_tree.topLevelItemCount()):
            top = self.objects_tree.topLevelItem(i)
            for j in range(top.childCount()):
                child = top.child(j)
                if child.data(0, Qt.UserRole) is target_obj:
                    self.objects_tree.blockSignals(True)
                    self.objects_tree.setCurrentItem(child)
                    self.objects_tree.scrollToItem(child)
                    self.objects_tree.blockSignals(False)
                    return

    def _update_tree_item_pos(self, target_obj: LevelObject):
        """Update position string in the hierarchy tree column 2."""
        pos_str = f"({target_obj.position[0]:.1f}, {target_obj.position[1]:.1f}, {target_obj.position[2]:.1f})"
        for i in range(self.objects_tree.topLevelItemCount()):
            top = self.objects_tree.topLevelItem(i)
            for j in range(top.childCount()):
                child = top.child(j)
                if child.data(0, Qt.UserRole) is target_obj:
                    child.setText(2, pos_str)
                    return

    def _populate_textures_gallery(self, scene: LevelSceneData):
        self.textures_table.setRowCount(len(scene.textures))
        self.tex_count_badge.setText(f"{len(scene.textures)} textures")
        for row, (key, img) in enumerate(scene.textures.items()):
            try:
                rgba = img.convert("RGBA")
                qimg = QImage(rgba.tobytes(), rgba.width, rgba.height, QImage.Format_RGBA8888)
                pixmap = QPixmap.fromImage(qimg).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_label = QLabel()
                icon_label.setPixmap(pixmap)
                icon_label.setAlignment(Qt.AlignCenter)
                self.textures_table.setCellWidget(row, 0, icon_label)
            except Exception:
                self.textures_table.setItem(row, 0, QTableWidgetItem("N/A"))

            key_item = QTableWidgetItem(f"0x{key:08X}")
            key_item.setData(Qt.UserRole, key)
            self.textures_table.setItem(row, 1, key_item)

            self.textures_table.setItem(row, 2, QTableWidgetItem(f"{img.width} x {img.height}"))

            tex_info = scene.texture_infos.get(key)
            blob_info = scene.texture_original_blobs.get(key)
            ext = blob_info[1].upper() if blob_info else ""
            fmt_str = f"{tex_info.format} ({ext})" if tex_info else (f"DDS ({ext})" if ext == ".DDS" else f"TGA ({ext})")
            self.textures_table.setItem(row, 3, QTableWidgetItem(fmt_str))

            source_name = scene.texture_sources.get(key, scene.name)
            self.textures_table.setItem(row, 4, QTableWidgetItem(source_name))

            if blob_info:
                size_bytes = len(blob_info[0])
                size_str = f"{size_bytes / 1024:.1f} KB" if size_bytes >= 1024 else f"{size_bytes} B"
            else:
                size_str = f"{(img.width * img.height * 4) // 1024:,} KB"
            self.textures_table.setItem(row, 5, QTableWidgetItem(size_str))

    def _filter_textures_gallery(self):
        query = self.tex_search_input.text().strip().casefold()
        visible_count = 0
        for row in range(self.textures_table.rowCount()):
            if not query:
                self.textures_table.setRowHidden(row, False)
                visible_count += 1
                continue
            match = False
            for col in (1, 3, 4):  # Key, Format, Source Asset
                item = self.textures_table.item(row, col)
                if item and query in item.text().casefold():
                    match = True
                    break
            self.textures_table.setRowHidden(row, not match)
            if match:
                visible_count += 1
        total = self.textures_table.rowCount()
        self.tex_count_badge.setText(f"{visible_count}/{total} textures" if query else f"{total} textures")

    def _extract_selected_texture_original(self):
        if not self.current_scene or not self.current_scene.textures:
            QMessageBox.information(self, "Extract Texture", "No level or textures currently loaded.")
            return

        row = self.textures_table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Extract Texture", "Please select a texture from the table first.")
            return

        key_item = self.textures_table.item(row, 1)
        if not key_item:
            return
        key = key_item.data(Qt.UserRole)
        blob_info = self.current_scene.texture_original_blobs.get(key)
        if not blob_info:
            QMessageBox.warning(self, "Extract Texture", f"Original format data not available for texture 0x{key:08X}.")
            return

        blob, ext = blob_info
        suggested_name = f"tex_0x{key:08X}{ext}"
        filter_str = f"Native Texture (*{ext});;All Files (*)"
        out_path, _ = QFileDialog.getSaveFileName(self, "Extract Texture in Original Format", suggested_name, filter_str)
        if not out_path:
            return

        try:
            Path(out_path).write_bytes(blob)
            self.statusBar().showMessage(f"Extracted 0x{key:08X} in original format ({ext.upper()}) to {out_path}", 6000)
            QMessageBox.information(self, "Extraction Successful", f"Saved texture in original format ({ext.upper()}):\n{out_path}")
        except Exception as e:
            QMessageBox.critical(self, "Extraction Failed", f"Failed to write file:\n{e}")

    def _extract_single_texture_png(self, key: int):
        img = self.current_scene.textures.get(key)
        if not img:
            return
        out_path, _ = QFileDialog.getSaveFileName(
            self, "Extract Texture as PNG", f"tex_0x{key:08X}_{img.width}x{img.height}.png", "PNG Image (*.png)"
        )
        if out_path:
            try:
                img.save(out_path, "PNG")
                self.statusBar().showMessage(f"Saved texture 0x{key:08X} as PNG to {out_path}", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Extraction Failed", f"Could not save PNG:\n{e}")

    def _extract_all_textures_original(self):
        if not self.current_scene or not self.current_scene.textures:
            QMessageBox.information(self, "Extract All Textures", "No level or textures currently loaded.")
            return

        dest_dir = QFileDialog.getExistingDirectory(self, "Select Directory to Extract All Textures (Original Format)")
        if not dest_dir:
            return

        dest_path = Path(dest_dir) / f"{self.current_scene.name}_textures_original"
        dest_path.mkdir(parents=True, exist_ok=True)

        extracted_count = 0
        for key, blob_info in self.current_scene.texture_original_blobs.items():
            blob, ext = blob_info
            tex_info = self.current_scene.texture_infos.get(key)
            dims = f"_{tex_info.width}x{tex_info.height}" if tex_info else ""
            out_file = dest_path / f"tex_0x{key:08X}{dims}{ext}"
            out_file.write_bytes(blob)
            extracted_count += 1

        self.statusBar().showMessage(f"Extracted {extracted_count} textures in original format to {dest_path}", 6000)
        QMessageBox.information(
            self, "Extraction Complete",
            f"Successfully extracted {extracted_count} textures in their native format (.dds / .tga) to:\n{dest_path}"
        )

    def _extract_all_textures_png(self):
        if not self.current_scene or not self.current_scene.textures:
            QMessageBox.information(self, "Extract All Textures", "No level or textures currently loaded.")
            return

        dest_dir = QFileDialog.getExistingDirectory(self, "Select Directory to Extract All Textures (PNG)")
        if not dest_dir:
            return

        dest_path = Path(dest_dir) / f"{self.current_scene.name}_textures_png"
        dest_path.mkdir(parents=True, exist_ok=True)

        extracted_count = 0
        for key, img in self.current_scene.textures.items():
            try:
                out_file = dest_path / f"tex_0x{key:08X}_{img.width}x{img.height}.png"
                img.save(out_file, "PNG")
                extracted_count += 1
            except Exception:
                continue

        self.statusBar().showMessage(f"Extracted {extracted_count} textures as PNG to {dest_path}", 6000)
        QMessageBox.information(
            self, "Extraction Complete",
            f"Successfully extracted {extracted_count} textures as PNG to:\n{dest_path}"
        )

    def _on_texture_context_menu(self, pos: QPoint):
        item = self.textures_table.itemAt(pos)
        if not item:
            return
        row = item.row()
        key_item = self.textures_table.item(row, 1)
        if not key_item:
            return
        key = key_item.data(Qt.UserRole)

        menu = QMenu(self)
        act_orig = menu.addAction(f"💾 Extract 0x{key:08X} in Original Format (.dds / .tga)...")
        act_orig.triggered.connect(self._extract_selected_texture_original)

        act_png = menu.addAction(f"🖼️ Extract 0x{key:08X} as PNG...")
        act_png.triggered.connect(lambda: self._extract_single_texture_png(key))

        menu.addSeparator()
        act_copy = menu.addAction("📋 Copy Texture Key (Hex)")
        act_copy.triggered.connect(lambda: QApplication.clipboard().setText(f"0x{key:08X}"))

        menu.exec(self.textures_table.viewport().mapToGlobal(pos))

    def _on_file_tree_context_menu(self, pos: QPoint):
        item = self.file_tree.itemAt(pos)
        if not item:
            return
        entry: Optional[BigFileEntry] = item.data(0, Qt.UserRole)
        if not entry:
            return

        menu = QMenu(self)
        act_load = menu.addAction("🎮 Load as 3D Level")
        act_load.triggered.connect(self._load_selected_level)

        kind = level_asset_kind(entry.name)
        if kind == "character" or "_wow" in entry.name.casefold():
            act_spawn = menu.addAction(f"👤 Spawn {entry.name} into Current Level...")
            act_spawn.triggered.connect(lambda: self._open_spawn_character_dialog(default_entry=entry))

        menu.addSeparator()
        act_ext_orig = menu.addAction("💾 Extract Textures in Original Format (.dds / .tga)...")
        act_ext_orig.triggered.connect(lambda: self._extract_textures_from_entry(entry, original_format=True))

        act_ext_png = menu.addAction("🖼️ Extract Textures as PNG...")
        act_ext_png.triggered.connect(lambda: self._extract_textures_from_entry(entry, original_format=False))

        menu.addSeparator()
        act_uncook = menu.addAction("⚡ Uncook into Development Assets (.gao, .gro, .wow)...")
        act_uncook.triggered.connect(lambda: self._uncook_entry(entry))

        menu.exec(self.file_tree.viewport().mapToGlobal(pos))

    def _uncook_selected_level(self):
        item = self.file_tree.currentItem()
        if not item:
            QMessageBox.information(self, "No Selection", "Please select a level or room in the tree to uncook.")
            return
        entry: Optional[BigFileEntry] = item.data(0, Qt.UserRole)
        if not entry:
            return
        self._uncook_entry(entry)

    def _uncook_entry(self, entry: BigFileEntry):
        if not self.bf_archive:
            return
        dest_dir = QFileDialog.getExistingDirectory(self, f"Select Output Folder to Uncook {entry.name}")
        if not dest_dir:
            return
        try:
            from tools.uncook_bigfile import uncook_bin_data
            self.statusBar().showMessage(f"Uncooking {entry.name}...")
            raw_data = self.bf_archive.read_entry(entry)
            stem = Path(entry.name).stem
            out_folder = Path(dest_dir) / stem
            out_folder.mkdir(parents=True, exist_ok=True)
            assets = uncook_bin_data(raw_data, entry.name)
            for a in assets:
                with open(out_folder / a["filename"], "wb") as f:
                    f.write(a["payload"])
            self.statusBar().showMessage(f"Uncooked {len(assets)} assets to {out_folder.name}", 6000)
            QMessageBox.information(
                self, "Uncooking Complete",
                f"Successfully reversed {entry.name} into {len(assets)} uncooked assets (.gao, .gro, .grm, .wow):\n{out_folder}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Uncooking Error", f"Failed to uncook {entry.name}:\n{e}")

    def _uncook_entire_bigfile(self):
        if not self.bf_archive:
            QMessageBox.information(self, "No Archive", "Please open a BigFile archive first.")
            return
        dest_dir = QFileDialog.getExistingDirectory(self, "Select Output Folder for Full Uncooked Archive")
        if not dest_dir:
            return
        try:
            from tools.uncook_bigfile import uncook_archive
            self.statusBar().showMessage(f"Uncooking all {len(self.bf_archive.entries)} entries to {dest_dir}...")
            uncook_archive(self.bf_archive.path, Path(dest_dir))
            self.statusBar().showMessage(f"Finished uncooking entire archive to {dest_dir}", 8000)
            QMessageBox.information(
                self, "Full Uncook Complete",
                f"Successfully reversed entire {self.bf_archive.path.name} into loose development assets (.gao, .gro, .grm, .wow, .wol):\n{dest_dir}\n\nA master manifest 'uncooked_manifest.json' was generated."
            )
        except Exception as e:
            QMessageBox.critical(self, "Uncooking Error", f"Failed to uncook archive:\n{e}")

    def _extract_textures_from_entry(self, entry: BigFileEntry, original_format: bool):
        if not self.bf_archive:
            return
        dest_dir = QFileDialog.getExistingDirectory(self, f"Select Output Folder for Textures from {entry.name}")
        if not dest_dir:
            return

        try:
            self.statusBar().showMessage(f"Reading {entry.name}...")
            raw_data = self.bf_archive.read_entry(entry)
            stem = entry.name.replace(".bin", "").replace(".wow", "").replace(".wol", "")
            out_folder = Path(dest_dir) / f"{stem}_textures"
            results = extract_all_textures(raw_data, out_folder, prefix=f"{stem}_", include_png=not original_format)

            if not results:
                QMessageBox.information(self, "No Textures", f"No embedded textures found in {entry.name}.")
                return

            ext_label = "original format (.dds / .tga)" if original_format else "PNG"
            self.statusBar().showMessage(f"Extracted {len(results)} textures from {entry.name}", 6000)
            QMessageBox.information(
                self, "Extraction Complete",
                f"Extracted {len(results)} textures in {ext_label} to:\n{out_folder}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Extraction Error", f"Failed to extract textures from {entry.name}:\n{e}")

    # ================= VIEW & TOOLBAR ACTIONS =================

    def _update_viewer_options(self):
        self.viewer.show_textures = self.chk_textures.isChecked()
        self.viewer.show_meshes = self.chk_meshes.isChecked()
        self.viewer.show_wireframe = self.chk_wireframe.isChecked()
        self.viewer.show_objects = self.chk_objects.isChecked()
        self.viewer.show_bones = self.chk_bones.isChecked()
        self.viewer.enable_fog = self.chk_fog.isChecked()
        self.viewer.cull_backfaces = not self.chk_two_sided.isChecked()

        idx = self.combo_lighting.currentIndex()
        modes = ["ingame", "golden", "studio", "unlit"]
        self.viewer.lighting_mode = modes[idx] if 0 <= idx < len(modes) else "ingame"
        self.viewer.enable_lighting = (self.viewer.lighting_mode != "unlit")

        self.viewer.update()

    def _reset_camera(self):
        self.viewer.frame_level()
        self.viewer.update()

    def _toggle_wireframe_menu(self, checked: bool):
        self.chk_wireframe.setChecked(checked)

    def _toggle_textures_menu(self, checked: bool):
        self.chk_textures.setChecked(checked)

    def _toggle_scene_animation(self, checked: bool):
        self.viewer.set_scene_animation(checked)

    def _toggle_turntable(self, checked: bool):
        self.viewer.set_turntable(checked)

    def _on_light_volume_changed(self, value: int):
        factor = value / 100.0
        self.label_light_val.setText(f"{value}%")
        self.viewer.set_light_intensity(factor)

    def _on_bg_color_changed(self, idx: int):
        presets = [
            (0.09, 0.10, 0.14),   # Dark Slate
            (0.00, 0.00, 0.00),   # Pitch Black
            (0.18, 0.14, 0.09),   # Sands Amber
            (0.06, 0.09, 0.16),   # Deep Navy
            (0.22, 0.23, 0.26),   # Neutral Gray
            (0.95, 0.96, 0.98),   # Pure White
        ]
        if idx < len(presets):
            r, g, b = presets[idx]
            self.viewer.set_background_color(r, g, b)
        elif idx == len(presets):  # Custom Color...
            self._pick_custom_bg_color()

    def _pick_custom_bg_color(self):
        curr_r, curr_g, curr_b = self.viewer.bg_color
        initial = QColor(int(curr_r * 255), int(curr_g * 255), int(curr_b * 255))
        color = QColorDialog.getColor(initial, self, "Choose Viewport Background Color")
        if color.isValid():
            r = color.redF()
            g = color.greenF()
            b = color.blueF()
            self.viewer.set_background_color(r, g, b)
            # Update combo text if on a preset
            self.combo_bg_color.blockSignals(True)
            self.combo_bg_color.setCurrentIndex(6)
            self.combo_bg_color.blockSignals(False)

    def _export_to_obj(self):
        if not self.current_scene or not self.current_scene.meshes:
            QMessageBox.information(self, "Export OBJ", "No level is currently loaded to export.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Export Level as Wavefront OBJ", f"{self.current_scene.name}.obj", "OBJ Files (*.obj)")
        if not path:
            return

        try:
            out_file = Path(path)
            lines = [f"# Jade Engine export of {self.current_scene.name}\n"]
            vert_offset = 1

            for obj in self.current_scene.objects:
                mesh_keys = self.current_scene.mesh_links.get(id(obj), [])
                linked = [self.current_scene.meshes[k] for k in mesh_keys if k in self.current_scene.meshes]
                if not linked:
                    continue

                for mesh in linked:
                    lines.append(f"o {obj.name}_mesh_{mesh.key:08X}\n")
                    from jade_engine.level_scene import transformed_vertices
                    world_verts = list(transformed_vertices(mesh.vertices, obj))

                    for vx, vy, vz in world_verts:
                        lines.append(f"v {vx:.5f} {vy:.5f} {vz:.5f}\n")

                    for u, v in mesh.uvs:
                        lines.append(f"vt {u:.5f} {1.0 - v:.5f}\n")

                    for f_idx, face in enumerate(mesh.faces):
                        if len(face) == 3:
                            v0, v1, v2 = (face[i] + vert_offset for i in range(3))
                            if mesh.uv_indices and f_idx < len(mesh.uv_indices):
                                uv0, uv1, uv2 = (mesh.uv_indices[f_idx][i] + vert_offset for i in range(3))
                                lines.append(f"f {v0}/{uv0} {v1}/{uv1} {v2}/{uv2}\n")
                            else:
                                lines.append(f"f {v0} {v1} {v2}\n")

                    vert_offset += len(world_verts)

            out_file.write_text("".join(lines), encoding="utf-8")
            QMessageBox.information(self, "Export Complete", f"Successfully exported level geometry to:\n{out_file}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Failed to export OBJ:\n{e}")

    # ================= ANIMATION PLAYBACK & BROWSER =================

    def _populate_animations_tab(self, scene: LevelSceneData):
        clips: List[AnimationClip] = getattr(scene, "animation_clips", []) or []
        self._all_scene_clips = clips

        self.combo_anim_clip.blockSignals(True)
        self.combo_anim_clip.clear()

        if not clips:
            self.anim_bar.setVisible(False)
            self.animations_table.setRowCount(0)
            self.anim_count_badge.setText("0 animation clips")
            self.combo_anim_clip.blockSignals(False)
            return

        # Show animation toolbar
        self.anim_bar.setVisible(True)
        self.anim_count_badge.setText(f"{len(clips)} animation clips")

        best_index = 0
        max_f = 0
        for idx, clip in enumerate(clips):
            self.combo_anim_clip.addItem(self._clip_selector_label(idx, clip), clip)
            if clip.frames > max_f:
                max_f = clip.frames
                best_index = idx

        self._filter_animations_table()

        # Auto-select the longest multi-frame animation clip
        if clips:
            self.combo_anim_clip.setCurrentIndex(best_index)
            self.viewer.set_active_clip(clips[best_index])
            self.slider_anim_frame.setRange(0, max(0, clips[best_index].frames - 1))
            self.slider_anim_frame.setValue(0)
            self._update_frame_label(0, clips[best_index].frames)

        self.combo_anim_clip.blockSignals(False)

    def _clip_selector_label(self, idx: int, clip: AnimationClip) -> str:
        who = format_clip_character(getattr(clip, "character_group", ""))
        sec = clip.frames / 60.0
        return (
            f"{who}  ·  #{idx + 1}  0x{clip.key:08X}  ·  "
            f"{clip.frames} frames, {len(clip.tracks)} bones, {sec:.2f}s"
        )

    def _filter_animations_table(self):
        query = self.anim_search_input.text().strip().lower()
        clips = getattr(self, "_all_scene_clips", [])
        filtered = []
        for idx, c in enumerate(clips):
            who = format_clip_character(getattr(c, "character_group", ""))
            group = (getattr(c, "character_group", "") or "").lower()
            key_str = f"0x{c.key:08x}"
            haystack = f"{who} {group} {key_str} {c.frames} {len(c.tracks)}"
            if not query or query in haystack.lower():
                filtered.append((idx, c))

        self.animations_table.setRowCount(len(filtered))
        for row, (idx, clip) in enumerate(filtered):
            item_num = QTableWidgetItem(f"#{idx + 1}")
            item_num.setData(Qt.UserRole, clip)
            self.animations_table.setItem(row, 0, item_num)

            item_who = QTableWidgetItem(format_clip_character(getattr(clip, "character_group", "")))
            item_who.setData(Qt.UserRole, clip)
            self.animations_table.setItem(row, 1, item_who)

            item_key = QTableWidgetItem(f"0x{clip.key:08X}")
            item_key.setData(Qt.UserRole, clip)
            self.animations_table.setItem(row, 2, item_key)

            item_frames = QTableWidgetItem(f"{clip.frames} frames")
            self.animations_table.setItem(row, 3, item_frames)

            item_tracks = QTableWidgetItem(f"{len(clip.tracks)} bone tracks")
            self.animations_table.setItem(row, 4, item_tracks)

            sec = clip.frames / 60.0
            item_dur = QTableWidgetItem(f"{sec:.2f} sec")
            self.animations_table.setItem(row, 5, item_dur)

    def _on_anim_clip_changed(self, index: int):
        if index < 0 or not hasattr(self, "_all_scene_clips") or not self._all_scene_clips:
            return
        clip = self.combo_anim_clip.currentData()
        if not clip and 0 <= index < len(self._all_scene_clips):
            clip = self._all_scene_clips[index]
        if clip:
            was_playing = self.viewer.anim_playing
            self.viewer.set_active_clip(clip, activate_mode=was_playing)
            if was_playing:
                self.viewer.set_anim_playing(True)
            self.slider_anim_frame.blockSignals(True)
            self.slider_anim_frame.setRange(0, max(0, clip.frames - 1))
            self.slider_anim_frame.setValue(0)
            self.slider_anim_frame.blockSignals(False)
            self._update_frame_label(0, clip.frames)

    def _toggle_anim_play(self):
        playing = not self.viewer.anim_playing
        self.viewer.set_anim_playing(playing)
        self.btn_anim_play.setText("⏸ Pause" if playing else "▶ Play")

    def _stop_anim(self):
        self.viewer.reset_animation()
        self.btn_anim_play.setText("▶ Play")
        self.slider_anim_frame.blockSignals(True)
        self.slider_anim_frame.setValue(0)
        self.slider_anim_frame.blockSignals(False)
        clip = self.viewer.active_clip
        total = clip.frames if clip else 0
        self._update_frame_label(0, total)

    def _on_anim_slider_moved(self, value: int):
        self.viewer.set_anim_frame(float(value))
        clip = self.viewer.active_clip
        total = clip.frames if clip else 0
        self._update_frame_label(value, total)

    def _on_anim_speed_changed(self, index: int):
        speeds = [0.25, 0.5, 1.0, 1.5, 2.0]
        speed = speeds[index] if 0 <= index < len(speeds) else 1.0
        self.viewer.set_anim_speed(speed)

    def _on_anim_frame_tick(self, frame: float):
        frame_int = int(round(frame))
        self.slider_anim_frame.blockSignals(True)
        self.slider_anim_frame.setValue(frame_int)
        self.slider_anim_frame.blockSignals(False)
        clip = self.viewer.active_clip
        total = clip.frames if clip else 0
        self._update_frame_label(frame_int, total)

    def _update_frame_label(self, current: int, total: int):
        sec = current / 60.0
        self.label_anim_frame.setText(f"Frame: {current} / {total} ({sec:.2f}s)")

    def _on_anim_table_double_clicked(self, item: QTableWidgetItem):
        clip = self.animations_table.item(item.row(), 0).data(Qt.UserRole)
        if clip:
            self._play_clip_in_viewport(clip)

    def _play_selected_anim_from_tab(self):
        selected_rows = self.animations_table.selectionModel().selectedRows()
        if not selected_rows:
            return
        row = selected_rows[0].row()
        clip = self.animations_table.item(row, 0).data(Qt.UserRole)
        if clip:
            self._play_clip_in_viewport(clip)

    def _play_clip_in_viewport(self, clip: AnimationClip):
        clips = getattr(self, "_all_scene_clips", [])
        for idx, c in enumerate(clips):
            if c.key == clip.key:
                self.combo_anim_clip.setCurrentIndex(idx)
                break
        self.viewer.set_active_clip(clip, activate_mode=True)
        self.viewer.set_anim_playing(True)
        self.btn_anim_play.setText("⏸ Pause")
        self.tabs.setCurrentIndex(0)  # Switch to 3D Viewport

    # ================= AI & GAMEPLAY SCRIPTS TAB =================

    def _populate_ai_scripts_tab(self, scene: LevelSceneData):
        scripts: List[Dict[str, Any]] = getattr(scene, "ai_scripts", []) or []
        self._all_ai_scripts = list(scripts)
        self._filter_ai_scripts_table()
        if self._all_ai_scripts:
            self.ai_scripts_table.selectRow(0)

    def _filter_ai_scripts_table(self):
        query = self.ai_search_input.text().strip().lower()
        filter_mode = self.ai_script_filter_combo.currentIndex()  # 0: All, 1: Functions, 2: Models
        all_scripts = getattr(self, "_all_ai_scripts", [])

        filtered = []
        for s in all_scripts:
            kind = s.get("kind", "")
            if filter_mode == 1 and kind != "function":
                continue
            if filter_mode == 2 and kind != "model":
                continue

            name = s.get("name", "").lower()
            key_hex = f"0x{s.get('key', 0):08x}"
            src = s.get("source", "").lower()

            if not query or query in name or query in key_hex or query in src:
                filtered.append(s)

        self._filtered_ai_scripts = filtered
        self.ai_scripts_table.setRowCount(len(filtered))
        self.ai_count_badge.setText(f"{len(filtered)} scripts")

        for row, s in enumerate(filtered):
            kind = s.get("kind", "")
            kind_icon = "📜" if kind == "function" else "🧠"
            kind_text = "Function" if kind == "function" else "Model"

            item_kind = QTableWidgetItem(f"{kind_icon} {kind_text}")
            item_kind.setData(Qt.UserRole, s)
            self.ai_scripts_table.setItem(row, 0, item_kind)

            item_key = QTableWidgetItem(f"0x{s.get('key', 0):08X}")
            self.ai_scripts_table.setItem(row, 1, item_key)

            item_name = QTableWidgetItem(s.get("name", ""))
            self.ai_scripts_table.setItem(row, 2, item_name)

            size_val = s.get("size", 0)
            item_size = QTableWidgetItem(f"{size_val:,} B")
            self.ai_scripts_table.setItem(row, 3, item_size)

        if not filtered:
            self.ai_script_header_lbl.setText("No scripts match current filter")
            self.ai_decompiled_view.setPlainText("// No scripts found.")
            self.ai_disasm_view.setPlainText("// No scripts found.")

    def _on_ai_script_selected(self):
        selected_rows = self.ai_scripts_table.selectionModel().selectedRows()
        if not selected_rows:
            return
        row = selected_rows[0].row()
        item = self.ai_scripts_table.item(row, 0)
        if not item:
            return
        script_info = item.data(Qt.UserRole)
        if not script_info:
            return

        self._current_selected_script = script_info
        kind = script_info.get("kind", "")
        key = script_info.get("key", 0)
        name = script_info.get("name", "")
        source = script_info.get("source", "")

        self.ai_script_header_lbl.setText(f"{name} (Key: 0x{key:08X}) — {source}")

        if kind == "function":
            func: AIFunction = script_info.get("func")
            if func:
                decompiled = decompile_ai_function(func)
                disassembled = disassemble_ai_function(func)
                self.ai_decompiled_view.setPlainText(decompiled)
                self.ai_disasm_view.setPlainText(disassembled)
            else:
                self.ai_decompiled_view.setPlainText("// Unable to parse function.")
                self.ai_disasm_view.setPlainText("// Unable to parse function.")

        elif kind == "model":
            model: AIModel = script_info.get("model")
            if model:
                lines = [
                    f"/*",
                    f" * Jade Engine AI Model Definition",
                    f" * Model: {model.name}",
                    f" * Key: 0x{model.key:08X}",
                    f" * Total Function Tracks: {len(model.function_keys)}",
                    f" * Total Variable Slots: {len(model.var_keys)}",
                    f" */",
                    "",
                    f"model {model.name}",
                    "{",
                    "    // Functions & State Machine Tracks:",
                ]
                for idx, fk in enumerate(model.function_keys):
                    lines.append(f"    track[{idx}] = function 0x{fk:08X};")
                lines.append("")
                lines.append("    // Instance Variables:")
                for idx, vk in enumerate(model.var_keys):
                    lines.append(f"    var[{idx}] = variable 0x{vk:08X};")
                lines.append("}")
                self.ai_decompiled_view.setPlainText("\n".join(lines))

                disasm_lines = [
                    f"// ============================================================================",
                    f"// AI Model: {model.name} (Key: 0x{model.key:08X})",
                    f"// Functions ({len(model.function_keys)}):",
                ]
                for idx, fk in enumerate(model.function_keys):
                    disasm_lines.append(f"  Track[{idx:02d}]: 0x{fk:08X}")
                disasm_lines.append(f"// Variables ({len(model.var_keys)}):")
                for idx, vk in enumerate(model.var_keys):
                    disasm_lines.append(f"  Var[{idx:02d}]: 0x{vk:08X}")
                self.ai_disasm_view.setPlainText("\n".join(disasm_lines))

    def _copy_ai_script_to_clipboard(self):
        curr_tab = self.ai_code_tabs.currentIndex()
        text = self.ai_decompiled_view.toPlainText() if curr_tab == 0 else self.ai_disasm_view.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.statusBar().showMessage("Copied script text to clipboard!", 3000)

    def _export_selected_script(self):
        script_info = getattr(self, "_current_selected_script", None)
        if not script_info:
            QMessageBox.information(self, "Export Script", "Please select a script from the table first.")
            return

        name = script_info.get("name", "script")
        default_name = f"{Path(name).stem}.jade"
        path, _ = QFileDialog.getSaveFileName(self, "Export Decompiled Jade Script", default_name, "Jade Script (*.jade);;Assembly (*.asm);;All Files (*)")
        if not path:
            return

        decompiled = self.ai_decompiled_view.toPlainText()
        disassembled = self.ai_disasm_view.toPlainText()

        out_path = Path(path)
        out_path.write_text(decompiled, encoding="utf-8")

        asm_path = out_path.with_suffix(".asm")
        asm_path.write_text(disassembled, encoding="utf-8")

        self.statusBar().showMessage(f"Exported script to {out_path.name} and {asm_path.name}!", 4000)

    def _export_all_scripts(self):
        scripts = getattr(self, "_all_ai_scripts", [])
        if not scripts:
            QMessageBox.information(self, "Export All Scripts", "No AI scripts currently loaded.")
            return

        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory to Export All Scripts")
        if not dir_path:
            return

        exported = export_decompiled_scripts_to_dir(scripts, dir_path)
        QMessageBox.information(self, "Export Complete", f"Successfully exported {exported} AI scripts (.jade and .asm) to:\n{dir_path}")

    def _scan_all_bigfile_scripts(self):
        if not self.bf_archive:
            QMessageBox.warning(self, "No BigFile Opened", "Please open a BigFile archive first before scanning.")
            return

        self.statusBar().showMessage("Scanning BigFile for all AI scripts and bytecode functions...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        QApplication.processEvents()

        try:
            found = scan_all_ai_scripts_in_archive(self.bf_archive)
            existing_keys = {s.get("key") for s in getattr(self, "_all_ai_scripts", [])}
            added = 0
            for item in found:
                if item.get("key") not in existing_keys:
                    self._all_ai_scripts.append(item)
                    existing_keys.add(item.get("key"))
                    added += 1

            self._filter_ai_scripts_table()
            self.tabs.setCurrentIndex(3)  # Switch to AI Scripts tab
            QMessageBox.information(
                self,
                "BigFile AI Scan Complete",
                f"Scanned {len(found)} scripts from BigFile.\n"
                f"Added {added} new AI scripts to the browser!\n"
                f"Total scripts available: {len(self._all_ai_scripts)}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Scan Error", f"Failed to scan BigFile AI scripts:\n{e}")
        finally:
            self.progress_bar.setVisible(False)
            self.statusBar().showMessage(f"AI Scripts ready ({len(self._all_ai_scripts)} total).", 4000)

    def _load_and_show_ai_entry(self, entry: BigFileEntry):
        if not self.bf_archive:
            return
        try:
            data = self.bf_archive.read_entry(entry)
            ext = entry.name.lower().split(".")[-1] if "." in entry.name else ""

            if ext in ("ofc", "fct"):
                func = parse_ai_function(data, key=entry.key, name=entry.name)
                item = {
                    "kind": "function",
                    "key": entry.key,
                    "name": entry.name,
                    "size": entry.size,
                    "func": func,
                    "source": "BigFile Entry",
                }
            else:
                model = parse_ai_model(data, key=entry.key, name=entry.name)
                item = {
                    "kind": "model",
                    "key": entry.key,
                    "name": entry.name,
                    "size": entry.size,
                    "model": model,
                    "source": "BigFile Entry",
                }

            if not hasattr(self, "_all_ai_scripts"):
                self._all_ai_scripts = []

            existing = next((i for i, s in enumerate(self._all_ai_scripts) if s.get("key") == entry.key), None)
            if existing is None:
                self._all_ai_scripts.insert(0, item)
            self._filter_ai_scripts_table()
            self.tabs.setCurrentIndex(3)  # Switch to AI Scripts tab

            # Select this script in the table
            for row in range(self.ai_scripts_table.rowCount()):
                row_item = self.ai_scripts_table.item(row, 0)
                if row_item and row_item.data(Qt.UserRole).get("key") == entry.key:
                    self.ai_scripts_table.selectRow(row)
                    break
        except Exception as e:
            QMessageBox.warning(self, "AI Script Error", f"Could not load AI script {entry.name}:\n{e}")

    # ================= SPAWN CHARACTER FEATURE =================

    def _on_objects_tree_context_menu(self, pos: QPoint):
        item = self.objects_tree.itemAt(pos)
        if not item:
            return
        obj: Optional[LevelObject] = item.data(0, Qt.UserRole)
        if not obj:
            return

        menu = QMenu(self)
        act_focus = menu.addAction(f"🎯 Focus Camera on {obj.name}")
        act_focus.triggered.connect(lambda: self.viewer.focus_object(obj))

        act_spawn = menu.addAction(f"👤 Spawn Character Here (at {obj.name})...")
        act_spawn.triggered.connect(lambda: self._open_spawn_character_dialog(default_pos=obj.position))

        menu.addSeparator()
        act_copy_pos = menu.addAction(f"📋 Copy Coordinates ({obj.position[0]:.2f}, {obj.position[1]:.2f}, {obj.position[2]:.2f})")
        act_copy_pos.triggered.connect(
            lambda: QApplication.clipboard().setText(f"{obj.position[0]:.2f}, {obj.position[1]:.2f}, {obj.position[2]:.2f}")
        )

        menu.exec(self.objects_tree.viewport().mapToGlobal(pos))

    def _open_spawn_character_dialog(
        self,
        default_entry: Optional[BigFileEntry] = None,
        default_pos: Optional[Tuple[float, float, float]] = None,
    ):
        if not self.current_scene:
            QMessageBox.information(
                self,
                "Spawn Character",
                "Please load a 3D level world (WOL) or room (WOW) first before spawning a character."
            )
            return

        dlg = SpawnCharacterDialog(
            parent=self,
            archive=self.bf_archive,
            scene=self.current_scene,
            selected_obj=self.viewer.selected_object,
            cam_target=self.viewer.target,
            default_entry=default_entry,
            default_pos=default_pos,
        )

        if dlg.exec() == QDialog.Accepted:
            entry = dlg.get_selected_entry()
            raw_path = dlg.get_custom_file_path()
            spawn_pos = dlg.get_spawn_position()
            focus_cam = dlg.get_focus_camera()
            auto_play = dlg.get_auto_play()

            self._execute_spawn_character(
                entry=entry,
                raw_path=raw_path,
                spawn_pos=spawn_pos,
                focus_camera=focus_cam,
                auto_play=auto_play,
            )

    def _execute_spawn_character(
        self,
        entry: Optional[BigFileEntry],
        raw_path: Optional[Path],
        spawn_pos: Tuple[float, float, float],
        focus_camera: bool = True,
        auto_play: bool = True,
    ):
        if not self.current_scene:
            return

        try:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            char_name = entry.name if entry else (raw_path.name if raw_path else "Character")
            self.statusBar().showMessage(f"Spawning {char_name} into level at ({spawn_pos[0]:.1f}, {spawn_pos[1]:.1f}, {spawn_pos[2]:.1f})...")

            if entry and self.bf_archive:
                char_scene = load_level_from_archive(self.bf_archive, entry)
            elif raw_path:
                raw_bytes = raw_path.read_bytes()
                char_scene = load_level_from_raw_data(raw_path.name, raw_bytes, self.bf_archive)
            else:
                raise ValueError("No character asset provided.")

            # Shift all character objects so they are anchored precisely at the target spawn position
            dx, dy, dz = spawn_pos
            for obj in char_scene.objects:
                obj.position = (obj.position[0] + dx, obj.position[1] + dy, obj.position[2] + dz)

            # Merge scene data
            self.current_scene.objects.extend(char_scene.objects)
            self.current_scene.meshes.update(char_scene.meshes)
            self.current_scene.textures.update(char_scene.textures)
            self.current_scene.texture_maps.update(char_scene.texture_maps)
            self.current_scene.color_maps.update(char_scene.color_maps)
            self.current_scene.mesh_links.update(char_scene.mesh_links)
            self.current_scene.texture_infos.update(char_scene.texture_infos)
            self.current_scene.texture_original_blobs.update(char_scene.texture_original_blobs)
            self.current_scene.texture_sources.update(char_scene.texture_sources)
            if char_scene.source_assets:
                self.current_scene.source_assets.extend(char_scene.source_assets)

            # Merge animation clips (prepend new character clips so they are immediately active in viewer)
            new_clips = []
            if char_scene.animation_clips:
                char_group = infer_character_group(char_name) or "prince"
                for c in char_scene.animation_clips:
                    c.character_group = char_group
                existing_keys = {c.key for c in self.current_scene.animation_clips}
                new_clips = [c for c in char_scene.animation_clips if c.key not in existing_keys]
                self.current_scene.animation_clips = new_clips + self.current_scene.animation_clips

            # Incrementally register newly spawned character objects in OpenGL viewport
            self.viewer.add_spawned_character(
                char_scene.objects,
                char_scene.textures,
                focus_pos=spawn_pos if focus_camera else None,
            )

            # Refresh UI trees and tabs
            self._populate_scene_objects(self.current_scene)
            self._populate_animations_tab(self.current_scene)
            self._populate_textures_gallery(self.current_scene)
            self._populate_ai_scripts_tab(self.current_scene)

            # Update stats badge
            total_poly = sum(len(m.faces) for m in self.current_scene.meshes.values())
            self.stats_badge.setText(
                f"Level: {self.current_scene.name} | "
                f"Objects: {len(self.current_scene.objects):,} | "
                f"Meshes: {len(self.current_scene.meshes):,} | "
                f"Polygons: {total_poly:,} | "
                f"Textures: {len(self.current_scene.textures)} | "
                f"Clips: {len(self.current_scene.animation_clips)}"
            )

            # If auto-play requested and clips available, start playback immediately;
            # otherwise keep character in clean upright rest T-shape
            if auto_play and self.current_scene.animation_clips:
                active_clip = new_clips[0] if (char_scene.animation_clips and new_clips) else self.current_scene.animation_clips[0]
                self.viewer.set_active_clip(active_clip, activate_mode=True)
                self.viewer.set_anim_playing(True)
                self.btn_anim_play.setText("⏸ Pause")
            else:
                self.viewer.set_anim_playing(False)
                self.btn_anim_play.setText("▶ Play")

            QApplication.restoreOverrideCursor()
            self.statusBar().showMessage(
                f"✨ Successfully spawned {char_name} at ({spawn_pos[0]:.1f}, {spawn_pos[1]:.1f}, {spawn_pos[2]:.1f}) with {len(char_scene.animation_clips)} clips!",
                10000,
            )
        except Exception as e:
            QApplication.restoreOverrideCursor()
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Spawn Failed", f"Could not spawn character:\n{e}")
            self.statusBar().showMessage(f"Failed to spawn character: {e}")

    def _show_controls_help(self):
        msg = (
            "<h3>3D Viewport & Object Manipulation Controls</h3>"
            "<ul>"
            "<li><b>Left Click on any Object or Character:</b> Directly select it in the 3D scene & Inspector</li>"
            "<li><b>Alt + Left Mouse Drag:</b> Rotate / Orbit camera scene</li>"
            "<li><b>Alt + Right Mouse Drag (or Middle Mouse Drag):</b> Move / Pan camera scene</li>"
            "<li><b>Mouse Scroll Wheel (or Right Drag):</b> Zoom in / out</li>"
            "<li><b>1 Key:</b> Select Mode (Pick objects in scene)</li>"
            "<li><b>2 or G / T Key:</b> Move / Translate Gizmo (Drag Red X, Green Y, Blue Z arrows or Center handle)</li>"
            "<li><b>3 Key:</b> Rotate Gizmo (Drag Red Pitch, Green Roll, Blue Yaw rings)</li>"
            "<li><b>4 Key:</b> Scale Gizmo (Drag Red X, Green Y, Blue Z cubes or Center handle)</li>"
            "<li><b>I Key / 🛠️ Inspector Button:</b> Toggle floating Transform Inspector window</li>"
            "<li><b>Transform Inspector (Floating Window):</b> Freely movable & dockable precision numerical controls for Position, Rotation, Scale, Uniform Scale & Linked Character Grouping</li>"
            "<li><b>F / R Key:</b> Frame entire level or focused object to fit screen</li>"
            "<li><b>W, A, S, D, Q, E Keys:</b> Fly camera navigation</li>"
            "<li><b>Double-click on Object in list:</b> Center camera directly onto that object</li>"
            "</ul>"
        )
        QMessageBox.information(self, "Controls & Navigation", msg)

    def _show_about(self):
        msg = (
            "<h3>Jade Engine 3D Level Editor</h3>"
            "<p>Advanced level and scene viewer for Prince of Persia: The Sands of Time trilogy.</p>"
            "<p>Supports:</p>"
            "<ul>"
            "<li>BF BigFile archives (prince.bf, prince2.bf, prince3.bf)</li>"
            "<li>WOL World Object Lists & WOW World Object Waves</li>"
            "<li>In-memory LZO decompression for 128KB block streams</li>"
            "<li>Full texture decoding (DXT1, DXT3, DXT5, RAW, PAL8, 4bit)</li>"
            "<li>OpenGL textured & lit 3D preview with display list optimization</li>"
            "</ul>"
        )
        QMessageBox.about(self, "About Jade Engine Level Editor", msg)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Jade Engine Level Editor")

    window = LevelEditor()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
