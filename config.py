### configuration file for assos_listen
# upload
upload = False

# config for this sensor
sensorID = "al_01"

# sampling rate & chunk size
chunkSize = 8192
samplingRate = 44100 # 44100 needed for Aves sampling
# choices=[4000, 8000, 16000, 32000, 44100] :: default 16000

# sample length in seconds
sampleLength = 10

# configuration for assos_store container
ftp_server_ip = "192.168.0.157"
username = "sensor"
password = "sensor"

# storage on assos_listen device
storagePath = "/home/pi/assos_listen_pi/storage/"

channels = 2    #Number of channels recorded, here the microphones from left and right wing
sample_frequency = 44100    #Sample frequency of the field sensor
buffer_size = 4096      #Size of the field data buffer