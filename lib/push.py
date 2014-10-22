# IMPORTS ########################

import httplib
import urllib


def send_message(message, title=None):
    """

    Function sends push messages to the specified user

    :param from_ip: senders IP address
    :param message: Message to user
    :param title: Title of the message
    """

    app_token = 'YOUR APP TOKEN'
    usr_token = 'YOUR USER TOKEN'
    #device = 'nexus5'

    if title is None:
        _title = "Smart Home Notification"
    else:
        _title = title

    # Start your connection with the Pushover API server
    conn = httplib.HTTPSConnection("api.pushover.net:443")

    # Send a POST request in urlencoded json
    conn.request("POST", "/1/messages.json",
    urllib.urlencode({
    "token": app_token,
    "user": usr_token,
    #"device": device,
    "title": _title,
    "message": message,
    }), {"Content-type": "application/x-www-form-urlencoded"})

    # Listen for any error messages or other responses
    conn.getresponse()
