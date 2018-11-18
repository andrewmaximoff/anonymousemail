import os

import sentry_sdk
import markdown

from flask_wtf import CSRFProtect
from flask import (
    Flask,
    render_template,
    request,
    Markup,
    redirect,
    jsonify
)
from sentry_sdk.integrations.flask import \
    FlaskIntegration

from .utils import notify

sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    integrations=[FlaskIntegration()]
)

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET', 'CHANGEME')
app.debug = os.environ.get('DEBUG', False)

csrf = CSRFProtect(app)


@app.route('/')
def index():
    return redirect('/send')


@csrf.exempt
@app.route('/send', methods=["GET", "POST"])
def send_email():
    if request.method == 'POST':
        body = request.form['body']
        subject = request.form['subject']
        email_to = request.form['emailTo']
        email_from = request.form['emailFrom']

        if not body or not subject or not email_from or not email_from:
            return jsonify(
                {
                    'message': 'Fields cannot be empty!',
                    'error': True,
                }
            )

        # Replace newlines with <br> tags.
        body = request.form['body']
        body = '---NEWLINE---'.join(body.split('\n'))

        # Strip any HTML away.
        body = Markup(body).striptags()
        subject = Markup(subject).striptags()

        body = markdown.markdown(body)
        body = '<br>'.join(body.split('---NEWLINE---'))

        sendgrid_response = notify(content=body, subject=subject, email_to=email_to, email_from=email_from)

        status_code = list(str(sendgrid_response.status_code))

        if status_code[0] == '2':
            return jsonify(
                {
                    'message': 'Letter sent!',
                    'error': False,
                }
            )
        elif status_code[0] == '4':
            return jsonify(
                {
                    'message': 'Oops! Something went wrong.',
                    'error': True,
                }
            )
        else:
            return jsonify(
                {
                    'message': 'Oops! Something went wrong.',
                    'error': True
                }
            )
    else:
        return render_template('send_email.html')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500
