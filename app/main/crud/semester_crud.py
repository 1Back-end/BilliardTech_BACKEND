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


class CRUDSemester(CRUDBase[models.Semester,schemas.SemesterCreate,schemas.SemesterUpdate]):

    @classmethod
    def get_by_name(cls,db:Session,*,name:str):
        return db.query(models.Semester).filter(models.Semester.name == name,models.Semester.is_deleted==False).first()
    
    @classmethod
    def get_by_year(cls, db: Session,*, academic_year_uuid:str):
        return db.query(models.Semester).filter(models.Semester.academic_year_uuid == academic_year_uuid, models.Semester.is_deleted==False,models.Semester.status.in_(["ACTIVE"])).all()
    
    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Semester).filter(models.Semester.uuid == uuid, models.Semester.is_deleted==False).first()
    
    @classmethod
    def get_by_academic_year(cls,db:Session,*,academic_year_uuid:str):
        return db.query(models.Semester).filter(models.Semester.academic_year_uuid == academic_year_uuid, models.Semester.is_deleted==False,models.Semester.status.in_(["ACTIVE"])).all()
    

    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.SemesterCreate,added_by:str):
        db_obj = models.Semester(
            uuid=str(uuid.uuid4()),
            name=obj_in.name,
            start_date = obj_in.start_date,
            end_date = obj_in.end_date,
            academic_year_uuid=obj_in.academic_year_uuid,
            added_by=added_by,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    

    @classmethod
    def update(cls,db:Session,*,obj_in:schemas.SemesterUpdate,added_by:str):
        semester  = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if not semester:
            raise HTTPException(status_code=404, detail=__("semester-not-found"))
        
        semester.name = obj_in.name if obj_in.name else semester.name
        semester.start_date = obj_in.start_date if obj_in.start_date else semester.start_date
        semester.end_date = obj_in.end_date if obj_in.end_date else semester.end_date
        semester.academic_year_uuid = obj_in.academic_year_uuid if obj_in.academic_year_uuid else semester.academic_year_uuid
        
        db.flush()
        db.commit()
        db.refresh(semester)
        return semester
    


    @classmethod
    def delete(cls, db: Session,*, uuid: str):
        semester = cls.get_by_uuid(db=db, uuid=uuid)
        if not semester:
            raise HTTPException(status_code=404, detail=__("semester-not-found"))
        semester.is_deleted = True
        db.commit()

    @classmethod
    def update_status(cls,db:Session,uuid:str,status:str):
        semester = cls.get_by_uuid(db=db,uuid=uuid)
        if not semester:
            raise HTTPException(status_code=404, detail=__("semester-not-found"))
        semester.status = status
        db.commit()


    @classmethod
    def get_all(cls,db:Session):
        return db.query(models.Semester).filter(models.Semester.is_deleted==False).all()
    
    @classmethod
    def get_many(
        cls,
        db:Session,
        page:int = 1,
        per_page:int = 10,

    ):
        record_query = db.query(models.Semester).filter( models.Semester.is_deleted==False)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)

        return schemas.SemesterResponseList(
            total = total,
            pages = math.ceil(total/per_page),
            per_page = per_page,
            current_page =page,
            data =record_query
        )




semester = CRUDSemester(models.Semester)