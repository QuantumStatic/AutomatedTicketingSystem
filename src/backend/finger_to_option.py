
import HandTracking
import numpy
import cv2
from myfunctions_compat import execute_this
from typing import *


hands = HandTracking.HandDetector()

def distance(point1:'tuple[int, int]', point2:'tuple[int, int]') -> float:
    """Returns the distance between two points."""
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5


def tip_touch_to_option(img: numpy.ndarray, draw=True) -> 'tuple[numpy.ndarray, str, bool]':
    """Returns the option that the user is pointing at."""
    points: dict[int, tuple[int, int]] = hands.getAllLandMarks(img, draw)
    opt: int = -1

    try:
        tip_locs = (points[HandTracking.INDEX_TIP], points[HandTracking.MIDDLE_TIP], points[HandTracking.RING_TIP], points[HandTracking.PINKY_TIP])
        
        if hands.finger_tip_touching(points[HandTracking.INDEX_TIP], points[HandTracking.THUMB_TIP]):
            opt = 0
        elif hands.finger_tip_touching(points[HandTracking.MIDDLE_TIP], points[HandTracking.THUMB_TIP]):
            opt = 1
        elif hands.finger_tip_touching(points[HandTracking.RING_TIP], points[HandTracking.THUMB_TIP]):
            opt = 2
        elif hands.finger_tip_touching(points[HandTracking.PINKY_TIP], points[HandTracking.THUMB_TIP]):
            opt = 3
    except KeyError:
        return (img, -1, ())
    
    return (img, opt, tip_locs)


def check_thumbs_up(img: numpy.ndarray, draw=True):
    """Returns True if the user is showing a thumbs up."""
    points: dict[int, tuple[int, int]] = hands.getAllLandMarks(img, draw)
    
    finger: list[bool] = [False]*4
    try:
        finger[0] = distance(points[HandTracking.INDEX_TIP], points[HandTracking.WRIST]) > distance(points[HandTracking.INDEX_MCP], points[HandTracking.WRIST])
        finger[1] = distance(points[HandTracking.MIDDLE_TIP], points[HandTracking.WRIST]) > distance(points[HandTracking.MIDDLE_MCP], points[HandTracking.WRIST])
        finger[2] = distance(points[HandTracking.RING_TIP], points[HandTracking.WRIST]) > distance(points[HandTracking.RING_MCP], points[HandTracking.WRIST])
        finger[3] = distance(points[HandTracking.PINKY_TIP], points[HandTracking.WRIST]) > distance(points[HandTracking.PINKY_MCP], points[HandTracking.WRIST])
        
    except (KeyError, TypeError):
        return (img, False)
    else:
        return (img, (sum(finger) == 0) and (points[HandTracking.THUMB_TIP][1] < 0.95*points[HandTracking.INDEX_TIP][1]))


def number_from_finger(img: numpy.ndarray, draw=True) -> 'tuple[numpy.ndarray, int]':
    """Returns the number that the user is showing."""
    points: dict[int, tuple[int, int]] = hands.getAllLandMarks(img, draw)
    finger: list[bool] = [False]*5
    try:
        finger[0] = distance(points[HandTracking.THUMB_TIP], points[HandTracking.PINKY_MCP]) > 1.2*distance(points[HandTracking.INDEX_MCP], points[HandTracking.PINKY_MCP])
        finger[1] = distance(points[HandTracking.INDEX_TIP], points[HandTracking.WRIST]) > 1.25*distance(points[HandTracking.INDEX_MCP], points[HandTracking.WRIST])
        finger[2] = distance(points[HandTracking.MIDDLE_TIP], points[HandTracking.WRIST]) > 1.15*distance(points[HandTracking.MIDDLE_MCP], points[HandTracking.WRIST])
        finger[3] = distance(points[HandTracking.RING_TIP], points[HandTracking.WRIST]) > 1.1*distance(points[HandTracking.RING_MCP], points[HandTracking.WRIST])
        finger[4] = distance(points[HandTracking.PINKY_TIP], points[HandTracking.WRIST]) > 1.4*distance(points[HandTracking.PINKY_MCP], points[HandTracking.WRIST])
        
    except (KeyError, TypeError):
        return (img, 0)
    else:
        return (img, sum(finger))
    

# @execute_this
def test_finger_analysation():
    video = cv2.VideoCapture(0)
    w_Cam, h_Cam = 640, 480
    video.set(3, w_Cam)
    video.set(4, h_Cam)
    

    while True:
        success, img = video.read()
        img = cv2.flip(img, 1)
        
        # clear_output_screen()
        img, opt, _ = tip_touch_to_option(img)
        print(opt)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


        
    
    
