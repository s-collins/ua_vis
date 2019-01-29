import cv2 as cv

CAMERA_DEVICE_ID = 0

class Camera:

    def __init__(self):
        self.capture = cv.VideoCapture(CAMERA_DEVICE_ID)
        self.open = self.capture.isOpened()

    def __del__(self):
        self.capture.release()

    def good(self):
        return self.open

    def get_frame(self):
        if self.open:
            ret, frame = self.capture.read()
            return frame
        else:
            raise RuntimeError('Camera could not get frame.')
