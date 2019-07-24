import pyaudio
from multiprocessing import Process, Queue, Manager
import numpy as np
import time
import config
from matplotlib import pyplot as plt

class Stamped_field():
    def __init__(self):
        self.field_right = np.array([])
        self.field_left = np.array([])
        self.time_stamp = 0

class FieldStreamer(Process):
    def __init__(self, streaming_queue, stop_event, channels=2, rate=44100, frames_per_buffer=2048):
        super(FieldStreamer, self).__init__()
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.streaming_queue = streaming_queue
        self._field = Stamped_field()
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=True,
                                     frames_per_buffer=self.frames_per_buffer,
                                     input_device_index=4,
                                     stream_callback=self.get_callback())
        self.stop_event = stop_event

    def terminate(self):
        self._stream.close()
        self._pa.terminate()
        super(FieldStreamer, self).terminate()

    def run(self):
        # Use a stream with a callback in non-blocking mode
        self._stream.start_stream()
        print("#######################################")
        print("####  Field begins to be streamed  ####")
        print("#######################################")
        while not self.stop_event.is_set():
            time.sleep(0.1)
        self.terminate()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            #print(time_info)
            inputADCtime_CompBasis = time.time()    #- time_info['current_time'] + time_info['input_buffer_adc_time']
            field = self.demux(in_data, self.channels)
            field = np.transpose(field)
            self._field.field_right = field[0, :]
            self._field.field_left = field[1, :]
            self._field.time_stamp = inputADCtime_CompBasis

            try:
                self.streaming_queue.put_nowait(self._field)
            except:
                print("#### !!!!!!!! #### Chunk jumped !!")
                pass

            return in_data, pyaudio.paContinue
        return callback

    def demux(self, in_data, channels):
        """
        Convert a byte stream into a 2D numpy array with
        shape (chunk_size, channels)

        Samples are interleaved, so for a stereo stream with left channel
        of [L0, L1, L2, ...] and right channel of [R0, R1, R2, ...], the output
        is ordered as [L0, R0, L1, R1, ...]
        """
        # TODO: handle data type as parameter, convert between pyaudio/numpy types
        result = np.fromstring(in_data,  dtype=np.int16)

        chunk_length = len(result) / channels
        assert chunk_length == int(chunk_length)
        #print("chunk length : " +str(chunk_length)+ " ; channels : " +str(channels))
        result = np.reshape(result, (int(chunk_length), channels))
        return result


if __name__ == "__main__":
    manager = Manager()
    stop_event = manager.Event()
    field_queue = Queue(10)
    field_streamer = FieldStreamer(field_queue, stop_event)

    field_streamer.start()
    i = 0

    while i < 1:

        i = i + 1
        field = field_queue.get(True)

        #print("Chanel 1 : " + str(min(field_queue.get(True)[:, 0])))
        #print("Chanel 2 : " + str(min(field_queue.get(True)[:, 1])))

    time_range = np.linspace(0, 0.5, len(field.field_right))
    plt.figure()
    plt.plot(time_range, field.field_right, 'r-', time_range, field.field_left, 'b-')
    plt.show()
    field_streamer.terminate()