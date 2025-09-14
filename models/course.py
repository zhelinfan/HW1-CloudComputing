from datetime import datetime
from typing import Optional, Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, StringConstraints

CourseCode = Annotated[str, StringConstraints(pattern=r"^[A-Z]{4}\d{4}$")]

class CourseBase(BaseModel):
    course_code: CourseCode = Field(
        ...,
        description="Unique course code (department + number).",
        json_schema_extra={"example": "COMS4153"},
    )
    title: str = Field(
        ...,
        description="Full course title.",
        json_schema_extra={"example": "Cloud Computing"},
    )
    description: Optional[str] = Field(
        None,
        description="Course description.",
        json_schema_extra={"example": "Introduction to cloud computing concepts and technologies."},
    )
    credits: int = Field(
        ...,
        description="Number of credits for this course.",
        json_schema_extra={"example": 3},
    )
    instructor: Optional[str] = Field(
        None,
        description="Instructor's full name.",
        json_schema_extra={"example": "Prof. Ferguson"},
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "course_code": "COMS4153",
                "title": "Cloud Computing",
                "description": "Introduction to cloud computing concepts and technologies.",
                "credits": 3,
                "instructor": "Prof. Ferguson"
            }
        }
    }

class CourseCreate(CourseBase):
    """Payload for creating a new course."""

    model_config = {
        "json_schema_extra": {
            "example": {
                "course_code": "COMS4156",
                "title": "Advanced Software Engineering",
                "description": "Software testing, RESTful API, and microservices.",
                "credits": 3,
                "instructor": "Prof. Ferguson",
            }
        }
    }

class CourseUpdate(BaseModel):
    """Partial update for course fields."""
    course_code: Optional[CourseCode] = Field(None, json_schema_extra={"example": "COMS4170"})
    title: Optional[str] = Field(None, json_schema_extra={"example": "User Interface Design"})
    description: Optional[str] = Field(None, json_schema_extra={
        "example": "Create user interfaces for people"})
    credits: Optional[int] = Field(None, json_schema_extra={"example": 4})
    instructor: Optional[str] = Field(None, json_schema_extra={"example": "Prof. Smith"})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "course_code": "COMS4170",
                    "title": "Advanced Cloud Computing",
                    "description": "Deep dive into distributed systems and cloud architectures.",
                    "credits": 4,
                    "instructor": "Prof. Smith",
                }
            ]
        }
    }

class CourseRead(CourseBase):
    """Representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Person ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
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
                    "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                    "course_code": "COMS4153",
                    "title": "Cloud Computing",
                    "description": "Introduction to cloud computing concepts and technologies.",
                    "credits": 3,
                    "instructor": "Prof. Ferguson",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
