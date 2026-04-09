#  YOLO-Based People Counting System

##  Overview

This project is a **real-time people counting system** that uses a laptop webcam and a pretrained YOLO model.
It detects people in the camera view, draws bounding boxes, and displays the current count on the screen in real time.

 The goal is to help colleges monitor classroom/lab occupancy using only a regular laptop.

---

##  What it does

* Opens your laptop webcam and reads live video frames
* Runs a YOLO model on each frame to detect **person** objects
* Draws bounding boxes and labels around detected people
* Displays real-time count (e.g., **Count: 7**)
* (Optional) Logs timestamp and count to a CSV file

 You can place the laptop at a classroom or lab entrance and use it as a **low-cost smart counting system**.

---

##  Tech Stack

* **Language:** Python
* **Model:** YOLO (Ultralytics – pretrained)
* **Computer Vision:** OpenCV
* **Environment:** Local (Laptop-based system)
* **Data Logging:** CSV (optional)

---

##  Project Structure

```
.
├── main.py              # Main script (webcam + YOLO + counting)
├── requirements.txt     # Dependencies
├── models/              # YOLO weights (optional)
├── utils/               # Helper functions (optional)
└── logs/
    └── counts.csv       # Logged data (optional)
```

---

##  How to Run

###  Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

###  Create virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

###  Install dependencies

```bash
pip install -r requirements.txt
```

###  Run the application

```bash
python main.py
```

 A webcam window will open showing:

* Bounding boxes around detected people
* Live people count on screen

 Press **q** to exit

---

##  How it works

1. Capture video using OpenCV
2. Process each frame using YOLO
3. Filter detections for **person class**
4. Draw bounding boxes
5. Count detected people
6. Display results in real time
7. (Optional) Save data to CSV

---

##  Use Cases

* Monitor classroom or lab occupancy
* Analyze peak usage times
* Build a real-world AI + Computer Vision project

---

##  Future Improvements

* Direction-based counting (entry/exit tracking)
* Dashboard for visualizing data
* Support for recorded video input
* Cloud deployment and remote monitoring

---

##  Author

Lavanya Surianarayanan

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!
