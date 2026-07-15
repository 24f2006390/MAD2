import json

import redis
from flask import request

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

cached_urls = ["/api/student_dash_data/<int:id>/", "/api/company_dash_data/<int:id>/"]
cached_endpoints = [
    "/api/applications/",
    "/api/jobs/",
    "/api/companies/",
    "/api/students/",
    "/api/admin_dash_data/"
]


def fetch_cached_response():
    if request.method.upper() != "GET":
        return

    if request.url_rule.rule in cached_urls:
        key = request.method + request.path
        if redis_client.exists(key):
            print("cache hit")
            return json.loads(redis_client.get(key))

    if request.path in cached_endpoints:
        key = request.method + request.path
        print(key)
        if redis_client.exists(key):
            print("cache hit")
            return json.loads(redis_client.get(key))

    return None


def cache_response(response):
    # Invalidate Cache
    if request.method.upper() != "GET":
        if request.url_rule.rule == "/api/student/<int:id>/":
            redis_client.delete("GET/api/students/")

        if request.method.upper() == "POST" and request.path == "/api/student/":
            redis_client.delete("GET/api/students/")

        if request.url_rule.rule == "/api/company/<int:id>/":
            redis_client.delete("GET/api/companies/")

        if request.method.upper() == "POST" and request.path == "/api/company/":
            redis_client.delete("GET/api/companies/")

        if request.url_rule.rule == "/api/job/<int:id>/":
            redis_client.delete("GET/api/jobs/")

        if request.method.upper() == "POST" and request.path == "/api/job/":
            redis_client.delete("GET/api/jobs/")

        if request.url_rule.rule == "/api/application/<int:id>/":
            redis_client.delete("GET/api/application/")

        if request.method.upper() == "POST" and request.path == "/api/application/":
            redis_client.delete("GET/api/applications/")

        return response

    # cache dashboard data for 20 seconds
    if request.url_rule.rule in cached_urls:
        key = request.method + request.path
        data = response.get_json()
        data = json.dumps(data)
        redis_client.set(key, data, ex=20)

    if request.path in cached_endpoints:
        key = request.method + request.path
        data = response.get_json()
        data = json.dumps(data)
        redis_client.set(key, data, ex=20)

    return response
