from pydantic import BaseModel,Field
from pydantic_core.core_schema import FieldValidationInfo

class ApplicationInput(BaseModel):
    job_id: int =Field(gt=0)
    