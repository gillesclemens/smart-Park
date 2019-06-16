from RPi import GPIO
import time
from flask import Flask
from threading import Thread

from DP1Database import Database
import datetime

app = Flask(__name__)

conn = Database(app=app, user='gilles', password='Clemens9010',
                db='project', host='localhost', port=3306)

GPIO.setmode(GPIO.BCM)
TRIG = 20
ECHO = 21

delay = .5
value = 0
ldr = 18
led = 27

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, 0)


class Verlichting(Thread):
    def __init__(self, mysqlcon):
        Thread.__init__(self)
        self.deamon = True
        self.conn = mysqlcon

        self.sensor_id_distance1 = self.conn.get_data('SELECT * FROM Sensor WHERE sensorNaam="distance1"')
        if not self.sensor_id_distance1:
            self.sensor_id_distance1 = self.conn.set_data('INSERT INTO Sensor VALUES (NULL, "distance1", "cm" )')
        else:
            self.sensor_id_distance1 = int(self.sensor_id_distance1[0]['idSensor'])

        self.sensor_id_ldr = self.conn.get_data('SELECT * FROM Sensor WHERE sensorNaam="ldr"')
        if not self.sensor_id_ldr:
            self.sensor_id_ldr = self.conn.set_data('INSERT INTO Sensor VALUES (NULL, "ldr", NULL )')
        else:
            self.sensor_id_ldr = int(self.sensor_id_ldr[0]['idSensor'])

        self.start()

    def run(self):
        def berekenen_ldr(ldr):
            count = 0
            GPIO.setup(ldr, GPIO.OUT)
            GPIO.output(ldr, 0)
            time.sleep(delay)
            GPIO.setup(ldr, GPIO.IN)
            while GPIO.input(ldr) == 0:
                count += 1
            return count

        while True:
            GPIO.output(TRIG, True)
            time.sleep(0.001)
            GPIO.output(TRIG, False)

            end = 0
            start = 0

            print(GPIO.input(ECHO))

            while not GPIO.input(ECHO):
                start = time.time()

            while GPIO.input(ECHO):
                end = time.time()

            sig_time = end - start
            distance = (sig_time * 34300) / 2

            if distance < 4:
                licht = berekenen_ldr(ldr)
                if (licht >= 500):
                    GPIO.output(led, GPIO.HIGH)
                    time.sleep(5)
                    GPIO.output(led, GPIO.LOW)
                print("waarde = {0}".format(licht))
                currnet_time = datetime.datetime.now()
                datum = str(currnet_time)[0:16]
                row_inserted_ldr = conn.set_data(
                    "INSERT INTO Historiek(date, value, Sensor_idSensor) VALUES (%s,%s,%s)",
                    [datum, licht, 1]
                )

            currnet_time = datetime.datetime.now()
            datum = str(currnet_time)[0:16]
            row_inserted_distance1 = conn.set_data(
                "INSERT INTO Historiek(date, value, Sensor_idSensor) VALUES (%s,%s,%s)",
                [datum, distance, 2])

            print("Measured Distance = %.1f cm" % distance)
            time.sleep(4)


verlichting = Verlichting(conn)
