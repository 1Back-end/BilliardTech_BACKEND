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

router = APIRouter(prefix="/type_examns", tags=["type_examns"])

@router.post("/create",response_model=schemas.Msg)
def create_type_examns(
     *,
    db: Session = Depends(get_db),
    obj_in: schemas.TypeOfExamnCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    exist_name = crud.type_of_examen.get_by_name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=409,detail=__(key="type-examen-name-already-exist"))
    
    exist_code = crud.type_of_examen.get_by_code(db=db,code=obj_in.code)
    if exist_code:
        raise HTTPException(status_code=409,detail=__(key="type-examen-code-already-exist"))
    crud.type_of_examen.create(db=db,obj_in=obj_in,added_by=current_user.uuid)
    return {"message": __(key="type-examen-created-successfully")}

@router.put("/update",response_model=schemas.Msg)
def update_type_examns(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.TypeOfExamnUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))  
):
    crud.type_of_examen.update(db=db,obj_in=obj_in,updated_by=current_user.uuid)
    return schemas.Msg(message=__(key="type-examen-updated-successfully"))
    
@router.get("/get_many", response_model=None)
def get_all_type_examns(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 5,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    """
    get administrator with all data by passing filters
    """
    
    return crud.type_of_examen.get_many(
        db, 
        page, 
        per_page, 
    )

@router.put("/delete",response_model=schemas.Msg)
def delete_type_examns(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TypeOfExamnDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.type_of_examen.delete(db=db, uuid=obj_in.uuid)
    return {"message": __(key="type-examen-deleted-successfully")}
