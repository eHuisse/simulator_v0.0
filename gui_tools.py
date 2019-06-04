import pygame
import math
import cv2
import numpy as np
from tkinter import *


class Vu_meter():
    def __init__(self, displaysurf, position=[0, 0], size=[130, 500], BGCOLOR=(0, 0, 0)):
        self.DISPLAYSURF = displaysurf
        self.position = position
        self.size = size
        w, h = pygame.display.get_surface().get_size()

        if w < size[0]:
            size[0] = w
        if h < size[1]:
            size[1] = h

        self.WINDOWWIDTH = size[0]
        self.WINDOWHEIGHT = size[1]
        self.BGCOLOR = BGCOLOR
        self.PeakL = 0
        self.PeakR = 0

    def update(self, data):
        """

        :param data:
        :return:
        """
        pygame.draw.rect(self.DISPLAYSURF, self.BGCOLOR, (self.position[0],
                                                          self.position[1],
                                                          self.size[0],
                                                          self.size[1]))
        fontSmall = pygame.font.Font('freesansbold.ttf', 12)

        amplitudel = (abs(max(data[:, 0])) / 32767)
        LevelL = (int(41 + (20 * (math.log10(amplitudel + (1e-40))))))

        amplituder = (abs(max(data[:, 1])) / 32767)
        LevelR = (int(41 + (20 * (math.log10(amplituder + (1e-40))))))

        #print(amplitudel)

        indicator_step = self.size[1] / 42
        indicator_height = self.size[1] / 50
        indicator_width = self.size[0] / 4

        line1 = self.size[0] / 13
        line2 = self.size[0] / 2 + line1 * 2

        # Use the levels to set the peaks
        if LevelL > self.PeakL:
            self.PeakL = LevelL
        elif self.PeakL > 0:
            self.PeakL = self.PeakL - 0.2
        if LevelR > self.PeakR:
            self.PeakR = LevelR
        elif self.PeakR > 0:
            self.PeakR = self.PeakR - 0.2



        for dB in range(0, 40, 4):
            number = str(dB)
            text = fontSmall.render("-" + number, 1, (255, 255, 255))
            textpos = text.get_rect()
            middle_screen_w = int(self.size[0] / 2)
            self.DISPLAYSURF.blit(text, (self.position[0] + middle_screen_w - self.size[0]/15,
                                         self.position[1] + (indicator_step * dB)))

            pygame.draw.rect(self.DISPLAYSURF, (220, 255, 220), (self.position[0],
                                                                 self.position[1],
                                                                 4,
                                                                 self.size[1]))

            pygame.draw.rect(self.DISPLAYSURF, (220, 255, 220), (self.position[0] + self.size[0]-4,
                                                                 self.position[1],
                                                                 4,
                                                                 self.size[1]))

            # Draw the boxes
        for i in range(0, LevelL):
            if i < 20:
                pygame.draw.rect(self.DISPLAYSURF, (220, 255, 220), (self.position[0] + line1,
                                                                 (self.position[1] + self.size[1] - i * indicator_step),
                                                                 indicator_width,
                                                                 indicator_height))
            elif i >= 20 and i < 30:
                pygame.draw.rect(self.DISPLAYSURF, (255, 255, 220), (self.position[0] + line1,
                                                                   (self.position[1] + self.size[1] - i * indicator_step),
                                                                   indicator_width,
                                                                   indicator_height))
            else:
                pygame.draw.rect(self.DISPLAYSURF, (255, 220, 220), (self.position[0] + line1,
                                                                 (self.position[1] + self.size[1] - i * indicator_step),
                                                                 indicator_width,
                                                                 indicator_height))

        for i in range(0, LevelR):
            if i < 20:
                pygame.draw.rect(self.DISPLAYSURF, (220, 255, 220), (self.position[0] + line2,
                                                                 (self.position[1] + self.size[1] - i * indicator_step),
                                                                 indicator_width,
                                                                 indicator_height))
            elif i >= 20 and i < 30:
                pygame.draw.rect(self.DISPLAYSURF, (255, 255, 220), (self.position[0] + line2,
                                                                   (self.position[1] + self.size[1] - i * indicator_step),
                                                                   indicator_width,
                                                                   indicator_height))
            else:
                pygame.draw.rect(self.DISPLAYSURF, (255, 220, 220), (self.position[0] + line2,
                                                                 (self.position[1] + self.size[1] - i * indicator_step),
                                                                 indicator_width,
                                                                 indicator_height))

        pygame.display.update()

def frame_show(image, DISPLAYSURF, position=[0, 0], size=[640, 480]):
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)

    DISPLAYSURF.blit(frame, (position[0], position[1]))

    pygame.display.update()


class MyWindow:
    def __init__(self, win):
        self.is_recording = False

        self.btn_text = StringVar()
        self.btn_text.set("Start Recording")

        self.lbl1=Label(win, text='Title')
        self.lbl2=Label(win, text='Comments')

        self.t1=Entry()
        self.t2=Entry()

        self.lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=50)
        self.lbl2.place(x=100, y=100)
        self.t2.place(x=200, y=100)

        self.b1=Button(win, textvariable=self.btn_text, command=self.start_pause_recording)
        self.b2=Button(win, text='Stop Recording', command=self.stop_recording)
        self.b1.place(x=50, y=150)
        self.b2.place(x=250, y=150)

    def start_pause_recording(self):
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.btn_text.set("Pause Recording")
        else:
            self.btn_text.set("Start Recording")

        print(self.is_recording)

    def stop_recording(self):
        print("is stopped")

    def is_recording(self):
        return self.is_recording
