def get_asset_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

from datetime import datetime
import os
import sys
import cv2
from database import get_all_employees, get_today_attendance, mark_attendance
import numpy as np
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QImage, QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl
from blink_detector import BlinkDetector
from popup import StatusPopup

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

        # =========================
        # FACE DATA
        # =========================
        self.known_encodings = []
        self.known_ids = []
        self.known_names = []

        # =========================
        # SECURITY / STATE
        # =========================
        self.last_recognized = ""
        self.cooldown = 0
    
        self.blink_verified = False
        self.blink_detector = BlinkDetector()


        # 1. Success Sound
        self.success_sound = QSoundEffect()
        self.success_sound.setSource(
            QUrl.fromLocalFile(get_asset_path("sound/meldix-success-340660.wav")))
        self.success_sound.setVolume(0.8)

        # 2. Error Sound
        self.error_sound = QSoundEffect()
        self.error_sound.setSource(
            QUrl.fromLocalFile(get_asset_path("sound/freesound_community-access-denied-102628.wav")))
        self.error_sound.setVolume(0.8)

        # 3. Info Sound
        self.info_sound = QSoundEffect()
        self.info_sound.setSource(
            QUrl.fromLocalFile(get_asset_path("sound/u_4quckyrjhw-notification-sound-349341.wav")))
        self.info_sound.setVolume(0.8)

        # 4. Double Info Sound
        self.double_info_sound = QSoundEffect()
        self.double_info_sound.setSource(
            QUrl.fromLocalFile(get_asset_path("sound/freesound_community-beep-warning-6387.wav")))
        self.double_info_sound.setVolume(0.5)

        # =========================
        # UI
        # =========================
        self.setup_ui()
        self.load_employees()

    # =========================
    # UI
    # =========================

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        # =========================
        # TITLE
        # =========================
        title = QLabel("Face Authentication")
        title.setObjectName("page_title")
        sub = QLabel(
            "Look into the camera to mark your attendance automatically"
        )
        sub.setObjectName("page_subtitle")
        layout.addWidget(title)
        layout.addWidget(sub)

        # =========================
        # MAIN ROW
        # =========================
        row = QHBoxLayout()
        row.setSpacing(24)

        # =========================
        # CAMERA CARD
        # =========================
        cam_card = QFrame()
        cam_card.setObjectName("section_card")
        cam_layout = QVBoxLayout(cam_card)
        cam_layout.setContentsMargins(20, 20, 20, 20)
        cam_layout.setSpacing(12)
        cam_lbl_title = QLabel("LIVE CAMERA")
        cam_lbl_title.setObjectName("card_title")
        cam_layout.addWidget(cam_lbl_title)

        # =========================
        # CAMERA VIEW
        # =========================
        self.cam_widget = QLabel("📷 Press Start to begin")
        self.cam_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cam_widget.setStyleSheet(
            """
            background:#080a0f;
            border-radius:12px;
            color:#4a5568;
            font-size:14px;
            """
        )
        self.cam_widget.setMinimumSize(400, 300)
        self.cam_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        cam_layout.addWidget(self.cam_widget)

        # =========================
        # STATUS
        # =========================
        self.auth_status = QLabel("Waiting for face...")
        self.auth_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.auth_status.setMinimumHeight(42)
        self.auth_status.setStyleSheet(
            """
            background:#1e2433;
            color:#718096;
            border-radius:10px;
            padding:10px;
            font-size:14px;
            font-weight:600;
            """
        )
        cam_layout.addWidget(self.auth_status)

        # =========================
        # BUTTONS
        # =========================
        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("▶ Start Camera")
        self.start_btn.setObjectName("primary_btn")
        self.start_btn.setMinimumHeight(44)
        self.start_btn.clicked.connect(self.start_camera)
        self.stop_btn = QPushButton("■ Stop")
        self.stop_btn.setObjectName("danger_btn")
        self.stop_btn.setMinimumHeight(44)
        self.stop_btn.clicked.connect(self.stop_camera)
        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.stop_btn)
        cam_layout.addLayout(btn_row)
        row.addWidget(cam_card, 3)

        # =========================
        # RIGHT PANEL
        # =========================
        right = QVBoxLayout()
        right.setSpacing(16)

        # =========================
        # TODAY LOG
        # =========================
        log_card = QFrame()
        log_card.setObjectName("section_card")
        log_layout = QVBoxLayout(log_card)
        log_layout.setContentsMargins(20, 20, 20, 20)
        log_title = QLabel("TODAY'S LOG")
        log_title.setObjectName("card_title")
        log_layout.addWidget(log_title)
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(3)
        self.log_table.setHorizontalHeaderLabels(["NAME", "CHECK IN", "STATUS"])
        self.log_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.log_table.verticalHeader().setVisible(False)
        self.log_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.log_table.setShowGrid(False)
        self.log_table.setMinimumHeight(260)
        log_layout.addWidget(self.log_table)
        refresh_btn = QPushButton("↻ Refresh Log")
        refresh_btn.setObjectName("primary_btn")
        refresh_btn.clicked.connect(self.refresh_log)
        log_layout.addWidget(refresh_btn)
        right.addWidget(log_card)

        # =========================
        # LAST RECOGNIZED
        # =========================
        self.recognized_card = QFrame()
        self.recognized_card.setObjectName("stat_card")
        rec_layout = QVBoxLayout(self.recognized_card)
        rec_layout.setContentsMargins(20, 20, 20, 20)
        rec_title = QLabel("LAST RECOGNIZED")
        rec_title.setObjectName("card_title")
        self.rec_name = QLabel("No Face Detected")
        self.rec_name.setStyleSheet("font-size:24px;")
        self.rec_empid = QLabel("Employee ID : --")
        self.rec_department = QLabel("Department : --")
        self.rec_status = QLabel("Status : Waiting")
        self.rec_time = QLabel("")
        rec_layout.addWidget(rec_title)
        rec_layout.addWidget(self.rec_name)
        rec_layout.addWidget(self.rec_empid)
        rec_layout.addWidget(self.rec_department)
        rec_layout.addWidget(self.rec_status)
        rec_layout.addWidget(self.rec_time)
        right.addWidget(self.recognized_card)
        row.addLayout(right, 2)
        layout.addLayout(row)
        self.refresh_log()

    # =========================
    # LOAD EMPLOYEES
    # =========================

    def load_employees(self):
        emps = get_all_employees()
        self.known_encodings.clear()
        self.known_ids.clear()
        self.known_names.clear()
        for emp in emps:
            if emp["face_encoding"] is not None:
                self.known_encodings.append(emp["face_encoding"])
                self.known_ids.append(emp["emp_id"])
                self.known_names.append(emp["name"])

    # =========================
    # START CAMERA
    # =========================

    def start_camera(self):
        self.load_employees()
        self.is_processing_detection = False
        self.cooldown = 0
        self.blink_detector.reset()
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        for _ in range(5):
            self.cap.read()
        if self.cap.isOpened():
            self.timer.start(40)
            self.start_btn.setEnabled(False)
        else:
            QMessageBox.warning(
                self, "Camera Error", "Could not open camera!"
            )

    # =========================
    # STOP CAMERA
    # =========================

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.cam_widget.clear()
        self.cam_widget.setText("📷 Camera stopped")
        self.start_btn.setEnabled(True)
        self.blink_detector.reset()

    # =========================
    # UPDATE FRAME
    # =========================

    def _update_frame(self):
        if not self.cap:
            return
        ret, frame = self.cap.read()
        if not ret:
            return

        # =========================
        # MIRROR CAMERA
        # =========================
        frame = cv2.flip(frame, 1)

        # =========================
        # RGB
        # =========================
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # =========================
        # IMPROVE LIGHTING
        # =========================
        rgb = cv2.convertScaleAbs(rgb, alpha=1.2, beta=20)

        # =========================
        # COOLDOWN
        # =========================
        if self.cooldown > 0:
            self.cooldown -= 1

        # =========================
        # FACE DETECTION ONLY
        # =========================
        if (
            FACE_LIB
            and self.cooldown == 0
            and not self.is_processing_detection
        ):
            small = cv2.resize(rgb, (0, 0), fx=0.5, fy=0.5)
            locations = face_recognition.face_locations(small, model="hog")
            face_count = len(locations)
            scale = 2

            # =========================
            # MULTIPLE FACES
            # =========================
            if face_count > 1:
                self.blink_detector.reset()
                self._set_auth_status(
                    "⚠ Multiple Faces Detected - Please Stand Alone", "red"
                )
                for top, right, bottom, left in locations:
                    cv2.rectangle(
                        rgb,
                        (left * scale, top * scale),
                        (right * scale, bottom * scale),
                        (255, 0, 0),
                        3,
                    )
                    self.double_info_sound.play()
                self._show_frame(rgb)
                return

            # =========================
            # SINGLE FACE
            # =========================
            if face_count == 1:
                for top, right, bottom, left in locations:
                    cv2.rectangle(
                        rgb,
                        (left * scale, top * scale),
                        (right * scale, bottom * scale),
                        (0, 255, 0),
                        2,
                    )
                # =========================
                # AUTO CAPTURE
                # =========================
                if not self.blink_detector.verified:

                    self._set_auth_status(
                        f"👁 Blink Required ({self.blink_detector.blink_count}/1)",
                        "blue"
                    )

                    blink_ok = self.blink_detector.process(rgb)

                    if blink_ok:

                        self.blink_detector.verified = True

                    self._show_frame(rgb)
                    return

                # Blink passed
                captured_frame = frame.copy()

                self.is_processing_detection = True

                self.process_attendance(captured_frame)

            # =========================
            # NO FACE
            # =========================
            else:
                
                self.blink_detector.reset()
                self._set_auth_status("No face detected", "blue")

        # =========================
        # SHOW FRAME
        # =========================
        self._show_frame(rgb)

    # =========================
    # PROCESS ATTENDANCE
    # =========================

    def process_attendance(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # =========================
        # DETECT AGAIN
        # =========================
        locations = face_recognition.face_locations(rgb)

        # =========================
        # SECURITY CHECK
        # =========================
        if len(locations) != 1:
            self.is_processing_detection = False
            self._set_auth_status("⚠ Invalid Face Detection", "red")
            return

        # =========================
        # ENCODE FACE
        # =========================
        encodings = face_recognition.face_encodings(rgb, locations)
        if not encodings:
            self.is_processing_detection = False
            self._set_auth_status("✗ Face Encoding Failed", "red")
            return
        enc = encodings[0]

        # =========================
        # MATCHING
        # =========================
        name = "Unknown"
        emp_id = None
        color = (255, 71, 87)
        if self.known_encodings:
            matches = face_recognition.compare_faces(
                self.known_encodings, enc, tolerance=0.5
            )
            dists = face_recognition.face_distance(self.known_encodings, enc)
            best = np.argmin(dists)
            if matches[best]:
                name = self.known_names[best]
                emp_id = self.known_ids[best]
                color = (0, 230, 118)

        # =========================
        # UNKNOWN FACE
        # =========================
        if not emp_id:
            self.is_processing_detection = False
            self.cooldown = 15
            self._set_auth_status("✗ Unknown Face", "red")
            self.error_sound.play()
            QTimer.singleShot(2000, lambda: self._set_auth_status("", ""))
            return

        # =========================
        # MARK ATTENDANCE
        # =========================
        marked = mark_attendance(emp_id)
        self.last_recognized = emp_id

        # =========================
        # UPDATE UI
        # =========================
        self.rec_name.setText(name)
        self.rec_empid.setText(f"Employee ID : {emp_id}")

        # =========================
        # FIND DEPARTMENT
        # =========================
        emps = get_all_employees()
        department = "N/A"
        for emp in emps:
            if emp["emp_id"] == emp_id:
                department = emp["department"]
                break
        self.rec_department.setText(f"Department : {department}")
        self.rec_status.setText("Status : Present")
        self.rec_time.setText(
            f"Recognized At : {datetime.now().strftime('%H:%M:%S')}"
        )

        # =========================
        # SUCCESS
        # =========================

        if marked == "SUCCESS":
            self._set_auth_status(f"✓ {name} — Attendance Marked!", "green")
            self.refresh_log()
            self.success_sound.play()
            
            # TRIGGER SUCCESS POPUP
            self.trigger_popup("✅", "Attendance Marked", f"Identity verified for {name}", "#16a34a")
            
            QTimer.singleShot(4000, lambda: self._set_auth_status("", ""))
            self.stop_camera()
            self._set_auth_status(f"✓ {name} — Attendance Marked!", "green")
            self.is_processing_detection = False

        elif marked == "ALREADY_DONE":
            self.info_sound.play()
            self._set_auth_status(f"ℹ {name} — Already Marked Today", "blue")
            
            # TRIGGER INFO POPUP
            self.trigger_popup("ℹ️", "Already Taken", f"{name} is already present today.", "#b6df5b")
            
            QTimer.singleShot(4000, lambda: self._set_auth_status("", ""))
            self.stop_camera()
            self.is_processing_detection = False

        else:
            self._set_auth_status(f"✗ {name} — Attendance Failed", "red")
            
            # TRIGGER ERROR POPUP
            self.trigger_popup("❌", "Failed", "Could not mark attendance.", "#dc2626")
            
            QTimer.singleShot(4000, lambda: self._set_auth_status("", ""))
            self.stop_camera()
            self.is_processing_detection = False
    
        # SECURITY RESET
        self.cooldown = 30

        
    def trigger_popup(self, icon, title, subtitle, color):
        # Create the dynamic popup
        self.popup = StatusPopup(self, icon, title, subtitle, color)

        # Center it inside the AttendancePage widget
        self.popup.move(
            (self.width() - self.popup.width()) // 2,
            (self.height() - self.popup.height()) // 2
        )

        self.popup.setWindowOpacity(0)
        self.popup.show()

        # Fade In
        self.fade_in = QPropertyAnimation(self.popup, b"windowOpacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.start()

        # Auto close after 2.5 seconds
        QTimer.singleShot(2500, self.fade_out_popup)

    def fade_out_popup(self):
        self.fade_out = QPropertyAnimation(self.popup, b"windowOpacity")
        self.fade_out.setDuration(300)
        self.fade_out.setStartValue(1)
        self.fade_out.setEndValue(0)
        self.fade_out.finished.connect(self.popup.close)
        self.fade_out.start()


    def _show_frame(self, rgb):
        if self.cap is not None:
            h, w, ch = rgb.shape
            img = QImage(rgb.data, w, h, QImage.Format.Format_RGB888)
            pix = QPixmap.fromImage(img).scaled(
                self.cam_widget.width(),
                self.cam_widget.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.cam_widget.setPixmap(pix)

    # =========================
    # STATUS
    # =========================

    def _set_auth_status(self, text, color):
        colors = {
            "green": """
                background:#00e67622;
                color:#00e676;
                border:1px solid #00e67650;
                """,
            "red": """
                background:#ff475722;
                color:#ff4757;
                border:1px solid #ff475750;
                """,
            "blue": """
                background:#00d4ff22;
                color:#00d4ff;
                border:1px solid #00d4ff50;
                """,
        }
        self.auth_status.setText(text)
        self.auth_status.setStyleSheet(
            f"""
            border-radius:10px;
            padding:10px;
            font-size:14px;
            font-weight:600;
            {colors.get(color, '')}
            """
        )

    # =========================
    # REFRESH LOG
    # =========================

    def refresh_log(self):
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

    # =========================
    # CLOSE EVENT
    # =========================

    def closeEvent(self, e):
        self.stop_camera()
        super().closeEvent(e)