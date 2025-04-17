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
from app.main.core.mail import send_account_creation_email,send_student_matricule
from app.main.crud.base import CRUDBase
from app.main import models,schemas
from app.main.core.security import generate_matricule


class CRUDStudents(CRUDBase[models.Student,schemas.StudentCreate,schemas.StudentUpdate]):

    @classmethod
    def get_by_email(cls,db:Session,*,email:str):
        return db.query(models.Student).filter(models.Student.email==email,models.Student.is_deleted==False).first()
    
    @classmethod
    def get_by_matricule(cls,db:Session,*,matricule:str):
        return db.query(models.Student).filter(models.Student.matricule==matricule,models.Student.is_deleted==False).first()
    
    @classmethod
    def get_by_phone_number(cls,db:Session,*,phone_number:str):
        return db.query(models.Student).filter(models.Student.phone_number==phone_number,models.Student.is_deleted==False).first()    
    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Student).filter(models.Student.uuid==uuid,models.Student.is_deleted==False).first()
    
    @classmethod
    def get_by_class(cls,db:Session,*,class_uuid:str):
        return db.query(models.Student).filter(models.Student.class_uuid==class_uuid, models.Student.is_deleted==False).all()
    
    @classmethod
    def get_academic_year(cls,db:Session,*,academic_year_uuid:str):
        return db.query(models.Student).filter(models.Student.academic_year_uuid==academic_year_uuid, models.Student.is_deleted==False).all()
    
    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.StudentCreate,added_by:str):
        matricule = generate_matricule()
        print(f"Matricule created", matricule)
        db_obj = models.Student(
            uuid=str(uuid.uuid4()),
            matricule=matricule,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            phone_number=obj_in.phone_number,
            birthdate=obj_in.birthdate,
            address=obj_in.address,
            gender = obj_in.gender,
            nationality=obj_in.nationality,
            group_uuid=obj_in.group_uuid,
            storage_uuid=obj_in.storage_uuid,
            academic_year_uuid=obj_in.academic_year_uuid,
            program_uuid = obj_in.program_uuid,
            speciality_uuid = obj_in.speciality_uuid,
            added_by=added_by
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        send_student_matricule(email_to=obj_in.email,name=f"{obj_in.first_name} {obj_in.last_name}",matricule=matricule)
        return db_obj
    

    @classmethod
    def update(cls,db:Session,*,obj_in:schemas.StudentUpdate,added_by:str):
        db_obj = cls.get_by_uuid(db,uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="student-not-found"))
        db_obj.first_name = obj_in.first_name if obj_in.first_name else db_obj.first_name
        db_obj.last_name = obj_in.last_name if obj_in.last_name else db_obj.last_name
        db_obj.email = obj_in.email if obj_in.email else db_obj.email
        db_obj.phone_number = obj_in.phone_number if obj_in.phone_number else db_obj.phone_number
        db_obj.birthdate = obj_in.birthdate if obj_in.birthdate else db_obj.birthdate
        db_obj.address = obj_in.address if obj_in.address else db_obj.address
        db_obj.gender = obj_in.gender if obj_in.gender else db_obj.gender
        db_obj.nationality = obj_in.nationality if obj_in.nationality else db_obj.nationality
        db_obj.group_uuid = obj_in.group_uuid if obj_in.group_uuid else db_obj.group_uuid
        db_obj.storage_uuid = obj_in.storage_uuid if obj_in.storage_uuid else db_obj.storage_uuid
        db_obj.academic_year_uuid = obj_in.academic_year_uuid if obj_in.academic_year_uuid else db_obj.academic_year_uuid
        db_obj.program_uuid = obj_in.program_uuid if obj_in.program_uuid else db_obj.program_uuid
        db_obj.speciality_uuid = obj_in.speciality_uuid if obj_in.speciality_uuid else db_obj.speciality_uuid
        added_by=added_by
        db.commit()
        db.refresh(db_obj)
        return db_obj

    
    @classmethod
    def delete(cls,db:Session,*,uuid:str):
        db_obj = cls.get_by_uuid(db=db, uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="student-not-found"))
        db_obj.is_deleted = True
        db.commit()

    @classmethod
    def get_many(
        cls,
        db:Session,
        page:int = 1,
        per_page:int = 25,

    ):
        record_query = db.query(models.Student).filter( models.Student.is_deleted == False)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)

        return schemas.StudentResponseList(
            total = total,
            pages = math.ceil(total/per_page),
            per_page = per_page,
            current_page =page,
            data =record_query
        )

    

students = CRUDStudents(models.Student)