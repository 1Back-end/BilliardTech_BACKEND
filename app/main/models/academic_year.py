from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime,Date,Boolean
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum


class AcademicYearStatus(str,Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


class AcademicYear(Base):
    __tablename__ = "academic_years"

    uuid = Column(String, primary_key=True,index=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String, default=AcademicYearStatus.ACTIVE)
    added_by = Column(String, ForeignKey('users.uuid',ondelete="CASCADE",onupdate="CASCADE"), nullable=False)  # Candidat postulant
    user = relationship("User", foreign_keys=[added_by])
    created_at = Column(DateTime, default=func.now())  # Account creation timestamp
    is_deleted = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Last update timestamp


    def __repr__(self):
        return f'<AcademicYear(uuid="{self.uuid}", name="{self.name}")>'

