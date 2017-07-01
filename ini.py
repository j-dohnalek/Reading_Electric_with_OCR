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

# IMPORTS ###################################################################

from ConfigParser import SafeConfigParser
import os
import os.path

# CONSTANTS #################################################################

MAIL = '/home/shares/nas/smartCam/conf/email.ini'
USER = '/home/shares/nas/smartCam/users.ini'
CONF = '/home/shares/nas/smartCam/conf/config.ini'

# FUNCTIONS #################################################################


def get_email_setting(section, option, _return=None):
    """
    :param section: section to retrieve from INI file
    :param option: option to retrieve from INI file
    """

    parser = SafeConfigParser()
    parser.read(MAIL)

    if _return is None:
        return str(parser.get(section, option))
    elif _return == 'int':
        return parser.getint(section, option)


def get_conf_setting(section, option, _return=None):
    """
    :param section: section to retrieve from INI file
    :param option: option to retrieve from INI file
    """

    parser = SafeConfigParser()
    parser.read(CONF)

    if _return is None:
        return str(parser.get(section, option))
    elif _return == 'int':
        return parser.getint(section, option)


def get_user_info(num):

    user = []
    from ConfigParser import SafeConfigParser

    parser = SafeConfigParser()
    parser.read(USER)

    section = "user" + str(num + 1)
    if parser.has_section(section):
        for name in parser.options(section):
            user.append(parser.get(section, name))

    return user


def users_list():

    _list = []

    for i in range(10):
        if len(get_user_info(i)) is not 0:
            _list.append(get_user_info(i))

    return _list


def read_file(_file):
    check_file_exists(_file)

    f = open(_file, "r")
    data = f.read()
    f.close()

    return data


def write_to_file(_file, data):
    check_file_exists(_file)

    f = open(_file, "w")
    f.write(data)
    f.close()


def check_file_exists(_file):
    if not os.path.exists(_file):
        f = open(_file, "w")
        f.write('0')
        f.close()


def clean_directory(path):
    """

    :param _path:  path to clean
    """

    _file = os.listdir(path)

    for i in range(0, len(_file)):
        if os.path.exists(path + '/' + _file[i]):
            os.remove(path + '/' + _file[i])


def setup(path):
    """ Set up the folder structure """
    if not os.path.exists(path + get_conf_setting('general', 'temp')):
        os.makedirs(path + get_conf_setting('general', 'temp'))
    if not os.path.exists(path + get_conf_setting('general', 'cache')):
        os.makedirs(path + get_conf_setting('general', 'cache'))
