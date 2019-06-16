from RPi import GPIO
import time
import subprocess
import Adafruit_CharLCD as LCD

GPIO.setmode(GPIO.BCM)

delay = .5
value = 0
ldr = 18
led = 27

GPIO.setup(led, GPIO.OUT)
GPIO.output(led, 0)


def berekenen(ldr):
    count = 0
    GPIO.setup(ldr, GPIO.OUT)
    GPIO.output(ldr, 0)
    time.sleep(delay)
    GPIO.setup(ldr, GPIO.IN)
    while (GPIO.input(ldr) == 0):
        count += 1
    return count


try:
    while True:
        value = berekenen(ldr)
        print("waarde = {0}".format(value))
        if (value <= 500):
            GPIO.output(led, False)
        if (value > 500):
            GPIO.output(led, True)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()



