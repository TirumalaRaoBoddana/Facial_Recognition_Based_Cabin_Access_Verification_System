import cv2
import face_recognition
import numpy as np
import pandas as pd
from datetime import datetime
import os
import csv
import time

# Import the UserRegistration class from your add_user.py file
from add_user import UserRegistration

class FaceAccessControl:
    def __init__(self, db_file='authorized_users.csv', log_file='access_log.csv', train_dir='train'):
        self.db_file = db_file
        self.log_file = log_file
        self.train_dir = train_dir

        self.authorized_face_encodings = []
        self.authorized_face_names = []

        self._init_log_file()
        self._load_authorized_users()

        # Initialize the UserRegistration instance, passing the same paths
        self.registrar = UserRegistration(train_dir=self.train_dir, db_file=self.db_file)

        # Variables for display feedback
        self.display_message = ""
        self.message_color = (255, 255, 255) # White
        self.message_start_time = 0
        self.message_duration = 3 # seconds

    def _init_log_file(self):
        """Initializes the access log CSV file if it doesn't exist."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Timestamp", "Status"])

    def _load_authorized_users(self):
        """Loads authorized users' names and encodings from the database."""
        if not os.path.exists(self.db_file):
            print(f"[ERROR] Authorized users database '{self.db_file}' not found. Please register users using the 'A' key functionality.")
            self.authorized_face_encodings = []
            self.authorized_face_names = []
            return

        try:
            df = pd.read_csv(self.db_file)
        except pd.errors.EmptyDataError:
            print("[WARNING] Authorized users database is empty. No users to recognize.")
            self.authorized_face_encodings = []
            self.authorized_face_names = []
            return

        if df.empty:
            print("[WARNING] Authorized users database is empty. No users to recognize.")
            self.authorized_face_encodings = []
            self.authorized_face_names = []
            return

        loaded_names = []
        loaded_encodings = []

        for index, row in df.iterrows():
            name = row["Name"]
            encoding_str = row["Encoding"]

            if pd.isna(encoding_str):
                print(f"[WARNING] Skipping user '{name}' due to missing or invalid face encoding.")
                continue

            try:
                encoding_list = eval(str(encoding_str))
                if isinstance(encoding_list, list):
                    loaded_names.append(name)
                    loaded_encodings.append(np.array(encoding_list))
                else:
                    print(f"[WARNING] Encoding for user '{name}' is not a list after eval(). Skipping.")
            except (SyntaxError, NameError, TypeError, ValueError) as e:
                print(f"[ERROR] Failed to parse encoding for user '{name}': {e}. Skipping this entry.")

        self.authorized_face_names = loaded_names
        self.authorized_face_encodings = loaded_encodings

        print(f"[INFO] Loaded {len(self.authorized_face_names)} authorized users from {self.db_file}.")

    def _log_access(self, name, status):
        """Logs the access attempt to the CSV file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, timestamp, status])
        print(f"[LOG] {name} - {timestamp} - {status}")

    def _set_display_message(self, message, color=(255, 255, 255)):
        """Sets a message to be displayed on the screen for a short duration."""
        self.display_message = message
        self.message_color = color
        self.message_start_time = time.time()

    def run_access_control(self):
        """Runs the main facial recognition access control system."""
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            print("[ERROR] Cannot access the camera. Exiting.")
            return

        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        print("[INFO] Facial Recognition Access Control System Active.")
        print("[INFO] Press 'A' to register a new user (admin functionality).")
        print("[INFO] Press 'Q' to quit.")
        
        cv2.namedWindow('Facial Recognition-Based Cabin Access Verification System', cv2.WINDOW_NORMAL) # Create window at start

        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("[ERROR] Failed to grab frame. Reattempting...")
                time.sleep(0.1)
                continue

            frame = cv2.flip(frame, 1) # Flip frame horizontally

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    name = "Unknown"
                    access_status = "Denied"

                    if self.authorized_face_encodings:
                        matches = face_recognition.compare_faces(self.authorized_face_encodings, face_encoding)
                        face_distances = face_recognition.face_distance(self.authorized_face_encodings, face_encoding)

                        if len(face_distances) > 0:
                            best_match_index = np.argmin(face_distances)
                            if matches[best_match_index]:
                                name = self.authorized_face_names[best_match_index]
                                access_status = "Granted"

                    face_names.append(name)
                    self._log_access(name, access_status)
                    self._set_display_message(f"Access: {access_status} for {name}",
                                               color=(0, 255, 0) if access_status == "Granted" else (0, 0, 255))

            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                color = (0, 0, 255) if name == "Unknown" else (0, 255, 0)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            if time.time() - self.message_start_time < self.message_duration:
                (text_width, text_height), _ = cv2.getTextSize(self.display_message, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                text_x = (frame.shape[1] - text_width) // 2
                text_y = 30

                cv2.putText(frame, self.display_message, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4, cv2.LINE_AA)
                cv2.putText(frame, self.display_message, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, self.message_color, 2, cv2.LINE_AA)

            font_instructions = cv2.FONT_HERSHEY_SIMPLEX
            text_color_instructions = (255, 255, 255)
            outline_color_instructions = (0, 0, 0)

            text_a = "Press 'A' to Register New User"
            (text_a_width, text_a_height), _ = cv2.getTextSize(text_a, font_instructions, 0.7, 2)
            text_a_x = frame.shape[1] - text_a_width - 20
            text_a_y = frame.shape[0] - 60

            cv2.putText(frame, text_a, (text_a_x, text_a_y), font_instructions, 0.7, outline_color_instructions, 3, cv2.LINE_AA)
            cv2.putText(frame, text_a, (text_a_x, text_a_y), font_instructions, 0.7, text_color_instructions, 1, cv2.LINE_AA)

            text_q = "Press 'Q' to Quit"
            (text_q_width, text_q_height), _ = cv2.getTextSize(text_q, font_instructions, 0.7, 2)
            text_q_x = frame.shape[1] - text_q_width - 20
            text_q_y = frame.shape[0] - 20

            cv2.putText(frame, text_q, (text_q_x, text_q_y), font_instructions, 0.7, outline_color_instructions, 3, cv2.LINE_AA)
            cv2.putText(frame, text_q, (text_q_x, text_q_y), font_instructions, 0.7, text_color_instructions, 1, cv2.LINE_AA)
            
            cv2.imshow('Facial Recognition Access Control', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("[INFO] Quitting Facial Recognition-Based Cabin Access Verification System")
                break
            elif key == ord('a'): # Press 'A' to register a new user
                print("\n[ADMIN] Initiating new user registration process...")
                
                # Release the current video capture and close its window
                video_capture.release()
                cv2.destroyAllWindows()
                
                # Call the register_user method from the UserRegistration instance
                # This will handle the name input from console and background face capture
                self.registrar.register_user()
                
                # Re-initialize the video capture for access control
                video_capture = cv2.VideoCapture(0)
                if not video_capture.isOpened():
                    print("[FATAL ERROR] Could not re-access camera after registration. Please restart the script.")
                    self.display_message = "Camera Error! Restart Needed."
                    self.message_color = (0, 0, 255) # Red
                    time.sleep(5) # Give user time to read error
                    break # Exit if camera cannot be re-opened

                # Re-create the main access control window
                cv2.namedWindow('Facial Recognition Access Control', cv2.WINDOW_NORMAL) 
                
                # Reload authorized users to include the new one
                self._load_authorized_users()
                # Set display message to confirm registration attempt
                self._set_display_message("Registration Process Completed", (0, 255, 255)) # Cyan message

        video_capture.release()
        cv2.destroyAllWindows()

# For direct execution
if __name__ == "__main__":
    os.makedirs('train', exist_ok=True)
    access_system = FaceAccessControl()
    access_system.run_access_control()