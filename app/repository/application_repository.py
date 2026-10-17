from sqlalchemy.orm import Session
from sqlalchemy import text


def application_exists(
    db: Session,
    user_id: int,
    job_id: int
) -> bool:
    """
    Check whether this user has already applied for this job.
    """

    query = text("""
        SELECT 1
        FROM applications
        WHERE user_id = :user_id
          AND job_id = :job_id
        LIMIT 1
    """)

    result = db.execute(
        query,
        {
            "user_id": user_id,
            "job_id": job_id
        }
    )

    return result.first() is not None


def insert_application(
    db: Session,
    user_id: int,
    job_id: int,
    posted_id: int,
    resume_path: str
) -> int:
    """
    Insert a new application with its resume path.
    """

    query = text("""
        INSERT INTO applications (
            user_id,
            job_id,
            posted_by,
            resume_path
        )
        VALUES (
            :user_id,
            :job_id,
            :posted_id,
            :resume_path
        )
    """)

    result = db.execute(
        query,
        {
            "user_id": user_id,
            "job_id": job_id,
            "posted_id": posted_id,
            "resume_path": resume_path
        }
    )

    return result.lastrowid