import os

import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail

# Email Infrastructure
# --------------------

API_KEY = os.environ['SENDGRID_API_KEY']
sg = sendgrid.SendGridAPIClient(apikey=API_KEY)


def notify(content, email_address):
    from_address = Email('no-reply@mailsender.io', name="MailSender.io")
    to_address = Email(email_address)
    content = Content('text/plain', str(content))
    subject = 'Anonymous letter'

    mail = Mail(from_address, subject, to_address, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response
