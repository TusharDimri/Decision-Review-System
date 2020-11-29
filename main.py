import tkinter # In built package

import PIL.Image, PIL.ImageTk # pip install pillow

import cv2 # pip install opencv-python

from functools import partial # this is used with command argument of button to give functio anme for button

import threading # This isused to prevent te blocking of mainloop while changing background image

import imutils # Used for resizing image (pip install imutils)

import time

stream = cv2.VideoCapture("clip.mp4")
flag = True

def play(speed):
    global flag
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)     
    
    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(134, 25, fill="red", font="Times 25 bold", text="Decision Pending")
    flag = not flag 


def pending(decision):
    # 1. Display Decision Pending Image
    # 2. Wait for 1 second
    # 3. Display Sponsor Image
    # 4. Wait for 1.5 seconds
    # 5. Display Decision Image
    # 6. Wait for 1.5 seconds
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    time.sleep(2)

    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    time.sleep(2)

    if decision == 'out':
        frame = cv2.cvtColor(cv2.imread("out.png"), cv2.COLOR_BGR2RGB)
        frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
        frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.image = frame
        canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    elif decision == 'notout':
        frame = cv2.cvtColor(cv2.imread("notout.png"), cv2.COLOR_BGR2RGB)
        frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
        frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.image = frame
        canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)



def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()


def notout():
    thread = threading.Thread(target=pending, args=("notout",))
    thread.daemon = 1
    thread.start()



# Width and Height of our main screen
SET_WIDTH = 650
SET_HEIGHT = 368
# Above variables are in upper case because they contain constant values

# Tkinter GUI starts here
window = tkinter.Tk()
window.title("Decision Review System by Tushar Dimri")
cv_img = cv2.cvtColor(cv2.imread("background.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width = SET_WIDTH, height = SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0 , anchor = tkinter.NW, image = photo)
canvas.pack()


# Buttons to control playback 
btn = tkinter.Button(window, text="<< Previous (fast)", width = 50,  command = partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (slow)", width = 50, command = partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next (fast) >>", width = 50, command = partial(play, +25))
btn.pack()

btn = tkinter.Button(window, text="Next (slow) >>", width = 50, command = partial(play, +2))
btn.pack()

btn = tkinter.Button(window, text="Out", width = 50, command = out)
btn.pack()

btn = tkinter.Button(window, text="Not Out", width = 50, command = notout)
btn.pack()

window.mainloop()