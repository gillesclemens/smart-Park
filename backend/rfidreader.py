import RPi.GPIO as GPIO
import sys
import time
from threading import Thread

sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522
import pigpio

# Initialization


class rfid(Thread):
    def __init__(self, mysqlcon, callback):
        self.servoPIN = 17
        GPIO.setmode(GPIO.BCM)
        self.callback = callback
        # GPIO.setup(servoPIN, GPIO.OUT)

        Thread.__init__(self)
        self.deamon = True
        self.conn = mysqlcon
        self.reader = SimpleMFRC522()

        # self.p = GPIO.PWM(servoPIN, 50)
        # self.p.start(7.5)

        self.piGPIO = pigpio.pi()
        self.piGPIO.set_PWM_frequency(self.servoPIN, 50)
        self.piGPIO.set_PWM_dutycycle(self.servoPIN, (7.5/100)*255)

        self.start()

    def run(self):
        while True:
            print("Hold a tag near the reader")

            id, text = self.reader.read()
            print(id)
            print(text)

            isGood = self.conn.get_data("SELECT * FROM project.rfid WHERE project.rfid.adress = %s;", id)

            if isGood:
                print("open")
                self.callback()
                print("stopped")
            else:
                print("sorry")
                time.sleep(3)