import RPi.GPIO as GPIO
import time
import datetime
from threading import Thread
from flask import Flask
from DP1Database import Database

app = Flask(__name__)
conn = Database(app=app, user='gilles', password='Clemens9010',
                db='project', host='localhost', port=3306)

GPIO.setmode(GPIO.BCM)
TRIG = 5
ECHO = 26

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


class parkingSensor(Thread):
    def __init__(self, mysqlcon):
        Thread.__init__(self)
        self.deamon = True
        self.conn = mysqlcon
        self.start()

    def run(self):
        while True:
            GPIO.output(TRIG, True)
            time.sleep(0.001)
            GPIO.output(TRIG, False)

            end = 0
            start = 0

            while not GPIO.input(ECHO):
                start = time.time()

            while GPIO.input(ECHO):
                end = time.time()

            sig_time = end - start
            distance = (sig_time * 34300) / 2

            print("Measured Distance = %.1f cm" % distance)
            time.sleep(4)

            if distance <= 6:
                # 1 = occupied
                current_time = datetime.datetime.now()
                datum = str(current_time)[0:16]
                conn.set_data(
                    "INSERT INTO Historiek(date, value, Sensor_idSensor) VALUES (%s,%s,%s)",
                    [datum, 1, 3])

            else:
                # 0 = not occupied
                current_time = datetime.datetime.now()
                datum = str(current_time)[0:16]
                conn.set_data(
                    "INSERT INTO Historiek(date, value, Sensor_idSensor) VALUES (%s,%s,%s)",
                    [datum, 0, 3])


parking = parkingSensor(conn)
