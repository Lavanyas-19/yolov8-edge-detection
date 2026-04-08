import cv2
from ultralytics import YOLO

# Load the model
model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)

print("SecureEye Logic Active... Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # Run YOLO detection
    results = model(frame)
    
    # Extract only 'person' detections (Class 0 in YOLO)
    persons = [box for box in results[0].boxes if int(box.cls[0]) == 0]
    person_count = len(persons)

    # --- LOGIC 1: PRIVACY SHIELD ---
    # If more than 1 person is detected, blur the screen to protect data
    if person_count > 1:
        frame = cv2.GaussianBlur(frame, (99, 99), 0)
        cv2.putText(frame, "PRIVACY BREACH: MULTIPLE PEOPLE", (50, 200), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # --- LOGIC 2: ERGONOMIC COACH ---
    for box in persons:
        # Get coordinates: x1, y1 (top left), x2, y2 (bottom right)
        x1, y1, x2, y2 = box.xyxy[0]
        
        # Calculate Height of the bounding box
        height = y2 - y1
        
        # If the box is too tall, it means you are leaning too close to the webcam
        if height > 420: # You can adjust this number
            cv2.putText(frame, "SIT BACK! TOO CLOSE!", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 3)
        
        # Draw a clean green box around the user (if not blurred)
        if person_count == 1:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    # Display the result
    cv2.imshow("SecureEye System", frame)

    # Use 'q' to quit instead of Ctrl+C for a clean exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()