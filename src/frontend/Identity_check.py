"""This file creates the first screen after the booking process starts.
It checks identity of the user and then proceeds to the next screen."""

import sys
sys.path.append(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/backend")

import cv2
import face_matcher
import face_detector
import finger_to_option

import tkinter

from PIL import Image, ImageTk
from Timer import Timer

def identity_check_screen():
    """This function renderes the identity checking screen."""

    root = tkinter.Tk()
    root.title("Automated Ticketing System")

    bg_colour = "#2596be"

    root.configure(background=bg_colour)

    window_header = tkinter.Label(root, text="Identity Checking", font=('Helvetica', 30), fg='white', bg=bg_colour)
    window_header.grid(row=0, column=0, padx=10, pady=5)

    labelframe_for_video = tkinter.LabelFrame(root, bg=bg_colour)
    labelframe_for_video.grid(row=1, column=0)

    label_to_hold_video = tkinter.Label(labelframe_for_video, bg=bg_colour)
    label_to_hold_video.grid(row=0, column=0)

    label_to_display_user_details = tkinter.Label(root, bg=bg_colour, text='Looking for user', font=('Helvetica', 20), fg='white')
    label_to_display_user_details.grid(row=1, column=1, padx=5, pady=5)

    progress_label = tkinter.Label(root, bg=bg_colour, text='', font=('Helvetica', 20), fg='white')
    progress_label.grid(row=2, column=0, padx=10, pady=5)

    video_capture = cv2.VideoCapture(0)
    w_cam, h_cam = 640, 480
    video_capture.set(3, w_cam)
    video_capture.set(4, h_cam)
    timer = Timer(5, precision=0.1)
    face_timer = Timer(2)
    back_recv_counter = 0

    while True:
        _, cv2_img = video_capture.read()
        cv2_img_cpy = cv2_img.copy()
        cv2_img_cpy = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        cv2_img = cv2.flip(cv2_img, 1)

        

        cv2_img, co_ord = face_detector.detect_face(cv2_img)
        _, back_gesture, _ = finger_to_option.tip_touch_to_option(cv2_img_cpy, draw=False)
        if back_gesture == 3:
            back_recv_counter += 1
        
        if back_recv_counter >= 4:
            back_recv_counter = 0
            label_to_display_user_details.configure(text=f"Looking for user")
            timer.reset()
            face_timer.reset()

        frame = Image.fromarray(cv2_img)
        # frame = ImageTk.PhotoImage(frame)

        # if user_id != -1:
        if len(co_ord) > 0:
            face_timer.start()
        
        if face_timer.completed:
            frame.paste(Image.open(r"frontend/Assets/square_tick.png"), (572, 4))
            label_to_display_user_details.configure(text=f"User: Arina\nID: 1234567890")
            timer.start()

        frame = ImageTk.PhotoImage(frame)

        label_to_hold_video['image'] = frame

        if timer.running:
            # TODO: support Back button
            pass
        elif timer.completed:
            root.destroy()
            break
            # TODO: Implement Jumping to next screen

        root.update()


def testing():
    identity_check_screen()
