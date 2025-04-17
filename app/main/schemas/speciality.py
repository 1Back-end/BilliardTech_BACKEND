from datetime import date, datetime
from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional
from app.main.schemas.academic_year import AcademicYearSlim
from app.main.schemas.programs import ProgramsSlim
from app.main.schemas.user import AddedBy


class SpecialityBase(BaseModel):
    code:str
    name:str
    program_uuid:str
    academic_year_uuid:str

class SpecialityCreate(SpecialityBase):
    pass

class SpecialityUpdate(BaseModel):
    uuid:str
    code: Optional[str] = None
    name: Optional[str] = None
    program_uuid: Optional[str] = None
    academic_year_uuid:Optional[str]=None

class SpecialityDelete(BaseModel):
    uuid: str


class Speciality(BaseModel):
    uuid: str
    code: str
    name: str
    program:ProgramsSlim
    academic_year:AcademicYearSlim
    user:AddedBy
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class SpecialityResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[Speciality]

    model_config = ConfigDict(from_attributes=True)


class SpecialitySlim(BaseModel):
    uuid:str
    name : str
    model_config = ConfigDict(from_attributes=True)