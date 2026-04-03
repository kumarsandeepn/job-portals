from fastapi import FastAPI
from app.routers import job

app = FastAPI()

# 👇 ये line MUST होनी चाहिए
app.include_router(job.router)

@app.get("/")
def root():
    return {"message": "Working 🚀"}