import cv2
import mediapipe as mp
import pyautogui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QPushButton, QComboBox
import sys

pyautogui.PAUSE = 0.01

threshold = 0.2
speed = 20

valid_cams = []

MIN_THRESHOLD_VALUE = 0
MAX_THRESHOLD_VALUE = 70
MIN_SPEED_VALUE = 1
MAX_SPEED_VALUE = 100
DEFAULT_SPEED_VALUE = 20
DEFAULT_THRESHOLD_VALUE = int(threshold * 100)
DEFAULT_TICK_VALUE = 5
CAMERA = 0

ESCAPE_BUTTON = 27

def detect_cameras():
    global valid_cams
    # detect all connected webcams
    for i in range(5):
        cap = cv2.VideoCapture(i)
        try:
            if cap is not None and cap.isOpened():
                valid_cams.append(i)
                print('Found video source:', i)
        except Exception as e:
            print(e)

    return valid_cams

valid_cams = detect_cameras()
if not valid_cams:
    print("No valid cameras")


def main():
    mp_face_detection = mp.solutions.face_detection

    # Initialize face detection
    face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

    # Load video using OpenCV
    video = cv2.VideoCapture(CAMERA)

    while True:
        ret, frame = video.read()

        if not ret:
            break
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

        if results.detections:
            for detection in results.detections:
                # Extract the bounding box coordinates
                bbox = detection.location_data.relative_bounding_box
                h, w, _ = frame.shape

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

                left_start_point, left_end_point, = int(w * threshold), int(w * (1 - threshold))

                if left_start_point > xmin and left_end_point < xmax:
                    continue

                if xmin < left_start_point:
                    pyautogui.scroll(speed)
                elif xmax > left_end_point:
                    pyautogui.scroll(-speed)

        # Display the frame
        cv2.imshow('Face Detection', frame)
        

        if cv2.waitKey(10) & 0xFF == ESCAPE_BUTTON or cv2.getWindowProperty('Face Detection', cv2.WND_PROP_VISIBLE) < 1:
            break

    # Release the video capture and close all windows
    video.release()
    cv2.destroyAllWindows()

def update_threshold(value):
    global threshold
    threshold = value / 100.0
    print(f"Updated threshold to {value}")


def update_speed(value):
    global speed
    speed = value
    print(f"Updated speed to {value}")


class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("AutoScroller Configuration")
        self.setFixedSize(640, 480)
        self.set_dark_mode()

        layout = QVBoxLayout()

        # App Name
        name_label = QLabel("AutoScroller V1.0")
        name_label.setFont(QFont("Arial", 22, QFont.Bold))
        layout.addWidget(name_label)

        # Camera Selection
        camera_label = QLabel("Available Cameras")
        camera_label.setFont(QFont("Arial", 12))
        layout.addWidget(camera_label)

        self.camera_dropdown = QComboBox()
        self.camera_dropdown.addItems([str(cam) for cam in valid_cams])
        self.camera_dropdown.currentIndexChanged.connect(self.update_camera)
        layout.addWidget(self.camera_dropdown)

        # Speed
        speed_label = QLabel("Scroll Speed")
        speed_label.setFont(QFont("Arial", 12))
        layout.addWidget(speed_label)

        # Create speed slider
        speed_slider = QSlider(Qt.Horizontal)
        speed_slider.setMinimum(MIN_SPEED_VALUE)
        speed_slider.setMaximum(MAX_SPEED_VALUE)
        speed_slider.setValue(DEFAULT_SPEED_VALUE)  # Set initial value
        speed_slider.setTickPosition(QSlider.TicksBelow)
        speed_slider.setTickInterval(DEFAULT_TICK_VALUE)
        speed_slider.valueChanged.connect(update_speed)
        layout.addWidget(speed_slider)

        # Create threshold label
        threshold_label = QLabel("Threshold")
        threshold_label.setFont(QFont("Arial", 12))
        layout.addWidget(threshold_label)

        # Create threshold slider
        threshold_slider = QSlider(Qt.Horizontal)
        threshold_slider.setMinimum(MIN_THRESHOLD_VALUE)
        threshold_slider.setMaximum(MAX_THRESHOLD_VALUE)
        threshold_slider.setValue(DEFAULT_THRESHOLD_VALUE)  # Set initial value based on the current threshold
        threshold_slider.setTickPosition(QSlider.TicksBelow)
        threshold_slider.setTickInterval(DEFAULT_TICK_VALUE)
        threshold_slider.valueChanged.connect(update_threshold)
        layout.addWidget(threshold_slider)

        # Start Button
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.on_click_start)
        layout.addWidget(self.start_button)

        self.setLayout(layout)
    
    def update_camera(self):
        global CAMERA
        CAMERA = int(self.camera_dropdown.currentText())
        print(CAMERA)
        print(f"Updated source to {CAMERA}")


    def on_click_start(self):
        self.start_button.setEnabled(False)  # Disable the start button
        print("Starting Face Detection...")

        try:
            main()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            self.start_button.setEnabled(True)  # Enable the start button again

    def set_dark_mode(self):
        # Set dark mode palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(0, 51, 102))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Base, QColor(162, 162, 196))


        QApplication.setPalette(palette)


if __name__ == "__main__":
    app = QApplication([])
    config_window = ConfigWindow()
    config_window.show()
    app.setStyle("Fusion")
    app.exec_()


