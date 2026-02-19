from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.dependencies.dependency import get_current_user
from app.services.skill_based_job_filter_service import matched_jobs as matched_jobs_service
from app.exceptions.exception import NoMatchedJobs

router=APIRouter(prefix="/recomended",tags=["recomended"])

@router.get("/matching_jobs/me")
def matching_jobs(db:Session=get_db,current_user=Depends(get_current_user)):
    try:
        return matched_jobs_service(db,current_user.user_id)
    except NoMatchedJobs:
        raise HTTPException(
            status_code=404,
            detail="NO_MATCHED_JOBS"
        )

