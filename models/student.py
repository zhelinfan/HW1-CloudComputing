from datetime import datetime
from typing import Optional, Annotated, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, EmailStr, StringConstraints

from models.course import CourseBase

# Columbia UNI: 2–3 lowercase letters + 1–4 digits (e.g., abc1234)
Uni = Annotated[str, StringConstraints(pattern=r"^[a-z]{2,3}\d{1,4}$")]

class StudentBase(BaseModel):
    uni: Uni = Field(
        ...,
        description="Columbia University UNI (2–3 lowercase letters + 1–4 digits).",
        json_schema_extra={"example": "abc1234"},
    )
    first_name: str = Field(
        ...,
        description="Given name.",
        json_schema_extra={"example": "Ada"},
    )
    last_name: str = Field(
        ...,
        description="Family name.",
        json_schema_extra={"example": "Lovelace"},
    )
    email: EmailStr = Field(
        ...,
        description="Primary email address.",
        json_schema_extra={"example": "ada@example.com"},
    )
    student_status: str = Field(
        ...,
        description="Status of the student.",
        json_schema_extra={"example": "graduate"}
    )
    courses: List[CourseBase] = Field(
        default_factory=list,
        description="Courses this student is enrolled in.",
        json_schema_extra={
            "example": [
                {
                    "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                    "course_code": "COMS4153",
                    "title": "Cloud Computing",
                    "description": "cloud computing",
                    "credits": 3,
                    "instructor": "Prof. Ferguson"
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "uni": "zf1234",
                "first_name": "Jocelyn",
                "last_name": "Fan",
                "email": "zf1234@columbia.edu",
                "student_status": "graduate",
                "courses": [
                    {
                        "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                        "course_code": "COMS4153",
                        "title": "Cloud Computing",
                        "description": "Introduction to cloud computing concepts and technologies.",
                        "credits": 3,
                        "instructor": "Prof. Ferguson"
                    }
                ]
            }
        }
    }

class StudentCreate(StudentBase):
    """Creation payload for a Person."""
    model_config = {
        "json_schema_extra": {
            "example": {
                "uni": "xy1234",
                "first_name": "Ann",
                "last_name": "Xie",
                "email": "xa1234@columbia.edu",
                "student_status": "senior",
                "courses": [
                    {
                        "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                        "course_code": "COMS4156",
                        "title": "Advanced Software Engineering",
                        "description": "Software testing, Restful API",
                        "credits": 3,
                        "instructor": "Prof. Ferguson"
                    }
                ]
            }
        }
    }

class StudentUpdate(BaseModel):
    """Partial update for student fields."""
    uni: Optional[Uni] = Field(
        None, description="Columbia UNI.", json_schema_extra={"example": "ab1234"}
    )
    first_name: Optional[str] = Field(None, json_schema_extra={"example": "Augusta"})
    last_name: Optional[str] = Field(None, json_schema_extra={"example": "King"})
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "ada@newmail.com"})
    student_status: Optional[str] = Field(None, json_schema_extra={"example": "freshman"})
    courses: Optional[List[CourseBase]] = Field(
        None,
        description="Replace the entire set of course with this list.",
        json_schema_extra={
            "example": [
                {
                    "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                    "course_code": "COMS4170",
                    "title": "User Interface Design",
                    "description": "Design friendly used interfaces for people",
                    "credits": 3,
                    "instructor": "Prof. Ferguson"
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"first_name": "Augusta", "last_name": "King"},
                {"email": "augusta.king@columbia.edu"},
                {"student_status": "freshman"},
                {
                    "courses": [
                        {
                            "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                            "course_code": "COMS4170",
                            "title": "User Interface Design",
                            "description": "Design friendly user interfaces for people",
                            "credits": 3,
                            "instructor": "Prof. Ferguson"
                        }
                    ]
                }
            ]
        }
    }
class StudentRead(StudentBase):
    """Representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Person ID.",
        json_schema_extra={"example": "11111111-1111-4111-8111-111111111111"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "11111111-1111-4111-8111-111111111111",
                    "uni": "abc1234",
                    "first_name": "Ada",
                    "last_name": "Lovelace",
                    "email": "ada@example.com",
                    "student_status": "sophomore",
                    "courses": [
                        {
                            "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                            "course_code": "COMS4170",
                            "title": "User Interface Design",
                            "description": "Design friendly user interfaces for people",
                            "credits": 3,
                            "instructor": "Prof. Ferguson"
                        }
                    ],
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z"
                }
            ]
        }
    }