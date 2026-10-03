from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from Database.database import engine
from Models.user import UserProgress
from Models.job import Job
from Models.skill import Skill
from Models.application import JobApplication
from Backend.admin_auth import verify_admin

import httpx
from datetime import datetime


router = APIRouter()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def get_db():
    db = Session(bind=engine)

    try:
        yield db
    finally:
        db.close()


# =========================
# REGISTER USER
# =========================

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


@router.post("/register")
def register_user(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(UserProgress)
        .filter(UserProgress.email == data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(data.password)

    user = UserProgress(
        name=data.name,
        email=data.email,
        password=hashed_password,
        career="",
        level="Beginner"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Registration successful 🚀",
        "user_id": user.id
    }


# =========================
# LOGIN USER
# =========================

class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login_user(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(UserProgress)
        .filter(UserProgress.email == data.email)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not pwd_context.verify(data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful 🚀",
        "user_id": user.id,
        "name": user.name,
        "career": user.career,
        "level": user.level
    }


# =========================
# CAREER DISCOVERY
# =========================

class CareerRequest(BaseModel):
    interest: str
    level: str


@router.post("/career-discovery")
def career_discovery(data: CareerRequest):

    career = ""

    if data.interest == "AI":
        career = "AI Engineer"

    elif data.interest == "Data Science":
        career = "Data Scientist"

    elif data.interest == "Web Development":
        career = "Web Developer"

    elif data.interest == "Software Development":
        career = "Software Developer"

    elif data.interest == "Cyber Security":
        career = "Cyber Security Analyst"

    elif data.interest == "Cloud":
        career = "Cloud Engineer"

    else:
        career = "Career path not found"

    return {
        "interest": data.interest,
        "level": data.level,
        "recommended_career": career
    }


# =========================
# SKILL ASSESSMENT
# =========================

class AssessmentRequest(BaseModel):
    score: int
    total: int


@router.post("/skill-assessment")
def skill_assessment(data: AssessmentRequest):

    if data.total <= 0:
        raise HTTPException(
            status_code=400,
            detail="Total must be greater than zero"
        )

    percentage = (data.score / data.total) * 100

    if percentage >= 80:
        level = "Advanced"

    elif percentage >= 50:
        level = "Intermediate"

    else:
        level = "Beginner"

    return {
        "score": data.score,
        "total": data.total,
        "percentage": percentage,
        "level": level
    }


# =========================
# SKILL GAP
# =========================

class SkillGapRequest(BaseModel):
    career: str
    level: str
    known_skills: list[str]


@router.post("/skill-gap")
def skill_gap(data: SkillGapRequest):

    if data.career == "Data Scientist":

        required_skills = [
            "Python",
            "SQL",
            "Statistics",
            "Pandas",
            "NumPy",
            "Machine Learning",
            "Data Visualization"
        ]

    elif data.career == "AI Engineer":

        required_skills = [
            "Python",
            "Mathematics",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "PyTorch"
        ]

    elif data.career == "Web Developer":

        required_skills = [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Backend Development",
            "Database"
        ]

    else:

        required_skills = [
            "Programming",
            "Problem Solving",
            "Communication"
        ]

    known_lower = {
        skill.strip().lower()
        for skill in data.known_skills
    }

    missing_skills = [
        skill
        for skill in required_skills
        if skill.lower() not in known_lower
    ]

    matched_skills = [
        skill
        for skill in required_skills
        if skill.lower() in known_lower
    ]

    gap_percentage = (
        len(missing_skills) / len(required_skills)
    ) * 100

    return {
        "career": data.career,
        "current_level": data.level,
        "required_skills": required_skills,
        "known_skills": matched_skills,
        "missing_skills": missing_skills,
        "gap_percentage": gap_percentage,
        "message": "Skill gap analysis completed successfully"
    }


# =========================
# SAVE PROGRESS
# =========================

@router.post("/save-progress")
def save_progress(
    name: str,
    career: str,
    level: str,
    assessment_score: float,
    skill_gap: float,
    practice_score: float,
    interview_score: float,
    resume_score: float,
    db: Session = Depends(get_db)
):
    user = UserProgress(
        name=name,
        career=career,
        level=level,
        assessment_score=assessment_score,
        skill_gap=skill_gap,
        practice_score=practice_score,
        interview_score=interview_score,
        resume_score=resume_score
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Progress saved successfully 🚀",
        "user_id": user.id
    }


# =========================
# LATEST PROGRESS
# =========================

@router.get("/latest-progress")
def latest_progress(
    db: Session = Depends(get_db)
):
    user = (
        db.query(UserProgress)
        .order_by(UserProgress.id.desc())
        .first()
    )

    if user is None:
        return {
            "message": "No progress data found"
        }

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "career": user.career,
        "level": user.level,
        "assessment_score": user.assessment_score,
        "skill_gap": user.skill_gap,
        "practice_score": user.practice_score,
        "interview_score": user.interview_score,
        "resume_score": user.resume_score
    }


# =========================
# DATABASE JOBS
# =========================

@router.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()

    return {
        "jobs": [
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "career": job.career,
                "skills": job.skills,
                "job_type": job.job_type
            }
            for job in jobs
        ]
    }


@router.post("/jobs")
def add_job(
    title: str,
    company: str,
    location: str,
    career: str,
    skills: str,
    job_type: str,
    db: Session = Depends(get_db)
):
    job = Job(
        title=title,
        company=company,
        location=location,
        career=career,
        skills=skills,
        job_type=job_type
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "message": "Job added successfully 🚀",
        "job_id": job.id
    }


# =========================
# JOB READY
# =========================

@router.get("/job-ready")
def job_ready():
    return {
        "status": "Job Ready",
        "message": "You have completed your career preparation."
    }


# =========================
# TEST
# =========================

@router.get("/test")
def test():
    return {
        "message": "AI Career Hub Backend is working 🚀"
    }


# =========================
# SKILLS
# =========================

@router.get("/skills")
def get_skills(db: Session = Depends(get_db)):
    skill_list = db.query(Skill).all()

    result = []

    for item in skill_list:
        result.append({
            "id": item.id,
            "name": item.name,
            "category": item.category
        })

    return {
        "skills": result
    }


# =========================
# SELECTED SKILLS
# =========================

@router.post("/selected-skills")
def save_selected_skills(skills: list[str]):
    return {
        "message": "Skills selected successfully 🚀",
        "selected_skills": skills,
        "count": len(skills)
    }


# =========================
# ADMIN USER COUNT
# =========================

@router.get("/admin/user-count")
def get_user_count(
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin)
):
    total_users = (
        db.query(UserProgress)
        .filter(
            UserProgress.email.isnot(None),
            UserProgress.email != ""
        )
        .distinct(UserProgress.email)
        .count()
    )

    return {
        "total_users": total_users
    }

# =========================
# APPLY JOB
# =========================

class ApplyRequest(BaseModel):
    user_id: int
    job_id: int
    name: str
    email: str


@router.post("/apply-job")
def apply_job(
    data: ApplyRequest,
    db: Session = Depends(get_db)
):
    application = JobApplication(
        user_id=data.user_id,
        job_id=data.job_id,
        name=data.name,
        email=data.email,
        status="Applied"
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return {
        "message": "Job application submitted successfully 🚀",
        "application_id": application.id,
        "status": application.status
    }


# =========================
# REALITY CHECK
# =========================

class RealityCheckRequest(BaseModel):
    career: str
    answers: list[str]


@router.post("/reality-check")
def reality_check(data: RealityCheckRequest):

    yes_count = data.answers.count("yes")
    score = yes_count * 20

    if score >= 80:
        status = "Career Reality Match: Strong"

    elif score >= 50:
        status = "Career Reality Match: Moderate"

    else:
        status = "Career Reality Match: Needs Improvement"

    return {
        "career": data.career,
        "score": score,
        "status": status,
        "message": "Reality check completed successfully"
    }


# =========================
# LIVE JOB SEARCH - COURSE BASED
# =========================

# Known course/career names-ku relevant search terms.
# Mapping-la illaadha course name direct-ah search aagum.

COURSE_JOB_KEYWORDS = {
    "3d artist": "3D artist",
    "3d modeler": "3D modeler OR 3D modeling",
    "3d animator": "3D animator OR animation",
    "data scientist": "data scientist",
    "data analyst": "data analyst",
    "data engineer": "data engineer",
    "business analyst": "business analyst",
    "machine learning engineer": "machine learning engineer",
    "ai engineer": "AI engineer",
    "artificial intelligence": "artificial intelligence",
    "deep learning": "deep learning",
    "generative ai": "generative AI",
    "prompt engineer": "prompt engineer",
    "python developer": "Python developer",
    "java developer": "Java developer",
    "software developer": "software developer",
    "software engineer": "software engineer",
    "web developer": "web developer",
    "frontend developer": "frontend developer",
    "backend developer": "backend developer",
    "full stack developer": "full stack developer",
    "react developer": "React developer",
    "android developer": "Android developer",
    "ios developer": "iOS developer",
    "mobile app developer": "mobile app developer",
    "ui ux designer": "UI UX designer",
    "ui designer": "UI designer",
    "ux designer": "UX designer",
    "graphic designer": "graphic designer",
    "game developer": "game developer",
    "game designer": "game designer",
    "cyber security analyst": "cyber security analyst",
    "cybersecurity": "cybersecurity",
    "ethical hacker": "ethical hacker",
    "penetration tester": "penetration tester",
    "network engineer": "network engineer",
    "cloud engineer": "cloud engineer",
    "aws": "AWS cloud engineer",
    "azure": "Azure cloud engineer",
    "devops engineer": "DevOps engineer",
    "site reliability engineer": "site reliability engineer",
    "database administrator": "database administrator",
    "sql developer": "SQL developer",
    "power bi developer": "Power BI developer",
    "tableau developer": "Tableau developer",
    "business intelligence": "business intelligence analyst",
    " qa engineer": "QA engineer",
    "software tester": "software tester",
    "automation tester": "automation tester",
    "technical writer": "technical writer",
    "digital marketer": "digital marketing",
    "seo specialist": "SEO specialist",
    "content writer": "content writer",
    "video editor": "video editor",
    "video production": "video production",
    "animator": "animator",
    "photographer": "photographer",
    "product manager": "product manager",
    "project manager": "project manager",
    "scrum master": "Scrum master",
    "electrical engineer": "electrical engineer",
    "mechanical engineer": "mechanical engineer",
    "civil engineer": "civil engineer",
    "robotics engineer": "robotics engineer",
    "iot developer": "IoT developer",
    "embedded systems": "embedded systems engineer",
    "blockchain developer": "blockchain developer",
    "cloud architect": "cloud architect",
    "solutions architect": "solutions architect",
    "financial analyst": "financial analyst",
    "accountant": "accountant",
    "hr": "human resources",
    "human resources": "human resources",
    "salesforce developer": "Salesforce developer",
    "salesforce administrator": "Salesforce administrator"
}

def get_job_search_term(course_name: str) -> str:
    normalized = " ".join(course_name.lower().strip().split())

    if normalized in COURSE_JOB_KEYWORDS:
        return COURSE_JOB_KEYWORDS[normalized]

    # Match course name exactly, ignoring case and extra spaces
    for course, keyword in COURSE_JOB_KEYWORDS.items():
        if " ".join(course.lower().split()) == normalized:
            return keyword

    # Unmapped course: search using the exact course name
    return course_name.strip()

@router.get("/live-jobs")
async def live_jobs(search: str = "data scientist"):

    search = " ".join(search.strip().split())

    if not search:
        raise HTTPException(
            status_code=400,
            detail="Please provide a course or career name"
        )

    normalized = search.lower()

    title_aliases = {
        "3d artist": ["3d artist", "3d modeler", "3d modeller", "3d generalist", "3d character artist"],
        "3d modeler": ["3d modeler", "3d modeller", "3d artist", "3d generalist"],
        "3d animator": ["3d animator", "3d animation"],
        "ui/ux designer": ["ui/ux designer", "ui ux designer", "ux designer", "ui designer"],
        "cybersecurity analyst": ["cybersecurity analyst", "cyber security analyst", "information security analyst", "soc analyst"],
        "machine learning engineer": ["machine learning engineer", "ml engineer"],
        "generative ai engineer": ["generative ai engineer", "genai engineer", "llm engineer"],
        "business intelligence analyst": ["business intelligence analyst", "bi analyst"],
        "software tester": ["software tester", "qa engineer", "quality assurance engineer"],
    }

    keywords = title_aliases.get(normalized, [normalized])

    search_terms = [search]
    if normalized in ["3d artist", "3d modeler", "3d modeller"]:
        search_terms = ["3D Artist", "3D Modeler", "3D Generalist"]

    url = "https://remotive.com/api/remote-jobs"
    all_jobs = {}

    try:
        async with httpx.AsyncClient(timeout=30) as client:

            # First: search Remotive using the selected course/career
            for term in search_terms:
                response = await client.get(url, params={"search": term})
                response.raise_for_status()

                for job in response.json().get("jobs", []):
                    job_id = job.get("id")
                    if job_id:
                        all_jobs[job_id] = job

            # Fallback: get the general job feed too
            response = await client.get(url)
            response.raise_for_status()

            for job in response.json().get("jobs", []):
                job_id = job.get("id")
                if job_id:
                    all_jobs[job_id] = job

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Live job source timed out. Please try again."
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Job source returned status {exc.response.status_code}"
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to live job source"
        )

    jobs = []

    for job in all_jobs.values():
        company = job.get("company_name")
        title = job.get("title") or ""
        description = job.get("description") or ""
        category = job.get("category") or ""

        if not company or company == "[Company Name]" or not title:
            continue

        searchable_text = " ".join(
            [title, description, category]
        ).lower()

        # Match selected course/career in title, description, or category
        if not any(keyword in searchable_text for keyword in keywords):
            continue

        jobs.append({
            "id": job.get("id"),
            "title": title,
            "company": company,
            "location": job.get("candidate_required_location"),
            "job_type": job.get("job_type"),
            "category": category,
            "publication_date": job.get("publication_date"),
            "salary": job.get("salary"),
            "description": description,
            "original_url": job.get("url"),
            "source": "Remotive",
            "matched_search": search
        })

    return {
        "source": "Remotive",
        "search": search,
        "search_terms": search_terms,
        "source_jobs_checked": len(all_jobs),
        "last_checked": datetime.now().isoformat(),
        "count": len(jobs),
        "jobs": jobs
    }
# =========================
# JOB NEWS
# =========================

@router.get("/job-news")
async def job_news():

    url = "https://remotive.com/api/remote-jobs"

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail="News source is currently unavailable"
            )

        data = response.json()

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="News source timed out. Please try again."
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to news source"
        )

    news = []

    for job in data.get("jobs", [])[:20]:

        company = job.get("company_name")
        title = job.get("title")
        job_url = job.get("url")
        published = job.get("publication_date")

        if not company or company == "[Company Name]":
            continue

        if not title or not job_url:
            continue

        news.append({
            "headline": f"{company} - {title}",
            "company": company,
            "published_date": published,
            "original_url": job_url,
            "source": "Remotive"
        })

    return {
        "source": "Remotive",
        "last_checked": datetime.now().isoformat(),
        "count": len(news),
        "news": news
    }