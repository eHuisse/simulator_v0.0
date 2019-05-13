import pygame
from pygame.locals import *
import time
import numpy as np
from matplotlib import pyplot as plt


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)



class App:
    def __init__(self, feature_width=50):
        self._running = True
        self._display_surf = None
        self.clock = pygame.time.Clock()
        self.size = self.width, self.height = 1280, 720
        self._time_previous = time.time()
        self._feature_offset = 0
        self._feature_width = feature_width
        self._feature = np.array([])

        self.change_feature(self._feature_width)

    def change_feature(self, feature_width):
        self._feature_width = feature_width
        new_width = int(self.width // (2 * self._feature_width) + 2) * (2 * self._feature_width)
        self._feature = np.zeros((new_width, self.height, 3))
        white = np.array([255, 255, 255])

        for i in range(new_width):
            modulo_step = i % (2 * self._feature_width)
            if modulo_step < self._feature_width:
                self._feature[i, :, :] = white

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size,
                                                     RESIZABLE)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        # Draw a solid rectangle
        index = np.arange(0, self.width + 4 * self._feature_width, self._feature_width)
        black_or_white = [bool(i % 2) for i in range(len(index))]
        i=0
        offset = self.ask_feature_offset()


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

        # while i < int(self.width // (2 * self._feature_width) + 1):
        #     white_rect = pygame.Rect(i*self._feature_width*2 + offset, 0, self._feature_width, self.height)
        #     pygame.draw.rect(self._display_surf, (255, 255, 255), white_rect)
        #     pygame.display.update(white_rect)
        #     black_rect = pygame.Rect((2 * i + 1) * self._feature_width + offset, 0, self._feature_width, self.height)
        #     pygame.draw.rect(self._display_surf, (0, 0, 0), black_rect)
        #     pygame.display.update(black_rect)
        #     i = i + 1


        self._time_previous = time.time()


    def on_render(self):
        pygame.display.flip()
        #pygame.time.wait(5)
        pass

    def on_cleanup(self):
        pygame.quit()

    def ask_feature_offset(self, colors = (255, 255, 255), speed=-5., feature_width=50):
        delta_T = time.time() - self._time_previous
        self._feature_offset = self._feature_offset + 2 * feature_width * delta_T * speed
        #
        #self._feature_offset = self._feature_offset - 1

        if self._feature_offset >= self._feature_width * 2:
            self._feature_offset = 0.
        elif self._feature_offset <= 0.:
            self._feature_offset = self._feature_width * 2 - 1

        return self._feature_offset

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
                elif event.type == VIDEORESIZE:
                    self.size = self.width, self.height = event.dict['size']
                    self._display_surf = pygame.display.set_mode(event.dict['size'], RESIZABLE)
                    self.change_feature(self._feature_width)
                    self.on_loop()
                    self.on_render()

            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
