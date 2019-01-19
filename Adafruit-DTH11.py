#!/usr/bin/python
import requests
import json
import sys
import Adafruit_DHT
import datetime
from time import sleep   #this lets us have a time delay
import RPi.GPIO as GPIO
from state import State

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.OUT)

sensor = Adafruit_DHT.DHT11
pin=4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

url = "https://www.nahoj.nl/api/v1"
sensorid = 1

cycles_length =  3000
i = 0
btn_up = 0

def outputOff(output):
    GPIO.output(output,0)

def outputOn(output):
    GPIO.output(output,1)
    

def start():
    outputOff(24)
    c = 0
    while (c < 10):
        outputOn(24)
        sleep(0.2)
        outputOff(24)
        sleep(0.2)
        c += 1

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
        
def sendSwitchState(url, switchId, state):
        t_url = url + "/switch"
        data = {}
        date["switchId"] = switchId
        data["state"] = value
        sendJson(t_url, data)

try:
    
    GPIO.setwarnings(False)
    
    switchState = State;
    
    start()
    
    while True:
        if (i == cycles_length):
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            print (datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"))
            print('Temperature={0:0.1f}C  Humidity={1:0.1f}%'.format(temperature, humidity))

            sendTemperature(url, temperature)
 
            sendHumidity(url, humidity)
            i = 0
        

        if GPIO.input(25):
            if(btn_up == 0):
                if (switchState.getState() == 0):
                   GPIO.output(24,1)
                   switchState.setState(1)
                else:
                    GPIO.output(24,0)
                    switchState.setState(0)

                btn_up = 1
        else:
            btn_up = 0
            
        
        i += 1
        sleep(0.1)
finally:
    GPIO.cleanup()
    print ("gestopt")
