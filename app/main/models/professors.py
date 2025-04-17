from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime,Date,Boolean
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum

class Teacher(Base):
    __tablename__ = "teachers"

    uuid = Column(String, primary_key=True)
    matricule = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    grade = Column(String)  # Exemple : Chargé de cours
    status = Column(String, default="Actif")  # Actif/Inactif
    is_deleted = Column(Boolean,default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    
