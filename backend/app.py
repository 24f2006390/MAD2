import os

from dotenv import load_dotenv
from flask import Flask
from werkzeug.security import generate_password_hash

from db import db
from models import Admin

load_dotenv()

app = Flask(__name__)
app.config.from_pyfile("config.py")

db.init_app(app)





def admin_setup():

    password = os.getenv("ADMIN_PASSWORD")
    email_id = os.getenv("ADMIN_EMAIL")
    password = generate_password_hash(password)

    admin = Admin.query.filter_by(email_id=email_id).first()

    if admin is None:
        admin = Admin(email_id=email_id, password=password)
        db.session.add(admin)
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        admin_setup()
    app.run(port=5000, debug=True)
