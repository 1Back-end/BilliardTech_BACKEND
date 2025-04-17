
from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime,Date,Boolean
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum

class Group(Base):
    __tablename__ = "groups"

    uuid = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(String, nullable=False)

    added_by = Column(String, ForeignKey('users.uuid'), nullable=False)  # Candidat postulant
    user = relationship("User", foreign_keys=[added_by])

    academic_year_uuid = Column(String, ForeignKey("academic_years.uuid",ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    academic_year = relationship("AcademicYear", foreign_keys=[academic_year_uuid])

    speciality_uuid = Column(String, ForeignKey("specialities.uuid"), nullable=False)  # Relier à la filière
    speciality = relationship("Speciality", foreign_keys=[speciality_uuid])

    is_deleted = Column(Boolean,default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
