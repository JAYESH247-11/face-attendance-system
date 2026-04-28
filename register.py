from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QComboBox, QPushButton, QFrame,
                             QGridLayout, QMessageBox, QSizePolicy, QScrollArea)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap, QFont
import cv2
import numpy as np
from database import add_employee
from database import get_all_employees
import face_recognition
import numpy as np


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
        # Use the faster constructor and avoid unnecessary copying
        img = QImage(frame_rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        
        # Scaling is expensive; only do it if the widget size actually changed
        pix = QPixmap.fromImage(img).scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation # High quality scaling
        )
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
        self.setup_ui()
        self.frame_counter = 0
        self.face_locations = []

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

    def start_camera(self):
        # 🔥 Use faster backend (Windows)
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # 🔥 Reduce buffer (VERY IMPORTANT)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # 🔥 Set resolution (balance speed + quality)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # 🔥 Optional: reduce exposure delay
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        if self.cap.isOpened():
            self.timer.start(40)   # slightly slower = smoother
            self.capture_btn.setEnabled(True)
            self.start_btn.setEnabled(False)
        else:
            QMessageBox.warning(self, "Camera Error", "Could not open camera!")

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
        if not self.cap or not self.cap.isOpened():
            return
            
        ret, frame = self.cap.read()
        if not ret: return

        frame = cv2.flip(frame, 1)
        self.current_frame = frame.copy()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.frame_counter += 1
        if self.frame_counter % 3 == 0:
            if FACE_LIB:
                # Resize to 1/4 size for much faster detection
                small_frame = cv2.resize(rgb, (0, 0), fx=0.25, fy=0.25)
                self.face_locations = face_recognition.face_locations(small_frame)
                self.face_detected = len(self.face_locations) > 0
            else:
                # Fallback detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                self.face_locations = face_cascade.detectMultiScale(gray, 1.1, 4)
                self.face_detected = len(self.face_locations) > 0

        # --- DRAWING (Every frame for smoothness) ---
        scale = 4 # match the 0.25 resize
        for (top, right, bottom, left) in self.face_locations:
            # Scale coordinates back up
            cv2.rectangle(rgb, (left*scale, top*scale), (right*scale, bottom*scale), (0, 212, 255), 2)

        # Update status text only when it changes to prevent UI flickering
        self.update_status_ui()

        self.cam_widget.show_frame(rgb)
    
    def update_status_ui(self):
        if self.face_detected:
                msg = f"✓ Face detected"
                if self.face_status.text() != msg:
                    self.face_status.setText(msg)
                    self.face_status.setObjectName("face_status_ok")
                    self.face_status.setStyleSheet("background:#00e67622; color:#00e676; border-radius:8px;")
        else:
                if self.face_status.text() != "No face detected":
                    self.face_status.setText("No face detected")
                    self.face_status.setObjectName("face_status_neutral")
                    self.face_status.setStyleSheet("background:#1e2433; color:#718096; border-radius:8px;")

    def is_dublicate_face(self,new_encoding):
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
            QMessageBox.warning(self, "Error", "No camera frame available!")
            return
        if not self.face_detected:
            QMessageBox.warning(self, "No Face", "Please position your face in front of the camera.")
            return

        frame = self.current_frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if FACE_LIB:
            encs = face_recognition.face_encodings(rgb)
            if encs:
                self.captured_encoding = encs[0]
                self.captured_lbl.setText("✓  Face captured & encoded successfully!")
                QMessageBox.information(self, "Success", "Face captured successfully!")
            else:
                QMessageBox.warning(self, "Error", "Could not encode face. Try again.")
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
            QMessageBox.warning(self, "Validation", "Employee ID and Name are required!")
            return
        if self.captured_encoding is None:
            QMessageBox.warning(self, "Face Required", "Please capture face photo before registering!")
            return

        if self.is_dublicate_face(self.captured_encoding):
            QMessageBox.warning(self,"Dublicate Face", "This face is already registered")
            return

        ok, msg = add_employee(emp_id, name, dept, desig, phone, email, self.captured_encoding)
        if ok:
            QMessageBox.information(self, "Success", msg)
            self.clear_form()
        else:
            QMessageBox.critical(self, "Error", msg)

    def clear_form(self):
        for inp in self.inputs.values():
            inp.clear()
        self.captured_encoding = None
        self.captured_lbl.setText("")

    def closeEvent(self, e):
        self.stop_camera()
        super().closeEvent(e)
