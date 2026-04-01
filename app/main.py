from fastapi import FastAPI
from app.routers import users, job, dashboard, auth, application

app = FastAPI()

app.include_router(users.router)
app.include_router(job.router)
app.include_router(dashboard.router)
app.include_router(auth.router)
app.include_router(application.router)

@app.get("/")
def home():
    return {"message": "Job Portal Live 🚀"}