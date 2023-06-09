import cv2
import mediapipe as mp
import pyautogui

pyautogui.PAUSE = 0.01
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Make detection
        results = hands.process(image)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            index_tip_location = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP.value]

            cx, cy = int(index_tip_location.x * frame.shape[1]), int(index_tip_location.y * frame.shape[0])
            cv2.circle(frame, (cx, cy), 10, (121, 22, 76), -1)

            if index_tip_location.y > 0.70:
                pyautogui.scroll(-20)   
            elif index_tip_location.y < 0.30:
                pyautogui.scroll(80)

        cv2.imshow('Feed', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
