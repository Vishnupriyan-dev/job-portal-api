from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.connection import get_db
from app.dependencies.dependency import get_current_user
from app.schema.job_schema import JobCreateInput,JobStatusInput

from app.services.job_service import job_posting as job_posting_service
from app.services.job_service import get_application_count as application_count_service
from app.services.job_service import check_status as check_status_service
from app.exceptions.exception import ( AuthorizationError,
                                      JobExpiredError,
                                      NoStatusFound,
                                      JobInsertionError,
                                      SkillInsertionError)

router=APIRouter(prefix="/jobs",tags=["jobs"])

@router.post("/post_job")
def post_job(payload:JobCreateInput,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        job_data={
             "job_title": payload.job_title,
             "job_description": payload.job_description,
             "requirements": payload.requirements,
             "salary": payload.salary,
             "company_id": payload.comp_id,
             "job_type": payload.job_type,
             "location_id": payload.location_id,
             "skill_id": payload.skill_id
        }
        return job_posting_service(db,
                                   user_id=current_user.user_id,
                                   role=current_user.role,
                                   job_data=job_data
                                   )
        db.commit()
    
    except AuthorizationError :
        db.rollback()
        raise HTTPException(
            status_code=401,
            detail="unauthorized"
        )
    
    except JobInsertionError as e:
        db.rollback()
        raise HTTPException(
            status_code=402,
            detail=e.msg
        )
    
    except SkillInsertionError as e:
        db.rollback()
        raise HTTPException(
            status_code=402,
            detail=e.msg
        )
    
    
@router.get("/applications{job_id}")
def get_applications(job_id,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        return application_count_service(db,job_id=job_id,user_role=current_user.user_role)
    except AuthorizationError as e:
        raise HTTPException(
            status_code=401,
            detail=e.msg
        )
    except JobExpiredError as e:
        raise HTTPException(
            status_code=401,
            detail=e.msg
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )


@router.get("{job_id}/status")
def applied_job_status(job_id,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        return check_status_service(db,job_id=job_id)
    except NoStatusFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.msg
        )
    
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

