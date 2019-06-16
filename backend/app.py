import time
from RPi import GPIO
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from DP1Database import Database
import ldr
import rfidreader
from LCD import LCD_run
import parkingSensor
import pigpio

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
conn = Database(app=app, user='gilles', password='Clemens9010',
                db='project', host='localhost', port=3306)

# refers to the class that makes lcd run
LCD_run()

# refers to the class that makes the lighting work
licht = ldr.Verlichting(conn)

parking = parkingSensor.parkingSensor(conn)

servoPIN = 17

GPIO.setmode(GPIO.BCM)

piGPIO = pigpio.pi()

piGPIO.set_PWM_frequency(servoPIN, 50)
piGPIO.set_PWM_dutycycle(servoPIN, (7.5 / 100) * 255)


@socketio.on('button')
def openSlagboom():
    piGPIO.set_PWM_dutycycle(servoPIN, (14 / 100) * 255)
    time.sleep(3)
    piGPIO.set_PWM_dutycycle(servoPIN, (7.5 / 100) * 255)


@socketio.on('getAuto')
def auto():
    state = conn.get_data(
        "SELECT value FROM project.Historiek WHERE project.Historiek.Sensor_idSensor = 3 ORDER BY project.Historiek.idHistoriek DESC LIMIT 1;")
    socketio.emit('giveAuto', str(state[0]['value']))


# refers to the class that works the rfid reader and the automatic barrier
slagboom = rfidreader.rfid(conn, openSlagboom)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port="5000")
