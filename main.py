import time
from raspi.peripherals import Sensor, Motor
from thingspeak.api import send_data
from aws.iot import IOT
import json

GPIO_DHT = 4

GPIO_MOTOR_2 = 22
GPIO_MOTOR_1 = 27

SAMPLE_PERIOD = 2  # seconds
PUBLISH_PERIOD = 10 # seconds

TEMP_THRESH = 26  # deg C
HUMI_THRESH = 65  # %


class BloomAir:

    def __init__(self):
        self.ALIVE, self.DEAD = True, False

        self.sensor = Sensor({"dht": GPIO_DHT})
        self.motor = Motor([GPIO_MOTOR_1, GPIO_MOTOR_2])
        self.IOT = IOT()
        self.reset()

    def reset(self):
        self.status = self.ALIVE
        self.motor.backward(1) # reset flower position

    def run(self):
        loop = True
        i = 0
        publish_iter = PUBLISH_PERIOD // SAMPLE_PERIOD
        while loop:
            print('here', i)
            out = self.sensor.read()
            print('out',out)
            temp, humi = out['temp_c'], out['humidity']

            print("Temperature: {} °C, humidity: {} %".format(temp, humi))
            if temp > TEMP_THRESH or humi > HUMI_THRESH:
                if self.status is self.ALIVE:
                    self.die()
            else:
                if self.status is self.DEAD:
                    self.live()
            print(i,temp,humi)
            if i == 0:
                send_data(temp, humi)
                self.IOT.publish(json.dumps({"temperature": temp, "humidity": humi}))
            i = (i+1) % publish_iter
            time.sleep(SAMPLE_PERIOD)

    def die(self):
        print("I'm dying")
        self.status = self.DEAD
        self.motor.forward(1)

    def live(self):
        print("I'm alive")
        self.status = self.ALIVE
        self.motor.backward(1)


if __name__ == "__main__":
    inst = BloomAir()
    inst.run()
