# 🛡️ VisionGuard AI

### Real-Time Bike Helmet Violation Detection System

VisionGuard AI is a real-time computer vision system that detects people and identifies whether they are wearing a helmet or not.

The system uses YOLO-based object detection, person tracking, multi-frame prediction stabilization, and automatic violation logging to detect helmet violations through a live camera feed.

---

## 🚀 Features

- 👤 Real-time person detection
- 🪖 Helmet detection
- 🚫 Without-helmet detection
- 🎯 Person tracking using ByteTrack
- 🧠 Multi-frame prediction stabilization
- 🚨 Automatic no-helmet alert
- 📸 Automatic violation screenshot
- 📝 Violation logging
- 🎥 Real-time webcam detection
- ⚡ Lightweight YOLO models
- ▶️ One-command project execution using `run.sh`

---

## 🎯 Problem Statement

Riding a motorcycle without a helmet is a major road-safety violation.

Traditional helmet monitoring requires manual observation or expensive surveillance systems.

VisionGuard AI aims to automate this process using computer vision by detecting people in a camera feed and determining whether they are wearing helmets.

---

## 💡 How It Works

The system follows this pipeline:

```text
Camera Feed
     │
     ▼
Person Detection
     │
     ▼
Person Tracking
     │
     ▼
Head Region Extraction
     │
     ▼
Helmet Detection
     │
     ▼
Multi-Frame Stabilization
     │
     ├───────────────┐
     ▼               ▼
With Helmet      Without Helmet
     │               │
     ▼               ▼
   SAFE          ALERT
                     │
              ┌──────┴──────┐
              ▼             ▼
         Screenshot       Log