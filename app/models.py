from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String, unique=True)
    role = Column(String)

    applications = relationship("Application", back_populates="user")

# -----------------------
# Job Table
# -----------------------
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    company = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    # 🔥 ADD THIS
    applications = relationship("Application", back_populates="job")


# -----------------------
# Application Table
# -----------------------
class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    # 🔗 relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")