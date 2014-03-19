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
#    3) read the _file
#    ssocr -d <number of digits> -t <threshold> out.jpg
#
#    if you wish to run it on in pattern like 1 time a day consider using crontabs
#
#############################################################################

# IMPORTS ###################################################################


# PARTICULAR IMPORTS ########################################################

from commands import getoutput
from os import remove, listdir
from os.path import exists

from execute import execute

# THIRD-PARTY IMPORTS #######################################################

import jemail
import raspicamera




# CONSTANTS #################################################################

SMTP_USERNAME = "smtp_username"
SMTP_PASSWORD = "smtp_password"
EMAIL_TO = "myemail@goes.here"
SUBJECT = "subject"
RECIPIENT_NAME = "your name"

# digits you are about to convert
NUMBER_OF_DIGITS = 5

# Absolute _path to the directory where the python _files are stores
# this will help to run it in the crontabs
APP_PATH = 'full _path to the application directory'

TEMP_DIR = APP_PATH + 'temporary/'

# name of the first image
IMAGE_IN = TEMP_DIR + 'img.jpg'

# name of the image after the convertion
IMAGE_OUT = TEMP_DIR + 'out.jpg'


# VARIABLES #################################################################

# CLASSES ###################################################################

# FUNCTIONS #################################################################


def begin():

    """
    Entry point for code.  Takes no arguments.

    """
    message = "Hello " + RECIPIENT_NAME + ",\n\n\n"

    try:
        # create temporary directory to store the images
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)
        # Process the picture
        raspicamera.take_picture(IMAGE_IN)
        convert_image(IMAGE_IN, IMAGE_OUT)
        reading = cut_zero(convert_image_to_text(IMAGE_OUT, NUMBER_OF_DIGITS))

        # email message with the result (edit to needs)
        message += "Your current credit is " + reading + " pounds."
    # bad practice not to specify what type of error you want to handle like this!
    except:
        # error message
        message = "Monitoring system has come up to a error, please contact developer."

    message += "\n\nRegards\nYour Rasperry Pi"
    jemail.send_email(SUBJECT, message, EMAIL_TO, SMTP_USERNAME, SMTP_PASSWORD)
    # clear the images
    clean_dir(TEMP_DIR)


def convert_image(imagename, output_image, size=None, margin=None, resize=None, threshold=None):
    """

    :param imagename:  name of the image you want to read
    :param output_image:  name of the image you want to create
    :param size:  trimmed size of the image
    :param margin:  any margins that you want to add
    :param resize:  resized size as a percentage
    :param threshold:  some threshold or other!
    """

    # size[0] = width of the new image being cut out
    # size[1] = height of the new image being cut out
    if size is None:
        _size = [560, 200]
    else:
        _size = size

    # margin[0] = left margin (pixels)
    # margin[1] = top margin (pixels)
    if margin is None:
        _margin = [290, 140]
    else:
        _margin = margin

    # size of the output image
    if resize is None:
        _resize = 20  # <- percent of original
    else:
        _resize = resize

    if threshold is None:
        _threshold = 2
    else:
        _threshold = threshold

# # picture setting commands
# cmd = '/usr/bin/convert ' + imagename
# cmd += ' -crop ' + str(_size[0]) + 'x' + str(_size[1])
# cmd += '+' + str(_margin[0]) + '+' + str(_margin[1])
# cmd += ' -resize ' + str(_resize)
# cmd += '% -threshold ' + str(_threshold) + '% ' + output_image

    cmd = """/usr/bin/convert {0} -crop {1}x{2}+{3}x{4} -resize {5}% -threshold {6}% {7}
        """.format(imagename,  # 0
                   str(_size[0]),  # 1
                   str(_size[1]),  # 2
                   str(_margin[0]),  # 3
                   str(_margin[1]),  # 4
                   str(_resize),  # 5
                   str(_threshold),  # 6
                   output_image  # 7
                   )

    cmd_list = cmd.split(' ')

    print cmd_list

    # picture processing
    output = execute(cmd_list)  # what is this actually doing?
    # check if the returned value is good enough.


def convert_image_to_text(img, number_of_digits):
    """

    :param img:  image to convert
    :param number_of_digits:  number of digits you want to read
    :return:
    """
    returned_image = getoutput('/usr/local/bin/ssocr -d ' + str(number_of_digits) + ' ' + img)
    return returned_image

def clean_dir(_path):
    """

    :param _path:  path to clean
    """
    _file = listdir(_path)
    for i in range(0, len(_file)):
        if exists(_path + _file[i]):
            remove(_path + _file[i])


def cut_zero(var):
    """

    :param var:  no idea what this is doing really!
    :return:
    """
    if var[:1] == '0':
        return var[1:]
    else:
        return var


def main():
    """


    """
    begin()

###############################################

if __name__ == "__main__":
    main()
