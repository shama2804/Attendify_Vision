import cv2
import os
import csv

cam = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

student_id = input("Enter Student ID: ")
student_name = input("Enter Student Name: ")
dataset_path = f"dataset/{student_id}_{student_name}"

if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

csv_file = "students.csv"

student_exists = False
try:
    with open(csv_file, 'r', newline='') as file:  
        reader = csv.reader(file)
        header = next(reader, None)  
        if header != ['id', 'name']:
            print("[ERROR] students.csv header is incorrect.  It should be 'id,name'")
            exit()

        for row in reader:
            if row and len(row) == 2 and row[0] == student_id: 
                student_exists = True
                break
except FileNotFoundError:
    print(f"[ERROR] students.csv not found.  Make sure it exists and has a header row 'id,name'")
    exit()
except Exception as e:
    print(f"[ERROR] An error occurred while reading students.csv: {e}")
    exit()


if not student_exists:
    try:
        with open(csv_file, 'a', newline='') as file: 
            writer = csv.writer(file)
            writer.writerow([student_id, student_name])
        print(f"[INFO] Added {student_name} (ID: {student_id}) to students.csv")
    except Exception as e:
        print(f"[ERROR] Could not write to students.csv: {e}")
        exit()

print("[INFO] Capturing images. Look at the camera...")

count = 0
while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        cv2.imwrite(f"{dataset_path}/{count}.jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow("Capture Images", frame)
    if cv2.waitKey(1)==27 or count >= 200:  
        break

print("[INFO] Image capturing complete.")
cam.release()
cv2.destroyAllWindows()
