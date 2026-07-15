from db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String, nullable=False)

    admin_email_id = db.Column(db.String)
    student_email_id = db.Column(db.String)
    hr_email_id = db.Column(db.String)

    student = db.relationship("Student", back_populates="user")
    company = db.relationship("Company", back_populates="user")
    admin = db.relationship("Company", back_populates="user")
