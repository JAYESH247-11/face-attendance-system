from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class StatusPopup(QWidget):
    def __init__(self, parent, icon_char, title_text, subtitle_text, text_color):
        super().__init__(parent)

        self.setFixedSize(340, 240) 
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15) 

        # --- The Container Frame ---
        self.frame = QFrame(self)
        self.frame.setObjectName("section_card") # Links to styles.py

        # --- Drop Shadow Effect ---
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 80)) 
        self.frame.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        # --- Dynamic UI Elements ---
        
        # 1. Dynamic Icon
        self.icon = QLabel(icon_char)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon.setStyleSheet("font-size: 72px; background: transparent;") 

        # 2. Dynamic Title
        self.title = QLabel(title_text)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # We override just the color inline, but inherit font family/size from styles.py
        self.title.setStyleSheet(f"color: {text_color}; font-size: 22px; font-weight: bold; background: transparent;")

        # 3. Dynamic Subtitle
        self.subtitle = QLabel(subtitle_text)
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setObjectName("page_subtitle") 

        layout.addWidget(self.icon)
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)

        main_layout.addWidget(self.frame)