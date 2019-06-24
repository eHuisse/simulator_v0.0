import pygame
import numpy as np
import time

class PGOscilloscope():
    def __init__(self, display_surf, size=(100, 100), position=(0, 0), max_value=0.5):
        self.display_surf = display_surf
        self.size = size
        self.position = position
        self.max_value = max_value
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

    def update(self, left=0, right=0):
        pygame.draw.rect(self.display_surf, self.BLACK, [self.position[0], self.position[1], self.size[0], self.size[1]])
        pygame.draw.lines(self.display_surf, self.WHITE, False, [[self.position[0],
                                                           self.position[1] + self.size[1]//2],
                                                          [self.position[0] + self.size[0],
                                                           self.position[1] + self.size[1]//2]], 1)
        left = self.shape_it_shape_it(left)
        right = self.shape_it_shape_it(right)
        #print(left)
        pygame.draw.aalines(self.display_surf, self.RED, False, left, 1)
        pygame.draw.aalines(self.display_surf, self.GREEN, False, right, 1)

        pygame.display.flip()

    def shape_it_shape_it(self, arr):

        def scale_it_scale_it(coord):
            coord[:, 1] = -(coord[:, 1] / self.max_value) * self.size[1] / 2 + self.size[1] / 2 + self.position[1]
            coord = coord.tolist()
            return coord

        if arr.shape[0] > self.size[0]:
            sample_windows_size = arr.shape[0] // self.size[0]
            subsampled = []
            for i in range(self.size[0]):
                begin = i * sample_windows_size
                if i == self.size[0]:
                    subsampled.append(arr[-1])
                subsampled.append(arr[begin])
            ord = range(self.position[0], self.size[0] + self.position[0])
            return scale_it_scale_it(np.array([ord, subsampled]).transpose())

        elif arr.shape[0] <= self.size[0]:
            ord = np.linspace(self.position[0], self.size[0] + self.position[0], arr.shape[0]).astype(int)
            return scale_it_scale_it(np.array([ord, arr]).transpose())




if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Oscilloscope")
    screen = pygame.display.set_mode([1280, 720])
    oscillo = PGOscilloscope(screen, (1280, 720), (0, 0))

    time_previous = time.time()
    while True:
        valuesl = np.random.rand(10) - 0.5
        valuesr = np.random.rand(115) - 0.5
        oscillo.update(left = valuesl, right=valuesr)
        time.sleep(0.1)
        print(time.time() - time_previous)
        time_previous = time.time()
