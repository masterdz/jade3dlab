import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTreeWidget, QTreeWidgetItem, QLabel, QFileDialog,
    QSplitter, QTextEdit, QMenuBar, QMenu, QStatusBar, QCheckBox,
    QGroupBox, QFormLayout, QLineEdit, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from jade_engine.bf_parser import load_bf, BFArchive
from jade_engine.bin_parser import decompress_bin, extract_all_from_bin
from jade_engine.wow_parser import parse_wow, parse_wol
from jade_engine.mesh import LevelData
from jade_engine.viewer import GLViewer


class LevelEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jade Engine Level Editor")
        self.setGeometry(100, 100, 1400, 900)

        self.bf_archive = None
        self.current_level = None
        self.extracted_files = {}

        self._create_menu()
        self._create_ui()
        self.statusBar().showMessage("Ready - Open a .bf file to begin")

    def _create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")

        open_action = QAction("&Open BF Archive...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_bf)
        file_menu.addAction(open_action)

        open_dir_action = QAction("Open &Extracted Folder...", self)
        open_dir_action.setShortcut("Ctrl+D")
        open_dir_action.triggered.connect(self._open_directory)
        file_menu.addAction(open_dir_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        view_menu = menubar.addMenu("&View")

        reset_action = QAction("&Reset Camera", self)
        reset_action.setShortcut("R")
        reset_action.triggered.connect(self._reset_camera)
        view_menu.addAction(reset_action)

        wireframe_action = QAction("&Wireframe", self)
        wireframe_action.setShortcut("W")
        wireframe_action.setCheckable(True)
        wireframe_action.triggered.connect(self._toggle_wireframe)
        view_menu.addAction(wireframe_action)

        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _create_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(4, 4, 4, 4)

        bf_group = QGroupBox("BF Archive")
        bf_layout = QVBoxLayout(bf_group)

        self.bf_path_label = QLabel("No archive loaded")
        self.bf_path_label.setWordWrap(True)
        bf_layout.addWidget(self.bf_path_label)

        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabels(["Files", "Size"])
        self.file_tree.setColumnWidth(0, 250)
        self.file_tree.itemClicked.connect(self._on_file_selected)
        bf_layout.addWidget(self.file_tree)

        left_layout.addWidget(bf_group)

        info_group = QGroupBox("Selection Info")
        info_layout = QVBoxLayout(info_group)

        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setMaximumHeight(200)
        info_layout.addWidget(self.info_text)

        left_layout.addWidget(info_group)

        splitter.addWidget(left_panel)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(4, 4, 4, 4)

        toolbar = QHBoxLayout()

        self.btn_load_level = QPushButton("Load Level")
        self.btn_load_level.setEnabled(False)
        self.btn_load_level.clicked.connect(self._load_selected_level)
        toolbar.addWidget(self.btn_load_level)

        self.chk_meshes = QCheckBox("Show Meshes")
        self.chk_meshes.setChecked(True)
        self.chk_meshes.stateChanged.connect(self._update_view)
        toolbar.addWidget(self.chk_meshes)

        self.chk_objects = QCheckBox("Show Objects")
        self.chk_objects.setChecked(True)
        self.chk_objects.stateChanged.connect(self._update_view)
        toolbar.addWidget(self.chk_objects)

        self.chk_wireframe = QCheckBox("Wireframe")
        self.chk_wireframe.stateChanged.connect(self._update_view)
        toolbar.addWidget(self.chk_wireframe)

        toolbar.addStretch()

        right_layout.addLayout(toolbar)

        self.viewer = GLViewer()
        right_layout.addWidget(self.viewer)

        self.stats_label = QLabel("No level loaded")
        right_layout.addWidget(self.stats_label)

        splitter.addWidget(right_panel)
        splitter.setSizes([400, 1000])

    def _open_bf(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open BF Archive", "", "BF Archives (*.bf);;All Files (*)"
        )
        if not path:
            return

        try:
            self.statusBar().showMessage(f"Loading {os.path.basename(path)}...")
            self.bf_archive = load_bf(path)
            self.bf_path_label.setText(
                f"{os.path.basename(path)}\n"
                f"Version: {self.bf_archive.version} | "
                f"Files: {self.bf_archive.elem_count}"
            )
            self._populate_file_tree()
            self.statusBar().showMessage(
                f"Loaded {path} - {len(self.bf_archive.files)} files"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load BF archive:\n{e}")

    def _open_directory(self):
        path = QFileDialog.getExistingDirectory(
            self, "Open Extracted Folder"
        )
        if not path:
            return

        self.extracted_files = {}
        for f in Path(path).rglob("*.dec"):
            self.extracted_files[f.stem] = f.read_bytes()

        for f in Path(path).rglob("*.wow"):
            self.extracted_files[f.stem] = f.read_bytes()

        for f in Path(path).rglob("*.wol"):
            self.extracted_files[f.stem] = f.read_bytes()

        self.bf_path_label.setText(f"Directory: {path}")
        self._populate_directory_tree()
        self.statusBar().showMessage(f"Loaded {len(self.extracted_files)} files from {path}")

    def _populate_file_tree(self):
        self.file_tree.clear()

        if not self.bf_archive:
            return

        wow_item = QTreeWidgetItem(["WOW Files", ""])
        wol_item = QTreeWidgetItem(["WOL Files", ""])
        bin_item = QTreeWidgetItem(["BIN Files", ""])
        other_item = QTreeWidgetItem(["Other Files", ""])

        for bf_file in self.bf_archive.files:
            name = bf_file.filename or f"0x{bf_file.key:08X}"
            size = f"{bf_file.size:,} B"

            if name.lower().endswith('.wow'):
                QTreeWidgetItem(wow_item, [name, size])
            elif name.lower().endswith('.wol'):
                QTreeWidgetItem(wol_item, [name, size])
            elif name.lower().endswith('.bin'):
                QTreeWidgetItem(bin_item, [name, size])
            else:
                QTreeWidgetItem(other_item, [name, size])

        for item in [wow_item, wol_item, bin_item, other_item]:
            if item.childCount() > 0:
                self.file_tree.addTopLevelItem(item)

        self.file_tree.expandAll()

    def _populate_directory_tree(self):
        self.file_tree.clear()

        wow_item = QTreeWidgetItem(["WOW Files", ""])
        wol_item = QTreeWidgetItem(["WOL Files", ""])
        dec_item = QTreeWidgetItem(["DEC Files", ""])

        for name, data in self.extracted_files.items():
            size = f"{len(data):,} B"
            if name.lower().endswith('.wow'):
                QTreeWidgetItem(wow_item, [name, size])
            elif name.lower().endswith('.wol'):
                QTreeWidgetItem(wol_item, [name, size])
            else:
                QTreeWidgetItem(dec_item, [name, size])

        for item in [wow_item, wol_item, dec_item]:
            if item.childCount() > 0:
                self.file_tree.addTopLevelItem(item)

        self.file_tree.expandAll()

    def _on_file_selected(self, item: QTreeWidgetItem, column: int):
        if item.childCount() > 0:
            return

        name = item.text(0)
        self.info_text.clear()

        if self.bf_archive:
            bf_file = self.bf_archive.get_file_by_name(name)
            if bf_file:
                self.info_text.append(f"File: {name}")
                self.info_text.append(f"Key: 0x{bf_file.key:08X}")
                self.info_text.append(f"Size: {bf_file.size:,} bytes")
                self.info_text.append(f"Offset: 0x{bf_file.offset:X}")

                if name.lower().endswith('.bin'):
                    self.btn_load_level.setEnabled(True)
                    self.info_text.append("\nClick 'Load Level' to parse this file.")
                else:
                    self.btn_load_level.setEnabled(False)
        else:
            if name in self.extracted_files:
                data = self.extracted_files[name]
                self.info_text.append(f"File: {name}")
                self.info_text.append(f"Size: {len(data):,} bytes")

                if name.lower().endswith('.wow') or name.lower().endswith('.wol'):
                    self.btn_load_level.setEnabled(True)
                    self.info_text.append("\nClick 'Load Level' to parse this file.")
                else:
                    self.btn_load_level.setEnabled(False)

    def _load_selected_level(self):
        item = self.file_tree.currentItem()
        if not item or item.childCount() > 0:
            return

        name = item.text(0)

        try:
            if self.bf_archive:
                bf_file = self.bf_archive.get_file_by_name(name)
                if not bf_file:
                    return
                raw_data = bf_file.data
            else:
                if name not in self.extracted_files:
                    return
                raw_data = self.extracted_files[name]

            self.statusBar().showMessage(f"Parsing {name}...")

            if name.lower().endswith('.wol'):
                wow_files = parse_wol(raw_data)
                self.info_text.append(f"\nWOL file references {len(wow_files)} WOW files:")
                for wow_hash, ext in wow_files[:20]:
                    self.info_text.append(f"  {wow_hash} {ext}")
                if len(wow_files) > 20:
                    self.info_text.append(f"  ... and {len(wow_files) - 20} more")
                return

            decompressed = decompress_bin(raw_data)
            blocks = decompressed.split(b'\x99\xC0\xFF\xEE')

            from jade_engine.mesh_extractor import extract_all_meshes, find_object_transforms
            meshes = extract_all_meshes(blocks)
            objects = find_object_transforms(blocks)

            block_infos = []
            for i, block in enumerate(blocks):
                if len(block) < 8:
                    continue
                hash_id = block[:4][::-1].hex().upper()
                type_id = block[4:8][::-1].hex().upper()
                type_str = block[4:8].decode('ascii', errors='replace')
                block_infos.append({
                    'index': i,
                    'hash': hash_id,
                    'type': type_str,
                    'type_id': type_id,
                    'size': len(block),
                })

            self.viewer.set_blocks(block_infos, meshes, objects)

            stats = (
                f"Level: {name}\n"
                f"  Blocks: {len(block_infos)}\n"
                f"  Meshes: {len(meshes)}\n"
                f"  Objects: {len(objects)}"
            )
            self.stats_label.setText(stats)
            self.info_text.append(f"\n{stats}")

            self.statusBar().showMessage(f"Loaded level: {name}")

        except Exception as e:
            QMessageBox.critical(self, "Parse Error", f"Failed to parse level:\n{e}")
            import traceback
            traceback.print_exc()

    def _update_view(self):
        self.viewer.show_meshes = self.chk_meshes.isChecked()
        self.viewer.show_objects = self.chk_objects.isChecked()
        self.viewer.show_wireframe = self.chk_wireframe.isChecked()
        self.viewer.update()

    def _reset_camera(self):
        self.viewer._reset_view()
        self.viewer.update()

    def _toggle_wireframe(self, state):
        self.chk_wireframe.setChecked(state == Qt.Checked)

    def _show_about(self):
        QMessageBox.about(
            self,
            "About Jade Engine Level Editor",
            "<h2>Jade Engine Level Editor</h2>"
            "<p>A Python tool for extracting and previewing levels from "
            "Ubisoft's Jade Engine games.</p>"
            "<p>Supports:</p>"
            "<ul>"
            "<li>Prince of Persia: Sands of Time</li>"
            "<li>Prince of Persia: Warrior Within</li>"
            "<li>Prince of Persia: The Two Thrones</li>"
            "</ul>"
            "<p>Controls:</p>"
            "<ul>"
            "<li>Left click + drag: Rotate</li>"
            "<li>Middle click + drag: Pan</li>"
            "<li>Scroll: Zoom</li>"
            "<li>R: Reset camera</li>"
            "<li>W: Toggle wireframe</li>"
            "<li>M: Toggle meshes</li>"
            "<li>O: Toggle objects</li>"
            "</ul>"
        )


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Jade Engine Level Editor")

    window = LevelEditor()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
