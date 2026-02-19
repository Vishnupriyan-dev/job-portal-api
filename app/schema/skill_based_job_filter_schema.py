from pydantic import BaseModel,Field
class RecomendedInput(BaseModel):
    user_id:int=Field(gt=0)