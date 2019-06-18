import io
import time
from multiprocessing import Process, Queue, Pipe, Manager
import cv2
import numpy as np
import sys
import glob
import serial
import config

class Stamped_serial():
    def __init__(self):
        self.left = False
        self.right = False
        self.time_stamp = 0

    def __str__(self):
        return str(self.time_stamp) + " :: dataleft : " + str(self.left) + " ; dataright : " + str(self.right)

class SerialStreamer(Process):
    def __init__(self, serial_queue, stop_event, port, baudrate):
        super(SerialStreamer, self).__init__()
        self.ser = serial.Serial(port, baudrate)
        self.serial_stamped = Stamped_serial()
        self.serial_queue = serial_queue
        self.stop_event = stop_event

    def parser(self, data, timestamp):
        data = data.replace('\n', '')
        data = data.replace('\r', '')
        data = data.split(";")
        if data[0] == "0":
            self.serial_stamped.left = False
        else:
            self.serial_stamped.left = True
        if data[1] == "0":
            self.serial_stamped.right = False
        else:
            self.serial_stamped.right = True
        self.serial_stamped.time_stamp = timestamp

    def run(self):
        print("#######################################")
        print("### Direction begins to be streamed  ##")
        print("#######################################")
        while not self.stop_event.is_set():
            line = self.ser.readline().decode('utf-8', 'slashescape')
            timenow = time.time()
            self.parser(line, timenow)
            self. serial_queue.put(self.serial_stamped)



if __name__ == '__main__':
    manager = Manager()
    stop_event = manager.Event()

    serial_queue = Queue(10)

    serial_stream = SerialStreamer(serial_queue, stop_event, config.serial_port, config.baudrate)
    serial_stream.deamon = True

    serial_stream.start()

    while True:
        print(serial_queue.get())