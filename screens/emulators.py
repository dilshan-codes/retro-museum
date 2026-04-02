from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt


class EmulatorsScreen(QWidget):
    def __init__(self, navigate):
        super().__init__()
        self.navigate = navigate
        self.setStyleSheet("background-color: #f5f0e8;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        # Title
        title = QLabel("Emulators")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: bold;
                color: #1a1a1a;
                margin-bottom: 10px;
            }
        """)

        # Subtitle
        subtitle = QLabel("Select a machine to emulate")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #555;
                margin-bottom: 40px;
            }
        """)

        # Turing Machine button
        turing_btn = self.make_button(
            "Turing Machine",
            "1936  ·  The theoretical machine that defined computation",
            "turing"
        )

        # Manchester Baby button
        baby_btn = self.make_button(
            "Manchester Baby",
            "1948  ·  The world's first stored-program computer",
            "baby"
        )

        # CHIP-8 button
        chip8_btn = self.make_button(
            "CHIP-8",
            "1977  ·  The virtual machine that brought gaming to hobbyists",
            "chip8"
        )

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(turing_btn)
        layout.addSpacing(16)
        layout.addWidget(baby_btn)
        layout.addSpacing(16)
        layout.addWidget(chip8_btn)
        layout.addStretch()

    def make_button(self, title, description, route):
        btn = QPushButton(f"{title}\n{description}")
        btn.setFixedSize(600, 80)
        btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                text-align: left;
                padding: 12px 20px;
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 8px;
                color: #1a1a1a;
            }
            QPushButton:hover {
                background-color: #e8e0d0;
                border-color: #999;
            }
        """)
        btn.clicked.connect(lambda: self.navigate(route))
        return btn