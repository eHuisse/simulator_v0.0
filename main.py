#!/usr/bin/python
# VU meter written in Python (www.python.org) by Tim Howlett 1st April 2013,
# Does not work with Python 2.7.3 or 2.7.4 Does work with 3.2.3
# Requires the Pygame module (www.pygame.org)and the Pyaudio module (http://people.csail.mit.edu/hubert/pyaudio/)

import sys
import pygame
import time
from pygame.locals import *
from multiprocessing import Process, Queue, Manager
import field_streamer as fs
import camera_streamer as cs
import gui_tools as gt
import tkinter as tk


# set up a bunch of constants
BGCOLOR = (0, 0, 0)
WINDOWWIDTH = 770
WINDOWHEIGHT = 480
PeakL = 0
PeakR = 0
vumeter_size = [130, 480]
vumeter_position = [640, 0]

#Manager for all the process
manager = Manager()
stop_event = manager.Event()

# setup code
pygame.init()
pygame.mixer.quit()  # stops unwanted audio output on some computers
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), HWSURFACE)
pygame.display.set_caption('VU Meter')

window = tk.Tk()
mywin = gt.MyWindow(window)
window.title('Hello Python')
window.geometry("400x200+10+10")

#Creation of fieldstreamer
field_queue = Queue(10)
field_streamer = fs.FieldStreamer(field_queue, stop_event)
field_streamer.start()

#Creation of camera streamer
image_queue = Queue(10)
image_streamer = cs.ImageStreamer(image_queue, stop_event)
image_streamer.start()

vumeter = gt.Vu_meter(DISPLAYSURF, position=vumeter_position, size=vumeter_size)

time_previous = time.time()
while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            stop_event.set()
            pygame.quit()
            sys.exit(0)

    #update tkinter windows
    window.update_idletasks()
    window.update()

    # Read the data and calcualte the left and right levels
    try:
        image = image_queue.get(False)
        gt.frame_show(image[0], DISPLAYSURF)
    except:
        pass

    try:
        field = field_queue.get(False)
        time_previous = time.time()
        vumeter.update(field)
    except:
        pass



