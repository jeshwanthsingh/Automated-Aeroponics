#!/usr/bin/env python2

# you can remove the code from here
"""#import RPi.GPIO as GPIO
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
"""

# till here

import smtplib
import os.path as op
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import sys

username = "demo7365iot@gmail.com"
password = "demo7365"

# Note :- If you get a authentication error go over to https://myaccount.google.com/lesssecureapps?pli=1  and click on allow secure apps

# usage :- python2 mail.py  "subject" "Sensor_data" "attachment.jpg"

def send_mail(send_from, send_to, subject, text, files,
              username=username, password=password):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(op.basename(path)))
        msg.attach(part)

    smtp = smtplib.SMTP_SSL('smtp.gmail.com')
    print("\n Logging in...\n")
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    print("Email Sent.")
    smtp.quit()


send_mail("state", ["ssss.sahoo68@gmail.com"], sys.argv[1], sys.argv[2], [sys.argv[3]])

