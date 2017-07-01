# -*- coding: utf-8 -*- 
#!/usr/bin/python
"""
Reading Electric Consumption with OCR
Copyright (C) 2017 Jiri Dohnalek

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

# ############################################################################
#    monitor.py - Python 2.7
#
#    You can test how the image looks like just copy and paste the command bellow
#    ----------------------------------------------------------------------------
#    1) take the picture
#    raspistill -ISO 800 -ss 150000 -mm matrix -awb auto -ex night -co 60 -w 800 -h 600 -o image.jpg
#    2) convert the image for the ssocr
#    convert image.jpg -crop 560x200+290+140 -threshold 3% -resize 20% out.jpg
#    3) read the _file
#    ssocr -d <number of digits> -t <threshold> out.jpg
#
#    if you wish to run it on in pattern like 1 time a day consider using crontabs
#
# ###########################################################################

#  IMPORTS ##################################################################

import os
import os.path
import subprocess
import time
import sys

# THIRD-PARTY IMPORTS #######################################################

import ini
import push

# CONSTANTS #################################################################

# Absolute _path to the directory where the python _files are stores
# this will help to run it in the crontabs
PATH = '<INSERT PATH>'
LAST = '/last_reading.txt'  # Last reading

# FUNCTIONS #################################################################


def begin():

    """  Entry point for code.  Takes no arguments.  """
    
    credit = latest_meter_reading()
    consumtion = last_reading_read(credit)
    ini.clean_directory(PATH + ini.get_conf_setting('general', 'temp'))
    
    # Message composition
    message = "Remaining credit: £%.2f\n" % credit
    message += "Consumption: £%.2f per day\n" % consumtion
    
    if credit < 5:
        message += "\nPlease top up, the credit is getting lower."
    
    last_reading_write(credit)
    
    # Send the message
    push.send_message(message, 'Electric Meter Reading')
    

    
def last_reading_read(credit):
    """
    :param credit: current credit reading
    """
    if not os.path.exists(PATH + LAST):
        f = open(LAST, "w")
        f.write('0')
        f.close()
    
    f = open(PATH + LAST, "r")
    data = f.read()
    f.close()
    
    return  float(data) - float(credit)
    
   
def last_reading_write(data):
    """
    
    :param data: current reading to record
    """
    f = open(PATH + LAST, "w")
    f.write(str(data))
    f.close()


def take_picture(imagename):
    """
    Adjust the script command to your needs!
    
    Why I have not used the raspberry pi python camera module?
    My camera stopped working with the python library, however it worked with command line.
    Later it stopped working at all, curretly waiting for replacement
    
    -ISO Camera ISO settings
    -ss  Shutter Speed
    -awb White Balance
    -ex  Exposure Settins
    -co  Contrast Settings
    -w   Width of the image
    -h   Height of the image
    -o   output image name
    
    TODO: Use the python camera library
    """
    cmd = "/usr/bin/raspistill -ISO 1600 -ss 300000 -mm matrix -awb auto -ex night -co 80 -w 800 -h 600 -o %s" % imagename
    cmd_list = cmd.split()
    subprocess.check_output(cmd_list)    

    
def convert_image(image_name, output_image, size=None, margin=None, resize=None, threshold=None):
    """
    :param image_name:  name of the image you want to read
    :param output_image:  name of the image you want to create
    :param size:  trimmed size of the image
    :param margin:  any margins that you want to add
    :param resize:  resized size as a percentage
    :param threshold:  some threshold or other!
    """

    # size[0] = width of the new image being cut out
    # size[1] = height of the new image being cut out
    if size is None:
        _size = [600, 240]
    else:
        _size = size

    # margin[0] = left margin (pixels)
    # margin[1] = top margin (pixels)
    if margin is None:
        _margin = [150, 220]
    else:
        _margin = margin

    # size of the output image
    if resize is None:
        _resize = 15  # percent of original
    else:
        _resize = resize
        
    if threshold is None:
        _threshold = 19.80
    else:
        _threshold = threshold

    cmd = """/usr/bin/convert {0} -crop {1}x{2}+{3}+{4} -resize {5}% -threshold {6}% {7}
        """.format(image_name,  # 0
                   str(_size[0]),  # 1
                   str(_size[1]),  # 2
                   str(_margin[0]),  # 3
                   str(_margin[1]),  # 4
                   str(_resize),  # 5
                   str(_threshold), # 6
                   output_image  # 7 
                   )
                
    cmd_list = cmd.split()

    try:
        subprocess.call(cmd_list)
    except subprocess.CalledProcessError as err:
        print err

        
def latest_meter_reading():

    credit = 0

    image_in = PATH + ini.get_conf_setting('files', 'raw_image')
    image_out = PATH + ini.get_conf_setting('files', 'ready_image')

    for i in range(ini.get_conf_setting('variable', 'max_attempts', 'int')):

        time.sleep(1)
        # Process the picture
        print("Taking picture")
        take_picture(image_in)
        print("Converting picture")
        convert_image(image_in, image_out)
        print("Converting picture to text")
        credit = convert_image_to_text(image_out,5)

        if isinstance(credit, float):
            return credit

        else:
            ini.clean_directory(PATH + ini.get_conf_setting('general', 'temp'))

    # kill the application after the max attempts is crossed
    push.send_message("Application have failed to get the meter reading.", 'Electric Meter Reading')
    return sys.exit("Application have failed to get the meter reading.")


def convert_image_to_text(image, number_of_digits):
    """

    :param img:  image to convert
    :param number_of_digits:  number of digits you want to read
    :return:
    """

    cmd = "/usr/local/bin/ssocr -d %s %s" % (number_of_digits, image)
    cmd_list = cmd.split()
    
    try:
        returned_text = subprocess.check_output(cmd_list)
    
        if len(returned_text.strip()) is number_of_digits:
            try:
                return float(returned_text)
            except ValueError:
                pass
                
    except subprocess.CalledProcessError:
        pass

        
def main():
    begin()

###############################################

if __name__ == "__main__":
    main()
