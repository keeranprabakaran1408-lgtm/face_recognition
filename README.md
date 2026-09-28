# Facial Recognition Access Control (Raspberry Pi)

A facial recognition-based access control system built on a Raspberry Pi 4, using OpenCV for face detection and recognition, GPIO-controlled hardware output, and SQLite logging of every access attempt. Developed as a personal portfolio project.

## Overview

A webcam captures a live video feed. Detected faces are compared against a trained model of enrolled users. If the recognition confidence passes a threshold, access is "granted" (LED lights up, on-screen banner turns green); otherwise it's "denied" (LED off, banner turns red). Every attempt — granted or denied — is logged to a local database with a timestamp and confidence score.

## Features

- Real-time face detection using OpenCV Haar Cascades
- Face recognition using LBPH (Local Binary Pattern Histogram)
- Confidence-threshold-based access decision logic
- On-screen colour-coded status banner (green = granted, red = denied)
- GPIO-controlled LED reflecting the access decision
- SQLite logging of every access attempt (label, confidence, status, timestamp)

## Hardware

- Raspberry Pi 4 (4GB)
- USB webcam
- Breadboard, LED, resistor, jumper wires

## Software / Tech Stack

- Python 3
- OpenCV (`opencv-contrib-python`)
- NumPy
- `gpiozero`
- SQLite (`sqlite3`)

## Project Structure

```
pi_recognition_project/
├── camera_detect.py           # Main script: capture, detect, recognize, decide, log
├── train_recogniser.py        # Trains the LBPH recognizer from the dataset
├── haarcascade_frontalface_default.xml
├── trainer.yml                 # Saved trained model
├── access_log.db               # SQLite database of access attempts
└── dataset/
    └── keeran/                 # Captured training images
```

## Setup

1. Flash Raspberry Pi OS (64-bit) onto a microSD card and boot the Pi.
2. Install dependencies:
   ```
   pip install opencv-contrib-python numpy --break-system-packages
   ```
3. Connect a webcam and wire the LED circuit to the Pi's GPIO pins.

## Usage

1. **Capture a dataset** of your own face (run the capture stage in `camera_detect.py`).
2. **Train the recognizer**:
   ```
   python3 train_recogniser.py
   ```
3. **Run the access control system**:
   ```
   python3 camera_detect.py
   ```
4. Press `q` to quit.

## How It Works

1. **Detection** — Haar Cascade locates faces in each frame.
2. **Recognition** — LBPH compares the detected face against the trained model, returning an identity label and confidence score (lower = better match).
3. **Decision** — If confidence is below a set threshold, access is granted; otherwise denied.
4. **Output** — The decision drives an on-screen banner, a GPIO-controlled LED, and a database log entry.

## Limitations

- Recognizes only a small, pre-enrolled set of individuals (not general public identification).
- Vulnerable to spoofing (e.g. a photo held up to the camera), since it uses 2D recognition without liveness detection.
- Performance is affected by lighting and camera angle.
- Threshold was tuned against a single enrolled user.
- The GPIO LED does not reliably turn off on an "Access Denied" decision during testing; the decision logic itself was confirmed correct in isolation, but the on-device LED behaviour was not fully resolved.

## Future Work

- Add liveness detection to mitigate photo spoofing.
- Expand to multiple enrolled users.
- Add a servo-actuated physical lock in place of the LED simulation.

## Author

Keeran — Computer Science with AI, Brunel University London
