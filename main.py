import sys
import pygame
import time
from pygame.locals import *
from multiprocessing import Process, Queue, Manager
import field_streamer as fs
import camera_streamer as cs
import feature_streamer as feat
import gui_tools as gt
import tkinter as tk
import recorder as rec
import config

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

window = tk.Tk()
mywin = gt.MyWindow(window)
window.title('Hello Python')
window.geometry("400x200+10+10")

#Creation of fieldstreamer
field_queue = Queue(100)
field_streamer = fs.FieldStreamer(field_queue, stop_event, channels=config.channels, rate=config.sample_frequency, frames_per_buffer=config.buffer_size)
field_streamer.start()
field_stamped = fs.Stamped_field()

#Creation of camera streamer
image_queue = Queue(100)
image_streamer = cs.ImageStreamer(image_queue, stop_event, resolution=config.image_size, frame_rate=config.frame_rate)
image_streamer.start()
image_stamped = cs.Stamped_image()

#Creation of feature streamer
speedQueue = Queue(1)
feature_streamer = feat.Feature_streamer(speedQueue)
feature_streamer.start()

recorder = rec.Recorder(config.buffer_size, config.image_size)
recorder.create_new_file('Test')

monitor = gt.Monitoring(position=vumeter_position, size=vumeter_size)

time_previous = time.time()
while not stop_event.is_set():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            print("We quit and stop the threads")
            stop_event.set()
            pygame.quit()
            sys.exit(0)

    #update tkinter windows
    window.update_idletasks()
    window.update()

    # Read the data and calcualte the left and right levels
    try:
        image_stamped = image_queue.get(False)
        recorder.record_image(image_stamped)
        monitor.update_frame(image_stamped.image)
    except:
        pass

    try:
        #print(field_queue.qsize())
        field_stamped = field_queue.get(False)
        recorder.record_field(field_stamped)
        monitor.update_vumeter(field_stamped.field_left, field_stamped.field_right)
    except:
        pass
    #print(time.time() - time_previous)
    if time.time()-time_previous > 3:
        recorder.close_current_file()
        break
    #print(time.time() - time_previous)
    #time_previous = time.time()



