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


class CRUDSubjects(CRUDBase[models.Subject,schemas.SubjectCreate,schemas.SubjectUpdate]):


    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Subject).filter(models.Subject.uuid == uuid,models.Subject.is_deleted==False).first()
    
    @classmethod
    def get_by_code(cls,db:Session,*,code:str):
        return db.query(models.Subject).filter(models.Subject.code == code,models.Subject.is_deleted==False).first()
    
    @classmethod
    def get_by_name(cls,db:Session,*,name:str):
        return db.query(models.Subject).filter(models.Subject.name == name,models.Subject.is_deleted==False).first()
    
    @classmethod
    def get_by_program(cls,db:Session,*,program_uuid:str):
        return db.query(models.Subject).filter(models.Subject.program_uuid == program_uuid,models.Subject.is_deleted==False).all()
    

    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.SubjectCreate,added_by:str):
        subject = models.Subject(
            uuid = str(uuid.uuid4()),
            name = obj_in.name,
            code = obj_in.code,
            credits = obj_in.credits,
            program_uuid = obj_in.program_uuid,
            semester_uuid = obj_in.semester_uuid,
            added_by = added_by
        )
        db.add(subject)
        db.commit()
        db.refresh(subject)
        return subject
    

    @classmethod
    def update(cls,db:Session,*,obj_in:schemas.SubjectUpdate,added_by:str):
        subject = cls.get_by_uuid(db=db, uuid=obj_in.uuid)
        if not subject:
            raise HTTPException(status_code=404, detail=__(key="subject-not-found"))
        
        subject.name = obj_in.name if obj_in.name else subject.name
        subject.code = obj_in.code if obj_in.code else subject.code
        subject.credits = obj_in.credits if obj_in.credits else subject.credits
        subject.program_uuid = obj_in.program_uuid if obj_in.program_uuid else subject.program_uuid
        subject.semester_uuid = obj_in.semester_uuid if obj_in.semester_uuid else subject.semester_uuid
        db.commit()
        db.refresh(subject)
        return subject
    

    @classmethod
    def delete(cls,db:Session,*,uuid:str):
        subject = cls.get_by_uuid(db=db, uuid=uuid)
        if not subject:
            raise HTTPException(status_code=404, detail=__(key="subject-not-found"))
        
        subject.is_deleted = True
        db.commit()
        
    
subjects = CRUDSubjects(models.Subject)