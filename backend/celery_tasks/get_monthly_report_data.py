from datetime import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy import func

from app import app
from db import db
from models import Application, Company, Job, Student

today = datetime.now()

start = (today.replace(day=1) - relativedelta(months=1)).replace(
    day=1, hour=0, minute=0, second=0, microsecond=0
)

# end = today.replace(
#     day=1,
#     hour=0,
#     minute=0,
#     second=0,
#     microsecond=0
# )

end = today + relativedelta(days=2)


with app.app_context():
    overview = {
        "new_students": Student.query.filter(
            Student.created_at >= start, Student.created_at < end
        ).count(),
        "new_companies": Company.query.filter(
            Company.created_at >= start, Company.created_at < end
        ).count(),
        "new_jobs": Job.query.filter(
            Job.created_at >= start, Job.created_at < end
        ).count(),
        "applications": Application.query.filter(
            Application.created_at >= start, Application.created_at < end
        ).count(),
        "selected": Application.query.filter(
            Application.created_at >= start,
            Application.created_at < end,
            Application.status == "selected",
        ).count(),
        "shortlisted": Application.query.filter(
            Application.created_at >= start,
            Application.created_at < end,
            Application.status == "shortlisted",
        ).count(),
        "rejected": Application.query.filter(
            Application.created_at >= start,
            Application.created_at < end,
            Application.status == "rejected",
        ).count(),
        "pending": Application.query.filter(
            Application.created_at >= start,
            Application.created_at < end,
            Application.status == "pending",
        ).count(),
    }

    pending_counts = {
        "students": Student.query.filter(Student.approval_status == "pending").count(),
        "companies": Company.query.filter(Company.approval_status == "pending").count(),
        "jobs": Job.query.filter(Job.approval_status == "pending").count(),
    }

    pending_students = (
        Student.query.filter(Student.approval_status == "pending")
        .order_by(Student.created_at.desc())
        .limit(5)
        .all()
    )

    pending_companies = (
        Company.query.filter(Company.approval_status == "pending")
        .order_by(Company.created_at.desc())
        .limit(5)
        .all()
    )

    pending_companies = (
        Company.query.filter(Company.approval_status == "pending")
        .order_by(Company.created_at.desc())
        .limit(5)
        .all()
    )

    pending_jobs = (
        Job.query.join(Company)
        .filter(Job.approval_status == "pending")
        .order_by(Job.created_at.desc())
        .limit(5)
        .all()
    )

    top_companies = (
        db.session.query(Company.name, func.count(Application.id).label("applications"))
        .join(Job, Company.jobs)
        .join(Application, Job.applications)
        .filter(Application.created_at >= start, Application.created_at < end)
        .group_by(Company.id, Company.name)
        .order_by(func.count(Application.id).desc())
        .limit(5)
        .all()
    )

    top_jobs = (
        db.session.query(
            Job.title,
            Company.name.label("company"),
            func.count(Application.id).label("applications"),
        )
        .join(Company)
        .join(Application)
        .filter(Application.created_at >= start, Application.created_at < end)
        .group_by(Job.id, Job.title, Company.name)
        .order_by(func.count(Application.id).desc())
        .limit(10)
        .all()
    )

    application_stats = dict(
        db.session.query(Application.status, func.count(Application.id))
        .filter(Application.created_at >= start, Application.created_at < end)
        .group_by(Application.status)
        .all()
    )

    pending = application_stats.get("pending", 0)
    shortlisted = application_stats.get("shortlisted", 0)
    selected = application_stats.get("selected", 0)
    rejected = application_stats.get("rejected", 0)

    total = pending + shortlisted + selected + rejected

    selection_rate = round(selected * 100 / total, 2) if total else 0

    shortlisting_rate = round(shortlisted * 100 / total, 2) if total else 0

    application_stats = {
        "pending": application_stats.get("pending", 0),
        "shortlisted": application_stats.get("shortlisted", 0),
        "selected": application_stats.get("selected", 0),
        "rejected": application_stats.get("rejected", 0),
        "total": total,
        "selection_rate": selection_rate,
        "shortlisting_rate": shortlisting_rate,
    }


if __name__ == "__main__":
    print(start)
    print(end)
    print(overview)
