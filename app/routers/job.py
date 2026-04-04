from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import JobCreate
from app.dependencies import role_required

router = APIRouter(prefix="/jobs", tags=["Jobs"])


# ✅ CREATE JOB (Only recruiter)
 ✅ ONLY recruiter allowed
@router.post("/")
def create_job(
    job: schemas.JobCreate,
    db: Session = Depends(get_db),
    user = Depends(role_required("recruiter"))
):
    new_job = models.Job(
        title=job.title,
        description=job.description,
        company=job.company,
        owner_id=user["user_id"]
    )

    db.add(new_job)
    db.commit()

    return {"message": "Job created"}

@router.get("/")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()
    return jobs