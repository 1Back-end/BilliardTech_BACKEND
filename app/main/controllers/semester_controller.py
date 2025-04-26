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

router = APIRouter(prefix="/semester", tags=["semester"])


@router.post("/create",response_model=schemas.Msg)
def create_semester(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.SemesterCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    academic_year = crud.academic_year.get_by_uuid(db=db,uuid=obj_in.academic_year_uuid)
    if not academic_year:
        raise HTTPException(status_code=404, detail=__(key="academic_year-not-found"))
    
    exist_name = crud.semester.get_by_name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=400, detail=__(key="semester-exist-name"))
    
    added_by = current_user.uuid
    crud.semester.create(db=db,obj_in=obj_in,added_by=added_by)
    return schemas.Msg(message=__(key="semester-add-sucessfully"))
    


@router.put("/update",response_model=schemas.Msg)
def update_semester(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.SemesterUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    semester = crud.semester.get_by_uuid(db=db,uuid=obj_in.uuid)
    if not semester:
        raise HTTPException(status_code=404, detail=__(key="semester-not-found"))
    
    added_by = current_user.uuid
    crud.semester.update(db=db,obj_in=obj_in,added_by=added_by)
    return schemas.Msg(message=__(key="semester-update-sucessfully"))
    
@router.put("/delete",response_model=schemas.Msg)
def delete_semester(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.SemesterDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.semester.delete(db=db, uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="semester-delete-sucessfully"))


@router.get("/get_all",response_model=List[schemas.Semester])
def get_all_semester(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    return crud.semester.get_all(db=db)

@router.get("/get_uuid_and_name_semester",response_model=List[schemas.SemesterSlim1])
def get_all_semester(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN","PROFESSEUR"]))
):
    return crud.semester.get_all(db=db)


@router.get("/get_many", response_model=None)
def get(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    """
    get administrator with all data by passing filters
    """
    
    return crud.semester.get_many(
        db, 
        page, 
        per_page, 
    )

@router.put('/update-status-semester',response_model=schemas.Msg)
def update_status_academic_year(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.SemesterUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.semester.update_status(db=db,uuid=obj_in.uuid,status=obj_in.status)
    return schemas.Msg(message=__(key="semester-status-updated-successfully"))