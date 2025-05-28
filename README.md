# Facial Recognition-Based Cabin Access Verification System

## Project Description

This project implements a real-time facial recognition system designed for access control. It utilizes a webcam feed to detect and recognize faces, comparing them against a database of authorized users. Based on the recognition, access is either granted or denied. The system also includes functionalities for registering new users and maintaining a log of all access attempts.

---

## Features

- **Real-time Face Detection & Recognition:** Identifies faces from a live webcam feed using `face_recognition` and OpenCV.
- **Access Validation:** Compares detected faces against a local database of authorized users (`authorized_users.csv`) to grant or deny access.
- **User Registration:** Admin can press `'A'` during live access control to register a new user by entering their name and capturing their face.
- **Access Logging:** Records every access attempt (Name, Timestamp, Status: Granted/Denied) in `access_log.csv`.
- **Persistent Data Storage:** Uses CSV files (`authorized_users.csv`, `access_log.csv`) for storing user data and logs.
- **Visual Feedback:** Displays bounding boxes around faces and status messages (Granted/Denied/Unknown) on the webcam feed.

---

## Folder Structure

facial_access_system/
├── train/                    # Stores authorized user face images
├── access_log.csv            # Log of all access attempts
├── authorized_users.csv      # Database of registered users (Name + Encodings)
├── add_user.py               # Script to add a new user
├── access_control.py         # Main script for recognition & access
├── report.pdf                # Summary of the work done
├── presentation.pptx         # 3-5 slides showcasing functionality
└── README.md                 # Instructions to run the project

---

## Prerequisites

Before running the project, ensure you have the following:

- **Python 3.7+**
- A working **webcam**
- **C++ Build Tools (for Windows):** Required for `dlib` and `face_recognition` installations.
  - You can get pre-built wheels or instructions at:
    [https://github.com/z-mahmud22/Dlib_Windows_Python3.x](https://github.com/z-mahmud22/Dlib_Windows_Python3.x)
  - Alternatively, install **Build Tools for Visual Studio** from
    [https://visualstudio.microsoft.com/downloads/](https://visualstudio.microsoft.com/downloads/)
    and select **"Desktop development with C++"** during installation.

---

## Installation

1.  **Clone the Repository** (or ensure all files are in one directory):
    ```bash
    git clone [https://github.com/TirumalaRaoBoddana/Facial_Recognition_Based_Cabin_Access_Verification_System](https://github.com/TirumalaRaoBoddana/Facial_Recognition_Based_Cabin_Access_Verification_System)
    cd Facial_Recognition_Based_Cabin_Access_Verification_System
    ```
2.  **Create a Virtual Environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install opencv-python face_recognition numpy<1.24 pandas
    ```
    **⚠️ Important Notes:**
    * `face_recognition` requires `dlib`, which may fail without C++ build tools on Windows.
    * Do not use `numpy==1.5`. It's very outdated and incompatible. Use `numpy<1.24` instead.

4.  **How to Run the Project**

    This project runs as a desktop application with a console interface for user registration.

    1.  **Ensure you have at least one user registered.** If not, you can register a user directly from the `access_control.py` app after starting it (see step 3 below).

    2.  **Open your terminal or command prompt** in the `facial_access_system/` directory.

    3.  **Run the main access control script:**

        ```bash
        python access_control.py
        ```

5.  **Interaction:**
    * A webcam window will appear titled "Facial Recognition Access Control".
    * Registered face: Shows user name + "Access Granted".
    * Unknown face: Shows "Unknown" + "Access Denied".
    * **To add a new user:**
        * Press 'A' while webcam is open.
        * Follow prompts in the console to input name and capture face.
    * To exit: Press 'Q' in the webcam window.

6. Important Notes & Troubleshooting
    * **Camera Access:** Ensure your webcam is available and permission is granted to Python/OpenCV.
    * **Lighting :** Good lighting improves recognition accuracy.
    * **First-time Setup:** `authorized_users.csv` and `access_log.csv` will be created automatically if they don't exist when the application runs for the first time. The `train/` directory will also be created.
    * **Dependencies:** If you encounter `ModuleNotFoundError`, ensure all libraries listed in the `Installation` section are correctly installed in your active Python environment.
7. Acknowledgments:
    * OpenCV for real-time video processing.
    * face_recognition for facial encoding and matching.
    * Special thanks to the contributors of community-built dlib wheels for Windows.
