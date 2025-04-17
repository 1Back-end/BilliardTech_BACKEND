from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime,Date,Boolean
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum

class Professor(Base):
    __tablename__ = "professors"
    
    uuid = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String)
    specialty_uuid = Column(String, ForeignKey("specialties.uuid",ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    
    specialty = relationship("Specialty", back_populates="professors")
