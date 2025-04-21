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
from app.main import models,schemas


class CRUDTeacherCourseAssignment(CRUDBase[models.TeacherCourseAssignment,schemas.TeacherCourseAssignment,schemas.TeacherCourseAssignmentCreate]):

    @classmethod
    def create(cls, db: Session, *, obj_in: schemas.TeacherCourseAssignmentCreate, added_by: str):
        assignments = []
        already_assigned_courses = []

        for course_uuid in obj_in.course_uuids:
            existing = db.query(
                models.TeacherCourseAssignment,
                models.Course.title,
                models.Teacher.first_name,
                models.Teacher.last_name
            ).join(
                models.Course, models.TeacherCourseAssignment.course_uuid == models.Course.uuid
            ).join(
                models.Teacher, models.TeacherCourseAssignment.teacher_uuid == models.Teacher.uuid
            ).filter(
                models.TeacherCourseAssignment.course_uuid == course_uuid,
                models.TeacherCourseAssignment.is_deleted == False
            ).first()

            if existing:
                course_title = existing[1]
                teacher_name = f"{existing[2]} {existing[3]}"
                already_assigned_courses.append(f"{course_title} (enseigné par {teacher_name})")
            else:
                assignment = models.TeacherCourseAssignment(
                    uuid=str(uuid.uuid4()),
                    teacher_uuid=obj_in.teacher_uuid,
                    course_uuid=course_uuid,
                    added_by=added_by
                )
                db.add(assignment)
                assignments.append(assignment)

        if already_assigned_courses:
            if len(already_assigned_courses) == 1:
                error_message = f"Le cours {already_assigned_courses[0]} est déjà assigné."
            else:
                error_message = f"Les cours suivants sont déjà assignés : {', '.join(already_assigned_courses)}"
            raise HTTPException(status_code=400, detail=error_message)

        db.commit()

        success_message = "Cours assigné avec succès." if len(assignments) == 1 else "Tous les cours ont été assignés avec succès."

        return {"message": success_message}



    
    @classmethod
    def update(cls, db: Session, *, assignment_uuid: str, obj_in: schemas.TeacherCourseAssignmentUpdate, added_by: str):
        assignment = db.query(models.TeacherCourseAssignment).filter(
            models.TeacherCourseAssignment.uuid == assignment_uuid,
            models.TeacherCourseAssignment.is_deleted == False
        ).first()

        if not assignment:
            raise HTTPException(status_code=404, detail="Affectation non trouvée.")

        modifications = 0

        # Vérifier si on essaie d'assigner un cours déjà pris par un autre enseignant
        if assignment.course_uuid != obj_in.course_uuid:
            existing = db.query(
                models.TeacherCourseAssignment,
                models.Course.title,
                models.Teacher.first_name,
                models.Teacher.last_name
            ).join(
                models.Course, models.TeacherCourseAssignment.course_uuid == models.Course.uuid
            ).join(
                models.Teacher, models.TeacherCourseAssignment.teacher_uuid == models.Teacher.uuid
            ).filter(
                models.TeacherCourseAssignment.course_uuid == obj_in.course_uuid,
                models.TeacherCourseAssignment.uuid != assignment_uuid,
                models.TeacherCourseAssignment.is_deleted == False
            ).first()

            if existing:
                course_title = existing[1]
                teacher_name = f"{existing[2]} {existing[3]}"
                raise HTTPException(
                    status_code=400,
                    detail=f"Le cours {course_title} est déjà assigné à {teacher_name}."
                )
            assignment.course_uuid = obj_in.course_uuid
            modifications += 1

        if assignment.teacher_uuid != obj_in.teacher_uuid:
            assignment.teacher_uuid = obj_in.teacher_uuid
            modifications += 1

        if modifications == 0:
            return {"message": "Aucun changement détecté."}

        assignment.added_by = added_by
        db.commit()

        message = "Cours modifié avec succès." if modifications == 1 else "Cours modifiés avec succès."
        return {"message": message}

    
    @classmethod
    def delete(cls, db: Session, *, teacher_uuid: str, course_uuid: str):
        # Récupérer l'assignation à supprimer
        assignment = db.query(models.TeacherCourseAssignment).filter(
            models.TeacherCourseAssignment.teacher_uuid == teacher_uuid,
            models.TeacherCourseAssignment.course_uuid == course_uuid,
            models.TeacherCourseAssignment.is_deleted == False
        ).first()

        if not assignment:
            raise HTTPException(status_code=404,detail=__(key="assignment-not-found"))

        # Effectuer un soft delete (mise à jour de `is_deleted` à True)
        assignment.is_deleted = True
        db.commit()

        return assignment
    
    @classmethod
    def get_by_teacher(cls, db: Session, teacher_uuid: str):
        # Récupérer toutes les assignations non supprimées d'un professeur
        return db.query(models.TeacherCourseAssignment).filter(
            models.TeacherCourseAssignment.teacher_uuid == teacher_uuid,
            models.TeacherCourseAssignment.is_deleted == False
        ).all()

    @classmethod
    def get_by_uuid(cls, db: Session, assignment_uuid: str):
        return db.query(models.TeacherCourseAssignment).filter(
            models.TeacherCourseAssignment.uuid == assignment_uuid
        ).first()


assignments = CRUDTeacherCourseAssignment(models.TeacherCourseAssignment)
        
        