# ✋ Gesture_PC_Control

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![YOLOv26n](https://img.shields.io/badge/YOLOv26n-green?style=flat-square)

Control PC mouse and system volume using hand gestures detected in real time by a YOLOv26n neural network via webcam — no extra hardware needed.

## 🛠️ Stack

- **YOLOv26n** (ultralytics) — gesture detection & model inference
- **OpenCV** (cv2) — webcam capture, frame display
- **PyTorch** — model backend
- **ctypes / win32api** — mouse events & volume control (Windows only)
- **NumPy** — frame processing
- **threading** — parallel webcam, display & controller loops

## 🚀 Quick Start

```bash
git clone https://github.com/Crossword88/Gesture_PC_Control
pip install -r pips.txt
python main.py
```
