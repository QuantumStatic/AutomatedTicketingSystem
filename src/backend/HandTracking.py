from __future__ import annotations
import cv2
import mediapipe as mp
import math
from typing import *

THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP = 4, 8, 12, 16, 20
THUMB_MCP, INDEX_MCP, MIDDLE_MCP, RING_MCP, PINKY_MCP = 2, 5, 9, 13, 17
THUMB_IP, INDEX_IP, MIDDLE_IP, RING_IP, PINKY_IP = 2, 6, 10, 14, 18
THUMB_PIP, INDEX_PIP, MIDDLE_PIP, RING_PIP, PINKY_PIP = 3, 6, 10, 14, 18
WRIST = 0

class HandDetector:

    _most_recent_frame_idx:dict = {}
    def __init__(self, detection_con=0.5, tracking_con=0.5):
        self.mpHands = mp.solutions.mediapipe.python.solutions.hands
        self.hands = self.mpHands.Hands(min_detection_confidence=detection_con, min_tracking_confidence=tracking_con, max_num_hands=3)
        self.mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils

    
    def getPosition(self, img, hand_no=0, draw=True):
        lst:list[tuple[int, int]] = []
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        if results.multi_hand_landmarks:
            if len(results.multi_hand_landmarks) >= hand_no+1:
                for _, lm in enumerate(results.multi_hand_landmarks[hand_no].landmark):
                    h, w, c = img.shape
                    x, y = int(lm.x*w), int(lm.y*h)
                    lst.append((x,y))
                if draw:
                    self.mpDraw.draw_landmarks(img, results.multi_hand_landmarks[hand_no], self.mpHands.HAND_CONNECTIONS)
        return lst

    def getAllLandMarks(self, img, draw=True) -> dict[int, tuple[int, int]]:
        
        points: dict[int, tuple[int, int]] = {}
        
        results = self.hands.process(img)
        if results.multi_hand_landmarks:
            if len(results.multi_hand_landmarks) >= 1:
                for id, lm in enumerate(results.multi_hand_landmarks[0].landmark):
                        h, w, c = img.shape
                        x, y = int(lm.x*w), int(lm.y*h)
                        points[id] = (x, y)
                if draw:
                    self.mpDraw.draw_landmarks(img, results.multi_hand_landmarks[0], self.mpHands.HAND_CONNECTIONS)
        
        return points

    def _distance(self, point1:tuple[int, int], point2:tuple[int, int]) -> float:
        """Returns the distance between two points."""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def finger_tip_touching(self, tip1:tuple[int, int], tip2:tuple[int, int], threshold:int = 35) -> bool:
        """Returns True if the two fingers are touching."""

        try:
            return self._distance(tip1, tip2) < threshold
        except (IndexError, TypeError):
            return False

