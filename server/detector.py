import torch
import numpy as np
import cv2
import time
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import threading
from collections import deque

class Reader:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)
        assert self.cap.isOpened()
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.stop = False
        self.max_buffer_size = 4
        self.frame_buffer = deque(maxlen=self.max_buffer_size)

    def __call__(self):
        thread = threading.Thread(target=self.read)
        thread.start()

    def read(self):
        while not self.stop :
            time.sleep(0.03)  # Adjust the sleep time to control the frame processing rate
            success, frame = self.cap.read()  # Read a frame from the camera
            if success:
                self.frame_buffer.append(frame)
    
    def capture(self):
        if len(self.frame_buffer)<self.max_buffer_size-1:
            return False, None
        else:
            return True, self.frame_buffer[-2]

    def terminate(self):
        self.stop = True
        self.cap.release()

class ObjectDetection:

    def __init__(self, source):
        # default parameters
        self.reader = Reader(source)

        # model information
        self.model = YOLO("D:\\jongp\\rstream\\yolotest\\stream_test3\\v8sbest.pt")

        # visual information
        self.annotator = None
        self.last_time = 0
        self.this_time = 0

        # device information
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.max_buffer_size = 4
        self.frame_buffer = deque(maxlen=self.max_buffer_size)
        self.stop = False
    
    def __call__(self):
        self.last_time = time.time()
        thread = threading.Thread(target=self.detect)
        thread.start()

    def predict(self, im0):
        results = self.model.predict(im0, verbose=False, stream=True)
        return next(results)

    def display_fps(self, im0):
        self.this_time = time.time()
        fps = 1 / np.round(self.this_time - self.last_time, 2)
        self.last_time = self.this_time
        text = f'FPS: {int(fps)}'
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
        gap = 10
        cv2.rectangle(im0, (20 - gap, 70 - text_size[1] - gap), (20 + text_size[0] + gap, 70 + gap), (255, 255, 255), -1)
        cv2.putText(im0, text, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)

    def plot_bboxes(self, result, im0):
        class_ids = []
        self.annotator = Annotator(im0, 3, result.names)
        boxes = result.boxes.xyxy.cpu()
        clss = result.boxes.cls.cpu().tolist()
        names = result.names
        for box, cls in zip(boxes, clss):
            class_ids.append(cls)
            self.annotator.box_label(box, label=names[int(cls)], color=colors(int(cls), True))
        return im0, class_ids

    def detect(self):
        self.reader()
        while not self.stop:
            captured, frame = self.reader.capture()
            if captured:
                result = self.predict(frame)
                frame, _ = self.plot_bboxes(result, frame)
                self.display_fps(frame)
                self.frame_buffer.append(frame)
        self.reader.terminate()
        cv2.destroyAllWindows()
    
    def capture(self):
        if len(self.frame_buffer) < self.max_buffer_size-1:
            return False, None
        else:
            return True, self.frame_buffer[-2]
    
    def terminate(self):
        self.stop = True
        pass

if __name__ == '__main__' :
    detector = ObjectDetection(source='rtsp://210.99.70.120:1935/live/cctv001.stream')
    #detector = ObjectDetection(source='rtsp://192.168.123.20:8554/stream')
    detector()
    while True:
        captured, frame = detector.capture()
        if captured:
            cv2.imshow("Frame", frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cv2.destroyAllWindows()
    detector.terminate()