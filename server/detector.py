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
from DBmanagement import Management
import os
from dotenv import load_dotenv, find_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

CONFIDENCE_THRESHOLD = 0.3
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

class Reader:
    def __init__(self, source):
        self.source = source
        self.cap = cv2.VideoCapture(source)
        while not self.cap.isOpened():
            print(f"Failed to open camera from {self.source}")
            self.cap.release()
            time.sleep(10)
            self.cap = cv2.VideoCapture(source)
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
            try:
                success, frame = self.cap.read()
                if success:
                    self.frame_buffer.append(frame)
                else:
                    print(f"Failed to read frame from {self.source}")
            except Exception as e:
                print(e)
                self.cap.release()
                self.__init__(self.source)
                print(f"Failed to read frame from {self.source}")
                time.sleep(10)


    def capture(self):
        if len(self.frame_buffer) < self.max_buffer_size - 1:
            return False, None
        else:
            return True, self.frame_buffer[-2]

    def terminate(self):
        self.stop = True
        self.cap.release()


class Detector:
    email_receivers = []
    notification_time_limit = datetime.datetime(year=1,month=1,day=1)

    def __init__(self, source):
        self.source = source
        self.reader = Reader(source)
        self.model = YOLO("./v8sbest.pt")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.max_buffer_size = 4
        self.frame_buffer = deque(maxlen=self.max_buffer_size)
        self.stop = False
        self.tracker = DeepSort(max_age=60)

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
        capNum = 1
        while not self.stop:
            try:
                start = datetime.datetime.now()
                captured, frame = self.reader.capture()
                if captured:
                    detection = self.model.predict(source=[frame], save=False, verbose=False)[0]
                    results = []

                    for data in detection.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
                        confidence = float(data[4])
                        if confidence < CONFIDENCE_THRESHOLD:
                            continue

                        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
                        label = int(data[5])
                        results.append([[xmin, ymin, xmax-xmin, ymax-ymin], confidence, label])

                    tracks = self.tracker.update_tracks(results, frame=frame)

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
                                print(f"Fire of smoke Detected at {self.source}")
                                img_captured = cv2.imwrite('./capture/capture_%02d.png' % capNum, frame)
                                self.send_email(capNum)
                                capNum += 1
                                if (capNum > 10):
                                    capNum = 1
                                
                                break
                    end = datetime.datetime.now()
                    total = (end - start).total_seconds()
                    fps = f'FPS: {1 / total:.2f}'
                    cv2.putText(frame, fps, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    self.frame_buffer.append(frame)
            except Exception as e:
                print(f"Error during detection: {e}")
                time.sleep(10)
        self.reader.terminate()

    def capture(self):
        if len(self.frame_buffer) < self.max_buffer_size - 1:
            return False, None
        else:
            return True, self.frame_buffer[-2]

    def terminate(self):
        cv2.destroyAllWindows()
        self.stop = True

    def send_email(self, capNum):
        now = datetime.datetime.now()
        if now > self.notification_time_limit:
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            EMAIL_ADDR = 'testhunetgaia@gmail.com'
            smtp.login(EMAIL_ADDR, 'kfzxrsvnqitwnrab')
            message = MIMEMultipart('related')
            # email message body
            message_body = f'Fire or smoke has been detected at {now}'
            message_html = MIMEText(f'<html><body>{message_body}<br><img src="cid:image1" style="width: 100%; max-width:600px; margin: 10px;"></body></html>', 'html')
            message.attach(message_html)

            # Add an image to your email
            self.capNum = capNum
            image_path = './capture/capture_%02d.png' % self.capNum
            with open(image_path,'rb') as img:
                    image_file = MIMEImage(img.read(), name=image_path)
            image_file.add_header('Content-ID','<image1>')
            message.attach(image_file)
            
            subject = f'Fire or smoke has been detected'
            message["Subject"] = subject
            message["From"] = EMAIL_ADDR
            message["To"] = ', '.join(self.email_receivers)
            smtp.send_message(message)
            smtp.quit()

            # Don't send email before notification_time_limit
            self.notification_time_limit = now + datetime.timedelta(hours=24)
            print(f'sent e-mail at {now}, set notification time limit at {self.notification_time_limit} with capNum:{self.capNum}')

if __name__ == "__main__":
    print("Initializing Detectors. Press Ctrl+C to stop.")
    env_path = find_dotenv()
    assert env_path, ".env not found. Please Create one and retry."
    load_dotenv(env_path)

    assert os.path.isfile('v8sbest.pt'), "Missing v8sbest.pt. Aborting..."

    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    try:
        db = Management(db_host, db_user, db_password)
    except Exception as  e:
        print(e)
        print("Failed to open DB. Is DB created and .env info correct?")
        exit()
    
    detectors = dict()
    rtsps = []
    email_receivers = []

    while True:

        new_rtsps = db.rtsp_get()
        new_email_receivers = [email for _, email in db.email_get()]
        print(f'Currently watching:',*[rtsp for _, _, rtsp in new_rtsps], sep='\n\t', end='\n\n')
        print(f'Email receivers:', *new_email_receivers, sep='\n\t', end='\n\n')

        if new_rtsps != rtsps:
            for index, _, address in set(rtsps) - set(new_rtsps):
                detectors[index].terminate()
                del(detectors[index])
                print(f'{address} deleted.')
            for index, _, address in set(new_rtsps) - set(rtsps):
                detector = Detector(address)
                detector()
                detectors[index] = detector
                print(f'{address} added.')
            rtsps = new_rtsps
        
        if new_email_receivers != email_receivers:
            Detector.email_receivers = new_email_receivers
            email_receivers = new_email_receivers
            print("E-mail address info updated.")
        
        db.refresh_connection(db_host, db_user, db_password)
        time.sleep(30)