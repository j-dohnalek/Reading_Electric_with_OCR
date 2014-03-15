#!/usr/bin/python

#############################################################################
#    monitor.py - Python 2.7
#    Copyright (C) 2014 Jiri Dohnalek
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#    You can test how the image looks like just copy and paste the command bellow
#    ----------------------------------------------------------------------------
#    1) take the picture
#    raspistill -ISO 800 -ss 150000 -mm matrix -awb auto -ex night -co 60 -w 800 -h 600 -o image.jpg
#    2) convert the image for the ssocr 
#    convert image.jpg -crop 560x200+290+140 -threshold 3% -resize 20% out.jpg
#    3) read the file
#    ssocr -d <number of digits> -t <threshold> out.jpg
#
#############################################################################

from commands import getoutput
from os import remove
from os import listdir
from os.path import exists
import time
import picamera
import sys
import smtplib

# ------------------
#	Functions
# ------------------


def SendEmail(fromEmail,emailTo,subject,body,smtpPass,smtpUser):

	header = 'To: '+ emailTo + '\n' + 'From: ' + fromEmail + '\n'+ 'Subject: ' + subject
	s = smtplib.SMTP('smtp.gmail.com',587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login(smtpUser, smtpPass)
	s.sendmail(fromAdd, emailTo, header + '\n\n' + body)
	s.quit()

def takePicture(imageName,resolution,settings):
    with picamera.PiCamera() as camera:
        camera.resolution = (resolution[0], resolution[1])
        camera.start_preview()
        camera.contrast = settings['co']
        camera.ISO = settings['iso']
        camera.exposure_mode = settings['em']
        camera.meter_mode = settings['mm']
        camera.shutter_speed = settings['ss']
        camera.AWB = settings['awb']
        # Give the camera some time to adjust to conditions
        time.sleep(2)
        camera.capture(imageName)
        camera.stop_preview()

def convertImage(imageName,outputImage,size,margin,resize,threshold):
    # picture setting commands
    cmd = '/usr/bin/convert '+ imageName
    cmd = cmd + ' -crop '+ str(size[0]) +'x'+ str(size[1])
    cmd = cmd + '+' + str(margin[0]) + '+' + str(margin[1])
    cmd = cmd + ' -resize '+ str(resize) 
    cmd = cmd +'% -threshold ' + str(threshold) + '% ' + outputImage
    # picture processing
    getoutput(cmd)

def convertImageToText(JpgImg):
    return getoutput('/usr/local/bin/ssocr -d 5 '+ JpgImg );

def cleanDir(Path):
    file = listdir(Path)
    for i in range(0,len(file)):
        if(exists(Path + file[i])):
            remove(Path + file[i])

def cutZero(var):
    if var[:1] == '0':
        return var[1:]
    else:
        return var
        
# ------------------
#	Variables
# ------------------

# Absolute path to the directory where the python files are stores
# this will help to run it in the crontabs
AppPath = '/home/shares/nas/homeApps/'
TempDir = AppPath + 'temporary/'
# name of the first image
imgIn   = TempDir + 'img.jpg'
# name of the image after the convertion
imgOut  = TempDir + 'out.jpg'
# Resolution of the image from the camera
# better to keep is lower this will decrease
# the processing time
resolution = [800,600]
# camera settings
cameraSettings = {
					'co'  : 80,       # contrast
					'iso' : 800,      # ISO
					'em'  : 'night',  # exposure mode
					'mm'  : 'matrix', # metering mode
					'ss'  : 150000,   # shutter speed
					'awb' : 'auto'    # white balance
				}
# Picture settings have to be ajdusted based on the position
# how you will fit on the camera (i.e. to wall, or to the door) as
# the idea is to cut only the area where all the digits are.
# margin[0] = left margin (pixels)
# margin[1] = top margin (pixels)
margin    = [290,140]
# size[0] = width of the new image being cut out
# size[1] = height of the new image being cut out
size      = [560,200]
# size of the output image
resize    = 20 # <- percent of original
threshold = 2
# email settings
smtpPass = "smtpPassword"
smtpUser = "smtpUser"
emailTo  = "myemail@goes.here"
subject  = "Subject"
# start of message
message = "Hello \n\n\n"

# -----------------
#	Application
# ------------------

try:
	# Process the picture
	takePicture(imgIn,resolution,cameraSettings)
	convertImage(imgIn,imgOut,size,margin,resize,threshold)
	reading = cutZero(convertImageToText(imgOut))
	message = message + "Your current credit is "+ reading +" pounds."
except:
	message = "Monitoring system has come up to a error, please contact developer."

message = message + "\n\nRegards\nYour Rasperry Pi"
SendEmail(emailTo,subject,message)    
# clear the images
cleanDir(TempDir)
