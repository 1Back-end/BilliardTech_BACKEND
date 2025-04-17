from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime,Date,Boolean,Float
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum


class Grade(Base):
    __tablename__ = "grades"

    id = Column(String, primary_key=True)
    student_uuid = Column(String, ForeignKey("students.uuid"))
    course_uuid = Column(String, ForeignKey("courses.uuid"))
    type_of_exam_uuid = Column(String, ForeignKey("type_of_exams.uuid"))
    value = Column(Float, nullable=False)

    student = relationship("Student", backref="grades")
    course = relationship("Course", backref="grades")
    type_of_exam = relationship("TypeOfExam", backref="grades")
    is_deleted = Column(Boolean, default=False)


    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
