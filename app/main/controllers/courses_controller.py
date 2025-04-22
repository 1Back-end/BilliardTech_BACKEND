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

router = APIRouter(prefix="/courses", tags=["courses"])

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
    
    return crud.course.get_many(
        db, 
        page, 
        per_page, 
    )

@router.get("/get_by_uuid",response_model=schemas.Course)
def get_student_by_uuid(
    *,
    db: Session = Depends(get_db),
    uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.course.get_by_uuid(db=db,uuid=uuid)


@router.post("/create",response_model=schemas.Msg)
def create_courses(
     *,
    db: Session = Depends(get_db),
    obj_in: schemas.CourseCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    exist_name = crud.course.get_by_title(db=db,title=obj_in.title)
    if exist_name:
        raise HTTPException(status_code=400, detail=__(key="course-already-exists"))
    exist_code = crud.course.get_by_code(db=db,code=obj_in.code)
    if exist_code:
        raise HTTPException(status_code=400, detail=__(key="course-already-exists"))
    group= crud.group.get_by_uuid(db=db, uuid=obj_in.group_uuid)
    if not group:
        raise HTTPException(status_code=404, detail=__(key="class-not-found"))
    
    academic_year_uuid = crud.academic_year.get_by_uuid(db=db,uuid=obj_in.academic_year_uuid)
    if not academic_year_uuid:
        raise HTTPException(status_code=400, detail=__(key="academic-year-not-found"))
    
    speciality_uuid = crud.departments.get_by_uuid(db=db,uuid=obj_in.speciality_uuid)
    if not speciality_uuid:
        raise HTTPException(status_code=400, detail=__(key="department-not-found"))
    
    semester = crud.semester.get_by_uuid(db=db, uuid=obj_in.semester_uuid)
    if not semester:
        raise HTTPException(status_code=404, detail=__(key="semester-not-found"))
    
    crud.course.create(db=db,obj_in=obj_in,added_by=current_user.uuid)
    return {"message": __(key="course-created-successfully")}

@router.put("/update",response_model=schemas.Msg)
def update_courses(
     *,
    db: Session = Depends(get_db),
    obj_in: schemas.CourseUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    group= crud.group.get_by_uuid(db=db, uuid=obj_in.group_uuid)
    if not group:
        raise HTTPException(status_code=404, detail=__(key="class-not-found"))
    
    academic_year_uuid = crud.academic_year.get_by_uuid(db=db,uuid=obj_in.academic_year_uuid)
    if not academic_year_uuid:
        raise HTTPException(status_code=400, detail=__(key="academic-year-not-found"))

    
    speciality_uuid = crud.departments.get_by_uuid(db=db,uuid=obj_in.speciality_uuid)
    if not speciality_uuid:
        raise HTTPException(status_code=400, detail=__(key="department-not-found"))
    
    semester = crud.semester.get_by_uuid(db=db, uuid=obj_in.semester_uuid)
    if not semester:
        raise HTTPException(status_code=404, detail=__(key="semester-not-found"))
    
    crud.course.update(db=db,obj_in=obj_in,added_by=current_user.uuid)
    return {"message": __(key="course-updated-successfully")}

@router.put("/delete",response_model=schemas.Msg)
def delete_student(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.CourseDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.course.delete(db=db, uuid=obj_in.uuid)
    return {"message": __(key="course-deleted-successfully")}

@router.get("/get_all_courses", response_model=List[schemas.CoursesSlim1])
def get_courses(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
   courses = crud.course.get_all_courses(db=db)
   return courses

