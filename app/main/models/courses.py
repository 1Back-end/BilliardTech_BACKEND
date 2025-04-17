from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime,Date,Boolean
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum


class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    credits = Column(Integer, default=0)
    type = Column(String)  # CM, TP, TD

    semester_uuid = Column(String, ForeignKey("semesters.uuid",ondelete="CASCADE",onupdate="CASCADE"))
    group_uuid = Column(String, ForeignKey("groups.uuid",ondelete="CASCADE",onupdate="CASCADE"))
    teacher_uuid = Column(String, ForeignKey("teachers.uuid",ondelete="CASCADE",onupdate="CASCADE"))

    semester = relationship("Semester", foreign_keys=[semester_uuid])
    group = relationship("Group", foreign_keys=[group_uuid])
    teacher = relationship("Teacher", foreign_keys=[teacher_uuid])

    added_by = Column(String, ForeignKey('users.uuid',ondelete="CASCADE",onupdate="CASCADE"), nullable=False)  # Candidat postulant
    user = relationship("User", foreign_keys=[added_by])
    created_at = Column(DateTime, default=func.now())  # Account creation timestamp
    is_deleted = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Last update timestamp
