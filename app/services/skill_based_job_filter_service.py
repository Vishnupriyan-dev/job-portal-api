from app.repository.skill_based_job__repository import get_recommended_jobs
from app.exceptions.exception import NoMatchedJobs
from sqlalchemy.orm import Session


def matched_jobs(db:Session,user_id:int):
    jobs= get_recommended_jobs(db,user_id)
    if not jobs:
        raise NoMatchedJobs()
    return jobs