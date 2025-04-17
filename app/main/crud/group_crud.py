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
from app.main import models,schemas,crud


class CRUDClass(CRUDBase[models.Group,schemas.GroupResponse,schemas.GroupCreate]):


    @classmethod
    def get_by_name(cls,db:Session,*,name:str):
        return db.query(models.Group).filter(models.Group.name==name,models.Group.is_deleted==False).first()
    

    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
         return db.query(models.Group).filter(models.Group.uuid==uuid,models.Group.is_deleted==False).first()
    
    @classmethod
    def create(cls,db:Session,obj_in:schemas.GroupCreate,added_by:str):
        db_obj = models.Group(
            uuid = str(uuid.uuid4()),
            name = obj_in.name,
            level = obj_in.level,
            academic_year_uuid = obj_in.academic_year_uuid,
            speciality_uuid = obj_in.speciality_uuid,
            added_by =added_by
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    

    @classmethod
    def update(cls,db:Session,obj_in:schemas.GroupUpdate,added_by:str):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="class-not-found"))
        db_obj.name = obj_in.name if obj_in.name else db_obj.name
        db_obj.level = obj_in.level if obj_in.level else db_obj.level
        db_obj.academic_year_uuid = obj_in.academic_year_uuid if obj_in.academic_year_uuid else db_obj.academic_year_uuid
        db_obj.speciality_uuid = obj_in.speciality_uuid if obj_in.speciality_uuid else db_obj.speciality_uuid

        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    @classmethod
    def get_all(cls,db:Session):
        return db.query(models.Group).filter(models.Group.is_deleted==False).all()
    
    @classmethod
    def delete(cls,db:Session,*,uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="class-not-found"))
        db_obj.is_deleted = True
        db.commit()
    
    @classmethod
    def get_many(
        cls,
        db:Session,
        page:int = 1,
        per_page:int = 5,

    ):
        record_query = db.query(models.Group).filter(models.Group.is_deleted == False)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)

        return schemas.GroupResponseList(
            total = total,
            pages = math.ceil(total/per_page),
            per_page = per_page,
            current_page =page,
            data =record_query
        )


group = CRUDClass(models.Group)