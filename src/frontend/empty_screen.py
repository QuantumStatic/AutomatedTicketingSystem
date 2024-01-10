"""This file creates the screen before the booking process starts."""

import tkinter
import cv2

import sys
sys.path.append(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/backend")

import finger_to_option
from Timer import Timer

from PIL import Image, ImageTk

def empty_screen():
    """This Function renderes the empty screen."""

    root = tkinter.Tk()
    root.title("Automated Ticketing System")

    bg_colour = "#2596be"

    root.configure(background=bg_colour)

    window_header = tkinter.Label(root, text="Are you ready to start?", font=('Helvetica', 30), fg='white', bg=bg_colour)
    window_header.grid(row=0, column=0, padx=10, pady=5)

    labelframe_for_video = tkinter.LabelFrame(root, bg=bg_colour)
    labelframe_for_video.grid(row=1, column=0)

    label_to_hold_video = tkinter.Label(labelframe_for_video, bg=bg_colour)
    label_to_hold_video.grid(row=0, column=0)

    progress_label = tkinter.Label(root, bg=bg_colour, text='Waiting for User', font=('Helvetica', 20), fg='white')
    progress_label.grid(row=2, column=0, padx=10, pady=5)

    video_capture = cv2.VideoCapture(0)
    w_cam, h_cam = 640, 480
    video_capture.set(3, w_cam)
    video_capture.set(4, h_cam)

    start_timer = Timer(2, precision=0.1)
    next_window_timer = Timer(5, precision=0.1)
    back_recv_counter = 0

    while True:
        progress_label.configure(text='Waiting for User')
        _, cv2_img = video_capture.read()
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        cv2_img = cv2.flip(cv2_img, 1)

        cv2_img, thumbs_up = finger_to_option.check_thumbs_up(cv2_img)
        _, back_gesture, _ = finger_to_option.tip_touch_to_option(cv2_img, draw=False)
        if thumbs_up and not start_timer.running:
            start_timer.start()
        
        if back_gesture == 3:
            back_recv_counter += 1
        
        print(back_recv_counter)
        
        if back_recv_counter >= 4:
            back_recv_counter = 0
            progress_label.configure(text='Back Gesture Detected')
            start_timer.reset()
            next_window_timer.reset()

        frame = Image.fromarray(cv2_img)

        if start_timer.completed:
            frame.paste(Image.open(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/frontend/Assets/square_tick.png"), (572, 4))
            next_window_timer.start()
            progress_label.configure(text='Starting Booking Process')

        frame = ImageTk.PhotoImage(frame)

        label_to_hold_video['image'] = frame

        if next_window_timer.completed:
            root.destroy()
            break

        root.update()


def testing():
    empty_screen()
