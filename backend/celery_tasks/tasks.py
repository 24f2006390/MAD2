import csv
import os

from flask_mail import Message
from sqlalchemy import select

from app import app, mail
from celery_tasks.celery_app import celery
from celery_tasks.render_monthly_report import monthly_report_html
from db import db
from models import Application, Company, Job, Student


@celery.task
def say_hello():
    print("Hello!")


@celery.task
def send_daily_emails():

    with app.app_context():
        jobs = (
            Job.query.join(Company)
            .filter(
                Company.approval_status == "approved", Job.approval_status == "approved"
            )
            .order_by(Job.application_deadline.desc())
            .limit(5)
            .all()
        )

        html = """
            <h2>Latest Approved Jobs</h2>
            <ul>
        """

        for job in jobs:
            html += f"""
            <li>
                <b>{job.title}</b><br>
                Company: {job.company.name}<br>
                Location: {job.location}<br>
                Salary: {job.salary}<br>
                Deadline: {job.application_deadline:%d %b %Y}
            </li>
            <br>
            """

        html += "</ul>"

        emails = db.session.scalars(
            select(Student.email_id).where(Student.approval_status == "approved")
        ).all()

        msg = Message(subject="Latest Job Openings", recipients=emails, html=html)

        mail.send(msg)
    return "Successfully sent daily update to  users."


@celery.task
def send_admin_report():
    with app.app_context():
        msg = Message(
            subject="Monthly Report",
            recipients=["admin@example.com"],
            html=monthly_report_html,
        )

        mail.send(msg)


@celery.task
def sent_application_history(id):

    EXPORT_FOLDER = "exports"

    os.makedirs(EXPORT_FOLDER, exist_ok=True)

    with app.app_context():
        student_history = (
            db.session.query(
                Student.id.label("Student_id"),
                Company.name.label("Company_name"),
                Job.title.label("Job_title"),
                Application.status.label("Status"),
                Application.created_at.label("Date"),
            )
            .select_from(Application)
            .join(Student, Student.id == Application.student_id)
            .join(Job, Job.id == Application.job_id)
            .join(Company, Company.id == Job.company_id)
            .filter(Application.student_id == id)
            .all()
        )

        filename = f"student_{id}_applications.csv"
        filepath = os.path.join(EXPORT_FOLDER, filename)

        with open(filepath, "w") as f:
            csv_writer = csv.writer(f)

            csv_writer.writerow(
                [
                    "Student ID",
                    "Company Name",
                    "Job Title",
                    "Application Status",
                    "Application Date",
                ]
            )
            for row in student_history:
                csv_writer.writerow(list(row))

        student = Student.query.get(id)

        msg = Message(subject="Your Placement History", recipients=[student.email_id])
        msg.body = f"""
        Hello {student.first_name},

        Your placement application history has been exported successfully.

        The CSV file is attached to this email.

        Regards,
        Placement Portal
        """
        with open(filepath, "r") as f:
            msg.attach(filename, "text/csv", f.read())
        mail.send(msg)


# celery -A celery_app.celery worker --loglevel=info
