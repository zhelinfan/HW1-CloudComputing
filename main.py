import os
from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException

from models.course import CourseRead, CourseCreate, CourseUpdate
from models.student import StudentRead, StudentCreate, StudentUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))
# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
students: Dict[UUID, StudentRead] = {}
courses: Dict[UUID, CourseRead] = {}

app = FastAPI(
    title="Student/Course API",
    description="Demo FastAPI app using Pydantic v2 models for Student and Course",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Student endpoints
# -----------------------------------------------------------------------------
@app.post("/students", response_model=StudentRead, status_code=201)
def create_student(student: StudentCreate):
    student_read = StudentRead(**student.model_dump())
    students[student_read.id] = student_read
    return student_read

@app.get("/students", response_model=List[StudentRead])
def list_students():
    return list(students.values())

@app.get("/students/{student_id}", response_model=StudentRead)
def get_student(student_id: UUID):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]

@app.put("/students/{student_id}", response_model=StudentRead)
def update_student(student_id: UUID, update: StudentUpdate):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    stored = students[student_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    students[student_id] = StudentRead(**stored)
    return students[student_id]

@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: UUID):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return None


# -----------------------------------------------------------------------------
# Course endpoints
# -----------------------------------------------------------------------------
@app.post("/courses", response_model=CourseRead, status_code=201)
def create_course(course: CourseCreate):
    course_read = CourseRead(**course.model_dump())
    courses[course_read.id] = course_read
    return course_read

@app.get("/courses", response_model=List[CourseRead])
def list_courses():
    return list(courses.values())

@app.get("/courses/{course_id}", response_model=CourseRead)
def get_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]

@app.put("/courses/{course_id}", response_model=CourseRead)
def update_course(course_id: UUID, update: CourseUpdate):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    stored = courses[course_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    courses[course_id] = CourseRead(**stored)
    return courses[course_id]

@app.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    del courses[course_id]
    return None

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Student/Course API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
