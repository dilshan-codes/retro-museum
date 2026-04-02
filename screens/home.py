import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap, QPainter, QColor

class HomeScreen(QWidget):
    def __init__(self, navigate):
        super().__init__()
        self.navigate = navigate

        # Load all background images
        self.images = []
        images_path = os.path.join("assets", "images")
        for i in range(1, 6):
            for ext in ["jpg", "png"]:
                path = os.path.join(images_path, f"img{i}.{ext}")
                if os.path.exists(path):
                    self.images.append(QPixmap(path))
                    break

        self.current_index = 0
        self.next_index = 1
        self.opacity = 1.0

        # Timer to switch images every 4 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.start_transition)
        self.timer.start(4000)

        # Fade timer for smooth crossfade
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(self.fade_step)
        self.fading = False

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        # App title
        self.title = QLabel("Retro Computing Museum")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                font-size: 42px;
                font-weight: bold;
                color: white;
                background-color: rgba(0, 0, 0, 140);
                padding: 20px 40px;
                border-radius: 10px;
            }
        """)

        # Subtitle
        self.subtitle = QLabel("Explore the machines that changed the world")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: white;
                background-color: rgba(0, 0, 0, 120);
                padding: 8px 24px;
                border-radius: 6px;
            }
        """)

        # History button
        self.history_btn = QPushButton("📖  History")
        self.history_btn.setFixedSize(220, 60)
        self.history_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                background-color: rgba(255, 255, 255, 200);
                border: 2px solid white;
                border-radius: 8px;
                color: #1a1a1a;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 240);
            }
        """)
        self.history_btn.clicked.connect(lambda: self.navigate("history"))

        # Emulators button
        self.emulators_btn = QPushButton("🖥  Emulators")
        self.emulators_btn.setFixedSize(220, 60)
        self.emulators_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                background-color: rgba(255, 255, 255, 200);
                border: 2px solid white;
                border-radius: 8px;
                color: #1a1a1a;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 240);
            }
        """)
        self.emulators_btn.clicked.connect(lambda: self.navigate("emulators"))

        layout.addStretch()
        layout.addWidget(self.title)
        layout.addSpacing(10)
        layout.addWidget(self.subtitle)
        layout.addSpacing(40)
        layout.addWidget(self.history_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(16)
        layout.addWidget(self.emulators_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

    def start_transition(self):
        if len(self.images) < 2:
            return
        self.next_index = (self.current_index + 1) % len(self.images)
        self.fade_opacity = 0.0
        self.fading = True
        self.fade_timer.start(30)

    def fade_step(self):
        self.fade_opacity += 0.05
        if self.fade_opacity >= 1.0:
            self.fade_opacity = 1.0
            self.current_index = self.next_index
            self.fading = False
            self.fade_timer.stop()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        if not self.images:
            painter.fillRect(self.rect(), QColor("#2c2c2c"))
            return

        # Draw current image scaled to fill
        current = self.images[self.current_index]
        scaled = current.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        x = (self.width() - scaled.width()) // 2
        y = (self.height() - scaled.height()) // 2
        painter.setOpacity(1.0)
        painter.drawPixmap(x, y, scaled)

        # Draw next image on top with increasing opacity for crossfade
        if self.fading and self.next_index < len(self.images):
            next_img = self.images[self.next_index]
            scaled_next = next_img.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            x2 = (self.width() - scaled_next.width()) // 2
            y2 = (self.height() - scaled_next.height()) // 2
            painter.setOpacity(self.fade_opacity)
            painter.drawPixmap(x2, y2, scaled_next)

        # Dark overlay so text is readable over any image
        painter.setOpacity(0.35)
        painter.fillRect(self.rect(), QColor("#000000"))