from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.connection import get_db

from app.schema.user_schema import (
    RegisterUserInput,
    UserUpdateInput,
    LoginInput,
    RemoveAccountInput,
    GetAppliedJobsInput,
    RecruiterInput,
    InsertSkillInput,
    JobSearchInput
)

from app.exceptions.exception import (
    AuthenticationError,
    AuthorizationError,
    UserNotFoundError,
    RoleAlreadyGranted,
    MobileAlreadyExistsError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    EmptyError,
    ApplicationNotFound,
    NoFieldError)



from app.services.user_service import register_user as register_user_service
from app.services.user_service import grant_recruiter_role as grant_recruiter_service
from app.services.user_service import user_update as user_update_service
from app.services.user_service import log_in as log_in_service
from app.services.user_service import remove_account as remove_account_service
from app.services.user_service import get_applied_jobs as get_applied_service
from app.services.user_service import my_applications_count as my_applications_count_service
from app.services.user_service import my_skills as my_skills_service
from app.services.user_service import insert_skills as insert_skills_service
from app.services.user_service import job_search as job_search_service
from app.services.user_service import list_skills as list_skills_service
from app.services.user_service import my_recents as my_recents_service
from app.dependencies.dependency import require_admin,get_current_user


router=APIRouter(prefix="/user",tags=["user"])

@router.post("/signup")
def signup(payload:RegisterUserInput,db:Session=Depends(get_db)):
    try:
        return register_user_service(db,name=payload.name,
        number=payload.number,
        email=payload.email,
        password=payload.password)
    except MobileAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="MOBILE_NUMBER_ALREADY_EXIST"
        )
    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="EMAIL_ALREADY_EXISTS"
        )

@router.post("/grant_recruiter/{user_id}")
def grant_recruiter(user_id:int,payload:RecruiterInput,db:Session=Depends(get_db),admin=Depends(require_admin)):
        try:
            return grant_recruiter_service(db,
                                           target_user_id=user_id,
                                           admin_id=admin.user_id,
                                           comp_name=payload.comp_name,
    employee_count=payload.employee_count,
    industry_type=payload.industry_type,
    location=payload.location,
    state=payload.state,
    country=payload.country,
    address=payload.address,
    )
        except InvalidCredentialsError as e:
            db.rollback()
            raise HTTPException(
                status_code=404,
                detail= str(e)
            )
        except RoleAlreadyGranted:
            db.rollback()
            raise HTTPException(
                status_code=409,
                detail="CANNOT_ASSIGN_SAME_ROLE_AGAIN"
            )
        except Exception:
            db.rollback()
            raise
    

@router.patch("/update_profile/me")#server decides the exact user using token
def update_profile(payload:UserUpdateInput,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
       return user_update_service(db,user_id=current_user.user_id,name=payload.name,
                               number=payload.number,email=payload.email,
                               password=payload.password)
    
    except NoFieldError as e:
        raise HTTPException(
            status_code=400,
            detail=e.msg
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=409,
            detail="USER_NOT_FOUND"
        )
    
    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="EMAIL_ALREADY_EXISTS"
        )


@router.post("/login",status_code=200)
def login(payload:LoginInput,db:Session=Depends(get_db)):
    try:

       return log_in_service(db,email=payload.email,password=payload.password)
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=422,
            detail=e.msg
        )

@router.delete("/delete_account/me")
def delete_account(payload:RemoveAccountInput,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return remove_account_service(db,current_user.user_id,payload.password)

@router.get("/applied_jobs/me")
def my_jobs(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return get_applied_service(db,current_user.user_id)

@router.get("/applications/me/count")
def applications(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return my_applications_count_service(db,current_user.user_id)

@router.get("/skills/me")
def skills(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return my_skills_service(db,current_user.user_id)

@router.post("/skills/me",status_code=201)
def add_skills_to_me(payload:InsertSkillInput,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return insert_skills_service(db,current_user.user_id,skill_name=payload.skill_name,min_exp=payload.min_exp,max_exp=payload.max_exp)

@router.post("/search")
def job_search(payload:JobSearchInput,db:Session=Depends(get_db)):
    return job_search_service(db,job_title=payload.job_title,comp_title=payload.comp_title,location=payload.location,industry=payload.industry)

@router.get("/skills")
def get_skills(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return list_skills_service(db)

@router.post("/skills/{days}",status_code=200)
def recently_applied_jobs(days,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        return my_recents_service(db,user_id=current_user.user_id,days=days)
    except ApplicationNotFound:
        raise HTTPException(
            status_code=404,
            detail="NO_RECENT_APPLICATIONS"
        )
