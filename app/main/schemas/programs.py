from datetime import date, datetime
from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional

from app.main.schemas.academic_year import AcademicYearSlim
from app.main.schemas.user import AddedBy


class ProgramsBase(BaseModel):
    code:str
    name:str
    academic_year_uuid:str

class ProgramsCreate(ProgramsBase):
    pass

class ProgramsUpdate(BaseModel):
    uuid : str
    code:Optional[str]
    name:Optional[str]
    academic_year_uuid:Optional[str]=None

class ProgramsDelete(BaseModel):
    uuid: str

class Programs(ProgramsBase):
    uuid: str
    created_at: datetime
    updated_at: datetime
    user:AddedBy
    academic_year:AcademicYearSlim
    model_config = ConfigDict(from_attributes=True)

class ProgramsSlim(BaseModel):
    uuid:str
    code:str
    name:str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProgramsSlim2(BaseModel):
    uuid:str
    name:str
    model_config = ConfigDict(from_attributes=True)



class ProgramResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[Programs]

    model_config = ConfigDict(from_attributes=True)