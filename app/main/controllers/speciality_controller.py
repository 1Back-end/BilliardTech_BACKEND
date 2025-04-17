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

router = APIRouter(prefix="/speciality", tags=["speciality"])

@router.post("/create",response_model=schemas.Msg)
def create_department(
    *,
    obj_in : schemas.SpecialityCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    exist_code = crud.departments.get_by_code(db=db,code=obj_in.code)
    if exist_code:
        raise HTTPException(status_code=400, detail=__(key="department-code-already-exists"))
    exist_name = crud.departments.get_by_name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=400, detail=__(key="department-name-already-exists"))
    program_uuid = crud.programs.get_by_uuid(db=db,uuid=obj_in.program_uuid)
    if not program_uuid:
        raise HTTPException(status_code=400, detail=__(key="program-not-found"))
    academic_year_uuid = crud.academic_year.get_by_uuid(db=db,uuid=obj_in.academic_year_uuid)
    if not academic_year_uuid:
        raise HTTPException(status_code=400, detail=__(key="academic-year-not-found"))
    crud.departments.create(db=db, obj_in=obj_in,added_by=current_user.uuid)
    return {"message": __(key="department-created-successfully")}



@router.put("/update",response_model=schemas.Msg)
def update_department(
    *,
    obj_in: schemas.SpecialityUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    program_uuid = crud.programs.get_by_uuid(db=db,uuid=obj_in.program_uuid)
    if not program_uuid:
        raise HTTPException(status_code=400, detail=__(key="program-not-found"))
    crud.departments.update(db=db,obj_in=obj_in,added_by=current_user.uuid)
    return {"message": __(key="department-updated-successfully")}

@router.put("/delete",response_model=schemas.Msg)
def delete_department(
    *,
    obj_in: schemas.SpecialityDelete,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.departments.delete(db=db,uuid=obj_in.uuid)
    return {"message": __(key="department-deleted-successfully")}

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
    
    return crud.departments.get_many(
        db, 
        page, 
        per_page, 
    )

@router.get("/get_uuid_and_name_department",response_model=List[schemas.SpecialitySlim])
def get_all_academic_year(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    departments = crud.departments.get_all(db=db)
    return departments
