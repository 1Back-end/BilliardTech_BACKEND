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

        for note_data in obj_in.notes:
            note = db.query(models.StudentExamNote).filter_by(
                student_uuid=note_data.student_uuid,
                course_uuid=obj_in.course_uuid,
                semester_uuid=obj_in.semester_uuid,
                academic_year_uuid=obj_in.academic_year_uuid,
                is_deleted=False
            ).first()

            # Si note existe, on met à jour uniquement les champs fournis
            if note:
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
                    academic_year_uuid=obj_in.academic_year_uuid,
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


        return created_notes
    @staticmethod
    def calcul_note_finale_et_statut(note_cc: float = None, note_sn: float = None, credits: float = 1):
        cc = note_cc if note_cc is not None else 0
        sn = note_sn if note_sn is not None else 0
        total = 0
        coef = 0

        if note_cc is not None:
            total += cc * 0.3 * credits
            coef += 0.3 * credits
        if note_sn is not None:
            total += sn * 0.7 * credits
            coef += 0.7 * credits

        final_note = round(total / coef, 2) if coef > 0 else None

        if final_note is None:
            status = models.StudentExamStatus.EN_ATTENTE
        elif final_note >= 10:
            status = models.StudentExamStatus.VALIDE
        else:
            status = models.StudentExamStatus.RATTRAPAGE

        return final_note, status



examn_notes = CRUDExamnNotes(models.StudentExamNote)