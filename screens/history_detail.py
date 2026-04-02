import os
import markdown
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt


class HistoryDetailScreen(QWidget):
    def __init__(self, navigate, event_id=None):
        super().__init__()
        self.navigate = navigate
        self.event_id = event_id
        self.setStyleSheet("background-color: #e8e0d0;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Top bar with back button and title
        top_bar = QWidget()
        top_bar.setStyleSheet("background-color: transparent;")
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 16, 20, 8)
        top_bar.setLayout(top_layout)

        back_btn = QPushButton("← Back to History")
        back_btn.setFixedWidth(160)
        back_btn.setStyleSheet("""
            QPushButton {
                font-size: 13px;
                color: #8b6914;
                background-color: transparent;
                border: 1px solid #8b6914;
                border-radius: 4px;
                padding: 4px 10px;
            }
            QPushButton:hover {
                background-color: #e8d9b0;
            }
        """)
        back_btn.clicked.connect(lambda: self.navigate("history"))

        top_layout.addWidget(back_btn)
        top_layout.addStretch()
        layout.addWidget(top_bar)

        # Separator line
        line = QWidget()
        line.setFixedHeight(2)
        line.setStyleSheet("background-color: #2a2a2a;")
        layout.addWidget(line)

        # Scrollable document area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: #e8e0d0;")
        scroll.viewport().setStyleSheet("background-color: #e8e0d0;")

        doc_widget = QWidget()
        doc_widget.setStyleSheet("background-color: #e8e0d0;")
        doc_layout = QVBoxLayout()
        doc_layout.setContentsMargins(60, 30, 60, 40)
        doc_widget.setLayout(doc_layout)

        # Load and render the markdown document
        content = self.load_document()

        doc_label = QLabel()
        doc_label.setWordWrap(True)
        doc_label.setTextFormat(Qt.TextFormat.RichText)
        doc_label.setText(content)
        doc_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #1a1a1a;
                background-color: transparent;
                line-height: 1.6;
            }
        """)
        doc_label.setOpenExternalLinks(False)

        doc_layout.addWidget(doc_label)
        doc_layout.addStretch()

        scroll.setWidget(doc_widget)
        layout.addWidget(scroll)

    def load_document(self):
        # Build path from event_id
        path = os.path.join("content", "docs", "events", f"{self.event_id}.md")

        if not os.path.exists(path):
            return "<h2>Document not found</h2><p>No document exists for this event yet.</p>"

        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()

        # Convert markdown to HTML
        html = markdown.markdown(raw, extensions=["tables"])

        # Wrap in styled HTML
        return f"""
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