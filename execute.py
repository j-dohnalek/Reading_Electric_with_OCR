__author__ = 'ihavelock'


def execute(command, shell=False):

    """
    command needs to be a LIST, split at each space, so all command line parameters are actually
    strings within the list.  Shell defaults to false, but can be overridden.

    Need to rewrite this to accept unix style commands!

    :param command: command must be a valid Windows command-prompt command.
    :param shell:
    :return:
    """
    return_code = subprocess.call(command, shell=False)

    # Standard Windows error return codes - http://msdn.microsoft.com/en-us/library/ms681382(v=vs.85).aspx for details.
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
