from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal

class NavBar(QWidget):
    navigate = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.menu = QComboBox()
        self.location = QLabel("Home")

        self.menu.addItems([
            "Home",
            "History",
            "Emulators",
            "── Turing Machine",
            "── Manchester Baby",
            "── CHIP-8"
        ])

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
        labels = {
            "home": "Home",
            "history": "Home > History",
            "emulators": "Home > Emulators",
            "turing": "Home > Emulators > Turing Machine",
            "baby": "Home > Emulators > Manchester Baby",
            "chip8": "Home > Emulators > CHIP-8"
        }
        self.location.setText(labels.get(route, "Home"))
    
    