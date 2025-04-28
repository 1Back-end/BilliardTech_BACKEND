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

router = APIRouter(prefix="/type_courses", tags=["type_courses"])

@router.post("/create",response_model=schemas.Msg)
def create_type_courses(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.TypeCoursesCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    exist_name = crud.type_courses.get_by_name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=409,detail=__(key="name-is-already-exist"))
    crud.type_courses.create(db=db,obj_in=obj_in,added_by=current_user.uuid)
    return {"message":__(key="type-courses-created-successfully")}

@router.put("/update",response_model=schemas.Msg)
def update_type_courses(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.TypeCoursesUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    crud.type_courses.update(db=db,obj_in=obj_in,added_by=current_user.uuid)
    return {"message":__(key="type-courses-updated-successfully")}
    
@router.put("/delete",response_model=schemas.Msg)
def delete_type_courses(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.TypeCoursesDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    crud.type_courses.delete(db=db,obj_in=obj_in)
    return {"message":__(key="type-courses-deleted-successfully")}
    
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
    
    return crud.type_courses.get_many(
        db, 
        page, 
        per_page, 
    )