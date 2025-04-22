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

router = APIRouter(prefix="/course-assignments", tags=["course-assignments"])

@router.post("/assign-to-teacher", response_model=schemas.Msg)
def create_course_assignment(
    *,
    obj_in: schemas.TeacherCourseAssignmentCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN", "ADMIN"]))
):
    teacher = crud.teacher.get_by_uuid(db=db, uuid=obj_in.teacher_uuid)
    if not teacher:
        raise HTTPException(status_code=404, detail=__(key="teacher-not-found"))
    
    courses = crud.course.get_by_uuids(db=db, uuids=obj_in.course_uuids)
    if not courses or len(courses) != len(obj_in.course_uuids):
        raise HTTPException(status_code=404, detail=__(key="course-not-found"))
    
    result = crud.assignments.create(db=db, obj_in=obj_in, added_by=current_user.uuid)

    return {"message": result["message"]}


@router.put("/update-teacher-courses", response_model=schemas.Msg)
def update_teacher_courses(
    *,
    obj_in: schemas.TeacherCourseAssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN", "ADMIN"]))
):
        teacher = crud.teacher.get_by_uuid(db=db,uuid=obj_in.teacher_uuid)
        if not teacher:
             raise HTTPException(status_code=404, detail=__(key="teacher-not-found"))
        # Modification ici pour gérer un tableau de UUIDs
        courses = crud.course.get_by_uuids(db=db, uuids=obj_in.course_uuids)
        if not courses or len(courses) != len(obj_in.course_uuids):
            raise HTTPException(status_code=404, detail=__(key="course-not-found"))
        result= crud.assignments.update(db=db, obj_in=obj_in, added_by=current_user.uuid)
        return {"message": result["message"]}
   
# Récupérer les assignations d'un professeur
@router.get("/get-by-teacher", response_model=List[schemas.TeacherCourseAssignment])
def get_teacher_assignments(
    teacher_uuid: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN", "ADMIN"]))
):
    assignments = crud.assignments.get_by_teacher(db=db, teacher_uuid=teacher_uuid)
    print(assignments)
    if not assignments:
        raise HTTPException(status_code=404, detail=__("assignments-not-found"))
    return assignments

# Récupérer une assignation par son UUID
@router.get("/get-by-uuid", response_model=schemas.TeacherCourseAssignment)
def get_assignment_by_uuid(
    assignment_uuid: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN", "ADMIN"]))
):
    assignment = crud.assignments.get_by_uuid(db=db, assignment_uuid=assignment_uuid)
    if not assignment:
        raise HTTPException(status_code=404, detail=__("assignment-not-found"))
    return assignment