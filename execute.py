__author__ = 'ihavelock'

import sys
import subprocess


def execute(command, shell=False):

    """
    http://docs.python.org/2/library/subprocess.html?highlight=subprocess.call#subprocess.call

    Need to rewrite this to accept unix style commands!

    :param command: command needs to be a LIST, split at each space, so all command line parameters are actually
    strings within the list.
    :param shell:  Shell defaults to false, but can be overridden.  Only use this if you know what you're doing!
    :return:  returns a return code?
    """

    if sys.platform.startswith('win32'):
        # for Windows systems (not Cygwyn)

        return_code = subprocess.call(command, shell=False)
        # Standard Windows error return codes.
        # http://msdn.microsoft.com/en-us/library/ms681382(v=vs.85).aspx for details.
        if return_code == 0:
            print "The operation completed successfully."
        elif return_code == 1:
            print "Incorrect function."
        elif return_code == 2:
            print "The system cannot find the file specified."
        elif return_code == 3:
            print "The system cannot find the path specified."
        elif return_code == 4:
            print "The system cannot open the file."
        elif return_code == 5:
            print "Access is denied."

        return return_code

    elif sys.platform.startswith('darwin'):
        # for OS X
        pass

    elif sys.platform.startswith('linux2'):
        # for linux systems
        pass