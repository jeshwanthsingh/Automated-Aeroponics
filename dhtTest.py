import RPi.GPIO as GPIO
import time
import urllib2
import subprocess
import Adafruit_DHT
# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.DHT11

GPIO.setmode(GPIO.BCM)

def ts():
    print("Reading DHT")
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 27)
    return humidity, temperature

while (1):
    humi,temp=ts()
    print(humi,temp)
    time.sleep(2)
    
