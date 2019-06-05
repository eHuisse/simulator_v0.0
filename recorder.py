import h5py
from multiprocessing import Process, Queue, Manager
import field_streamer as fs
import camera_streamer as cs
import traceback
import config

class Recorder():
    def __init__(self, field_chunk_size, image_size):
        self.file = None
        self.field_chunk_size = field_chunk_size
        self.image_size = image_size

    def create_new_file(self, title):
        self.file = h5py.File(title + '.hdf5', 'w')

        self.field_left_dset = self.file.create_dataset('field_left_dataset', (1, self.field_chunk_size),
                                                        maxshape=(None, self.field_chunk_size))
        self.field_right_dset = self.file.create_dataset('field_right_dataset', (1, self.field_chunk_size),
                                                        maxshape=(None, self.field_chunk_size))
        self.field_time_dset = self.file.create_dataset('field_time_dataset', (1, 1), maxshape=(None, 1),
                                                        dtype=float)

        self.image_dset = self.file.create_dataset('image_dataset', (self.image_size[1], self.image_size[0], 1),
                                                        maxshape=(self.image_size[1], self.image_size[0], None))
        self.image_time_dset = self.file.create_dataset('image_time_dataset', (1, 1), maxshape=(None, 1),
                                                        dtype=float)

        self.file.attrs['field_channels'] = config.channels
        self.file.attrs['field_sample_freq'] = config.sample_frequency
        self.file.attrs['field_buffer_size'] = config.buffer_size
        self.file.attrs['frame_rate'] = config.frame_rate
        self.file.attrs['frame_size'] = config.image_size

    def close_current_file(self):
        self.file.flush()
        self.file.close()

    def record_image(self, image):
        self.image_time_dset.resize((self.image_time_dset.shape[0] + 1, 1))
        self.image_dset.resize((self.image_size[1], self.image_size[0], self.image_dset.shape[2] + 1))

        try:
            self.image_dset[:, :, -1] = image.image
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
        self.field_time_dset.resize((self.field_time_dset.shape[0] + 1, 1))

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

        return True