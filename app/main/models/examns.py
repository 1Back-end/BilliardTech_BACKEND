from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime,Date,Boolean
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum


class Examn(Base):

    __tablename__ = "examns"
    uuid = Column(String, primary_key=True, index=True)  # Identifiant unique du cours

    added_by = Column(String, ForeignKey('teachers.uuid',ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    teacher = relationship("Teacher", foreign_keys=[added_by])

    type_examns_uuid = Column(String,ForeignKey('type_of_examns.uuid',ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    type_examns = relationship("TypeOfExam",foreign_keys=[type_examns_uuid])

    semester_uuid = Column(String, ForeignKey("semesters.uuid",ondelete="CASCADE",onupdate="CASCADE"), nullable=True)
    semester = relationship("Semester", foreign_keys=[semester_uuid])

    group_uuid = Column(String, ForeignKey("groups.uuid",ondelete="CASCADE",onupdate="CASCADE"), nullable=True)
    group = relationship("Group", foreign_keys=[group_uuid])

    academic_year_uuid = Column(String, ForeignKey("academic_years.uuid",ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    academic_year = relationship("AcademicYear", foreign_keys=[academic_year_uuid])

    created_at = Column(DateTime, default=func.now())  # Date de création du cours
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Date de dernière mise à jour
    is_deleted = Column(Boolean, default=False)  # Si le cours est supprimé ou non

    