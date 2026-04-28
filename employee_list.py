from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QLineEdit, QComboBox, QFrame,
                             QSizePolicy,QDateEdit,QMessageBox)
from PyQt6.QtCore import Qt, QTimer,QDate
from PyQt6.QtGui import QColor, QFont
from database import get_today_attendance, get_stats
from datetime import date
from database import get_attendance_by_date



class EmployeeListPage(QWidget):
    def __init__(self):
        super().__init__()
        self.all_records = []
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        # Header row
        header_row = QHBoxLayout()
        title_col = QVBoxLayout()
        title = QLabel("Employee List")
        title.setObjectName("page_title")
        self.date_lbl = QLabel(f"Date: {date.today().strftime('%d %B %Y')}")
        self.date_lbl.setObjectName("page_subtitle")
        title_col.addWidget(title)
        title_col.addWidget(self.date_lbl)
        header_row.addLayout(title_col)
        header_row.addStretch()

        refresh_btn = QPushButton("↻  Refresh")
        refresh_btn.setObjectName("primary_btn")
        refresh_btn.setMinimumHeight(40)
        refresh_btn.clicked.connect(self.refresh)
        header_row.addWidget(refresh_btn)
        layout.addLayout(header_row)

        # Stats row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(16)
        self.total_card  = self._mini_card("Total", "0", "#e2e8f0")
        self.present_card = self._mini_card("Present", "0", "#00e676")
        self.absent_card  = self._mini_card("Absent",  "0", "#ff4757")
        for c in [self.total_card, self.present_card, self.absent_card]:
            stats_row.addWidget(c)
        stats_row.addStretch()
        layout.addLayout(stats_row)

        # Filter row
        filter_card = QFrame()
        filter_card.setObjectName("section_card")
        filter_layout = QHBoxLayout(filter_card)
        filter_layout.setContentsMargins(16, 12, 16, 12)
        filter_layout.setSpacing(12)

        search_lbl = QLabel("🔍")
        search_lbl.setStyleSheet("color:#4a5568; font-size:14px;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or employee ID...")
        self.search_input.setMinimumHeight(36)
        self.search_input.textChanged.connect(self.apply_filter)

        filter_lbl = QLabel("Status:")
        filter_lbl.setObjectName("form_label")
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Present", "Absent"])
        self.status_filter.setMinimumHeight(36)
        self.status_filter.setMinimumWidth(120)
        self.status_filter.currentTextChanged.connect(self.apply_filter)

        date_lbl = QLabel("Date:")
        date_lbl.setObjectName("from_label")
        self.date_filter = QDateEdit()
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.setMinimumHeight(36)
        self.date_filter.dateChanged.connect(self.refresh)

        filter_layout.addWidget(search_lbl)
        filter_layout.addWidget(self.search_input, 1)
        filter_layout.addWidget(filter_lbl)
        filter_layout.addWidget(self.status_filter)
        filter_layout.addWidget(self.date_filter)
        layout.addWidget(filter_card)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "EMP ID", "NAME", "DEPARTMENT", "CHECK IN", "STATUS", "DELETE"
        ])

        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(False)
        layout.addWidget(self.table)

        # Footer
        self.footer_lbl = QLabel("")
        self.footer_lbl.setObjectName("page_subtitle")
        self.footer_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.footer_lbl)

    def _mini_card(self, label, value, color):
        card = QFrame()
        card.setObjectName("stat_card")
        card.setMinimumWidth(120)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(16, 12, 16, 12)
        cl.setSpacing(4)
        lbl = QLabel(label.upper())
        lbl.setObjectName("card_title")
        val = QLabel(value)
        val.setStyleSheet(f"font-size:24px; font-weight:700; color:{color};")
        val.setObjectName(f"_stat_{label}")
        cl.addWidget(lbl)
        cl.addWidget(val)
        return card

    def _update_mini(self, card, value):
        for child in card.findChildren(QLabel):
            if child.objectName().startswith("_stat_"):
                child.setText(str(value))

    def refresh(self):
        # 1. Get the date from the widget
        selected_date_str = self.date_filter.date().toPyDate().isoformat()
        self.date_lbl.setText(f"Date: {self.date_filter.date().toString('dd MMMM yyyy')}")
        
        # 2. Fetch records
        self.all_records = get_attendance_by_date(selected_date_str)
        if not self.all_records:
            self.table.setRowCount(0)
            self.footer_lbl.setText("⚠️No Employee Entry Found.")
        else:
            self.footer_lbl.setText(f"Total {len(self.all_records)} Employee Found.")
        
        # 3. Calculate stats
        total = len(self.all_records)
        present_count = len([r for r in self.all_records if r["status"] == "Present"])
        absent_count = total - present_count

        # --- NEW MESSAGE LOGIC ---
        # If there are employees in the system, but NO ONE is present for this date
        if total > 0 and present_count == 0:
            QMessageBox.information(self, "No Data", 
                f"No attendance records found for {self.date_filter.date().toString('dd-MM-yyyy')}.\n"
                "All employees are currently marked as Absent.")
        
        # If the system has 0 employees registered at all
        elif total == 0:
            QMessageBox.warning(self, "Empty Entry", "No employees found in the database. Please Check the date.")
        # -------------------------

        self._update_mini(self.total_card, total)
        self._update_mini(self.present_card, present_count)
        self._update_mini(self.absent_card, absent_count)
        self.apply_filter()

    def delete_employee(self, emp_id):
        from PyQt6.QtWidgets import QMessageBox
        from database import delete_employee

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete employee {emp_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            delete_employee(emp_id)
            QMessageBox.information(self, "Deleted", "Employee deleted successfully")
            self.refresh()

    def apply_filter(self):
        query = self.search_input.text().lower()
        status_f = self.status_filter.currentText()

        filtered = []
        for rec in self.all_records:
            if query and query not in rec["name"].lower() and query not in rec["emp_id"].lower():
                continue
            if status_f != "All" and rec["status"] != status_f:
                continue
            filtered.append(rec)

        self.table.setRowCount(len(filtered))

        for row, rec in enumerate(filtered):
            self.table.setRowHeight(row, 46)
            status = rec["status"]

            values = [rec["emp_id"], rec["name"], rec["department"] or "—",
                    rec["check_in"], status]

            for col, val in enumerate(values):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                if col == 4:
                    if status == "Present":
                        item.setForeground(QColor("#00e676"))
                        item.setBackground(QColor("#00e67610"))
                    else:
                        item.setForeground(QColor("#ff4757"))
                        item.setBackground(QColor("#ff475710"))

                self.table.setItem(row, col, item)

            # 🔥 DELETE BUTTON
            delete_btn = QPushButton("🗑️")
            delete_btn.setStyleSheet("""
                QPushButton { background: transparent; font-size:16px; }
                QPushButton:hover { color: red; }
            """)

            delete_btn.clicked.connect(
                lambda _, emp_id=rec["emp_id"]: self.delete_employee(emp_id)
            )

            self.table.setCellWidget(row, 5, delete_btn)

        self.footer_lbl.setText(
            f"Showing {len(filtered)} of {len(self.all_records)} employees  •  "
            f"{date.today().strftime('%d %B %Y')}"
        )