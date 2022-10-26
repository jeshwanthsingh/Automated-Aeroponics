import time
import picamera
i =1
while True:
    with picamera.PiCamera() as camera:
        camera.capture(str(i)+'.jpg')
        time.sleep(2)
        i=i+1
