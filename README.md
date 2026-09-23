# 🛡️ VisionGuard AI

## AI-Powered Helmet Detection & Safety Monitoring System

VisionGuard AI is an AI-powered computer vision system designed to detect people and identify whether they are wearing a helmet.

The project combines **YOLOv8, FastAPI, React, OpenCV, and a custom helmet detection model** to provide both image-based and real-time camera-based helmet detection.

---

## 🚀 Features

- 👤 Person Detection
- 🪖 Helmet Detection
- 🚫 Without-Helmet Detection
- 🎥 Real-Time Camera Detection
- 📷 Image-Based Detection
- 📊 Real-Time Detection Statistics
- 📈 Helmet Compliance Percentage
- 🎯 YOLOv8-based Computer Vision
- ⚡ FastAPI AI Backend
- 💻 React + Vite Web Dashboard
- 🧠 Custom Helmet Detection Model
- 🖥️ Browser Camera Support
- 🔍 Detection Confidence Scores
- 📱 Responsive Web Interface

---

# 🎯 Problem Statement

Helmet compliance is an important part of road and workplace safety.

Traditional monitoring systems often require continuous manual observation. VisionGuard AI aims to automate helmet monitoring using computer vision.

The system detects people from images or camera frames and analyzes the head region to determine whether a helmet is present.

---

# 💡 Solution

VisionGuard AI uses a two-stage detection pipeline:

1. Detect people using YOLOv8.
2. Extract the upper/head region of each detected person.
3. Run the custom helmet detection model.
4. Classify the result as:
   - `With Helmet`
   - `Without Helmet`
   - `Checking...`
5. Display detection results and compliance statistics.

---

# 🏗️ System Architecture

```text
                    VisionGuard AI
                          │
             ┌────────────┴────────────┐
             │                         │
       Image Detection           Live Camera
             │                         │
             └────────────┬────────────┘
                          │
                          ▼
                   React Frontend
                          │
                          ▼
                    FastAPI Backend
                          │
                          ▼
                   YOLOv8 Person
                     Detection
                          │
                          ▼
                  Head Region Crop
                          │
                          ▼
                Helmet Detection Model
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
        With Helmet              Without Helmet
             │                         │
             ▼                         ▼
           SAFE                       ALERT
```

---

# 🧠 Detection Pipeline

```text
Input Image / Camera Frame
            │
            ▼
     Person Detection
        (YOLOv8)
            │
            ▼
     Person Bounding Box
            │
            ▼
      Head Region Crop
            │
            ▼
   Helmet Detection Model
            │
       ┌────┴────┐
       │         │
       ▼         ▼
 With Helmet  Without Helmet
       │         │
       ▼         ▼
     SAFE       ALERT
```

---

# 🛠️ Technology Stack

## AI / Computer Vision

- Python
- YOLOv8
- Ultralytics
- OpenCV
- NumPy
- PyTorch
- Custom Helmet Detection Model

## Backend

- FastAPI
- Uvicorn
- Python
- REST API

## Frontend

- React
- Vite
- JavaScript
- HTML
- CSS
- Browser MediaDevices API

## Development Tools

- Git
- GitHub
- VS Code

---

# 📁 Project Structure

```text
VisionGuard-AI/
│
├── backend/
│   └── main.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── models/
│   └── helmet.pt
│
├── src/
│   └── main.py
│
├── yolov8n.pt
├── capture_helmet.py
├── requirements.txt
├── run.sh
├── README.md
└── .gitignore
```

---

# 🚀 Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/Prince736802/VisionGuard-AI.git
```

Go inside the project:

```bash
cd VisionGuard-AI
```

---

# 🐍 Backend Setup

## 2. Create Python Virtual Environment

```bash
python3 -m venv .venv
```

Activate the virtual environment.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

---

## 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

The backend uses:

- FastAPI
- Uvicorn
- OpenCV
- NumPy
- PyTorch
- Ultralytics YOLO

---

# ⚡ Start Backend

After activating the virtual environment, make sure you are inside the **main VisionGuard-AI folder**.

Run:

```bash
uvicorn backend.main:app --reload
```

If everything is working correctly, you should see:

```text
Uvicorn running on http://127.0.0.1:8000
```

### Backend URL

```text
http://127.0.0.1:8000
```

### API Documentation

FastAPI provides interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Health Check

```text
http://127.0.0.1:8000/health
```

> **Important:** Keep this terminal running while using the frontend.

---

# 💻 Frontend Setup

Open a **NEW terminal window**.

Do not stop the backend terminal.

Go to the frontend folder:

```bash
cd ~/VisionGuard-AI/frontend
```

If your project is located somewhere else, use the appropriate path to the `frontend` folder.

---

## 4. Install Frontend Dependencies

Run:

```bash
npm install
```

---

# ▶️ Start Frontend

Run:

```bash
npm run dev
```

You should see something similar to:

```text
VITE ready

Local: http://localhost:5173/
```

Open this URL in your browser:

```text
http://localhost:5173
```

---

# 🎥 How to Start the Complete Application

VisionGuard AI requires **two terminals**.

## Terminal 1 — Backend

Open Terminal 1:

```bash
cd ~/VisionGuard-AI
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Start the backend:

```bash
uvicorn backend.main:app --reload
```

Keep this terminal running.

---

## Terminal 2 — Frontend

Open a **new terminal**.

Run:

```bash
cd ~/VisionGuard-AI/frontend
```

Start the frontend:

```bash
npm run dev
```

Then open:

```text
http://localhost:5173
```

---

# 🔄 Complete Application Flow

```text
Terminal 1
    │
    ▼
FastAPI Backend
http://127.0.0.1:8000
    │
    │
    ▼
Terminal 2
    │
    ▼
React Frontend
http://localhost:5173
    │
    ▼
Browser
    │
    ▼
Camera / Image
    │
    ▼
AI Detection
    │
    ▼
Helmet Result
```

---

# 🎥 Live Camera Detection

After starting both backend and frontend:

### Step 1

Open:

```text
http://localhost:5173
```

### Step 2

Open the **Live Camera Detection** section.

### Step 3

Click:

```text
Start Live Detection
```

### Step 4

When the browser asks for camera permission, click:

```text
Allow
```

### Step 5

The system will process camera frames and detect:

- 👤 Person
- 🪖 With Helmet
- ⚠️ Without Helmet

The dashboard will also display detection statistics.

---

# 📷 Image Detection

VisionGuard AI also supports image-based helmet detection.

### Workflow

```text
Upload Image
     │
     ▼
React Frontend
     │
     ▼
FastAPI Backend
     │
     ▼
YOLOv8 Person Detection
     │
     ▼
Head Region Extraction
     │
     ▼
Helmet Detection
     │
     ▼
Annotated Result
     │
     ▼
Statistics
```

---

# 📊 Detection Statistics

The dashboard provides:

- Total Persons
- With Helmet
- Without Helmet
- Checking
- Helmet Compliance Percentage

Example:

```text
Total Persons      : 10
With Helmet        : 8
Without Helmet     : 2
Compliance         : 80%
```

The compliance percentage is calculated as:

```text
Compliance =
(With Helmet / Total Persons) × 100
```

---

# 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Backend health check |
| GET | `/model-info` | Model information |
| POST | `/detect` | Detect helmets from uploaded image |
| POST | `/live-detect` | Process a camera frame |

---

# 🧪 Testing Backend

Start the backend:

```bash
uvicorn backend.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

You can test the available API endpoints directly from Swagger UI.

---

# 🧪 Testing Frontend

Open another terminal:

```bash
cd ~/VisionGuard-AI/frontend
```

Run:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

---

# 🏗️ Production Build

To create a production build of the React frontend:

```bash
cd ~/VisionGuard-AI/frontend
```

Then:

```bash
npm run build
```

The production files will be generated inside:

```text
frontend/dist/
```

---

# 🪖 Helmet Detection Model

The custom helmet model contains two classes:

```text
Class 0 → With Helmet
Class 1 → Without Helmet
```

The system first detects a person and then analyzes the upper/head region using the custom helmet detection model.

---

# 🎯 Detection Logic

### Stage 1 — Person Detection

YOLOv8 detects people in the image or camera frame.

### Stage 2 — Head Region Extraction

The upper region of the detected person is extracted.

### Stage 3 — Helmet Detection

The custom helmet model analyzes the extracted region.

### Stage 4 — Result

The system returns:

```text
With Helmet
Without Helmet
Checking...
```

---

# 🔬 Original OpenCV Detection Mode

The project also contains the standalone OpenCV implementation:

```text
src/main.py
```

This version provides a local camera-based detection workflow using OpenCV and YOLO tracking functionality.

Run it from the project root:

```bash
python src/main.py
```

> The web dashboard and the standalone OpenCV implementation are separate ways of running the VisionGuard AI detection system.

---

# 🔐 Privacy & Safety

VisionGuard AI is designed to process images and camera frames locally during development.

The local development setup does not require uploading camera footage to an external cloud service.

When deploying computer-vision systems in public or workplace environments, applicable privacy, consent, and surveillance requirements should be considered.

---

# 🔮 Future Improvements

- 🚦 Automatic violation alerts
- 📸 Automatic violation screenshots
- 📝 Persistent violation logs
- 👥 Advanced multi-person tracking
- 📊 Historical analytics dashboard
- 🔔 Email/SMS notifications
- ☁️ Cloud deployment
- 🗄️ Database integration
- 📱 Mobile application
- 🚗 Vehicle and traffic-rule detection
- 🎯 Improved helmet detection accuracy
- ⚡ GPU acceleration

---

# 📈 Project Highlights

VisionGuard AI demonstrates practical implementation of:

- Computer Vision
- Object Detection
- Deep Learning
- YOLOv8
- Custom ML Models
- REST APIs
- FastAPI
- React
- Real-Time Video Processing
- Browser Camera Integration
- Full-Stack AI Application Development

---

# 👨‍💻 Developer

**Prince Kumar**

B.Tech — Artificial Intelligence & Machine Learning

GitHub:

https://github.com/Prince736802/VisionGuard-AI

---

# ⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is intended for educational, research, and demonstration purposes.
