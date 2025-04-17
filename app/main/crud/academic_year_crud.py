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

class CRUDAcademicYear(CRUDBase[models.AcademicYear,schemas.AcademicYearCreate,schemas.AcademicYearUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.AcademicYear).filter(models.AcademicYear.uuid == uuid,models.AcademicYear.is_deleted==False,models.AcademicYear.status.in_(["ACTIVE"])).first()
    
    @classmethod
    def get_by_name(cls,db:Session,*,name:str):
        return db.query(models.AcademicYear).filter(models.AcademicYear.name == name,models.AcademicYear.is_deleted==False,models.AcademicYear.status.in_(["ACTIVE"])).first()
    
    @classmethod
    def get_by_start_date(cls,db:Session,*,start_date:date):
        return db.query(models.AcademicYear).filter(models.AcademicYear.start_date == start_date,models.AcademicYear.is_deleted==False,models.AcademicYear.status.in_(["ACTIVE"])).first()
    
    @classmethod
    def get_by_end_date(cls, db:Session,*, end_date: date):
        return db.query(models.AcademicYear).filter(models.AcademicYear.end_date == end_date,models.AcademicYear.is_deleted==False,models.AcademicYear.status.in_(["ACTIVE"])).first()
    

    @classmethod
    def get_all(cls,*,db:Session):
        return db.query(models.AcademicYear).filter(models.AcademicYear.is_deleted==False,models.AcademicYear.status.in_(["ACTIVE"]),models.AcademicYear.status.in_(["ACTIVE"])).all()
    
    @classmethod
    def get_by_date_range(cls,*,db: Session, start_date: date, end_date: date):
        return db.query(models.AcademicYear).filter(
            models.AcademicYear.start_date <= end_date,
            models.AcademicYear.end_date >= start_date,
            models.AcademicYear.is_deleted==False,
            models.AcademicYear.status.in_(["ACTIVE"])
        ).first()
    
    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.AcademicYearCreate,added_by:str):
        academic_year = models.AcademicYear(
            uuid = str(uuid.uuid4()),
            name = obj_in.name,
            start_date = obj_in.start_date,
            end_date = obj_in.end_date,
            added_by = added_by
        )
        db.add(academic_year)
        db.commit()
        db.refresh(academic_year)
        return academic_year
    
    @classmethod
    def update(cls,db:Session,*,obj_in:schemas.AcademicYearUpdate):
        academic_year = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if not academic_year:
            raise HTTPException(status_code=404, detail=__(key="academic_year-not-found"))
        
        academic_year.name = obj_in.name if obj_in.name else academic_year.name
        academic_year.start_date = obj_in.start_date if obj_in.start_date else academic_year.start_date
        academic_year.end_date = obj_in.end_date if obj_in.end_date else academic_year.end_date
        db.flush()
        db.commit()
        db.refresh(academic_year)
        return academic_year
    

    @classmethod
    def update_status(cls,db:Session,uuid:str,status:str):
        academic_year = cls.get_by_uuid(db=db, uuid=uuid)
        if not academic_year:
            raise HTTPException(status_code=404, detail=__(key="academic_year-not-found"))
        academic_year.status = status
        db.commit()


    @classmethod
    def delete(cls, db: Session,*, uuid: str):
        academic_year = cls.get_by_uuid(db=db, uuid=uuid)
        if not academic_year:
            raise HTTPException(status_code=404, detail=__(key="academic_year-not-found"))
        academic_year.is_deleted = True
        db.commit()

    @classmethod
    def get_many(
        cls,
        db:Session,
        page:int = 1,
        per_page:int = 5,

    ):
        record_query = db.query(models.AcademicYear).filter( models.AcademicYear.is_deleted == False)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)

        return schemas.AcademicYearResponseList(
            total = total,
            pages = math.ceil(total/per_page),
            per_page = per_page,
            current_page =page,
            data =record_query
        )



academic_year = CRUDAcademicYear(models.AcademicYear)