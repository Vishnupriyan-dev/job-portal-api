from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter,Depends,HTTPException
from app.dependencies.dependency import get_current_user
from app.schema.application_schema import ApplicationInput
from app.services.application_service import job_apply as  job_apply_service
from app.exceptions.exception import JobExpiredError,UserInactiveError,AuthorizationError
from app.db.connection import get_db

router=APIRouter(prefix="/applications",tags=["applications"])

@router.post("/apply/me")
def apply(payload:ApplicationInput,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        return job_apply_service(db,user_id=current_user.user_id,job_id=payload.job_id,user_role=current_user.role)
    
    except AuthorizationError as e:
        raise HTTPException(
            status_code=401,
            detail=e.msg
        )
    except UserInactiveError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )
    
    except JobExpiredError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )
    
    except IntegrityError :
        raise HTTPException(
            status_code=409,
            detail= "DATABASE_ERRROR"
        )