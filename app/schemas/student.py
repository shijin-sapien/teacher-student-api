from pydantic import BaseModel,EmailStr,ConfigDict


class StudentCreate(BaseModel):
    name:str
    age:int
    email:EmailStr

class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int
    name:str
    age:int
    email:EmailStr


class StudentUpdate(BaseModel):
    

    name:str|None = None
    age:int|None = None
    email:EmailStr|None = None