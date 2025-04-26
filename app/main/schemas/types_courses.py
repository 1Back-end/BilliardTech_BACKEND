from datetime import date, datetime
from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional
from app.main.schemas.user import AddedBy


class TypeCoursesBase(BaseModel):
    name :str

class TypeCoursesCreate(TypeCoursesBase):
    pass

class TypeCoursesUpdate(BaseModel):
    uuid :str
    name : Optional[str]=None

class TypeCoursesDelete(BaseModel):
    uuid :str

class TypeCourses(BaseModel):
    uuid :str
    name:Optional[str]=None
    created_at:datetime
    updated_at:datetime
    user:AddedBy
    model_config = ConfigDict(from_attributes=True)

class TypeCoursesResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[TypeCourses]

    model_config = ConfigDict(from_attributes=True)