from flask import Flask, Response, render_template
from detector import ObjectDetection, Reader
from time import sleep
import cv2

class User:
    user_list = []
    def __init__(self):
        self.username = ''
        self.password = ''
        self.email = ''
        self.preferredNumberOfColumns = 0

        self.videos = []

        self.detectors = []

        User.user_list.append(self)
    
    def findUser(username):
        for v in User.user_list:
            if v.username==username:
                return v


app = Flask(__name__)

user = User()
user.username = 'orange'
user.password = 'juice'
user.email = 'limetree81@gmail.com'
user.videos = ['rtsp://210.99.70.120:1935/live/cctv001.stream',
               'rtsp://210.99.70.120:1935/live/cctv002.stream',
               'rtsp://210.99.70.120:1935/live/cctv003.stream',
               'rtsp://210.99.70.120:1935/live/cctv004.stream']

for v in user.videos:
    d = ObjectDetection(v)
    d()
    user.detectors.append(d)

@app.route('/')
def index():
    return render_template('monitor.html')  # Render the HTML template

@app.route('/<username>/video_feed/<int:index>')
def video_feed(username, index):
    user = User.findUser(username=username)
    return Response(gen_frames(user, index), mimetype='multipart/x-mixed-replace; boundary=frame')  # Stream the frames

def gen_frames(user, index):
    while True:
        sleep(0.03)
        captured, img = user.detectors[index].capture()
        if captured:
            encoded, buffer = cv2.imencode('.jpg', img)
            if encoded:
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Yield the frame as JPEG data

@app.route('/<username>/all')
def all_video_feeds(username):
    user = User.findUser(username=username)
    return render_template('all_video_feeds.html', username=username, detector_count=len(user.detectors))

'''
TODO List
?column=i 로 칼럼 개수 조절 가능
회원가입, 로그인, 설정 페이지(e-mail등록, CCTV 주소 추가/삭제, 회원 탈퇴 기능), DB
'''


if __name__ == '__main__':
    app.run()