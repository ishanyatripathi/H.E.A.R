🎧 H.E.A.R Hand Enabled Audio Regulator
=========================================
A Python-based, gesture-controlled volume adjustment system

H.E.A.R lets you control your system’s volume effortlessly using just your hands.
With OpenCV, MediaPipe, and Pycaw, it detects your hand in real-time, interprets gestures,
and adjusts the audio output instantly — no keyboard, mouse, or physical volume knob required.

🚀 Features
-----------
- 📷 Real-time Hand Tracking: Tracks hand landmarks with high accuracy using MediaPipe.
- ✋ Gesture-based Volume Control: Adjust volume by simply moving your fingers closer or farther apart.
- 🎨 Visual Feedback: Displays tracking visuals and volume indicators in the OpenCV window.
- ⚡ Low Latency: Smooth and responsive volume changes.

📦 Requirements
---------------
Python 3.x

Install dependencies:
    pip install opencv-python mediapipe numpy pycaw comtypes

🛠 Installation
---------------
1. Clone the Repository
    git clone https://github.com/ishanyatripathi/HEAR.git

2. Navigate to Project Directory
    cd HEAR

3. Install Dependencies (if not already installed)
    pip install -r requirements.txt

▶ Usage
-------
Run the script:
    python hear.py

- Move your thumb and index finger closer → Volume decreases 🔉
- Move them farther apart → Volume increases 🔊
- Press 'q' to quit.


📂 Project Structure
--------------------
HEAR/

│── main.py              
│── LICENSE     
│── README.md            

🧠 How It Works
---------------
1. Capture Frame: OpenCV reads video feed from your webcam.
2. Detect Hand Landmarks: MediaPipe identifies and tracks key points on your hand.
3. Measure Finger Distance: Calculates the distance between thumb and index finger.
4. Map Distance to Volume: Uses Pycaw to adjust system volume accordingly.
5. Display Feedback: Shows hand tracking and volume level in real-time.

📜 License
----------
This project is licensed under the MIT License – feel free to use and modify it.

💡 Future Improvements
-----------------------
- Multi-hand volume control for different audio devices.
- Gesture-based mute/unmute.
- Integration with media player controls (play/pause/skip).
