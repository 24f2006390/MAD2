import random
from datetime import datetime, timedelta

import requests
from faker import Faker

BASE_URL = "http://127.0.0.1:5000/api"  # Change if needed

fake = Faker("en_IN")
random.seed(42)

# ------------------------------
# Configuration
# ------------------------------

NUM_COMPANIES = 10
JOBS_PER_COMPANY = (2, 5)  # min, max
NUM_STUDENTS = 50

# ------------------------------
# Data
# ------------------------------

industries = [
    "Information Technology",
    "FinTech",
    "Healthcare",
    "EdTech",
    "Cyber Security",
    "Cloud Computing",
    "Artificial Intelligence",
    "E-Commerce",
]

company_prefix = [
    "Tech",
    "Cloud",
    "Byte",
    "Nova",
    "Quantum",
    "Data",
    "Future",
    "Next",
    "Prime",
]

company_suffix = [
    "Solutions",
    "Technologies",
    "Systems",
    "Labs",
    "Soft",
    "AI",
    "Networks",
    "Innovations",
]

branches = [
    "Computer Science",
    "Information Technology",
    "Electronics",
    "Electrical",
    "Mechanical",
    "Civil",
    "AI & Data Science",
]

degrees = [
    "B.Tech",
    "B.E.",
]

job_titles = [
    "Software Engineer",
    "Backend Developer",
    "Frontend Developer",
    "Full Stack Developer",
    "Machine Learning Engineer",
    "Data Scientist",
    "DevOps Engineer",
    "Cloud Engineer",
    "Python Developer",
    "SDE Intern",
]

locations = [
    "Pune",
    "Bengaluru",
    "Hyderabad",
    "Mumbai",
    "Delhi",
    "Chennai",
    "Remote",
]

salary_ranges = [
    "4 LPA",
    "6 LPA",
    "8 LPA",
    "10 LPA",
    "12 LPA",
    "15 LPA",
    "18 LPA",
    "20 LPA",
]

experience_levels = [
    "Fresher",
    "0-1 years",
    "0-2 years",
    "1-3 years",
]

approval_statuses = ["approved", "pending"]


# ------------------------------
# Helpers
# ------------------------------

def post(endpoint, payload):
    r = requests.post(f"{BASE_URL}{endpoint}", json=payload)

    try:
        body = r.json()
    except Exception:
        body = r.text

    print(f"{endpoint:<12} {r.status_code}")

    return r.status_code, body


# ------------------------------
# Create Companies
# ------------------------------

company_ids = []

print("\nCreating companies...\n")

for i in range(NUM_COMPANIES):
    name = (
        random.choice(company_prefix)
        + random.choice(company_suffix)
    )

    payload = {
        "name": name,
        "website": f"https://{name.lower().replace(' ', '')}.com",
        "hr_email": f"hr{i}@{name.lower().replace(' ', '')}.com",
        "hr_phone": f"9{random.randint(100000000,999999999)}",
        "hq_address": fake.address().replace("\n", ", "),
        "tagline": fake.catch_phrase(),
        "industry": random.choice(industries),
        "founded_year": random.randint(1995, 2024),
        "description": fake.paragraph(nb_sentences=6),
        "no_of_offices": random.randint(1, 40),
        "staff_size": random.randint(50, 5000),
        "approval_status": random.choice(approval_statuses),
        "password": "password123",
    }

    status, body = post("/company/", payload)

    if isinstance(body, dict):
        company_ids.append(body.get("id", i + 1))
    else:
        company_ids.append(i + 1)

# ------------------------------
# Create Jobs
# ------------------------------

print("\nCreating jobs...\n")

for company_id in company_ids:

    for _ in range(random.randint(*JOBS_PER_COMPANY)):

        deadline = (
            datetime.now()
            + timedelta(days=random.randint(10, 90))
        ).isoformat()

        payload = {
            "title": random.choice(job_titles),
            "location": random.choice(locations),
            "salary": random.choice(salary_ranges),
            "experience": random.choice(experience_levels),
            "application_deadline": deadline,
            "approval_status": random.choice(approval_statuses),
            "description": fake.paragraph(nb_sentences=8),
            "company_id": company_id,
            "is_closed": 0,
        }

        post("/job/", payload)

# ------------------------------
# Create Students
# ------------------------------

print("\nCreating students...\n")

for i in range(NUM_STUDENTS):

    first = fake.first_name()
    last = fake.last_name()

    payload = {
        "first_name": first,
        "last_name": last,
        "email_id": f"{first.lower()}.{last.lower()}{i}@example.com",
        "phone_no": f"9{random.randint(100000000,999999999)}",
        "cgpa": round(random.uniform(6.0, 9.9), 2),
        "graduation_year": random.randint(2026, 2029),
        "branch": random.choice(branches),
        "degree": random.choice(degrees),
        "approval_status": random.choice(approval_statuses),
        "password": "password123",
        "photo_path": None,
    }

    post("/student/", payload)

print("\nDone.")