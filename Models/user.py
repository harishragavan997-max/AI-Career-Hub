from sqlalchemy import Column, Integer, String, Float
from Database.database import Base


class UserProgress(Base):

    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    career = Column(String)
    level = Column(String)

    assessment_score = Column(Float, default=0)
    skill_gap = Column(Float, default=0)
    practice_score = Column(Float, default=0)
    interview_score = Column(Float, default=0)
    resume_score = Column(Float, default=0)