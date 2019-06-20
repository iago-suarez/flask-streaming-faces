###############################################################################
# @author Iago Suarez
###############################################################################
import abc
import cv2
from base_camera import BaseCamera


class Camera(BaseCamera):
    # TODO Here you should put your IP camera for example:
    #  video_source = "http://user:password@128.130.144.122/video.cgi"
    video_source = 0
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def process_frame(frame):
        """"Generator that returns frames from the camera."""
        raise RuntimeError('Must be implemented by subclasses.')

    @classmethod
    def frames(cls):
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            cls.process_frame(img)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()


class DefaultCamera(Camera):
    """ A simple class that do not process the input frame."""

    @staticmethod
    def process_frame(frame):
        return frame


class FaceDetectionCamera(Camera):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    @staticmethod
    def process_frame(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = FaceDetectionCamera.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            eyes = FaceDetectionCamera.eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        return frame
