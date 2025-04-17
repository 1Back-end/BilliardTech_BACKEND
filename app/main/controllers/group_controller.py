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

router = APIRouter(prefix="/class", tags=["class"])


@router.post("/create",response_model=schemas.Msg)
def create_class(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.GroupCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    exist_name = crud.group.get_by_name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=409,detail=__(key="class-already-exists"))
    academic_year_uuid = crud.academic_year.get_by_uuid(db=db,uuid=obj_in.academic_year_uuid)
    if not academic_year_uuid:
        raise HTTPException(status_code=400, detail=__(key="academic-year-not-found"))
    speciality_uuid = crud.departments.get_by_uuid(db=db,uuid=obj_in.speciality_uuid)
    if not speciality_uuid:
        raise HTTPException(status_code=400, detail=__(key="department-not-found"))
    
    crud.group.create(db=db,obj_in=obj_in,added_by=current_user.uuid)
    return {"message": __(key="class-created-successfully")}

@router.put("/update",response_model=schemas.Msg)
def update_class(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.GroupUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    academic_year_uuid = crud.academic_year.get_by_uuid(db=db,uuid=obj_in.academic_year_uuid)
    if not academic_year_uuid:
        raise HTTPException(status_code=400, detail=__(key="academic-year-not-found"))
    speciality_uuid = crud.departments.get_by_uuid(db=db,uuid=obj_in.speciality_uuid)
    if not speciality_uuid:
        raise HTTPException(status_code=400, detail=__(key="department-not-found"))
    
    crud.group.update(db=db,obj_in=obj_in,added_by=current_user.uuid)
    return {"message": __(key="class-updated-successfully")}

@router.put("/delete",response_model=schemas.Msg)
def delete_class(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.GroupDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.group.delete(db=db,uuid=obj_in.uuid)
    return {"message": __(key="class-deleted-successfully")}


@router.get("/get_all",response_model=List[schemas.GroupSlim])
def get_all_class(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    return crud.group.get_all(db=db)

@router.get("/get_many", response_model=None)
def get(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 5,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    """
    get administrator with all data by passing filters
    """
    
    return crud.group.get_many(
        db, 
        page, 
        per_page, 
    )