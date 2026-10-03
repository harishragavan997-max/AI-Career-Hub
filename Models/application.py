from sqlalchemy import Column, Integer, String
from Database.database import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    job_id = Column(Integer)
    name = Column(String)
    email = Column(String)
    status = Column(String, default="Applied")