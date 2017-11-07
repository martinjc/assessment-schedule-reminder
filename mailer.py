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

    def build_msg(self, send_from, send_to, subject, text_body=None, html_body=None, files=[]):

        # header
        self.msg = MIMEMultipart('alternative')
        self.msg['From'] = send_from
        self.msg['To'] = send_to
        self.msg['Date'] = formatdate(localtime=True)
        self.msg['Subject'] = subject

        if text_body:
            self.msg.attach(MIMEText(text_body, 'plain'))
        if html_body:
            self.msg.attach(MIMEText(html_body, 'html'))

        # attach files
        for f in files:
            with open(f, 'rb') as attach_file:
                part = MIMEApplication(
                    attach_file.read(),
                    Name = os.path.basename(f)
                )
                part['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(f)
                self.msg.attach(part)


    def send(self, send_from, send_to, subject, text_body=None, html_body=None, files=[]):

        self.build_msg(send_from, send_to, subject, text_body, html_body, files)

        """authenticate with SMTP server and send email"""
        self.sender = smtplib.SMTP(self.server, self.port)
        self.sender.ehlo()
        self.sender.starttls()
        self.sender.login(self.uname, self.pwd)
        print("SENDING MESSAGE!")
        self.sender.sendmail(send_from, send_to, self.msg.as_string())
        self.sender.quit()


    def mock(self, send_from, send_to, subject, text_body=None, html_body=None, files=[]):
        self.build_msg(send_from, send_to, subject, text_body, html_body, files)
        # save the message rather than send it
        with open('test-send-%s.txt' % subject, 'w') as email_file:
            email_file.write(self.msg.as_string())
