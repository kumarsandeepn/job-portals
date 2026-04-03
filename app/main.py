from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import job

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# 👇 ये line MUST होनी चाहिए
app.include_router(job.router)

@app.get("/")
def root():
    return {"message": "Working 🚀"}