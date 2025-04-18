from datetime import date, datetime
from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional
from app.main.schemas.file import FileSlim2
from app.main.schemas.user import AddedBy


class TeacherBase(BaseModel):
    first_name:str
    last_name : str
    address : str
    phone_number:str
    phone_number_2:Optional[str]=None
    email : EmailStr
    grade:str
    login:str
    avatar_uuid:Optional[str]=None

class TeacherCreate(TeacherBase):
    pass

class TeacherUpdate(BaseModel):
    uuid : str
    first_name : Optional[str]=None
    last_name : Optional[str]=None
    address : Optional[str]=None
    phone_number : Optional[str]=None
    phone_number_2 : Optional[str]=None
    email : Optional[EmailStr]=None
    grade : Optional[str]=None
    login:Optional[str]=None
    avatar_uuid:Optional[str]=None

 
class TeacherSlim(BaseModel):
    uuid : str
    first_name : Optional[str]=None
    last_name : Optional[str]=None
    model_config = ConfigDict(from_attributes=True)



class TeacherDelete(BaseModel):
    uuid :str

class TeacherUpdateStatus(BaseModel):
    uuid : str
    status: str

class Teacher(BaseModel):
    uuid:str
    matricule:str
    first_name:str
    last_name : str
    address : str
    phone_number:str
    phone_number_2:Optional[str]=None
    email : EmailStr
    grade:str
    login:str
    status : str
    avatar:Optional[FileSlim2]=None
    user : AddedBy
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TeacherResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[Teacher]

    model_config = ConfigDict(from_attributes=True)
