from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class EmulatorsScreen(QWidget):
    def __init__(self, navigate):
        super().__init__()
        self.navigate = navigate
        self.setup_ui()

    def setup_ui(self):
        # Main layout — no AlignCenter so widgets stretch full width
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Set background on the whole screen
        self.setAutoFillBackground(True)
        palette = self.palette()
        from PyQt6.QtGui import QColor
        palette.setColor(self.backgroundRole(), QColor("#e8e0d0"))
        self.setPalette(palette)

        # Page title
        title = QLabel("Emulators")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #1a1a1a;
                padding: 20px;
                background-color: transparent;
            }
        """)

        # Subtitle
        subtitle = QLabel("Select a machine to emulate")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #555;
                padding-bottom: 20px;
                background-color: transparent;
            }
        """)

        # Three emulator buttons
        turing_btn = self.make_button(
            "Turing Machine",
            "1936  ·  The theoretical machine that defined computation",
            "turing"
        )
        baby_btn = self.make_button(
            "Manchester Baby",
            "1948  ·  The world's first stored-program computer",
            "baby"
        )
        chip8_btn = self.make_button(
            "CHIP-8",
            "1977  ·  The virtual machine that brought gaming to hobbyists",
            "chip8"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(12)
        layout.addWidget(turing_btn)
        layout.addSpacing(12)
        layout.addWidget(baby_btn)
        layout.addSpacing(12)
        layout.addWidget(chip8_btn)
        layout.addStretch()

    def make_button(self, title, description, route):
        # Container acts as clickable card
        # Unique object name per button prevents style bleeding
        container = QWidget()
        container.setObjectName(f"card_{route}")
        container.setFixedHeight(80)
        container.setStyleSheet(f"""
            QWidget#card_{route} {{
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 8px;
            }}
            QWidget#card_{route}:hover {{
                background-color: #e8e0d0;
                border-color: #8b6914;
            }}
        """)
        container.setCursor(Qt.CursorShape.PointingHandCursor)

        inner = QVBoxLayout()
        inner.setContentsMargins(20, 10, 20, 10)
        inner.setSpacing(4)
        container.setLayout(inner)

        # Bold title — transparent to mouse so hover goes to container
        title_label = QLabel(title)
        title_label.setStyleSheet(
            "font-size: 15px; font-weight: bold; color: #1a1a1a; border: none; background-color: transparent;"
        )
        title_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # Description — also transparent to mouse
        desc_label = QLabel(description)
        desc_label.setStyleSheet(
            "font-size: 13px; color: #555; border: none; background-color: transparent;"
        )
        desc_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        inner.addWidget(title_label)
        inner.addWidget(desc_label)

        # Navigate when container clicked
        container.mousePressEvent = lambda event: self.navigate(route)

        return container