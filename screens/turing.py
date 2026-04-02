import os
import markdown
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QScrollArea, QComboBox, QSlider)
from PyQt6.QtCore import Qt, QTimer
from emulators.turing_engine import TuringMachine


class TuringScreen(QWidget):
    def __init__(self, navigate):
        super().__init__()
        self.navigate = navigate
        self.machine = TuringMachine()
        self.machine.load_program("binary_increment")
        self.showing_history = False

        # Timer for auto-run
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

        # Title
        title = QLabel("Turing Machine  ·  1936")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1a1a1a;")

        # Toggle button
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

        # Content area — swaps between emulator and history
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area.setLayout(self.content_layout)
        self.main_layout.addWidget(self.content_area)

        self.show_emulator()

    def show_emulator(self):
        self.clear_content()
        self.toggle_btn.setText("📖  View History")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        # Program selector
        selector_row = QHBoxLayout()
        selector_label = QLabel("Program:")
        selector_label.setStyleSheet("font-size: 13px; color: #555;")

        self.program_selector = QComboBox()
        self.program_selector.addItems([
            "binary_increment",
            "unary_add",
            "copy"
        ])
        self.program_selector.setFixedWidth(200)
        self.program_selector.currentTextChanged.connect(self.load_program)

        selector_row.addWidget(selector_label)
        selector_row.addWidget(self.program_selector)
        selector_row.addStretch()
        layout.addLayout(selector_row)

        # Tape display
        tape_label = QLabel("Tape")
        tape_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #555;")
        layout.addWidget(tape_label)

        self.tape_widget = QWidget()
        self.tape_widget.setFixedHeight(70)
        self.tape_widget.setStyleSheet("background-color: transparent;")
        self.tape_row = QHBoxLayout()
        self.tape_row.setContentsMargins(0, 0, 0, 0)
        self.tape_row.setSpacing(4)
        self.tape_widget.setLayout(self.tape_row)
        layout.addWidget(self.tape_widget)

        # State display
        state_row = QHBoxLayout()
        state_row.setSpacing(30)

        self.state_label = QLabel(f"State:  {self.machine.state}")
        self.state_label.setStyleSheet("font-size: 15px; color: #1a1a1a;")

        self.steps_label = QLabel(f"Steps:  {self.machine.steps}")
        self.steps_label.setStyleSheet("font-size: 15px; color: #1a1a1a;")

        self.symbol_label = QLabel(f"Reading:  {self.machine.read()}")
        self.symbol_label.setStyleSheet("font-size: 15px; color: #1a1a1a;")

        state_row.addWidget(self.state_label)
        state_row.addWidget(self.steps_label)
        state_row.addWidget(self.symbol_label)
        state_row.addStretch()
        layout.addLayout(state_row)

        # Controls
        controls_row = QHBoxLayout()
        controls_row.setSpacing(12)

        step_btn = QPushButton("Step")
        step_btn.setFixedSize(100, 36)
        step_btn.clicked.connect(self.step)

        self.run_btn = QPushButton("Run")
        self.run_btn.setFixedSize(100, 36)
        self.run_btn.clicked.connect(self.toggle_run)

        reset_btn = QPushButton("Reset")
        reset_btn.setFixedSize(100, 36)
        reset_btn.clicked.connect(self.reset)

        for btn in [step_btn, self.run_btn, reset_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 13px;
                    background-color: #ffffff;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #e8e0d0;
                    border-color: #8b6914;
                }
            """)

        # Speed slider
        speed_label = QLabel("Speed:")
        speed_label.setStyleSheet("font-size: 13px; color: #555;")

        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(10)
        self.speed_slider.setValue(5)
        self.speed_slider.setFixedWidth(120)

        controls_row.addWidget(step_btn)
        controls_row.addWidget(self.run_btn)
        controls_row.addWidget(reset_btn)
        controls_row.addSpacing(20)
        controls_row.addWidget(speed_label)
        controls_row.addWidget(self.speed_slider)
        controls_row.addStretch()
        layout.addLayout(controls_row)

        # Status message
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("font-size: 13px; color: #8b6914;")
        layout.addWidget(self.status_label)

        layout.addStretch()

        wrapper = QWidget()
        wrapper.setLayout(layout)
        self.content_layout.addWidget(wrapper)

        self.update_tape_display()

    def show_history_doc(self):
        self.clear_content()
        self.toggle_btn.setText("⚙  View Emulator")

        path = os.path.join("content", "docs", "turing.md")
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
        doc_label.setStyleSheet("font-size: 14px; color: #1a1a1a; background-color: transparent;")
        doc_layout.addWidget(doc_label)
        doc_layout.addStretch()

        scroll.setWidget(doc_widget)
        self.content_layout.addWidget(scroll)

    def clear_content(self):
        # Remove all widgets from content area
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

    def update_tape_display(self):
        # Clear existing tape cells
        while self.tape_row.count():
            item = self.tape_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Draw tape cells
        cells = self.machine.get_tape_view(10)
        for pos, symbol in cells:
            cell = QLabel(symbol)
            cell.setFixedSize(40, 40)
            cell.setAlignment(Qt.AlignmentFlag.AlignCenter)

            if pos == self.machine.head:
                # Current head position — highlighted
                cell.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        font-weight: bold;
                        background-color: #8b6914;
                        color: white;
                        border: 2px solid #5a3e10;
                        border-radius: 4px;
                    }
                """)
            else:
                cell.setStyleSheet("""
                    QLabel {
                        font-size: 14px;
                        background-color: #ffffff;
                        color: #1a1a1a;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                    }
                """)
            self.tape_row.addWidget(cell)

        # Update state labels
        self.state_label.setText(f"State:  {self.machine.state}")
        self.steps_label.setText(f"Steps:  {self.machine.steps}")
        self.symbol_label.setText(f"Reading:  {self.machine.read()}")

    def step(self):
        if self.machine.state == "halt":
            self.status_label.setText("Machine has halted.")
            return
        result = self.machine.step()
        self.update_tape_display()
        if not result:
            self.status_label.setText("Machine halted.")
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
        program = self.program_selector.currentText()
        self.machine.load_program(program)
        self.update_tape_display()
        self.status_label.setText("Reset.")

    def load_program(self, name):
        self.run_timer.stop()
        self.run_btn.setText("Run")
        self.machine.load_program(name)
        self.update_tape_display()
        self.status_label.setText(f"Loaded: {name}")