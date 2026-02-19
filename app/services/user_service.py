from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.security.auth_security import hash_password
from app.security.auth_security import verify_password,create_access_token
from app.repository.user_repository import create_user
from app.repository.user_repository import fetch_user_by_email
from app.repository.user_repository import fetch_user_by_id
from app.repository.user_repository import delete_user
from app.repository.user_repository import applied_jobs
from app.repository.user_repository import get_application_count
from app.repository.user_repository import fetch_user_skill
from app.repository.user_repository import add_skills,fetch_all_skills
from app.repository.user_repository import search_jobs
from app.repository.user_repository import update_user
from app.repository.user_repository import update_user_role
from app.repository.user_repository import fetch_user_with_same_email,get_recent_applications
from app.repository.company_repository import insert_company,insert_location,fetch_company_by_name
from app.schema.user_schema import RegisterUserInput
from app.schema.user_schema import RemoveAccountInput
from app.schema.user_schema import GetAppliedJobsInput
from app.schema.user_schema import MyApplicationsCountInput
from app.schema.user_schema import MySkillsInput
from app.schema.user_schema import InsertSkillInput
from app.schema.user_schema import JobSearchInput
from app.schema.user_schema import UserUpdateInput,LoginInput

import re
from app.exceptions.exception import(
    InvalidEmailFormat,
    InvalidPasswordFormat,
    UserNotFoundError,
    RoleAlreadyGranted,
    PasswordMismatchError,
    InvalidCredentialsError,
    JobNotFound,
    ApplicationNotFound,
    NoSkillsFound,
    EmailAlreadyExist,
    DomainError,
    SkillAlreadyExistsError,
    EmailAlreadyExistsError,
    MobileAlreadyExistsError,
    AuthorizationError,
    NoFieldError
)



def register_user(
    db: Session,
    name: str,
    number: str,
    email: str,
    password: str,
):
    role = "JOB_SEEKER"
    hashed_password = hash_password(password)

    try:
        user_id = create_user(
            db,
            name=name,
            number=number,
            email=email,
            role=role,
            password=hashed_password
        )
        return create_access_token(user_id, role)
    except IntegrityError as e:
        error_msg = str(e.orig)

        if "users.mob_no" in error_msg:
            raise MobileAlreadyExistsError()
        elif "users.email" in error_msg:
            raise EmailAlreadyExistsError()
        else:
            raise


def grant_recruiter_role(
    db: Session,
    target_user_id: int,
    comp_name: str,
    employee_count: int,
    industry_type: str,
    location: str,
    state: str,
    country: str,
    address: str,
    admin_id: int
):
    role = "recruiter"

    user = fetch_user_by_id(db, target_user_id)
    if not user:
        raise InvalidCredentialsError("INVALID_USER_CREDENTIALS")

    if user.role == "recruiter":
        raise RoleAlreadyGranted("REQUESTED_ROLE_ALREADY_GRANTED")

    try:
        comp_id = insert_company(
            db,
            comp_name,
            employee_count,
            industry_type,
            target_user_id
        )
    except IntegrityError:
        db.rollback()  
        comp_id = fetch_company_by_name(db, comp_name)

    if not comp_id:
        raise InvalidCredentialsError("COMPANY_RESOLUTION_FAILED")

    loc_insert = insert_location(
        db,
        location,
        comp_id,
        state,
        country,
        address
    )

    if not loc_insert:
        raise InvalidCredentialsError("LOCATION_CREATION_FAILED")

    update_user_role(
        db,
        target_user_id,
        role,
        comp_id,
        admin_id
    )

    db.commit()

    return {"message": "Recruiter role granted"}

def log_in(db: Session, email: str, password: str):
    user_data = fetch_user_by_email(db, email)
    if not user_data:
        raise InvalidCredentialsError()
    if user_data["password"] is None:
        raise InvalidCredentialsError()
    if not verify_password(password, user_data["password"]):
        raise InvalidCredentialsError("INVALID_EMAIL_OR_PASSWORD")
    return create_access_token(user_data["user_id"], user_data["role"])


def remove_account(db: Session, user_id: int):
    affected = delete_user(db, user_id)

    if affected == 0:
        raise UserNotFoundError("User already deleted or not found")

    return {"message": "User deleted successfully"}

def get_applied_jobs(db: Session, user_id: int):
    jobs_applied = applied_jobs(db, user_id)

    return [
        {
            "job_title": job["job_title"],
            "job_status": job["app_status"],
            "date": job["app_date"],
            "company": job["comp_name"],
        }
        for job in jobs_applied
    ] if jobs_applied else []

def my_applications_count(db: Session, user_id: int):
    return get_application_count(db, user_id)

def my_skills(db: Session, user_id: int):
    skills = fetch_user_skill(db, user_id)

    if not skills:
        raise NoSkillsFound()

    return [
        {
            "name": s["user_name"],
            "skills": s["skills"],
            "minimum_experience": s["user_mini_exp"],
            "maximum_experience": s["user_maxi_exp"],
        }
        for s in skills
    ]
def insert_skills(
    db: Session,
    user_id: int,
    skill_id: int,
    min_exp: int,
    max_exp: int,
):
    try:
        return add_skills(db, user_id, skill_id, min_exp, max_exp)
    except Exception:
        raise SkillAlreadyExistsError()
    
def job_search(
    db: Session,
    job_title: str | None = None,
    comp_title: str | None = None,
    location: str | None = None,
    industry: str | None = None,
):
    params = {
        k: v.strip()
        for k, v in {
            "job_title": job_title,
            "comp_title": comp_title,
            "location": location,
            "industry": industry,
        }.items()
        if isinstance(v, str) and v.strip()
    }

    if not params:
        raise DomainError("At least one search parameter required")

    return search_jobs(db, **params)

def user_update(
    db: Session,
    user_id: int,
    name: str | None = None,
    number: str | None = None,
    email: str | None = None,
    password: str | None = None,
):
    params = {}
    user_data=fetch_user_by_id(db,user_id)
    if not user_data:
        raise UserNotFoundError()

    if name is not None:
        params["name"] = name
    if number is not None:
        params["number"] = number
    if email is not None:
        email_data=fetch_user_with_same_email(db,email,user_id)
        if email_data:
            raise EmailAlreadyExistsError()
        params["email"] = email
    if password is not None:
        params["password"] = hash_password(password)

    if not params:
        raise NoFieldError("At least one field must be provided")

    return update_user(db, user_id, **params)



def my_recents(db: Session, user_id: str, days: int):
    recents = get_recent_applications(
        db,
        user_id,
        days=days
    )

    if not recents:
        raise ApplicationNotFound()
    return recents

def list_skills(db:Session):
    return fetch_all_skills(db)
