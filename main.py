import time
from raspi.peripherals import Sensor, Motor
from thingspeak.api import send_data
from aws.iot import IOT
import json

GPIO_DHT = 26

GPIO_MOTOR = 13

PUBLISH_PERIOD = 2  # seconds

TEMP_THRESH = 35  # deg C
HUMI_THRESH = 65  # %


class BloomAir:

    def __init__(self):
        self.ALIVE, self.DEAD = True, False

        self.sensor = Sensor({"dht": GPIO_DHT})
        self.motor = Motor(GPIO_MOTOR)
        self.IOT = IOT()
        self.live()

    def run(self):
        loop, i = True, 0
        while loop:
            out = self.sensor.read()
            temp, humi = out['temp_c'], out['humidity']

            print("Temperature: {} °C, humidity: {} %".format(temp, humi))
            if temp > TEMP_THRESH or humi > HUMI_THRESH:
                if self.status is self.ALIVE:
                    self.die()
            else:
                if self.status is self.DEAD:
                    self.live()

            if i >= 5:
                send_data(temp, humi)
                self.IOT.publish(json.dumps(
                    {"temperature": temp, "humidity": humi}))
                i = 0
            else:
                i += 1
            time.sleep(PUBLISH_PERIOD)

    def die(self):
        print("I'm dying")
        self.status = self.DEAD
        self.motor.down()

    def live(self):
        print("I'm alive")
        self.status = self.ALIVE
        self.motor.up()


if __name__ == "__main__":
    inst = BloomAir()
    inst.run()
