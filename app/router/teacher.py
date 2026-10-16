from fastapi import APIRouter

router = APIRouter(prefix="/teacher",
                   tags=["teacher"],
                   )

@router.get("/")
def teacher() -> dict:
    return {"message":"this is teacher"}