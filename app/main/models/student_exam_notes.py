from sqlalchemy import (
    Column, String, ForeignKey, DateTime, Boolean, Float, Enum as SqlEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from app.main.models.db.base_class import Base

class StudentExamStatus(str, Enum):
    VALIDE = "Validé"
    RATTRAPAGE = "Rattrapage"
    EN_ATTENTE = "En attente"

class StudentExamNote(Base):
    __tablename__ = "student_exam_notes"

    uuid = Column(String, primary_key=True, index=True)

    student_uuid = Column(String, ForeignKey("students.uuid", ondelete="CASCADE"), nullable=False)
    student = relationship("Student", backref="exam_notes")

    added_by = Column(String, ForeignKey('users.uuid',ondelete="CASCADE",onupdate="CASCADE"), nullable=True)  
    user = relationship("User", foreign_keys=[added_by])


    course_uuid = Column(String, ForeignKey("courses.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    course = relationship("Course", foreign_keys=[course_uuid])

    semester_uuid = Column(String, ForeignKey("semesters.uuid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    semester = relationship("Semester", foreign_keys=[semester_uuid])

    
    note_cc = Column(Float, nullable=True)
    note_sn = Column(Float, nullable=True)
    final_note = Column(Float, nullable=True)

    status = Column(SqlEnum(StudentExamStatus), default=StudentExamStatus.EN_ATTENTE)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
