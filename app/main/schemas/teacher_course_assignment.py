# schemas/teacher_course_assignment.py
from pydantic import BaseModel, UUID4, ConfigDict
from typing import List
from datetime import datetime
from typing import Optional

from app.main.schemas.courses import CoursesSlim
from app.main.schemas.teacher import TeacherSlim
from app.main.schemas.user import AddedBy

class TeacherCourseAssignmentBase(BaseModel):
    teacher_uuid: str
    course_uuids: List[str]

class TeacherCourseAssignmentCreate(TeacherCourseAssignmentBase):
    pass

class TeacherCourseAssignmentSlim(BaseModel):
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TeacherCourseAssignmentUpdate(BaseModel):
    uuid:str
    teacher_uuid: Optional[str]=None
    course_uuids: Optional[List[str]]=None

class TeacherCourseAssignment(BaseModel):
    uuid:str
    courses:CoursesSlim
    teacher:TeacherSlim
    user : AddedBy
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TeacherCourseAssignmentResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[TeacherCourseAssignment]

    model_config = ConfigDict(from_attributes=True)