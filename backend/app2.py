import time
from RPi import GPIO
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from DP1Database import Database
# import ldr
import rfidreader
# import LCD
# import parkingSensor

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
conn = Database(app=app, user='gilles', password='Clemens9010',
                db='project', host='localhost', port=3306)

# refers to the class that makes lcd run
# lcdrunnen = LCD.lcdRun()

# refers to the class that works the rfid reader and the automatic barrier
slagboom = rfidreader.rfid(conn)

# refers to the class that makes the lighting work
# licht = ldr.Verlichting(conn)

# parking = parkingSensor.parkingSensor(conn)


# if __name__ == '__main__':
#   socketio.run(app, host="0.0.0.0", port="5000")
