from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime,Date,Boolean
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum


class CourseType(str,Enum):
    """Course type enum"""
    CM = "CM"
    TP = "TP"
    TD = "TD"

class Course(Base):
    __tablename__ = "courses"

    uuid = Column(String, primary_key=True, index=True)  # Identifiant unique du cours
    title = Column(String, nullable=False)  # Titre du cours
    code = Column(String, nullable=False)  # Code unique du cours
    credits = Column(Integer, default=0)  # Nombre de crédits du cours
    type = Column(String,default=CourseType.CM,nullable=False)  # Type de cours (CM, TD, TP, etc.)

    speciality_uuid = Column(String, ForeignKey("specialities.uuid"), nullable=True)  # Relier à la filière
    speciality = relationship("Speciality", foreign_keys=[speciality_uuid])

    
    group_uuid = Column(String, ForeignKey("groups.uuid",ondelete="CASCADE",onupdate="CASCADE"), nullable=True)
    group = relationship("Group", foreign_keys=[group_uuid])

    added_by = Column(String, ForeignKey('users.uuid',ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    user = relationship("User", foreign_keys=[added_by])

    academic_year_uuid = Column(String, ForeignKey("academic_years.uuid",ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    academic_year = relationship("AcademicYear", foreign_keys=[academic_year_uuid])

    semester_uuid = Column(String, ForeignKey("semesters.uuid",ondelete="CASCADE",onupdate="CASCADE"), nullable=True)
    semester = relationship("Semester", foreign_keys=[semester_uuid])




    created_at = Column(DateTime, default=func.now())  # Date de création du cours
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Date de dernière mise à jour
    is_deleted = Column(Boolean, default=False)  # Si le cours est supprimé ou non

    # assignments = relationship("TeacherCourseAssignment", back_populates="course")  # Assignations des cours
