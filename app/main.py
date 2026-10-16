from fastapi import FastAPI
from  .router import student,teacher

app = FastAPI()

app.include_router(student.router)
app.include_router(teacher.router)


@app.get("/")
def root() -> dict:
    return {"message":"teacher and student is running"}