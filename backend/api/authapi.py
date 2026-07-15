import os
from datetime import datetime, timedelta, timezone

import jwt
from flask import jsonify, request
from flask_restful import Resource
from werkzeug.security import check_password_hash

from ApiException.ApiError import AuthenticationError, NotFoundError,ValidationError
from models import Admin, Company, Student


class AuthApi(Resource):
    # Login route for different users
    def post(self):
        data = request.get_json()
        role = data.get("role")

        email_id = data.get("email_id") or data.get("hr_email")
        password = data.get("password")

        if email_id is None or password is None or role is None :
            raise ValidationError({"error" : "Missing Fields" },400)

        if role == "student":
            entity = Student.query.filter(Student.email_id == email_id).first()

        elif role == "company":
            entity = Company.query.filter(Company.hr_email == email_id).first()

        else:
            entity = Admin.query.filter(Admin.email_id == email_id).first()

        if entity is None:
            raise NotFoundError({"error": f"No Such {role}"}, 404)

        if not check_password_hash(entity.password, password):
            raise AuthenticationError({"error": "Incorrect Credentials"}, 401)

        if role != "admin" and entity.approval_status == "rejected":
            return {"status": "banned"}, 403

        token = jwt.encode(
            {
                "role": role,
                "id": entity.id,
                "exp": datetime.now(timezone.utc) + timedelta(days=7),
            },
            os.getenv("SECRET_KEY"),
            algorithm="HS256",
        )

        response = jsonify({"id": entity.id})

        response.set_cookie(
            "access_token",
            token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=60 * 60 * 24 * 7,
        )

        return response
