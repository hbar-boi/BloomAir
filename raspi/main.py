import time
import board
import adafruit_dht

dev = adafruit_dht.DHT11(board.D17)
while True:
	try:
		temp = dev.temperature
		humi = dev.humidity

		print("Temp: {:.1f} C, humi: {:.1f}%")
	except RuntimeError as e:
		pass
	time.sleep(2.0)
