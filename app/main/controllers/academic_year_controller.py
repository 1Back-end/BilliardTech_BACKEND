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

router = APIRouter(prefix="/academic_year", tags=["academic_year"])

@router.post("/create", response_model=schemas.Msg)
def create_academic_year(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.AcademicYearCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    # Vérifie si une année scolaire avec le même nom existe déjà
    exist_name = crud.academic_year.get_by_name(db=db, name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=400, detail=__(key="academic-year-with-same-name-already-exists"))
    
    # Vérifie si une année scolaire existe déjà avec la même date de début
    exist_start_date = crud.academic_year.get_by_start_date(db=db, start_date=obj_in.start_date)
    if exist_start_date:
        raise HTTPException(status_code=400, detail=__(key="academic-year-with-same-start-date-already-exists"))
    
    # Vérifie si une année scolaire existe déjà avec la même date de fin
    exist_end_date = crud.academic_year.get_by_end_date(db=db, end_date=obj_in.end_date)
    if exist_end_date:
        raise HTTPException(status_code=400, detail=__(key="academic-year-with-same-end-date-already-exists"))
    
    # Vérifie si une année scolaire a des dates qui se chevauchent avec les dates proposées
    overlap = crud.academic_year.get_by_date_range(db=db, start_date=obj_in.start_date, end_date=obj_in.end_date)
    if overlap:
        raise HTTPException(status_code=400, detail=__(key="academic-year-with-overlapping-dates-already-exists"))
    
    # Si toutes les vérifications sont réussies, on peut créer l'année scolaire
    added_by = current_user.uuid
    crud.academic_year.create(db=db, obj_in=obj_in, added_by=added_by)
    
    return schemas.Msg(message=__(key="academic-year-created-successfully"))

@router.put('/update-status-academic-year',response_model=schemas.Msg)
def update_status_academic_year(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.AcademicYearUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.academic_year.update_status(db=db,uuid=obj_in.uuid,status=obj_in.status)
    return schemas.Msg(message=__(key="academic-year-status-updated-successfully"))


@router.put("/delete-academic-year",response_model=schemas.Msg)
def delete_academic_year(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.AcademicYearDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.academic_year.delete(db=db, uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="academic-year-deleted-successfully"))

@router.put("/update",response_model=schemas.Msg)
def update_academic_year(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.AcademicYearUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))  
):
    crud.academic_year.update(db=db,obj_in=obj_in)
    return schemas.Msg(message=__(key="academic-year-updated-successfully"))

@router.get("/get_all",response_model=List[schemas.AcademicYearResponse])
def get_all_academic_year(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    return crud.academic_year.get_all(db=db)

@router.get("/get_uuid_and_name_academic_year",response_model=List[schemas.AcademicYearSlim])
def get_all_academic_year(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    academic_year = crud.academic_year.get_all(db=db)
    return academic_year



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
    
    return crud.academic_year.get_many(
        db, 
        page, 
        per_page, 
    )