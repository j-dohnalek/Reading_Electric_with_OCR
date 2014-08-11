__author__ = 'ihavelock'

import smtplib
import os

#particular imports

from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from email.Utils import formatdate


def send_email(subject, body, recipients, smtp_username, smtp_password, attachment=None):
    """
    Facilitates sending emails and massively-simplifies scripts.
    :param subject:  subject of the email
    :param body:  body/content of the email
    :param recipients:  recipients of the email as a comma separated string
    :param attachment: (optional) point this to a file object to be attached to the email
    """

    #smtp_username = "jiri@gmail.com"
    #smtp_password = "password"
    smtp_server = "smtp.gmail.com"
    ssl_port = 465

    # Generate and send an email containing the summary and the HTML as a file.
    print "\nPreparing to send email..."

    try:
        msg = MIMEMultipart()
        msg["From"] = smtp_username
        msg["To"] = recipients
        msg["Subject"] = subject
        msg['Date'] = formatdate(localtime=True)

        raw_html = """
        <html>
          <head></head>
          <body>
            <p>
               {0}
            </p>
          </body>
        </html>
        """

        html = raw_html.format(body)

        #Attach parts into message container.
        #According to RFC 2046, the last part of a multipart message, in this case
        #the HTML message, is best and preferred.
        msg.attach(MIMEText(html, 'html'))

        if attachment is not None:
            # attach a file
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(attachment, "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
            msg.attach(part)

        server = smtplib.SMTP_SSL(smtp_server, ssl_port)
        server.login(smtp_username, smtp_password)

        send_to = recipients.split(',')
        server.sendmail(smtp_username, send_to, msg.as_string())

        print "\nEmail sent!"

        server.quit()

    except Exception, e:
        errormsg = "\nUnable to send email. Error: %s" % str(e)
        print errormsg
