import os

import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail

# Email Infrastructure
# --------------------

API_KEY = os.environ['SENDGRID_API_KEY']
sg = sendgrid.SendGridAPIClient(apikey=API_KEY)


def notify(subject, content, email_to, email_from):
    from_address = Email(email_from, name="MailSender.io")
    to_address = Email(email_to)
    content = Content('text/html', content)
    subject = subject

    mail = Mail(from_address, subject, to_address, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response
