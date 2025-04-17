from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.security import create_access_token, get_password_hash
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired
from typing import List

router = APIRouter(prefix="/programs", tags=["programs"])

@router.post("/create",response_model=schemas.Msg)
def create_programs(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.ProgramsCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    exist_programs = crud.programs.get_by_name(db=db,name=obj_in.name)
    if exist_programs:
        raise HTTPException(status_code=400, detail=__(key="program-already-exists"))
    academic_year_uuid = crud.academic_year.get_by_uuid(db=db,uuid=obj_in.academic_year_uuid)
    if not academic_year_uuid:
        raise HTTPException(status_code=400, detail=__(key="academic_year-not-found"))
    crud.programs.create(db=db,obj_in=obj_in,added_by=current_user.uuid)
    return {"message": __(key="program-created-successfully")}


@router.put("/update",response_model=schemas.Msg)
def update_programs(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.ProgramsUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.programs.update(db=db,obj_in=obj_in,added_by=current_user.uuid)
    return {"message": __(key="program-updated-successfully")}
    
@router.put("/delete",response_model=schemas.Msg)
def delete_programs(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.ProgramsDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.programs.delete(db=db,uuid=obj_in.uuid)
    return {"message": __(key="program-deleted-successfully")}


@router.get("/get_all",response_model=List[schemas.ProgramsSlim2])
def get_all_programs(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    return crud.programs.get_all(db=db)

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
    
    return crud.programs.get_many(
        db, 
        page, 
        per_page, 
    )