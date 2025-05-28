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
        os.makedirs(self.train_dir, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Initializes the CSV database if it doesn't exist."""
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Encoding", "Timestamp"])

    def save_user(self, name, encoding, image):
        """Saves user encoding and image."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = {
            "Name": name,
            "Encoding": encoding.tolist(),
            "Timestamp": timestamp
        }

        try:
            df = pd.read_csv(self.db_file)
        except (pd.errors.EmptyDataError, FileNotFoundError):
            df = pd.DataFrame(columns=["Name", "Encoding", "Timestamp"])

        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(self.db_file, index=False)

        img_path = os.path.join(self.train_dir, f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
        cv2.imwrite(img_path, image)
        print(f"[SUCCESS] User '{name}' registered. Image saved at: {img_path}")

    def register_user(self, frame=None):
        """Main function to handle user registration."""
        name = input("Enter the new user's name: ").strip()
        if not name:
            print("[ERROR] Name cannot be empty.")
            return

        # Load existing users
        try:
            df = pd.read_csv(self.db_file)
        except (pd.errors.EmptyDataError, FileNotFoundError):
            df = pd.DataFrame(columns=["Name", "Encoding", "Timestamp"])

        # Check if user already exists
        if name in df["Name"].values:
            choice = input(f"[WARNING] User '{name}' already exists. Do you want to overwrite? (y/n): ").strip().lower()
            if choice != 'y':
                print("[INFO] Registration cancelled by user.")
                return
            # Drop existing entries for the user
            df = df[df["Name"] != name]

        if frame is None:
            print("[ERROR] No frame provided for registration.")
            return

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if len(face_locations) == 0:
            print("[ERROR] No face detected. Try again.")
            return
        elif len(face_locations) > 1:
            print(f"[ERROR] Detected {len(face_locations)} faces. Show only one face.")
            return

        face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]

        # Save the new user
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = {
            "Name": name,
            "Encoding": face_encoding.tolist(),
            "Timestamp": timestamp
        }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(self.db_file, index=False)

        img_path = os.path.join(self.train_dir, f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
        cv2.imwrite(img_path, frame)
        print(f"[SUCCESS] User '{name}' registered. Image saved at: {img_path}")
