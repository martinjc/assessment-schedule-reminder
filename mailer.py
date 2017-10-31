from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import smtplib
import os

class Mailer:
    """mailer"""

    def __init__(self, uname, pwd, server, port):

        self.uname = uname
        self.pwd = pwd
        self.server = server
        self.port = port


    def send(self, send_from, send_to, subject, body, files=[]):

        # header
        self.msg = MIMEMultipart()
        self.msg['From'] = send_from
        self.msg['To'] = COMMASPACE.join(send_to)
        self.msg['Date'] = formatdate(localtime=True)
        self.msg['Subject'] = subject

        self.msg.attach(MIMEText(body, 'plain'))

        # attach files
        for f in files:
            with open(f, 'rb') as attach_file:
                part = MIMEApplication(
                    attach_file.read(),
                    Name = os.path.basename(f)
                )
                part['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(f)
                self.msg.attach(part)

        """authenticate with SMTP server and send email"""
        self.sender = smtplib.SMTP(self.server, self.port)
        self.sender.ehlo()
        self.sender.starttls()
        self.sender.login(self.uname, self.pwd)
        self.sender.sendmail(send_from, send_to, self.msg.as_string())
        self.sender.quit()
