from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QComboBox, QSizePolicy
from PyQt6.QtCore import pyqtSignal

class NavBar(QWidget):
    navigate = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setFixedHeight(45)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(8, 4, 8, 4)
        self.layout.setSpacing(4)
        self.setLayout(self.layout)

        # Back and forward buttons with fixed width
        self.back_btn = QPushButton("⬅️ Back")
        self.back_btn.setFixedWidth(100)

        self.forward_btn = QPushButton("Forward ➡️")
        self.forward_btn.setFixedWidth(100)

        # Dropdown menu with fixed width
        self.menu = QComboBox()
        self.menu.setFixedWidth(200)
        self.menu.addItems([
            "Home",
            "History",
            "Emulators",
            "── Turing Machine",
            "── Manchester Baby",
            "── CHIP-8"
        ])

        # Location label expands to fill remaining space
        self.location = QLabel("Home")
        self.location.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        self.location.setStyleSheet("""
            QLabel {
                border: 1px solid #aaa;
                border-radius: 3px;
                padding: 2px 8px;
                background-color: #f0ece4;
                color: #1a1a1a;
            }
        """)

        self.layout.addWidget(self.back_btn)
        self.layout.addWidget(self.forward_btn)
        self.layout.addWidget(self.menu)
        self.layout.addWidget(self.location)

        self.back_btn.clicked.connect(self.on_back)
        self.forward_btn.clicked.connect(self.on_forward)
        self.menu.currentIndexChanged.connect(self.on_menu)

    def on_back(self):
        self.navigate.emit("back")

    def on_forward(self):
        self.navigate.emit("forward")

    def on_menu(self, index):
        routes = ["home", "history", "emulators", "turing", "baby", "chip8"]
        if index < len(routes):
            self.navigate.emit(routes[index])

    def update_location(self, route):
        # Handle dynamic history detail routes
        if route.startswith("history_detail_"):
            event_id = route.replace("history_detail_", "")
            self.location.setText(f"Home > History > {event_id}")
            route_to_index = {"home": 0, "history": 1}
            self.menu.blockSignals(True)
            self.menu.setCurrentIndex(1)
            self.menu.blockSignals(False)
            return

        # Update dropdown without triggering navigation signal
        route_to_index = {
            "home": 0,
            "history": 1,
            "emulators": 2,
            "turing": 3,
            "baby": 4,
            "chip8": 5
        }
        self.menu.blockSignals(True)
        self.menu.setCurrentIndex(route_to_index.get(route, 0))
        self.menu.blockSignals(False)

        labels = {
            "home": "Home",
            "history": "Home > History",
            "emulators": "Home > Emulators",
            "turing": "Home > Emulators > Turing Machine",
            "baby": "Home > Emulators > Manchester Baby",
            "chip8": "Home > Emulators > CHIP-8"
        }
        self.location.setText(labels.get(route, "Home"))

