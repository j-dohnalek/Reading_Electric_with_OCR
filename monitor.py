#!/usr/bin/python

# ############################################################################
#    monitor.py - Python 2.7
#    Copyright (C) 2014 Jiri Dohnalek
#    Last update: 13.9.2014
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
# ###########################################################################

#  IMPORTS ##################################################################

import os
import os.path
import subprocess
import time
import datetime
import sys

from pytz import timezone

# THIRD-PARTY IMPORTS #######################################################

from lib import ini
from lib import jemail
from lib import raspicamera
from lib import debug

# CONSTANTS #################################################################

# Absolute _path to the directory where the python _files are stores
# this will help to run it in the crontabs
PATH = os.getcwd()

# FUNCTIONS #################################################################


def begin():

    """  Entry point for code.  Takes no arguments.  """

    start = time.time()  # measure execution time of the script
    ini.setup(PATH)
    latest_meter_reading()
    ini.clean_directory(PATH + ini.get_conf_setting('general', 'temp'))

    print "Script execution time %5.2f seconds." % (time.time() - start)


def count_consumtion(credit):
    """
    :param credit: current credit
    """

    last = ini.read_file(PATH + ini.get_conf_setting('files', 'last_reading'))
    if len(last) is 0:
        return False
    else:
        last = float(last)

    current = float(credit)

    if current > last:
        return False
    else:
        return last - current


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
    cmd_list = cmd.split()

    try:
        returned_text = subprocess.check_output(cmd_list)
        if len(returned_text.strip()) is number_of_digits:
            return float(returned_text)
        else:
            print("Not enough digits found!")

    except subprocess.CalledProcessError as err:
        debug.write_csv_error_log('monitor.py', 'convert_image_to_text()', err)


def latest_meter_reading():

    credit = 0

    image_in = PATH + ini.get_conf_setting('files', 'raw_image')
    image_out = PATH + ini.get_conf_setting('files', 'ready_image')

    for i in range(ini.get_conf_setting('variable', 'max_attempts', 'int')):

        # Process the picture
        raspicamera.take_picture(image_in)
        convert_image(image_in, image_out)
        credit = convert_image_to_text(image_out, ini.get_conf_setting('variable', 'digits', 'int'))

        if isinstance(credit, float):

            # send email to user and update last reading file
            send_html_email(credit)
            ini.write_to_file(PATH + ini.get_conf_setting('files', 'last_reading'), str(credit))
            return

        else:

            ini.clean_directory(PATH + ini.get_conf_setting('general', 'temp'))

    # kill the application after the max attempts is crossed
    return sys.exit("Application have failed to get the meter reading.")


def send_html_email(credit):

    # set current time zone
    time_zone = timezone(ini.get_conf_setting('general', 'timezone'))
    current_time_zone = datetime.datetime.now(time_zone)

    # email settings
    smtp_user = ini.get_email_setting('email', 'smtp_username')
    smtp_pass = ini.get_email_setting('email', 'smtp_password')
    subject = ini.get_email_setting('email', 'subject')

    # user settings
    users = ini.users_list()

    # count consumption
    consumption = ''
    if count_consumtion(credit) is not False:
        consumption = """Consumption from last reading: &pound;%.2f <br>""" % count_consumtion(credit)

    for user in users:

        if user[2] == 'yes':

            # message build
            msg = """
                    Hello {0},
                    <br><br>
                    This is a message from you automated system to monitor reamining credit on your electric meter. The
                    current version of the system is 0.14.9
                    <h3>
                        Current balance: &pound;{1} <br />
                        {2}
                        Reading Date: {3}
                    </h3>

                    <br>Regards
                    <br>Your Rasperry Pi Automated System"
            """.format(user[1],  # 0
                       str("%.2f" % credit),  # 1
                       consumption,  # 2
                       str(current_time_zone.strftime('%H:%M:%S %d.%m.%Y'))  # 3
                       )

            # sends the email
            print("Sending email to {0}, {1}".format(user[1], user[0]))
            jemail.send_email(subject, msg, user[0], smtp_user, smtp_pass)


def main():
    begin()

###############################################

if __name__ == "__main__":
    main()
