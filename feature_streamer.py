import pygame
from pygame.locals import *
import time
import numpy as np
from multiprocessing import Process, Queue, Pipe


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

def flight_detector(signal, threshold):
    if max(signal) >= threshold:
        return True
    else:
        return False

class Stamped_Feature():
    def __init__(self):
        self.stamp = 0
        self.dir = ''


class Feature_streamer(Process):
    def __init__(self, speedQueue, feature_width=80):
        '''
        This class is multiprocessing. It is used to stream on screen some feature for the stimulation of bee.
        :param speedQueue (Real): This queue is used to stream the moving speed of the feature if - to the left if + to the right
        :param feature_width (Int): The features are rectangle, this is their width
        '''
        super(Feature_streamer, self).__init__()
        self._running = True    #Flag for stopping program
        self._display_surf = None
        self.clock = pygame.time.Clock() #To see FPS
        self.size = self.width, self.height = 1280, 720
        self._time_previous = time.time()
        self._feature_offset = 0    # This value will be incremented or decremented in fonction of feature move
        self._feature_width = feature_width
        self._feature = np.array([])
        self.speed_queue = speedQueue
        self.feature_speed = 0

    def on_init(self):
        '''
        Simple initialisation of pyGame
        :return:
        '''
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size,
                                                     RESIZABLE)
        pygame.display.set_caption('featureDisplay')
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self, asked_speed):
        # Draw a solid rectangle
        # Give us a the point in pixel of begining for each feature
        index = np.arange(0, self.width + 4 * self._feature_width, self._feature_width)
        #Give a list of same length with one or zero alternate (black and white)
        black_or_white = [bool(i % 2) for i in range(len(index))]
        i=0
        offset = self.ask_feature_offset(speed=asked_speed)


        for ind in range(len(index)):
            if index[ind] - offset < 0:
                if ind < -self._feature_width:
                    continue
                else:
                    if black_or_white[ind]:
                        white_rect = pygame.Rect(0, 0, index[ind] - offset + self._feature_width,
                                                  self.height)
                        pygame.draw.rect(self._display_surf, (255, 255, 255), white_rect)
                        pygame.display.update(white_rect)
                    else:
                        black_rect = pygame.Rect(0, 0, index[ind] - offset + self._feature_width,
                                                  self.height)
                        pygame.draw.rect(self._display_surf, (0, 0, 0), black_rect)
                        pygame.display.update(black_rect)
            else:
                if black_or_white[ind]:
                    white_rect = pygame.Rect(index[ind] - offset, 0, self._feature_width,
                                             self.height)
                    pygame.draw.rect(self._display_surf, (255, 255, 255), white_rect)
                    pygame.display.update(white_rect)
                else:
                    black_rect = pygame.Rect(index[ind] - offset, 0, self._feature_width,
                                             self.height)
                    pygame.draw.rect(self._display_surf, (0, 0, 0), black_rect)
                    pygame.display.update(black_rect)
        self._time_previous = time.time()


    def on_render(self):
        pygame.display.flip()
        #pygame.time.wait(5)
        pass

    def on_cleanup(self):
        pygame.display.quit()
        pygame.quit()


    def ask_feature_offset(self, speed=-5., feature_width=50):
        delta_T = time.time() - self._time_previous
        self._feature_offset = self._feature_offset + 2 * feature_width * delta_T * speed

        if self._feature_offset >= self._feature_width * 2:
            self._feature_offset = 0.
        elif self._feature_offset <= 0.:
            self._feature_offset = self._feature_width * 2 - 1

        return self._feature_offset

    def run(self):
        if self.on_init() == False:
            self._running = False
        print("#######################################")
        print("### Features begins to be streamed  ###")
        print("#######################################")

        while (self._running):
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.on_cleanup()
                elif event.type == VIDEORESIZE:
                    self.size = self.width, self.height = event.dict['size']
                    self._display_surf = pygame.display.set_mode(event.dict['size'], RESIZABLE)
                    self.on_loop(self.feature_speed)
                    self.on_render()
            if self.speed_queue.full():
                self.feature_speed = self.speed_queue.get()

            self.on_loop(self.feature_speed)
            self.on_render()
        self.on_cleanup()

    def terminate(self):
        super(Feature_streamer, self).terminate()


if __name__ == "__main__":
    speedQueue = Queue(1)
    theApp = Feature_streamer(speedQueue)
    theApp.start()

    for i in range(100):
        try:
            speedQueue.put_nowait(10*np.sin(0.02*np.pi*i))
        except:
            pass
        time.sleep(0.1)
        print(i)

    theApp.terminate()