# 🛡️ VisionGuard AI

A real-time **Edge AI and Computer Vision** system for person tracking and helmet safety monitoring using **Python, OpenCV, and YOLOv8**.

VisionGuard AI detects people through a webcam, assigns unique tracking IDs, checks helmet usage, and generates alerts when a person is detected without a helmet.

---

## 🚀 Features

- 🎥 Real-time webcam detection
- 👤 Person detection
- 🔢 Person counting
- 🎯 Person tracking with unique IDs
- 🪖 Helmet detection
- 🚨 Without-helmet alert system
- 🧠 Head/upper-body ROI based helmet detection
- 📊 Temporal smoothing for more stable predictions
- 📸 Automatic screenshot capture for violations
- 📝 CSV-based violation logging
- ⚡ Edge AI ready architecture
- 📈 Real-time FPS monitoring
- 🎚️ Confidence-based detection

---

## 🧠 System Architecture

```text
                    Camera
                       │
                       ▼
              YOLOv8 Person Detection
                       │
                       ▼
                 ByteTrack
                       │
                       ▼
                Person Tracking
                (Unique Person ID)
                       │
                       ▼
                 Head / ROI Crop
                       │
                       ▼
              Helmet Detection Model
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
        With Helmet         Without Helmet
             │                   │
             ▼                   ▼
          SAFE              🚨 ALERT
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
              Screenshot                 CSV Log