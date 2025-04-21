from datetime import date, datetime
from pydantic import BaseModel,EmailStr,ConfigDict
from typing import List, Optional
from app.main.models.courses import CourseType
from app.main.schemas.academic_year import AcademicYearSlim
from app.main.schemas.group import GroupSlim
from app.main.schemas.semester import SemesterSlim1
from app.main.schemas.speciality import SpecialitySlim
from app.main.schemas.user import AddedBy, AddedBySlim


class CourseBase(BaseModel):
    title:str
    code:str
    credits:int
    type:CourseType
    speciality_uuid:str
    group_uuid:str
    academic_year_uuid:str
    semester_uuid:str

class CoursesSlim1(BaseModel):
    uuid:str
    title:str
    code:str
    model_config = ConfigDict(from_attributes=True)  

class CoursesSlim2(BaseModel):
    title:str
    code:str
    user:AddedBySlim
    created_at: datetime
    updated_at: Optional[datetime]
    # groups: List[GroupSlim]  # <-- Ajouté
    model_config = ConfigDict(from_attributes=True)  


class CoursesSlim(BaseModel):
    uuid:str
    title:str
    code:str
    credits:int
    type:CourseType
    model_config = ConfigDict(from_attributes=True)

class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    uuid:str
    title:Optional[str]=None
    code : Optional[str]=None
    credits : Optional[int]=None
    type : Optional[CourseType]=None
    speciality_uuid : Optional[str]=None
    group_uuid : Optional[str]=None
    academic_year_uuid : Optional[str]=None
    semester_uuid : Optional[str]=None


class Course(BaseModel):
    uuid:str
    title:str
    code:str
    credits:int
    type:str
    speciality:SpecialitySlim
    group:GroupSlim
    user:AddedBy
    created_at:datetime
    updated_at:datetime
    academic_year:AcademicYearSlim
    semester:Optional[SemesterSlim1]=None
    model_config = ConfigDict(from_attributes=True)

class CourseResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[Course]

    model_config = ConfigDict(from_attributes=True)

class CourseDelete(BaseModel):
    uuid:str