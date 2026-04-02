import os
import markdown
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QScrollArea, QSlider, QGridLayout)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from emulators.baby_engine import ManchesterBaby


class BabyScreen(QWidget):
    def __init__(self, navigate):
        super().__init__()
        self.navigate = navigate
        self.machine = ManchesterBaby()
        self.machine.load_first_program()
        self.showing_history = False

        self.run_timer = QTimer()
        self.run_timer.timeout.connect(self.auto_step)

        self.setStyleSheet("background-color: #e8e0d0;")
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        # Top bar
        top_bar = QWidget()
        top_bar.setStyleSheet("background-color: transparent;")
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 12, 20, 12)
        top_bar.setLayout(top_layout)

        title = QLabel("Manchester Baby  ·  1948")
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

        # Memory display title
        mem_title = QLabel("Memory Display  (32 words × 32 bits)")
        mem_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #555;")
        layout.addWidget(mem_title)

        # Memory grid — shows all 32 words as binary
        self.mem_labels = []
        mem_grid = QWidget()
        mem_grid.setStyleSheet("background-color: transparent;")
        grid_layout = QGridLayout()
        grid_layout.setSpacing(2)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        mem_grid.setLayout(grid_layout)

        mono_font = QFont("Courier New", 9)

        for i in range(32):
            # Row number
            row_label = QLabel(f"{i:02d}")
            row_label.setFixedWidth(24)
            row_label.setStyleSheet("font-size: 10px; color: #8b6914;")
            grid_layout.addWidget(row_label, i, 0)

            # Binary word
            word_label = QLabel(self.machine.to_binary(self.machine.memory[i]))
            word_label.setFont(mono_font)
            word_label.setFixedWidth(280)
            word_label.setStyleSheet("""
                QLabel {
                    font-size: 10px;
                    color: #1a1a1a;
                    background-color: #ffffff;
                    border: 1px solid #ddd;
                    padding: 1px 4px;
                }
            """)
            grid_layout.addWidget(word_label, i, 1)
            self.mem_labels.append(word_label)

        layout.addWidget(mem_grid)

        # Registers display
        reg_row = QHBoxLayout()
        reg_row.setSpacing(30)

        self.pc_label = QLabel(f"PC:  {self.machine.pc}")
        self.pc_label.setStyleSheet("font-size: 15px; color: #1a1a1a;")

        self.acc_label = QLabel(f"Accumulator:  {self.machine.accumulator}")
        self.acc_label.setStyleSheet("font-size: 15px; color: #1a1a1a;")

        self.steps_label = QLabel(f"Steps:  {self.machine.steps}")
        self.steps_label.setStyleSheet("font-size: 15px; color: #1a1a1a;")

        reg_row.addWidget(self.pc_label)
        reg_row.addWidget(self.acc_label)
        reg_row.addWidget(self.steps_label)
        reg_row.addStretch()
        layout.addLayout(reg_row)

        # Current instruction
        self.instr_label = QLabel("Current instruction: —")
        self.instr_label.setStyleSheet("font-size: 13px; color: #8b6914;")
        layout.addWidget(self.instr_label)

        # Controls
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

        step_btn = QPushButton("Step")
        step_btn.setFixedSize(100, 36)
        step_btn.setStyleSheet(btn_style)
        step_btn.clicked.connect(self.step)

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
        self.speed_slider.setMaximum(10)
        self.speed_slider.setValue(3)
        self.speed_slider.setFixedWidth(120)

        controls_row.addWidget(step_btn)
        controls_row.addWidget(self.run_btn)
        controls_row.addWidget(reset_btn)
        controls_row.addSpacing(20)
        controls_row.addWidget(speed_label)
        controls_row.addWidget(self.speed_slider)
        controls_row.addStretch()
        layout.addLayout(controls_row)

        # Status
        self.status_label = QLabel("Ready — loaded first program ever run (June 21, 1948)")
        self.status_label.setStyleSheet("font-size: 13px; color: #8b6914;")
        layout.addWidget(self.status_label)

        layout.addStretch()
        scroll.setWidget(wrapper)
        self.content_layout.addWidget(scroll)

        self.update_display()

    def show_history_doc(self):
        self.clear_content()
        self.toggle_btn.setText("⚙  View Emulator")

        path = os.path.join("content", "docs", "baby.md")
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
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def toggle_view(self):
        self.run_timer.stop()
        if self.showing_history:
            self.showing_history = False
            self.show_emulator()
        else:
            self.showing_history = True
            self.show_history_doc()

    def update_display(self):
        # Update memory grid
        for i, label in enumerate(self.mem_labels):
            word = self.machine.memory[i]
            label.setText(self.machine.to_binary(word))
            # Highlight current PC row
            if i == self.machine.pc % 32:
                label.setStyleSheet("""
                    QLabel {
                        font-size: 10px;
                        color: white;
                        background-color: #8b6914;
                        border: 1px solid #5a3e10;
                        padding: 1px 4px;
                    }
                """)
            else:
                label.setStyleSheet("""
                    QLabel {
                        font-size: 10px;
                        color: #1a1a1a;
                        background-color: #ffffff;
                        border: 1px solid #ddd;
                        padding: 1px 4px;
                    }
                """)

        # Update register labels
        self.pc_label.setText(f"PC:  {self.machine.pc}")
        self.acc_label.setText(f"Accumulator:  {self.machine.accumulator}")
        self.steps_label.setText(f"Steps:  {self.machine.steps}")

        if self.machine.current_instruction:
            self.instr_label.setText(
                f"Current instruction:  {self.machine.current_instruction}"
            )

    def step(self):
        if not self.machine.running:
            self.status_label.setText("Machine has stopped.")
            return
        result = self.machine.step()
        self.update_display()
        if not result:
            self.status_label.setText("Machine stopped.")
            self.run_timer.stop()
            self.run_btn.setText("Run")
        else:
            self.status_label.setText(f"Running... step {self.machine.steps}")

    def toggle_run(self):
        if self.run_timer.isActive():
            self.run_timer.stop()
            self.run_btn.setText("Run")
            self.status_label.setText("Paused.")
        else:
            speed = self.speed_slider.value()
            interval = int(1000 / speed)
            self.run_timer.start(interval)
            self.run_btn.setText("Pause")
            self.status_label.setText("Running...")

    def auto_step(self):
        self.step()

    def reset(self):
        self.run_timer.stop()
        self.run_btn.setText("Run")
        self.machine.load_first_program()
        self.update_display()
        self.status_label.setText("Reset — loaded first program ever run (June 21, 1948)")