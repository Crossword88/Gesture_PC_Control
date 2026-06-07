from threading import Thread
from time import sleep

from matplotlib.pyplot import imshow
from ultralytics import YOLO
import torch
import cv2

import win32con
import win32api
import time
import numpy as np
import threading
import ctypes
import time
import win32api
import sys
from pathlib import Path
import threading

import ctypes

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def get_mouse_pos():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

VOLUME_GESTURE = 0
RIGHT_MOUSE = 1
UP_MOUSE = 2
LEFT_MOUSE = 3
DOWN_MOUSE = 4
CLICK = 5

MOUSEEVENTF_MOVE = 0x0001

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

model = YOLO(r"C:\Models\Gesture_Controller_YOLO\Gesture_Model_26n13\weights\best.engine")

def show():
    while True:
        if window_frame is None: continue

        final_frame = window_frame.copy()


        rgb = 0, 0, 0
        if CLASS == 0: rgb = 0,255,0
        elif CLASS == 1: rgb = 0,255,100
        elif CLASS == 2: rgb = 200,0,200
        elif CLASS == 3: rgb = 0,0,255
        elif CLASS == 4: rgb = 100,115,0


        if CLASS is not None:
            label = f"{model.names[int(CLASS)]} {float(CONFIDENCE):.2f}"
            x1, y1, x2, y2 = [int(v.cpu().item()) for v in BBOX]
            cv2.rectangle(final_frame, (width - x1, y1), (width - x2, y2), (rgb), 2)      #flipped frame, convert box to the other side
            cv2.putText(final_frame, label, (width - x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (rgb), 2)


        cv2.imshow("cam", final_frame)
        c = cv2.waitKey(1)
        if c == 27:
            break

    cv2.destroyAllWindows()



def controller():
    while True:
        sleep(0.0001)

        if CLASS == VOLUME_GESTURE:
            ctypes.windll.user32.SetCursorPos(int(1400-(int(gesture_center_X) * 1.25)), int(gesture_center_Y) + 10)        #simle formula, there is ~1400px for max X mouse coordinate, and ~1200px for gesture max center X coordinate

        elif CLASS == CLICK:
            fast_click()
            sleep(0.3)



def fast_click():
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # Минимальная пауза, чтобы игра засчитала клик
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def watcher():
    global window_frame, cap, CLASS, BBOX, CONFIDENCE
    CLASS = None
    window_frame = None

    cap = cv2.VideoCapture(0)
    cap.set(3, 1920)
    cap.set(4, 1080)

    global width, height
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # реальная ширина
    print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # реальная высота

    # camering = threading.Thread(target = shower, args=(cap,), daemon=True)
    # camering.start()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 30, (width, height))

    Thread(target=show, args=(), daemon=True).start()

    Thread(target=controller, args=(), daemon=True).start()

    global gesture_center_X, gesture_center_Y

    while True:
        ret, frame = cap.read()
        frame_to_model = cv2.cvtColor(np.array(frame,), cv2.COLOR_BGRA2BGR)
        #out.write(frame)
        window_frame = cv2.flip(frame, 1)

        CLASS = None

        result = model.predict(frame_to_model, conf = 0.4, device = 'cuda', verbose = False)[0]
        for box, cls, conf  in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
            x1, y1, x2, y2 = box

            if cls == VOLUME_GESTURE:
                gesture_center_Y = (y1 + y2) / 2
                gesture_center_X = (x1 + x2) / 2
                # print("X: ", int(gesture_center_X), " Y: ", int(gesture_center_Y))
                # print("Mouse: ", get_mouse_pos())



            CLASS = cls
            BBOX = box
            CONFIDENCE = conf

    out.release()
    cap.release()


if __name__ == '__main__':
    watcher()