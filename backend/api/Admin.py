from flask_restful import Resource, marshal

from models import Application, Company, Job, Student
from models.fields import application_fields, company_fields, job_fields, student_fields


# Only Handles DashBoard Data Fetching
class AdminDashboardApi(Resource):
    def get(self):

        students = Student.query.all()
        companies = Company.query.all()
        jobs = Job.query.all()
        applications = Application.query.all()

        return {
            "students": marshal(students, student_fields),
            "companies": marshal(companies, company_fields),
            "jobs": marshal(jobs, job_fields),
            "applications": marshal(applications, application_fields),
        }, 200
