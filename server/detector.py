import torch
import cv2
import time
import datetime
from ultralytics import YOLO
import threading
from collections import deque
from deep_sort_realtime.deepsort_tracker import DeepSort
import smtplib
from email.message import EmailMessage

CONFIDENCE_THRESHOLD = 0.2
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

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
    def __init__(self, source, email_receiver):
        self.reader = Reader(source)
        self.model = YOLO("./v8sbest.pt")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.max_buffer_size = 4
        self.frame_buffer = deque(maxlen=self.max_buffer_size)
        self.stop = False
        self.tracker = DeepSort(max_age=60)
        self.email_receiver = email_receiver
        self.notification_time_limit = datetime.datetime.now()

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
                    detection = self.model.predict(source=[frame], save=False, verbose=False)[0]
                    results = []
                    
                    detect_object_xmin = -1000

                    for data in detection.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
                        confidence = float(data[4])
                        if confidence < CONFIDENCE_THRESHOLD:
                            continue

                        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
                        label = int(data[5])
                        # cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                        # cv2.putText(frame, class_list[label]+' '+str(round(confidence, 3)) + '%', (xmin, ymin), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
                        results.append([[xmin, ymin, xmax-xmin, ymax-ymin], confidence, label])

                    tracks = self.tracker.update_tracks(results, frame=frame)
                    for i in results:
                        #print(i)
                        #print(i[0][0])
                        pass

                    for track in tracks:
                        if not track.is_confirmed():
                            continue
                        track_id = track.track_id
                        ltrb = track.to_ltrb()
                        xmin, ymin, xmax, ymax = int(ltrb[0]), int(ltrb[1]), int(ltrb[2]), int(ltrb[3])
                        for i in results:
                            gap_xmin = i[0][0] - xmin
                            gap_ymin = i[0][1] - ymin
                            error_range = 20
                            if (gap_xmin > -error_range and  gap_xmin < error_range and gap_ymin > -error_range and gap_ymin < error_range):
                                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)
                                cv2.rectangle(frame, (xmin, ymin - 20), (xmin + 20, ymin), GREEN, -1)
                                cv2.putText(frame, str(track_id) + ' ' + self.class_list[label]+' '+str(round(confidence, 2)), (xmin + 5, ymin - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
                                #print('id : %s label : %s (xmin, ymin) : (%d, %d) (xmax, ymax) : (%d, %d)' % (track_id,self.class_list[label],xmin,ymin,xmax,ymax))
                                self.send_email(self.email_receiver, self.class_list[label])
                                break
                        # if (gap_xmin > -error_range and gap_xmin < error_range and gap_xmax > -error_range and gap_xmax < error_range):
                        #     cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)
                        #     cv2.rectangle(frame, (xmin, ymin - 20), (xmin + 20, ymin), GREEN, -1)
                        #     cv2.putText(frame, str(track_id) + ' ' + class_list[label]+' '+str(round(confidence, 2)), (xmin + 5, ymin - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
                        #     print('id : %s label : %s (xmin, ymin) : (%d, %d) (xmax, ymax) : (%d, %d)' % (track_id,class_list[label],xmin,ymin,xmax,ymax))
                        
                    end = datetime.datetime.now()
                    total = (end - start).total_seconds()
                    # print(f'Time to process 1 frame: {total * 1000:.0f} milliseconds')

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
    
    def send_email(self, reciver,cctv):
        now = datetime.datetime.now()
        if now > self.notification_time_limit:
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            EMAIL_ADDR = 'testhunetgaia@gmail.com'
            smtp.login(EMAIL_ADDR, 'kfzxrsvnqitwnrab')
            message = EmailMessage()
            message.set_content(f'{cctv} has been detected at {now}')
            subject = f'{cctv} has been detected'
            message["Subject"] = subject
            message["From"] = EMAIL_ADDR  
            message["To"] = reciver
            smtp.send_message(message)
            smtp.quit()

            # Don't send email before notification_time_limit
            self.notification_time_limit = now + datetime.timedelta(hours=24) # For Distribution
            #self.notification_time_limit = now + datetime.timedelta(seconds=10) #Debug Feature
            print(f'sent e-mail at {now}, set notification time limit at {self.notification_time_limit}')
        else:
            print(f"didn't sent e-mail at {now}, notification time limit till {self.notification_time_limit}")


if __name__ == "__main__":
    #detector = Detector(source="rtsp://210.99.70.120:1935/live/cctv001.stream", email_receiver='kghun81@gmail.com')
    detector = Detector(source=0, email_receiver='kghun81@gmail.com')
    detector()
    while True:
        captured, frame = detector.capture()
        if captured:
            cv2.imshow("Frame", frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cv2.destroyAllWindows()
    detector.terminate()