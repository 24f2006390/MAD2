import os

import jwt
from flask import g, request

from ApiException.ApiError import AuthenticationError
from models import Application, Job


def check_authentication():

    token = request.cookies.get("access_token")

    if token is None:
        raise AuthenticationError({"error": "Not Authenticated"}, 401)

    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        raise AuthenticationError({"error": "Token Expired"}, 401)

    except jwt.InvalidSignatureError:
        raise AuthenticationError({"error": "Invalid Token"}, 401)

    g.role = payload["role"]
    g.id = payload["id"]


def check_student_permissions():
    GET_ONLY_ROUTES = [
        "/api/companies/",
        "/api/company/",
        "/api/jobs/",
        "/api/job/",
        "/api/job/<int:id>/",
        "/api/company/<int:id>/",
        "/api/company/<int:company_id>/jobs/",
    ]
    POST_ONLY_ROUTES = ["/api/application/"]

    print(request.url_rule, "url rule")
    if request.method.lower() == "get":
        # allow
        if request.path in GET_ONLY_ROUTES:
            return
        if request.url_rule.rule in GET_ONLY_ROUTES:
            return

    if request.method.lower() == "post" and request.path in POST_ONLY_ROUTES:
        # allow
        return

    id_match = [
        "/api/student_dash_data/<int:id>/",
        "/api/student/<int:id>/export/",
        "/api/student/<int:student_id>/applications/",
        "/api/student/<int:id>/",
        "/api/student/<int:student_id>/jobs/",
    ]
    if request.url_rule.rule in id_match:
        student_id = request.view_args.get("id") or request.view_args.get("student_id")
        if student_id == g.id:
            return

    if request.url_rule.rule == "/api/application/<int:id>/":
        app_id = request.view_args.get("id")

        app = Application.query.filter(Application.id == app_id).first()

        if app is not None:
            if app.student_id == g.id:
                return
        else:
            return

    raise AuthenticationError({"error": "Forbidden"}, 403)


def check_company_permissions():

    GET_ONLY_ROUTES = [
        "/api/students/",
        "/api/student/",
        "/api/jobs/",
        "/api/job/",
    ]

    POST_ONLY_ROUTES = [
        "/api/job/",
    ]

    print(request.url_rule)

    if request.method.lower() == "get" and request.path in GET_ONLY_ROUTES:
        return

    if request.method.lower() == "post" and request.path in POST_ONLY_ROUTES:
        return

    if (
        request.method.lower() == "get"
        and request.url_rule.rule == "/api/application/<int:id>/"
    ):
        return

    if (
        request.method.lower() == "get"
        and request.url_rule.rule == "/api/student/<int:id>/"
    ):
        return

    if (
        request.method.lower() == "get"
        and request.url_rule.rule == "/api/student/<int:student_id>/applications/"
    ):
        return

    id_match = [
        "/api/company/<int:id>/",
        "/api/company_dash_data/<int:id>/",
        "/api/company/<int:company_id>/jobs/",
        "/api/company/<int:company_id>/applications/",
    ]

    if request.url_rule.rule in id_match:
        company_id = request.view_args.get("id") or request.view_args.get("company_id")

        if company_id == g.id:
            return

    if request.url_rule.rule == "/api/job/<int:id>/":
        job_id = request.view_args.get("id")

        job = Job.query.get(job_id)

        if job is not None and job.company_id == g.id:
            return

        if job is None:
            return

        raise AuthenticationError({"error": "Forbidden"}, 403)

    if request.url_rule.rule == "/api/application/<int:id>/":
        app_id = request.view_args.get("id")

        application = Application.query.get(app_id)

        if application is not None:
            job = application.job

            if job.company_id == g.id:
                return

        raise AuthenticationError({"error": "Forbidden"}, 403)

    if request.url_rule.rule == "/api/job/<int:job_id>/applications/":
        job_id = request.view_args.get("job_id")
        job = Job.query.get(job_id)

        print("job company_id", job.company_id)
        print("role id", g.id)

        if job is None:
            return
        elif job.company_id == g.id:
            return

    raise AuthenticationError({"error": "Forbidden"}, 403)


def check_authorization():
    if g.role == "admin":
        return

    if g.role == "student":
        check_student_permissions()

    if g.role == "company":
        check_company_permissions()
