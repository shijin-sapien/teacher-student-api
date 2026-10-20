from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate,StudentUpdate
from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError

def create_student(
                    db: Session,
                    student_data: StudentCreate
                     ) -> Student:
    new_student = Student(**student_data.model_dump())

    try:
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return new_student

def all_student(
        db:Session) -> list[Student]:
    students = db.query(Student).all()
    return students

def get_a_student_by_id(db:Session,id:int) -> Student:
    student = db.query(Student).filter(Student.id == id).first()
    if student is None:
            raise HTTPException(status_code= 404,
                                detail= "student not found")
    return student

def student_update(db:Session,id:int,
                   data:StudentUpdate) -> Student :
    student = db.query(Student).filter(Student.id == id).first()
    if student is None:
        raise HTTPException(status_code=404,
                            detail="student not found")
    update_data = data.model_dump(exclude_unset=True)

    for key,value in update_data.items():
        setattr(student,key,value)

    
    db.commit()
    db.refresh(student)

    return student

def student_delete_by_id(db:Session,id:int) -> dict:
    student = db.query(Student).filter(Student.id == id).first()

    if student is None:
        raise HTTPException(status_code= 404,
                            detail= "student not found")

    db.delete(student)
    db.commit()
    

    return {"message":"student is deleted"}