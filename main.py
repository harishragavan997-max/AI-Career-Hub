from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from Backend.routes import router
from Database.database import Base, engine
from Models.user import UserProgress
from Models.job import Job
from Models.skill import Skill
from Models.application import JobApplication
from Models.visitor import Visitor
from Backend.visitor_routes import router as visitor_router
from Backend.admin_routes import router as admin_router
app = FastAPI(title="AI Career Hub")

# Create database tables
Base.metadata.create_all(bind=engine)
app.include_router(visitor_router)
app.include_router(admin_router)

# Allow frontend to connect with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect backend routes
app.include_router(router)

# Connect frontend
app.mount("/frontend", StaticFiles(directory="Frontend", html=True), name="frontend")

CAREER_JOB_SEARCH = {

    "Data Scientist":
        "data scientist",

    "Data Analyst":
        "data analyst",

    "AI Engineer":
        "artificial intelligence AI engineer",

    "Machine Learning Engineer":
        "machine learning engineer",

    "Data Engineer":
        "data engineer",

    "Python Developer":
        "python developer",

    "Web Developer":
        "web developer",

    "Cloud Engineer":
        "cloud engineer",

    "DevOps Engineer":
        "devops engineer",

    "Cyber Security Analyst":
        "cyber security cybersecurity"

}
@app.get("/")
def home():
    return {
        "message": "Welcome to AI Career Hub 🚀"
    }