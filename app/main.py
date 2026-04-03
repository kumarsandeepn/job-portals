from fastapi import FastAPI
from app.routers import job

app = FastAPI()

app.include_router(job.router)

@app.get("/")
def root():
    return {"message": "Working 🚀"}