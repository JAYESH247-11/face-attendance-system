import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QHBoxLayout, QVBoxLayout, QLabel,
                             QPushButton, QFrame, QStackedWidget, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QColor
from styles import MAIN_STYLE
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
    def __init__(self, on_nav):
        super().__init__()
        self.setObjectName("sidebar")
        self.on_nav = on_nav
        self.buttons = {}
        self.active = None
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo
        logo = QLabel("FACEMARK")
        logo.setObjectName("logo_label")
        sub  = QLabel("ATTENDANCE SYSTEM")
        sub.setObjectName("sub_logo")
        layout.addWidget(logo)
        layout.addWidget(sub)

        # Divider
        div = QFrame()
        div.setObjectName("divider")
        div.setFixedHeight(1)
        div.setStyleSheet("background:#1e2433;")
        layout.addWidget(div)
        layout.addSpacing(12)

        # Nav
        for key, icon, label in NAV_ITEMS:
            btn = QPushButton(f"  {icon}   {label}")
            btn.setObjectName("nav_btn")
            btn.setMinimumHeight(46)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, k=key: self.set_active(k))
            layout.addWidget(btn)
            self.buttons[key] = btn

        layout.addStretch()

        # Version
        ver = QLabel("v1.0.0  •  PyQt6")
        ver.setStyleSheet("color:#2d3748; font-size:10px; padding:16px;")
        layout.addWidget(ver)

    def set_active(self, key):
        if self.active:
            self.buttons[self.active].setObjectName("nav_btn")
            self.buttons[self.active].style().unpolish(self.buttons[self.active])
            self.buttons[self.active].style().polish(self.buttons[self.active])
        self.buttons[key].setObjectName("nav_btn_active")
        self.buttons[key].style().unpolish(self.buttons[key])
        self.buttons[key].style().polish(self.buttons[key])
        self.active = key
        self.on_nav(key)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FaceMark — Attendance System")
        self.setMinimumSize(1100, 720)
        self.resize(1280, 780)
        self.setStyleSheet(MAIN_STYLE)
        self._build()

    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar(self._navigate)
        root.addWidget(self.sidebar)

        # Content stack
        self.stack = QStackedWidget()
        self.stack.setObjectName("content_area")
        root.addWidget(self.stack)



        self.pages = {
            "dashboard":  DashboardPage(),
            "register":   RegisterPage(),
            "attendance": AttendancePage(),
            "list":       EmployeeListPage(),
        }
        for page in self.pages.values():
            self.stack.addWidget(page)

        # Start on dashboard
        self.sidebar.set_active("dashboard")
        self._navigate("dashboard")

    def _navigate(self, key):
        page = self.pages[key]
        self.stack.setCurrentWidget(page)
        # Refresh list if navigating to it
        if key == "list" and hasattr(page, "refresh"):
            page.refresh()
        if key == "dashboard" and hasattr(page, "refresh"):
            page.refresh()
        if key == "attendance" and hasattr(page, "load_employees"):
            page.load_employees()


def main():
    init_db()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
