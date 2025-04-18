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

router = APIRouter(prefix="/teachers", tags=["teachers"])

@router.post("/create",response_model=schemas.Msg)
def create_teacher(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TeacherCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    if obj_in.avatar_uuid:
        avatar = crud.storage_crud.get_file_by_uuid(db=db,file_uuid=obj_in.avatar_uuid)
        if not avatar:
            raise HTTPException(status_code=404, detail=__(key="avatar-not-found"))
    
    exist_phone = crud.teacher.get_by_phone_number(db=db, phone_number=obj_in.phone_number)
    if exist_phone:
        raise HTTPException(status_code=409, detail=__(key="phone_number-already-used"))
    
    # exist_phone_2 = crud.teacher.get_by_phone_number_2(db=db,phone_number_2=obj_in.phone_number_2)
    # if exist_phone_2:
    #     raise HTTPException(status_code=409, detail=__(key="phone_number-already-used"))

    exist_email = crud.teacher.get_by_email(db=db, email=obj_in.email)
    if exist_email:
        raise HTTPException(status_code=409, detail=__(key="email-already-used"))
    
    crud.teacher.create(
        db, obj_in=obj_in,added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="teacher-created-successfully"))



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
    
    return crud.teacher.get_many(
        db, 
        page, 
        per_page, 
    )
@router.get("/get_by_uuid",response_model=schemas.Teacher)
def get_teacher_by_uuid(
    *,
    db: Session = Depends(get_db),
    uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.teacher.get_by_uuid(db=db,uuid=uuid)

@router.put("/delete-teacher",response_model=schemas.Msg)
def delete_teacher(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TeacherDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.user.delete(db=db, uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="teacher-deleted-successfully"))

@router.put("/update-status",response_model=schemas.Msg)
def update_teacher_status(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TeacherUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.teacher.update_status(
        db,
        uuid=obj_in.uuid,
        status=obj_in.status
    )
    return schemas.Msg(message=__(key="teacher-status-updated-successfully"))

@router.put("/update-teacher",response_model=schemas.Msg)
def update(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TeacherUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    if obj_in.avatar_uuid:
        avatar = crud.storage_crud.get_file_by_uuid(db=db,file_uuid=obj_in.avatar_uuid)
        if not avatar:
            raise HTTPException(status_code=404, detail=__(key="avatar-not-found"))
    crud.teacher.update(
        db, obj_in=obj_in,added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="teacher-updated-successfully"))


@router.get("/get_all_teachers", response_model=List[schemas.TeacherSlim])
def get_user_teachers(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
   teachers = crud.teacher.get_all_teachers(db=db)
   return teachers