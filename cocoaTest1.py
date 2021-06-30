import datetime
import time
import board
import busio
import digitalio
import adafruit_max31865
import sys
import mysql.connector
import threading
import requests
import urllib
import os
from bs4 import BeautifulSoup



'''spi bus and sensor'''
spi1=busio.SPI(board.SCK,MOSI=board.MOSI,MISO=board.MISO)
cs1=digitalio.DigitalInOut(board.D5)
sensor1=adafruit_max31865.MAX31865(spi1,cs1,wires=3)

"""spi2=busio.SPI(board.SCK,MOSI=board.MOSI,MISO=board.MISO)
cs2=digitalio.DigitalInOut(board.D6)
sensor2=adafruit_max31865.MAX31865(spi2,cs2,wires=3)

spi3=busio.SPI(board.SCK,MOSI=board.MOSI,MISO=board.MISO)
cs3=digitalio.DigitalInOut(board.D13)
sensor3=adafruit_max31865.MAX31865(spi3,cs3,wires=3)
"""
def upload2(temp,x):
    data1=urllib.request.urlopen("https://api.thingspeak.com/update?api_key=API_KEY&field1={0}&created_at={1}".format(str(float(temp)),str(x)))
    page=data1.read()
    data1.close()
    
def thingspeak():
    time.sleep(5)
    temp=sensor1.temperature
    
    """temp2=sensor2.temperature
    
    temp3=sensor3.temperature"""
    try:
        x=datetime.datetime.now()
        upload2(temp,x)
        print("success")
    except urllib.error.URLError:
        print("saving offline")
        offTime=datetime.datetime.now()
        offlineData=open("offline.txt","a")
        offlineData.write(str(temp)+"!"+str(offTime)+"\n")
        offlineData.close()
def uploadOffline():
    offlineInput=open("offline.txt")
    for tt in offlineInput:
        tempTime=tt.split("!")
        temp1=tempTime[0]
        time1=tempTime[1]
        upload2(temp1,time1)
        time.sleep(20)
    offlineInput.close()
        
"""i=0
while i<10:
    thingspeak()
    i=i+1"""
uploadOffline()
