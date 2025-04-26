from datetime import date, datetime
from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional
from app.main.schemas.academic_year import AcademicYearSlim
from app.main.schemas.programs import ProgramsSlim
from app.main.schemas.speciality import SpecialitySlim
from app.main.schemas.user import AddedBy

class GroupBase(BaseModel):
    name:str
    level:str
    academic_year_uuid:str
    speciality_uuid:str

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    uuid:str
    name : Optional[str]=None
    level : Optional[str]=None
    academic_year_uuid : Optional[str]=None
    speciality_uuid : Optional[str]=None
   
class GroupDelete(BaseModel):
    uuid:str

class GroupResponse(BaseModel):
    uuid:str
    name:str
    level:str
    user:AddedBy
    speciality:SpecialitySlim
    academic_year:AcademicYearSlim
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class GroupSlim(BaseModel):
    uuid:str
    name:str
    model_config = ConfigDict(from_attributes=True)

class GroupSlim(BaseModel):
    uuid:str
    name:str
    level:str
    model_config = ConfigDict(from_attributes=True)

class GroupResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[GroupResponse]

    model_config = ConfigDict(from_attributes=True)


class GroupOut(BaseModel):
    uuid: str
    name: str
    model_config = ConfigDict(from_attributes=True)