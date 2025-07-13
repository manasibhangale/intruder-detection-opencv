import cv2
import os
import datetime
import numpy as np
import mediapipe as mp

# Load authorized image
authorized_img = cv2.imread("known_faces/authorized.jpg")
if authorized_img is None:
    print("❌ authorized.jpg not found.")
    exit()

# Convert authorized image to grayscale and resize
authorized_gray = cv2.cvtColor(authorized_img, cv2.COLOR_BGR2GRAY)
authorized_gray = cv2.resize(authorized_gray, (100, 100))

# Setup
if not os.path.exists("intruder_logs"):
    os.makedirs("intruder_logs")

mp_face = mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)
print("🔍 Intruder detection started... Press ESC to quit.")

detected_intruder = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_face.process(rgb)

    if results.detections:
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape
            x, y, bw, bh = int(bbox.xmin * w), int(bbox.ymin * h), int(bbox.width * w), int(bbox.height * h)
            face_crop = frame[y:y+bh, x:x+bw]

            if face_crop.size == 0:
                continue

            try:
                gray_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
                gray_crop = cv2.resize(gray_crop, (100, 100))
                diff = np.mean(cv2.absdiff(authorized_gray, gray_crop))

                if diff < 30:
                    label = "Authorized"
                    color = (0, 255, 0)
                    detected_intruder = False
                else:
                    label = "Intruder"
                    color = (0, 0, 255)
                    if not detected_intruder:
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        filename = f"intruder_logs/intruder_{timestamp}.jpg"
                        cv2.imwrite(filename, frame)
                        print(f"🚨 Intruder detected at {timestamp}")
                        detected_intruder = True

                cv2.rectangle(frame, (x, y), (x + bw, y + bh), color, 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            except Exception as e:
                print("⚠️ Face processing error:", e)

    cv2.imshow("Intruder Detection", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
