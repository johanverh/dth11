#!/usr/bin/python
import requests
import json
import sys
import Adafruit_DHT
import datetime
from time import sleep   #this lets us have a time delay

sensor = Adafruit_DHT.DHT11
pin=4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

url = "https://www.nahoj.nl/api/v1"
sensorid = 1

def sendJson(url, data):
    json_data = json.dumps(data, ensure_ascii=False)
    #print (json_data)
    #print (url)
    r = requests.post(url, json_data);

def sendTemperature(url, value):
        t_url = url + "/temperature"
        data = {}
        data["sensorId"] = sensorid
        data["temperature"] = value
        sendJson(t_url, data)

def sendHumidity(url, value):
        t_url = url + "/humidity"
        data = {}
        data["sensorId"] = sensorid
        data["humidity"] = value
        sendJson(t_url, data)

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        print (datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"))
        print('Temperature={0:0.1f}C  Humidity={1:0.1f}%'.format(temperature, humidity))

        sendTemperature(url, temperature)
 
        sendHumidity(url, humidity)

        sleep(60)
finally:
    print ("gestopt")
