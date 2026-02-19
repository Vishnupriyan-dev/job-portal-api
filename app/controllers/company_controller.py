from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.dependencies.dependency import get_current_user
from app.schema.company_schema import CompanyInput
from app.services.company_service import create_company as create_company_service
from app.exceptions.exception import AuthorizationError
router= APIRouter(prefix="/company",tags=["company"])

@router.post("/create")
def create_company(payload:CompanyInput,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
       return create_company_service(
        db,current_user.role,comp_name=payload.comp_name,employee_count=payload.employee_count,
        industry_type=payload.industry_type
    )
    except AuthorizationError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
