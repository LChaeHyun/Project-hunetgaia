from flask import Flask, Response, render_template
from detector import ObjectDetection, Reader
from time import sleep
import cv2

app = Flask(__name__)

detector = ObjectDetection('rtsp://210.99.70.120:1935/live/cctv001.stream')
#detector = ObjectDetection('rtsp://192.168.123.198:8554/live')
detector()

@app.route('/')
def index():
    return render_template('index1.html')  # Render the HTML template

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')  # Stream the frames


def gen_frames():
    while True:
        sleep(0.03)
        captured, img = detector.capture()
        if captured:
            encoded, buffer = cv2.imencode('.jpg', img)
            if encoded:
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Yield the frame as JPEG data

if __name__ == '__main__':
    app.run()