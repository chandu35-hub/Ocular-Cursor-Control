import cv2
import pyautogui
import time

from gaze_tracker import GazeTracker
from screen import Screen

def nothing (val):
    pass

RES_SCREEN = pyautogui.size()

SCREEN_WIDTH = RES_SCREEN[0]
SCREEN_HEIGHT = RES_SCREEN[1]

camera = cv2.VideoCapture (0)

gaze_tracker = GazeTracker()
screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT)

cv2.namedWindow("frame")
cv2.createTrackbar('threshold', 'frame', 0, 255, nothing)
cv2.setTrackbarPos('threshold', 'frame', 1)

screen.clean()
screen.show()

while True:
        _, frame = camera.read() 

        print(frame.shape)

        start = time.time()

        gaze_tracker.update(frame)

        end = time.time()

        cv2.namedWindow("frame")
        dec_frame = gaze_tracker.eye_tracker.decorate_frame()

        dec_frame = cv2.resize(dec_frame,(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))

        cv2.moveWindow("frame", 0 , 0)
        cv2.imshow('frame', dec_frame)

        try:
            gaze = gaze_tracker.get_gaze()
        except:
            gaze = None
            screen.print_message("CALIBRATION REQUIRED!")
            screen.show()
            print("CALIBRATION REQUIRED!")

        print("GAZE: {}".format(gaze))

camera.release()
cv2.destroyAllWindoes()