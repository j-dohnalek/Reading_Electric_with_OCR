import os
import csv
import sys
import os.path

from time import gmtime, strftime


def write_csv_error_log(_atfile, _function, _error):
    """

    :param _atfile: file where there error appeared
    :param _function: function where error appeared
    :param _error: error which was triggered
    """
    _date = strftime("%d%m%y", gmtime())
    _time = strftime("%H%M%S", gmtime())

    directory = 'cache/'
    _file = 'debug.csv'

    if not os.path.exists(directory + _file):
        log_message = [
                        ['Date', 'Time', 'File', 'Function', 'Error'],
                        [_date, _time, _atfile, _function, _error]
                      ]
    else:
        log_message = [[_date, _time, _atfile, _function, _error]]

    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory + _file, 'ab') as f:
            writer = csv.writer(f, delimiter=';',
                                   quotechar='|',
                                   quoting=csv.QUOTE_NONE,
                                   escapechar='\\')
            writer.writerows(log_message)
    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))


def creat_log_file():
    """

    function creates the log file for the script
    the file is only created not to trigger email
    attachement error of missing file
    """

    directory = 'cache/debug/'
    _file = 'error_log.csv'

    if not os.path.exists(directory + _file):
        log_message = [
                        ['Date', 'Time', 'File', 'Function', 'Error']
                      ]
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(directory + _file):
            with open(directory + _file, 'ab') as f:
                writer = csv.writer(f)
                writer.writerows(log_message)
    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
