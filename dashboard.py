from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QFrame, QGridLayout, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from database import get_stats, get_today_attendance
from datetime import datetime


class StatCard(QWidget):
    def __init__(self, title, value, color="normal"):
        super().__init__()
        self.setObjectName("stat_card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)

        title_lbl = QLabel(title.upper())
        title_lbl.setObjectName("card_title")

        val_id = {"blue": "card_value_blue",
                  "green": "card_value_green",
                  "red": "card_value_red"}.get(color, "card_value")

        self.val_lbl = QLabel(str(value))
        self.val_lbl.setObjectName(val_id)

        layout.addWidget(title_lbl)
        layout.addWidget(self.val_lbl)

    def update_value(self, v):
        self.val_lbl.setText(str(v))


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.refresh()
        # Auto refresh every 30s
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(30000)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(24)

        # Header
        header = QHBoxLayout()
        title_col = QVBoxLayout()
        title = QLabel("Dashboard")
        title.setObjectName("page_title")
        self.date_lbl = QLabel()
        self.date_lbl.setObjectName("page_subtitle")
        title_col.addWidget(title)
        title_col.addWidget(self.date_lbl)
        header.addLayout(title_col)
        header.addStretch()
        main_layout.addLayout(header)

        # Stat Cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)
        self.card_total   = StatCard("Total Employees", "0", "blue")
        self.card_present = StatCard("Present Today",   "0", "green")
        self.card_absent  = StatCard("Absent Today",    "0", "red")
        for c in [self.card_total, self.card_present, self.card_absent]:
            c.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            c.setMinimumHeight(110)
            cards_layout.addWidget(c)
        main_layout.addLayout(cards_layout)

        # Today's Attendance Table header
        tbl_header = QHBoxLayout()
        tbl_title = QLabel("Today's Attendance")
        tbl_title.setObjectName("page_title")
        tbl_title.setStyleSheet("font-size:16px;")
        self.refresh_lbl = QLabel()
        self.refresh_lbl.setObjectName("page_subtitle")
        tbl_header.addWidget(tbl_title)
        tbl_header.addStretch()
        tbl_header.addWidget(self.refresh_lbl)
        main_layout.addLayout(tbl_header)

        # Summary list
        from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["EMP ID", "NAME", "DEPARTMENT", "CHECK IN", "STATUS"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)
        main_layout.addWidget(self.table)

    def refresh(self):
        now = datetime.now()
        self.date_lbl.setText(now.strftime("%A, %d %B %Y"))
        self.refresh_lbl.setText(f"Last updated: {now.strftime('%H:%M:%S')}")

        total, present, absent = get_stats()
        self.card_total.update_value(total)
        self.card_present.update_value(present)
        self.card_absent.update_value(absent)

        from PyQt6.QtWidgets import QTableWidgetItem
        from PyQt6.QtGui import QColor
        records = get_today_attendance()
        self.table.setRowCount(len(records))
        for row, rec in enumerate(records):
            self.table.setRowHeight(row, 46)
            for col, key in enumerate(["emp_id", "name", "department", "check_in", "status"]):
                item = QTableWidgetItem(str(rec[key]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if key == "status":
                    if rec[key] == "Present":
                        item.setForeground(QColor("#00e676"))
                    else:
                        item.setForeground(QColor("#ff4757"))
                self.table.setItem(row, col, item)
