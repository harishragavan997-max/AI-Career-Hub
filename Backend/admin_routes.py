import os

from dotenv import load_dotenv
from fastapi import APIRouter, Form, Response, Depends
from passlib.context import CryptContext
from Backend.admin_auth import create_admin_token, verify_admin
from Database.database import engine
from sqlalchemy.orm import Session
from sqlalchemy import text

load_dotenv()

router = APIRouter()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD")


@router.post("/admin/login")
def admin_login(
    username: str = Form(...),
    password: str = Form(...),
    response: Response = None
):
    if username != "admin":
        return {
            "success": False,
            "message": "Invalid admin credentials"
        }

    if not ADMIN_PASSWORD_HASH:
        return {
            "success": False,
            "message": "Admin password is not configured"
        }

    if not pwd_context.verify(password, ADMIN_PASSWORD_HASH):
        return {
            "success": False,
            "message": "Invalid admin credentials"
        }

    response.set_cookie(
        key="admin_token",
        value=create_admin_token(),
        httponly=True,
        samesite="lax",
        max_age=3600
    )

    return {
        "success": True,
        "message": "Admin login successful"
    }


@router.get("/admin/application-count")
def application_count(
    _: bool = Depends(verify_admin)
):
    db = Session(bind=engine)

    try:
        total_applications = db.execute(
            text("SELECT COUNT(*) FROM job_applications")
        ).scalar()

        return {
            "total_applications": total_applications
        }

    finally:
        db.close()


@router.get("/admin/analytics")
def admin_analytics(
    _: bool = Depends(verify_admin)
):
    db = Session(bind=engine)

    try:
        applications = db.execute(
            text("SELECT COUNT(*) FROM job_applications")
        ).scalar()

        practice = db.execute(
            text(
                "SELECT COUNT(*) FROM user_progress "
                "WHERE practice_score > 0"
            )
        ).scalar()

        mock_interview = db.execute(
            text(
                "SELECT COUNT(*) FROM user_progress "
                "WHERE interview_score > 0"
            )
        ).scalar()

        skill_assessment = db.execute(
            text(
                "SELECT COUNT(*) FROM user_progress "
                "WHERE assessment_score > 0"
            )
        ).scalar()

        jobs = applications

        return {
            "applications": applications,
            "practice": practice,
            "mock_interview": mock_interview,
            "skill_assessment": skill_assessment,
            "jobs": jobs
        }

    finally:
        db.close()