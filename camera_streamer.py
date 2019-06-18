import io
import time
from multiprocessing import Process, Queue, Pipe, Manager
import cv2
import numpy as np


class Stamped_image():
    def __init__(self):
        self.image = np.array([])
        self.time_stamp = 0

class ImageStreamer(Process):
    def __init__(self, streaming_queue, stop_event, resolution=(640, 480), frame_rate=30):
        super(ImageStreamer, self).__init__()
        self.streaming_queue = streaming_queue
        self._camera = None
        self.frame_rate = frame_rate
        self.resolution = resolution
        self.raw_capture = io.BytesIO()
        # initialize the frame and the variable used to indicate
        # if the thread should be stopped

        self._image = Stamped_image()
        self.stop_event = stop_event


    def terminate(self):
        super(ImageStreamer, self).terminate()

    def run(self):
        for i in range(10):
            self._camera = cv2.VideoCapture(i)
            if self._camera.isOpened():
                break
        if not self._camera.isOpened():
            raise("Camera not detected")

        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        self._camera.set(cv2.CAP_PROP_FPS, self.frame_rate)
        self._camera.set(cv2.CAP_PROP_EXPOSURE, 20)

        #self._camera.resolution = self.resolution
        #self._camera.framerate = self.frame_rate
        # Begin streaming
        # self._camera.start_recording(self, format='mjpeg')
        print("#######################################")
        print("####  Image begins to be streamed  ####")
        print("#######################################")
        while not self.stop_event.is_set():
            receive_time = time.time()

            _, frame = self._camera.read()

            self._image.time_stamp = receive_time
            self._image.image = frame
            try:
                self.streaming_queue.put_nowait(self._image)
            except:
                pass
            cv2.waitKey(1)

        self.terminate()
        self._camera.release()

        return self

    # def write(self, buf):
    #     # Start of new frame; close the old one (if any) and
    #     # open a new output
    #     print("yolo")
    #     if buf.startswith(b'\xff\xd8'):
    #         receive_time = time.time()
    #         self.raw_capture.seek(0)
    #         self.raw_capture.truncate()
    #         self.raw_capture.write(buf)
    #         PIL_image = Image.open(self.raw_capture)
    #         self.streaming_queue.put([PIL_image, receive_time])


if __name__ == "__main__":
    manager = Manager()
    stop_event = manager.Event()

    camera_queue = Queue(10)
    image_streamer = ImageStreamer(camera_queue, stop_event)
    image_streamer.start()

    i = 0
    before = time.time()
    while i < 100:

        if not camera_queue.empty():
            i = i + 1

            image = camera_queue.get(True)
            print("FPS : " + str(1/(time.time() - before)))
            before = time.time()
            cv2.imshow('frame', image.image)
            cv2.waitKey(1)

    image_streamer.terminate()

