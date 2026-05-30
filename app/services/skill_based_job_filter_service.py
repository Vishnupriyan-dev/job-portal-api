from app.repository.skill_based_job_repository import get_recommended_jobs
from app.exceptions.exception import NoMatchedJobs
from app.db.connection import get_db
from sqlalchemy.orm import Session
from fastapi import Depends


def matched_jobs(user_id:int,db:Session=Depends(get_db)):
    jobs= get_recommended_jobs(db,user_id)
    if not jobs:
        raise NoMatchedJobs()
    return jobs