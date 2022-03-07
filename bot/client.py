import imap_tools.errors
from imap_tools import MailBox
import smtplib
from email.mime.text import MIMEText


class Client:
    imap_server_list = {
        'mail': 'imap.mail.ru',
        'gmail': 'imap.gmail.com',
    }

    smtp_server_list = {
        'mail': 'smtp.mail.ru:465',
        'gmail': 'smtp.gmail.com:587',
    }

    def __init__(self, email, password, server_name):
        self.email, self.password = email, password
        self.server_name = server_name
        self.imap_server_name = self.imap_server_list[self.server_name]
        self.smtp_server_name = self.smtp_server_list[self.server_name]

    def check_email(self):
        mail = MailBox(self.imap_server_name)
        try:
            mail.login(self.email, self.password)
            return mail.login_result[0]
        except imap_tools.errors.MailboxLoginError:
            return 'NO'

    def outbox(self):
        pass

    def send(self, subject, message, to_email):
        server = smtplib.SMTP_SSL(self.smtp_server_name)
        try:
            server.login(self.email, self.password)
            msg = MIMEText(message)
            msg['Subject'] = subject

            server.sendmail(self.email, to_email, msg.as_string())
            server.quit()
            return True
        except smtplib.SMTPRecipientsRefused:
            server.quit()
            return False

    def inbox(self, criteria='ALL'):
        with MailBox(self.imap_server_name).login(self.email, self.password) as mailbox:
            for mail in mailbox.fetch(criteria=criteria, reverse=True, ):
                yield {
                    'uid': mail.uid,
                    'from': mail.from_,
                    'subject': mail.subject,
                    'text': mail.text,
                    'date': mail.date,
                }
