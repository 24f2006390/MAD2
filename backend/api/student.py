from flask import request
from flask_restful import Resource, marshal

from api.base_api import BaseApi
from ApiException.ApiError import APIError, NotFoundError, ValidationError
from db import db
from models import Application, Company, Job, Student
from models.fields import application_fields, company_fields, job_fields, student_fields

class StudentDashboardApi(Resource):
    def get(self, id):

        student = Student.query.filter(Student.id == id).first()
        companies = Company.query.filter(Company.approval_status == "approved").all()
        jobs = (
            Job.query.join(Company)
            .filter(
                Company.approval_status == "approved", Job.approval_status == "approved"
            )
            .all()
        )
        applications = Application.query.filter(Application.student_id == id).all()

        application_count = len(applications)
        selected_application_ct = len(
            [app for app in applications if app["status"] == "selected"]
        )

        return {
            "student": marshal(student, student_fields),
            "companies": marshal(companies, company_fields),
            "jobs": marshal(jobs, job_fields),
            "total_app_ct": application_count,
            "selected_app_ct": selected_application_ct,
        }, 200


# Handles student routes
class StudentApi(BaseApi):
    def check_already_exists(self, data):

        student = Student.query.filter(Student.id == id).first()

        if student is not None:
            raise ValidationError({"error": "student already exists"}, 409)

    def patch(self, id):
        if "photo" in request.files:
            file = request.files["photo"]

            ext = file.filename.split(".")[-1]

            path = f"static/images/student_{id}.{ext}"
            file.save(path)

            student = db.session.get(Student, id)
            student.photo_path = path

            db.session.commit()
            return marshal(student, student_fields)

        else:
            return super().patch(id=id)


class ApplicationApi(BaseApi):
    def check_already_exists(self, data):

        student_id, job_id = data.get("student_id"), data.get("job_id")

        application = self.Model.query.filter(
            self.Model.student_id == student_id, self.Model.job_id == job_id
        ).first()

        if application is not None:
            raise APIError(
                {"error": "Multiple applications to the same job not allowed "}, 409
            )

    def post(self):
        data= request.form.to_dict()
        data = self.validate_data(data)
        self.check_already_exists(data)

        application =Application(**data)
        db.session.add(application)
        db.session.flush()

        file = request.files['resume']
        ext = file.filename.split(".")[-1]

        path = f"static/resumes/application_{application.id}.{ext}"
        file.save(path)

        application.resume_path = path
        db.session.commit()
        return marshal(application,application_fields)



    def validate_data(self, data, partial=False):
        data = super().validate_data(data, partial=partial)

        if not partial:
            # post request
            job_id = data.get("job_id")
            job = Job.query.get(job_id)
            if (
                job.approval_status != "approved"
                or job.company.approval_status != "approved"
            ):
                raise ValidationError({"error": "Can't Apply to UnApproved Jobs"}, 400)

        return data

    def get(self, student_id=None, job_id=None, company_id=None, id=None):
        if id is not None:
            application = db.session.get(Application, id)
            if application is None:
                raise NotFoundError({"error": "application not found"}, 404)

            return marshal(application, application_fields), 200
        else:
            if "company" in request.path:
                applications = (
                    Application.query.join(Job)
                    .join(Company)
                    .filter(Company.id == company_id)
                    .all()
                )

            elif "student" in request.path:
                applications = (
                    Application.query.join(Student)
                    .filter(Student.id == student_id)
                    .all()
                )

            elif "job" in request.path:
                applications = (
                    Application.query.join(Job).filter(Job.id == job_id).all()
                )

            else:
                applications = Application.query.all()

            return marshal(applications, application_fields), 200


class ExportHistory(Resource):
    def get(self, id):
        from celery_tasks.tasks import sent_application_history

        sent_application_history.delay(id)

        return "Application History Successfully sent on mail"
