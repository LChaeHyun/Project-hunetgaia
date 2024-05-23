from flask import Flask, Response, render_template, request, redirect, url_for
from detector import ObjectDetection, Reader
from time import sleep
import cv2

class User:
    user_list = []
    def __init__(self):
        self.username = ''
        self.password = ''
        self.email = ''

        self.videos = []

        self.detectors = []

        User.user_list.append(self)
    
    @classmethod
    def findUser(cls, username):
        for user in User.user_list:
            if user.username==username:
                return user

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
    return render_template('index.html')  # Render the HTML template

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
    #return render_template('all_video_feeds.html', username=username, detector_count=len(user.detectors))
    return render_template('monitor.html', username=username, detector_count=len(user.detectors))

# Profile route
@app.route('/<username>/profile', methods=['GET', 'POST'])
def profile(username):
    user = User.findUser(username)
    if not user:
        return "User not found", 404
    if request.method == 'POST':
        address = request.form.get('address')
        if address:
            user.videos.append(address)
            detect = ObjectDetection(address)
            detect()
            user.detectors.append(detect)
            return redirect(url_for('profile', username=username))
    return render_template('profile.html', username=username, addresses=user.videos)

# Remove address route
@app.route('/<username>/remove_address/<int:address_index>', methods=['POST'])
def remove_address(username, address_index):
    user = User.findUser(username)
    if not user or address_index >= len(user.videos):
        return "Address not found", 404
    user.detectors[address_index].terminate()
    user.videos.pop(address_index)
    user.detectors.pop(address_index)
    return redirect(url_for('profile', username=username))

'''
TODO List
css
네비게이션바, 홈, 회원가입?, 로그인?, 설정 페이지(e-mail등록, ?회원 탈퇴? 기능), DB
파일 이름 수정, 경로명 수정 app.py, monitor.py등
requirements.txt 작성
'''

if __name__ == '__main__':
    app.run()