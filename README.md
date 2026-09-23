# 🛡️ VisionGuard AI

### AI-Powered Helmet Detection & Safety Monitoring System

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

## 🎯 Problem Statement

Helmet compliance is an important part of road and workplace safety.

Traditional monitoring systems often require continuous manual observation. VisionGuard AI aims to automate helmet monitoring using computer vision.

The system detects people from images or camera frames and analyzes the head region to determine whether a helmet is present.

---

## 💡 Solution

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

## 🏗️ System Architecture

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
