import cv2
import csv
import os
from datetime import datetime

# Load the trained model and Haar cascade
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Paths
students_csv = "students.csv"
database_folder = "database"

# Ensure database folder exists
if not os.path.exists(database_folder):
    os.makedirs(database_folder)

# Get current date for folder naming
current_date = datetime.now().strftime("%d-%m-%Y")
date_folder_path = os.path.join(database_folder, current_date)

# Ensure date-based folder exists
if not os.path.exists(date_folder_path):
    os.makedirs(date_folder_path)

# Prompt for lecture/class name
lecture_name = input("Enter Lecture/Class Name: ")
lecture_folder_path = os.path.join(date_folder_path, lecture_name)

# Ensure lecture folder exists
if not os.path.exists(lecture_folder_path):
    os.makedirs(lecture_folder_path)

# Create a CSV file for attendance in the lecture folder
attendance_file = os.path.join(lecture_folder_path, f"{lecture_name}_attendance.csv")
if not os.path.exists(attendance_file):
    with open(attendance_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Student ID", "Name", "Attendance"])  # Header row

# Load student details from students.csv into a dictionary
students = {}
try:
    with open(students_csv, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            students[int(row[0])] = row[1]
except FileNotFoundError:
    print(f"[ERROR] File not found: {students_csv}")
    exit()

# Initialize webcam
cam = cv2.VideoCapture(0)
recognized_students = set()

print("[INFO] Recognizing faces...")
while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])
        print(f"[DEBUG] Face detected - ID: {id_}, Confidence: {confidence}")  # Debug line

        if confidence < 70:  # Confidence threshold
            name = students.get(id_, "Unknown")
            print(f"[DEBUG] Recognized face - ID: {id_}, Name: {name}")  # Debug line

            if id_ not in recognized_students:
                recognized_students.add(id_)

                # Write individual student attendance to a .txt file in the lecture folder
                student_attendance_file = os.path.join(lecture_folder_path, f"{name}.txt")
                with open(student_attendance_file, 'w') as student_file:
                    student_file.write(f"Student ID: {id_}\n")
                    student_file.write(f"Name: {name}\n")
                    student_file.write(f"Timestamp: {datetime.now()}\n")

                # Update attendance in the CSV file
                with open(attendance_file, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([id_, name, "Present"])

                print(f"[INFO] Attendance marked for {name}")

            cv2.putText(frame, name, (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        else:
            cv2.putText(frame, "Unknown", (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 3)

    cv2.imshow("Recognize Faces", frame)
    if cv2.waitKey(1) == 27:  # Press 'ESC' to exit
        break

cam.release()
cv2.destroyAllWindows()

# Mark absent students after recognition ends
with open(attendance_file, 'r') as file:
    reader = csv.reader(file)
    present_ids = [int(row[0]) for row in reader if row[0].isdigit()]

with open(attendance_file, 'a', newline='') as file:
    writer = csv.writer(file)
    for student_id, student_name in students.items():
        if student_id not in present_ids:
            writer.writerow([student_id, student_name, "Absent"])
