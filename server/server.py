from flask import Flask, Response, render_template
from detector import ObjectDetection
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML template

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')  # Stream the frames

def gen_frames():
    detector = ObjectDetection(capture_index='rtsp://210.99.70.120:1935/live/cctv001.stream')
    detector()
    while True:
        ret, img = detector.capture()
        print(ret)
        if ret:
            _, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Yield the frame as JPEG data

if __name__ == '__main__':
    app.run()
