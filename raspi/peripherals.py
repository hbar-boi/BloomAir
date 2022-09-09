from pigpio_dht import DHT22
import time
import pigpio


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
    def __init__(self, gpio):
        self.gpio = gpio

        pwm = pigpio.pi()
        pwm.set_mode(gpio, pigpio.OUTPUT)

        pwm.set_PWM_frequency(gpio, 50)
        pwm.set_servo_pulsewidth(gpio, 500)
        self.pwm = pwm

        self.up()

    def up(self):
        self.pwm.set_servo_pulsewidth(self.gpio, 500)

    def down(self):
        self.pwm.set_servo_pulsewidth(self.gpio, 2300)
