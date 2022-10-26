import urllib2
import time
myAPI = "N22ZCQ7T29G5QL1M"
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI # THINGSPEAK
try:
    print("Inside thingSpeak.py")
    urllib2.urlopen(baseURL +"&field1=%s" % (str(sys.argv[1])))
    print("updated 1")
    time.sleep(2)
    urllib2.urlopen(baseURL +"&field2=%s" % (str(sys.argv[2])))
    print("updated 2")
    time.sleep(2)
    urllib2.urlopen(baseURL +"&field3=%s" % (str(sys.argv[3])))
    print("updated 3")
    time.sleep(2)
    urllib2.urlopen(baseURL +"&field4=%s" % (str(sys.argv[4])))
    print("updated 4")
    time.sleep(2)
except:
    print "Failed to update ThingSpeak"
