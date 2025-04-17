from datetime import date, datetime
from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional

from app.main.schemas.academic_year import AcademicYearSlim
from app.main.schemas.user import AddedBy

class SemesterBase(BaseModel):
    name:str
    start_date:date
    end_date:date
    academic_year_uuid:str

class SemesterCreate(SemesterBase):
    pass

class SemesterUpdate(BaseModel):
    uuid:str
    name: Optional[str]=None
    start_date: Optional[date]=None
    end_date: Optional[date]=None
    academic_year_uuid: Optional[str]=None

class SemesterUpdateStatus(BaseModel):
    uuid: str


class SemesterDelete(BaseModel):
    uuid: str

class Semester(BaseModel):
    uuid:str
    name: Optional[str]=None
    start_date: Optional[date]=None
    end_date: Optional[date]=None
    created_at:datetime
    updated_at:datetime
    status:str
    academic_year:AcademicYearSlim
    user:AddedBy

    model_config = ConfigDict(from_attributes=True)

    
class SemesterSlim1(BaseModel):
    uuid:str
    name: Optional[str]=None
    model_config = ConfigDict(from_attributes=True)

class SemesterUpdateStatus(BaseModel):
    uuid: str
    status : str

class SemesterResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[Semester]

    model_config = ConfigDict(from_attributes=True)