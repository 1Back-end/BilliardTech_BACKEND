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


class CRUDTypeCourses(CRUDBase[models.TypeCourse,schemas.TypeCoursesBase,schemas.TypeCoursesResponseList]):

    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.TypeCourse).filter(models.TypeCourse.uuid==uuid,models.TypeCourse.is_deleted==False).first()
    
    @classmethod
    def get_by_name(cls,db:Session,*,name:str):
        return db.query(models.TypeCourse).filter(models.TypeCourse.name==name,models.TypeCourse.is_deleted==False).first()
    
    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.TypeCoursesCreate,added_by:str):
        db_obj = models.TypeCourse(
            uuid = str(uuid.uuid4()),
            name = obj_in.name,
            added_by=added_by
        )
        db.add()
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    @classmethod
    def update(cls,db:Session,*,obj_in:schemas.TypeCoursesUpdate,added_by:str):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="type-course-not-found"))
        db_obj.name = obj_in.name if obj_in.name else obj_in.name
        added_by=added_by
        db.commit()
        db.refresh(db_obj)
        return db_obj
    