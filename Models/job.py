from sqlalchemy import Column, Integer, String
from Database.database import Base


class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    company = Column(String)
    location = Column(String)
    career = Column(String)
    skills = Column(String)
    job_type = Column(String)