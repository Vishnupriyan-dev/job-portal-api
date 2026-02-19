from sqlalchemy.orm import Session
from sqlalchemy import text


def active_job(db:Session,job_id):
    query=text(
        """SELECT 
                status,
                posted_by
           FROM jobs
           where job_id= :job_id"""
    )

    return db.execute(
        query,
        {"job_id":job_id}
    ).mappings().first()


def get_company_id(db: Session, company_name: str, location: str):
    query = text("""
        SELECT c.comp_id, 
        FROM companies c
        WHERE c.comp_name = :company_name
    """)
    return db.execute(
        query,
        {"company_name": company_name, "location": location}
    ).mappings().first()


def get_location_id(db: Session, location: str):
    query = text("""
        SELECT location_id
        FROM  locations 
        WHERE location_name = :location
    """)
    return db.execute(
        query,
        { "location": location}
    ).mappings().first()


def get_job_id(db: Session, job_name: str, company_name: str, location: str) -> int | None:
    query = text("""
        SELECT j.job_id
        FROM jobs j
        INNER JOIN companies c ON j.comp_id = c.comp_id
        INNER JOIN locations l ON j.location_id = l.location_id
        WHERE j.job_title = :job_name
          AND c.comp_name = :company_name
          AND l.location_name = :location
    """)
    return db.execute(
        query,
        {
            "job_name": job_name,
            "company_name": company_name,
            "location": location
        }
    ).scalar()


def get_skill_id(db: Session, skill: str) -> int | None:
    query = text("""
        SELECT skill_id
        FROM skills
        WHERE skill_name = :skill
    """)
    return db.execute(query, {"skill": skill}).scalar()


def get_job_application_stats(db: Session, job_id: int):
    query = text("""
        SELECT
            j.status,
            j.job_title
        FROM jobs j
        LEFT JOIN applications a ON j.job_id = a.job_id
        WHERE j.job_id = :job_id
        GROUP BY j.job_id, j.job_title, j.status
    """)
    return db.execute(query, {"job_id": job_id}).mappings().first()


def insert_job(
    db: Session,
    job_title: str,
    job_description: str,
    requirements: str,
    salary: str,
    comp_id: int,
    job_type: str,
    location_id: int,
    posted_by:int
) -> int:
    query = text("""
        INSERT INTO jobs (
            job_title, job_description, requirements,
            salary, comp_id, job_type, location_id,posted_by
        )
        VALUES (
            :job_title, :job_description, :requirements,
            :salary, :comp_id, :job_type, :location_id,:posted_by
        )
    """)
    result = db.execute(query, locals())
    return result.lastrowid


def insert_application(db: Session, user_id: int, job_id: int, app_status: str) -> int:
    query = text("""
        INSERT INTO applications (user_id, job_id)
        VALUES (:user_id, :job_id)
    """)
    result = db.execute(query, locals())
    return result.lastrowid


def insert_job_skill(
    db: Session,
    job_id: int,
    skill_id: int,
    mini_req_exp: int,
    max_req_exp: int
) -> int:
    query = text("""
        INSERT INTO job_skills (
            job_id, skill_id, min_req_exp, max_req_exp
        )
        VALUES (
            :job_id, :skill_id, :mini_req_exp, :max_req_exp
        )
    """)
    result = db.execute(query, locals())
    return result.lastrowid


