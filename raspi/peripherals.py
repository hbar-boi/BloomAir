from pigpio_dht import DHT22
import RPi.GPIO as GPIO
import time


class Sensor:
    def __init__(self, gpios):
        self.gpios = gpios

        self.dht = DHT22(gpios["dht"])

    def read(self):
        while True:
            try:
                out = self.dht.read()
            except TimeoutError:
                continue
            if out['valid']:
                return out
            time.sleep(2)


class Motor:
    def __init__(self, gpios):
        self.FORWARD, self.BACKWARD = True, False

        self.gpios = gpios

        GPIO.setmode(GPIO.BCM)
        for gpio in gpios:
            GPIO.setup(gpio, GPIO.OUT)

        self.stop()

    def stop(self):
        for gpio in self.gpios:
            GPIO.output(gpio, False)

    def move(self, direction, duration):
        GPIO.output(self.gpios[0], direction)
        GPIO.output(self.gpios[1], not direction)

        if duration is not None:
            time.sleep(duration)
            self.stop()

    def forward(self, duration=None):
        self.move(self.FORWARD, duration)

    def backward(self, duration=None):
        self.move(self.BACKWARD, duration)
