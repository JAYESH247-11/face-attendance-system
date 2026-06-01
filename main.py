import os
import warnings

# 1. Suppress TensorFlow and MediaPipe C++ Logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["GLOG_minloglevel"] = "3" # Bumped to 3 (FATAL only)

# 2. Suppress specific Python warnings
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf.*")

# 3. Force the stubborn absl C++ logger to shut up (Fixes the W0000 warnings)
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

# 4. Suppress Qt Multimedia / FFmpeg info messages
os.environ["QT_LOGGING_RULES"] = "qt.multimedia.ffmpeg.*=false;qt.multimedia.*.info=false"

# NOW you can safely import mediapipe and your local modules
import mediapipe as mp
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QFrame, QStackedWidget,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from styles import get_style

from database import init_db
from dashboard import DashboardPage
from register import RegisterPage
from attendance import AttendancePage
from employee_list import EmployeeListPage


NAV_ITEMS = [
    ("dashboard",  "⬛",  "Dashboard"),
    ("register",   "👤",  "Register"),
    ("attendance", "📷",  "Attendance"),
    ("list",       "📋",  "Employee List"),
]


class Sidebar(QFrame):
    def __init__(self, on_nav, on_theme_toggle):
        super().__init__()

        self.setObjectName("sidebar")

        self.on_nav = on_nav
        self.on_theme_toggle = on_theme_toggle

        self.buttons = {}
        self.active = None

        self.current_theme = "dark"

        self._build()

    def _build(self):
        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # =========================
        # Logo
        # =========================

        logo = QLabel("FACEMARK")
        logo.setObjectName("logo_label")

        sub = QLabel("ATTENDANCE SYSTEM")
        sub.setObjectName("sub_logo")

        layout.addWidget(logo)
        layout.addWidget(sub)

        # =========================
        # Divider
        # =========================

        div = QFrame()
        div.setObjectName("divider")
        div.setFixedHeight(1)

        layout.addWidget(div)
        layout.addSpacing(12)

        # =========================
        # Navigation Buttons
        # =========================

        for key, icon, label in NAV_ITEMS:

            btn = QPushButton(f"  {icon}   {label}")

            btn.setObjectName("nav_btn")

            btn.setMinimumHeight(46)

            btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed
            )

            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            btn.clicked.connect(
                lambda _, k=key: self.set_active(k)
            )

            layout.addWidget(btn)

            self.buttons[key] = btn

        layout.addStretch()

        # =========================
        # Theme Toggle Button
        # =========================

        self.theme_btn = QPushButton("🌙 DARK MODE")

        self.theme_btn.setObjectName("theme_btn")

        self.theme_btn.setMinimumHeight(38)

        self.theme_btn.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.theme_btn.clicked.connect(
            self._handle_theme_click
        )

        layout.addWidget(self.theme_btn)

        # =========================
        # Version Label
        # =========================

        self.ver = QLabel("v1.0.0  •  PyQt6")

        self.ver.setObjectName("version_label")

        self.ver.setStyleSheet(
            "font-size:10px; padding:16px; color:#5a6a85;"
        )

        layout.addWidget(self.ver)

    def set_active(self, key):

        if self.active:

            self.buttons[self.active].setObjectName(
                "nav_btn"
            )

            self.buttons[self.active].style().unpolish(
                self.buttons[self.active]
            )

            self.buttons[self.active].style().polish(
                self.buttons[self.active]
            )

        self.buttons[key].setObjectName(
            "nav_btn_active"
        )

        self.buttons[key].style().unpolish(
            self.buttons[key]
        )

        self.buttons[key].style().polish(
            self.buttons[key]
        )

        self.active = key

        self.on_nav(key)

    def _handle_theme_click(self):

        if self.current_theme == "dark":

            self.current_theme = "light"

            self.theme_btn.setText(
                "☀️ LIGHT MODE"
            )

            self.ver.setStyleSheet(
                "font-size:10px; padding:16px; color:#94a3b8;"
            )

        else:

            self.current_theme = "dark"

            self.theme_btn.setText(
                "🌙 DARK MODE"
            )

            self.ver.setStyleSheet(
                "font-size:10px; padding:16px; color:#5a6a85;"
            )

        self.on_theme_toggle(self.current_theme)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "FaceMark — Attendance System"
        )

        self.setMinimumSize(1100, 720)

        self.resize(1280, 780)

        # Default Theme
        self.setStyleSheet(
            get_style("dark")
        )

        self._build()

    def _build(self):

        central = QWidget()

        self.setCentralWidget(central)

        root = QHBoxLayout(central)

        root.setContentsMargins(0, 0, 0, 0)

        root.setSpacing(0)

        # =========================
        # Sidebar
        # =========================

        self.sidebar = Sidebar(
            self._navigate,
            self._update_theme
        )

        root.addWidget(self.sidebar)

        # =========================
        # Content Area
        # =========================

        self.stack = QStackedWidget()

        self.stack.setObjectName(
            "content_area"
        )

        root.addWidget(self.stack)

        # =========================
        # Pages
        # =========================

        self.pages = {
            "dashboard": DashboardPage(),
            "register": RegisterPage(),
            "attendance": AttendancePage(),
            "list": EmployeeListPage(),
        }

        for page in self.pages.values():

            self.stack.addWidget(page)

        # =========================
        # Default Page
        # =========================

        self.sidebar.set_active("dashboard")

        self._navigate("dashboard")

    def _navigate(self, key):

        page = self.pages[key]

        self.stack.setCurrentWidget(page)

        # Refresh Pages

        if key == "list" and hasattr(page, "refresh"):
            page.refresh()

        if key == "dashboard" and hasattr(page, "refresh"):
            page.refresh()

        if key == "attendance" and hasattr(page, "load_employees"):
            page.load_employees()

    def _update_theme(self, theme):

        # Apply New Theme
        self.setStyleSheet(
            get_style(theme)
        )

        # Refresh Sidebar Styling
        self.sidebar.style().unpolish(
            self.sidebar
        )

        self.sidebar.style().polish(
            self.sidebar
        )

        # Refresh Content Styling
        self.stack.style().unpolish(
            self.stack
        )

        self.stack.style().polish(
            self.stack
        )


def main():

    init_db()

    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    win = MainWindow()

    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

