from sqlalchemy.orm import Session
from sqlalchemy import text


def insert_company(db: Session, comp_name: str, employee_count: int, industry_type: str,target_user_id:int):
    query = text("""
        INSERT INTO companies (comp_name, employee_count, industry_type,created_by)
        VALUES (:company_name, :employee_count, :industry,:created_by)
    """)
    
    result = db.execute(
        query,
        {
            "company_name": comp_name,
            "employee_count": employee_count,
            "industry": industry_type,
            "created_by":target_user_id
        }
    )
    return result.lastrowid



def insert_location(db: Session,location:str,comp_id:int,state:str,country:str,address:str):
    query=text(
        """ INSERT INTO LOCATIONS (
        location,comp_id,state,country,address)
         values (:location,:comp_id,:state,:country,:address)"""
    )

    result = db.execute(
        query,
        {
            "location":location,
            "comp_id":comp_id,
            "state":state,
            "country":country,
            "address":address
        }
    )
    return result.lastrowid

def fetch_company_by_name(db: Session, comp_name: str):
    query = text("""
        SELECT comp_id
        FROM companies
        WHERE comp_name = :name
    """)
    result = db.execute(query, {"name": comp_name}).fetchone()
    return result[0] if result else None


