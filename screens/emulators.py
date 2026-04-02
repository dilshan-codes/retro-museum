from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt


class EmulatorsScreen(QWidget):
    def __init__(self, navigate):
        super().__init__()
        self.navigate = navigate
        self.setStyleSheet("background-color: #e8e0d0;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Page title — exactly like history
        title = QLabel("Emulators")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #1a1a1a;
                padding: 20px;
            }
        """)
        layout.addWidget(title)

        # Scrollable area — exactly like history
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #e8e0d0;")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 10, 20, 10)
        content_layout.setSpacing(12)
        content_widget.setLayout(content_layout)

        # Subtitle inside scroll area
        subtitle = QLabel("Select a machine to emulate")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #555;
                padding: 8px 0px;
                background-color: transparent;
            }
        """)
        content_layout.addWidget(subtitle)

        # Three emulator cards — same structure as history cards
        machines = [
            ("Turing Machine", "1936  ·  The theoretical machine that defined computation", "turing"),
            ("Manchester Baby", "1948  ·  The world's first stored-program computer", "baby"),
            ("CHIP-8", "1977  ·  The virtual machine that brought gaming to hobbyists", "chip8"),
        ]

        for title_text, desc_text, route in machines:
            card = self.make_card(title_text, desc_text, route)
            content_layout.addWidget(card)

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

    def make_card(self, title, description, route):
        # Exact same card structure as history.py
        card = QWidget()
        card.setObjectName(f"card_{route}")
        card.setFixedHeight(80)
        card.setStyleSheet(f"""
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
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(16, 10, 16, 10)
        card_layout.setSpacing(4)
        card.setLayout(card_layout)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            "font-size: 15px; font-weight: bold; color: #1a1a1a; border: none;"
        )
        title_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        desc_label = QLabel(description)
        desc_label.setStyleSheet(
            "font-size: 13px; color: #555; border: none;"
        )
        desc_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        card_layout.addWidget(title_label)
        card_layout.addWidget(desc_label)

        card.mousePressEvent = lambda e: self.navigate(route)

        return card