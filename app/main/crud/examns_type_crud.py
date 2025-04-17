from datetime import date, datetime
import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models,schemas



class CRUDTypeOfExamn(CRUDBase[models.TypeOfExam,schemas.TypeOfExamnCreate,schemas.TypeOfExamnDelete]):


    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.TypeOfExam).filter(models.TypeOfExam.uuid==uuid,models.TypeOfExam.is_deleted==False).first()
    

    @classmethod
    def get_by_name(cls,db:Session,*,name:str):
        return db.query(models.TypeOfExam).filter(models.TypeOfExam.name==name,models.TypeOfExam.is_deleted==False).first()
    
    @classmethod
    def get_by_code(cls,db:Session,*,code:str):
        return db.query(models.TypeOfExam).filter(models.TypeOfExam.code==code,models.TypeOfExam.is_deleted==False).first()
    
    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.TypeOfExamnCreate,added_by:str):
        db_obj = models.TypeOfExam(
            uuid = str(uuid.uuid4()),
            code = obj_in.code,
            name = obj_in.name,
            percentage = obj_in.percentage,
            added_by = added_by
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    

    @classmethod
    def update(cls,db:Session,*,obj_in:schemas.TypeOfExamnUpdate,updated_by:str):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="type-examen-not-found"))
        db_obj.code = obj_in.code if obj_in.code else db_obj.code
        db_obj.name = obj_in.name if obj_in.name else db_obj.name
        db_obj.percentage = obj_in.percentage if obj_in.percentage else db_obj.percentage
        updated_by = updated_by
        db.flush()
        db.commit()
        db.refresh(db_obj)
        return db_obj
    

    @classmethod
    def delete(cls,db:Session,*,uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="type-examen-not-found"))
        db_obj.is_deleted = True
        db.commit()


    @classmethod
    def get_many(
        cls,
        db:Session,
        page:int = 1,
        per_page:int = 5,

    ):
        record_query = db.query(models.TypeOfExam).filter(models.TypeOfExam.is_deleted == False)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)

        return schemas.TypeOfExamnSlimResponseList(
            total = total,
            pages = math.ceil(total/per_page),
            per_page = per_page,
            current_page =page,
            data =record_query
        )



type_of_examen = CRUDTypeOfExamn(models.TypeOfExam)
    