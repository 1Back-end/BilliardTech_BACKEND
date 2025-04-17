from datetime import date, datetime
from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional
from app.main.schemas.user import AddedBy



class TypeOfExamnBase(BaseModel):
    code:str
    name:str
    percentage:str

class TypeOfExamnCreate(TypeOfExamnBase):
    pass

class TypeOfExamnUpdate(BaseModel):
    uuid : str
    code : Optional[str]=None
    name : Optional[str]=None
    percentage : Optional[str]=None


class TypeOfExamn(TypeOfExamnBase):
    uuid : str
    created_at:datetime
    updated_at:datetime
    user:AddedBy
    updated_user:Optional[AddedBy]=None
    model_config = ConfigDict(from_attributes=True)

class TypeOfExamnSlim(BaseModel):
    uuid:str
    name:str
    model_config = ConfigDict(from_attributes=True)

class TypeOfExamnDelete(BaseModel):
    uuid:str

class TypeOfExamnSlimResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[TypeOfExamn]

    model_config = ConfigDict(from_attributes=True)

    

