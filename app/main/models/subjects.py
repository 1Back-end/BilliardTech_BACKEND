from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime,Date,Boolean
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum

class Subject(Base):
    __tablename__ = "subjects"
    
    uuid = Column(String, primary_key=True,index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    credits = Column(Integer, nullable=False)
    program_uuid = Column(String, ForeignKey("programs.uuid",ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    semester_uuid = Column(String, ForeignKey("semesters.uuid",ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    is_deleted = Column(Boolean, default=False)
    added_by = Column(String, ForeignKey('users.uuid',ondelete="CASCADE",onupdate="CASCADE"), nullable=False)  # Candidat postulant
    user = relationship("User", foreign_keys=[added_by])

    program = relationship("Program", foreign_keys=[program_uuid])
    semester = relationship("Semester", foreign_keys=[semester_uuid])

 