from sqlalchemy.orm import Session
from app.repository.application_repository import insert_application
from app.repository.job_repository import active_job
from app.repository.user_repository import active_user
from app.exceptions.exception import JobExpiredError,UserInactiveError,AuthorizationError


def job_apply(
    db: Session,
    user_id:int,
    job_id: int,
    user_role:str
):
    if user_role!="job_seeker":
        raise AuthorizationError("UNAUTHORIZED")
    is_job_active=active_job(db,job_id)
    if not is_job_active:
        raise JobExpiredError("JOB_EXPIRED")
    is_user_active=active_user(db,user_id)
    if not is_user_active:
        raise UserInactiveError("USER_INACTIVE")
    app_id = insert_application(
            db,
            user_id=user_id,
            job_id=job_id,
            posted_id=is_job_active.posted_by
        )

    db.commit()
    return {"application_id": app_id}


   