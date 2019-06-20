#!/usr/bin/env python

###############################################################################
# @author Iago Suarez
###############################################################################
from flask import Flask, render_template, Response

# import camera driver
from camera_opencv import DefaultCamera, FaceDetectionCamera

app = Flask(__name__)

# TYPE_OF_CAMERA = DefaultCamera
TYPE_OF_CAMERA = FaceDetectionCamera


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(TYPE_OF_CAMERA()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
