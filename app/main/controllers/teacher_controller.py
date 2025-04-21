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

router = APIRouter(prefix="/teachers", tags=["teachers"])

@router.post("/create",response_model=schemas.Msg)
def create_teacher(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TeacherCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    if obj_in.avatar_uuid:
        avatar = crud.storage_crud.get_file_by_uuid(db=db,file_uuid=obj_in.avatar_uuid)
        if not avatar:
            raise HTTPException(status_code=404, detail=__(key="avatar-not-found"))
    
    exist_phone = crud.teacher.get_by_phone_number(db=db, phone_number=obj_in.phone_number)
    if exist_phone:
        raise HTTPException(status_code=409, detail=__(key="phone_number-already-used"))
    
    # exist_phone_2 = crud.teacher.get_by_phone_number_2(db=db,phone_number_2=obj_in.phone_number_2)
    # if exist_phone_2:
    #     raise HTTPException(status_code=409, detail=__(key="phone_number-already-used"))

    exist_email = crud.teacher.get_by_email(db=db, email=obj_in.email)
    if exist_email:
        raise HTTPException(status_code=409, detail=__(key="email-already-used"))
    
    crud.teacher.create(
        db, obj_in=obj_in,added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="teacher-created-successfully"))



@router.get("/get_many", response_model=None)
def get(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 25,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    """
    get administrator with all data by passing filters
    """
    
    return crud.teacher.get_many(
        db, 
        page, 
        per_page, 
    )
@router.get("/get_by_uuid",response_model=schemas.Teacher)
def get_teacher_by_uuid(
    *,
    db: Session = Depends(get_db),
    uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.teacher.get_by_uuid(db=db,uuid=uuid)

@router.put("/delete-teacher",response_model=schemas.Msg)
def delete_teacher(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TeacherDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.user.delete(db=db, uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="teacher-deleted-successfully"))

@router.put("/update-status",response_model=schemas.Msg)
def update_teacher_status(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TeacherUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.teacher.update_status(
        db,
        uuid=obj_in.uuid,
        status=obj_in.status
    )
    return schemas.Msg(message=__(key="teacher-status-updated-successfully"))

@router.put("/update-teacher",response_model=schemas.Msg)
def update(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TeacherUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    if obj_in.avatar_uuid:
        avatar = crud.storage_crud.get_file_by_uuid(db=db,file_uuid=obj_in.avatar_uuid)
        if not avatar:
            raise HTTPException(status_code=404, detail=__(key="avatar-not-found"))
    crud.teacher.update(
        db, obj_in=obj_in,added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="teacher-updated-successfully"))


@router.get("/get_all_teachers", response_model=List[schemas.TeacherSlim])
def get_user_teachers(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
   teachers = crud.teacher.get_all_teachers(db=db)
   return teachers

@router.get("/teachers-with-courses", response_model=schemas.PaginatedTeachersResponse)
def get_teachers_with_courses(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1)
):
    offset = (page - 1) * per_page

    # Total teachers with assignments
    total_teachers = db.query(models.Teacher)\
        .filter(models.Teacher.is_deleted == False)\
        .count()

    teachers = db.query(models.Teacher)\
        .filter(models.Teacher.is_deleted == False)\
        .offset(offset)\
        .limit(per_page)\
        .all()

    teachers_with_courses = []

    for teacher in teachers:
        assignments = db.query(models.TeacherCourseAssignment).join(models.Course).filter(
            models.TeacherCourseAssignment.teacher_uuid == teacher.uuid,
            models.TeacherCourseAssignment.is_deleted == False
        ).all()

        if not assignments:
            continue

        courses_with_added_by = []
        for assignment in assignments:
            course = db.query(models.Course).filter(models.Course.uuid == assignment.course_uuid).first()
            user_added_by = db.query(models.User).filter(models.User.uuid == assignment.added_by).first()

            courses_with_added_by.append(schemas.CoursesSlim2(
                title=course.title,
                code=course.code,
                user=schemas.AddedBySlim(
                    first_name=user_added_by.first_name if user_added_by else "Inconnu",
                    last_name=user_added_by.last_name if user_added_by else "Inconnu",
                    role=user_added_by.role if user_added_by else "Inconnu"
                ),
                created_at=assignment.created_at,
                updated_at=assignment.updated_at
            ))

        teacher_data = schemas.TeacherResponse(
            name=f"{teacher.first_name} {teacher.last_name}",
            created_at=teacher.created_at,
            courses=courses_with_added_by
        )
        teachers_with_courses.append(teacher_data)

    total_pages = (total_teachers + per_page - 1) // per_page  # Calcul du nombre total de pages

    return schemas.PaginatedTeachersResponse(
        total=total_teachers,
        pages=total_pages,
        per_page=per_page,
        current_page=page,
        data=teachers_with_courses
    )
