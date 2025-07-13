# 🔐 Intruder Detection System using OpenCV & MediaPipe

This project is a **real-time intruder detection system** using your webcam. It compares live faces with a previously registered authorized face. If the person in front of the camera doesn't match, it flags them as an intruder and saves a snapshot.

---

## 📸 Features

- ✅ Register one authorized face via webcam.
- 🧠 Detect faces in real-time using **MediaPipe**.
- 🔍 Compare live face with the authorized face using grayscale difference.
- 🚨 Save intruder snapshots with timestamps in a log folder.
- 💻 Lightweight — no training or model loading required.

---

## 🗂️ Project Structure

IntruderDetection/
├── known_faces/
│ └── authorized.jpg # Authorized face image (captured once)
├── intruder_logs/
│ └── intruder_*.jpg # Intruder snapshots with timestamps
├── register_face.py # Face capture script
└── intruder_detector.py # Real-time face detection & comparison

---

## 🛠️ Requirements

Install the required libraries using pip:


pip install opencv-python mediapipe numpy

🚀 How to Run
Step 1: Register Authorized Face
Run the following script to capture your face from webcam:
python register_face.py
Look directly at the camera.
Press SPACE to capture and save your face.
The image will be saved as known_faces/authorized.jpg
Step 2: Start Detection
Now run the intruder detection script:
python intruder_detector.py
If your face matches the registered one ➜ ✅ Authorized (Green box)
If not ➜ 🚨 Intruder (Red box), and a snapshot is saved.
Press ESC to exit the detection window.

⚙️ How It Works
1)MediaPipe is used to detect faces in real-time.
2)The registered authorized face and the live face are:
3)Converted to grayscale
4)Resized to 100x100
5)Compared using pixel-wise difference (cv2.absdiff)
6)If the difference is more than a threshold, the face is labeled as an intruder.

📌 Notes

1) Make sure lighting and camera position remain consistent.
2)Works best when only one face is present in front of the camera.
3)Only one authorized person can be registered at a time.

👩‍💻 Author
Manasi Bhangale
Student BTech Computer Engineering
Dr. Babasaheb Ambedkar Technological University

