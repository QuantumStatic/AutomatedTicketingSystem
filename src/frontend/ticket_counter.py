"""This file creates the screen where we count the number of tickets."""

import sys
sys.path.append(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/backend")

import cv2
import tkinter
import finger_to_option
import constants

from myfunctions_compat import execute_this
from PIL import Image, ImageTk
from Timer import Timer
from typing import *
from configure_tickets import ticket_config_screen

def num_tickets_screen():
    """This function renderes the number counting screen."""

    root = tkinter.Tk()
    root.title("Automated Ticketing System")

    bg_colour = "#2596be"

    root.configure(background=bg_colour)

    window_header = tkinter.Label(root, text="How many tickets do you want?", font=('Helvetica', 30), fg='white', bg=bg_colour)
    window_header.grid(row=0, column=0, padx=10, pady=5)

    labelframe_for_video = tkinter.LabelFrame(root, bg=bg_colour)
    labelframe_for_video.grid(row=1, column=0)

    label_to_hold_video = tkinter.Label(labelframe_for_video, bg=bg_colour)
    label_to_hold_video.grid(row=0, column=0)

    label_to_display_num_tickets = tkinter.Label(root, bg=bg_colour, text='Determining Tickets', font=('Helvetica', 20), fg='white')
    label_to_display_num_tickets.grid(row=1, column=1, padx=5, pady=5)

    progress_label = tkinter.Label(root, bg=bg_colour, text='Waiting for User', font=('Helvetica', 20), fg='white')
    progress_label.grid(row=2, column=0, padx=10, pady=5)

    video_capture = cv2.VideoCapture(0)
    w_cam, h_cam = 640, 480
    video_capture.set(3, w_cam)
    video_capture.set(4, h_cam)
    confirmation_timer = Timer(5, precision=0.1)
    hand_num_persist_timer = Timer(3, precision=0.05)

    init_num_chosen: Literal[0] = 0
    back_timer = Timer(1.5)

    while True:
        _, cv2_img = video_capture.read()
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        cv2_img = cv2.flip(cv2_img, 1)

        if not confirmation_timer.running and not confirmation_timer.completed:
            cv2_img, num_chosen = finger_to_option.number_from_finger(cv2_img)
            _, back_gesture, _ = finger_to_option.tip_touch_to_option(cv2_img, draw=False)

            if num_chosen != 0 and not hand_num_persist_timer.completed:
                # print(num_chosen)
                if hand_num_persist_timer.running:
                    if num_chosen != init_num_chosen:
                        hand_num_persist_timer.reset()
                        init_num_chosen = num_chosen
                        plural = "" if init_num_chosen == 1 else "s"
                        label_to_display_num_tickets.configure(text=f"{init_num_chosen} ticket{plural}")
                else:
                    init_num_chosen = num_chosen
                    hand_num_persist_timer.start()

            frame = Image.fromarray(cv2_img)
            if hand_num_persist_timer.completed:
                confirmation_timer.start()
                plural = "" if init_num_chosen == 1 else "s"
                label_to_display_num_tickets.configure(text=f"{init_num_chosen} ticket{plural}")
                
            frame = ImageTk.PhotoImage(frame)

            label_to_hold_video['image'] = frame

        elif confirmation_timer.running:
            _, back_gesture, _ = finger_to_option.tip_touch_to_option(cv2_img, draw=True)
            if back_gesture == 3:
                back_timer.start()
            

            if back_timer.completed:
                # back_recv_counter = 0
                label_to_display_num_tickets.configure(text='Determining Tickets')
                hand_num_persist_timer.reset()
                confirmation_timer.reset()
                back_timer.reset()

            frame = Image.fromarray(cv2_img)
            frame.paste(Image.open(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/frontend/Assets/square_tick.png"), (572, 4))
            frame = ImageTk.PhotoImage(frame)
            label_to_hold_video['image'] = frame
        elif confirmation_timer.completed:
            constants.TICKETS_REQUESTED = init_num_chosen
            root.destroy()
            # ticket_config_screen()
            break

        root.update()


@execute_this
def num_tickets_screen():
    num_tickets_screen()