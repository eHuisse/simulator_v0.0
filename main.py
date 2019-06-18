import sys
import pygame
import time
from pygame.locals import *
from multiprocessing import Process, Queue, Manager
import field_streamer as fs
import camera_streamer as cs
import serial_streamer as ss
import feature_streamer as feat
import gui_tools as gt
import tkinter as tk
import recorder as rec
import config
import random as rand
import traceback

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

#Creation of fieldstreamer
field_queue = Queue(100)
field_streamer = fs.FieldStreamer(field_queue, stop_event, channels=config.channels, rate=config.sample_frequency, frames_per_buffer=config.buffer_size)
field_streamer.deamon = True
field_streamer.start()
field_stamped = fs.Stamped_field()

#Creation of camera streamer
image_queue = Queue(100)
image_streamer = cs.ImageStreamer(image_queue, stop_event, resolution=config.image_size, frame_rate=config.frame_rate)
image_streamer.deamon = True
image_streamer.start()
image_stamped = cs.Stamped_image()

serial_queue = Queue(100)
serial_streamer = ss.SerialStreamer(serial_queue, stop_event, config.serial_port, config.baudrate)
serial_streamer.deamon = True
serial_streamer.start()
serial_stamped = ss.Stamped_serial()

#Creation of feature streamer
feature_queue = Queue(1)
feature_streamer = feat.Feature_streamer(feature_queue)
feature_streamer.deamon = True
feature_streamer.start()
feature_stamped = feat.Stamped_Feature()

#Initialisation of the recorder
recorder = rec.Recorder(config.buffer_size, config.image_size)

#Initialisation of the tkinter windows
window = tk.Tk()
mywin = gt.MyWindow(window, recorder)
window.title('Hello Python')
window.geometry("400x250+10+10")

#Initialisation of vu meter
monitor = gt.Monitoring(position=vumeter_position, size=vumeter_size)

time_previous = time.time()
time_previous_feature = time.time()

while not stop_event.is_set():
    try:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                print("We quit and stop the threads")
                stop_event.set()
                field_streamer.terminate()
                image_streamer.terminate()
                feature_streamer.terminate()
                field_streamer.join()
                image_streamer.join()
                serial_streamer.join()
                feature_streamer.join()
                pygame.quit()
                sys.exit(0)

        #update tkinter windows
        window.update_idletasks()
        window.update()

        # Read the data and calcualte the left and right levels
        try:
            image_stamped = image_queue.get(False)
            if mywin.fsm.isstate('recording'):
                monitor.is_recording = True
                recorder.record_image(image_stamped)
                #print(time.time()-time_previous)
            else:
                monitor.is_recording = False
            monitor.update_frame(image_stamped.image)
        except:
            pass

        try:
            field_stamped = field_queue.get(False)
            if mywin.fsm.isstate('recording'):
                monitor.is_recording = True
                recorder.record_field(field_stamped)
            else:
                monitor.is_recording = False
            monitor.update_vumeter(field_stamped.field_left, field_stamped.field_right)
        except:
            pass

        try:
            serial_stamped = serial_queue.get(False)
            monitor.update_direction(serial_stamped.left, serial_stamped.right)
            if mywin.fsm.isstate('recording'):
                monitor.is_recording = True
                recorder.record_serial(serial_stamped)
            else:
                pass
        except:
            pass

        try:
            if time.time() - time_previous_feature > config.features_toogle_period:
                time_previous_feature = time.time()
                right_or_left = rand.sample(["right", "left"], 1)[0]
                if right_or_left == "right":
                    feature_queue.put(-config.feature_speed)
                else:
                    feature_queue.put(config.feature_speed)

                feature_stamped.stamp = time.time()
                feature_stamped.dir = right_or_left
                recorder.record_feature(feature_stamped)
            else:
                pass
        except:
            pass
    except Exception as e:
        traceback.print_exc(e)
        stop_event.set()
        field_streamer.terminate()
        image_streamer.terminate()
        feature_streamer.terminate()
        field_streamer.join()
        image_streamer.join()
        serial_streamer.join()
        feature_streamer.join()
        pygame.quit()
        sys.exit(0)

    time_previous = time.time()
    #time_previous = time.time()



