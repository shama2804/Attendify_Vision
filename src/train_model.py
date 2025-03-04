import cv2
import numpy as np
import os
from PIL import Image

data_path = 'dataset/'
trainer_path = 'trainer/trainer.yml'

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
ids = []

for root, dirs, files in os.walk(data_path):
    for file in files:
        if file.endswith('.jpg'):
            image_path = os.path.join(root, file)
            gray_image = Image.open(image_path).convert('L')
            image_np = np.array(gray_image, 'uint8')
            id_ = int(os.path.basename(root).split('_')[0])
            faces_detected = face_cascade.detectMultiScale(image_np, scaleFactor=1.1, minNeighbors=5)
            print(f"Processing {image_path}, Faces detected: {len(faces_detected)}")  # Debug info

            for (x, y, w, h) in faces_detected:
                faces.append(image_np[y:y+h, x:x+w])
                ids.append(id_)

if len(faces) > 0:
    recognizer.train(faces, np.array(ids))
    recognizer.save(trainer_path)
    print(f"[INFO] Model trained and saved at {trainer_path}")
else:
    print("[WARNING] No faces found in the dataset!")
