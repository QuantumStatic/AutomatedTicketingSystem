import constants
import cv2
import numpy
import os
import pickle

from typing import *


from face_detector import detect_face
from myfunctions_compat import execute_this

def user_id_from_face(face_cutout:numpy.ndarray) -> int:
    """Get user info"""

    *_, filenames = next(os.walk(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/Database/registered_users"))

    for name in reversed(sorted(filenames)):
        if name == ".DS_Store":
            continue
        
        with open(f"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/Database/registered_users/processed_imgs/{name}", "rb") as f:
            img = pickle.load(f)

        # 420 pixels is limit
        face_cutout = cv2.resize(face_cutout, (420, 420), interpolation=cv2.INTER_AREA)

        detector = cv2.ORB_create(nfeatures=10_000)
        kpts = detector.detect(face_cutout, None)
        
        descriptor = cv2.xfeatures2d.BEBLID_create(0.65)
        kpts, des = descriptor.compute(face_cutout, kpts)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des, img, k=2)

        matches_f = len(tuple(filter(lambda match: match[0].distance < 0.885*match[1].distance, matches)))
        if matches_f > 35:
            print(f"found with {matches_f}")
            return int(name[0])
        else:
            print(f"Failed to match with {int(name[0])} as found {matches_f}")
    return -1


def face_matcher(img_frame:numpy.ndarray) -> 'tuple[numpy.ndarray, int]':
    frame, face_coordinates = detect_face(img_frame)
    if constants.LOCATED_USER != -1:
        return (frame, constants.LOCATED_USER)
    else:
        if len(face_coordinates) == 0:
            return (frame, -1)
        try:
            for (x, y, w, h) in face_coordinates:
                face_cutout = frame[y:y+h, x:x+w].copy()
                user_id = user_id_from_face(face_cutout)
                if user_id != -1:
                    constants.LOCATED_USER = user_id
                    return (frame, user_id)
            return (frame, -1)
        except IndexError:
            print(f"face: {face_coordinates}\nSize: {len(face_coordinates)}")
            input('>')
            return (frame, -1)



@execute_this
def testing():
    pass