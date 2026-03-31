from app.dependencies.auth import role_required

@router.post("/apply/{job_id}")
def apply_job(job_id: int,
              db: Session = Depends(get_db),
              user = Depends(role_required("job_seeker"))):  # 🔥

    application = models.Application(
        job_id=job_id,
        user_id=user.id
    )

    db.add(application)
    db.commit()

    return {"message": "Applied successfully"}