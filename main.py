import RPi.GPIO as GPIO
import time

RECORD_BUTTON = 2
RECORD_LED = 4

LED_1 = 17
LED_2 = 27
LED_3 = 22
LED_4 = 10
LED_5 = 9
LED_6 = 11
LED_7 = 18
LED_8 = 23
LED_9 = 24


Led_status = 1

def setup():
    GPIO.setmode(GPIO.BCM)     # Numbers GPIOs by physical location
    GPIO.setup(RECORD_LED, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.setup(RECORD_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.output(RECORD_LED, GPIO.HIGH) # Set LedPin high(+3.3V) to off led

def swLed(ev=None):
    global Led_status
    Led_status = not Led_status
    GPIO.output(RECORD_LED, Led_status)  # switch led status(on-->off; off-->on)
    if Led_status == 1:
        print 'led on...'
    else:
        print '...led off'

def loop():
    GPIO.add_event_detect(RECORD_BUTTON, GPIO.FALLING, callback=swLed, bouncetime=200) # wait for falling and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
    while True:
        time.sleep(1)   # Don't do anything

def destroy():
    GPIO.output(RECORD_LED, GPIO.HIGH)     # led off
    GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()