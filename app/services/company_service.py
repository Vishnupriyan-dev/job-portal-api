from sqlalchemy.orm import Session
from app.repository.company_repository import insert_company
from app.exceptions.exception import AuthorizationError

def create_company(
    db: Session,
    current_user_role: str,
    comp_name: str,
    employee_count: int,
    industry_type: str
):
    if current_user_role != "RECRUITER":
        raise AuthorizationError("USER_NOT_AUTHORIZED") 

    return insert_company(
        db=db,
        comp_name=comp_name,
        employee_count=employee_count,
        industry_type=industry_type
    )




        