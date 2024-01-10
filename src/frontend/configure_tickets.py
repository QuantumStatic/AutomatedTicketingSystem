"""This file creates the screen where we count the number of tickets."""

import sys
sys.path.append(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/backend")

import cv2
import tkinter
import finger_to_option
import constants
import ticket
import time

from PIL import Image, ImageTk, ImageDraw2
from Timer import Timer
from typing import *


def draw_marks_on_hand(locs:tuple, frame):
    if locs[3][1] > locs[0][1]: # Vertical Hand
        frame.paste(Image.open(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/frontend/Assets/a.png"), (locs[0][0]-8, locs[0][1]-35))
        frame.paste(Image.open(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/frontend/Assets/b.png"), (locs[1][0]-12, locs[1][1]-35))
        frame.paste(Image.open(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/frontend/Assets/c.png"), (locs[2][0]-15, locs[2][1]-35))
        frame.paste(Image.open(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/frontend/Assets/d.png"), (locs[3][0]-10, locs[3][1]-35))
    else:   # Horizontal Hand
        if locs[0][0] > locs[3][0]: #Left Hand
            frame.paste(Image.open(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/frontend/Assets/a.png"), (locs[0][0]+15, locs[0][1]-10))
            frame.paste(Image.open(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/frontend/Assets/b.png"), (locs[1][0]+15, locs[1][1]-12))
            frame.paste(Image.open(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/frontend/Assets/c.png"), (locs[2][0]+15, locs[2][1]-15))
            frame.paste(Image.open(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/frontend/Assets/d.png"), (locs[3][0]+15, locs[3][1]-10))
        else: # Right Hand
            frame.paste(Image.open(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/frontend/Assets/a.png"), (locs[0][0]-35, locs[0][1]-10))
            frame.paste(Image.open(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/frontend/Assets/b.png"), (locs[1][0]-35, locs[1][1]-12))
            frame.paste(Image.open(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/frontend/Assets/c.png"), (locs[2][0]-35, locs[2][1]-15))
            frame.paste(Image.open(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/frontend/Assets/d.png"), (locs[3][0]-35, locs[3][1]-15))

    return frame



def ticket_config_screen():
    """This function renderes the number counting screen."""

    root = tkinter.Tk()
    root.title("Automated Ticketing System")

    bg_colour = "#2596be"

    root.configure(background=bg_colour)

    window_header = tkinter.Label(root, text="Ticket Type Summary", font=('Helvetica', 30), fg='white', bg=bg_colour)
    window_header.grid(row=0, column=0, padx=10, pady=5)

    labelframe_for_video = tkinter.LabelFrame(root, bg=bg_colour)
    labelframe_for_video.grid(row=1, column=0)

    label_to_hold_video = tkinter.Label(labelframe_for_video, bg=bg_colour)
    label_to_hold_video.grid(row=0, column=0)

    frame_to_display_num_tickets = tkinter.Frame(root, bg=bg_colour)
    frame_to_display_num_tickets.grid(row=1, column=1, padx=5, pady=5)

    # Ticket info space
    ticket_rows = [tkinter.Label(frame_to_display_num_tickets, text=f"Tickets", font=('Helvetica', 20), fg='white', bg=bg_colour)]
    ticket_rows[0].grid(row=1, column=0, padx=5, pady=5)
    for x in range(5):
        ticket_rows.append(tkinter.Label(frame_to_display_num_tickets, font=('Helvetica', 16), fg='white', bg=bg_colour))
        ticket_rows[-1].grid(row=x+2, column=0, padx=5, pady=5)
    ticket_rows.append(tkinter.Label(frame_to_display_num_tickets, font=('Helvetica', 20), fg='white', bg=bg_colour))
    ticket_rows[-1].grid(row=constants.TICKETS_REQUESTED+2, column=0, padx=5, pady=5)

    # Issue tickets
    # TODO: get user type of tickets
    tickets = [ticket.get_ticket_by_name("Standard") for _ in range(constants.TICKETS_REQUESTED)]
    
    # Dynamic labels to display ticket settings
    for x in range(constants.TICKETS_REQUESTED):
        if x == 0:
            ticket_rows[x+1].configure(text=f"{tickets[x].name}: ${tickets[x].price}")
        else:
            ticket_rows[x+1].configure(text=f"{chr(64+x)}. {tickets[x].name}: ${tickets[x].price}")
    ticket_rows[-1].configure(text=f"Total: ${sum((ticket.price for ticket in tickets))}")
    
    # Build Progress Label
    progress_label = tkinter.Label(root, bg=bg_colour, text='', font=('Helvetica', 20), fg='white')
    progress_label.grid(row=2, column=0, padx=10, pady=5)

    # Preparing for video capture
    video_capture = cv2.VideoCapture(0)
    w_cam, h_cam = 640, 480
    video_capture.set(3, w_cam)
    video_capture.set(4, h_cam)

    # Creating Timers & other variables
    confirmation_timer = Timer(5)
    hand_opt_persist_timer = Timer(2.5, precision=0.05)
    type_choser_timer = Timer(2.5, precision=0.05)

    init_opt_chosen: 'Literal[0]' = -1
    init_ticket_opt_chosen: 'Literal[0]' = -1

    ticket_idx = 1

    pause_here, flag = False, True
    while True:
        _, cv2_img = video_capture.read()
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        cv2_img = cv2.flip(cv2_img, 1)

        if not confirmation_timer.running and not confirmation_timer.completed and not hand_opt_persist_timer.completed:

            for x in range(constants.TICKETS_REQUESTED):
                if x == 0:
                    ticket_rows[x+1].configure(text=f"{tickets[x].name}: ${tickets[x].price}")
                else:
                    ticket_rows[x+1].configure(text=f"{chr(64+x)}. {tickets[x].name}: ${tickets[x].price}")
            ticket_rows[0].configure(text=f"Tickets")
            
            cv2_img, opt_chosen, locs = finger_to_option.tip_touch_to_option(cv2_img)

            if opt_chosen != -1 and not hand_opt_persist_timer.completed:
                if hand_opt_persist_timer.running:
                    if opt_chosen != init_opt_chosen and opt_chosen < constants.TICKETS_REQUESTED-1:
                        hand_opt_persist_timer.restart()
                        ticket_rows[init_opt_chosen+2].config(font=('Helvetica', 16))
                        ticket_rows[opt_chosen+2].config(font=('Helvetica', 18))
                else:
                    hand_opt_persist_timer.start()
                init_opt_chosen = opt_chosen
            elif opt_chosen == -1:
                cv2_img, thumbs_up = finger_to_option.check_thumbs_up(cv2_img, draw=False)
                if thumbs_up:
                    confirmation_timer.start()

            frame = Image.fromarray(cv2_img)
            
            try:
                frame = draw_marks_on_hand(locs, frame)
            except IndexError:
                pass

            flag = True

        elif not confirmation_timer.running and hand_opt_persist_timer.completed:

            if flag:
                ticket_rows[0].configure(text='Loading Ticket Options')
                for x in range(constants.TICKETS_REQUESTED):
                    ticket_rows[x+1].configure(text='')
                ticket_rows[-1].configure(text='')
                flag = False
                pause_here = True
                frame = Image.fromarray(cv2_img)
            else:
                ticket_rows[0].config(text="Change ticket type")

                ticks = tickets[init_opt_chosen+1].get_other_ticket_types()
                for idx, tick in enumerate(ticks):
                    ticket_rows[idx+1].configure(text=f"{chr(65+idx)}. {tick.name}: ${tick.price}", font=('Helvetica', 16))
                
                if init_ticket_opt_chosen >= 0:
                    ticket_rows[init_ticket_opt_chosen+1].config(font=('Helvetica', 18))

                cv2_img, ticket_opt_chosen, locs = finger_to_option.tip_touch_to_option(cv2_img)
                if ticket_opt_chosen >= 0 and not type_choser_timer.completed:
                    if type_choser_timer.running:
                        if ticket_opt_chosen != init_ticket_opt_chosen and ticket_opt_chosen < len(ticks)-1:
                            type_choser_timer.restart()
                            ticket_rows[init_ticket_opt_chosen+1].config(font=('Helvetica', 16))
                            ticket_rows[ticket_opt_chosen+1].config(font=('Helvetica', 18))
                    else:
                        type_choser_timer.start()
                    init_ticket_opt_chosen = ticket_opt_chosen
                elif type_choser_timer.completed:
                    tickets[init_opt_chosen+1] = ticket.get_ticket_by_name(ticks[init_ticket_opt_chosen].type)
                    hand_opt_persist_timer.reset()
                    type_choser_timer.reset()
                    init_opt_chosen = -1
                    init_ticket_opt_chosen = -1
                    for x in range(5):
                        ticket_rows[x+1].config(font=('Helvetica', 16), text="")
                    ticket_rows[0].config(text="Going back to tickets")
                    pause_here = True
                    ticket_rows[-1].configure(text=f"Total: ${sum((ticket.price for ticket in tickets))}")

                frame = Image.fromarray(cv2_img)
                try:
                    frame = draw_marks_on_hand(locs, frame)
                except IndexError:
                    pass

        elif confirmation_timer.running:
            #TODO: Implement back button
            frame = Image.fromarray(cv2_img)
            # frame = ImageDraw2.Draw(frame)
            # frame.text((w_cam//2, h_cam//2), "Confirm", fill="white", font=("Helvetica", 20))
            frame.paste(Image.open(r"/Users/utkarsh/Desktop/Utkarsh/College/Year 4/Semester 1/Multimodal Interface Design/Group Report/Project/src/frontend/Assets/square_tick.png"), (572, 4))
        elif confirmation_timer.completed:
            root.destroy()
            break
            # TODO: Implement Jumping to next screen

        frame = ImageTk.PhotoImage(frame)
        label_to_hold_video['image'] = frame
        root.update()
        if pause_here:
            time.sleep(2)
            pause_here = False

def ticket_config_screen_test():
    ticket_config_screen()
