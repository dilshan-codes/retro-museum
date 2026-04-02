import json
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt


class HistoryScreen(QWidget):
    def __init__(self, navigate):
        super().__init__()
        self.navigate = navigate
        self.setStyleSheet("background-color: #e8e0d0;")
        self.timeline_data = self.load_timeline()
        self.setup_ui()

    def load_timeline(self):
        # Load timeline events from JSON file
        path = os.path.join("content", "timeline.json")
        with open(path, "r") as f:
            data = json.load(f)
        return data["events"]

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Page title
        title = QLabel("History of Computing")
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

        # Scrollable area so timeline can grow beyond window height
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        timeline_widget = QWidget()
        timeline_widget.setStyleSheet("background-color: #e8e0d0;")
        timeline_layout = QVBoxLayout()
        timeline_layout.setContentsMargins(20, 10, 20, 10)
        timeline_layout.setSpacing(12)
        timeline_widget.setLayout(timeline_layout)

        # Build one entry per event
        for i, event in enumerate(self.timeline_data):
            entry = self.make_event_entry(event, i)
            timeline_layout.addWidget(entry)

        timeline_layout.addStretch()
        scroll.setWidget(timeline_widget)
        layout.addWidget(scroll)

    def make_event_entry(self, event, index):
        # Row container — holds year, dot, and card side by side
        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        container.setLayout(row)

        # Year label on the left
        year_label = QLabel(str(event["year"]))
        year_label.setFixedWidth(80)
        year_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        year_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #8b6914;
            }
        """)

        # Dot separator between year and card
        dot = QLabel("●")
        dot.setFixedWidth(30)
        dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dot.setStyleSheet("font-size: 20px; color: #6b4c11;")

        # Card widget — acts as a clickable button
        # setObjectName lets stylesheet target only this widget
        # without accidentally styling its children
        card = QWidget()
        card.setObjectName("card")
        card.setFixedHeight(80)
        card.setStyleSheet("""
            QWidget#card {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            QWidget#card:hover {
                background-color: #e8e0d0;
                border-color: #8b6914;
            }
        """)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(16, 10, 16, 10)
        card_layout.setSpacing(4)
        card.setLayout(card_layout)

        # Bold title label
        # WA_TransparentForMouseEvents makes label invisible to mouse
        # so hover and click go through to the card beneath
        title_label = QLabel(event["title"])
        title_label.setStyleSheet(
            "font-size: 15px; font-weight: bold; color: #1a1a1a; border: none;"
        )
        title_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # Description label
        desc_label = QLabel(event["short"])
        desc_label.setStyleSheet(
            "font-size: 13px; color: #555; border: none;"
        )
        desc_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        card_layout.addWidget(title_label)
        card_layout.addWidget(desc_label)

        # Navigate to detail screen when card is clicked
        event_id = event["id"]
        card.mousePressEvent = lambda e, eid=event_id: self.navigate(
            f"history_detail_{eid}"
        )

        row.addWidget(year_label)
        row.addWidget(dot)
        row.addWidget(card)

        return container