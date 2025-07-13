import cv2
import os
import mediapipe as mp

# Ensure the known_faces directory exists
if not os.path.exists("known_faces"):
    os.makedirs("known_faces")

# Initialize Mediapipe face detector
mp_face = mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

# Start webcam
cam = cv2.VideoCapture(0)
print("📸 Look at the camera. Press SPACE to capture your face.")

while True:
    ret, frame = cam.read()
    if not ret:
        continue

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_face.process(rgb)

    if results.detections:
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape
            x, y, bw, bh = int(bbox.xmin * w), int(bbox.ymin * h), int(bbox.width * w), int(bbox.height * h)
            cv2.rectangle(frame, (x, y), (x + bw, y + bh), (0, 255, 0), 2)

    cv2.imshow("Register Face", frame)
    key = cv2.waitKey(1)

    if key == 32 and results.detections:  # SPACE key
        # Save the face crop instead of full frame
        face_crop = frame[y:y+bh, x:x+bw]
        face_gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
        face_resized = cv2.resize(face_gray, (100, 100))
        face_path = os.path.join("known_faces", "authorized.jpg")
        cv2.imwrite(face_path, face_resized)
        print("✅ Face saved as 'authorized.jpg'")
        break
    elif key == 27:  # ESC key
        break

cam.release()
cv2.destroyAllWindows()
