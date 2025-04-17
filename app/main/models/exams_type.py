from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime,Date,Boolean
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum


class TypeOfExam(Base):
     
     __tablename__ = "type_of_examns"



     uuid = Column(String, primary_key=True,index=True)
     code = Column(String,nullable=False)
     name = Column(String, nullable=False)
     percentage = Column(String,nullable=False)
     added_by = Column(String, ForeignKey('users.uuid', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
     updated_by = Column(String, ForeignKey('users.uuid', ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
     user = relationship("User", foreign_keys=[added_by])
     updated_user = relationship("User", foreign_keys=[updated_by])
     created_at = Column(DateTime, default=func.now())  # Account creation timestamp
     is_deleted = Column(Boolean, default=False)
     updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Last update timestamp
