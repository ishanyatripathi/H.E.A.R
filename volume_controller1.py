import cv2
import mediapipe as mp
from math import hypot
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volMin, volMax = volume.GetVolumeRange()[:2]

while True:
    success, img = cap.read()
    if not success:
        break  

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmDict = {}  

   
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmark.landmark):
                h, w, _ = img.shape
                lmDict[id] = (int(lm.x * w), int(lm.y * h))
            mpDraw.draw_landmarks(img, hand_landmark, mpHands.HAND_CONNECTIONS)

    
    if 4 in lmDict and 8 in lmDict:
        x1, y1 = lmDict[4]  
        x2, y2 = lmDict[8]  

        
        cv2.circle(img, (x1, y1), 5, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

       
        length = hypot(x2 - x1, y2 - y1)

        
        vol = np.interp(length, [20, 200], [volMin, volMax])
        volume.SetMasterVolumeLevel(vol, None)

        
        vol_bar = np.interp(length, [20, 200], [400, 150])
        cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 2)

        
        vol_percentage = int(np.interp(length, [20, 200], [0, 100]))
        cv2.putText(img, f"{vol_percentage}%", (40, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    
    cv2.imshow('Hand Gesture Volume Control', img)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
