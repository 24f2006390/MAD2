from db import db


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
