
from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime,Date,Boolean
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Student(Base):
    __tablename__ = "students"

    uuid = Column(String, primary_key=True, index=True)
    matricule = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    gender = Column(String, nullable=False,default=GenderEnum.MALE)
    nationality = Column(String, nullable=False)

    added_by = Column(String, ForeignKey('users.uuid',ondelete="CASCADE",onupdate="CASCADE"), nullable=False)  
    user = relationship("User", foreign_keys=[added_by])

    program_uuid = Column(String, ForeignKey("programs.uuid",ondelete="CASCADE",onupdate="CASCADE"), nullable=True)
    program = relationship("Program", foreign_keys=[program_uuid])
    

    speciality_uuid = Column(String, ForeignKey("specialities.uuid"), nullable=True)  # Relier à la filière
    speciality = relationship("Speciality", foreign_keys=[speciality_uuid])

    
    group_uuid = Column(String, ForeignKey("groups.uuid",ondelete="CASCADE",onupdate="CASCADE"), nullable=True)
    group = relationship("Group", foreign_keys=[group_uuid])

    storage_uuid: str = Column(String, ForeignKey('storages.uuid',ondelete="CASCADE",onupdate="CASCADE"), nullable=True)
    avatar = relationship("Storage", foreign_keys=[storage_uuid])

    academic_year_uuid = Column(String, ForeignKey("academic_years.uuid",ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    academic_year = relationship("AcademicYear", foreign_keys=[academic_year_uuid])
    
    is_deleted = Column(Boolean, default=False)


    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
