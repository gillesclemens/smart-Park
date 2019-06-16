#!/usr/bin/env python

import sys, tty, termios, time, pigpio

servos = [17]

dit = pigpio.pi()

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def motor1_forward():
    dit.set_servo_pulsewidth(servos[0], 1600)
    print("motor1=1600")

def motor1_reverse():
    dit.set_servo_pulsewidth(servos[0], 1400)
    print("motor1=1400")

def motor1_stop():
    dit.set_servo_pulsewidth(servos[0], 1500)
    print("motor1=1500")

def motor2_forward():
    dit.set_servo_pulsewidth(servos[1], 1600)
    print("motor2=1600")

def motor2_reverse():
    dit.set_servo_pulsewidth(servos[1], 1400)
    print("motor2=1400")

def motor2_stop():
    dit.set_servo_pulsewidth(servos[1], 1500)
    print("motor2=1500")

while True:
    char = getch()

    print("          " + char)

    if char == "w":
        motor1_forward()
        motor2_forward()

    elif char == "s":
        motor1_reverse()
        motor2_reverse()

    elif char == "a":
        motor1_stop()
        motor2_forward()

    elif char == "d":
        motor1_forward()
        motor2_stop()

    elif char == "x":
        print("STOPPED")
        motor1_stop()
        motor2_stop()
        time.sleep(1)
        for s in servos: # stop servo pulses
            dit.set_servo_pulsewidth(s, 0)
        dit.stop()
        break

dit.stop()