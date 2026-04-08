import cv2
from ultralytics import YOLO
import pandas as pd
from datetime import datetime

# Initialize
model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)
data_logs = [] # To store events

print("SecureEye PRO Active. Monitoring for Report...")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    results = model(frame)
    persons = [box for box in results[0].boxes if int(box.cls[0]) == 0]
    person_count = len(persons)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # LOGIC 1: Privacy Breach Logging
    if person_count > 1:
        frame = cv2.GaussianBlur(frame, (99, 99), 0)
        cv2.putText(frame, "PRIVACY BREACH", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        data_logs.append({"Time": timestamp, "Event": "Privacy Breach", "Details": f"{person_count} people detected"})

    # LOGIC 2: Posture Logging
    for box in persons:
        x1, y1, x2, y2 = box.xyxy[0]
        height = y2 - y1
        if height > 420:
            cv2.putText(frame, "SIT BACK!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 3)
            data_logs.append({"Time": timestamp, "Event": "Bad Posture", "Details": "Leaning too close"})

    cv2.imshow("SecureEye Professional", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- FINAL STEP: SAVE THE DATA ---
cap.release()
cv2.destroyAllWindows()

if data_logs:
    df = pd.DataFrame(data_logs)
    df.to_csv("session_report.csv", index=False)
    print("Session Ended. Data saved to session_report.csv")
else:
    print("Session Ended. No incidents recorded.")