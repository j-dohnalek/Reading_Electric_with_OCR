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
