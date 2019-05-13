import io
import time
from multiprocessing import Process, Queue, Pipe
import threading
from matplotlib import pyplot as plt
import picamera
from PIL import Image

#class Imageandstamp(object):
#    def __init__(self.):


class ImageStreamer(Process):
    def __init__(self, streaming_queue, resolution=(640, 480), frame_rate=30):
        super(ImageStreamer, self).__init__()
        self.streaming_queue = streaming_queue
        self._camera = None
        self.frame_rate = frame_rate
        self.resolution = resolution
        self.raw_capture = io.BytesIO()
        # initialize the frame and the variable used to indicate
        # if the thread should be stopped

        self.stopped = False


    def terminate(self):
        self.stopped = True
        super(ImageStreamer, self).terminate()

    def run(self):
        self._camera = picamera.PiCamera()
        self._camera.resolution = self.resolution
        self._camera.framerate = self.frame_rate
        # Begin streaming
        self._camera.start_recording(self, format='mjpeg')
        print("yolo")

        while not self.stopped:
            self._camera.wait_recording(0.0001)
        self._camera.stop_recording()
        self._camera.close()

        return self

    def write(self, buf):
        # Start of new frame; close the old one (if any) and
        # open a new output
        print("yolo")
        if buf.startswith(b'\xff\xd8'):
            receive_time = time.time()
            self.raw_capture.seek(0)
            self.raw_capture.truncate()
            self.raw_capture.write(buf)
            PIL_image = Image.open(self.raw_capture)
            self.streaming_queue.put([PIL_image, receive_time])


if __name__ == "__main__":
    camera_queue = Queue(10)
    image_streamer = ImageStreamer(camera_queue)
    image_streamer.start()

    i = 0
    before = time.time()
    while i < 100:

        if not camera_queue.empty():
            i = i + 1

            image = camera_queue.get(True)
            print(image[1])
            print(i, 1/(time.time() - before))
            before = time.time()

    image.save('out.jpg')
    image_streamer.terminate()

