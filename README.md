# face-attendance-system
Real-time face recognition based attendance system using Python, OpenCV, and PyQt6 with automatic attendance marking and dashboard analytics.

# 🎯 FaceMark – Face Recognition Attendance System

![Python](https://img.shields.io/badge/Python-3.x-blue)
![PyQt6](https://img.shields.io/badge/UI-PyQt6-green)
![OpenCV](https://img.shields.io/badge/OpenCV-ComputerVision-red)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 📌 Overview

**FaceMark** is a real-time face recognition–based attendance system that automates employee attendance using biometric authentication.

The system captures facial data during registration and uses computer vision to recognize individuals via a live camera feed. Once identified, attendance is recorded automatically in a local database.

This project demonstrates the practical use of **Computer Vision + GUI Development + Database Integration** in a real-world application.

---

## 🚀 Features

* 🔍 Real-time face detection and recognition
* 🧠 Face encoding using `face_recognition` (dlib)
* 📝 Automatic attendance marking
* 📊 Dashboard with live statistics
* 👨‍💼 Employee registration system
* 📋 Present / Absent tracking
* 🔎 Search and filter functionality
* 🎨 Modern UI using PyQt6

---

## 🧰 Tech Stack

* **Language:** Python
* **Computer Vision:** OpenCV, face_recognition
* **GUI:** PyQt6
* **Database:** SQLite
* **Libraries:** NumPy, dlib

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/face-attendance-system.git
cd face-attendance-system
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ If face_recognition fails:

```bash
pip install cmake
pip install dlib
pip install face_recognition
```

---

## ▶️ Run the Application

```bash
python main.py
```

---

## 📂 Project Structure

```
face-attendance-system/
│
├── main.py           # Entry point
├── database.py       # Database operations
├── attendance.py     # Face recognition logic
├── register.py       # Employee registration
├── dashboard.py      # Analytics dashboard
├── employee_list.py  # Employee records
├── styles.py         # UI styling
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔄 How It Works

### 🧑‍💼 1. Register Employee

* Enter employee details
* Start camera
* Capture face
* Face encoding stored in database

### 📸 2. Mark Attendance

* Start camera
* System detects and recognizes face
* Attendance marked automatically

### 📋 3. View Records

* See Present / Absent status
* Filter by date or employee
* Real-time updates

---

## ⚠️ Important Notes

* `attendance.db` is **NOT included** for privacy reasons
* Face encodings (biometric data) are stored locally
* You must register employees before marking attendance

---

## 🔐 Privacy & Security

This project handles **biometric data (face encoding)**.
Do **not upload real user data publicly**.

---

## 📌 Future Improvements

* 🌐 Web-based version (FastAPI / Django)
* ☁️ Cloud database integration
* 📱 Mobile app support
* 🔔 Notification system
* 📈 Advanced analytics

---

## 👨‍💻 Author

**Jayesh Baraiya**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
