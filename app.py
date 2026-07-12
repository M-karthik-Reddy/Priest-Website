from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
# from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

import requests
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f1544168ff729e8e6ed58803541886d07'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///priest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

CORS(app)

# app.config['MAIL_SERVER'] = os.getenv('EMAIL_HOST')
# app.config['MAIL_PORT'] = int(os.getenv('EMAIL_PORT', 587))
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = os.getenv('EMAIL_HOST_USER')
# app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_HOST_PASSWORD')
# app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_HOST_USER')

# mail = Mail(app)

import requests
import os

# def send_email_via_brevo_api(subject, body):
#     brevo_api_key = os.getenv("BREVO_API_KEY")
#     if not brevo_api_key:
#         raise ValueError("BREVO_API_KEY is missing in .env")

#     url = "https://api.brevo.com/v3/smtp/email"
#     headers = {
#         "accept": "application/json",
#         "api-key": brevo_api_key.strip(),
#         "content-type": "application/json"
#     }

#     payload = {
#         "sender": {
#             "name": "Temple Website",
#             "email": "srikaryasidditempleusa@gmail.com"
#         },
#         "to": [
#             {"email": "acharya88@gmail.com"}
#         ],
#         "subject": subject,
#         "textContent": body
#     }

#     response = requests.post(url, json=payload, headers=headers, timeout=120)
#     print("Brevo status:", response.status_code)
#     print("Brevo response:", response.text)
#     response.raise_for_status()

def send_email_via_brevo_api(subject, body):
    brevo_api_key = os.getenv("BREVO_API_KEY")

    if not brevo_api_key:
        raise Exception("BREVO_API_KEY not found")

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": brevo_api_key,
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "name": "Temple Website",
            "email": os.getenv("DEFAULT_FROM_EMAIL")
        },
        "to": [
            {
                "email": "mkarthikreddy27@gmail.com"
            }
        ],
        "subject": subject,
        "textContent": body
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

    response.raise_for_status()



class AdminUser(db.Model, UserMixin):
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("home-page.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/priest-services")
def priest_services():
    return render_template("priest-services.html")

@app.route("/pooja-items")
def pooja_items():
    return render_template("pooja-items.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

from flask import request, redirect, url_for, flash, render_template
import smtplib
from email.mime.text import MIMEText

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    print("BREVO_API_KEY:", os.getenv("BREVO_API_KEY"))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')

        body = f"""New contact form submission

Name: {name}
Email: {email}
Phone: {phone}
Subject: {subject}

Message:
{message}
"""

        # try:
        #     msg = MIMEText(body)
        #     msg['Subject'] = f"Website Contact: {subject}"
        #     msg['From'] = os.getenv('DEFAULT_FROM_EMAIL', 'srikaryasidditempleusa@gmail.com')
        #     msg['To'] = 'mkarthikreddy27@gmail.com'

        #     smtp_host = os.getenv('EMAIL_HOST', 'smtp-relay.brevo.com')
        #     smtp_port = int(os.getenv('EMAIL_PORT', 587))
        #     smtp_user = os.getenv('EMAIL_HOST_USER')
        #     smtp_password = os.getenv('EMAIL_HOST_PASSWORD')
            
        #     print("SMTP HOST:", smtp_host)
        #     print("SMTP PORT:", smtp_port)
        #     print("SMTP USER:", smtp_user)
        #     print("SMTP PASSWORD EXISTS:", smtp_password is not None)
        #     print("FROM:", msg["From"])

        #     with smtplib.SMTP(smtp_host, smtp_port) as server:
        #         server.starttls()
        #         server.login(smtp_user, smtp_password)
        #         server.sendmail(msg['From'], [msg['To']], msg.as_string())
        #     print("Mail sent ! ")
        #     flash('Your message has been sent successfully!', 'success')
        # except Exception as e:
        #     flash(f'Error sending email: {e}', 'danger')
        
        
        try:
            print("BREVO_API_KEY:", os.getenv("BREVO_API_KEY"))

            send_email_via_brevo_api(
                subject=f"Website Contact: {subject}",
                body=body
            )

            flash("Your message has been sent successfully!", "success")

        except Exception as e:

            print(e)
            flash(f"Error sending email: {e}", "danger")

        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)