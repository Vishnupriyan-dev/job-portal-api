from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.repository.job_repository import (
    get_job_id,
    get_skill_id,
    insert_job,
    insert_application,
    insert_job_skill,
    get_job_application_stats
)

from app.repository.user_repository import fetch_user_by_email

from app.exceptions.exception import (
    JobNotFound,
    UserNotFoundError,
    ApplicationNotFound,
    DomainError,
    CompanyNotFound,
    LocationNotFound,
    AuthorizationError,
    JobExpiredError,
    NoStatusFound,
    JobInsertionError
)

def get_application_count(db: Session, job_id: int,user_role:str):
    if user_role!="recruiter":
        raise AuthorizationError("UNAUTHORIZED")
    stats = get_job_application_stats(db, job_id)

    if not stats:
        raise JobExpiredError("JOB_EXPIRED")

    return {
        "job_title": stats["job_title"],
        "status": stats["status"],
        "applicant_count": stats["applicant_count"],
    }

def job_posting(
    db: Session,
    user_id:int,
    role:str,
    job_data:dict
    ):
    
    if role!="recruiter":
        raise AuthorizationError("UNAUTHORIZED")
    job_id = insert_job(
           db,
           job_title=job_data["job_title"],
           job_description=job_data["job_description"],
           requirements=job_data["requirements"],
           salary=job_data["salary"],
           comp_id=job_data["company_id"],
           job_type=job_data["job_type"],
           location_id=job_data["location_id"],
           posted_by=user_id
        )
    if not job_id:
        raise JobInsertionError("ERROR_DURING_JOB_INSERTION")
    for skill in job_data["skill_id"]:
        insert_job_skill(
            db,
            job_id=job_id,
            skill_id=skill.skill_id,
            mini_req_exp=skill.min_exp,
            max_req_exp=skill.max_exp
        )
    return {"job_id": job_id}

def add_skills_job(
    db: Session,
    job_id:int,
    skill_id: str,
    mini_exp: int,
    maxi_exp: int,
):

    job_skill_id = insert_job_skill(
            db,
            job_id=job_id,
            skill_id=skill_id,
            mini_req_exp=mini_exp,
            max_req_exp=maxi_exp,
        )

    db.commit()
    return {"job_skill_id": job_skill_id}
    

def check_status(db:Session,job_id:int):
    status=get_job_application_stats(db,job_id)
    if not status:
        raise NoStatusFound("N0_STATUS_FOUND")
    return status
