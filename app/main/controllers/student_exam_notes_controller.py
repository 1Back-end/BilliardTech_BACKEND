from datetime import timedelta, datetime
from typing import Any, List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import TeacherTokenRequired, get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.security import create_access_token, get_password_hash
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired
from app.main.core.mail import send_notify_student
router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/exam-notes/bulk", response_model=schemas.Msg)
def add_or_update_exam_notes(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.StudentExamNoteCreateBulk,
    current_user: models.User = Depends(TokenRequired(roles=["PROFESSEUR"]))
):
    semester = crud.semester.get_by_uuid(db=db, uuid=obj_in.semester_uuid)
    if not semester:
        raise HTTPException(status_code=404, detail=__(key="semester-not-found"))

    course = crud.course.get_by_uuid(db=db, uuid=obj_in.course_uuid)
    if not course:
        raise HTTPException(status_code=404, detail=__(key="course-not-found"))

    student_uuids = [note.student_uuid for note in obj_in.notes]
    students = crud.students.get_by_uuids(db=db, uuids=student_uuids)
    if not students or len(students) != len(student_uuids):
        raise HTTPException(status_code=404, detail=__(key="students-not-found"))
    try:
        crud.examn_notes.update_or_insert_notes(
            db=db,
            obj_in=obj_in,
            added_by=current_user.uuid
        )
        return {"message": __(key="notes-success")}
    except HTTPException:
        raise
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


@router.get("/group/{group_uuid}/courses", response_model=list[schemas.CourseSlim3])
def get_courses_by_group(
    group_uuid: str,
    semester_uuid: str = Query(None),  # <-- Ajout du semestre
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["PROFESSEUR"]))
):
    query = db.query(models.Course).filter(
        models.Course.group_uuid == group_uuid,
        models.Course.is_deleted == False
    )

    if semester_uuid:
        query = query.filter(models.Course.semester_uuid == semester_uuid)

    courses = query.all()
    return courses


@router.get("/group/{group_uuid}", response_model=list[schemas.StudentOut])
def get_students_by_group(
    group_uuid: str, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["PROFESSEUR"]))
):
    students = (
        db.query(models.Student)
        .filter(models.Student.group_uuid == group_uuid, models.Student.is_deleted == False)
        .all()
    )
    
    if not students:
        raise HTTPException(status_code=404, detail="Aucun étudiant trouvé pour cette classe")

    return students

@router.get("/get_many", response_model=None)
def get(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 25,
    group_uuid: Optional[str] = None,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN","PROFESSEUR"]))
):
    """
    get administrator with all data by passing filters
    """
    return crud.examn_notes.get_many(
        db=db,
        page=page,
        per_page=per_page,
        group_uuid=group_uuid,
    )

@router.post("/notify-students", response_model=schemas.Msg)
def notify_students(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN", "ADMIN"])),
    background_tasks: BackgroundTasks
):
    students = db.query(models.Student).filter(models.Student.is_deleted==False).all()  # Obtient les étudiants à notifier
    if not students:
        raise HTTPException(status_code=404, detail=__(key="students-not-found"))

    # Envoi des emails en arrière-plan
    for student in students:
        background_tasks.add_task(
            send_notify_student,
            email_to=student.email,
            name=f"{student.first_name} {student.last_name}",
            matricule=student.matricule,  # Assurez-vous que chaque étudiant a un matricule
            subject="Résultats disponibles",
            message="Les résultats sont désormais disponibles. Veuillez consulter les résultats sur votre espace étudiant en entrant votre matricule."
        )

    return {"message": __(key="notification-sent")} 

def calculate_mention(avg: float) -> str:
    if avg >= 16:
        return "Très Bien"
    elif avg >= 14:
        return "Bien"
    elif avg >= 12:
        return "Assez Bien"
    elif avg >= 10:
        return "Passable"
    else:
        return "Ajourné"

@router.get("/student-report", response_model=schemas.StudentReportPaginationResponse)
def get_all_student_reports(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),  # Paramètre de la page, avec un minimum de 1
    per_page: int = Query(10, ge=1, le=100)  # Paramètre pour le nombre d'éléments par page, max 100
):
    # Calcul des limites pour la pagination
    offset = (page - 1) * per_page

    # Récupère tous les étudiants qui ne sont pas supprimés avec la pagination
    students = db.query(models.Student).filter_by(is_deleted=False)\
        .offset(offset).limit(per_page).all()

    # Récupère le nombre total d'étudiants qui ne sont pas supprimés
    total_students = db.query(models.Student).filter_by(is_deleted=False).count()

    if not students:
        raise HTTPException(status_code=404, detail="Aucun étudiant trouvé")

    reports = []

    # Boucle à travers chaque étudiant pour générer son rapport
    for student in students:
        # Récupère les notes de l'étudiant pour chaque matière
        notes = (
            db.query(models.StudentExamNote)
            .join(models.Course)
            .join(models.Semester)  # Jointure avec la table des semestres
            .filter(
                models.StudentExamNote.student_uuid == student.uuid,
                models.StudentExamNote.is_deleted == False
            )
            .offset(offset)
            .limit(per_page)
            .all()
        )

        # Si l'étudiant n'a aucune note, on le passe à l'étudiant suivant
        if not notes:
            continue

        notes_data = []
        total_final_note = 0
        note_count = 0

        # Traitement des notes pour chaque étudiant
        for note in notes:
            final = note.final_note or 0
            notes_data.append(schemas.StudentExamNoteOutSlim1(
                course_data=schemas.CoursesSlim3(
                    uuid=note.course.uuid,
                    title=note.course.title,
                    code=note.course.code
                ),
                course=note.course,
                note_cc=note.note_cc,
                note_sn=note.note_sn,
                final_note=note.final_note,
                semester=schemas.SemesterSlim1(  # Ajout des données du semestre
                    uuid=note.semester.uuid,
                    name=note.semester.name
                )
            ))

            if note.final_note is not None:
                total_final_note += final
                note_count += 1

        # Calcul de la moyenne générale de l'étudiant
        moyenne = total_final_note / note_count if note_count > 0 else 0
        
        # Calcul de la mention en fonction de la moyenne
        mention = calculate_mention(moyenne)

        # Ajout des données au rapport
        reports.append(
            schemas.StudentReportResponse(
                student=schemas.StudentSlim.model_validate(student),
                notes=notes_data,
                moyenne_generale=round(moyenne, 2),
                mention=mention
            )
        )

    # Calcul du nombre total de pages
    total_pages = (total_students + per_page - 1) // per_page

    # Retourne la structure paginée avec les informations supplémentaires
    return {
        "total": total_students,
        "pages": total_pages,
        "per_page": per_page,
        "current_page": page,
        "data": reports
    }
