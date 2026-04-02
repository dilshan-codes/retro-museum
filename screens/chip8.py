import os
import markdown
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QScrollArea, QSlider, QFileDialog)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor
from emulators.chip8_engine import Chip8


class Chip8Display(QWidget):
    # Custom widget that draws the 64x32 CHIP-8 display
    def __init__(self, parent_screen):
        super().__init__()
        self.parent_screen = parent_screen
        self.pixels = [[0] * 64 for _ in range(32)]
        self.setMinimumSize(512, 256)
        self.setStyleSheet("background-color: #1a1a1a;")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def mousePressEvent(self, event):
        # When display clicked grab focus so key events work
        self.parent_screen.setFocus()

    def update_pixels(self, pixels):
        self.pixels = pixels
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixel_w = self.width() // 64
        pixel_h = self.height() // 32

        for y in range(32):
            for x in range(64):
                if self.pixels[y][x]:
                    painter.fillRect(
                        x * pixel_w, y * pixel_h,
                        pixel_w, pixel_h,
                        QColor("#00ff88")
                    )
                else:
                    painter.fillRect(
                        x * pixel_w, y * pixel_h,
                        pixel_w, pixel_h,
                        QColor("#1a1a1a")
                    )


class Chip8Screen(QWidget):
    def __init__(self, navigate):
        super().__init__()
        self.navigate = navigate
        self.machine = Chip8()
        self.showing_history = False
        self.rom_loaded = False

        # Run timer — CHIP-8 runs at ~500Hz
        self.run_timer = QTimer()
        self.run_timer.timeout.connect(self.run_cycle)

        # Key mapping — keyboard to CHIP-8 hex keypad
        self.key_map = {
            Qt.Key.Key_1: 0x1, Qt.Key.Key_2: 0x2,
            Qt.Key.Key_3: 0x3, Qt.Key.Key_4: 0xC,
            Qt.Key.Key_Q: 0x4, Qt.Key.Key_W: 0x5,
            Qt.Key.Key_E: 0x6, Qt.Key.Key_R: 0xD,
            Qt.Key.Key_A: 0x7, Qt.Key.Key_S: 0x8,
            Qt.Key.Key_D: 0x9, Qt.Key.Key_F: 0xE,
            Qt.Key.Key_Z: 0xA, Qt.Key.Key_X: 0x0,
            Qt.Key.Key_C: 0xB, Qt.Key.Key_V: 0xF,
        }

        self.setStyleSheet("background-color: #e8e0d0;")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        # Top bar
        top_bar = QWidget()
        top_bar.setStyleSheet("background-color: #e8e0d0;")
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 12, 20, 12)
        top_bar.setLayout(top_layout)

        title = QLabel("CHIP-8  ·  1977")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1a1a1a;")

        self.toggle_btn = QPushButton("📖  View History")
        self.toggle_btn.setFixedWidth(160)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                font-size: 13px;
                color: #8b6914;
                background-color: transparent;
                border: 1px solid #8b6914;
                border-radius: 4px;
                padding: 4px 10px;
            }
            QPushButton:hover { background-color: #e8d9b0; }
        """)
        self.toggle_btn.clicked.connect(self.toggle_view)

        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(self.toggle_btn)
        self.main_layout.addWidget(top_bar)

        # Separator
        line = QWidget()
        line.setFixedHeight(2)
        line.setStyleSheet("background-color: #2a2a2a;")
        self.main_layout.addWidget(line)

        # Content area
        self.content_area = QWidget()
        self.content_area.setStyleSheet("background-color: #e8e0d0;")
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.content_area.setLayout(self.content_layout)
        self.main_layout.addWidget(self.content_area)

        self.show_emulator()

    def show_emulator(self):
        self.clear_content()
        self.toggle_btn.setText("📖  View History")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: #e8e0d0;")
        scroll.viewport().setStyleSheet("background-color: #e8e0d0;")

        wrapper = QWidget()
        wrapper.setStyleSheet("background-color: #e8e0d0;")
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)
        wrapper.setLayout(layout)

        # Load ROM button row
        load_row = QHBoxLayout()

        self.load_btn = QPushButton("📂  Load ROM")
        self.load_btn.setFixedSize(140, 36)
        self.load_btn.setStyleSheet("""
            QPushButton {
                font-size: 13px;
                color: #1a1a1a;
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e8e0d0;
                border-color: #8b6914;
            }
        """)
        self.load_btn.clicked.connect(self.load_rom)

        self.rom_label = QLabel("No ROM loaded — load a .ch8 file to begin")
        self.rom_label.setStyleSheet("font-size: 13px; color: #555;")

        load_row.addWidget(self.load_btn)
        load_row.addWidget(self.rom_label)
        load_row.addStretch()
        layout.addLayout(load_row)

        # CHIP-8 display — pass self so display can focus parent on click
        self.chip8_display = Chip8Display(self)
        layout.addWidget(self.chip8_display)

        # Click hint
        click_hint = QLabel("Click the display area first, then use keyboard keys to play")
        click_hint.setStyleSheet("font-size: 11px; color: #8b6914;")
        layout.addWidget(click_hint)

        # Registers title
        reg_title = QLabel("Registers")
        reg_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #555;")
        layout.addWidget(reg_title)

        # Register labels — two rows of 8
        self.reg_labels = []
        reg_row1 = QHBoxLayout()
        reg_row2 = QHBoxLayout()

        for i in range(16):
            lbl = QLabel(f"V{i:X}: 00")
            lbl.setStyleSheet("""
                QLabel {
                    font-size: 11px;
                    color: #1a1a1a;
                    background-color: #ffffff;
                    border: 1px solid #ddd;
                    padding: 2px 6px;
                    border-radius: 3px;
                }
            """)
            self.reg_labels.append(lbl)
            if i < 8:
                reg_row1.addWidget(lbl)
            else:
                reg_row2.addWidget(lbl)

        reg_row1.addStretch()
        reg_row2.addStretch()
        layout.addLayout(reg_row1)
        layout.addLayout(reg_row2)

        # PC, I, Steps info row
        info_row = QHBoxLayout()
        self.pc_label = QLabel("PC: 0x200")
        self.pc_label.setStyleSheet("font-size: 13px; color: #1a1a1a;")
        self.i_label = QLabel("I: 0x000")
        self.i_label.setStyleSheet("font-size: 13px; color: #1a1a1a;")
        self.steps_label = QLabel("Steps: 0")
        self.steps_label.setStyleSheet("font-size: 13px; color: #1a1a1a;")
        info_row.addWidget(self.pc_label)
        info_row.addSpacing(20)
        info_row.addWidget(self.i_label)
        info_row.addSpacing(20)
        info_row.addWidget(self.steps_label)
        info_row.addStretch()
        layout.addLayout(info_row)

        # Controls row
        controls_row = QHBoxLayout()
        controls_row.setSpacing(12)

        btn_style = """
            QPushButton {
                font-size: 13px;
                color: #1a1a1a;
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e8e0d0;
                border-color: #8b6914;
            }
        """

        self.run_btn = QPushButton("Run")
        self.run_btn.setFixedSize(100, 36)
        self.run_btn.setStyleSheet(btn_style)
        self.run_btn.clicked.connect(self.toggle_run)

        reset_btn = QPushButton("Reset")
        reset_btn.setFixedSize(100, 36)
        reset_btn.setStyleSheet(btn_style)
        reset_btn.clicked.connect(self.reset)

        speed_label = QLabel("Speed:")
        speed_label.setStyleSheet("font-size: 13px; color: #1a1a1a;")

        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(20)
        self.speed_slider.setValue(10)
        self.speed_slider.setFixedWidth(120)

        controls_row.addWidget(self.run_btn)
        controls_row.addWidget(reset_btn)
        controls_row.addSpacing(20)
        controls_row.addWidget(speed_label)
        controls_row.addWidget(self.speed_slider)
        controls_row.addStretch()
        layout.addLayout(controls_row)

        # Keyboard hint
        key_hint = QLabel("Keys: 1234 / QWER / ASDF / ZXCV → CHIP-8 hex keypad")
        key_hint.setStyleSheet("font-size: 11px; color: #888;")
        layout.addWidget(key_hint)

        scroll.setWidget(wrapper)
        self.content_layout.addWidget(scroll)

        # Grab focus immediately so keys work without clicking first
        self.setFocus()

    def show_history_doc(self):
        self.clear_content()
        self.toggle_btn.setText("⚙  View Emulator")

        path = os.path.join("content", "docs", "chip8.md")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
            html = markdown.markdown(raw, extensions=["tables"])
        else:
            html = "<p>Document not found.</p>"

        styled = f"""
        <style>
            h1 {{ font-size: 24px; font-weight: bold; color: #1a1a1a; margin-bottom: 8px; }}
            h2 {{ font-size: 18px; font-weight: bold; color: #5a3e10; margin-top: 24px; margin-bottom: 6px; }}
            p {{ font-size: 14px; color: #2a2a2a; margin-bottom: 12px; line-height: 1.7; }}
            table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
            th {{ background-color: #c8b89a; padding: 8px 12px; text-align: left; font-weight: bold; }}
            td {{ padding: 8px 12px; border-bottom: 1px solid #ccc; }}
            tr:nth-child(even) {{ background-color: #f0ece4; }}
        </style>
        {html}
        """

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: #e8e0d0;")
        scroll.viewport().setStyleSheet("background-color: #e8e0d0;")

        doc_widget = QWidget()
        doc_widget.setStyleSheet("background-color: #e8e0d0;")
        doc_layout = QVBoxLayout()
        doc_layout.setContentsMargins(60, 30, 60, 40)
        doc_widget.setLayout(doc_layout)

        doc_label = QLabel()
        doc_label.setWordWrap(True)
        doc_label.setTextFormat(Qt.TextFormat.RichText)
        doc_label.setText(styled)
        doc_label.setStyleSheet(
            "font-size: 14px; color: #1a1a1a; background-color: transparent;"
        )
        doc_layout.addWidget(doc_label)
        doc_layout.addStretch()

        scroll.setWidget(doc_widget)
        self.content_layout.addWidget(scroll)

    def clear_content(self):
        self.run_timer.stop()
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def toggle_view(self):
        if self.showing_history:
            self.showing_history = False
            self.show_emulator()
        else:
            self.showing_history = True
            self.show_history_doc()

    def load_rom(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load CHIP-8 ROM", "",
            "CHIP-8 ROMs (*.ch8 *.rom *.bin);;All Files (*)"
        )
        if path:
            with open(path, "rb") as f:
                rom_bytes = list(f.read())
            self.machine.load_rom(rom_bytes)
            self.rom_loaded = True
            self.rom_label.setText(f"Loaded: {os.path.basename(path)}")
            self.chip8_display.update_pixels(self.machine.display)
            self.update_registers()
            # Grab focus after loading so keys work immediately
            self.setFocus()

    def run_cycle(self):
        if not self.machine.running:
            return
        cycles = self.speed_slider.value()
        for _ in range(cycles):
            self.machine.step()
        if self.machine.draw_flag:
            self.chip8_display.update_pixels(self.machine.display)
            self.machine.draw_flag = False
        self.update_registers()

    def toggle_run(self):
        if self.run_timer.isActive():
            self.run_timer.stop()
            self.run_btn.setText("Run")
        else:
            if not self.rom_loaded:
                return
            self.run_timer.start(16)
            self.run_btn.setText("Pause")
            self.setFocus()

    def reset(self):
        self.run_timer.stop()
        self.run_btn.setText("Run")
        self.machine.reset()
        self.chip8_display.update_pixels(self.machine.display)
        self.update_registers()

    def update_registers(self):
        for i, lbl in enumerate(self.reg_labels):
            lbl.setText(f"V{i:X}: {self.machine.v[i]:02X}")
        self.pc_label.setText(f"PC: 0x{self.machine.pc:03X}")
        self.i_label.setText(f"I: 0x{self.machine.i:03X}")
        self.steps_label.setText(f"Steps: {self.machine.steps}")

    def keyPressEvent(self, event):
        key = self.key_map.get(event.key())
        if key is not None:
            self.machine.keys[key] = True

    def keyReleaseEvent(self, event):
        key = self.key_map.get(event.key())
        if key is not None:
            self.machine.keys[key] = False