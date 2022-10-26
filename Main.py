import RPi.GPIO as GPIO
import time
import urllib2
import subprocess


GPIO.setmode(GPIO.BCM)



myAPI = "J31X9OFZ15GKDV7K"
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI # THINGSPEAK


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
pump=26
# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
GPIO.setup(motor, GPIO.OUT)
GPIO.setup(pump, GPIO.OUT)
GPIO.output(motor, True)
GPIO.output(pump, True)
try:
    while True:
        temp  = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        temp=(temp-60)
        ldr = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        moist   = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print("Temp:{0},Moist:{1},LDR:{2}".format(temp,moist,ldr))
        Sensordata = ("Temp:"+ str(temp)+"Moist:"+str(moist)+"LDR:"+str(ldr))
          
        if(temp>35):
                data="Your Green House state is Ubnormal, High Temperature"
                GPIO.output(motor,False)
                subprocess.call(["sudo","python","mail.py",Sensordata,data])
                
        elif(moist<1000):
                data="Your Green House state is Ubnormal, Low Moisture"
                GPIO.output(pump,False)
                subprocess.call(["sudo","python","mail.py",Sensordata,data])
        else:
                GPIO.output(pump,True)
                GPIO.output(motor,True)
                
	# THINGSPEAK
        urllib2.urlopen(baseURL +"&field1=%s" % (str(temp)))   
        time.sleep(15)
        urllib2.urlopen(baseURL +"&field2=%s" % (str(ldr)))
        time.sleep(15)
        urllib2.urlopen(baseURL +"&field3=%s" % (str(moist)))
        time.sleep(15)									
		
											

except KeyboardInterrupt:
    print("stopping")
    GPIO.cleanup()
