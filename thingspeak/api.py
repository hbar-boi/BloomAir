from time import sleep
import requests

def send_data(temp, humidity):
    #headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    requests.get("https://api.thingspeak.com/update", params={'field1': temp, 'field2': humidity, 'api_key':'OM2Q7PTXDBD4OOSQ'})
