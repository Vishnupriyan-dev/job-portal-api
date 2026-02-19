from pydantic import BaseModel,EmailStr,field_validator,Field,model_validator
from pydantic_core.core_schema import FieldValidationInfo
from app.validators.string_validators import require_valid_non_empty


class CompanyInput(BaseModel):
    comp_name:str=Field(...,min_length=2)
    industry_type:str=Field(...,min_length=2)
    employee_count:int

    @field_validator("comp_name","industry_type")
    @classmethod
    def string_check(cls,value,info=FieldValidationInfo):
        field_name=info.field_name
        value=require_valid_non_empty(value,field_name)
        return value
    

class BranchInput(BaseModel):
    location:str=Field(...,min_length=2)
    comp_id:int
    state:str=Field(...,min_length=2)
    country:str=Field(...,min_length=2)
    address:str=Field(...,min_length=2)
    
    @field_validator("location","state","country","address")
    @classmethod
    def string_check(cls,info=FieldValidationInfo):
        field_name=info.field_name
        value=require_valid_non_empty(value)
        return value
    