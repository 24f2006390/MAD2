from flask import g, request
from flask_restful import Resource, marshal

from api.base_api import BaseApi
from ApiException.ApiError import APIError, NotFoundError
from db import db
from models import Application, Company, Job
from models.fields import company_fields, job_fields



class CompanyApi(BaseApi):
    def check_already_exists(self, data):
        company = Company.query.filter(data["hr_email"] == Company.hr_email).first()
        if company is not None:
            raise APIError({"error": "company already exists"}, 409)


class JobApi(BaseApi):
    def get(self, company_id=None, student_id=None, id=None):
        if id is not None:
            job = db.session.get(Job, id)
            if job is None:
                return NotFoundError({"error": "job not found"}, 404)

            return marshal(job, self.entity_fields), 200
        else:
            if "company" in request.path:
                jobs = Job.query.filter(Job.company_id == company_id).all()
            elif "student" in request.path:
                jobs = Job.query.join(Application).filter(
                    Application.student_id == student_id
                )
            else:
                jobs = Job.query.all()

            if g.role == "student":
                jobs = [job for job in jobs if job.approval_status == "approved"]

            return marshal(jobs, self.entity_fields), 200

    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)
