
## Data relative to field streaming
channels = 2    #Number of channels recorded, here the microphones from left and right wing
sample_frequency = 44100    #Sample frequency of the field sensor
buffer_size = 1024      #Size of the field data buffer
device_index = 5

## Data relative to image streaming
image_size = (640, 480)
frame_rate = 30

## Definition of serial port for controler
serial_port = '/dev/ttyUSB0'
baudrate = 115200

features_toogle_period = 1
feature_speed = 4
feature_width = 110

field_threshold = 10000
