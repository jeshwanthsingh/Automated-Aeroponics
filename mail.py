#import RPi.GPIO as GPIO
from subprocess import call
import time
import os
import glob
import smtplib
import base64
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText
import subprocess
import sys

gmail_user = "demo7365iot@gmail.com"
gmail_pwd = "demo7365"
FROM = 'demo7365iot@gmail.com'
TO = ['ssss.sahoo68@gmail.com'] #must be a list

#IMAGE

#subprocess.Popen("sudo fswebcam input.jpg",shell=True).communicate()      
#time.sleep(1)

msg = MIMEMultipart()
time.sleep(1)
msg['Subject'] ="Aeroponics Alert!!!"

#BODY with 2 argument

body=sys.argv[1]+sys.argv[2]          
msg.attach(MIMEText(body,'plain'))
time.sleep(1)

##body = "Alert!@!!"                               #for testing alone
##msg.attach(MIMEText(body,'plain'))



try:
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        print "smtp.gmail"
        server.ehlo()
        print "ehlo"
        server.starttls()
        print "starttls"
        server.login(gmail_user, gmail_pwd)
        print "reading mail & password"
        server.sendmail(FROM, TO, msg.as_string())
        print "from"
        server.close()
        print 'successfully sent the mail'
except:
        print "failed to send mail"


