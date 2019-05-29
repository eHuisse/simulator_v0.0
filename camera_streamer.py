import io
import time
from multiprocessing import Process, Queue, Pipe
import cv2

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
        self._camera = cv2.VideoCapture(0)
        if not self._camera.read()[0]:
            self._camera = cv2.VideoCapture(1)
            if not self._camera.read()[0]:
                raise("Camera not conected")

        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        self._camera.set(cv2.CAP_PROP_FPS, self.frame_rate)
        self._camera.set(cv2.CAP_PROP_EXPOSURE, 20)

        #self._camera.resolution = self.resolution
        #self._camera.framerate = self.frame_rate
        # Begin streaming
        # self._camera.start_recording(self, format='mjpeg')

        while not self.stopped:
            receive_time = time.time()
            _, frame = self._camera.read()
            self.streaming_queue.put([frame, receive_time])
            cv2.waitKey(1)

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
    camera_queue = Queue(10)
    image_streamer = ImageStreamer(camera_queue)
    image_streamer.start()

    i = 0
    before = time.time()
    while i < 100:

        if not camera_queue.empty():
            i = i + 1

            image = camera_queue.get(True)
            print("FPS : " + str(1/(time.time() - before)))
            before = time.time()
            cv2.imshow('frame', image[0])
            cv2.waitKey(1)

    image_streamer.terminate()

