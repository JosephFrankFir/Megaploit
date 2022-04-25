import cv2
import mss
import numpy
import threading
import time
import pyautogui




class Camera(object):
    thread = None
    frame = None
    last_access = 0

    def __init__(self):
        if Camera.thread is None:
            Camera.last_access = time.time()
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()

        return Camera.frame

    @staticmethod
    def frames():
        monitor = {
            'top': 0,
            'left': 0,
            'width': 1366,
            'height': 768
        }
        with mss.mss() as sct:
            while True:
                time.sleep(0)
                raw = sct.grab(monitor)
                # Use numpy and opencv to convert the data to JPEG.
                img = cv2.imencode('.jpg', numpy.array(raw))[1].tobytes()
                yield(img)

    @classmethod
    def _thread(cls):
        print('Starting camera thread.')
        frames_iter = cls.frames()
        for frame in frames_iter:
            Camera.frame = frame
            if time.time() - cls.last_access > 10:
                print('inactivity.')
        cls.thread = None