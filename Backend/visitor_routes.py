from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime, timezone,time

from Database.database import engine
from Models.visitor import Visitor
from Backend.admin_auth import verify_admin

router = APIRouter()


# PUBLIC - Track visitor
@router.get("/visitor-count")
def track_visitor(
    request: Request,
    response: Response
):
    # Admin browser-ai public visitor count-la சேர்க்காதே
    if request.cookies.get("admin_token"):
        return {
            "message": "Admin visit excluded from visitor count"
        }

    visitor_id = request.cookies.get("visitor_id")

    db = Session(bind=engine)

    try:
        if not visitor_id:
            visitor_id = str(uuid4())

            response.set_cookie(
                key="visitor_id",
                value=visitor_id,
                max_age=63072000,
                httponly=True,
                samesite="lax"
            )

        visitor = (
            db.query(Visitor)
            .filter(Visitor.visitor_key == visitor_id)
            .first()
        )

        if not visitor:
            new_visitor = Visitor(
                visitor_key=visitor_id,
                first_seen=datetime.utcnow(),
                last_seen=datetime.utcnow()
            )
            db.add(new_visitor)
        else:
            visitor.last_seen = datetime.utcnow()

        db.commit()

        return {
            "message": "Visitor tracked successfully"
        }

    finally:
        db.close()



# ADMIN - Total Visitors
@router.get("/admin/visitor-count")
def admin_visitor_count(
    db: Session = Depends(
        lambda: Session(bind=engine)
    ),
    _: bool = Depends(verify_admin)
):

    total_visitors = db.query(Visitor).count()

    return {
        "total_visitors": total_visitors
    }


# ADMIN - Today Visitors
@router.get("/admin/today-visitor-count")
def admin_today_visitor_count(
    db: Session = Depends(
        lambda: Session(bind=engine)
    ),
    _: bool = Depends(verify_admin)
):

    today_start = datetime.combine(
    datetime.now(timezone.utc).date(),
    time.min
    )

    today_visitors = (
        db.query(Visitor)
        .filter(
            Visitor.last_seen >= today_start
        )
        .count()
    )

    return {
        "today_visitors": today_visitors
    }