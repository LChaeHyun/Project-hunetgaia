import torch
import numpy as np
import cv2
import time
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import threading

class Reader:

    frame_buffer = []
    stop = False
    buf_max = 120

    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)
        assert self.cap.isOpened()
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def __call__(self):
        thread = threading.Thread(target=self.read)
        thread.start()

    def read(self):
        while not self.stop :
            success, frame = self.cap.read()  # Read a frame from the camera
            if not success:
                break
            else:
                if len(self.frame_buffer) < self.buf_max:
                    self.frame_buffer.append(frame)  # Add the frame to the buffer
                time.sleep(0.03)  # Adjust the sleep time to control the frame processing rate

    def capture(self):
        ret = False
        frame = None
        if(len(self.frame_buffer) > 0):
            ret = True
            frame = self.frame_buffer.pop()
            self.frame_buffer.clear()
        return ret, frame
    
    def terminate(self):
        self.stop = True
        self.cap.release()
        pass

class ObjectDetection:

    frame_buffer = []
    stop = False
    buf_max = 120

    def __init__(self, capture_index):
        # default parameters
        self.reader = Reader(capture_index)

        # model information
        self.model = YOLO("D:\\jongp\\rstream\\wandlab-cv-streamer\\lab\\wandlab\\v8sbest.pt")

        # visual information
        self.annotator = None
        self.start_time = 0
        self.end_time = 0

        # device information
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    def __call__(self):
        thread = threading.Thread(target=self.detect)
        thread.start()

    def predict(self, im0):
        results = self.model(im0)
        return results

    def display_fps(self, im0):
        self.end_time = time.time()
        fps = 1 / np.round(self.end_time - self.start_time, 2)
        text = f'FPS: {int(fps)}'
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
        gap = 10
        cv2.rectangle(im0, (20 - gap, 70 - text_size[1] - gap), (20 + text_size[0] + gap, 70 + gap), (255, 255, 255), -1)
        cv2.putText(im0, text, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)

    def plot_bboxes(self, results, im0):
        class_ids = []
        self.annotator = Annotator(im0, 3, results[0].names)
        boxes = results[0].boxes.xyxy.cpu()
        clss = results[0].boxes.cls.cpu().tolist()
        names = results[0].names
        for box, cls in zip(boxes, clss):
            class_ids.append(cls)
            self.annotator.box_label(box, label=names[int(cls)], color=colors(int(cls), True))
        return im0, class_ids

    def detect(self):
        self.reader()
        while not self.stop:
            self.start_time = time.time()
            ret, frame = self.reader.capture()
            if ret:
                results = self.predict(frame)
                frame, _ = self.plot_bboxes(results, frame)
                self.display_fps(frame)
                self.frame_buffer.append(frame)
        self.reader.terminate()
        cv2.destroyAllWindows()
    
    def capture(self):
        ret = False
        frame = None
        if(len(self.frame_buffer) > 0):
            ret = True
            frame = self.frame_buffer.pop()
            self.frame_buffer.clear()
        return ret, frame
    
    def terminate(self):
        self.stop = True
        pass

if __name__ == '__main__' :
    detector = ObjectDetection(capture_index='rtsp://210.99.70.120:1935/live/cctv001.stream')
    #detector = ObjectDetection(capture_index='rtsp://192.168.123.20:8554/stream')
    detector()