"""File containing to recognise human in a video stream."""

import cv2
import numpy as np

from typing import *

from myfunctions_compat import execute_this
        

def detect_face(frame:np.ndarray) -> 'tuple[np.ndarray, list[tuple[int]]]':
    face_detector = cv2.CascadeClassifier("/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/cv2/data/haarcascade_frontalface_default.xml")

    try:
        bounding_box_cordinates = face_detector.detectMultiScale(frame, 1.1, 8)
    except ValueError:
        return (frame, [])
    else:
        for (x, y, w, h) in bounding_box_cordinates:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.putText(frame, 'Status : found', (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # print("found")

        # cv2.putText(frame, 'Status : Searching', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
        # cv2.imshow('output', frame)
    
    return (frame, [tuple(co_ordinates) for co_ordinates in bounding_box_cordinates]) if len(bounding_box_cordinates) != 0 else (frame, [])


# @execute_this
def test_it():
    """Testing the code in this file."""
    detect_face(None)