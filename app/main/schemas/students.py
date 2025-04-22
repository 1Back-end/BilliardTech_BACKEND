from datetime import date, datetime
from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional
from app.main.schemas.academic_year import AcademicYearSlim
from app.main.schemas.group import GroupSlim
from app.main.schemas.file import FileSlim2
from app.main.schemas.programs import ProgramsSlim2
from app.main.schemas.speciality import SpecialitySlim
from app.main.schemas.user import AddedBy

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number:str
    birthdate: date
    address:str
    gender : str
    nationality:str
    group_uuid:str
    storage_uuid: Optional[str] = None
    academic_year_uuid:str
    program_uuid:str
    speciality_uuid:str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    uuid:str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    birthdate: Optional[date] = None
    address: Optional[str] = None
    gender : Optional[str] = None
    nationality: Optional[str] = None
    group_uuid: Optional[str] = None
    storage_uuid: Optional[str] = None
    academic_year_uuid: Optional[str] = None
    program_uuid: Optional[str] = None
    speciality_uuid: Optional[str] = None
    

class StudentDelete(BaseModel):
    uuid: str

class StudentDetails(BaseModel):
    uuid: str


class Student(BaseModel):
    uuid:str
    matricule:str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number:str
    birthdate: date
    address:str
    gender : str
    nationality:str
    group:GroupSlim
    academic_year:AcademicYearSlim
    program:Optional[ProgramsSlim2]=None
    speciality : Optional[SpecialitySlim]=None
    avatar:Optional[FileSlim2]=None
    user:AddedBy
    created_at:datetime
    updated_at:datetime
    model_config = ConfigDict(from_attributes=True)

class StudentSlim2(BaseModel):
    uuid:str
    matricule:str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number:str
    birthdate: date
    address:str
    gender : str
    nationality:str
    group:GroupSlim
    created_at:datetime
    updated_at:datetime
    model_config = ConfigDict(from_attributes=True)
    
class StudentSlim(BaseModel):
    uuid:str
    matricule:str
    first_name: str
    last_name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
class StudentResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[Student]

    model_config = ConfigDict(from_attributes=True)