import h5py
from multiprocessing import Process, Queue, Manager
import field_streamer as fs
import camera_streamer as cs
import traceback
import config
import time
import os
import numpy as np
import cv2


def __init__(self, field_chunk_size, image_size, video_fps=30):
    self.data_file_path = os.path.dirname(os.path.realpath(__file__)) + '/data'
    self.field_chunk_size = field_chunk_size
    self.image_size = image_size
    self.video_record = None
    self.video_fps = video_fps


def create_new_file(self, title):
    # New directory to record data
    os.mkdir(self.data_file_path + title)
    self.video_record = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), self.video_fps, self.image_size)

class Recorder():
    def __init__(self, field_chunk_size, image_size, video_fps=30):
        self.data_file_path = os.path.dirname(os.path.realpath(__file__)) + '/data'
        self.field_chunk_size = field_chunk_size
        self.image_size = image_size
        self.video_record = None
        self.video_fps = video_fps
        self.file = None


    def create_new_file(self, title):
        if not os.path.exists(self.data_file_path):
            os.makedirs(self.data_file_path)
        os.mkdir(self.data_file_path + '/' + title)
        self.file = h5py.File(self.data_file_path + '/' + title + '/' + title + '.hdf5', 'w')

        self.field_left_dset = self.file.create_dataset('field_left_dataset', (1, self.field_chunk_size),
                                                        maxshape=(None, self.field_chunk_size))
        self.field_right_dset = self.file.create_dataset('field_right_dataset', (1, self.field_chunk_size),
                                                        maxshape=(None, self.field_chunk_size))
        self.field_time_dset = self.file.create_dataset('field_time_dataset', (1, 1), maxshape=(None, 1),
                                                        dtype='float64')

        self.image_time_dset = self.file.create_dataset('image_time_dataset', (1, 1), maxshape=(None, 1),
                                                        dtype='float64')

        self.dir_right_dset = self.file.create_dataset('direction_right_dataset', (1, 1), maxshape=(None, 1),
                                                        dtype=float)

        self.dir_left_dset = self.file.create_dataset('direction_left_dataset', (1, 1), maxshape=(None, 1),
                                                        dtype=float)

        self.dir_time_dset = self.file.create_dataset('direction_time_dataset', (1, 1), maxshape=(None, 1),
                                                      dtype='float64')

        self.feature_dset = self.file.create_dataset('feature_dataset', (1, 1), maxshape=(None, 1),
                                                          dtype='S10')

        self.feature_time_dset = self.file.create_dataset('feature_time_dataset', (1, 1), maxshape=(None, 1),
                                                      dtype='float64')

        self.video_record = cv2.VideoWriter(self.data_file_path + '/' + title + '/' + title + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), self.video_fps,
                                            self.image_size)

        self.field_right_dset.attrs['field_channels'] = config.channels
        self.field_right_dset.attrs['field_sample_freq'] = config.sample_frequency
        self.field_right_dset.attrs['field_buffer_size'] = config.buffer_size
        self.field_left_dset.attrs['field_channels'] = config.channels
        self.field_left_dset.attrs['field_sample_freq'] = config.sample_frequency
        self.field_left_dset.attrs['field_buffer_size'] = config.buffer_size
        self.image_time_dset.attrs['frame_rate'] = config.frame_rate
        self.image_time_dset.attrs['frame_size'] = config.image_size

    def close_current_file(self):
        print('file close')
        self.video_record.release()
        self.file.flush()
        self.file.close()

    def record_image(self, image):

        self.image_time_dset.resize((self.image_time_dset.shape[0] + 1, 1))

        try:
            time_previous = time.time()
            self.video_record.write(image.image)
        except Exception:
            traceback.print_exc()
            return False

        try:
            self.image_time_dset[-1, :] = image.time_stamp
        except Exception:
            traceback.print_exc()
            return False

        return True

    def record_field(self, field):
        self.field_left_dset.resize((self.field_left_dset.shape[0] + 1, self.field_chunk_size))
        self.field_right_dset.resize((self.field_right_dset.shape[0] + 1, self.field_chunk_size))

        try:
            self.field_left_dset[-1, :] = field.field_left
            self.field_right_dset[-1, :] = field.field_right
        except Exception:
            traceback.print_exc()
            return False

        self.field_time_dset.resize((self.field_time_dset.shape[0] + 1, 1))
        try:
            self.field_time_dset[-1, :] = field.time_stamp
        except Exception:
            traceback.print_exc()
            return False

    def record_serial(self, serial):
        self.dir_right_dset.resize((self.dir_right_dset.shape[0] + 1, 1))
        self.dir_left_dset.resize((self.dir_left_dset.shape[0] + 1, 1))

        try:
            self.dir_right_dset[-1, :] = serial.right
            self.dir_left_dset[-1, :] = serial.left
        except Exception:
            traceback.print_exc()
            return False

        self.dir_time_dset.resize((self.dir_time_dset.shape[0] + 1, 1))
        try:
            self.dir_time_dset[-1, :] = serial.time_stamp
        except Exception:
            traceback.print_exc()
            return False

    def record_feature(self, feature):
        self.feature_dset.resize((self.feature_dset.shape[0] + 1, 1))

        try:
            self.feature_dset[-1, :] = feature.dir.encode("ascii", "ignore")

        except Exception:
            traceback.print_exc()
            return False

        self.feature_time_dset.resize((self.feature_time_dset.shape[0] + 1, 1))

        try:
            self.feature_time_dset[-1, :] = feature.stamp
        except Exception:
            traceback.print_exc()
            return False

        return True