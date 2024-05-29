import torch
import cv2
import time
import datetime
from ultralytics import YOLO
import threading
from collections import deque

CONFIDENCE_THRESHOLD = 0.6
GREEN = (0, 255, 0)
WHITE = (0, 0, 0)

class Reader:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise ValueError(f"Unable to open video source: {source}")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.stop = False
        self.max_buffer_size = 4
        self.frame_buffer = deque(maxlen=self.max_buffer_size)

    def __call__(self):
        thread = threading.Thread(target=self.read, daemon=True)
        thread.start()

    def read(self):
        while not self.stop:
            #time.sleep(0.03)  # Adjust the sleep time to control the frame processing rate
            success, frame = self.cap.read()  # Read a frame from the camera
            if success:
                self.frame_buffer.append(frame)
            else:
                print("Failed to read frame from video source")

    def capture(self):
        if len(self.frame_buffer) < self.max_buffer_size - 1:
            return False, None
        else:
            return True, self.frame_buffer[-2]

    def terminate(self):
        self.stop = True
        self.cap.release()


class Detector:
    def __init__(self, source):
        self.reader = Reader(source)
        self.model = YOLO("./v8sbest.pt")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.max_buffer_size = 4
        self.frame_buffer = deque(maxlen=self.max_buffer_size)
        self.stop = False

        fire_label = open('./Fire.txt', 'r')
        data = fire_label.read()
        self.class_list = data.split('\n')
        fire_label.close()

    def __call__(self):
        self.last_time = time.time()
        thread = threading.Thread(target=self.detect, daemon=True)
        thread.start()

    def detect(self):
        self.reader()
        while not self.stop:
            try:
                start = datetime.datetime.now()
                captured, frame = self.reader.capture()
                if captured:
                    detection = self.model.predict(frame, verbose=False)[0]
                    for data in detection.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
                        confidence = float(data[4])
                        if confidence < CONFIDENCE_THRESHOLD:
                            continue

                        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
                        label = int(data[5])
                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)
                        cv2.putText(frame, self.class_list[label], (xmin, ymin), cv2.FONT_ITALIC, 1, WHITE, 2)

                    end = datetime.datetime.now()

                    total = (end - start).total_seconds()
                    print(f'Time to process 1 frame: {total * 1000:.0f} milliseconds')

                    fps = f'FPS: {1 / total:.2f}'
                    cv2.putText(frame, fps, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    self.frame_buffer.append(frame)
            except Exception as e:
                print(f"Error during detection: {e}")
                self.stop = True
        self.reader.terminate()

    def capture(self):
        if len(self.frame_buffer) < self.max_buffer_size - 1:
            return False, None
        else:
            return True, self.frame_buffer[-2]

    def terminate(self):
        self.stop = True


if __name__ == "__main__":
    detector = Detector(source="rtsp://210.99.70.120:1935/live/cctv001.stream")
    detector()
    while True:
        captured, frame = detector.capture()
        if captured:
            cv2.imshow("Frame", frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cv2.destroyAllWindows()
    detector.terminate()