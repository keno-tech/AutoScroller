import cv2
import mediapipe as mp
import pyautogui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QPushButton


pyautogui.PAUSE = 0.01

mp_face_detection = mp.solutions.face_detection

# Initialize face detection
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

# Load video using OpenCV
video = cv2.VideoCapture(0)
threshold = 0.2
speed = 20

MIN_THRESHOLD_VALUE = 0
MAX_THRESHOLD_VALUE = 70
MIN_SPEED_VALUE = 1
MAX_SPEED_VALUE = 100
DEFAULT_SPEED_VALUE = 20
DEFAULT_THRESHOLD_VALUE = int(threshold * 100)
DEFAULT_TICK_VALUE = 5

def main():
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
        

        left_start_point = (int(w * threshold),  h)
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

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Release the video capture and close all windows
    video.release()
    cv2.destroyAllWindows()


def update_threshold(value):
    global threshold
    threshold = value / 100.0

def update_speed(value):
    global speed
    speed = value

class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("AutoScroller Configuration")
        self.setFixedSize(640, 480)        
        self.set_dark_mode()

        layout = QVBoxLayout()
        
        name_label = QLabel("AutoScroller")
        name_label.setFont(QFont("Arial", 22, QFont.Bold))
        layout.addWidget(name_label)

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
        start_button = QPushButton("Start", self)
        start_button.clicked.connect(main)
        layout.addWidget(start_button)

        self.setLayout(layout)

    def set_dark_mode(self):
        # Set dark mode palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(palette)

app = QApplication([])
config_window = ConfigWindow()
config_window.show()

app.exec_()
