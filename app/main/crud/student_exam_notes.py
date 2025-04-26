from datetime import date, datetime
import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models,schemas,crud



class CRUDExamnNotes(CRUDBase[schemas.StudentNoteInput,schemas.StudentExamNoteCreateBulk,models.StudentExamNote]):

    @classmethod
    def update_or_insert_notes(cls, db: Session, obj_in: schemas.StudentExamNoteCreateBulk, added_by: str):
        course = crud.course.get_by_uuid(db=db, uuid=obj_in.course_uuid)
        if not course:
            raise HTTPException(status_code=404, detail=__(key="course-not-found"))

        credits = course.credits or 1
        updated_or_created = []

        student_uuids = [note.student_uuid for note in obj_in.notes]
        student_map = {s.uuid: s for s in crud.students.get_by_uuids(db=db, uuids=student_uuids)}

        for note_data in obj_in.notes:
            note = db.query(models.StudentExamNote).filter_by(
                student_uuid=note_data.student_uuid,
                course_uuid=obj_in.course_uuid,
                semester_uuid=obj_in.semester_uuid,
                is_deleted=False
            ).first()

            student = student_map.get(note_data.student_uuid)

            if note:
                if note_data.note_cc is not None and note.note_cc is not None:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Les notes de CC existent déjà pour {student.first_name} {student.last_name}"
                    )

                if note_data.note_sn is not None and note.note_sn is not None:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Les notes de SN existent déjà pour {student.first_name} {student.last_name}"
                    )

                if note_data.note_cc is not None:
                    note.note_cc = note_data.note_cc
                if note_data.note_sn is not None:
                    note.note_sn = note_data.note_sn

                final_note, status = cls.calcul_note_finale_et_statut(
                    note_cc=note.note_cc,
                    note_sn=note.note_sn,
                    credits=credits
                )
                note.final_note = final_note
                note.status = status
            else:
                final_note, status = cls.calcul_note_finale_et_statut(
                    note_cc=note_data.note_cc,
                    note_sn=note_data.note_sn,
                    credits=credits
                )

                note = models.StudentExamNote(
                    uuid=str(uuid.uuid4()),
                    student_uuid=note_data.student_uuid,
                    added_by=added_by,
                    course_uuid=obj_in.course_uuid,
                    semester_uuid=obj_in.semester_uuid,
                    note_cc=note_data.note_cc,
                    note_sn=note_data.note_sn,
                    final_note=final_note,
                    status=status
                )
                db.add(note)

            updated_or_created.append(note)

        db.commit()
        for note in updated_or_created:
            db.refresh(note)

        return updated_or_created



    @staticmethod
    def calcul_note_finale_et_statut(note_cc: float = None, note_sn: float = None, credits: float = 1):
        # Si l'une des deux notes est manquante, retourner "En attente"
        if note_cc is None or note_sn is None:
            return None, models.StudentExamStatus.EN_ATTENTE

        # Calcul de la note finale lorsque les deux notes sont présentes
        total = (note_cc * 0.3 + note_sn * 0.7) * credits
        final_note = round(total / credits, 2)

        # Déterminer le statut en fonction de la note finale
        if final_note >= 10:
            status = models.StudentExamStatus.VALIDE
        else:
            status = models.StudentExamStatus.RATTRAPAGE

        return final_note, status
    
    @classmethod
    def get_many(
        cls,
        db: Session,
        page: int = 1,
        per_page: int = 25,
        group_uuid: Optional[str] = None,
    ):
        # Jointure avec Student pour filtrer par group_uuid
        record_query = db.query(models.StudentExamNote).join(models.Student).filter(
            models.StudentExamNote.is_deleted == False
        )

        if group_uuid:
            record_query = record_query.filter(models.Student.group_uuid == group_uuid)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.PaginatedStudentExamNResponse(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )
    




examn_notes = CRUDExamnNotes(models.StudentExamNote)