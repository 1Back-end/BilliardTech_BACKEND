from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime,Date,Boolean
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum


class TypeCourse(Base):
    __tablename__ = "type_courses"

    uuid = Column(String,primary_key=True,index=True)
    name = Column(String,nullable=False)
    is_deleted = Column(Boolean,default=False)
    added_by = Column(String, ForeignKey('users.uuid',ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    user = relationship("User", foreign_keys=[added_by])
    created_at = Column(DateTime, default=func.now())  # Date de création du cours
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Date de dernière mise à jour
