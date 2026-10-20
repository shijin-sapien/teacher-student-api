from pydantic import (BaseModel,EmailStr,ConfigDict,
                      Field)


class StudentCreate(BaseModel):
    name:str
    age:int = Field(ge= 0 , le= 120)
    email:EmailStr

class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int
    name:str
    age:int
    email:EmailStr


class StudentUpdate(BaseModel):
    

    name:str|None = None
    age:int|None = Field(ge=0, le=120)
    email:EmailStr|None = None