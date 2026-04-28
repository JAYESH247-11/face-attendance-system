from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QSizePolicy, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap, QColor
import cv2
import numpy as np
from database import get_all_employees, mark_attendance, get_today_attendance
from datetime import datetime

try:
    import face_recognition
    FACE_LIB = True
except ImportError:
    FACE_LIB = False


class AttendancePage(QWidget):
    def __init__(self):
        super().__init__()
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)
        self.known_encodings = []
        self.known_ids = []
        self.known_names = []
        self.last_recognized = ""
        self.cooldown = 0
        
        # --- SMOOTHNESS VARIABLES ---
        self.frame_counter = 0
        self.face_locations = []
        self.face_names = []
        self.face_colors = []
        
        self.setup_ui()
        self.load_employees()
        self.attendance_done = False

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        # Title
        title = QLabel("Face Authentication")
        title.setObjectName("page_title")
        sub = QLabel("Look into the camera to mark your attendance automatically")
        sub.setObjectName("page_subtitle")
        layout.addWidget(title)
        layout.addWidget(sub)

        # Main row
        row = QHBoxLayout()
        row.setSpacing(24)

        # Camera card
        cam_card = QFrame()
        cam_card.setObjectName("section_card")
        cam_layout = QVBoxLayout(cam_card)
        cam_layout.setContentsMargins(20, 20, 20, 20)
        cam_layout.setSpacing(12)

        cam_lbl_title = QLabel("LIVE CAMERA")
        cam_lbl_title.setObjectName("card_title")
        cam_layout.addWidget(cam_lbl_title)

        self.cam_widget = QLabel("📷  Press Start to begin")
        self.cam_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cam_widget.setStyleSheet("background:#080a0f; border-radius:12px; color:#4a5568; font-size:14px;")
        self.cam_widget.setMinimumSize(400, 300)
        self.cam_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        cam_layout.addWidget(self.cam_widget)

        # Auth status
        self.auth_status = QLabel("Waiting for face...")
        self.auth_status.setObjectName("face_status_neutral")
        self.auth_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.auth_status.setMinimumHeight(42)
        self.auth_status.setStyleSheet(
            "background:#1e2433; color:#718096; border-radius:10px; "
            "padding:10px; font-size:14px; font-weight:600;")
        cam_layout.addWidget(self.auth_status)

        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("▶  Start Camera")
        self.start_btn.setObjectName("primary_btn")
        self.start_btn.setMinimumHeight(44)
        self.start_btn.clicked.connect(self.start_camera)

        self.stop_btn = QPushButton("■  Stop")
        self.stop_btn.setObjectName("danger_btn")
        self.stop_btn.setMinimumHeight(44)
        self.stop_btn.clicked.connect(self.stop_camera)

        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.stop_btn)
        cam_layout.addLayout(btn_row)

        if not FACE_LIB:
            warn = QLabel("⚠  face_recognition not installed.\nRunning in demo mode.")
            warn.setStyleSheet("color:#ffb300; font-size:11px; background:#ffb30015; border-radius:6px; padding:8px;")
            warn.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cam_layout.addWidget(warn)

        row.addWidget(cam_card, 3)

        # Right panel: log + stats
        right = QVBoxLayout()
        right.setSpacing(16)

        # Today's log
        log_card = QFrame()
        log_card.setObjectName("section_card")
        log_layout = QVBoxLayout(log_card)
        log_layout.setContentsMargins(20, 20, 20, 20)
        log_layout.setSpacing(10)

        log_title = QLabel("TODAY'S LOG")
        log_title.setObjectName("card_title")
        log_layout.addWidget(log_title)

        from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(3)
        self.log_table.setHorizontalHeaderLabels(["NAME", "CHECK IN", "STATUS"])
        self.log_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.log_table.verticalHeader().setVisible(False)
        self.log_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.log_table.setShowGrid(False)
        self.log_table.setMinimumHeight(300)
        log_layout.addWidget(self.log_table)

        refresh_btn = QPushButton("↻  Refresh Log")
        refresh_btn.setObjectName("primary_btn")
        refresh_btn.setMinimumHeight(38)
        refresh_btn.clicked.connect(self.refresh_log)
        log_layout.addWidget(refresh_btn)

        right.addWidget(log_card)

        # Recognized card
        self.recognized_card = QFrame()
        self.recognized_card.setObjectName("stat_card")
        rec_layout = QVBoxLayout(self.recognized_card)
        rec_layout.setContentsMargins(20, 16, 20, 16)

        rec_title = QLabel("LAST RECOGNIZED")
        rec_title.setObjectName("card_title")
        self.rec_name = QLabel("—")
        self.rec_name.setObjectName("card_value_blue")
        self.rec_time = QLabel("")
        self.rec_time.setObjectName("page_subtitle")

        rec_layout.addWidget(rec_title)
        rec_layout.addWidget(self.rec_name)
        rec_layout.addWidget(self.rec_time)
        right.addWidget(self.recognized_card)
        right.addStretch()

        row.addLayout(right, 2)
        layout.addLayout(row)
        self.refresh_log()

    def load_employees(self):
        self.known_encodings = []
        self.known_ids = []
        self.known_names = []
        
        employees = get_all_employees()
        for emp in employees:
            if emp['face_encoding'] is not None:
                self.known_encodings.append(emp['face_encoding'])
                self.known_ids.append(emp['emp_id'])
                self.known_names.append(emp['name'])

    def start_camera(self):
        # Using CAP_DSHOW for faster startup on Windows
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        # Optimized hardware settings
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        if self.cap.isOpened():
            # 30ms interval (~33 FPS) for a very smooth look
            self.timer.start(30)
            self.start_btn.setEnabled(False)
            self.attendance_done = False # Reset state
            self.last_recognized = ""
        else:
            QMessageBox.warning(self, "Camera Error", "Could not open camera!")

    def stop_camera(self):
        """Safely stops the camera and clears the display."""
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.cam_widget.clear()
        self.cam_widget.setText("📷  Camera stopped")
        self.start_btn.setEnabled(True)
        # Reset tracking variables for a clean start next time
        self.face_locations = []
        self.face_names = []

    def _update_frame(self):
        if not self.cap or not self.cap.isOpened():
            return
            
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        self.frame_counter += 1
        
        # --- INITIALIZE VARIABLES AT THE TOP ---
        # This prevents the UnboundLocalError
        current_emp_id = None 
        current_name = None

        # --- HEAVY PROCESSING (Every 3rd frame) ---
        if FACE_LIB and self.cooldown == 0 and not self.attendance_done:
            if self.frame_counter % 3 == 0:
                small = cv2.resize(rgb, (0, 0), fx=0.25, fy=0.25)
                self.face_locations = face_recognition.face_locations(small)
                encodings = face_recognition.face_encodings(small, self.face_locations)
                
                self.face_names = []
                self.face_colors = []
                
                for enc, loc in zip(encodings, self.face_locations):
                    name = "Unknown"
                    emp_id = None
                    color = (255, 71, 87) # Red

                    if self.known_encodings:
                        matches = face_recognition.compare_faces(self.known_encodings, enc, tolerance=0.5)
                        dists = face_recognition.face_distance(self.known_encodings, enc)
                        best = np.argmin(dists)
                        
                        if matches[best]:
                            name = self.known_names[best]
                            emp_id = self.known_ids[best]
                            color = (0, 230, 118) # Green
                            
                            # Capture these to use outside the loop
                            current_emp_id = emp_id
                            current_name = name

                    self.face_names.append(name)
                    self.face_colors.append(color)

        # --- ATTENDANCE LOGIC ---
        # Use current_emp_id which is guaranteed to exist now
        if current_emp_id and current_emp_id != self.last_recognized:
            result = mark_attendance(current_emp_id) 

            if result in ["SUCCESS", "ALREADY_DONE"]:
                self.last_recognized = current_emp_id
                self.attendance_done = True
                self.cooldown = 60 

                self.rec_name.setText(current_name)
                self.rec_time.setText(datetime.now().strftime("%H:%M:%S"))
                
                if result == "SUCCESS":
                    msg_text = f"Done! {current_name}, your attendance has been recorded."
                    status_text = f"✓ {current_name} — Attendance Marked!"
                else:
                    msg_text = f"Hey {current_name}, your attendance is already done!"
                    status_text = f"ℹ {current_name} — Already Logged"

                self._set_auth_status(status_text, "green")
                self.refresh_log()

                msg = QMessageBox(self)
                msg.setWindowTitle("Attendance Status")
                msg.setText(msg_text)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setStyleSheet("""
                    QMessageBox { background-color: #151820; }
                    QLabel { color: #f1f5f9; font-size: 14px; }
                    QPushButton { 
                        background-color: #00e676; 
                        color: #0b0d11; 
                        font-weight: bold; 
                        border-radius: 8px; 
                        padding: 8px 20px; 
                    }
                """)
                
                QTimer.singleShot(100, lambda: msg.exec())
                QTimer.singleShot(1000, self.stop_camera) #[cite: 50]

        # --- RENDERING (Every frame) ---
        scale = 4
        for loc, name, color in zip(self.face_locations, self.face_names, self.face_colors):
            top, right, bottom, left = [v * scale for v in loc]
            
            # Draw sophisticated box
            cv2.rectangle(rgb, (left, top), (right, bottom), color, 2)
            cv2.rectangle(rgb, (left, bottom-30), (right, bottom), color, cv2.FILLED)
            cv2.putText(rgb, name, (left+6, bottom-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        if self.cooldown > 0:
            self.cooldown -= 1

        # Convert to Pixmap and scale smoothly
        h, w, ch = rgb.shape
        img = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        pix = QPixmap.fromImage(img)
        
        # Using SmoothTransformation here is key for "visibility"
        self.cam_widget.setPixmap(pix.scaled(
            self.cam_widget.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))

    def _set_auth_status(self, text, color):
        colors = {
            "green": ("background:#00e67622; color:#00e676; border:1px solid #00e67650;"),
            "red":   ("background:#ff475722; color:#ff4757; border:1px solid #ff475750;"),
            "blue":  ("background:#00d4ff22; color:#00d4ff; border:1px solid #00d4ff50;"),
        }
        self.auth_status.setText(text)
        self.auth_status.setStyleSheet(
            f"border-radius:10px; padding:10px; font-size:14px; font-weight:600; {colors.get(color,'')}")

    def refresh_log(self):
        from PyQt6.QtWidgets import QTableWidgetItem
        from PyQt6.QtGui import QColor
        records = get_today_attendance()
        present = [r for r in records if r["status"] == "Present"]
        self.log_table.setRowCount(len(present))
        for row, rec in enumerate(present):
            self.log_table.setRowHeight(row, 40)
            for col, key in enumerate(["name", "check_in", "status"]):
                item = QTableWidgetItem(str(rec[key]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if key == "status":
                    item.setForeground(QColor("#00e676"))
                self.log_table.setItem(row, col, item)

    def closeEvent(self, e):
        self.stop_camera()
        super().closeEvent(e)
