import cv2

from myfunctions_compat import execute_this
from HandTrackingTest import FindHands




@execute_this
def main() -> None:
    video_capture = cv2.VideoCapture(0)
    w_cam, h_cam = 640, 480
    video_capture.set(3, w_cam)
    video_capture.set(4, h_cam)

    hands = FindHands()

    while True:
        _, cv2_img = video_capture.read()
        # cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        cv2_img = cv2.flip(cv2_img, 1)
        print(hands.finger_tip_touching(cv2_img, 4, 8))
    



        

