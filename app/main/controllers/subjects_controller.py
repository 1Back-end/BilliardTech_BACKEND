from datetime import timedelta, datetime
from typing import Any, List
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.security import create_access_token
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.post("/create", response_model=schemas.Msg)
def create_subject(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.SubjectCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    exist_code = crud.subjects.get_by_code(db=db, code=obj_in.code)
    if exist_code:
        raise HTTPException(status_code=409, detail=__(key="code-subject-already-exists"))
    
    exist_name = crud.subjects.get_by_name(db=db, name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=409, detail=__(key="name-subjects-already-exists"))
    
    program = crud.programs.get_by_uuid(db=db, uuid=obj_in.program_uuid)
    if not program:
        raise HTTPException(status_code=404, detail=__(key="program-not-found"))
    
    semester = crud.semester.get_by_uuid(db=db, uuid=obj_in.semester_uuid)
    if not semester:
        raise HTTPException(status_code=404, detail=__(key="semester-not-found"))
    
    added_by = current_user.uuid
    crud.subjects.create(db=db, obj_in=obj_in, added_by=added_by)
    return {"message":__(key="subject-created-successfully")}


@router.get("/get_subjects_by_program",response_model=List[schemas.Subject])
def get_subjects_by_program(
    *,
    db: Session = Depends(get_db),
    program_uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    return crud.subjects.get_by_program(db=db, program_uuid=program_uuid)


@router.get("/get_subjects_by_uuid",response_model=schemas.Subject)
def get_subjects_by_uuid(
    *,
    db: Session = Depends(get_db),
    uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    return crud.subjects.get_by_uuid(db=db, uuid=uuid)


@router.put("/update",response_model=schemas.Msg)
def update_subject(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.SubjectUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    program = crud.programs.get_by_uuid(db=db, uuid=obj_in.program_uuid)
    if not program:
        raise HTTPException(status_code=404, detail=__(key="program-not-found"))
    
    semester = crud.semester.get_by_uuid(db=db, uuid=obj_in.semester_uuid)
    if not semester:
        raise HTTPException(status_code=404, detail=__(key="semester-not-found"))
    
    crud.subjects.update(db=db, obj_in=obj_in, added_by=current_user.uuid)
    return {"message":__(key="subject-updated-successfully")}


@router.put("/delete",response_model=schemas.Msg)
def delete_subject(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.SubjectDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.subjects.delete(db=db, uuid=obj_in.uuid)
    return {"message":__(key="subject-deleted-successfully")}