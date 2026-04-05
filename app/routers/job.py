from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user, role_required

router = APIRouter(prefix="/jobs", tags=["Jobs"])


# ============================
# ✅ GET ALL JOBS (Public)
# ============================
@router.get("/")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()
    return jobs


# ============================
# ✅ GET CURRENT USER (Protected)
# ============================
@router.get("/me")
def get_current_user_data(user = Depends(get_current_user)):
    return {"user": user}


# ============================
# ✅ CREATE JOB (Recruiter Only)
# ============================
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

    return {"message": "Job created successfully"}

@router.post("/apply")
def apply_job(data: schemas.ApplyJob, db: Session = Depends(get_db), user=Depends(get_current_user)):
    
    new_app = models.Application(
        user_id=user["user_id"],
        job_id=data.job_id
    )

    db.add(new_app)
    db.commit()

    return {"message": "Applied successfully"}

@router.get("/applications")
def get_applications(db: Session = Depends(get_db)):
    apps = db.query(models.Application).all()
    return apps