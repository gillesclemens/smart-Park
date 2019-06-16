from RPi import GPIO
import PCF8574A
import time
from subprocess import check_output
import subprocess

class LCD:

    def __init__(self, clock, rs, pcfpins=[22, 20]):
        self.clock = clock
        self.rs = rs
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(clock, GPIO.OUT)
        GPIO.setup([22, 20], GPIO.OUT)
        GPIO.setup(rs, GPIO.OUT)

        self.pcf = PCF8574A.PCF8574A(6, 13)

        GPIO.output(clock, 1)

    def init_lcd(self):
        self.write_byte(0x38, instruction=True)

    def reset(self):
        self.write_byte(0b1, instruction=True)

    def display_on(self):
        self.write_byte(0b1100, instruction=True)

    def write_one_bit(self, bit):

        # address = 0b0 | (pin << 4)
        # print(bin(address))

        self.pcf.write_byte(bit)

    def write_byte(self, byte, instruction=False):

        if instruction:
            GPIO.output(self.rs, 0)
        else:
            GPIO.output(self.rs, 1)
        GPIO.output(self.clock, 1)
        mask = 1
        # for i in reversed(range(8)):
        #     bit = byte & (mask << i)
        #     self.pcf.write_byte(bit)

        self.pcf.write_byte(byte)
        GPIO.output(self.clock, 0)

        time.sleep(0.001)

    def send_char(self, c):
        ascii_code = ord(c)
        # print("Sending char: '{0}': {1} = 0b{1:0=8b}".format(c, ascii_code))
        self.write_byte(ascii_code)

    def send_string(self, s, secondrow):
        if secondrow:
            self.write_byte((0b1 << 7) | 0x40, instruction=True)
        else:
            self.write_byte((0b1 << 7) | 0x0, instruction=True)

        for i in s:
            print("sending char")
            self.send_char(i)


class LCD_run:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        lcd = LCD(24, 23)
        lcd.pcf.start_data()
        lcd.pcf.write_byte(0b01110000)
        lcd.init_lcd()
        lcd.display_on()
        lcd.reset()
        cmd = "ip -4 addr show wlan0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'"
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ps.communicate()
        ip = output[0].decode('ascii')[0:-1]

        # ips = check_output(['hostname', '--all-ip-addresses'])
        # ip4 = ips.decode('utf-8', errors='ignore').rstrip('\n')
        # ip = ip4.split()[0]

        lcd.pcf.start_data()
        lcd.pcf.write_byte(0b01110000)
        print("Made it")
        lcd.reset()
        lcd.init_lcd()
        lcd.display_on()
        lcd.send_string("SMART PARK", False)
        lcd.send_string(ip, True)
        lcd.pcf.stop_data()