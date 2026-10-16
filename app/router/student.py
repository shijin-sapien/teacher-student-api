from fastapi import APIRouter


router = APIRouter(prefix="/students",
                   tags=["students"],
                   )

@router.get("/")
def list_student() -> dict:
    return {"message": "Student list"}