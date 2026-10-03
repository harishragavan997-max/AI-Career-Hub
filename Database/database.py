from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql://postgres:harish12@localhost:5432/ai_career_hub"

engine = create_engine(DATABASE_URL)

Base = declarative_base()