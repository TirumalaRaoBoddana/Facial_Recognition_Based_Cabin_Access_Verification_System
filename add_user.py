import cv2
import face_recognition
import numpy as np
import pandas as pd
from datetime import datetime
import os
import csv
class UserRegistration:
    def __init__(self, train_dir='train', db_file='authorized_users.csv'):
        self.train_dir = train_dir
        self.db_file = db_file
        os.makedirs(self.train_dir, exist_ok=True) # Ensure train directory exists [cite: 6]
        self._init_database()

    def _init_database(self):
        """Initializes the CSV database if it doesn't exist."""
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Encoding", "Timestamp"]) # Columns for Name, Encoding, Timestamp [cite: 4]

    def capture_face(self):
        """Captures a single face from the webcam."""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[ERROR] Cannot access the camera. Please check if it's connected and not in use by another application.")
            return None, None

        print("[INFO] Press A to capture your face. Ensure only one face is visible.")

        frame = None
        while True:
            ret, current_frame = cap.read()
            if not ret:
                print("[ERROR] Failed to capture frame. Exiting camera stream.")
                break

            # Display instructions on the frame
            cv2.putText(current_frame, "Press SPACE to Capture", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("Register New User", current_frame)

            key = cv2.waitKey(1) & 0xFF 
            if key == ord('a'):  
                frame = current_frame
                break
            elif key == ord('q'): # Allow 'q' to quit capture early
                print("[INFO] Capture cancelled by user.")
                break
        cap.release()
        cv2.destroyAllWindows()

        if frame is None:
            print("[ERROR] No frame captured or capture cancelled.")
            return None, None

        # Convert the captured frame to RGB (face_recognition expects RGB) [cite: 1]
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect face locations [cite: 1]
        face_locations = face_recognition.face_locations(rgb_frame)

        if len(face_locations) == 0:
            print("[ERROR] No face detected. Please try again ensuring your face is clearly visible.")
            return None, None
        elif len(face_locations) > 1:
            print(f"[ERROR] Detected {len(face_locations)} faces. Please ensure only one face is visible.")
            return None, None

        # Encode the detected face [cite: 1]
        face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]

        return frame, face_encoding

    def save_user(self, name, encoding, image):
        """Saves user encoding and image to CSV and train directory."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create new data row as a dictionary
        new_data = {
            "Name": name,
            "Encoding": encoding.tolist(),  # Convert numpy array to list for CSV storage
            "Timestamp": timestamp
        }

        # Load existing data from CSV
        # Handle case where CSV might be empty or new
        try:
            df = pd.read_csv(self.db_file)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=["Name", "Encoding", "Timestamp"])
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Name", "Encoding", "Timestamp"])
            # This case is handled by _init_database, but good for robustness

        # Convert new_data dictionary to a DataFrame row
        new_df_row = pd.DataFrame([new_data])

        # Use pd.concat to add the new row
        df = pd.concat([df, new_df_row], ignore_index=True)
        df.to_csv(self.db_file, index=False) # Save updated DataFrame back to CSV [cite: 2]

        # Save user image to the train directory [cite: 6]
        image_path = os.path.join(self.train_dir, f"{name}.jpg")
        cv2.imwrite(image_path, image)
        print(f"[SUCCESS] User '{name}' registered and saved. Image at: {image_path}")

    def register_user(self):
        """Main function to handle the entire registration process."""
        name = input("Enter the new user's name: ").strip()
        if not name:
            print("[ERROR] Name cannot be empty. Registration cancelled.")
            return

        # Check if the name already exists in the database
        if os.path.exists(self.db_file):
            df = pd.read_csv(self.db_file)
            if name in df["Name"].values:
                print(f"[WARNING] User '{name}' already exists. A new entry will be added. Consider a unique name or update manually.")
                # You could add logic here to ask if they want to overwrite/update

        image, encoding = self.capture_face()
        if encoding is not None and image is not None:
            self.save_user(name, encoding, image)
        else:
            print("[INFO] User registration process aborted.")
# For direct execution
if __name__ == "__main__":
    registrar = UserRegistration()
    registrar.register_user()