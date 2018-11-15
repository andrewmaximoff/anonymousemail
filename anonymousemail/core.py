import os

from flask import (
    Flask,
    render_template,
    request,
    Markup,
    redirect,
    jsonify
)
from .utils import notify

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET', 'CHANGEME')
app.debug = os.environ.get('APP_SECRET', False)


@app.route('/')
def index():
    return redirect('/send')


@app.route('/send', methods=["GET", "POST"])
def send_email():
    if request.method == 'POST':
        body = request.form['body']
        email = request.form['email']
        response = notify(body, email)

        status_code = list(str(response.status_code))

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
