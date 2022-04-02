from flask import Response
from flask import Flask
from flask import render_template
import threading
import numpy
import time
import cv2
import mss
from record import Camera

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def start_server():
    app.run(host='0.0.0.0', debug=True)
start_server()