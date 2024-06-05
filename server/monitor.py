from flask import (
    Flask,
    Response,
    request,
    jsonify,
    session,
)

from flask_cors import CORS
import cv2
from flask_session import Session
from DBmanagement import Management
from dotenv import load_dotenv
from datetime import timedelta

import os


load_dotenv()

try:
    host = os.environ.get("DB_HOST")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    management = Management(host, user, password)
    print("DB connected")
except:
    print("mysql loading error")


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SESSION_TYPE"] = os.environ.get("SESSION_TYPE")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=720)
Session(app)
CORS(app, supports_credentials=True)


@app.route("/", methods=["POST"])
def login():
    try:
        id = request.json["id"]
        password = request.json["password"]

        login_success = management.login(id, password)

        if login_success:
            session["session_id"] = id
            print(id)
            return jsonify({"isLogin": True, "session_id": id})
        else:
            return jsonify({"isLogin": False})
    except:
        return jsonify({"isLogin": False})


@app.route("/signup", methods=["POST"])
def signup():
    try:
        id = request.json["id"]
        password = request.json["password"]

        signup_success = management.add_user(id, password)
        if signup_success:
            return jsonify({"signup": True}), 200
        else:
            return jsonify({"signup": False}), 204
    except:
        return jsonify({"signup": False}), 204


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("session_id", None)
    return jsonify({"message": "Logged out successfully!"}), 200


@app.route("/get_all", methods=["GET"])
def get_all():
    if "session_id" not in session:
        return jsonify({"message": "Authentication is required!"}), 204
    rtsp_addresses = management.rtsp_get()
    email = management.email_get()
    return jsonify({"addresses": rtsp_addresses, "email": email})


@app.route("/get_rtsp", methods=["GET"])
def get_rtsp():
    if "session_id" not in session:
        return jsonify({"message": "Authentication is required!"}), 204
    rtsp_addresses = management.rtsp_get()
    return jsonify({"rtsp": rtsp_addresses})


@app.route("/add_rtsp", methods=["POST"])
def add_rtsp():
    if "session_id" not in session:
        return jsonify({"message": "Authentication is required!"}), 204
    name = request.json["name"]
    address = request.json["address"]

    try:
        success_add_rtsp = management.rtsp_add(name, address)
        if success_add_rtsp:
            return jsonify({"add": True}), 200
        else:
            return jsonify({"add": False}), 204
    except:
        return jsonify({"message": "can not add rtsp address"})


@app.route("/delete_rtsp", methods=["POST"])
def delete_rtsp():
    if "session_id" not in session:
        return jsonify({"message": "Authentication is required!"}), 204
    try:
        rtsp_id = request.json["id"]

        management.rtsp_delete(rtsp_id)

        return jsonify({"message": "RTSP stream deleted successfully."})
    except:
        return jsonify({"message": "can not delete that RTSP stream"})


@app.route("/get_email", methods=["GET"])
def get_email():
    if "session_id" not in session:
        return jsonify({"message": "Authentication is required!"}), 204
    email = management.email_get()
    return jsonify({"email": email})


@app.route("/add_email", methods=["POST"])
def add_email():
    if "session_id" not in session:
        return jsonify({"message": "Authentication is required!"}), 204

    email = request.json["email"]

    try:
        success_add_email = management.email_add(email)
        if success_add_email:
            return jsonify({"message": "Email added successfully"}), 200
        else:
            return jsonify({"message": "Email added Failed"}), 204
    except:
        return jsonify({"message": "something went wrong"})


@app.route("/delete_email", methods=["POST"])
def delete_email():
    if "session_id" not in session:
        return jsonify({"message": "Authentication is required!"}), 204

    try:
        email_id = request.json.get("id")

        management.email_delete(email_id)

        return jsonify({"message": "Email deleted successfully."})
    except:
        return jsonify({"message": "can not delete that email"})


def webcam(url):
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
