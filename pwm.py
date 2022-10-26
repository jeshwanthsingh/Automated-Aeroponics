import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)

while(1):
    ldr=1000
    if(ldr<100):
        r = GPIO.PWM(27,100)
        b=GPIO.PWM(17,100)
        g=GPIO.PWM(4,100)
        r.start(100)
        time.sleep(0.5)
        r.stop()
        b.start(100)
        time.sleep(0.5)
        b.stop()
        g.start(100)
        time.sleep(0.5)
        g.stop()
    elif(ldr>100):
        r = GPIO.PWM(27,100)
        b=GPIO.PWM(17,100)
        g=GPIO.PWM(4,100)
        r.start(10)
        time.sleep(0.5)
        r.stop()
        b.start(10)
        time.sleep(0.5)
        b.stop()
        g.start(10)
        time.sleep(0.5)
        g.stop()
        




