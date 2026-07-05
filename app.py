from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

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

# ---------------- EMAIL (BREVO) ----------------
def send_email_via_brevo_api(subject, body):
    BREVO_API_KEY = os.getenv("BREVO_API_KEY")

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "name": "Priest Services Website",
            "email": "srikaryasidditempleusa@gmail.com"
        },
        "to": [
            {"email": "acharya88@gmail.com"},
            {"email": "mkarthikreddy27@gmail.com"}
        ],
        "subject": subject,
        "textContent": body
    }

    response = requests.post(url, json=payload, headers=headers, timeout=120)
    response.raise_for_status()


# ---------------- ADMIN ----------------
class AdminUser(db.Model, UserMixin):
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ---------------- OPTIONAL MODELS (KEEP IF NEEDED LATER) ----------------
class Inquiry(db.Model):
    __tablename__ = 'inquiries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- LOGIN ----------------
@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))


# ---------------- ROUTES ----------------

# HOME (Priest Landing Page)
@app.route("/")
def home():
    return render_template("home-page.html")


# ABOUT PRIEST
@app.route("/index")
def index():
    return render_template("index.html")


# PRIEST SERVICES PAGE
@app.route("/priest-services")
def priest_services():
    return render_template("priest-services.html")


# POOJA ITEMS PAGE
@app.route("/pooja-items")
def pooja_items():
    return render_template("pooja-items.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


# CONTACT / INQUIRY (optional future form)
# @app.route("/contact", methods=["GET", "POST"])
# def contact():
#     if request.method == "POST":
#         name = request.form.get("name")
#         email = request.form.get("email")
#         phone = request.form.get("phone")
#         message = request.form.get("message")

#         new_inquiry = Inquiry(
#             name=name,
#             email=email,
#             phone=phone,
#             message=message
#         )

#         db.session.add(new_inquiry)
#         db.session.commit()

#         send_email_via_brevo_api(
#             subject="New Priest Service Inquiry",
#             body=f"""
# Name: {name}
# Email: {email}
# Phone: {phone}
# Message: {message}
# """
#         )

#         flash("Your request has been submitted successfully!", "success")
#         return redirect(url_for("home"))

#     return render_template("contact.html")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=False)