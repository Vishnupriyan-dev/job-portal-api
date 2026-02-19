from pydantic import BaseModel,EmailStr,field_validator,Field,model_validator
from pydantic_core.core_schema import FieldValidationInfo
from app.validators.string_validators import (
    require_non_empty,
    require_valid_non_empty,
    password_check,
    number_pattern
    )
from app.exceptions.exception import NoFieldError
    
    
from pydantic import BaseModel, EmailStr, field_validator, Field, model_validator
from pydantic_core.core_schema import FieldValidationInfo
from app.validators.string_validators import (
    require_non_empty,
    require_valid_non_empty,
    password_check,
    number_pattern
)


class NameValidationMixin:
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str, info: FieldValidationInfo):
        if value is None:
            return value

        field_name = info.field_name
        value = require_valid_non_empty(value, field_name)

        bad_values = {"none", "null", "undefined", "nil", "nan"}
        if value.lower() in bad_values:
            raise ValueError(f"{field_name} cannot be a placeholder value")

        return value


class NumberValidationMixin:
    @field_validator("number")
    @classmethod
    def validate_number(cls, value: str, info: FieldValidationInfo):
        if value is None:
            return value

        field_name = info.field_name
        value = require_non_empty(value, field_name)
        value = number_pattern(value, field_name)

        return value


class PasswordValidationMixin:
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str, info: FieldValidationInfo):
        if value is None:
            return value

        field_name = info.field_name
        value = require_non_empty(value, field_name)
        value = password_check(value, field_name)

        return value


class RegisterUserInput(
    BaseModel,
    NameValidationMixin,
    NumberValidationMixin,
    PasswordValidationMixin
):
    name: str
    number: str
    email: EmailStr
    password: str


class LoginInput(BaseModel):
    email: EmailStr
    password: str



class UserUpdateInput(
    BaseModel,
    NameValidationMixin,
    NumberValidationMixin,
    PasswordValidationMixin
):
    name: str | None = None
    number: str | None = None
    email: EmailStr | None = None
    password: str | None = None

    @model_validator(mode="after")
    def at_least_one_field(cls, model):
        if not any(
            getattr(model, field) is not None
            for field in ["name", "number", "email", "password"]
        ):
            raise ValueError("At least one value must be provided")

        return model



class RemoveAccountInput(BaseModel):
    user_id: int = Field(gt=0)


class GetAppliedJobsInput(BaseModel):
    user_id: int = Field(gt=0)


class MyApplicationsCountInput(BaseModel):
    user_id: int = Field(gt=0)


class MySkillsInput(BaseModel):
    user_id: int = Field(gt=0)


class InsertSkillInput(BaseModel):
    user_id: int = Field(gt=0)
    skill_id: int = Field(gt=0)
    user_mini_exp: int = Field(gt=0)
    user_maxi_exp: int = Field(gt=0)


class JobSearchInput(BaseModel):
    job_title: str | None = None
    comp_title: str | None = None
    location: str | None = None
    industry: str | None = None

    @field_validator("job_title", "comp_title", "location", "industry")
    @classmethod
    def validate_optional_strings(cls, value: str, info: FieldValidationInfo):
        if value is None:
            return value

        field_name = info.field_name
        return require_valid_non_empty(value, field_name)

    @model_validator(mode="after")
    def at_least_one_filter(cls, model):
        if not any(
            getattr(model, field) is not None
            for field in ["job_title", "comp_title", "location", "industry"]
        ):
            raise ValueError("At least one filter must be provided")

        return model
    
class RecruiterInput(BaseModel):
    comp_name:str
    employee_count:int =Field(gt=0)
    industry_type:str
    location:str
    state:str
    country:str
    address:str

    @field_validator("comp_name","industry_type","location","state","country")
    @classmethod
    def validate_name(cls, value: str, info: FieldValidationInfo):
        if value is None:
            return value

        field_name = info.field_name
        value = require_valid_non_empty(value, field_name)

        bad_values = {"none", "null", "undefined", "nil", "nan"}
        if value.lower() in bad_values:
            raise ValueError(f"{field_name} cannot be a placeholder value")
        return value
    


