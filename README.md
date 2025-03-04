# Attendify_Vision

## Overview
This Attendance Management System is an automated solution using facial recognition to streamline the attendance-taking process in educational institutions. It utilizes OpenCV for face detection and recognition, providing an efficient way to manage student profiles and track attendance.

## Features
- Face detection and recognition for automated attendance marking
- Student profile management
- Real-time attendance logging
- Attendance report generation
- Database exploration for attendance records

## Prerequisites
- Python 3.7+
- OpenCV
- NumPy
- Other dependencies (listed in requirements.txt)


## Usage

### **1. Add New Students**
Run the `capture_image.py` script to add new students:
python src/capture_image.py

text
- Enter the student's ID and name when prompted.
- Images will be captured and stored in the `dataset` directory.

### **2. Train the Model**
Run the `train_model.py` script to train the facial recognition model:
python src/train_model.py

text
- This will generate or update the `trainer.yml` file in the `trainer` folder.

### **3. Recognize Faces**
Run the `recognize_face.py` script to start real-time face recognition:
python src/recognize_face.py

text
- Enter the lecture/class name when prompted (e.g., `Adv Java`, `CN`, etc.).
- Attendance will be logged:
  - Individual `.txt` files will be created in the corresponding class folder inside `database`.
  - A centralized CSV file (`attendance.csv`) will be updated.

### **4. Check Attendance Logs**
Open the `attendance_logs/attendance.csv` file to view centralized attendance records.

### **5. Explore Database**
Navigate to the `database` folder to view dynamically created folders and files:
- Folders named by date (`date-month-year`).
- Subfolders for lecture/class names containing individual `.txt` files.

## Example Workflow

1. Run `capture_image.py` to add students (`Shama`, `Vicky`) with IDs (`1`, `2`).
2. Run `train_model.py` to train the model using captured images.
3. Run `recognize_face.py` during a lecture (e.g., `Adv Java`) to mark attendance.
4. Check:
   - Individual `.txt` files in `database/04-03-2025/Adv Java`.
   - Centralized logs in `attendance_logs/attendance.csv`.

## Future Enhancements
- Implement machine learning models for improved accuracy in facial recognition.
- Add support for generating PDF or Excel reports from attendance logs.
- Integrate with school management systems for seamless administrative workflows.


## Acknowledgments
- OpenCV for computer vision capabilities.
- Haar cascades for face detection algorithms.

