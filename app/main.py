from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import job
from app.routers import auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# ✅ routers include
app.include_router(job.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "working 🚀"}