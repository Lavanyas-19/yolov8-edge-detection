import customtkinter as ctk
from tkinter import messagebox
import cv2
from ultralytics import YOLO
import pyttsx3
import threading
import time
import os
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import matplotlib.pyplot as plt

# Set the appearance and theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SecureEyeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SecureEye AI - Professional")
        self.geometry("400x550") # Slightly taller for extra button

        # Initialize State Variables
        self.last_speech_time = 0 
        self.last_save_time = 0
        self.data_logs = []

        # Create necessary folders
        for folder in ["incidents"]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        # UI Elements
        self.label = ctk.CTkLabel(self, text="SecureEye AI", font=("Roboto", 28, "bold"))
        self.label.pack(pady=30)

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Enter Your Name", width=250)
        self.name_entry.pack(pady=10)

        self.dept_options = ["IT Department", "Human Resources", "Finance", "Legal", "Operations"]
        self.dept_menu = ctk.CTkOptionMenu(self, values=self.dept_options, width=250)
        self.dept_menu.pack(pady=20)
        self.dept_menu.set("IT Department")

        self.start_btn = ctk.CTkButton(self, text="Start Secure Session", 
                                       command=self.start_session,
                                       height=40, font=("Arial", 14, "bold"))
        self.start_btn.pack(pady=10)

        # NEW: Dashboard Button
        self.dash_btn = ctk.CTkButton(self, text="View Analytics Dashboard", 
                                       command=self.show_dashboard,
                                       fg_color="transparent", border_width=2,
                                       height=40, font=("Arial", 14))
        self.dash_btn.pack(pady=10)

    # --- ENHANCEMENT 3: EMAIL ALERTS ---
    def send_email_alert(self, image_path):
        # CONFIGURATION - Replace with your details
        SENDER_EMAIL = "laavsuri@gmail.com" 
        RECEIVER_EMAIL = "laavss19@gmail.com" 
        APP_PASSWORD = "tisl vzzx mrsw vigc" 

        msg = EmailMessage()
        msg['Subject'] = f"🚨 SECURE-EYE ALERT: Privacy Breach!"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg.set_content(f"Unauthorized person detected near {self.user_name}.\nEvidence snapshot is attached.")

        try:
            with open(image_path, 'rb') as f:
                file_data = f.read()
                msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename=os.path.basename(image_path))

            def dispatch():
                try:
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(SENDER_EMAIL, APP_PASSWORD)
                        smtp.send_message(msg)
                except: pass # Silent fail if no internet

            threading.Thread(target=dispatch, daemon=True).start()
        except: pass

    # --- ENHANCEMENT 4: VISUAL DASHBOARD ---
    def show_dashboard(self):
        if not self.data_logs:
            messagebox.showwarning("No Data", "Please complete a session first to generate analytics.")
            return
        
        df = pd.DataFrame(self.data_logs)
        event_counts = df['Event'].value_counts()

        plt.figure(figsize=(8, 5))
        plt.style.use('dark_background')
        
        # Plotting
        event_counts.plot(kind='pie', autopct='%1.1f%%', colors=['#ff4d4d', '#33adff'])
        plt.title(f"Security Profile: {self.user_name}")
        plt.ylabel('')
        plt.tight_layout()
        plt.show()

    def speak(self, text):
        current_time = time.time()
        if current_time - self.last_speech_time > 5: 
            self.last_speech_time = current_time
            def run_speech():
                local_engine = pyttsx3.init()
                local_engine.setProperty('rate', 155) 
                local_engine.say(text)
                local_engine.runAndWait()
                local_engine.stop()
            threading.Thread(target=run_speech, daemon=True).start()

    def generate_final_report(self):
        if not self.data_logs: return None
        
        breaches = len([log for log in self.data_logs if log['Event'] == "Privacy Breach"])
        posture_issues = len([log for log in self.data_logs if log['Event'] == "Bad Posture"])
        safety_score = max(0, 100 - (breaches * 15) - (posture_issues * 5))

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(200, 15, txt="SECURE EYE: EXECUTIVE AUDIT REPORT", ln=True, align='C')
        pdf.ln(5)

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="1. REAL-TIME DATA HANDLING SUMMARY", ln=True)
        pdf.set_font("Arial", '', 10)
        summary = (f"The session for {self.user_name} utilized edge-processing to monitor workspace privacy. "
                   "Data was analyzed locally using YOLOv8 architectures. Security incidents were "
                   "forwarded via SMTP protocol for remote notification.")
        pdf.multi_cell(0, 5, summary)
        pdf.ln(5)

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=f"2. COMPLIANCE SCORE: {safety_score}/100", ln=True)
        pdf.ln(10)

        pdf.set_font("Arial", 'B', 10)
        pdf.cell(40, 10, "Timestamp", 1)
        pdf.cell(50, 10, "Event Category", 1)
        pdf.cell(100, 10, "System Action Taken", 1)
        pdf.ln()

        pdf.set_font("Arial", '', 9)
        for log in self.data_logs:
            pdf.cell(40, 10, log['Time'], 1)
            pdf.cell(50, 10, log['Event'], 1)
            pdf.cell(100, 10, log['Details'], 1)
            pdf.ln()

        report_filename = f"Executive_Report_{self.user_name}.pdf"
        pdf.output(report_filename)
        return report_filename

    def start_session(self):
        self.user_name = self.name_entry.get()
        self.user_dept = self.dept_menu.get()

        if self.user_name:
            messagebox.showinfo("Session Initialized", f"Welcome {self.user_name}!\nFull Security Suite Active.")
            self.withdraw()
            self.run_ai_engine()
        else:
            messagebox.showerror("Error", "Please enter your name!")

    def run_ai_engine(self):
        model = YOLO('yolov8n.pt')
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success: break

            results = model(frame, conf=0.5)
            bodies = [box for box in results[0].boxes if int(box.cls[0]) == 0]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            ts = datetime.now().strftime("%H:%M:%S")

            if len(bodies) > 1 or len(faces) > 1:
                current_time = time.time()
                if current_time - self.last_save_time > 30: # 30s Cooldown for Email
                    img_name = f"incidents/breach_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    cv2.imwrite(img_name, frame)
                    self.last_save_time = current_time
                    self.send_email_alert(img_name) # Send Alert
                    self.data_logs.append({"Time": ts, "Event": "Privacy Breach", "Details": "Email Sent + Snapshot"})

                frame = cv2.GaussianBlur(frame, (99, 99), 0)
                cv2.putText(frame, "PRIVACY SHIELD ACTIVE", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                self.speak("Unidentified person detected. Sending alert.")
            
            elif len(bodies) == 1:
                for box in bodies:
                    x1, y1, x2, y2 = box.xyxy[0]
                    if (y2 - y1) > 450:
                        cv2.putText(frame, "POSTURE ALERT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 3)
                        self.speak("Please sit back.")
                        self.data_logs.append({"Time": ts, "Event": "Bad Posture", "Details": "Ergonomic Warning"})

            cv2.rectangle(frame, (0, 0), (640, 40), (40, 40, 40), -1)
            cv2.putText(frame, f"SECURE EYE PRO | {self.user_name.upper()}", (15, 25), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow("SecureEye AI Console", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        cap.release()
        cv2.destroyAllWindows()
        
        report = self.generate_final_report()
        if report:
            messagebox.showinfo("Session Closed", f"Report generated: {report}")
            os.startfile(report) 
        
        self.deiconify()

if __name__ == "__main__":
    app = SecureEyeApp()
    app.mainloop()