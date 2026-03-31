from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import User, Job, Application

router = APIRouter()

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_jobs = db.query(Job).count()
    total_applications = db.query(Application).count()

    jobs_per_company = db.query(
        Job.company,
        func.count(Job.id).label("total_jobs")
    ).group_by(Job.company).all()

    return {
        "total_users": total_users,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "jobs_per_company": [
            {"company": j[0], "total_jobs": j[1]} for j in jobs_per_company
        ]
    }