from datetime import date, datetime
from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional
from app.main.schemas.academic_year import AcademicYearSlim
from app.main.schemas.group import GroupSlim
from app.main.schemas.file import FileSlim2
from app.main.schemas.programs import ProgramsSlim2
from app.main.schemas.semester import SemesterSlim1
from app.main.schemas.user import AddedBy


class SubjectBase(BaseModel):
    name:str
    code:str
    credits:int
    program_uuid:str
    semester_uuid:str

class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    uuid:str
    code : Optional[str]=None
    name : Optional[str]=None
    credits : Optional[int]=None
    program_uuid :Optional[str]=None
    semester_uuid : Optional[str]=None


class SubjectDelete(BaseModel):
    uuid: str


class Subject(BaseModel):
    uuid:str
    name:str
    code:str
    credits:int
    program:ProgramsSlim2
    semester:SemesterSlim1
    user:AddedBy
    model_config = ConfigDict(from_attributes=True)
