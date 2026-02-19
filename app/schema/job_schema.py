from pydantic import BaseModel, Field,EmailStr,field_validator,model_validator
from pydantic_core.core_schema import FieldValidationInfo
from typing import Literal
import re
from app.exceptions.exception import InvalidJobNameError,InvalidSalaryError
from app.validators.string_validators import pattern_salary

job_title_pattern=re.compile(r"^[A-Za-z0-9][A-Za-z0-9#+.]*([ -][A-Za-z0-9#+.]+)*$")


class SkillInput(BaseModel):
    skill_id: int = Field(gt=0)
    min_exp: int = Field(ge=0)
    max_exp: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_exp(cls, values):
        if values.max_exp < values.min_exp:
            raise ValueError("max_exp must be >= min_exp")
        return values



class JobCreateInput(BaseModel):
    job_title: str = Field(..., min_length=2, max_length=100)
    job_description: str = Field(..., min_length=10)
    requirements: str = Field(..., min_length=5)
    salary: str 
    comp_id: int=Field(gt=0)
    job_type: Literal["FULL_TIME", "PART_TIME", "INTERNSHIP","CONTRACT"]
    location_id: int = Field(gt=0)
    skill_id:list[SkillInput]
   


    @field_validator("job_title")
    @classmethod
    def title_check(cls,value,info=FieldValidationInfo):
        field_name=info.field_name
        if not job_title_pattern.fullmatch(value):
            raise InvalidJobNameError("INVALID_JOB_ERROR")
        return value
        
    @field_validator("salary")
    @classmethod
    def salary_check(cls,value,info=FieldValidationInfo):
        field_name=info.field_name
        if not pattern_salary.fullmatch(value):
            raise InvalidSalaryError("INVALID_SALARY_ERROR")
        return value


class JobApplyInput(BaseModel):
    user_id:int
    job_title: str = Field(..., min_length=2)
    company_name: str = Field(..., min_length=2)
    location: str = Field(..., min_length=2)

class JobSkillInput(BaseModel):
    job_title: str = Field(..., min_length=2)
    company_name: str = Field(..., min_length=2)
    location: str = Field(..., min_length=2)
    skill: str = Field(..., min_length=2)
    mini_exp: int = Field(..., ge=0)
    maxi_exp: int = Field(..., ge=0)

class RecentApplicationsInput(BaseModel):
    email: EmailStr
    days: int = Field(..., gt=0)

class RecommendedJobsInput(BaseModel):
    email: EmailStr


class JobStatusInput(BaseModel):
    job_id:int
