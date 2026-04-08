from ultralytics import YOLO
import cv2

# This will download a small 6MB model into your project folder
model = YOLO('yolov8n.pt') 

cap = cv2.VideoCapture(0)

print("Starting Webcam... Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if success:
        # AI runs here
        results = model(frame)
        
        # Visualize the boxes
        annotated_frame = results[0].plot()
        
        cv2.imshow("SecureEye Test", annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()