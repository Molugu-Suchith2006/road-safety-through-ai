# Real-Time Driver Drowsiness Detection (Active Development)

## Overview
This repository contains the core computer vision logic for an automated safety monitoring system designed to detect early signs of driver fatigue. The system actively processes live video feeds to map facial landmarks and calculate blink duration, triggering stage-based alerts when critical fatigue thresholds are breached.

## Current State: Algorithmic Core Complete
The project is currently in the active development phase. The core software architecture has been successfully implemented and tested:
* **Facial Landmark Mapping:** Utilizes MediaPipe to continuously track facial geometry in real-time.
* **Eye Aspect Ratio (EAR) Calculation:** The algorithm dynamically measures eye closure states.
* **Time-Threshold Logic:** Successfully detects prolonged eye closures (e.g., > 5 seconds) and outputs stage-based console warnings.

## Next Phase: Hardware Integration Roadmap
With the vision processing pipeline finalized in `rtrp.py`, the immediate next steps involve bridging the software-to-hardware gap:
1. **Microcontroller Integration:** Serial communication with an Arduino/ESP32.
2. **Physical Actuators:** Triggering physical audio-visual alerts (buzzers, LEDs) inside a vehicle environment upon reaching the 5-second fatigue threshold.

## Tech Stack
* Python 3.x
* OpenCV (Frame processing)
* MediaPipe (High-fidelity landmark tracking)
