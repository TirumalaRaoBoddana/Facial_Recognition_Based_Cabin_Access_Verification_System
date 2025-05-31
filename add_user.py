import cv2
import face_recognition
import numpy as np
import pandas as pd
from datetime import datetime
import os
import csv
import time

class UserRegistration:
    def __init__(self, train_dir='train', db_file='authorized_users.csv'):
        self.train_dir = train_dir
        self.db_file = db_file

        # Just making sure the folder for storing images is there
        if not os.path.isdir(self.train_dir):
            os.makedirs(self.train_dir)

        self._setup_db()

    def _setup_db(self):
        # Set up the CSV file if it doesn't already exist
        if not os.path.exists(self.db_file):
            with open(self.db_file, mode='w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Name", "Encoding", "Timestamp"])  # setting up basic headers

    def save_user(self, name, encoding, image_data):
        # Save the user's face encoding and image snapshot
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        face_data = {
            "Name": name,
            "Encoding": encoding.tolist(),  # this gets huge in the CSV, FYI
            "Timestamp": ts
        }
        try:
            data = pd.read_csv(self.db_file)
        except Exception as e:
            print(f"[DEBUG] Couldn't read CSV, creating new one. Error: {e}")
            data = pd.DataFrame(columns=["Name", "Encoding", "Timestamp"])
        data = pd.concat([data, pd.DataFrame([face_data])], ignore_index=True)
        data.to_csv(self.db_file, index=False)
        filename = f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        filepath = os.path.join(self.train_dir, filename)
        cv2.imwrite(filepath, image_data) 
        print(f"[OK] Registered '{name}' — snapshot saved at: {filepath}")
    def register_user(self, frame=None):
        user_name = input("Enter the new user's name: ").strip()
        if not user_name:
            print("[ERROR] Gotta enter a name.")
            return
        try:
            users = pd.read_csv(self.db_file)
        except Exception:
            users = pd.DataFrame(columns=["Name", "Encoding", "Timestamp"])  
        if user_name in users["Name"].values:
            overwrite = input(f"[!] '{user_name}' is already in the system. Overwrite? (y/n): ").strip().lower()
            if overwrite != 'y':
                print("[INFO] Alright, skipping registration.")
                return
            users = users[users["Name"] != user_name] 
        if frame is None:
            print("[FAIL] No image frame passed. Was the camera on?")
            return
        # Convert image from BGR (OpenCV default) to RGB — required for face_recognition
        try:
            rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(f"[ERROR] Failed to convert image. {e}")
            return
        faces_found = face_recognition.face_locations(rgb_img)
        if len(faces_found) == 0:
            print("[X] No face detected. Try getting closer?")
            return
        elif len(faces_found) > 1:
            print(f"[!] Multiple faces found ({len(faces_found)}). Try registering just one at a time.")
            return
        # Grab the face encoding — should only be one
        try:
            encoding = face_recognition.face_encodings(rgb_img, faces_found)[0]
        except IndexError:
            print("[X] Couldn't extract encoding for some reason. Try again.")
            return
        # Append new user
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "Name": user_name,
            "Encoding": encoding.tolist(),
            "Timestamp": now
        }

        users = pd.concat([users, pd.DataFrame([entry])], ignore_index=True)
        users.to_csv(self.db_file, index=False)
        # Save the image with a bit of timestamp for uniqueness
        pic_name = f"{user_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        save_to = os.path.join(self.train_dir, pic_name)
        cv2.imwrite(save_to, frame)  # Not checking if this fails but maybe should
        print(f"[DONE] '{user_name}' successfully added. Image saved: {save_to}")