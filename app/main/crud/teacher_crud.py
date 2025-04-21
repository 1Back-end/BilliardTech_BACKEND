import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from app.main.core.security import generate_matricule, generate_password, get_password_hash,verify_password
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models,schemas
from app.main.core.mail import send_teacher_account_creation_email


class CRUDTeacher(CRUDBase[models.Teacher,schemas.TeacherBase,schemas.TeacherCreate]):

    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Teacher).filter(models.Teacher.uuid==uuid,models.Teacher.is_deleted==False).first()
    
    @classmethod
    def get_by_email(cls,db:Session,*,email:str):
        return db.query(models.Teacher).filter(models.Teacher.email==email,models.Teacher.is_deleted==False).first()
    
    @classmethod
    def get_by_login(cls,db:Session,*,login:str):
        return db.query(models.Teacher).filter(models.Teacher.login==login,models.Teacher.is_deleted==False).first()
    
    @classmethod
    def get_by_phone_number(cls,db:Session,*,phone_number:str):
        return db.query(models.Teacher).filter(models.Teacher.phone_number==phone_number,models.Teacher.is_deleted==False).first()
    @classmethod
    def get_by_phone_number_2(cls,db:Session,*,phone_number_2:str):
        return db.query(models.Teacher).filter(models.Teacher.phone_number_2==phone_number_2,models.Teacher.is_deleted==False).first()
    
    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.TeacherCreate,added_by:str):
        password: str = generate_password(8, 8)
        print(f"User password: {password}")
        matricule = generate_matricule()
        print(f"Matricule created", matricule)

        db_obj = models.Teacher(
            uuid=str(uuid.uuid4()),
            matricule = matricule,
            first_name = obj_in.first_name,
            last_name = obj_in.last_name,
            address = obj_in.address,
            phone_number = obj_in.phone_number,
            phone_number_2 = obj_in.phone_number_2,
            email = obj_in.email,
            grade = obj_in.grade,
            avatar_uuid = obj_in.avatar_uuid,
            added_by = added_by,
            login = obj_in.login,
            password_hash=get_password_hash(password),

        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        send_teacher_account_creation_email(email_to=obj_in.email,name=f"{obj_in.first_name} {obj_in.last_name}",login=obj_in.login,password=password)
        return db_obj
    

    @classmethod
    def update(cls,db:Session,obj_in:schemas.TeacherUpdate,added_by:str):
        teacher = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if not teacher:
            raise HTTPException(status_code=404, detail=__(key="teacher-not-found"))
        teacher.first_name = obj_in.first_name if obj_in.first_name else teacher.first_name
        teacher.last_name = obj_in.last_name if obj_in.last_name else teacher.last_name
        teacher.address = obj_in.address if obj_in.address else teacher.address
        teacher.phone_number = obj_in.phone_number if obj_in.phone_number else teacher.phone_number
        teacher.phone_number_2 = obj_in.phone_number_2 if obj_in.phone_number_2 else teacher.phone_number_2
        teacher.email = obj_in.email if obj_in.email else teacher.email
        teacher.grade = obj_in.grade if obj_in.grade else teacher.grade
        teacher.avatar_uuid = obj_in.avatar_uuid if obj_in.avatar_uuid else teacher.avatar_uuid
        added_by = added_by
        teacher.login = obj_in.login if obj_in.login else teacher.login
        db.flush()
        db.commit()
        db.refresh(teacher)
        return teacher
    


    @classmethod
    def get_many(
        cls,
        db:Session,
        page:int = 1,
        per_page:int = 25,

    ):
        record_query = db.query(models.Teacher).filter( models.Teacher.is_deleted == False)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)

        return schemas.TeacherResponseList(
            total = total,
            pages = math.ceil(total/per_page),
            per_page = per_page,
            current_page =page,
            data =record_query
        )
    
    @classmethod
    def delete(cls,db:Session,*,uuid:str):
        teacher = cls.get_by_uuid(db=db,uuid=uuid)
        if not teacher:
            raise HTTPException(status_code=404, detail=__(key="teacher-not-found"))
        teacher.is_deleted = True
        db.commit()

    @classmethod
    def update_status(cls,db:Session,*,uuid:str,status:str):
        teacher = cls.get_by_uuid(db=db,uuid=uuid)
        if not teacher:
            raise HTTPException(status_code=404, detail=__(key="teacher-not-found"))
        teacher.status = status
        db.commit()

    @classmethod
    def get_all_teachers(cls, db: Session):
        return db.query(models.Teacher).filter(
            models.Teacher.is_deleted == False
        ).all()
    @classmethod
    def authenticate(cls, db: Session, *, login: str, password: str) -> Union[models.Teacher, None]:
        db_obj: models.Teacher = db.query(models.Teacher).filter(models.Teacher.login == login).first()
        if not db_obj:
            return None
        if not verify_password(password, db_obj.password_hash):
            return None   
        return db_obj
    



teacher = CRUDTeacher(models.Teacher)