from db import db


class Application(db.Model):
    __tablename__ = "application"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(
        db.String,
        info=["pending", "shortlisted", "selected", "rejected"],
        default="pending",
    )

    resume_path = db.Column(db.String, nullable=True)
    why_hire = db.Column(db.Text, nullable=True)
    remark = db.Column(db.Text, nullable=True)

    # Foreign Keys
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))

    # Relationships
    student = db.relationship("Student", back_populates="applications", lazy="joined")
    job = db.relationship("Job", back_populates="applications", lazy="joined")

    def __getitem__(self, key):
        return getattr(self, key)


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    photo_path = db.Column(db.String, nullable=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email_id = db.Column(db.String, nullable=False)
    phone_no = db.Column(db.String, nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    graduation_year = db.Column(db.String, nullable=False)
    approval_status = db.Column(db.String, default="approved")

    branch = db.Column(db.String, nullable=False)
    degree = db.Column(db.String, nullable=False)

    password = db.Column(db.String, nullable=False)

    # Foreign Keys

    # Relationship attribute must be Class Name not table name
    applications = db.relationship(
        "Application",
        back_populates="student",
        cascade="all , delete-orphan",
        lazy="joined",
    )

    def __getitem__(self, key):
        return getattr(self, key)
