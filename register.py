import face_recognition
import numpy as np
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QComboBox, QPushButton, QFrame,
                             QGridLayout, QMessageBox, QSizePolicy, QScrollArea)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap, QFont
import cv2
import numpy as np
from database import add_employee
from database import get_all_employees
from popup import StatusPopup
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation


try:
    import face_recognition
    FACE_LIB = True
except ImportError:
    FACE_LIB = False


class CameraWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setObjectName("camera_label")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("📷  Camera not started")
        self.setMinimumSize(320, 240)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet("background:#080a0f; border-radius:12px; color:#4a5568; font-size:14px;")

    def show_frame(self, frame_rgb):
        h, w, ch = frame_rgb.shape
        img = QImage(frame_rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        pix = QPixmap.fromImage(img).scaled(
            self.width(), self.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(pix)


class RegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)
        self.captured_encoding = None
        self.current_frame = None
        self.face_detected = False
        face_count = 0
        self.setup_ui()

    def setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(32, 32, 32, 32)
        outer.setSpacing(20)

        # Title
        title = QLabel("Register Employee")
        title.setObjectName("page_title")
        sub = QLabel("Fill employee details and capture face photo for authentication")
        sub.setObjectName("page_subtitle")
        outer.addWidget(title)
        outer.addWidget(sub)

        # Main content
        content = QHBoxLayout()
        content.setSpacing(24)

        # ---- LEFT: Form ----
        form_card = QFrame()
        form_card.setObjectName("section_card")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(24, 24, 24, 24)
        form_layout.setSpacing(14)

        form_title = QLabel("EMPLOYEE INFORMATION")
        form_title.setObjectName("card_title")
        form_layout.addWidget(form_title)

        fields = [
            ("Employee ID *", "emp_id", "EMP-001"),
            ("Full Name *",   "name",   "John Doe"),
            ("Department",    "dept",   "Engineering"),
            ("Designation",   "desig",  "Software Engineer"),
            ("Phone",         "phone",  "+91 9876543210"),
            ("Email",         "email",  "john@company.com"),
        ]
        self.inputs = {}
        grid = QGridLayout()
        grid.setSpacing(10)
        for i, (label, key, placeholder) in enumerate(fields):
            lbl = QLabel(label)
            lbl.setObjectName("form_label")
            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            inp.setMinimumHeight(42)
            self.inputs[key] = inp
            grid.addWidget(lbl, i, 0)
            grid.addWidget(inp, i, 1)

        form_layout.addLayout(grid)
        form_layout.addStretch()

        # Submit button
        self.submit_btn = QPushButton("✓  Register Employee")
        self.submit_btn.setObjectName("success_btn")
        self.submit_btn.setMinimumHeight(46)
        self.submit_btn.clicked.connect(self.register)
        form_layout.addWidget(self.submit_btn)

        clear_btn = QPushButton("Clear Form")
        clear_btn.setObjectName("danger_btn")
        clear_btn.setMinimumHeight(38)
        clear_btn.clicked.connect(self.clear_form)
        form_layout.addWidget(clear_btn)

        content.addWidget(form_card, 1)

        # ---- RIGHT: Camera ----
        cam_card = QFrame()
        cam_card.setObjectName("section_card")
        cam_layout = QVBoxLayout(cam_card)
        cam_layout.setContentsMargins(20, 20, 20, 20)
        cam_layout.setSpacing(12)

        cam_title = QLabel("FACE CAPTURE")
        cam_title.setObjectName("card_title")
        cam_layout.addWidget(cam_title)

        self.cam_widget = CameraWidget()
        self.cam_widget.setMinimumHeight(260)
        cam_layout.addWidget(self.cam_widget)

        # Status label
        self.face_status = QLabel("No face detected")
        self.face_status.setObjectName("face_status_neutral")
        self.face_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.face_status.setMinimumHeight(36)
        cam_layout.addWidget(self.face_status)

        # Captured indicator
        self.captured_lbl = QLabel("")
        self.captured_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.captured_lbl.setStyleSheet("color:#00e676; font-weight:600; font-size:12px;")
        cam_layout.addWidget(self.captured_lbl)

        # Camera buttons
        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("▶  Start Camera")
        self.start_btn.setObjectName("primary_btn")
        self.start_btn.setMinimumHeight(42)
        self.start_btn.clicked.connect(self.start_camera)

        self.capture_btn = QPushButton("📸  Capture Face")
        self.capture_btn.setObjectName("capture_btn")
        self.capture_btn.setMinimumHeight(42)
        self.capture_btn.setEnabled(False)
        self.capture_btn.clicked.connect(self.capture_face)

        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.capture_btn)
        cam_layout.addLayout(btn_row)

        self.stop_btn = QPushButton("■  Stop Camera")
        self.stop_btn.setObjectName("danger_btn")
        self.stop_btn.setMinimumHeight(38)
        self.stop_btn.clicked.connect(self.stop_camera)
        cam_layout.addWidget(self.stop_btn)

        if not FACE_LIB:
            warn = QLabel("⚠  face_recognition not installed.\nInstall: pip install face_recognition")
            warn.setStyleSheet("color:#ffb300; font-size:11px; background:#ffb30015; border-radius:6px; padding:8px;")
            warn.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cam_layout.addWidget(warn)

        cam_layout.addStretch()
        content.addWidget(cam_card, 1)

        outer.addLayout(content)


    def trigger_popup(self, icon, title, subtitle, color):
        self.popup = StatusPopup(self, icon, title, subtitle, color)
        
        # Center the popup
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

    def start_camera(self):
        # Use faster backend (Windows)
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        # Reduce buffer (VERY IMPORTANT)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)

        # Set resolution (balance speed + quality)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Optional: reduce exposure delay
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        if self.cap.isOpened():
            self.timer.start(40)   # slightly slower = smoother
            self.capture_btn.setEnabled(True)
            self.start_btn.setEnabled(False)
        else:
            self.trigger_popup("📷", "Camera Error", "Could not open camera!", "#dc2626")

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.cam_widget.clear()
        self.cam_widget.setText("📷  Camera stopped")
        self.capture_btn.setEnabled(False)
        self.start_btn.setEnabled(True)
        self.face_status.setText("No face detected")
        self.face_status.setObjectName("face_status_neutral")

    def _update_frame(self):
        if not self.cap:
            return
        ret, frame = self.cap.read()
        if not ret:
            return
        frame = cv2.flip(frame,1)
        self.current_frame = frame.copy()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #improve brightness and contrast
        rgb = cv2.convertScaleAbs(rgb, alpha=1.2, beta=20)

        # Draw face rectangles
        if FACE_LIB:
            small = cv2.resize(rgb, (0, 0), fx=0.5, fy=0.5)
            locations = face_recognition.face_locations(small, model="hog")
            face_count = len(locations)
            self.face_detected = face_count > 0
            scale = 2
            if face_count > 1:
                self.face_status.setText(f"✓  Face detected ({len(locations)}), Not Allowed to register")
                self.face_status.setObjectName("face_status_warning")
                for (top, right, bottom, left) in locations:
                    cv2.rectangle(rgb,
                        (left * scale, top * scale),
                        (right * scale, bottom * scale),
                        (255, 0, 0),
                        3)
                self.cam_widget.show_frame(rgb)
                return
            
            #single face detected, draw green box
            if face_count == 1:
                self.face_status.setText(f"✓  Face detected")
                self.face_status.setObjectName("face_status_ok")
                for (top, right, bottom, left) in locations:
                    cv2.rectangle(rgb,
                        (left*scale, top*scale),
                        (right*scale, bottom*scale),
                        (0, 212, 255), 2)
            else:
                self.face_status.setText("No face detected")
                self.face_status.setObjectName("face_status_neutral")
            self.face_status.style().unpolish(self.face_status)
            self.face_status.style().polish(self.face_status)
        else:
            # OpenCV haar fallback
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            self.face_detected = len(faces) > 0
            for (x, y, w, h) in faces:
                cv2.rectangle(rgb, (x, y), (x+w, y+h), (0, 212, 255), 2)

        self.cam_widget.show_frame(rgb)

    def is_duplicate_face(self,new_encoding):
        employee = get_all_employees()

        for emp in employee:
            if emp["face_encoding"] is not None:
                known_encoding = emp["face_encoding"]

                match = face_recognition.compare_faces(
                    [known_encoding], new_encoding,tolerance=0.5
                )

                if match[0]:
                    return True
        return False


    def capture_face(self):
        if self.current_frame is None:
            self.trigger_popup("⚠️", "Error", "No camera frame available!", "#dc2626")
            return
        if not self.face_detected:
            self.trigger_popup("⚠️", "No Face", "Please position your face in front of the camera.", "#dc2626")
            return

        frame = self.current_frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if FACE_LIB:
            encs = face_recognition.face_encodings(rgb)
            if len(encs) != 1:
                self.trigger_popup("⚠️", "Face Error", "Exactly one face must be visible!", "#dc2626")
                return
            if encs:
                self.captured_encoding = encs[0]
                self.captured_lbl.setText("✓  Face captured & encoded successfully!")
                self.trigger_popup("✅", "Success", "Face captured successfully!", "#16a34a")
                self.stop_camera()
                return
            else:
                self.trigger_popup("❌", "Error", "Could not encode face. Try again.", "#dc2626")
        else:
            # Store dummy encoding if library not installed
            self.captured_encoding = np.zeros(128)
            self.captured_lbl.setText("✓  Face captured (basic mode)")

    def register(self):
        emp_id = self.inputs["emp_id"].text().strip()
        name   = self.inputs["name"].text().strip()
        dept   = self.inputs["dept"].text().strip()
        desig  = self.inputs["desig"].text().strip()
        phone  = self.inputs["phone"].text().strip()
        email  = self.inputs["email"].text().strip()

        if not emp_id or not name:
            self.trigger_popup("📝", "Validation", "Employee ID and Name are required!", "#eab308")
            return
            
        if self.captured_encoding is None:
            self.trigger_popup("📸", "Face Required", "Capture face photo before registering!", "#eab308")
            return

        if self.is_duplicate_face(self.captured_encoding):
            self.trigger_popup("🚫", "Duplicate Face", "This face is already registered.", "#dc2626")
            return

        ok, msg = add_employee(emp_id, name, dept, desig, phone, email, self.captured_encoding)
        if ok:
            # REPLACED: QMessageBox.information
            self.trigger_popup("✅", "Registered", f"{name} registered successfully!", "#16a34a")
            self.clear_form()
        else:
            # REPLACED: QMessageBox.critical
            self.trigger_popup("❌", "Database Error", msg, "#dc2626")

    def clear_form(self):
        for inp in self.inputs.values():
            inp.clear()
        self.captured_encoding = None
        self.captured_lbl.setText("")

    def closeEvent(self, e):
        self.stop_camera()
        super().closeEvent(e)
