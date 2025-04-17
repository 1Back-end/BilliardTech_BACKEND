from datetime import date, datetime
from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional
from app.main.schemas.user import AddedBy

class AcademicYear(BaseModel):
    name:str
    start_date: date
    end_date: date

class AcademicYearSlim(BaseModel):
     name:str
    

class AcademicYearCreate(AcademicYear):
    pass

class AcademicYearUpdate(BaseModel):
    uuid:str
    name : Optional[str]=None
    start_date : Optional[date]=None
    end_date : Optional[date]=None
    
class AcademicYearUpdateStatus(BaseModel):
    uuid: str
    status : str
class AcademicYearDelete(BaseModel):
    uuid: str

class AcademicYearResponse(BaseModel):
    uuid:str
    name : str
    start_date : date
    end_date : date
    status:str
    created_at:datetime
    updated_at:datetime
    user:AddedBy
    model_config = ConfigDict(from_attributes=True)

    
class AcademicYearSlim(BaseModel):
    uuid:str
    name : str
    status:str
    model_config = ConfigDict(from_attributes=True)

class AcademicYearResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[AcademicYearResponse]

    model_config = ConfigDict(from_attributes=True)