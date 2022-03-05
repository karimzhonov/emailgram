import os

TOKEN = os.environ.get('token')
APPNAME = '<b>📧 Emailgram 📱</b>'

ROUTER_DICT = {
    'mail': 'Mail',
    'gmail': 'Gmail',
    'email_inbox': 'Inbox',
    'email_sent': 'Sent',
    'add_email': 'Add Account',
}

ERROR_AUTH_TEXT = 'Error while auth'