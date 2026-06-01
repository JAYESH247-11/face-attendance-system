# FaceMark - Face Authentication Attendance System
## Requirements

### Install Python packages:
```
pip install PyQt6 opencv-python numpy face_recognition
```

### face_recognition install (needs cmake & dlib):
```
pip install cmake
pip install dlib
pip install face_recognition
```

### Run the app:
```
python main.py
```

---

## File Structure
```
face_attendance/
├── main.py           # Entry point + Main window
├── database.py       # SQLite DB operations
├── styles.py         # Dark theme stylesheet
├── dashboard.py      # Dashboard with stats
├── register.py       # Employee registration + face capture
├── attendance.py     # Face authentication attendance
├── employee_list.py  # Present/Absent list
└── attendance.db     # Auto-created SQLite database
```

---

## How It Works

### 1. Register Employee
- Fill employee details (ID, Name, Department, etc.)
- Start camera and align face
- Click "Capture Face" → face encoding stored in DB

### 2. Mark Attendance
- Go to Attendance page
- Click "Start Camera"
- Employee looks at camera → face matched → attendance marked automatically

### 3. View List
- Shows all employees with Present/Absent status
- Filter by status or search by name/ID
- Refreshes in real-time
