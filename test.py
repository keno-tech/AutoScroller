import cv2
import mediapipe as mp
import pyautogui
import time

mp_face_detection = mp.solutions.face_detection

CAMERA = 0
threshold = 0.2
speed = 20
ESCAPE_BUTTON = 27

# Initialize face detection
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

# Load video using OpenCV
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    print(ret, frame)
exit()

while True:
    if ret == False:
        print(ret, frame)
    else:
        print(ret, frame)

    frame = cv2.flip(frame, 1)
    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, _ = frame.shape

    # Process the frame with Mediapipe face detection
    results = face_detection.process(rgb_frame)

    left_start_point = (int(w * threshold), h)
    left_end_point = (int(w * threshold), 0)
    right_start_point = (int(w * (1 - threshold)), h)
    right_end_point = (int(w * (1 - threshold)), 0)

    cv2.line(frame, left_start_point, left_end_point, (0, 255, 0), 2)
    cv2.line(frame, right_start_point, right_end_point, (0, 255, 0), 2)
    print("TEST")
    if results.detections:
        for detection in results.detections:
            # Extract the bounding box coordinates
            bbox = detection.location_data.relative_bounding_box

            # Convert relative coordinates to absolute coordinates
            xmin = int(bbox.xmin * w)
            ymin = int(bbox.ymin * h)
            bbox_width = int(bbox.width * w)
            bbox_height = int(bbox.height * h)
            xmax = xmin + bbox_width
            ymax = ymin + bbox_height

            # Draw bounding box rectangle and label on the frame
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(frame, 'Face', (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            if xmin < left_start_point[0] and xmax > left_end_point[0]:
                continue

            if xmin < left_start_point[0]:
                pyautogui.scroll(speed)
            elif xmax > left_end_point[0]:
                pyautogui.scroll(-speed)

    # Display the frame
    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(10) & 0xFF == ESCAPE_BUTTON or cv2.getWindowProperty('Face Detection', cv2.WND_PROP_VISIBLE) < 1:
        break

# Release the video capture and close all windows
