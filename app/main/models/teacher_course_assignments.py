from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime,Date,Boolean
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum


class TeacherCourseAssignment(Base):
    __tablename__ = "teacher_course_assignments"

    uuid = Column(String, primary_key=True, index=True)  # Identifiant unique de l'assignation
    teacher_uuid = Column(String, ForeignKey("teachers.uuid", ondelete="CASCADE", onupdate="CASCADE"))  # UUID du professeur
    course_uuid = Column(String, ForeignKey("courses.uuid", ondelete="CASCADE", onupdate="CASCADE"))  # ID du cours

    teacher = relationship("Teacher", foreign_keys=[teacher_uuid])  # Relation vers le professeur
    courses = relationship("Course", foreign_keys=[course_uuid])  # Relation vers le cours

    added_by = Column(String, ForeignKey('users.uuid',ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    user = relationship("User", foreign_keys=[added_by])

    is_deleted = Column(Boolean, default=False)


    created_at = Column(DateTime, default=func.now())  # Date d'assignation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Date de dernière mise à jour
