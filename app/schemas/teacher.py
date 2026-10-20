from pydantic import BaseModel,ConfigDict


class TeacherCreate(BaseModel):
    name:str
    
class TeacherResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    name:str

class TeacherUpdate(BaseModel):
    name: str