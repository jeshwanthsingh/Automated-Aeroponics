#!/usr/bin/env python2
import RPi.GPIO as GPIO
import picamera
import time
from datetime import datetime
import urllib2
import subprocess
import Adafruit_DHT
import requests


sensor = Adafruit_DHT.DHT11
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
myAPI = "MJWUPT1PW0JWUXE5"  # "P27V7HXRBNNABMJA"  #MJWUPT1PW0JWUXE5
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI  # THINGSPEAK


def ts():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, DHTpin)
    return humidity, temperature


# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    GPIO.output(cspin, True)
    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)  # bring CS low

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3  # we only need to send 5 bits here
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if (GPIO.input(misopin)):
            adcout |= 0x1

    GPIO.output(cspin, True)

    adcout >>= 1  # first bit is 'null' so drop it
    return adcout


# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 12
SPIMISO = 16
SPIMOSI = 20
SPICS = 21
motor = 19
pump = 26
DHTpin = 17
led=24
# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
GPIO.setup(motor, GPIO.OUT)
GPIO.setup(pump, GPIO.OUT)
GPIO.setup(DHTpin, GPIO.IN)
GPIO.output(motor, True)
GPIO.output(pump, True)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(led,GPIO.OUT)
Figure = 1
try:
    while True:
        rootTemp = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        rootTemp = (rootTemp - 35)
        humi, shootTemp = ts()
        ldr = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print("Root Temp:{0}, Shoot Temp:{1}, LDR:{2}, Humi:{3}".format(rootTemp, shootTemp, ldr, humi))
        Sensordata = ("RootTemp:" + str(rootTemp) + "ShootTemp:" + str(shootTemp) + "LDR:" + str(ldr) + "Humidity:" + str(humi))
        GPIO.output(pump, False)  #
        time.sleep(6)  # Run Root pump for 6 seconds every 30 seconds
        GPIO.output(pump, True)  #
        time.sleep(10)  #

        if shootTemp > 22:
            print("High Shoot Temperature")
            data = "Your Green House state is abnormal, High Temperature"  # If Shoot temperature is greater than
            GPIO.output(motor, False)  # threshold, turn on Fan
            print("Fan On")
            f = open("log.txt", "a")
            f.write(Sensordata + "\n")
            f.close()
            with picamera.PiCamera() as camera:
                filename = str(Figure) + '.jpg'
                camera.capture(filename)
                Figure += 1
            print("Sending e-Mail")
            subprocess.call(["python", "mail.py", data, Sensordata, filename])  # and send email
            print("Mail Sent")
        else:
            GPIO.output(motor, True)  # else turn off Fan
            print("Fan Off")
            with picamera.PiCamera() as camera:
                camera.capture(str(Figure) + '.jpg')
                Figure += 1
        '''if ldr > 500:
            for i in range(1, 10):
                r = GPIO.PWM(27, 100)
                b = GPIO.PWM(18, 100)
                g = GPIO.PWM(4, 100)
                r.start(100)
                time.sleep(0.5)
                r.stop()
                b.start(100)
                time.sleep(0.5)
                b.stop()
                g.start(100)
                time.sleep(0.5)
                g.stop()
        else:
            GPIO.output(pump, True)
            GPIO.output(motor, True)
            for i in range(1, 10):
                r = GPIO.PWM(27, 100)
                b = GPIO.PWM(18, 100)
                g = GPIO.PWM(4, 100)
                r.start(10)
                time.sleep(0.5)
                r.stop()
                b.start(10)
                time.sleep(0.5)
                b.stop()
                g.start(10)
                time.sleep(0.5)
                g.stop()'''
	now = datetime.now().time() #To Get The Current Time
	print("The Light for Nourishment has started at {}".format(now)) #current time

	data = requests.post("https://maker.ifttt.com/trigger/turn_on/with/key/8qnVquiUbPIPeKtd0jFfa")


        GPIO.output(led, False)
        time.sleep(60)
        GPIO.output(led, True)
        time.sleep(60)
        print("Updating ThingSpeak...")
        urllib2.urlopen(baseURL + "&field1=%s" % (str(rootTemp)))
        print("Updated Root Temp")
        time.sleep(20)
        urllib2.urlopen(baseURL + "&field2=%s" % (str(shootTemp)))
        print("Updated Shoot Temp")
        time.sleep(20)
        urllib2.urlopen(baseURL + "&field3=%s" % (str(ldr)))
        print("Updated ldr")
        time.sleep(20)
        urllib2.urlopen(baseURL + "&field4=%s" % (str(humi)))
        print("Updated Humidity")
        time.sleep(20)
        print("Thingspeak Updated.")


except KeyboardInterrupt:
    print("stopping")
    GPIO.cleanup()


