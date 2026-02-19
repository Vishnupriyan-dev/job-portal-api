from sqlalchemy.orm import Session
from sqlalchemy import text

def insert_application(db: Session, user_id: int, job_id: int,posted_id:int) -> int:
    query = text("""
        INSERT INTO applications (user_id, job_id,posted_by)
        VALUES (:user_id, :job_id,:posted_id)
    """)
    result = db.execute(query, locals())
    return result.lastrowid