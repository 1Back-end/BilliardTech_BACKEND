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



class CRUDCourse(CRUDBase[models.Course,schemas.CourseBase,schemas.CourseCreate]):

    @staticmethod
    def get_by_uuids(db: Session, uuids: List[str]):
        return db.query(models.Course).filter(
            models.Course.uuid.in_(uuids),  # Utilisation de 'in' pour filtrer plusieurs UUIDs
            models.Course.is_deleted == False
        ).all()
    
    @classmethod
    def get_all_courses(cls, db: Session):
        return db.query(models.Course).filter(
            models.Course.is_deleted == False
        ).all()


    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Course).filter(models.Course.uuid==uuid,models.Course.is_deleted==False).first()
    
    @classmethod
    def get_by_title(cls,db:Session,*,title:str):
        return db.query(models.Course).filter(models.Course.title==title,models.Course.is_deleted==False).first()
    
    @classmethod
    def get_by_code(cls,db:Session,*,code:str):
        return db.query(models.Course).filter(models.Course.code==code,models.Course.is_deleted==False).first()
    
    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.CourseCreate,added_by:str):
        db_obj = models.Course(
            uuid = str(uuid.uuid4()),
            title = obj_in.title,
            code = obj_in.code,
            credits = obj_in.credits,
            type = models.CourseType.CM,
            speciality_uuid = obj_in.speciality_uuid,
            group_uuid = obj_in.group_uuid,
            academic_year_uuid = obj_in.academic_year_uuid,
            semester_uuid = obj_in.semester_uuid,
            added_by=added_by

        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    

    @classmethod
    def delete(cls,db:Session,*,uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="course-not-found"))
        db_obj.is_deleted = True
        db.commit()

    @classmethod
    def get_many(
        cls,
        db:Session,
        page:int = 1,
        per_page:int = 25,

    ):
        record_query = db.query(models.Course).filter(models.Course.is_deleted == False)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)

        return schemas.CourseResponseList(
            total = total,
            pages = math.ceil(total/per_page),
            per_page = per_page,
            current_page =page,
            data =record_query
        )
    
    @classmethod
    def update(cls,db:Session,*,obj_in:schemas.CourseUpdate,added_by:str):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="course-not-found"))
        db_obj.title = obj_in.title if obj_in.title else db_obj.title
        db_obj.code = obj_in.code if obj_in.code else db_obj.code
        db_obj.credits = obj_in.credits if obj_in.credits else db_obj.credits
        db_obj.type = obj_in.type if obj_in.type else db_obj.type
        db_obj.speciality_uuid = obj_in.speciality_uuid if obj_in.speciality_uuid else db_obj.speciality_uuid
        db_obj.group_uuid = obj_in.group_uuid if obj_in.group_uuid else db_obj.group_uuid
        db_obj.academic_year_uuid = obj_in.academic_year_uuid if obj_in.academic_year_uuid else db_obj.academic_year_uuid
        db_obj.semester_uuid = obj_in.semester_uuid if obj_in.semester_uuid else db_obj.semester_uuid

        db.flush()
        db.commit()
        db.refresh(db_obj)
        return db_obj
    



course = CRUDCourse(models.Course)

    
    