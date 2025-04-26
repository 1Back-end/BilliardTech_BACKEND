from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column, String, Text, Integer, DateTime, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.main.models.db.base_class import Base




class Teachertatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BLOCKED = "BLOCKED"


class Teacher(Base):
    __tablename__ = "teachers"

    # Identifiants
    uuid = Column(String, primary_key=True)
    matricule = Column(String, nullable=True)

    # Informations personnelles
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    phone_number_2 = Column(String, nullable=True)
    email = Column(String, unique=True)

    # Informations professionnelles
    grade = Column(String)  # Exemple : Chargé de cours
    status = Column(String, default=Teachertatus.ACTIVE)  # Actif / Inactif
    is_deleted = Column(Boolean, default=False)

    # Avatar (image de profil)
    avatar_uuid = Column(String, ForeignKey('storages.uuid', ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    avatar = relationship("Storage", foreign_keys=[avatar_uuid])

    added_by = Column(String, ForeignKey('users.uuid',ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    user = relationship("User", foreign_keys=[added_by])


    # Authentification et sécurité
    login = Column(String, nullable=True)  # Identifiant de connexion
    password_hash = Column(String, nullable=False)  # Mot de passe haché

    # Métadonnées
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
