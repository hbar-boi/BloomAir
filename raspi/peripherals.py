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
        self.FORWARD, self.BACKWARD = 0, 1

        self.pwms = []

        GPIO.setmode(GPIO.BCM)
        for gpio in gpios:
            GPIO.setup(gpio, GPIO.OUT)
            pwm = GPIO.PWM(gpio, 50)
            pwm.start(0.0)
            self.pwms.append(pwm)

        self.stop()

    def stop(self):
        for pwm in self.pwms:
            pwm.ChangeDutyCycle(0.0)

    def move(self, direction, speed, duration):
        self.pwms[direction].ChangeDutyCycle(speed)

        if duration is not None:
            time.sleep(duration)
            self.stop()

    def forward(self, speed=100.0, duration=None):
        self.move(self.FORWARD, speed, duration)

    def backward(self, speed=100.0, duration=None):
        self.move(self.BACKWARD, speed, duration)
