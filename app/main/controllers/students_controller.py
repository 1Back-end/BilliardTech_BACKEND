from datetime import timedelta, datetime
from typing import Any, List
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.security import create_access_token, get_password_hash
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/create", response_model=schemas.Msg)
def create_student(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.StudentCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    if obj_in.storage_uuid:
        avatar = crud.storage_crud.get_file_by_uuid(db=db,file_uuid=obj_in.storage_uuid)
        if not avatar:
            raise HTTPException(status_code=404, detail=__(key="avatar-not-found"))
        
    exist_email = crud.students.get_by_email(db=db, email=obj_in.email)
    if exist_email:
        raise HTTPException(status_code=409, detail=__(key="email-already-exists"))
    
    exist_phone = crud.students.get_by_phone_number(db=db, phone_number=obj_in.phone_number)
    if exist_phone:
        raise HTTPException(status_code=409, detail=__(key="phone-number-already-exists"))
    
    group= crud.group.get_by_uuid(db=db, uuid=obj_in.group_uuid)
    if not group:
        raise HTTPException(status_code=404, detail=__(key="class-not-found"))
    
    academic_year_uuid = crud.academic_year.get_by_uuid(db=db,uuid=obj_in.academic_year_uuid)
    if not academic_year_uuid:
        raise HTTPException(status_code=400, detail=__(key="academic-year-not-found"))
    
    program_uuid = crud.programs.get_by_uuid(db=db,uuid=obj_in.program_uuid)
    if not program_uuid:
        raise HTTPException(status_code=400, detail=__(key="program-not-found"))
    
    speciality_uuid = crud.departments.get_by_uuid(db=db,uuid=obj_in.speciality_uuid)
    if not speciality_uuid:
        raise HTTPException(status_code=400, detail=__(key="department-not-found"))
    
    crud.students.create(db=db, obj_in=obj_in, added_by=current_user.uuid)
    return {"message":__(key="student-created-successfully")}


@router.get("/get_students_by_class",response_model=List[schemas.Student])
def get_students_by_class(
    *,
    db: Session = Depends(get_db),
    class_uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    return crud.students.get_by_class(db=db, class_uuid=class_uuid)

@router.get("/get_students_by_academic_year",response_model=List[schemas.Student])
def get_students_by_academic_year(
    *,
    db: Session = Depends(get_db),
    academic_year_uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    return crud.students.get_academic_year(db=db, academic_year_uuid=academic_year_uuid)

@router.put("/delete",response_model=schemas.Msg)
def delete_student(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.StudentDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.students.delete(db=db, uuid=obj_in.uuid)
    return {"message":__(key="student-deleted-successfully")}

@router.put("/update",response_model=schemas.Msg)
def update_student(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.StudentUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    if obj_in.storage_uuid:
        avatar = crud.storage_crud.get_file_by_uuid(db=db,file_uuid=obj_in.storage_uuid)
        if not avatar:
            raise HTTPException(status_code=404, detail=__(key="avatar-not-found"))
        
    
    group= crud.group.get_by_uuid(db=db, uuid=obj_in.group_uuid)
    if not group:
        raise HTTPException(status_code=404, detail=__(key="class-not-found"))
    
    academic_year_uuid = crud.academic_year.get_by_uuid(db=db,uuid=obj_in.academic_year_uuid)
    if not academic_year_uuid:
        raise HTTPException(status_code=400, detail=__(key="academic-year-not-found"))
    
    program_uuid = crud.programs.get_by_uuid(db=db,uuid=obj_in.program_uuid)
    if not program_uuid:
        raise HTTPException(status_code=400, detail=__(key="program-not-found"))
    
    speciality_uuid = crud.departments.get_by_uuid(db=db,uuid=obj_in.speciality_uuid)
    if not speciality_uuid:
        raise HTTPException(status_code=400, detail=__(key="department-not-found"))
    
    crud.students.update(db=db, obj_in=obj_in,added_by=current_user.uuid)
    return {"message":__(key="student-updated-successfully")}
    

@router.get("/get_many", response_model=None)
def get(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 25,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    """
    get administrator with all data by passing filters
    """
    
    return crud.students.get_many(
        db, 
        page, 
        per_page, 
    )

@router.get("/get_by_uuid",response_model=schemas.Student)
def get_student_by_uuid(
    *,
    db: Session = Depends(get_db),
    uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.students.get_by_uuid(db=db,uuid=uuid)