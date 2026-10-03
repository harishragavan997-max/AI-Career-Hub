import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy.orm import Session
from Database.database import engine
from Models.skill import Skill
from Database.database import Base

Base.metadata.create_all(bind=engine)


skills = [
    ("Python", "Programming"),
    ("Java", "Programming"),
    ("C", "Programming"),
    ("C++", "Programming"),
    ("JavaScript", "Web Development"),
    ("TypeScript", "Web Development"),
    ("HTML", "Web Development"),
    ("CSS", "Web Development"),
    ("React", "Web Development"),
    ("Angular", "Web Development"),

    ("Node.js", "Backend"),
    ("SQL", "Database"),
    ("MongoDB", "Database"),
    ("PostgreSQL", "Database"),
    ("Git", "Tools"),
    ("GitHub", "Tools"),
    ("Linux", "Operating System"),
    ("AWS", "Cloud"),
    ("Azure", "Cloud"),
    ("Docker", "DevOps"),

    ("Kubernetes", "DevOps"),
    ("Networking", "Cyber Security"),
    ("Cyber Security", "Cyber Security"),
    ("Ethical Hacking", "Cyber Security"),
    ("Data Analysis", "Data Science"),
    ("Data Visualization", "Data Science"),
    ("Excel", "Data Science"),
    ("Power BI", "Data Science"),
    ("Tableau", "Data Science"),
    ("Statistics", "Data Science"),

    ("Machine Learning", "AI/ML"),
    ("Deep Learning", "AI/ML"),
    ("TensorFlow", "AI/ML"),
    ("PyTorch", "AI/ML"),
    ("Natural Language Processing", "AI/ML"),
    ("Computer Vision", "AI/ML"),
    ("Generative AI", "AI/ML"),
    ("Large Language Models", "AI/ML"),
    ("OpenAI API", "AI/ML"),
    ("LangChain", "AI/ML"),

    ("Data Science", "Data Science"),
    ("Data Engineering", "Data Engineering"),
    ("Apache Spark", "Big Data"),
    ("Hadoop", "Big Data"),
    ("R Programming", "Programming"),
    ("MATLAB", "Programming"),
    ("DevOps", "DevOps"),
    ("CI/CD", "DevOps"),
    ("System Design", "Software Engineering"),
    ("Data Structures & Algorithms", "Software Engineering"),
]


db = Session(bind=engine)

for name, category in skills:

    existing_skill = db.query(Skill).filter(Skill.name == name).first()

    if not existing_skill:
        db.add(
            Skill(
                name=name,
                category=category
            )
        )

db.commit()
db.close()

print("50 Skills added successfully 🚀")