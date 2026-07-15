from flask import request
from flask_restful import Resource, marshal
from werkzeug.security import generate_password_hash

from ApiException.ApiError import APIError, ValidationError
from db import db


class BaseApi(Resource):
    def __init__(self, Model, entity_schema, entity_fields):
        self.Model = Model
        self.entity_schema = entity_schema()
        self.entity_fields = entity_fields

    def check_already_exists(self, data):
        pass

    def validate_data(self, data, partial=False):
        try:
            data = self.entity_schema.load(data, partial=partial)

            if "password" in data:
                data["password"] = generate_password_hash(data["password"])

            return data
        except Exception as e:
            raise ValidationError({"error": f"{e}"}, status_code=400)

    def get(self, id=None):
        if id is not None:
            entity = db.session.get(self.Model, id)
            if entity is None:
                return {"error": "entity not found"}, 404

            entity = marshal(entity, self.entity_fields)

            return entity, 200
        else:
            entities = self.Model.query.all()

        return marshal(entities, self.entity_fields), 200

    # for registeration of users authentiation is not required.
    def post(self, *args, **kwargs):
        # validate data
        data = self.validate_data(request.get_json())

        self.check_already_exists(data)  # prevents creating same object multiple times

        try:
            entity = self.Model(**data)

            db.session.add(entity)
            db.session.commit()

            return marshal(entity, self.entity_fields), 201

        except Exception:
            raise APIError({"error": "unknown error occured "}, 500)

    def patch(self, id):
        #  Validate data first

        data = self.validate_data(request.get_json(), partial=True)

        entity = db.session.get(self.Model, id)
        if entity is None:
            return {"error": "entity not found"}, 404

        for key, val in data.items():
            setattr(entity, key, val)
        db.session.commit()

        return marshal(entity, self.entity_fields), 201

    def delete(self, id):
        entity = db.session.get(self.Model, id)
        if entity is None:
            return {"error": "entity not found"}, 404

        db.session.delete(entity)
        db.session.commit()
        return "Successfully Deleted", 200
