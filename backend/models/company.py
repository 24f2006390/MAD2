from db import db


class Job(db.Model):
    __tablename__ = "job"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    salary = db.Column(db.String, nullable=False)
    experience = db.Column(db.String, nullable=False)
    is_closed = db.Column(db.Integer, default=0)

    application_deadline = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)

    company = db.relationship("Company", back_populates="jobs", lazy="joined")

    approval_status = db.Column(db.String, nullable=False, default="pending")
    #  pending approved rejected

    applications = db.relationship(
        "Application", back_populates="job", cascade="all, delete-orphan"
    )

    def __getitem__(self, key):
        return getattr(self, key)


class Company(db.Model):
    __tablename__ = "company"

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    website = db.Column(db.String, nullable=False)
    hr_email = db.Column(db.String, nullable=False)
    hr_phone = db.Column(db.String, nullable=False)
    hq_address = db.Column(db.String, nullable=False)

    tagline = db.Column(db.String, nullable=False)
    industry = db.Column(db.String, nullable=False)
    founded_year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    no_of_offices = db.Column(db.Integer, nullable=False)
    staff_size = db.Column(db.Integer, nullable=False)

    approval_status = db.Column(db.String, default="pending", nullable=False)

    password = db.Column(db.String, nullable=False)
    # Foreign Keys
    jobs = db.relationship(
        "Job", back_populates="company", cascade="all, delete-orphan"
    )

    def __getitem__(self, key):
        return getattr(self, key)
