from RPi import GPIO


class PCF8574A:

    def __init__(self, sda, clk):
        self.sda = sda
        self.clk = clk

        GPIO.setmode(GPIO.BCM)
        GPIO.setup([sda, clk], GPIO.OUT)
        GPIO.output(sda, 1)
        GPIO.output(clk, 1)

    def start_data(self):
        GPIO.output(self.sda, 0)
        GPIO.output(self.clk, 0)

    def stop_data(self):
        GPIO.output(self.clk, 1)
        GPIO.output(self.sda, 1)

    def write_bit(self, bit):
        GPIO.output(self.sda, bit)
        GPIO.output(self.clk, 1)
        GPIO.output(self.clk, 0)
        GPIO.output(self.sda, 0)

    def write_byte(self, byte):
        mask = 1
        for i in reversed(range(8)):
            bit = byte & (mask << i)
            self.write_bit(bit)
        self.ack()

    def ack(self):
        GPIO.setup(self.sda, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(self.clk, 1)
        read = GPIO.input(self.sda)
        # if read:
        #     raise IOError('NOT ACK')
        # else:
        #     print('ACKNOWLEDGE')
        GPIO.setup(self.sda, GPIO.OUT)
        GPIO.output(self.clk, 0)

