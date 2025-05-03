import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time

# Initialize MediaPipe and OpenCV utilities
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)
cv2.namedWindow("Gesture Mouse", cv2.WINDOW_NORMAL)

# Parameters for controlling actions
last_click_time = 0
click_cooldown = 0.3
prev_x, prev_y = 0, 0
smooth_factor = 0.2
dead_zone = 5
last_zoom = None
zoom_sensitivity = 1
last_zoom_time = 0
zoom_delay = 0.1
scroll_center_y = 240
scroll_sensitivity = 20
scroll_last_time = 0
scroll_delay = 0.1
p_time = 0

def interpolate(val, src_range, dst_range):
    return np.interp(val, src_range, dst_range)

def debounce(last_time, cooldown):
    return (time.time() - last_time) > cooldown

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    h, w, _ = img.shape
    handedness_map = {}

    # Hand detection and landmark extraction
    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, (hand_landmark, hand_handedness) in enumerate(
            zip(results.multi_hand_landmarks, results.multi_handedness)
        ):
            label = hand_handedness.classification[0].label
            lmDict = {}
            for id, lm in enumerate(hand_landmark.landmark):
                lmDict[id] = (int(lm.x * w), int(lm.y * h))
            handedness_map[label] = lmDict
            mpDraw.draw_landmarks(img, hand_landmark, mpHands.HAND_CONNECTIONS)

    num_hands = len(handedness_map)

    # Mouse control when only the right hand is present
    if num_hands == 1 and 'Right' in handedness_map:
        lmDict_right = handedness_map['Right']

        # Smooth mouse movements
        if 8 in lmDict_right:
            x, y = lmDict_right[8]
            screen_x = interpolate(x, [0, w], [0, screen_w])
            screen_y = interpolate(y, [0, h], [0, screen_h])
            smooth_x = prev_x + (screen_x - prev_x) * smooth_factor
            smooth_y = prev_y + (screen_y - prev_y) * smooth_factor
            if abs(smooth_x - prev_x) > dead_zone or abs(smooth_y - prev_y) > dead_zone:
                pyautogui.moveTo(smooth_x, smooth_y)
                cv2.putText(img, f'Mouse Moving', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            prev_x, prev_y = smooth_x, smooth_y

        # Mouse click
        if 4 in lmDict_right and 8 in lmDict_right:
            x1, y1 = lmDict_right[4]
            x2, y2 = lmDict_right[8]
            click_distance = np.hypot(x2 - x1, y2 - y1)
            if click_distance < 30:
                if debounce(last_click_time, click_cooldown):
                    pyautogui.click()
                    last_click_time = time.time()
                    cv2.putText(img, 'Mouse Clicked!', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Zoom control with both hands
    if num_hands == 2:
        if 'Right' in handedness_map and 'Left' in handedness_map:
            lmDict_left = handedness_map['Left']
            lmDict_right = handedness_map['Right']

            if 8 in lmDict_left and 8 in lmDict_right:
                x1_left, y1_left = lmDict_left[8]
                x2_right, y2_right = lmDict_right[8]
                zoom_distance = np.hypot(x2_right - x1_left, y2_right - y1_left)

                current_time = time.time()
                min_length, max_length = 50, 300
                min_zoom, max_zoom = -20, 20
                zoom_value = np.interp(zoom_distance, [min_length, max_length], [min_zoom, max_zoom])

                if last_zoom is not None:
                    delta_zoom = (zoom_value - last_zoom) * zoom_sensitivity
                    delta_zoom = int(delta_zoom)
                    if abs(delta_zoom) > 0 and (current_time - last_zoom_time > zoom_delay):
                        if delta_zoom > 0:
                            pyautogui.hotkey('ctrl', '+')
                            cv2.putText(img, 'Zooming In', (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        elif delta_zoom < 0:
                            pyautogui.hotkey('ctrl', '-')
                            cv2.putText(img, 'Zooming Out', (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        last_zoom_time = current_time

                last_zoom = zoom_value

    # Scrolling when only the left hand is present
    if num_hands == 1 and 'Left' in handedness_map:
        lmDict_left = handedness_map['Left']

        if 8 in lmDict_left:
            y = lmDict_left[8][1]
            current_time = time.time()

            if current_time - scroll_last_time > scroll_delay:
                delta_scroll = (scroll_center_y - y) / scroll_sensitivity
                delta_scroll = int(delta_scroll)
                if delta_scroll != 0:
                    pyautogui.scroll(delta_scroll)
                    scroll_last_time = current_time
                    cv2.putText(img, f'Scrolling: {delta_scroll}', (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

    # Draw guide line and show FPS
    cv2.line(img, (0, scroll_center_y), (w, scroll_center_y), (0, 255, 0), 2)
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time
    cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    
    cv2.imshow("Gesture Mouse", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
