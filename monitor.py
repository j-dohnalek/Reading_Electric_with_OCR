#!/usr/bin/python

# ############################################################################
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
#    3) read the _file
#    ssocr -d <number of digits> -t <threshold> out.jpg
#
#    if you wish to run it on in pattern like 1 time a day consider using crontabs
#
# ############################################################################

# IMPORTS ###################################################################


# PARTICULAR IMPORTS ########################################################

import os
import os.path
import subprocess
import csv
import time
import datetime

from pytz import timezone
from collections import deque

# THIRD-PARTY IMPORTS #######################################################

import jemail
import raspicamera
import debug

# CONSTANTS #################################################################
TIMEZONE = 'Europe/London'

SMTP_USERNAME = ""
SMTP_PASSWORD = ""
EMAIL_TO = ""
SUBJECT = ""
RECIPIENT_NAME = ""

# digits you are about to convert
NUMBER_OF_DIGITS = 5

# Absolute _path to the directory where the python _files are stores
# this will help to run it in the crontabs
APP_PATH = '/home/shares/nas/testApp/'

TEMP_DIR = APP_PATH + 'temporary/'

# name of the first image
IMAGE_IN = TEMP_DIR + 'img.jpg'

# name of the image after the convertion
IMAGE_OUT = TEMP_DIR + 'out.jpg'

# history folder is where python saves all the previous readings
HISTORY = APP_PATH + 'cache/history/'
HISTORY_FILE = HISTORY + 'last_reading.csv'

# attachment error log
DEBUG_LOG = 'cache/debug/error_log.csv'

# FUNCTIONS #################################################################


def begin():

    """
    Entry point for code.  Takes no arguments.

    """
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    start = time.time()  # measure execution time of the script

    credit = 0
    for i in range(10):
		# Process the picture
		raspicamera.take_picture(IMAGE_IN)
		convert_image(IMAGE_IN, IMAGE_OUT)
		credit = convert_image_to_text(IMAGE_OUT, NUMBER_OF_DIGITS)
		
		if isinstance(credit, float):
			break
		else:
			clean_dir(TEMP_DIR)
    
		print("Number of tries {}".format(i))
	
    message = email_msg(RECIPIENT_NAME, credit)
    jemail.send_email(SUBJECT, message, EMAIL_TO, SMTP_USERNAME, SMTP_PASSWORD)
    clean_dir(TEMP_DIR)  # clear the images
    print "Script execution time %5.2f seconds." % (time.time() - start)


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
        _size = [690, 280]
    else:
        _size = size

    # margin[0] = left margin (pixels)
    # margin[1] = top margin (pixels)
    if margin is None:
        _margin = [110, 0]
    else:
        _margin = margin

    # size of the output image
    if resize is None:
        _resize = 20  # percent of original
    else:
        _resize = resize

    cmd = """/usr/bin/convert {0} -crop {1}x{2}+{3}+{4} -resize {5}% {6}
        """.format(image_name,  # 0
                   str(_size[0]),  # 1
                   str(_size[1]),  # 2
                   str(_margin[0]),  # 3
                   str(_margin[1]),  # 4
                   str(_resize),  # 5
                   output_image  # 6
                   )

    cmd_list = cmd.split()

    try:
        subprocess.call(cmd_list)
    except subprocess.CalledProcessError as err:
        debug.write_csv_error_log('monitor.py', 'convert_image()', err)


def convert_image_to_text(image, number_of_digits):
    """

    :param img:  image to convert
    :param number_of_digits:  number of digits you want to read
    :return:
    """

    cmd = "/usr/local/bin/ssocr -d {0} -t 10 {1}".format(str(number_of_digits), image)

    #returned_image = commands.getoutput(cmd)
    # what is this calling?  is this meant to be another call to subprocess.call?

    # the commands.getoutput have just outputed the value from the the
    # command which was than returned for future use.

    cmd_list = cmd.split()  # remember, if there is a space in your command,
                            # it has to be a list object split at the spaces.

    # found check_output here: http://docs.python.org/2/library/subprocess.html
    # subprocess.call will only return the returncode, not the output data from the command.

    try:
        returned_text = subprocess.check_output(cmd_list)
        if len(returned_text.strip()) is number_of_digits:
            return float(returned_text)
        else:
            print("Not enough digits found!")

    except subprocess.CalledProcessError as err:
        debug.write_csv_error_log('monitor.py', 'convert_image_to_text()', err)


def get_last_row(csv_filename):
    """

    :param csv_filename: file name to read the last recorded meter reading
    :return: string of the last reading
    """
    with open(csv_filename, 'rb') as f:
        return deque(csv.reader(f), 1)[0]


def email_msg(recipien, credit):

    time_zone = timezone(TIMEZONE)  # set current time zone
    current_time_zone = datetime.datetime.now(time_zone)  # set current time zone
    message = "Hello " + str(recipien) + ", <br><br>"
    message += """This is a message from you automated system to
                 monitor reamining credit on your electric meter."""
    message += """<h3>Current balance: &pound;{0} <br />""".format(str(credit))
    message += """Reading Date: {0}""".format(current_time_zone.strftime('%H:%M:%S %d.%m.%Y'))
    message += "</h3><br>Regards<br>Your Rasperry Pi Automated System"

    return message


def clean_dir(_path):
    """

    :param _path:  path to clean
    """
    _file = os.listdir(_path)
    for i in range(0, len(_file)):
        if os.path.exists(_path + _file[i]):
            os.remove(_path + _file[i])


def main():
    begin()

###############################################

if __name__ == "__main__":
    main()
