from datetime import datetime

from flask_marshmallow import Marshmallow
from marshmallow import EXCLUDE, validate

ma = Marshmallow()


class StudentSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    photo_path = ma.String(allow_none=True, validate=validate.Length(max=500))
    first_name = ma.String(required=True, validate=validate.Length(min=2, max=50))
    last_name = ma.String(required=True, validate=validate.Length(min=1, max=50))

    email_id = ma.Email(required=True)
    phone_no = ma.String(
        required=True,
        validate=validate.Regexp(r"\d{10}$", error="Invalid phone number"),
    )

    cgpa = ma.Float(required=True, validate=validate.Range(min=0, max=10))
    graduation_year = ma.Integer(
        required=True, validate=validate.Range(min=2020, max=datetime.now().year + 10)
    )
    branch = ma.String(required=True, validate=validate.Length(min=2, max=100))
    degree = ma.String(required=True)

    approval_status = ma.String(
        validate=validate.OneOf(["approved", "rejected", "pending"])
    )

    password = ma.String(
        required=True, load_only=True, validate=validate.Length(min=2, max=128)
    )


class CompanySchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    name = ma.String(required=True, validate=validate.Length(min=2, max=120))
    website = ma.URL(required=True)
    hr_email = ma.Email(required=True)
    hr_phone = ma.String(
        required=True,
        validate=validate.Regexp(r"^\d{10}$", error="Invalid phone number"),
    )
    hq_address = ma.String(required=True, validate=validate.Length(min=5, max=300))

    tagline = ma.String(required=True, validate=validate.Length(min=5, max=200))
    industry = ma.String(required=True, validate=validate.Length(min=2, max=100))
    founded_year = ma.Integer(
        required=True,
        validate=validate.Range(
            min=1800, max=datetime.now().year, error="Invalid founding year"
        ),
    )

    description = ma.String(required=True, validate=validate.Length(min=2, max=2000))
    no_of_offices = ma.Integer(required=True, validate=validate.Range(min=1, max=10000))
    staff_size = ma.Integer(
        required=True, validate=validate.Range(min=1, max=10_000_000)
    )

    approval_status = ma.String(
        validate=validate.OneOf(["approved", "rejected", "pending"])
    )
    password = ma.String(
        required=True, load_only=True, validate=validate.Length(min=2, max=128)
    )


class JobSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = ma.Integer(dump_only=True)
    title = ma.String(required=True, validate=validate.Length(min=1, max=50))
    location = ma.String(required=True, validate=validate.Length(min=1, max=100))
    salary = ma.String(required=True)
    experience = ma.String(required=True)
    is_closed = ma.Integer()
    application_deadline = ma.DateTime(required=True)
    approval_status = ma.String(
        validate=validate.OneOf(["pending", "approved", "rejected"])
    )
    description = ma.String(required=True)
    company_id = ma.Integer(required=True)


class ApplicationSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = ma.Integer(dump_only=True)
    created_at = ma.Integer(dump_only=True)
    status = ma.String(
        validate=validate.OneOf(["pending", "shortlisted", "selected", "rejected"])
    )
    resume_path = ma.String(allow_none=True)
    why_hire = ma.String(required=True)
    remark = ma.String()
    student_id = ma.Integer(required=True)
    student = ma.Nested(StudentSchema, dump_only=True)

    job_id = ma.Integer(required=True)
