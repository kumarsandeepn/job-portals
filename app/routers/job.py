from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import JobCreate
from app.dependencies import get_current_user
router = APIRouter(prefix="/jobs", tags=["Jobs"])


# ✅ CREATE JOB (Only recruiter)
@router.post("/")
def create_job(job: JobCreate,
               db: Session = Depends(get_db),
               user=Depends(role_required("recruiter"))):

    new_job = models.Job(
        title=job.title,
        description=job.description,
        company=job.company,
        owner_id=user["user_id"]
    )

    db.add(new_job)
    db.commit()

    return {"message": "Job created"}


# ✅ GET JOBS
@router.get("/")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()
    return jobs