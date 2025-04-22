from datetime import timedelta, datetime
from typing import Any, List
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import TeacherTokenRequired, get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.security import create_access_token, get_password_hash
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/exam-notes/bulk", response_model=List[schemas.StudentExamNoteOut])
def add_or_update_exam_notes(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.StudentExamNoteCreateBulk,
    current_user: models.Teacher = Depends(TeacherTokenRequired())
):
    # Vérifier l'année académique
    academic_year = crud.academic_year.get_by_uuid(db=db, uuid=obj_in.academic_year_uuid)
    if not academic_year:
        raise HTTPException(status_code=400, detail=__(key="academic-year-not-found"))

    # Vérifier le semestre
    semester = crud.semester.get_by_uuid(db=db, uuid=obj_in.semester_uuid)
    if not semester:
        raise HTTPException(status_code=404, detail=__(key="semester-not-found"))

    # Vérifier le cours
    course = crud.course.get_by_uuid(db=db, uuid=obj_in.course_uuid)
    if not course:
        raise HTTPException(status_code=404, detail=__(key="course-not-found"))

    # Vérifier que le cours appartient bien au semestre et à l'année académique
    if course.academic_year_uuid != obj_in.academic_year_uuid:
        raise HTTPException(status_code=400, detail="Ce cours n'appartient pas à l'année académique fournie.")
    if course.semester_uuid != obj_in.semester_uuid:
        raise HTTPException(status_code=400, detail="Ce cours n'est pas lié au semestre fourni.")

    # Vérifier l'assignation du professeur au cours
    teacher_course_assignment = db.query(models.TeacherCourseAssignment).filter(
        models.TeacherCourseAssignment.teacher_uuid == current_user.uuid,
        models.TeacherCourseAssignment.course_uuid == obj_in.course_uuid,
        models.TeacherCourseAssignment.is_deleted == False
    ).first()
    if not teacher_course_assignment:
        raise HTTPException(status_code=403, detail=__(key="course-not-assigned-to-teacher"))

    # Vérifier les étudiants
    student_uuids = [note.student_uuid for note in obj_in.notes]
    students = crud.students.get_by_uuids(db=db, uuids=student_uuids)
    if not students or len(students) != len(student_uuids):
        raise HTTPException(status_code=404, detail=__(key="students-not-found"))

    # Vérifier que tous les étudiants appartiennent à la même classe que celle du cours
    mismatched_students = [
        student for student in students
        if student.group_uuid != course.group_uuid
    ]
    if mismatched_students:
        raise HTTPException(
            status_code=400,
            detail="Un ou plusieurs étudiants n'appartiennent pas à la classe du cours."
        )
    # Enregistrement des notes
    try:
        notes = crud.examn_notes.update_or_insert_notes(
            db=db,
            obj_in=obj_in,
            added_by=current_user.uuid
        )
        return notes
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Une erreur est survenue lors de l'enregistrement des notes: {str(e)}"
        )

@router.get("/students/{matricule}/exam-results", response_model=List[schemas.StudentExamNoteData])
def get_student_results_by_matricule(matricule: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.matricule == matricule,
        models.Student.is_deleted == False
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")

    exam_notes = db.query(models.StudentExamNote).filter(
        models.StudentExamNote.student_uuid == student.uuid,
        models.StudentExamNote.is_deleted == False
    ).all()

    return exam_notes

