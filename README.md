
# Facial Recognition-Based Cabin Access Verification System

## Project Description

This project implements a real-time facial recognition system designed for access control. It utilizes a webcam feed to detect and recognize faces, comparing them against a database of authorized users. Based on the recognition, access is either granted or denied. The system also includes functionalities for registering new users and maintaining a log of all access attempts.

## Features

* **Real-time Face Detection & Recognition:** Identifies faces from a live webcam feed using `face_recognition` and OpenCV.
* **Access Validation:** Compares detected faces against a local database of authorized users (`authorized_users.csv`) to grant or deny access.
* **User Registration:** An admin can press 'A' during live access control (`access_control.py`) to register a new user by entering their name via the console and capturing their face from the webcam (webcam display is suppressed during capture).
* **Access Logging:** Records every access attempt (Name, Timestamp, Status: Granted/Denied) in `access_log.csv`.
* **Persistent Data Storage:** Uses CSV files (`authorized_users.csv`, `access_log.csv`) for storing user data and logs.
* **Visual Feedback:** Displays bounding boxes around faces and status messages (Granted/Denied/Unknown) on the webcam feed.
## Prerequisites

Before running the project, ensure you have the following installed:

* Python 3.7+
* A working webcam
* **C++ Build Tools (for Windows users):** The `dlib` and `face_recognition` libraries require C++ build tools for compilation during installation.
    * **Download manually:** You can find the necessary tools or pre-built wheels at [https://github.com/z-mahmud22/Dlib_Windows_Python3.x](https://github.com/z-mahmud22/Dlib_Windows_Python3.x). Follow the instructions on that page to install the appropriate tools for your Python version.
    * Alternatively, you can install the **Build Tools for Visual Studio** (e.g., from [visualstudio.microsoft.com/downloads/](https://visualstudio.microsoft.com/downloads/), select "Build Tools for Visual Studio" under "Tools for Visual Studio") and ensure "Desktop development with C++" workload is selected.

## Installation
1.  **Clone the repository** (if applicable, otherwise ensure all project files are in one directory):
    ```bash
    git clone https://github.com/TirumalaRaoBoddana/Facial_Recognition_Based_Cabin_Access_Verification_System
    cd facial_access_system
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install the required Python libraries:**

    ```bash
    pip install opencv-python face_recognition numpy==1.5 pandas
    ```

    * **Note for `face_recognition` / `dlib` installation:** If you encounter errors during the installation of `face_recognition` or `dlib` (especially on Windows), it's likely due to missing C++ build tools. Refer to the "Prerequisites" section above for instructions on installing them.
    * **⚠️ Important NumPy Version Warning ⚠️:** The project specifically requires `numpy==1.5`. Please be aware that this is a very old version of NumPy. Newer versions of `opencv-python` and `face_recognition` typically expect more recent NumPy versions. If you encounter installation errors or runtime issues related to NumPy compatibility, you might need to test with a slightly newer, yet compatible, NumPy version (e.g., `numpy<1.20` or `numpy<1.24` depending on the `face_recognition` and `opencv-python` versions that can be installed with it). However, for strict adherence to the `numpy==1.5` requirement, issues might arise.

    * `opencv-python`: For computer vision tasks.
    * `face_recognition`: For face detection and encoding.
    * `numpy==1.5`: **Specifically required version for NumPy.**
    * `pandas`: For data handling with CSV files.

## How to Run the Project

This project runs as a desktop application with a console interface for user registration.

1.  **Ensure you have at least one user registered.** If not, you can register a user directly from the `access_control.py` app after starting it (see step 3 below).

2.  **Open your terminal or command prompt** in the `facial_access_system/` directory.

3.  **Run the main access control script:**

    ```bash
    python access_control.py
    ```

4.  **Interaction:**
    * The webcam feed will appear in a new window titled "Facial Recognition Access Control".
    * If a registered face is detected, it will be labeled with the user's name and "Access Granted" will be displayed.
    * If an unknown face is detected, it will be labeled "Unknown" and "Access Denied" will be displayed.
    * **To register a new user:** Press the `'A'` key on your keyboard while the webcam window is active.
        * The webcam window will close temporarily.
        * You will be prompted in the **console** to enter the new user's name.
        * The camera will activate in the background (no separate window will appear for capture). Position your face clearly.
        * You will be prompted in the **console** to press `'A'` again to capture the image.
        * Once the face is captured and saved, the main access control window will reappear, and the system will reload the authorized users.
    * **To quit the application:** Press the `'Q'` key on your keyboard while the webcam window is active.

## Important Notes & Troubleshooting

* **Camera Access:** Ensure your webcam is properly connected and that your operating system has granted permission for Python/OpenCV to access it. If you face a "Cannot access the camera" error, check your system's privacy settings.
* **Face Detection:** For accurate recognition, ensure good lighting and clear visibility of the face.
* **Database Files:** `authorized_users.csv` and `access_log.csv` will be created automatically if they don't exist when the application runs for the first time. The `train/` directory will also be created.
* **Dependencies:** If you encounter `ModuleNotFoundError`, ensure all libraries listed in the `Installation` section are correctly installed in your active Python environment.
