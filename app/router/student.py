from fastapi import APIRouter
from app.schemas.student import (StudentResponse,
                                 StudentCreate,StudentUpdate)
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_db

from app.repositories.student import (create_student,student_delete_by_id,
                                      student_update,
                                      all_student,get_a_student_by_id)



router = APIRouter(prefix="/students",
                   tags=["students"],
                   )

@router.get("/",response_model=list[StudentResponse])
def list_student(db:Session = Depends(get_db)) -> list[StudentResponse]:

    return all_student(db)

@router.post("/",response_model = StudentResponse)
def create(data:StudentCreate,db:Session = Depends(get_db)) -> StudentResponse:
    return create_student(db,data)


@router.get("/{id}",response_model=StudentResponse)
def student_by_id(id:int,db:Session = Depends(get_db)) -> StudentResponse:
    return get_a_student_by_id(db,id)


@router.put("/{id}",response_model=StudentResponse)
def update(id:int,data:StudentUpdate,db:Session = Depends(get_db)) -> StudentResponse:
    return student_update(db,id,data)

@router.delete("/{id}")
def delete(id:int,db:Session = Depends(get_db)) -> dict:
    return student_delete_by_id(db,id)