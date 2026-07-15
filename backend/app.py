import os
import time


from dotenv import load_dotenv
from flask import Flask, request, g, jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_mail import Mail
from werkzeug.security import generate_password_hash
from security import check_authentication, check_authorization
from ApiException.ApiError import APIError

from api import (
    ApplicationApi,
    AuthApi,
    CompanyApi,
    JobApi,
    StudentApi,
    AdminDashboardApi,
    CompanyDashboardApi,
    StudentDashboardApi,
    ExportHistory
)

from db import db
from models import Admin, Application, Company, Job, Student
from models.fields import application_fields, company_fields, job_fields, student_fields
from models.schema import ApplicationSchema, CompanySchema, JobSchema, StudentSchema


load_dotenv()

app = Flask(__name__)
app.config.from_pyfile("config.py")
api = Api(app)
db.init_app(app)
mail = Mail(app)
CORS(app, origins="*", supports_credentials=True)


api.add_resource(
    CompanyApi,
    "/api/company/<int:id>/",
    "/api/companies/",
    "/api/company/",
    resource_class_args=(Company, CompanySchema, company_fields),
)

# Jobs
api.add_resource(
    JobApi,
    "/api/job/<int:id>/",
    "/api/jobs/",
    "/api/job/",
    "/api/company/<int:company_id>/jobs/",
    "/api/student/<int:student_id>/jobs/",
    resource_class_args=(Job, JobSchema, job_fields),
)

# Students
api.add_resource(
    StudentApi,
    "/api/student/<int:id>/",
    "/api/students/",
    "/api/student/",
    resource_class_args=(Student, StudentSchema, student_fields),
)

# Applications
api.add_resource(
    ApplicationApi,
    "/api/application/<int:id>/",
    "/api/applications/",
    "/api/application/",
    "/api/student/<int:student_id>/applications/",
    "/api/job/<int:job_id>/applications/",
    "/api/company/<int:company_id>/applications/",
    resource_class_args=(Application, ApplicationSchema, application_fields),
)

api.add_resource(AuthApi, "/api/login/")
api.add_resource(CompanyDashboardApi, "/api/company_dash_data/<int:id>/")
api.add_resource(AdminDashboardApi, "/api/admin_dash_data/")
api.add_resource(StudentDashboardApi, "/api/student_dash_data/<int:id>/")
api.add_resource(ExportHistory, "/api/student/<int:id>/export/")

@app.errorhandler(APIError)
def handle_api_error(error):
    response = jsonify(error.message_dict)
    response.status_code = error.status_code
    return response


UNAUTHENTICATED_ROUTES = {
    ("POST", "/api/login/"),
    ("POST", "/api/student/"),
    ("POST", "/api/company/"),
}


@app.before_request
def before():

    g.start_time = time.perf_counter()
    # unregistered 404 routes
    if request.url_rule is None:
        return

    if (request.method.upper(), request.path) in UNAUTHENTICATED_ROUTES:
        return

    if request.method.lower() == "options":
        return

    if request.path.startswith(("static", "/static")):
        return

    check_authentication()

    check_authorization()


@app.after_request
def after(response):
    if request.url_rule is None:
        return response

    response.headers["X-Response-Time"] = (
        str(time.perf_counter() - g.start_time) + " seconds"
    )


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
