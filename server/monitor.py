from flask import (
    Flask,
    Response,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    send_from_directory,
    session,
)
from detector import Detector, Reader
from time import sleep
from flask_cors import CORS
import cv2
import ffmpeg
import uuid

from DBmanagement import Management


try:
    management = Management()
    print("DB connected")
except:
    print("mysql loading error")


class User:
    user_list = []

    def __init__(self):
        self.username = ""
        self.password = ""
        self.email = ""

        self.videos = []

        self.detectors = []

        User.user_list.append(self)

    @classmethod
    def findUser(cls, username):
        for user in User.user_list:
            if user.username == username:
                return user


app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = "secret_key"
# user.username = "orange"
# user.password = "juice"
# user.email = "limetree81@gmail.com"
# user.videos = [
#     "rtsp://210.99.70.120:1935/live/cctv001.stream",
#     "rtsp://210.99.70.120:1935/live/cctv002.stream",
#     "rtsp://210.99.70.120:1935/live/cctv003.stream",
#     "rtsp://210.99.70.120:1935/live/cctv004.stream",
# ]


@app.route("/", methods=["POST"])
def login():
    try:
        id = request.json["id"]
        password = request.json["password"]

        login_success = management.login(id, password)

        if login_success:
            session_id = str(uuid.uuid4())
            session[session_id] = {"id": id}
            return jsonify({"isLogin": True, "session_id": session_id})
        else:
            return jsonify({"isLogin": False})
    except:
        return jsonify({"isLogin": False})


@app.route("/get_all", methods=["GET"])
def get_all():
    rtsp_addresses = management.rtsp_get()
    email = management.email_get()
    return jsonify({"addresses": rtsp_addresses, "email": email})


@app.route("/get_rtsp", methods=["GET"])
def get_rtsp():
    rtsp_addresses = management.rtsp_get()
    return jsonify({"rtsp": rtsp_addresses})


@app.route("/add_rtsp", methods=["POST"])
def add_rtsp():
    name = request.json["name"]
    address = request.json["address"]

    try:
        rtsp = management.rtsp_add(name, address)
        # return jsonify({"message": "RTSP added successfully"})
        return jsonify({"rtsp": rtsp})
    except:
        return jsonify({"message": "can not add rtsp address"})


@app.route("/delete_rtsp", methods=["POST"])
def delete_rtsp():
    try:
        rtsp_id = request.json["id"]

        management.rtsp_delete(rtsp_id)

        return jsonify({"message": "RTSP stream deleted successfully."})
    except:
        return jsonify({"message": "can not delete that RTSP stream"})


@app.route("/get_email", methods=["GET"])
def get_email():
    email = management.email_get()
    return jsonify({"email": email})


@app.route("/add_email", methods=["POST"])
def add_email():
    email = request.json["email"]

    try:
        management.email_add(email)
        return jsonify({"message": "Email added successfully"})
    except:
        return jsonify({"message": "something went wrong"})


@app.route("/delete_email", methods=["POST"])
def delete_email():
    try:
        # Get the ID from the request
        email_id = request.json.get("id")

        # Delete the email
        management.email_delete(email_id)

        return jsonify({"message": "Email deleted successfully."})
    except:
        return jsonify({"message": "can not delete that email"})


def webcam(url):
    # camera = cv2.VideoCapture("rtsp://admin:admin1234@211.105.100.174:3400/stream1")
    # camera = cv2.VideoCapture(0)
    # camera = cv2.VideoCapture("rtsp://210.99.70.120:1935/live/cctv004.stream")
    camera = cv2.VideoCapture(url)

    while True:
        success, frame = camera.read()
        if success:

            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        else:
            break


@app.route("/webcam")
def webcam_display():
    rtsp_url = request.args.get("url")
    print(rtsp_url)
    return Response(
        webcam(rtsp_url), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(debug=True)

# @app.route("/convert")
# def convert():
#     rtsp_url = request.args.get("rtsp_url")
#     if not rtsp_url:
#         return jsonify({"error": "RTSP URL is required"}), 400

#     # HLS output options
#     hls_output = "static/hls/stream.m3u8"

#     # Convert RTSP to HLS
#     ffmpeg.input(rtsp_url, rtsp_transport="tcp").output(
#         hls_output,
#         c="copy",
#         f="hls",
#         hls_time=2,
#         hls_list_size=3,
#         hls_flags="delete_segments",
#     ).run()

#     return jsonify({"success": True, "url": request.host_url + hls_output})


# @app.route("/hls/<path:path>")
# def serve_hls(path):
#     return send_from_directory("static/hls", path)


# # def index():
# #     username = "orange"
# #     return render_template("index.html", username=username)  # Render the HTML template

# @app.route('/<username>/video_feed/<int:index>')
# def video_feed(username, index):
#     user = User.findUser(username=username)
#     return Response(gen_frames(user, index), mimetype='multipart/x-mixed-replace; boundary=frame')  # Stream the frames

# def gen_frames(user, index):
#     while True:
#         sleep(0.03)
#         captured, img = user.detectors[index].capture()
#         if captured:
#             encoded, buffer = cv2.imencode('.jpg', img)
#             if encoded:
#                 frame = buffer.tobytes()
#                 yield (b'--frame\r\n'
#                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Yield the frame as JPEG data

# @app.route('/<username>/all')
# def all_video_feeds(username):
#     user = User.findUser(username=username)
#     #return render_template('all_video_feeds.html', username=username, detector_count=len(user.detectors))
#     return render_template('monitor.html', username=username, detector_count=len(user.detectors))

# # Profile route
# @app.route('/<username>/profile', methods=['GET', 'POST'])
# def profile(username):
#     user = User.findUser(username)
#     print(user)
#     if not user:
#         return "User not found", 404
#     if request.method == 'POST':
#         address = request.form.get('address')
#         if address:
#             user.videos.append(address)
#             detect = Detector(address)
#             detect()
#             user.detectors.append(detect)
#             return redirect(url_for('profile', username=username))
#     return render_template('profile.html', username=username, addresses=user.videos)

# # Remove address route
# @app.route('/<username>/remove_address/<int:address_index>', methods=['POST'])
# def remove_address(username, address_index):
#     user = User.findUser(username)
#     if not user or address_index >= len(user.videos):
#         return "Address not found", 404
#     user.detectors[address_index].terminate()
#     user.videos.pop(address_index)
#     user.detectors.pop(address_index)
#     return redirect(url_for('profile', username=username))

# '''
# TODO List
# css
# 네비게이션바, 홈, 회원가입?, 로그인?, 설정 페이지(e-mail등록, ?회원 탈퇴? 기능), DB
# 파일 이름 수정, 경로명 수정 app.py, monitor.py등
# requirements.txt 작성
# '''


# @app.route("/login")
# def signin():
#     username = "orange"
#     return render_template("loginForm.html", username=username)


# @app.route("/signup")
# def signup():
#     return render_template("signupForm.html")
# username = request.form["username"]
# password = request.form["password"]
# confirm_password = request.form["confirm_password"]
# email = request.form["email"]

# if password != confirm_password:
#     flash("Passwords do not match!", "danger")
#     return redirect(url_for("signup"))

# # DB에 저장
# user = User()
# user.username = username
# user.password = password
# user.email = email
# user.videos = [
#     "rtsp://210.99.70.120:1935/live/cctv001.stream",
#     "rtsp://210.99.70.120:1935/live/cctv004.stream",
# ]

# flash("Account created successfully!", "success")
# return redirect(
#     url_for("login")
# )
