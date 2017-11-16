#!/usr/bin/env python3
import pigpio # Library for getting temps and humdity from sensor
import DHT22
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from time import sleep
from datetime import datetime

cred = credentials.Certificate('/home/pi/SmartWeather/Smart Weather-831fcc7de0e7.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://smart-weather-58527.firebaseio.com/'})

# this connects to the pigpio daemon which must be started first
pi = pigpio.pi()
# Pigpio DHT22 module should be in same folder as your program
s = DHT22.sensor(pi, 4)

root = db.reference()
while(True):
    now = datetime.now()
    #currentDate = root.child((str(now.month) + "-" + str(now.day) + "-" + str(now.year)))
    currentDate = root.child(now.strftime('%Y-%m-%d'))
    temps = currentDate.child('temps')
    humiditys = currentDate.child('humidity')

    s.trigger()	 # reads in new temp and humidity
    sleep(.5)	 # the trigger() call needs time before values are taken from 's'
    humidity = s.humidity()
    temp = s.temperature() * (9/5) + 32

    
    print(now.strftime('%H:%M:%S'))
    temps.update({now.strftime('%H:%M:%S'): round(temp,2)})
    humiditys.update({now.strftime('%H:%M:%S'): round(humidity,2)})

    print("Time\t" + str(now.time()))
    print("Humidity:\t"+str(round(humidity,2))+"%")
    print("Temperature:\t"+str(round(temp,2))+" F")
    
    sleep(600)
